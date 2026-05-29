#!/usr/bin/env python3
"""_arm_common.py — shared infrastructure for Phase A.0 Arm A and Arm B runners.

NOT a CLI entry point. Import only.

Provides:
    AnthropicClient     thin SDK wrapper with cost accounting
    BudgetExceeded      raised when cumulative spend exceeds ceiling
    CostMeter           tracks cumulative spend, enforces ceiling
    ManifestReader      loads corpus/manifest.json, yields specimens
    ResultPersister     writes content-addressed JSON to results/raw/<arm>/
    ScoreRecord         typed value object from score-fixture.py output
    Scorer              calls score-fixture.py subprocess, parses ScoreRecord
    load_exemplars      deterministic exemplar sampler for K-sweep

Pricing (Opus 4.7 standard, 2026-05-28):
    Input:  $15.00 per MTok (million tokens)
    Output: $75.00 per MTok
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
import os
import random
import subprocess
import sys
from pathlib import Path
from typing import Generator, Sequence  # noqa: F401 — Sequence used by callers

# ---------------------------------------------------------------------------
# Pricing constants — Opus 4.7 standard pricing (USD per million tokens)
# ---------------------------------------------------------------------------
OPUS_INPUT_USD_PER_MTOK: float = 15.00
OPUS_OUTPUT_USD_PER_MTOK: float = 75.00

DEFAULT_MODEL: str = "claude-opus-4-7"
DEFAULT_TEMPERATURE: float = 0.0


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class BudgetExceeded(RuntimeError):
    """Raised when cumulative spend reaches the configured ceiling."""

    def __init__(self, spent: float, ceiling: float) -> None:
        self.spent = spent
        self.ceiling = ceiling
        super().__init__(
            f"BudgetExceeded: ${spent:.4f} spent >= ${ceiling:.2f} ceiling. "
            "Stop experiment; file AAR per DESIGN.md § 7."
        )


# ---------------------------------------------------------------------------
# Value objects
# ---------------------------------------------------------------------------

@dataclasses.dataclass(frozen=True)
class UsageRecord:
    """Token usage + cost from a single Anthropic completion."""
    input_tokens: int
    output_tokens: int
    cost_usd: float

    @classmethod
    def from_tokens(cls, input_tokens: int, output_tokens: int) -> "UsageRecord":
        cost = (
            input_tokens / 1_000_000 * OPUS_INPUT_USD_PER_MTOK
            + output_tokens / 1_000_000 * OPUS_OUTPUT_USD_PER_MTOK
        )
        return cls(input_tokens=input_tokens, output_tokens=output_tokens, cost_usd=cost)


@dataclasses.dataclass(frozen=True)
class CompletionResult:
    """Output of a single Anthropic API completion."""
    text: str
    usage: UsageRecord
    model: str
    stop_reason: str


@dataclasses.dataclass(frozen=True)
class SpecimenMeta:
    """One entry from the manifest corpus."""
    path: Path
    sha256: str
    stratum: str          # "A", "B", "C", or "held_out_A/B/C"
    marketplace_pass: bool
    marketplace_score: int
    held_out: bool

    @property
    def sha8(self) -> str:
        return self.sha256[:8]


@dataclasses.dataclass(frozen=True)
class ScoreRecord:
    """Parsed output of score-fixture.py (DESIGN.md § 4 dimensions)."""
    fixture_sha: str
    validator_version: str
    validator_commit: str
    marketplace_pass: bool
    marketplace_score_pct: int
    field_completeness: int
    deprecated_field_count: int
    security_finding_count: int
    is_extras_present: int

    def to_dict(self) -> dict:
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "ScoreRecord":
        tiers = d.get("tiers", {})
        mkt = tiers.get("marketplace", {})
        return cls(
            fixture_sha=d["fixture_sha"],
            validator_version=d.get("validator_version", "unknown"),
            validator_commit=d.get("validator_commit", "unknown"),
            marketplace_pass=mkt.get("pass", False),
            marketplace_score_pct=mkt.get("score_pct", 0),
            field_completeness=d.get("field_completeness", 0),
            deprecated_field_count=d.get("deprecated_field_count", 0),
            security_finding_count=d.get("security_finding_count", 0),
            is_extras_present=d.get("is_extras_present", 0),
        )

    def is_strict_improvement_over(self, baseline: "ScoreRecord") -> bool:
        """Arm B accept() predicate per DESIGN.md § 4.

        Returns True iff marketplace_score_pct is >= baseline AND no other
        dimension regresses AND at least one dimension strictly improves.

        Strict improvement on marketplace_pass (False -> True) counts as
        a strict improvement even if score_pct is unchanged.
        """
        # Any regression on any tracked dimension → reject
        if self.marketplace_score_pct < baseline.marketplace_score_pct:
            return False
        if self.field_completeness < baseline.field_completeness:
            return False
        if self.deprecated_field_count > baseline.deprecated_field_count:
            return False
        if self.security_finding_count > baseline.security_finding_count:
            return False
        # At least one dimension must strictly improve
        improved = (
            self.marketplace_score_pct > baseline.marketplace_score_pct
            or (not baseline.marketplace_pass and self.marketplace_pass)
            or self.field_completeness > baseline.field_completeness
            or self.deprecated_field_count < baseline.deprecated_field_count
        )
        return improved


# ---------------------------------------------------------------------------
# AnthropicClient
# ---------------------------------------------------------------------------

class AnthropicClient:
    """Thin wrapper around the Anthropic SDK's messages.create API.

    Raises EnvironmentError on import or missing key — fail fast, no silent
    fallback to empty responses.

    Parameters
    ----------
    model:
        Anthropic model ID. Default: claude-opus-4-7.
    temperature:
        Sampling temperature. DR-028 mandates 0.0 for replication.
    dry_run:
        When True, never calls the API; returns a synthetic response instead.
        Used by --dry-run CLI modes to validate the pipeline without spend.
    """

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        temperature: float = DEFAULT_TEMPERATURE,
        dry_run: bool = False,
    ) -> None:
        self.model = model
        self.temperature = temperature
        self.dry_run = dry_run
        self._client = None  # lazy-init so import doesn't error without key

    def _get_client(self):  # type: ignore[return]
        if self._client is not None:
            return self._client
        try:
            import anthropic  # type: ignore[import]
        except ImportError as exc:
            raise ImportError(
                "anthropic SDK not installed. Run: pip install anthropic"
            ) from exc
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            raise EnvironmentError(
                "ANTHROPIC_API_KEY is not set. Export the key before running arm scripts."
            )
        self._client = anthropic.Anthropic(api_key=api_key)
        return self._client

    def complete(
        self,
        prompt: str,
        max_tokens: int = 2048,
        *,
        model: str | None = None,
        temperature: float | None = None,
    ) -> CompletionResult:
        """Call the Anthropic messages API; return CompletionResult.

        In dry_run mode returns a synthetic result with realistic token
        estimates and zero actual API spend.

        Parameters
        ----------
        prompt:
            The full user-turn text.
        max_tokens:
            Hard cap on output tokens.
        model:
            Override instance model for this call.
        temperature:
            Override instance temperature for this call.
        """
        effective_model = model or self.model
        effective_temp = temperature if temperature is not None else self.temperature

        if self.dry_run:
            # Synthetic response: sniff the prompt to decide format.
            # Arm B propose prompts ask for JSON (schema_version arm-b-proposal/v1).
            # Arm A prompts ask for a frontmatter block.
            est_input = max(1, len(prompt) // 4)
            if "arm-b-proposal/v1" in prompt:
                # Arm B: return a valid JSON edit-proposal that adds the
                # "version" field (common gap in low-scoring fixtures).
                est_output = 120
                synthetic_text = json.dumps({
                    "schema_version": "arm-b-proposal/v1",
                    "rationale": (
                        "Dry-run synthetic proposal: adds version field if missing "
                        "to satisfy IS marketplace required set."
                    ),
                    "ops": [
                        {"op": "add", "field": "version", "value": "1.0.0"},
                    ],
                }, indent=2)
            else:
                # Arm A: return a plausible SKILL.md frontmatter block.
                est_output = 180
                synthetic_text = (
                    "---\n"
                    "name: example-skill\n"
                    "description: 'A placeholder response generated in dry-run mode.'\n"
                    "allowed-tools: Read, Write, Edit, Bash\n"
                    "version: 1.0.0\n"
                    "author: Jeremy Longshore <jeremy@intentsolutions.io>\n"
                    "license: Apache-2.0\n"
                    "compatibility: Designed for Claude Code\n"
                    "tags:\n"
                    "- example\n"
                    "- dry-run\n"
                    "---\n"
                )
            usage = UsageRecord.from_tokens(est_input, est_output)
            return CompletionResult(
                text=synthetic_text,
                usage=usage,
                model=effective_model,
                stop_reason="end_turn",
            )

        client = self._get_client()
        message = client.messages.create(
            model=effective_model,
            max_tokens=max_tokens,
            temperature=effective_temp,
            messages=[{"role": "user", "content": prompt}],
        )
        text = "".join(
            block.text
            for block in message.content
            if hasattr(block, "text")
        )
        usage = UsageRecord.from_tokens(
            input_tokens=message.usage.input_tokens,
            output_tokens=message.usage.output_tokens,
        )
        return CompletionResult(
            text=text,
            usage=usage,
            model=effective_model,
            stop_reason=str(message.stop_reason),
        )


# ---------------------------------------------------------------------------
# CostMeter
# ---------------------------------------------------------------------------

class CostMeter:
    """Track cumulative spend and enforce the budget ceiling.

    Parameters
    ----------
    ceiling_usd:
        Hard ceiling per DESIGN.md § 7. Raises BudgetExceeded when exceeded.
    """

    def __init__(self, ceiling_usd: float) -> None:
        self.ceiling_usd = ceiling_usd
        self._spent_usd: float = 0.0
        self._calls: int = 0

    @property
    def spent_usd(self) -> float:
        return self._spent_usd

    @property
    def calls(self) -> int:
        return self._calls

    def record(self, usage: UsageRecord) -> None:
        """Add usage to the meter; raise BudgetExceeded if ceiling crossed."""
        self._spent_usd += usage.cost_usd
        self._calls += 1
        if self._spent_usd >= self.ceiling_usd:
            raise BudgetExceeded(spent=self._spent_usd, ceiling=self.ceiling_usd)

    def remaining_usd(self) -> float:
        return max(0.0, self.ceiling_usd - self._spent_usd)

    def summary(self) -> dict:
        return {
            "spent_usd": round(self._spent_usd, 6),
            "ceiling_usd": self.ceiling_usd,
            "remaining_usd": round(self.remaining_usd(), 6),
            "api_calls": self._calls,
        }


# ---------------------------------------------------------------------------
# ManifestReader
# ---------------------------------------------------------------------------

class ManifestReader:
    """Load corpus/manifest.json; yield SpecimenMeta for requested strata.

    Parameters
    ----------
    manifest_path:
        Path to manifest.json (pre-registered per DESIGN.md § 6).
    include_held_out:
        Whether to yield held-out specimens. Default False (main corpus only).
    """

    def __init__(self, manifest_path: Path, include_held_out: bool = False) -> None:
        raw = json.loads(manifest_path.read_text(encoding="utf-8"))
        self._pre_registration = raw.get("pre_registration", {})
        self._strata: dict[str, list[dict]] = raw.get("strata", {})
        self._held_out_strata: dict[str, list[dict]] = raw.get("held_out", {})
        self._include_held_out = include_held_out

    @property
    def seed(self) -> int:
        return int(self._pre_registration.get("seed", 42))

    @property
    def validator_commit(self) -> str:
        return str(self._pre_registration.get("validator_commit", "unknown"))

    def specimens(self) -> Generator[SpecimenMeta, None, None]:
        """Yield all non-held-out specimens in stratum order."""
        for stratum_key, items in self._strata.items():
            for item in items:
                yield SpecimenMeta(
                    path=Path(item["path"]),
                    sha256=item["sha256"],
                    stratum=stratum_key,
                    marketplace_pass=item.get("marketplace_pass", False),
                    marketplace_score=item.get("marketplace_score", 0),
                    held_out=False,
                )
        if self._include_held_out:
            for stratum_key, items in self._held_out_strata.items():
                for item in items:
                    yield SpecimenMeta(
                        path=Path(item["path"]),
                        sha256=item["sha256"],
                        stratum=f"held_out_{stratum_key}",
                        marketplace_pass=item.get("marketplace_pass", False),
                        marketplace_score=item.get("marketplace_score", 0),
                        held_out=True,
                    )

    def all_specimen_shas(self) -> list[str]:
        """Return SHAs for all main-corpus specimens (used for exclude sets)."""
        return [s.sha256 for s in self.specimens()]


# ---------------------------------------------------------------------------
# ResultPersister
# ---------------------------------------------------------------------------

class ResultPersister:
    """Write content-addressed result files to results/raw/<arm>/<sha8>/.

    The directory layout follows DESIGN.md § 6:
        results/raw/<arm>/<sha8>/
            prompt.json
            response.json
            score.json

    Files are written atomically (write-then-rename where pathlib allows).
    Existing files are NOT overwritten unless force=True — idempotency for
    resume-on-failure.
    """

    def __init__(self, out_dir: Path, arm: str, force: bool = False) -> None:
        self.out_dir = out_dir
        self.arm = arm
        self.force = force
        (out_dir / arm).mkdir(parents=True, exist_ok=True)

    def _slot_dir(self, sha: str, sub: str = "") -> Path:
        """Return (and create) the per-specimen slot directory.

        sub: optional subdirectory within the slot (e.g. "k=3")
        """
        d = self.out_dir / self.arm / sha[:8]
        if sub:
            d = d / sub
        d.mkdir(parents=True, exist_ok=True)
        return d

    def exists(self, sha: str, filename: str, sub: str = "") -> bool:
        return (self._slot_dir(sha, sub) / filename).exists()

    def write_json(self, sha: str, filename: str, data: dict, sub: str = "") -> Path:
        """Write data as JSON to slot_dir/filename. Returns the path."""
        target = self._slot_dir(sha, sub) / filename
        if target.exists() and not self.force:
            return target
        target.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return target

    def write_text(self, sha: str, filename: str, text: str, sub: str = "") -> Path:
        """Write raw text to slot_dir/filename. Returns the path."""
        target = self._slot_dir(sha, sub) / filename
        if target.exists() and not self.force:
            return target
        target.write_text(text, encoding="utf-8")
        return target

    def log_error(self, sha: str, error: str, context: dict | None = None) -> None:
        """Append an error record to the arm-level errors.jsonl file."""
        import datetime as dt
        error_file = self.out_dir / self.arm / "errors.jsonl"
        record = {
            "sha8": sha[:8],
            "error": error,
            "context": context or {},
            "timestamp": dt.datetime.now(dt.UTC).isoformat(),
        }
        with error_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")


# ---------------------------------------------------------------------------
# Scorer
# ---------------------------------------------------------------------------

class Scorer:
    """Call score-fixture.py subprocess on a SKILL.md path.

    Parameters
    ----------
    score_script:
        Absolute path to score-fixture.py. Defaults to the canonical location
        inside the phase-a-0-baseline/scripts/ directory.
    validator_path:
        Path passed as --validator-path to score-fixture.py.
    validator_commit:
        Pinned commit SHA for SCHEMA 3.7.0 (post-D4).
    """

    def __init__(
        self,
        score_script: Path | None = None,
        validator_path: Path | None = None,
        validator_commit: str = "7b9eb8f",
    ) -> None:
        if score_script is None:
            here = Path(__file__).resolve().parent
            score_script = here / "score-fixture.py"
        self.score_script = score_script
        self.validator_path = validator_path
        self.validator_commit = validator_commit

    def score_file(self, skill_md_path: Path) -> ScoreRecord:
        """Run score-fixture.py on skill_md_path; return parsed ScoreRecord.

        Raises RuntimeError if the subprocess exits non-zero.
        """
        cmd = ["python3", str(self.score_script), str(skill_md_path),
               "--commit", self.validator_commit]
        if self.validator_path:
            cmd += ["--validator-path", str(self.validator_path)]

        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            raise RuntimeError(
                f"score-fixture.py exited {result.returncode} on {skill_md_path}: "
                f"{result.stderr[:300]}"
            )
        try:
            raw = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"score-fixture.py produced invalid JSON for {skill_md_path}: {exc}"
            ) from exc
        return ScoreRecord.from_dict(raw)

    def score_text(self, skill_md_text: str, tmp_dir: Path) -> ScoreRecord:
        """Score an in-memory SKILL.md string by writing to a temp file.

        tmp_dir must be a writable directory that persists for the call duration.
        The temp file is named by SHA8 of the content to avoid collisions.
        """
        sha8 = hashlib.sha256(skill_md_text.encode()).hexdigest()[:8]
        tmp_path = tmp_dir / f"_score_tmp_{sha8}.md"
        tmp_path.write_text(skill_md_text, encoding="utf-8")
        try:
            return self.score_file(tmp_path)
        finally:
            tmp_path.unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# load_exemplars
# ---------------------------------------------------------------------------

def load_exemplars(
    manifest: ManifestReader,
    k: int,
    seed: int = 42,
    exclude: set[str] | None = None,
) -> list[SpecimenMeta]:
    """Return a deterministic sample of k exemplars from the main corpus.

    Only specimens with marketplace_pass=True are eligible exemplars (they
    must demonstrate what a passing frontmatter looks like).

    Parameters
    ----------
    manifest:
        Loaded ManifestReader instance.
    k:
        Number of exemplars to return. 0 returns [].
    seed:
        RNG seed. Use manifest.seed for pre-registered reproducibility.
    exclude:
        Set of sha256 values to exclude (e.g. the current evaluation specimen).
    """
    if k == 0:
        return []

    exclude = exclude or set()
    eligible = [
        s for s in manifest.specimens()
        if s.marketplace_pass and s.sha256 not in exclude
    ]
    if len(eligible) < k:
        raise ValueError(
            f"load_exemplars: requested k={k} but only {len(eligible)} eligible "
            f"passing specimens available (after excluding {len(exclude)})."
        )
    rng = random.Random(seed)
    return rng.sample(eligible, k)


# ---------------------------------------------------------------------------
# Prompt helpers
# ---------------------------------------------------------------------------

def extract_frontmatter(skill_md_text: str) -> str:
    """Return only the YAML frontmatter block (with delimiters) or full text."""
    if not skill_md_text.startswith("---"):
        return skill_md_text
    end = skill_md_text.find("\n---", 4)
    if end == -1:
        return skill_md_text
    return skill_md_text[: end + 4]  # include closing ---


def build_arm_a_prompt(
    input_skill_text: str,
    exemplars: list[SpecimenMeta],
) -> str:
    """Build the Arm A naive-Opus prompt per DESIGN.md § 3 Arm A template.

    Parameters
    ----------
    input_skill_text:
        Full text of the SKILL.md being improved.
    exemplars:
        List of passing SpecimenMeta. Their SKILL.md files are read from disk
        and truncated to frontmatter only.
    """
    k = len(exemplars)
    exemplar_lines: list[str] = []
    for i, ex in enumerate(exemplars, 1):
        try:
            ex_text = ex.path.read_text(encoding="utf-8", errors="replace")
            fm = extract_frontmatter(ex_text)
        except OSError:
            fm = f"(exemplar {i}: file not readable)"
        exemplar_lines.append(f"<exemplar {i}>\n{fm}\n</exemplar {i}>")

    exemplar_block = "\n\n".join(exemplar_lines) if exemplar_lines else ""

    input_fm = extract_frontmatter(input_skill_text)

    if k == 0:
        exemplar_section = "(No exemplars provided for K=0 baseline.)"
    else:
        exemplar_section = (
            f"Here are {k} exemplar(s) of SKILL.md frontmatter that pass the IS "
            f"marketplace validator:\n\n{exemplar_block}"
        )

    prompt = (
        "You are improving a SKILL.md frontmatter file for the Intent Solutions "
        "marketplace tier. The IS marketplace tier requires 8 fields: name, "
        "description, allowed-tools, version, author, license, compatibility, tags. "
        "disallowed-tools is recognized (SCHEMA 3.7.0).\n\n"
        f"{exemplar_section}\n\n"
        "Now improve the following SKILL.md to maximize its IS-marketplace-tier "
        "validator score. Return ONLY the updated frontmatter block (from --- to ---). "
        "Do not include any explanation or prose outside the frontmatter delimiters.\n\n"
        f"<input>\n{input_fm}\n</input>"
    )
    return prompt
