#!/usr/bin/env python3
"""run-arm-b.py — Proposed Refiner mechanism arm (alternative hypothesis, Arm B).

Phase A.0 baseline experiment per DESIGN.md § 3 Arm B.

Implements the Refiner loop per Plan 027 § 4 Phase A + § 14 SAK § 14.4:
    1. propose(input, scored_rollouts) -> EditProposal (bounded add/del/replace ops)
    2. apply(input, EditProposal)      -> SkillDocV2  (pure function, no API call)
    3. score(SkillDocV2)               -> ScoreRecord (local subprocess)
    4. accept(score_v1, score_v2)      -> bool        (strict improvement, no regression)
    5. If reject and iteration < max_iterations: re-propose with rationale in context
    6. Emit final accepted SkillDocV2 (or v1 if all iterations rejected)

Per-specimen persistence layout (DESIGN.md § 6):
    results/raw/arm-b/<sha8>/
        proposal-0.json    # Opus JSON edit-proposal, iteration 0
        applied-0.md       # SKILL.md after applying proposal-0
        score-0.json       # ScoreRecord for applied-0
        accept-0.json      # {accepted: bool, rationale: str}
        proposal-1.json    # (if iteration 1 triggered)
        ...
        final.md           # last accepted (or original if all rejected)
        trajectory.json    # per-iteration summary

Emits results/raw/arm-b/_summary.json: mean per-specimen score delta, accept
rate, mean iterations to accept, rejected-buffer aggregate.

---

EDIT-PROPOSAL JSON SCHEMA (the Arm B structural contract):

Opus is asked to respond with a JSON object matching this schema (strictly
validated before apply()):

{
  "schema_version": "arm-b-proposal/v1",
  "rationale": "<string: 1-3 sentence explanation of what changed and why>",
  "ops": [
    {
      "op": "add",
      "field": "<yaml-key>",
      "value": "<scalar string or YAML-serialized value>"
    },
    {
      "op": "del",
      "field": "<yaml-key>"
    },
    {
      "op": "replace",
      "field": "<yaml-key>",
      "value": "<new scalar string or YAML-serialized value>"
    }
  ]
}

Constraints:
- ops[] is an ordered list; applies top-to-bottom.
- Each op targets a single top-level frontmatter field (no nested key paths).
- "add" is used for fields that do not exist in the input frontmatter.
- "del" is used for deprecated or invalid fields (e.g. "compatible-with").
- "replace" is used for fields that exist and need updating.
- ops[] length is bounded: 1..8 ops per proposal (enforced in validation).
- "value" for list-type fields (allowed-tools, tags) uses YAML list syntax:
    ["Read", "Write"]   (JSON array encoded as JSON string is also accepted)
- Empty ops[] is invalid (Opus must propose at least one change).
- schema_version must be exactly "arm-b-proposal/v1".

Why bounded ops instead of full-frontmatter rewrite (contrast to Arm A):
    The Refiner mechanism's core claim is that bounded, justified edits with
    a strict-improvement acceptance gate produce more reliable lift than
    unconstrained full-frontmatter replacement. Bounded ops make the delta
    auditable; the rationale field makes it explainable. This is what we are
    testing against the Arm A naive rewrite baseline.

Usage:
    run-arm-b.py --manifest <path> --out <dir> \\
                 --budget-ceiling-usd 200 \\
                 [--max-iterations 3] \\
                 [--dry-run] [--force] [--limit N]

--dry-run: simulates propose/apply/score/accept on each specimen with
           synthetic Opus responses. Zero API spend. Validates pipeline.
--limit N: process only the first N specimens (smoke test).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _arm_common import (
    AnthropicClient,
    BudgetExceeded,
    CostMeter,
    ManifestReader,
    ResultPersister,
    ScoreRecord,
    Scorer,
    SpecimenMeta,
    extract_frontmatter,
)

ARM_NAME = "arm-b"

# Constraint: maximum edit ops per proposal (enforced in _validate_proposal)
MAX_OPS = 8
MIN_OPS = 1

# Arm B uses no K exemplars — Refiner uses the input + rejection history only
# (contrast to Arm A which uses in-context exemplars)


# ---------------------------------------------------------------------------
# EditProposal types
# ---------------------------------------------------------------------------

from dataclasses import dataclass, field as dc_field


@dataclass
class EditOp:
    op: str          # "add" | "del" | "replace"
    field: str       # top-level YAML key
    value: str = ""  # for "add" / "replace"; unused for "del"


@dataclass
class EditProposal:
    schema_version: str
    rationale: str
    ops: list[EditOp]


def _validate_proposal(raw: dict) -> tuple[EditProposal, str | None]:
    """Parse + validate a raw dict as an EditProposal.

    Returns (proposal, None) on success; (None, error_message) on failure.
    """
    if not isinstance(raw, dict):
        return None, "Response is not a JSON object"  # type: ignore[return-value]

    sv = raw.get("schema_version", "")
    if sv != "arm-b-proposal/v1":
        return None, f"schema_version must be 'arm-b-proposal/v1', got {sv!r}"

    rationale = raw.get("rationale", "")
    if not isinstance(rationale, str) or not rationale.strip():
        return None, "rationale must be a non-empty string"

    ops_raw = raw.get("ops", [])
    if not isinstance(ops_raw, list):
        return None, "ops must be a list"
    if not (MIN_OPS <= len(ops_raw) <= MAX_OPS):
        return None, f"ops length must be {MIN_OPS}..{MAX_OPS}, got {len(ops_raw)}"

    valid_ops = {"add", "del", "replace"}
    ops: list[EditOp] = []
    for i, op_raw in enumerate(ops_raw):
        if not isinstance(op_raw, dict):
            return None, f"ops[{i}] must be a dict"
        op_kind = op_raw.get("op", "")
        if op_kind not in valid_ops:
            return None, f"ops[{i}].op must be one of {valid_ops}, got {op_kind!r}"
        field_name = op_raw.get("field", "")
        if not isinstance(field_name, str) or not field_name.strip():
            return None, f"ops[{i}].field must be a non-empty string"
        # field must not contain path separators (top-level only)
        if "." in field_name or "/" in field_name:
            return None, f"ops[{i}].field must be a top-level key, no dots/slashes"
        value = ""
        if op_kind in ("add", "replace"):
            value = op_raw.get("value", "")
            if not isinstance(value, (str, list)):
                return None, f"ops[{i}].value must be a string or list"
            if isinstance(value, list):
                value = json.dumps(value)  # normalize to JSON string representation
        ops.append(EditOp(op=op_kind, field=field_name, value=str(value)))

    return EditProposal(schema_version=sv, rationale=rationale, ops=ops), None


# ---------------------------------------------------------------------------
# Frontmatter apply() — pure function
# ---------------------------------------------------------------------------

def _parse_frontmatter_lines(skill_md_text: str) -> tuple[list[str], str]:
    """Split a SKILL.md into (frontmatter_lines, body_text).

    frontmatter_lines: lines between first --- and closing ---, NOT including delimiters
    body_text: everything after the closing ---\\n
    """
    if not skill_md_text.startswith("---"):
        return [], skill_md_text
    rest = skill_md_text[3:]
    end_idx = rest.find("\n---")
    if end_idx == -1:
        return rest.splitlines(), ""
    fm_block = rest[:end_idx]
    body = rest[end_idx + 4:]  # skip \n---
    return fm_block.splitlines(), body


def _lines_to_text(fm_lines: list[str], body: str) -> str:
    return "---\n" + "\n".join(fm_lines) + "\n---" + body


def apply_proposal(input_text: str, proposal: EditProposal) -> str:
    """Apply EditProposal ops to input_text; return new SKILL.md text.

    Pure function — no API calls, no filesystem side-effects.

    Each op targets a top-level frontmatter field. Multi-line YAML values
    (e.g. block scalars, lists) are handled by treating the field's existing
    block as everything from the field's key line until the next top-level key.
    """
    fm_lines, body = _parse_frontmatter_lines(input_text)

    # Build a list of (start_lineno, end_lineno_exclusive, key) tuples for top-level keys
    # so we can replace/delete existing fields cleanly.
    def find_field_range(lines: list[str], key: str) -> tuple[int, int] | None:
        pattern = re.compile(r"^" + re.escape(key) + r"\s*:")
        start = None
        for i, line in enumerate(lines):
            if pattern.match(line):
                start = i
                break
        if start is None:
            return None
        # End is the next line that matches a top-level key pattern (no indent)
        top_key_re = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*\s*:")
        end = start + 1
        while end < len(lines):
            if top_key_re.match(lines[end]):
                break
            end += 1
        return start, end

    for op in proposal.ops:
        if op.op == "del":
            r = find_field_range(fm_lines, op.field)
            if r is not None:
                fm_lines = fm_lines[: r[0]] + fm_lines[r[1] :]
        elif op.op == "replace":
            r = find_field_range(fm_lines, op.field)
            new_line = f"{op.field}: {_format_value(op.value)}"
            if r is not None:
                fm_lines = fm_lines[: r[0]] + [new_line] + fm_lines[r[1] :]
            else:
                # Field doesn't exist: treat as add
                fm_lines.append(new_line)
        elif op.op == "add":
            # Only add if field doesn't already exist (idempotent)
            r = find_field_range(fm_lines, op.field)
            if r is None:
                new_line = f"{op.field}: {_format_value(op.value)}"
                fm_lines.append(new_line)

    return _lines_to_text(fm_lines, body)


def _format_value(value: str) -> str:
    """Heuristic: if value looks like a JSON array, expand to YAML list lines."""
    v = value.strip()
    try:
        parsed = json.loads(v)
        if isinstance(parsed, list):
            items = "\n".join(f"- {item}" for item in parsed)
            return "\n" + items
    except (json.JSONDecodeError, ValueError):
        pass
    return value


# ---------------------------------------------------------------------------
# Prompt builders
# ---------------------------------------------------------------------------

def build_propose_prompt(
    input_text: str,
    iteration: int,
    rejection_history: list[dict],
) -> str:
    """Build the proposal prompt for the Refiner mechanism.

    On iteration 0: just the input SKILL.md + instructions.
    On iteration N>0: includes the rejection rationale from prior iterations
    so Opus can re-propose with context.
    """
    input_fm = extract_frontmatter(input_text)

    rejection_section = ""
    if rejection_history:
        lines = ["Prior proposals were rejected for the following reasons:"]
        for i, entry in enumerate(rejection_history):
            lines.append(
                f"\nIteration {i} rejection:\n"
                f"  Proposal rationale: {entry.get('proposal_rationale', '(none)')}\n"
                f"  Rejection reason:   {entry.get('rejection_reason', '(unknown)')}"
            )
        rejection_section = "\n".join(lines) + "\n\n"

    schema_desc = """\
