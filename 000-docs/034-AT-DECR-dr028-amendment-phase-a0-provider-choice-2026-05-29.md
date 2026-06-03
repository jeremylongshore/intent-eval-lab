---
date: 2026-05-29
type: AT-DECR
status: PROPOSED
acting-head-of-board: Claude (designated by Jeremy Longshore via CTO-mode delegation)
decisions: 1 amendment to DR-028 P0-RATIFY-3
related:
  plan: 027-PP-PLAN-skill-refiner-snoopy-fluttering-comet-v4-2026-05-26.md (v5)
  prior-DR: 028-AT-DECR-isedc-council-session-7-skill-refiner-plan-ratification-2026-05-27.md
  bandwidth: 029-DR-BAND-skill-refiner-bandwidth-model-2026-05-27.md
  eval-bootstrap: 030-AT-DECR-eval-set-bootstrap-decisions-2026-05-28.md
  design: research/phase-a-0-baseline/DESIGN.md
  bead: bd_000-projects-214c.8 (Phase A.0 null-hypothesis baseline)
---

| Beads | bd_000-projects-214c.8 |
| GitHub | jeremylongshore/intent-eval-lab — pending PR |
| Amends | DR-028 P0-RATIFY-3 (model choice pre-registration) |
| Status | PROPOSED — awaiting user ratification in next ISEDC session |

# DR-028 Amendment — Phase A.0 Provider Choice

## 1. Status

PROPOSED. Engineer files the amendment; ISEDC ratifies in the next session. Work under
this amendment (multi-provider harness code, DESIGN.md updates) is pre-authorized per
DR-028 P0-RATIFY-6 (hard-gate `bd-claim-precheck.sh`): the amendment addresses only
the _model selection_ inside P0-RATIFY-3, not the experimental protocol itself.

## 2. Context

DR-028 P0-RATIFY-3 pre-registered `claude-opus-4-7` as the canonical model for the
Phase A.0 null-hypothesis baseline. The pre-registration was made without a confirmed
Anthropic API budget from the user.

User constraint surfaced 2026-05-29: **$20 hard ceiling on Anthropic spend** for
Phase A.0. Running Arm A (60 specimens × 4 K-values) + Arm B (~10 specimens) on
`claude-opus-4-7` at standard pricing ($15/$75 per MTok input/output) would cost
approximately $120 + $40 = $160 — exceeding the ceiling by 8×.

Simultaneously, NVIDIA NIM and Groq provide OpenAI-compatible inference APIs with
free-tier access to models at or above the 70B parameter scale. These are production
inference endpoints, not research previews.

## 3. Decision

**Amend DR-028 P0-RATIFY-3:** replace `claude-opus-4-7` as the canonical Phase A.0
model with `meta/llama-3.1-405b-instruct` via NVIDIA NIM (free tier, zero cost).

Retain `claude-haiku-4-5` (Anthropic) as a $1-2 spot-check baseline to validate
cross-provider consistency. The spot-check runs Arm A at K=0 and K=3 on a 20-specimen
subset — enough to detect systematic behavioral divergence without exhausting budget.

Full provider matrix available via `--provider` CLI flag on both runners:

- `nvidia-llama-405b` (default, free)
- `nvidia-llama-70b` (free)
- `nvidia-nemotron` (free)
- `groq-llama-70b` (free)
- `groq-llama-70b-specdec` (free)
- `groq-mixtral` (free)
- `anthropic-haiku` (paid, ~$1-2 full run)
- `anthropic-sonnet` (paid, ~$8-12 full run)
- `anthropic-opus` (paid, ~$160 full run — use `--limit` within $20)

## 4. Rationale

**R1 — Mechanism question is model-agnostic.**
The null hypothesis being tested (H₀: naive in-context prompting matches ≥70% of
projected Refiner lift) does not depend on which model is prompted. The _mechanism_
under test is the propose/accept loop structure, not which provider's weights evaluate
the edit. If the Refiner loop fails to beat naive prompting on Llama-405B, the finding
is arguably stronger than the same result on Opus: it cannot be dismissed as "just use
a bigger model."

**R2 — Bitter-lesson result is stronger on a free model.**
The DR-028 P0-RATIFY-3 descope decision rule (> 70% lift → Phase B descoped) is meant
to trigger a pivot if naive prompting is good enough. If naive Llama-405B beats the
Refiner mechanism, it means the mechanism provides no useful structure even when the
base model is commoditized. That is a stronger and more generalizable bitter-lesson
conclusion than the same result on a frontier model.

**R3 — Production users mostly run cheaper models.**
The IS skills ecosystem (3,044 marketplace plugins, 45k+ NPM downloads) includes users
running on Haiku and open-source equivalents. A baseline measured against a model in
that cost class is directly relevant to the target population. Generalization from a
Llama-405B result to "this mechanism works for users who can't afford Opus" is tighter
than the reverse.

## 5. Threats to validity under the amended model

**T1 — Llama-405B capability floor.**
Llama-3.1-405B is a 405B-parameter instruction-tuned model with strong benchmark
performance. It is possible that the model is capable enough at YAML/structured-output
tasks that naive prompting saturates the achievable score delta — making the Refiner's
marginal contribution hard to measure regardless of mechanism quality. Mitigation: the
K=0 baseline (no exemplars) will reveal whether the model produces valid frontmatter
at all; if K=0 already scores near-perfect, the experiment's discriminability is low
and the result should be noted in the AAR as a measurement artifact.

**T2 — Provider rate limits forcing partial runs.**
NVIDIA NIM free tier and Groq free tier have rate limits (Groq: 30 req/min). The 240
Arm A runs (60 specimens × 4 K values) will take approximately 8 minutes at 30 req/min.
The Arm B runs (~10 specimens × avg 2 iterations) add ~1 minute. This is within free
tier limits; however if any single run hits a 429, the idempotent retry loop in the
runner handles it transparently (the specimen is logged to `errors.jsonl` and excluded
from headline stats).

## 6. Decision rule unchanged

The 70% threshold from DR-028 P0-RATIFY-3 is unchanged:

> If naive-{provider}-in-context-with-eval-set achieves > 70% of projected Refiner
> lift (pre-registered: 1.5pp marketplace-tier score lift) on the Phase B demo skill,
> DESCOPE Phase B mechanism.

The word "Opus" in the original formulation is replaced by "{provider}" — the threshold
is the same regardless of which model is naive-prompted.

## 7. Re-ratification trigger

If any 2026 frontier Anthropic model release (Opus 4.x successor, Sonnet 4.x
successor) includes a free-tier plan that makes a full Phase A.0 run feasible within
$20, re-run the canonical arm on that model and compare against the Llama-405B result.
Publish both as Part II of the blog post (VP DevRel binding per DR-028 P0-RATIFY-6).

## 8. References

- DR-028 P0-RATIFY-3: original model pre-registration (canonical arm = Opus 4.7)
- `029-DR-BAND-skill-refiner-bandwidth-model-2026-05-27.md` § 2 Phase A.0: bandwidth model
- `research/phase-a-0-baseline/DESIGN.md` § 7: cost ceiling (updated by this amendment)
- `research/phase-a-0-baseline/scripts/_arm_common.py`: `get_provider()` factory
- NVIDIA NIM API: <https://integrate.api.nvidia.com/v1>
- Groq API: <https://api.groq.com/openai/v1>

---

- Jeremy Longshore
  intentsolutions.io
