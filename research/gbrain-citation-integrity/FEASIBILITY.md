# gbrain Citation-Integrity Eval — Feasibility Record

**Bead:** `bd_000-projects-704w.3` (feasibility) under epic `bd_000-projects-704w`
**Goal:** install gbrain locally; confirm the (previously UNCONFIRMED) free OpenAI-compatible / NVIDIA-NIM embedding base-URL override; smoke `init` + capture + retrieval.
**Status:** CONFIRMED. Install ran. Offline smoke (init → put → list → search) passed. The embedding base-URL override mechanism is confirmed from source with file:line citations. The free-tier embedding/synthesis _call itself_ was not exercised here (no free-tier key in this environment); the exact run procedure + expected outputs are documented below so the run phase is mechanical.
**Date:** 2026-06-13 · **Environment:** Linux dev box, `bun 1.2.23`.

---

## 1. Install — DONE

```bash
bun install -g github:garrytan/gbrain
# → installed gbrain@github:garrytan/gbrain#4ee530f, 118 packages, ~3s
gbrain version            # → gbrain 0.42.42.0
```

The installed binary resolves on PATH (`~/.bun/bin/gbrain`). One postinstall step is blocked by bun's trust gate (`bun pm -g untrusted` to inspect) — not required for the smoke.

**CLI-surface note for the design doc:** the bead text references `gbrain capture` / `gbrain think`. In `0.42.42.0` those are:

- capture → `gbrain put <slug>` (single page) / `gbrain import <dir>` (bulk markdown).
- think → `gbrain query <question>` (alias `gbrain ask`) — hybrid pgvector + tsvector + multi-query expansion, returns a synthesized answer with cited source pages.

The DESIGN doc uses the current command names.

## 2. Offline smoke (no API key needed) — PASSED

PGLite store + keyword (tsvector) retrieval need no embedding provider, so the corpus-capture and keyword-retrieval path is provable fully offline:

```bash
export GBRAIN_HOME=/tmp/gbrain-smoke           # isolate from any real brain
gbrain init --pglite --no-embedding            # creates brain, defers embeddings
echo "# Smoke Test Page
gbrain feasibility smoke ..." | gbrain put smoke-test
gbrain list -n 5                               # → smoke-test  concept  2026-06-13  Smoke Test
gbrain search "feasibility"                    # → [0.2432] smoke-test -- # Smoke Test Page ...
```

Observed: brain initialized, page written, listed, and retrieved by keyword search. The full **closed-corpus capture + keyword-retrieval** half of the eval works offline with zero external dependency.

## 3. Embedding / synthesis provider override — CONFIRMED FROM SOURCE

The previously-UNCONFIRMED item ("which env var/config overrides the embedding endpoint to NVIDIA NIM") is resolved. gbrain routes every provider through a **recipe gateway**. The base URL is resolved as:

> `const baseURL = cfg.base_urls?.[recipe.id] ?? recipe.base_url_default;`
> — `src/core/ai/gateway.ts:382`

There is **no dedicated NVIDIA recipe**, but multiple **generic OpenAI-compatible recipes** exist whose base URL is overridable by environment variable. The env→`base_urls` wiring is explicit:

> ```ts
> if (process.env.LITELLM_BASE_URL)    envBaseUrls['litellm']    = process.env.LITELLM_BASE_URL;
> if (process.env.OPENROUTER_BASE_URL) envBaseUrls['openrouter'] = process.env.OPENROUTER_BASE_URL;
> if (process.env.OLLAMA_BASE_URL)     envBaseUrls['ollama']     = process.env.OLLAMA_BASE_URL;
> if (process.env.LLAMA_SERVER_BASE_URL) envBaseUrls['llama-server'] = ...;
> ...
> base_urls: { ...envBaseUrls, ...(c.provider_base_urls ?? {}) }, // config wins over env
> ```
>
> — `src/core/ai/build-gateway-config.ts:45-63`

The cleanest free wiring is the **`litellm` universal OpenAI-compatible recipe** (`src/core/ai/recipes/litellm-proxy.ts`): `tier: 'openai-compat'`, `implementation: 'openai-compatible'`, optional `LITELLM_BASE_URL` + `LITELLM_API_KEY`. Point it at the NIM OpenAI-compatible endpoint:

```bash
export LITELLM_BASE_URL="https://integrate.api.nvidia.com/v1"   # /v1/embeddings + /v1/chat/completions
export LITELLM_API_KEY="<free-dev-tier-key>"                    # nvapi-… ; runtime only, never committed
gbrain init --pglite \
  --embedding-model "litellm:nvidia/nv-embedqa-e5-v5" \
  --embedding-dimensions 1024
```

The model id format is `<recipe-id>:<model>` (confirmed by the in-package test `test/doctor-embedding-env-override.test.ts`, which exercises `openai:text-embedding-3-large` and `zeroentropyai:zembed-1`). `config.provider_base_urls` overrides the env var when both are present.

**The openai-compatible embedding path is real:** the gateway instantiates these via `createOpenAICompatible` (`@ai-sdk/openai-compatible`) and calls `${base_url}/embeddings` (`gateway.ts:1012, 1224-1249`). Any OpenAI-spec `/v1/embeddings` server — which the NIM endpoint is — is served by this path.

## 4. PGLite embedding-model immutability gotcha — CONFIRMED

`gbrain config set embedding_model …` on a PGLite brain **refuses in place** and prints the exact re-init recipe (verified live):

```text
[config] To switch embedding models/dimensions on PGLite, wipe and re-init:
[config]   gbrain init --pglite --embedding-model litellm:nvidia/nv-embedqa-e5-v5
[config] No --force escape: silently writing a no-op preserves the bug class this rejection closes.
```

**Implication for the run phase:** declare the embedding model **at `init` time**, not after. The DESIGN doc § 3 reflects this.

## 5. What was NOT exercised here, and why it's not a blocker

- **A live free-tier embedding/synthesis call.** No free OpenAI-compatible dev-tier key is present in this environment, and the design discipline forbids any paid call without surfacing to Jeremy first. The mechanism is confirmed from source + the offline path is proven; the remaining step is mechanical: export the two env vars + re-init.
- **The exact free synthesis model id for `gbrain query`** (chat completion). Open item Q1 in DESIGN § 11 — resolve in the run phase's first session. The embedding model (`nvidia/nv-embedqa-e5-v5`, 1024d) is confirmed.

## 6. Exact run-phase feasibility procedure + expected outputs

For the run-phase first session (after a free-tier key is exported):

```bash
export GBRAIN_HOME=/path/to/eval-brain
export LITELLM_BASE_URL="https://integrate.api.nvidia.com/v1"
export LITELLM_API_KEY="$NIM_FREE_KEY"
gbrain init --pglite \
  --embedding-model "litellm:nvidia/nv-embedqa-e5-v5" \
  --embedding-dimensions 1024
# expected: brain created, embedding probe succeeds (1 small /embeddings call)

gbrain doctor --fast --json    # expected: embeddings check = ok; pgvector = ok
gbrain put demo-page < page.md # expected: page stored + embedded
gbrain query "a question the corpus answers"
# expected: synthesized answer with cited source slug(s); pace ≤ ~40 req/min
```

Expected failure-to-watch: if `gbrain doctor` reports the embedding check `warn`/`fail` (auth, dim mismatch, or unreachable base URL), STOP and surface — do not fall back to a paid embedder (free-tier gate, DESIGN § 3).

---

— Jeremy Longshore
intentsolutions.io
