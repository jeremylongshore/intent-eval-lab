# gbrain Citation-Integrity Eval — Pre-Registered Experimental Design

**Bead:** `bd_000-projects-704w.1` (design) under epic `bd_000-projects-704w`
**Authority:** Snoopy-fluttering-comet plan Move 2 (re-scoped 2026-06-01 feasibility) · mirrors Phase A.0 pre-registration discipline (`../phase-a-0-baseline/DESIGN.md`)
**Tier:** Tier-2 independent lab research (Evidence Bench), methodology oversight by intent-eval-lab; emits an Evidence-Bundle-shaped result but carries no Evidence-Bundle runtime dependency.
**Status:** PRE-REGISTERED DRAFT — design only. No corpus capture, no API calls, no scoring runs are authorized by this document. They begin only after the open items in § 11 resolve.
**Cost ceiling:** $0.00 target (see § 8).

---

## 0. One-paragraph framing (read this first)

`gbrain` (github.com/garrytan/gbrain) is a **personal knowledge / memory system**, not an LLM and not a code generator. It ingests a document corpus (`put` / `import`), embeds it into a pgvector store, and answers natural-language questions via hybrid retrieval + synthesis (`query` / `ask`), returning a synthesized answer **with citations back to captured sources**. Running the Phase-A.0 SKILL.md-editing eval against it would be a category error (grading a librarian on writing code). The honest, **non-derivative** benchmark is a **citation-integrity eval**: feed it a known corpus, ask questions, and score whether every claim in its answer traces to a real captured source that actually supports the claim — versus a hallucinated citation that resolves to nothing or to a non-supporting source. Provenance / citation integrity is the lab's differentiated measurement lane; the upstream retrieval-eval suite measures retrieval precision/recall (P@K / R@K), **not** whether the cited source supports the synthesized claim. This design measures the dimension the upstream suite does not, and links to it rather than restating or claiming to beat its numbers.

## 1. Hypotheses

| Hypothesis           | Statement                                                                                                                                                                                                                                               |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **H₀ (null)**        | For a corpus with a known ground-truth source-to-claim map, the memory system's synthesized answers cite the supporting source for every claim — i.e. citation precision and recall are both at ceiling (1.0) and the hallucinated-citation count is 0. |
| **H₁ (alternative)** | The system produces a non-trivial rate of citation-integrity failures: claims cited to sources that do not support them, claims with no citation where a supporting source exists, or citations that resolve to no captured page.                       |

This is a **measurement** study, not a comparison-of-arms study. The deliverable is a per-question, per-claim citation verdict and three aggregate scores (§ 5). There is exactly one system under test (gbrain on a free OpenAI-compatible embedding + synthesis stack). The published result states the measured dimension loudly and scopes it honestly.

## 2. System under test

| Component             | Choice                                                                          | Why                                                                                      |
| --------------------- | ------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Memory system         | `gbrain` `0.42.42.0` (pinned; record exact `gbrain version` at run time)        | The system under test.                                                                   |
| Store                 | PGLite (`init --pglite`, no server)                                             | Zero-infra, fully local, deterministic, free.                                            |
| Retrieval + synthesis | `gbrain query <question>` (hybrid: pgvector + tsvector + multi-query expansion) | This is the "think" equivalent: it returns a synthesized answer with cited source pages. |
| Embedding provider    | free OpenAI-compatible endpoint via the `litellm` recipe override (§ 3)         | $0 within free dev-tier credits.                                                         |
| Synthesis provider    | free OpenAI-compatible chat endpoint (same recipe family)                       | $0 within free dev-tier credits.                                                         |

**Version-pinning discipline:** the headline result is bound to one `gbrain` version, one embedding model id, one synthesis model id, one corpus SHA, and one question-set SHA. Re-runs after any of these change are versioned and reported separately.

## 3. Free-tier embedding + synthesis wiring (CONFIRMED — see feasibility record)

The previously-UNCONFIRMED override mechanism is now **confirmed** (feasibility bead `704w.3`; full trace in `FEASIBILITY.md`). gbrain resolves an embedding/synthesis provider through a **recipe gateway** where the base URL is `cfg.base_urls[recipe.id] ?? recipe.base_url_default`. There is no dedicated NVIDIA recipe, but several **generic OpenAI-compatible recipes** exist whose base URL is overridable by environment variable. The canonical free wiring is the `litellm` universal recipe:

