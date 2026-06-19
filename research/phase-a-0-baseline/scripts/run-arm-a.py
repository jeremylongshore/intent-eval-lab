#!/usr/bin/env python3
"""run-arm-a.py — Naive {provider}-in-context arm (null hypothesis, Arm A).

Phase A.0 baseline experiment per DESIGN.md § 3 Arm A.

Iterates the 60 main-corpus specimens x K-sweep {0, 3, 8, 16} = 240 runs.
Per run:
  1. Load specimen SKILL.md.
  2. Sample K passing exemplars from the same corpus (exclude self).
  3. Build prompt per DESIGN.md § 3 Arm A template.
  4. Call the selected provider at temperature=0.0 (or --dry-run synthetic).
  5. Score the response as if it were the new SKILL.md frontmatter.
  6. Persist prompt.json + response.json + score.json content-addressed.

Idempotent: if results/raw/arm-a/<provider>/<sha8>/k=<N>/response.json already
exists, the run is skipped (no re-call). Pass --force to override.

Default provider: nvidia-llama-405b (NVIDIA NIM, free tier, zero cost).
Stops loudly with BudgetExceeded when CostMeter triggers on paid providers.

Emits results/raw/arm-a/<provider>/_summary.json at end: per-K mean+std
marketplace_score_pct delta vs input baseline.

Usage:
    run-arm-a.py --manifest <path> --out <dir> \\
                 --k-sweep 0,3,8,16 \\
                 --provider nvidia-llama-405b \\
                 --budget-ceiling-usd 20 \\
                 [--dry-run] [--force] [--limit N]

--provider: one of nvidia-llama-405b (default), nvidia-llama-70b,
            nvidia-nemotron, groq-llama-70b, groq-llama-70b-specdec,
            groq-mixtral, anthropic-opus, anthropic-sonnet, anthropic-haiku.
--dry-run:  builds prompts, prints estimated costs and synthetic responses,
            scores them. Zero API spend. Validates pipeline end-to-end.
--limit N:  process only the first N specimens (useful for smoke tests).
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import statistics
import sys
import tempfile
from pathlib import Path

# Resolve _arm_common relative to this script's location (avoids PYTHONPATH dep)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _arm_common import (
    ALL_PROVIDER_NAMES,
    DEFAULT_BUDGET_CEILING_USD,
    DEFAULT_PROVIDER,
    BudgetExceeded,
    CostMeter,
    ManifestReader,
    ResultPersister,
    Scorer,
    SpecimenMeta,
    build_arm_a_prompt,
    get_provider,
    is_free_provider,
    load_exemplars,
)

ARM_NAME = "arm-a"


def estimate_prompt_tokens(prompt: str) -> int:
    """Rough char-to-token estimate (4 chars per token) for dry-run cost display."""
    return max(1, len(prompt) // 4)


def score_pct_delta(baseline_score: int, new_score: int) -> int:
    return new_score - baseline_score


def run_single(
    specimen: SpecimenMeta,
    k: int,
    manifest: ManifestReader,
    client: object,  # any LLMProvider instance
    meter: CostMeter,
    persister: ResultPersister,
    scorer: Scorer,
    tmp_dir: Path,
    force: bool,
    dry_run: bool,
) -> dict | None:
    """Execute one specimen x K run. Returns result dict or None if skipped."""
    sub = f"k={k}"
    sha = specimen.sha256

    # Idempotency: skip if response already exists
    if persister.exists(sha, "response.json", sub=sub) and not force:
        return None

    # Load input SKILL.md
    try:
        input_text = specimen.path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        persister.log_error(sha, f"Cannot read specimen: {exc}", {"sub": sub})
        return None

    # Sample exemplars (exclude self)
    try:
        exemplars = load_exemplars(manifest, k=k, seed=manifest.seed, exclude={sha})
    except ValueError as exc:
        persister.log_error(sha, f"exemplar sampling failed: {exc}", {"k": k, "sub": sub})
        return None

    # Build prompt
    prompt = build_arm_a_prompt(input_text, exemplars)

    # Dry-run: print summary before actual call
    if dry_run:
        est_tokens = estimate_prompt_tokens(prompt)
        # cost is $0 for free providers; synthetic response will reflect this
        print(
            f"[dry-run] specimen={specimen.sha8} k={k} "
            f"provider={getattr(client, 'name', '?')}/{getattr(client, 'model', '?')} "
            f"est_input_tokens={est_tokens}"
        )
        prompt_preview = prompt[:300].replace("\n", " ")
        print(f"  prompt[:300]: {prompt_preview!r}")

    # Call provider (or get synthetic response in dry-run mode)
    try:
        completion = client.complete(prompt, max_tokens=1024)
    except Exception as exc:
        persister.log_error(sha, f"API call failed: {exc}", {"k": k, "sub": sub})
        return None

    # Persist prompt + response
    prompt_data = {
        "arm": ARM_NAME,
        "specimen_sha256": sha,
        "specimen_path": str(specimen.path),
        "k": k,
        "exemplar_shas": [e.sha256[:8] for e in exemplars],
        "prompt_text": prompt,
        "prompt_estimated_tokens": estimate_prompt_tokens(prompt),
        "generated_at": dt.datetime.now(dt.UTC).isoformat(),
    }
    response_data = {
        "arm": ARM_NAME,
        "specimen_sha256": sha,
        "k": k,
        "response_text": completion.text,
        "provider": completion.provider,
        "model": completion.model,
        "stop_reason": completion.stop_reason,
        "input_tokens": completion.usage.input_tokens,
        "output_tokens": completion.usage.output_tokens,
        "cost_usd": completion.usage.cost_usd,
        "dry_run": dry_run,
    }

    # Record cost BEFORE persisting (so budget gate fires before disk writes)
    meter.record(completion.usage)

    persister.write_json(sha, "prompt.json", prompt_data, sub=sub)
    persister.write_json(sha, "response.json", response_data, sub=sub)

    # Assemble candidate SKILL.md: frontmatter from response + original body
    response_fm = completion.text.strip()
    original_body_start = input_text.find("\n---", 4)
    original_body = input_text[original_body_start + 4 :] if original_body_start != -1 else ""
    candidate_text = response_fm + "\n" + original_body

    # Score candidate
    try:
        candidate_score = scorer.score_text(candidate_text, tmp_dir)
    except Exception as exc:
        persister.log_error(sha, f"scoring failed: {exc}", {"k": k, "sub": sub})
        persister.write_json(sha, "score.json", {"error": str(exc)}, sub=sub)
        return None

    score_data = candidate_score.to_dict()
    score_data["baseline_marketplace_score_pct"] = specimen.marketplace_score
    score_data["delta_marketplace_score_pct"] = score_pct_delta(
        specimen.marketplace_score, candidate_score.marketplace_score_pct
    )
    persister.write_json(sha, "score.json", score_data, sub=sub)

    if dry_run:
        print(
            f"  scored: baseline={specimen.marketplace_score} "
            f"candidate={candidate_score.marketplace_score_pct} "
            f"delta={score_data['delta_marketplace_score_pct']:+d}"
        )

    return {
        "sha8": specimen.sha8,
        "stratum": specimen.stratum,
        "k": k,
        "provider": completion.provider,
        "model": completion.model,
        "baseline_score": specimen.marketplace_score,
        "candidate_score": candidate_score.marketplace_score_pct,
        "delta": score_data["delta_marketplace_score_pct"],
        "cost_usd": completion.usage.cost_usd,
    }


def aggregate_results(
    all_results: list[dict],
    k_values: list[int],
) -> dict:
    """Compute per-K mean+std of marketplace_score_pct delta."""
    by_k: dict[int, list[int]] = {k: [] for k in k_values}
    for r in all_results:
        by_k[r["k"]].append(r["delta"])

    per_k_stats: dict[str, dict] = {}
    for k, deltas in by_k.items():
        if not deltas:
            per_k_stats[str(k)] = {"n": 0, "mean": None, "std": None, "min": None, "max": None}
        else:
            mean = statistics.mean(deltas)
            std = statistics.stdev(deltas) if len(deltas) > 1 else 0.0
            per_k_stats[str(k)] = {
                "n": len(deltas),
                "mean": round(mean, 3),
                "std": round(std, 3),
                "min": min(deltas),
                "max": max(deltas),
            }
    return per_k_stats


def write_summary(
    out_dir: Path,
    all_results: list[dict],
    k_values: list[int],
    meter: CostMeter,
    dry_run: bool,
    provider: str = "unknown",
) -> Path:
    """Write _summary.json under the provider-scoped directory; return its path."""
    per_k = aggregate_results(all_results, k_values)
    summary = {
        "arm": ARM_NAME,
        "provider": provider,
        "generated_at": dt.datetime.now(dt.UTC).isoformat(),
        "dry_run": dry_run,
        "cost_meter": meter.summary(),
        "total_runs": len(all_results),
        "per_k_marketplace_score_pct_delta": per_k,
        "per_run_results": all_results,
    }
    path = out_dir / ARM_NAME / provider / "_summary.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def main() -> int:
    ap = argparse.ArgumentParser(description="Run Arm A (naive provider-in-context) of Phase A.0 baseline experiment.")
    ap.add_argument("--manifest", type=Path, required=True, help="Path to corpus/manifest.json")
    ap.add_argument("--out", type=Path, required=True, help="Root output directory (results/raw/)")
    ap.add_argument(
        "--k-sweep", default="0,3,8,16", help="Comma-separated K values (exemplar counts). Default: 0,3,8,16"
    )
    ap.add_argument(
        "--provider",
        default=os.environ.get("PHASE_A0_PROVIDER", DEFAULT_PROVIDER),
        choices=ALL_PROVIDER_NAMES,
        help=(
            f"LLM provider to use. Default: {DEFAULT_PROVIDER} (free tier). "
            "Set PHASE_A0_PROVIDER env var to change default."
        ),
    )
    ap.add_argument(
        "--budget-ceiling-usd",
        type=float,
        default=float(os.environ.get("PHASE_A0_BUDGET_CEILING_USD", DEFAULT_BUDGET_CEILING_USD)),
        help=(
            f"Hard cost ceiling USD (paid providers only). Default: {DEFAULT_BUDGET_CEILING_USD}. "
            "Override via PHASE_A0_BUDGET_CEILING_USD env var."
        ),
    )
    ap.add_argument(
        "--dry-run", action="store_true", help="Simulate pipeline without real API calls. Validates end-to-end."
    )
    ap.add_argument("--force", action="store_true", help="Overwrite existing result files (re-run).")
    ap.add_argument("--limit", type=int, default=None, help="Process only first N specimens (smoke test).")
    ap.add_argument("--validator-path", type=Path, default=None, help="Override path to validate-skills-schema.py")
    args = ap.parse_args()

    # Parse K-sweep
    try:
        k_values = [int(v.strip()) for v in args.k_sweep.split(",")]
    except ValueError as exc:
        print(f"ERROR: --k-sweep must be comma-separated integers: {exc}", file=sys.stderr)
        return 2

    if not args.manifest.is_file():
        print(f"ERROR: manifest not found: {args.manifest}", file=sys.stderr)
        return 2

    args.out.mkdir(parents=True, exist_ok=True)

    manifest = ManifestReader(args.manifest)
    specimens = list(manifest.specimens())
    if args.limit:
        specimens = specimens[: args.limit]

    free = is_free_provider(args.provider)
    meter = CostMeter(ceiling_usd=args.budget_ceiling_usd)
    client = get_provider(args.provider, dry_run=args.dry_run)
    persister = ResultPersister(args.out, ARM_NAME, provider=args.provider, force=args.force)
    scorer = Scorer(validator_path=args.validator_path)

    all_results: list[dict] = []
    skipped_count = 0

    print(
        f"[arm-a] specimens={len(specimens)} k_sweep={k_values} "
        f"provider={args.provider} model={client.model} "
        f"ceiling=${args.budget_ceiling_usd:.0f} "
        f"free_tier={free} dry_run={args.dry_run}"
    )

    with tempfile.TemporaryDirectory(prefix="arm_a_score_") as tmp_str:
        tmp_dir = Path(tmp_str)

        try:
            for specimen in specimens:
                for k in k_values:
                    result = run_single(
                        specimen=specimen,
                        k=k,
                        manifest=manifest,
                        client=client,
                        meter=meter,
                        persister=persister,
                        scorer=scorer,
                        tmp_dir=tmp_dir,
                        force=args.force,
                        dry_run=args.dry_run,
                    )
                    if result is None:
                        skipped_count += 1
                    else:
                        all_results.append(result)

        except BudgetExceeded as exc:
            print(f"\nSTOP: {exc}", file=sys.stderr)
            print(
                f"Partial results ({len(all_results)} runs) written to {args.out}.",
                file=sys.stderr,
            )
            # Still write partial summary so the experiment is auditable
            summary_path = write_summary(args.out, all_results, k_values, meter, args.dry_run, args.provider)
            print(f"Partial summary: {summary_path}", file=sys.stderr)
            return 1

    summary_path = write_summary(args.out, all_results, k_values, meter, args.dry_run, args.provider)

    print(f"\n[arm-a] DONE: {len(all_results)} runs completed, {skipped_count} skipped (idempotent).")
    cost_note = "(free tier)" if free else f"of ${meter.ceiling_usd:.2f}"
    print(f"  cost: ${meter.spent_usd:.4f} {cost_note}")
    print(f"  summary: {summary_path}")

    # Print per-K stats to stdout
    per_k = aggregate_results(all_results, k_values)
    print("\nPer-K marketplace_score_pct delta (vs input baseline):")
    for k_str, stats in per_k.items():
        if stats["n"] == 0:
            print(f"  K={k_str}: no data")
        else:
            print(
                f"  K={k_str}: n={stats['n']} "
                f"mean={stats['mean']:+.1f} std={stats['std']:.2f} "
                f"[{stats['min']:+d} .. {stats['max']:+d}]"
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
