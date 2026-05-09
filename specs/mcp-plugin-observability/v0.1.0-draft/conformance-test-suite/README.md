# Conformance Test Suite — placeholder

This directory will hold the reference test suite for [SPEC.md v0.1.0-draft](../SPEC.md). It's currently a placeholder; the test harness lands as part of the post-M3 work tied to the first case-study implementation ([`../case-studies/kobiton-automate.md`](../case-studies/kobiton-automate.md)).

## Planned shape

- **`runner.py`** (or equivalent in another language) — drives `claude -p` against a representative prompt set, captures the OTel signal stream, runs assertions against the matcher-map rows.
- **`fixtures/`** — labeled prompt sets per finding-shape (one prompt set per matcher-map row).
- **`assertions/`** — per-requirement assertion modules (R1-R5 of the spec).
- **`collector-config/`** — minimal OTel collector configuration (~10-line Docker compose) for local testing without an external observability backend.

## Why it's not here yet

A test suite asserting on `claude_code.hook` spans (deeper-beta) requires an OTel collector to be standing up. Standing up the collector is parked under the engagement-internal post-M3 bead `kobiton-5cj.6` (rationale: pre-R3 the spans are referenced as architectural primitives, not as a measurement claim — no published numbers without the collector standup having actually happened).

When the collector standup lands, the test suite lands here, and at least one case-study conformance report has its results validated against this suite, the spec is promotion-eligible from `v0.1.0-draft` to `v0.1.0-rc`.

## RFC

If you have an existing OTel collector standup pattern that would be a good fit for the reference test suite, file a GitHub issue on [`jeremylongshore/intent-eval-lab`](https://github.com/jeremylongshore/intent-eval-lab) with `[mcp-plugin-observability]` in the title.