```bash
# Embedding + synthesis both point at the free OpenAI-compatible NIM endpoint.
export LITELLM_BASE_URL="https://integrate.api.nvidia.com/v1"   # OpenAI-compatible /v1/embeddings + /v1/chat/completions
export LITELLM_API_KEY="<free-dev-tier-key>"                    # nvapi-… style; exported at runtime, never committed

# Brain must be created WITH the embedding model declared — PGLite cannot
# switch embedding model in place (confirmed: config set refuses, prints the
# exact re-init command).
gbrain init --pglite \
  --embedding-model "litellm:nvidia/nv-embedqa-e5-v5" \
  --embedding-dimensions 1024
```

`config.provider_base_urls` (brain config) overrides the env var if both are set (`config wins over env`, gateway `build-gateway-config.ts:63`). The synthesis model id is set the same way through the gateway recipe.

**Free-tier gate (binding):** if a free OpenAI-compatible endpoint cannot serve BOTH embeddings and synthesis within dev-tier limits, surface to Jeremy BEFORE any paid embedder or paid synthesis call. Pace requests to the documented free-tier rate (≈40 req/min observed for the NIM dev tier); a paced run with explicit sleeps stays inside the window.

## 4. Corpus (pre-registered before any capture)

A **small, self-contained, fully-attributable** corpus is required so ground truth is auditable by a skeptic. The corpus is captured into the brain via `gbrain put <slug>` / `gbrain import <dir>`.

**Corpus design constraints:**

1. **Closed world.** Every fact the question set probes must be present in exactly one (or a known set of) captured pages — so "the supporting source" is unambiguous. No open-web facts.
2. **Disjoint-fact pages.** Pages are authored so each carries distinct, non-overlapping facts, making a mis-citation detectable (citing page X for a fact that lives only on page Y is a hard failure, not a near-miss).
3. **Decoy pages.** Include pages on adjacent topics that do NOT contain the probed fact, to expose "cited a plausible-but-wrong source" failures.
4. **Negative-control questions.** Include questions whose answer is genuinely absent from the corpus; the correct behavior is to decline / cite nothing. A fabricated citation here is a hallucination, scored as such.

