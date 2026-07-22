# `bbb-seed-v1` — the frozen public corpus for evaluating Bob's Big Brain

Sibling of `../drift-classification/`. This eval set exists so that **a stranger can reproduce a
number we publish** about the governed brain's retrieval quality.

**Status: SCAFFOLDED, NOT FROZEN.** The machinery is built and verified. `corpus/` is empty and
`MANIFEST.json` does not exist yet, because promoting content into the corpus is a human decision
that has not been made. `verify-manifest.mjs` correctly refuses to report green in this state.

## The two-corpus split

| Arm | Runs against | Rows publish to | Purpose |
|---|---|---|---|
| **public** | this frozen, pinned, sanitized corpus | `labs.intentsolutions.io` | reproducible by outsiders |
| **internal** | the live `~/.teamkb` (245 MB, real memories) | `site-internal/internal/results/` **only** | catches regressions on the *actual* brain |

Public numbers stay reproducible; private data never leaves the box. The dashboard's
`scripts/lint-arm-symmetry.ts` enforces that both arms are present or neither — so publish the pair
or publish nothing.

## Why `corpus/` is empty — the blocking finding

The live brain holds **17,321 curated memories, every one classified `sensitivity: 'internal'`.
Not one is `'public'`.** There is no schema-level marker to filter on, so a public corpus cannot be
derived by trusting the brain's own governance label. Any public corpus is, by construction, a
decision to publish content the brain classifies as internal — and that decision is a human's, not
a script's.

Accordingly `scripts/derive-corpus.ts` writes to `.candidate/` (git-ignored) and **has no flag that
writes to `corpus/`**. See `ALLOWLIST.md` for the full rule set and its rationale.

## What the derivation currently produces

```
eligible pool 733          Rule 1: lifecycle=active + category in
                           pattern/architecture/convention/decision/onboarding
                           (`reference` — 16,219 memories, 94% of the brain — refused wholesale)
admitted      608          Rule 2: zero risk markers
refused       125          secret_kw 87 · private_host 28 · person_name 11
                           long_hex_or_b64 11 · ip_address 7 · abs_home_path 2 · email 0
selected       80          for human review (33 of 38 gold-cited documents)
ESCALATED       5          gold-cited but Rule 2 refused — human adjudication required
```

The derivation is **deterministic**: no clock, no randomness, gold-first then id order. Two runs
against the same database produce a byte-identical report (verified).

### The five escalations, and why they matter

Rule 2 refuses the *neighbourhood* of a secret, not just a secret. Its known cost is that a document
**about** tokens trips the same marker as a document **containing** one:

| Document | Refused by | Why the match is subject matter |
|---|---|---|
| Compile-Then-Govern Architecture | `secret_kw` | The platform's signature architecture doc |
| Token Passthrough | `secret_kw` | The pattern is *named* for the word |
| Spool Boundary Threat Model | `secret_kw` | Threat models discuss credentials by necessity |
| Double-Gate Pattern | `secret_kw` | ditto |
| Team mode is member-proposes / server-disposes | `private_host` | names our own hostname |

These are **not** auto-admitted — that would be the default-accept path `ALLOWLIST.md` Rule 3
forbids. They are written to `.candidate/escalated/` for one-at-a-time adjudication. Until then the
**7 questions citing them are `blocked`** in `questions.yaml` and must not be scored: a query whose
gold document is absent scores 0 recall for a reason unrelated to retrieval quality, and averaging
it in would understate the system.

## Question bank

`questions.yaml` — all **42** queries from the hand-labeled `governed-brain-v1` dataset
(14 lexical / 28 semantic), lifted verbatim. Those queries and their gold labels are **already
public** (`bobs-big-brain-registrar` is a public repo), so restating them publishes nothing new —
only the corpus they are answered against is subject to the sanitization question.

| Status | Count | Meaning |
|---|---|---|
| `active` | 34 | gold present in the candidate corpus; scoreable |
| `blocked` | 7 | gold escalated; unanswerable until adjudicated |
| `unlabelled` | 1 | q39 has no gold labels in the source dataset; not scoreable for recall |

Recorded BM25 misses (q15, q29) are **kept**, not relabelled away — a miss on a valid semantic query
is evidence about the retrieval wall, which is the whole point of the semantic stratum.

Two further banks exist and are **not yet folded in**, because they lack `qmd://` gold labels:
the compiler's `dogfood/question-banks/intent-eval-core-v{1,2}.yaml` (substring-based) and the
registrar's 12-question outsider set (`000-docs/043-OD-EVAL-onboarding-qbank-v1.md`, scored 0/1/2 by
hand). Labelling those is follow-on work.

## Files

| Path | Role |
|---|---|
| `ALLOWLIST.md` | NORMATIVE derivation rules + why each exists |
| `scripts/derive-corpus.ts` | read-only sanitizer; writes `.candidate/`, never `corpus/` |
| `scripts/verify-manifest.mjs` | fail-closed pin verifier (exit 1 drift, 2 structural) |
| `questions.yaml` | the 42-query golden bank with per-query status |
| `gold-ids.txt` | the 38 unique gold document ids, so derivation can prioritise them |
| `corpus/` | **empty** — populated only by reviewed promotion |
| `MANIFEST.json` | **absent** — created at freeze time |
| `.candidate/` | git-ignored derivation output; contains internal-classified content |

## Reproducing

```bash
cd evals/bbb-seed-v1
node --experimental-strip-types scripts/derive-corpus.ts            # writes .candidate/
node --experimental-strip-types scripts/derive-corpus.ts --report-only | jq .   # no writes
node scripts/verify-manifest.mjs                                    # exit 2 until frozen
```

## To freeze this eval set

1. A human reads all 80 candidates (~60 KB of prose — the gold-cited subset runs 285–1,227 bytes each).
2. Adjudicate the 5 escalations individually, in writing.
3. Record sign-off in `corpus/PROVENANCE.md`.
4. Promote reviewed documents into `corpus/` by explicit `git add` of specific files — never a bulk
   add of `.candidate/`.
5. Generate `MANIFEST.json` (sha256 of every corpus file **and** `questions.yaml`).
6. `node scripts/verify-manifest.mjs` → exit 0.
7. Register the set in `intent-eval-dashboard/data/eval-sets.json`
   (`id: bbb-seed-v1`, `predicate_uri: evals.intentsolutions.io/gate-result/v1`,
   `page_path: /eval-sets/bbb-seed-v1/`) and let `scripts/regenerate.py` fill the volatile fields.

Step 1 is the gate. Steps 2–7 are mechanical.