Respond with ONLY a valid JSON object matching this exact schema (no prose outside it):

{
  "schema_version": "arm-b-proposal/v1",
  "rationale": "<1-3 sentences: what you changed and why>",
  "ops": [
    { "op": "add",     "field": "<yaml-key>", "value": "<new value>" },
    { "op": "del",     "field": "<yaml-key>" },
    { "op": "replace", "field": "<yaml-key>", "value": "<new value>" }
  ]
}

Rules:
- ops[] must have 1..8 entries.
- Each op targets ONE top-level frontmatter field only (no nested keys).
- Use "add" for fields missing from input. Use "del" for deprecated fields
  (e.g. "compatible-with"). Use "replace" for fields needing update.
- For list fields (allowed-tools, tags), encode value as a JSON array string
  e.g. ["Read", "Write", "Edit"].
- The 8 IS marketplace required fields are: name, description, allowed-tools,
  version, author, license, compatibility, tags.
- "disallowed-tools" is a recognized optional field (SCHEMA 3.7.0).
- Deprecated field: "compatible-with" — del it if present.
"""

    prompt = (
        "You are the Skill Refiner. Your task is to propose minimal, bounded "
        "edits to a SKILL.md frontmatter to improve its IS marketplace-tier "
        "validator score. You do NOT rewrite the whole frontmatter; you emit "
        "a structured JSON edit-proposal specifying only what to change.\n\n"
        f"{rejection_section}"
        f"{schema_desc}\n"
        "Input SKILL.md frontmatter to improve:\n\n"
        f"<input>\n{input_fm}\n</input>"
    )
    return prompt


# ---------------------------------------------------------------------------
# Core Refiner loop
# ---------------------------------------------------------------------------

def run_refiner(
    specimen: SpecimenMeta,
    input_text: str,
    client: AnthropicClient,
    meter: CostMeter,
    persister: ResultPersister,
    scorer: Scorer,
    tmp_dir: Path,
    max_iterations: int,
    dry_run: bool,
    force: bool,
) -> dict:
    """Execute the propose/apply/score/accept loop for one specimen.

    Returns a trajectory dict summarising all iterations.
    """
    sha = specimen.sha256

    # Score the input baseline
    try:
        score_v1 = scorer.score_text(input_text, tmp_dir)
    except Exception as exc:
        return {
            "sha8": specimen.sha8,
            "error": f"baseline scoring failed: {exc}",
            "accepted": False,
            "iterations": 0,
        }

    rejection_history: list[dict] = []
    best_text = input_text
    best_score = score_v1
    accepted = False
    iterations_to_accept: int | None = None
    trajectory: list[dict] = []

    for iteration in range(max_iterations):
        prompt = build_propose_prompt(input_text, iteration, rejection_history)

        if dry_run and iteration == 0:
            prompt_preview = prompt[:400].replace("\n", " ")
            print(
                f"  [dry-run] propose iteration={iteration} "
                f"specimen={specimen.sha8}"
            )
            print(f"    prompt[:400]: {prompt_preview!r}")

        # Call Opus for a proposal
        try:
            completion = client.complete(prompt, max_tokens=1024)
            meter.record(completion.usage)
        except BudgetExceeded:
            raise
        except Exception as exc:
            persister.log_error(
                sha, f"API call failed at iteration {iteration}: {exc}", {"iteration": iteration}
            )
            break

        # Parse the JSON proposal from the response
        raw_proposal: dict | None = None
        parse_error: str | None = None
        try:
            # Extract JSON from response (may be wrapped in markdown code block)
            text = completion.text.strip()
            json_match = re.search(r"```(?:json)?\s*([\s\S]+?)\s*```", text)
            if json_match:
                text = json_match.group(1)
            raw_proposal = json.loads(text)
        except json.JSONDecodeError as exc:
            parse_error = f"JSON decode error: {exc}"

        proposal_obj: EditProposal | None = None
        if raw_proposal is not None:
            proposal_obj, parse_error = _validate_proposal(raw_proposal)

        if dry_run:
            if parse_error:
                print(f"    proposal parse error: {parse_error}")
            else:
                print(
                    f"    proposal: {len(proposal_obj.ops)} ops — "
                    f"{[o.op + ':' + o.field for o in proposal_obj.ops]}"
                )

        # Persist proposal
        proposal_data = {
            "iteration": iteration,
            "prompt": prompt,
            "response_text": completion.text,
            "raw_proposal": raw_proposal,
            "parse_error": parse_error,
            "input_tokens": completion.usage.input_tokens,
            "output_tokens": completion.usage.output_tokens,
            "cost_usd": completion.usage.cost_usd,
            "dry_run": dry_run,
        }
        persister.write_json(sha, f"proposal-{iteration}.json", proposal_data)

        if proposal_obj is None:
            rejection_reason = f"Invalid proposal: {parse_error}"
            rejection_history.append({
                "proposal_rationale": "(unparseable)",
                "rejection_reason": rejection_reason,
            })
            accept_data = {
                "iteration": iteration,
                "accepted": False,
                "rejection_reason": rejection_reason,
            }
            persister.write_json(sha, f"accept-{iteration}.json", accept_data)
            trajectory.append({"iteration": iteration, "accepted": False,
                                "reason": rejection_reason})
            continue

        # Apply proposal
        try:
            candidate_text = apply_proposal(input_text, proposal_obj)
        except Exception as exc:
            rejection_reason = f"apply() raised: {exc}"
            rejection_history.append({
                "proposal_rationale": proposal_obj.rationale,
                "rejection_reason": rejection_reason,
            })
            persister.write_json(sha, f"accept-{iteration}.json",
                                 {"iteration": iteration, "accepted": False,
                                  "rejection_reason": rejection_reason})
            trajectory.append({"iteration": iteration, "accepted": False, "reason": rejection_reason})
            continue

        persister.write_text(sha, f"applied-{iteration}.md", candidate_text)

        # Score candidate
        try:
            score_v2 = scorer.score_text(candidate_text, tmp_dir)
        except Exception as exc:
            rejection_reason = f"score() raised: {exc}"
            rejection_history.append({
                "proposal_rationale": proposal_obj.rationale,
                "rejection_reason": rejection_reason,
            })
            persister.write_json(sha, f"score-{iteration}.json", {"error": str(exc)})
            persister.write_json(sha, f"accept-{iteration}.json",
                                 {"iteration": iteration, "accepted": False,
                                  "rejection_reason": rejection_reason})
            trajectory.append({"iteration": iteration, "accepted": False, "reason": rejection_reason})
            continue

        score_data = score_v2.to_dict()
        score_data["baseline_marketplace_score_pct"] = score_v1.marketplace_score_pct
        score_data["delta_marketplace_score_pct"] = (
            score_v2.marketplace_score_pct - score_v1.marketplace_score_pct
        )
        persister.write_json(sha, f"score-{iteration}.json", score_data)

        if dry_run:
            print(
                f"    score: baseline={score_v1.marketplace_score_pct} "
                f"candidate={score_v2.marketplace_score_pct} "
                f"delta={score_data['delta_marketplace_score_pct']:+d}"
            )

        # Acceptance gate (DESIGN.md § 4)
        is_accepted = score_v2.is_strict_improvement_over(score_v1)
        if not is_accepted:
            dims = []
            if score_v2.marketplace_score_pct < score_v1.marketplace_score_pct:
                dims.append("marketplace_score_pct regressed")
            if score_v2.field_completeness < score_v1.field_completeness:
                dims.append("field_completeness regressed")
            if score_v2.deprecated_field_count > score_v1.deprecated_field_count:
                dims.append("deprecated_field_count increased")
            if score_v2.security_finding_count > score_v1.security_finding_count:
                dims.append("security_finding_count increased")
            if not dims:
                dims.append("no dimension strictly improved")
            rejection_reason = "; ".join(dims)
        else:
            rejection_reason = ""

        accept_data = {
            "iteration": iteration,
            "accepted": is_accepted,
            "rejection_reason": rejection_reason if not is_accepted else None,
            "score_v1_marketplace_score_pct": score_v1.marketplace_score_pct,
            "score_v2_marketplace_score_pct": score_v2.marketplace_score_pct,
            "delta": score_data["delta_marketplace_score_pct"],
        }
        persister.write_json(sha, f"accept-{iteration}.json", accept_data)
        trajectory.append({
            "iteration": iteration,
            "accepted": is_accepted,
            "delta": score_data["delta_marketplace_score_pct"],
            "reason": rejection_reason if not is_accepted else "accepted",
        })

        if dry_run:
            print(f"    accept: {is_accepted}" + (f" — {rejection_reason}" if not is_accepted else ""))

        if is_accepted:
            best_text = candidate_text
            best_score = score_v2
            accepted = True
            iterations_to_accept = iteration
            break
        else:
            rejection_history.append({
                "proposal_rationale": proposal_obj.rationale,
                "rejection_reason": rejection_reason,
            })

    # Write final.md (best accepted or original if all rejected)
    persister.write_text(sha, "final.md", best_text)

    result = {
        "sha8": specimen.sha8,
        "stratum": specimen.stratum,
        "accepted": accepted,
        "iterations_to_accept": iterations_to_accept,
        "baseline_marketplace_score_pct": score_v1.marketplace_score_pct,
        "final_marketplace_score_pct": best_score.marketplace_score_pct,
        "delta_marketplace_score_pct": (
            best_score.marketplace_score_pct - score_v1.marketplace_score_pct
        ),
        "trajectory": trajectory,
    }
    persister.write_json(sha, "trajectory.json", result)
    return result


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

def write_summary(
    out_dir: Path,
    all_results: list[dict],
    meter: CostMeter,
    dry_run: bool,
) -> Path:
    """Emit _summary.json per DESIGN.md § 3 Arm B."""
    import statistics as _stats

    accepted_results = [r for r in all_results if r.get("accepted")]
    rejected_results = [r for r in all_results if not r.get("accepted") and "error" not in r]
    error_results = [r for r in all_results if "error" in r]

    deltas = [r["delta_marketplace_score_pct"] for r in all_results
              if "delta_marketplace_score_pct" in r]
    iters_list = [r["iterations_to_accept"] for r in accepted_results
                  if r.get("iterations_to_accept") is not None]

    def safe_mean(lst: list) -> float | None:
        return round(_stats.mean(lst), 3) if lst else None

    def safe_std(lst: list) -> float | None:
        return round(_stats.stdev(lst), 3) if len(lst) > 1 else (0.0 if len(lst) == 1 else None)

    summary = {
        "arm": ARM_NAME,
        "generated_at": dt.datetime.now(dt.UTC).isoformat(),
        "dry_run": dry_run,
        "cost_meter": meter.summary(),
        "total_specimens": len(all_results),
        "accepted_count": len(accepted_results),
        "rejected_all_iterations_count": len(rejected_results),
        "error_count": len(error_results),
        "accept_rate": (
            round(len(accepted_results) / len(all_results), 3)
            if all_results else None
        ),
        "mean_delta_marketplace_score_pct": safe_mean(deltas),
        "std_delta_marketplace_score_pct": safe_std(deltas),
        "mean_iterations_to_accept": safe_mean(iters_list),
        "rejected_buffer_aggregate": {
            "count": len(rejected_results),
            "sha8s": [r["sha8"] for r in rejected_results],
        },
        "per_specimen_results": all_results,
    }

    path = out_dir / ARM_NAME / "_summary.json"
    path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(
        description="Run Arm B (proposed Refiner mechanism) of Phase A.0 baseline experiment."
    )
    ap.add_argument("--manifest", type=Path, required=True,
                    help="Path to corpus/manifest.json")
    ap.add_argument("--out", type=Path, required=True,
                    help="Root output directory (results/raw/)")
    ap.add_argument("--budget-ceiling-usd", type=float, default=200.0,
                    help="Hard cost ceiling USD. Default: 200")
    ap.add_argument("--max-iterations", type=int, default=3,
                    help="Maximum Refiner propose/reject iterations per specimen. Default: 3")
    ap.add_argument("--dry-run", action="store_true",
                    help="Simulate pipeline without real API calls. Validates end-to-end.")
    ap.add_argument("--force", action="store_true",
                    help="Overwrite existing result files.")
    ap.add_argument("--limit", type=int, default=None,
                    help="Process only first N specimens (smoke test).")
    ap.add_argument("--validator-path", type=Path, default=None,
                    help="Override path to validate-skills-schema.py")
    args = ap.parse_args()

    if not args.manifest.is_file():
        print(f"ERROR: manifest not found: {args.manifest}", file=sys.stderr)
        return 2

    args.out.mkdir(parents=True, exist_ok=True)

    manifest = ManifestReader(args.manifest)
    specimens = list(manifest.specimens())
    if args.limit:
        specimens = specimens[: args.limit]

    meter = CostMeter(ceiling_usd=args.budget_ceiling_usd)
    client = AnthropicClient(dry_run=args.dry_run)
    persister = ResultPersister(args.out, ARM_NAME, force=args.force)
    scorer = Scorer(validator_path=args.validator_path)

    all_results: list[dict] = []

    print(
        f"[arm-b] specimens={len(specimens)} max_iterations={args.max_iterations} "
        f"ceiling=${args.budget_ceiling_usd:.0f} dry_run={args.dry_run}"
    )

    with tempfile.TemporaryDirectory(prefix="arm_b_score_") as tmp_str:
        tmp_dir = Path(tmp_str)

        try:
            for specimen in specimens:
                # Check idempotency: if trajectory.json exists, skip
                if (
                    persister.exists(specimen.sha256, "trajectory.json")
                    and not args.force
                ):
                    print(f"  skip (idempotent): {specimen.sha8}")
                    # Load and include in results for summary
                    traj_path = (
                        args.out / ARM_NAME / specimen.sha8 / "trajectory.json"
                    )
                    try:
                        traj = json.loads(traj_path.read_text())
                        all_results.append(traj)
                    except Exception:
                        pass
                    continue

                try:
                    input_text = specimen.path.read_text(encoding="utf-8", errors="replace")
                except OSError as exc:
                    persister.log_error(specimen.sha256, f"Cannot read specimen: {exc}")
                    all_results.append({"sha8": specimen.sha8, "error": str(exc)})
                    continue

                if args.dry_run:
                    print(f"\n[dry-run] specimen={specimen.sha8} stratum={specimen.stratum} "
                          f"baseline={specimen.marketplace_score}")

                result = run_refiner(
                    specimen=specimen,
                    input_text=input_text,
                    client=client,
                    meter=meter,
                    persister=persister,
                    scorer=scorer,
                    tmp_dir=tmp_dir,
                    max_iterations=args.max_iterations,
                    dry_run=args.dry_run,
                    force=args.force,
                )
                all_results.append(result)

        except BudgetExceeded as exc:
            print(f"\nSTOP: {exc}", file=sys.stderr)
            summary_path = write_summary(args.out, all_results, meter, args.dry_run)
            print(f"Partial summary: {summary_path}", file=sys.stderr)
            return 1

    summary_path = write_summary(args.out, all_results, meter, args.dry_run)

    accepted = sum(1 for r in all_results if r.get("accepted"))
    total = len(all_results)
    print(f"\n[arm-b] DONE: {total} specimens. Accepted: {accepted}/{total}.")
    print(f"  cost: ${meter.spent_usd:.4f} of ${meter.ceiling_usd:.2f}")
    print(f"  summary: {summary_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