**Corpus manifest** (`corpus/manifest.json`, authored at capture time, mirrors Phase A.0's manifest): records each page slug, its SHA256, the facts it is the authoritative source for, the capture timestamp, and the brain's `gbrain version` + embedding-model id. The manifest is the experimental record; the captured pages are the artifacts the run consumes.

Target size: **20–30 pages**, **~30 questions** (a count meaningful for a precision/recall read while staying hand-auditable). Final counts are frozen in the manifest before the first `query` call.

## 5. Ground truth + scoring rule (pre-registered)

**Ground-truth map** (`corpus/ground-truth.json`): for each question, the set of corpus page-slugs that genuinely support the correct answer (the empty set for negative-control questions).

For each question, parse the cited sources from the `gbrain query` synthesized answer, then classify each cited source against ground truth:

| Verdict          | Definition                                                                                                        |
| ---------------- | ----------------------------------------------------------------------------------------------------------------- |
| **supported**    | Cited a ground-truth source that supports the claim. (true positive)                                              |
| **wrong-source** | Cited a captured page that does NOT support the claim. (false positive — the headline citation-integrity failure) |
| **dangling**     | Cited a source that resolves to no captured page at all. (hallucinated citation)                                  |
| **missing**      | A ground-truth source exists but the answer cited nothing / omitted it. (false negative)                          |

**Aggregate scores (the three headline numbers):**

- **Citation precision** = supported / (supported + wrong-source + dangling) — of everything it cited, how much was a real supporting source.
- **Citation recall** = supported / (supported + missing) — of the supporting sources it should have cited, how many it did.
- **Hallucinated-citation count** = wrong-source + dangling — the absolute count of citations that do not support their claim (the dimension the upstream retrieval suite does not measure).

**Determinism of scoring:** the source-parsing rule (how a citation is extracted from the answer text / structured output) is fixed in `scripts/score.py` before any run and hash-pinned via `audit-harness init`. A second human-spot-check pass over ≥20% of verdicts validates the parser against manual reading; disagreements are reported, not silently corrected.

## 6. Replication discipline (mirrors Phase A.0 § 6)

1. **Pre-register** corpus + question set + ground-truth map + scoring rule BEFORE the first `gbrain query`. Hash-pin via `audit-harness init` once frozen.
2. **Single system version:** all scoring uses one pinned `gbrain version` + one embedding-model id + one synthesis-model id. Changes → versioned re-run, reported separately.
3. **Determinism:** synthesis temperature 0.0 where the provider honors it; record the exact model id + any non-deterministic provider caveat.
4. **All raw I/O persisted** content-addressed by SHA under `results/raw/<question-sha>/{query.json,answer.json,verdict.json}`; append-only.
5. **No silent retries** — failed `query` calls land in `results/errors.jsonl` and are excluded from headline stats (reported separately).

## 7. Result shape (Evidence-Bundle-mappable)

The aggregated result is emitted in a shape that maps cleanly onto `@intentsolutions/core` `evidence-bundle.schema.json`: a deterministic run record with the corpus SHA, question-set SHA, system version, per-question verdicts, and the three aggregate scores. **No predicate is claimed** (predicate URI set stays empty per DR-018 — the gbrain stack is not a kernel entity). Signing (production Rekor blob signature) is a downstream bead (`704w.9`), not authorized by this design.

## 8. Cost ceiling

| Path                                               | Cost                   | Ceiling behavior                                    |
| -------------------------------------------------- | ---------------------- | --------------------------------------------------- |
| PGLite store                                       | $0                     | Local, no service.                                  |
| Embeddings via free OpenAI-compatible NIM dev tier | $0 within free credits | Paced ≤ free-tier rate; informational ceiling only. |
| Synthesis via free OpenAI-compatible dev tier      | $0 within free credits | Same.                                               |

**Canonical run cost: $0.00.** Any unavoidable paid call is logged explicitly and surfaced to Jeremy BEFORE it is made (§ 3 free-tier gate).

## 9. Scope honesty (what this does and does NOT claim)

- **Does measure:** whether synthesized answers cite sources that actually support their claims, on a closed, hand-authored corpus.
- **Does NOT measure:** retrieval precision/recall at K (the upstream retrieval-eval suite's lane), end-to-end answer quality, or performance at scale. The published row links to the upstream suite and explicitly states it measures a different dimension; it does not restate or claim to beat upstream retrieval numbers.
- **Avoids the "upstream-eval-but-signed" trap:** the ground-truth here is citation support, authored from first principles, not a re-run of an existing retrieval benchmark.

## 10. Output deliverables (run phase, not this phase)

1. `corpus/manifest.json` + `corpus/ground-truth.json` + the captured pages — pre-registration artifacts.
2. `RESULTS.md` — the three aggregate scores + per-verdict table + honest scope caveat.
3. `scripts/{capture,run,score}.py` — deterministic harness.
4. Evidence-Bundle-shaped aggregated record under `results/aggregated/`.
5. Closed beads `704w.5` (harness) + `704w.7` (run) with links to RESULTS.

## 11. Open items — must resolve before the run phase

| #   | Question                                                                                                                   | Status                                                                                                                                                      |
| --- | -------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Q1  | Exact free synthesis model id for `gbrain query` on the NIM dev tier (chat completion, OpenAI-compatible)                  | OPEN — confirm in the run-phase first session; the embedding model (`nvidia/nv-embedqa-e5-v5`, 1024d) is confirmed.                                         |
| Q2  | Free-tier rate limits for embeddings vs synthesis (pace the run)                                                           | OPEN — observed ≈40 req/min for NIM dev; verify both surfaces before the full run.                                                                          |
| Q3  | Citation-extraction parser contract (how `gbrain query` surfaces cited slugs — prose vs structured `--detail`/JSON output) | OPEN — `query --detail` levels exist (low/medium/high); pick the most machine-parseable surface in the run-phase first session and freeze it in `score.py`. |
| Q4  | Final corpus size + question count                                                                                         | OPEN — frozen in `manifest.json` at capture time (target 20–30 pages / ~30 questions).                                                                      |
| Q5  | Where the signed bundle lands                                                                                              | DEFERRED to `704w.9` (production Rekor blob, predicate reserved).                                                                                           |

## 12. What this document (design phase) produces

This `DESIGN.md` + the `FEASIBILITY.md` record + the directory scaffold. **Nothing else.** No corpus capture, no API calls, no scoring. The run phase begins only after Q1–Q4 resolve in its first session.

---

— Jeremy Longshore
intentsolutions.io
