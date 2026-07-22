# `bbb-seed-v1` — corpus derivation allowlist

**Status:** NORMATIVE for `scripts/derive-corpus.ts`. The script reads this file's rules as code
(they are mirrored in `derive-corpus.ts` as `ALLOWLIST`); this document is the human-readable
statement of *why* each rule exists. If the two disagree, that is a bug — the script fails closed.

## The refusal that shapes everything

The live brain (`~/.teamkb/teamkb.db`) holds **17,321 curated memories, and every single one is
classified `sensitivity: 'internal'`**. Not one is `'public'`. Verified 2026-07-22:

```
sensitivity | lifecycle   | count
internal    | active      | 10128
internal    | superseded  |  6501
internal    | deprecated  |   681
internal    | archived    |    11
```

There is therefore **no schema-level `public` marker to filter on**. A public corpus cannot be
derived by trusting the brain's own governance label, because the label uniformly says "internal".
Any public `bbb-seed-v1` corpus is, by construction, a decision to publish content the brain's
governance layer classifies as internal.

**Consequence — the script never publishes.** `derive-corpus.ts` writes to a review directory and
emits a report. Promoting that output into `corpus/` (and therefore onto
`labs.intentsolutions.io`) is a **human decision requiring explicit operator sign-off**, recorded in
`corpus/PROVENANCE.md`. The script has no flag that skips this.

## Rule 1 — category allowlist (structural)

Only these `category` values are eligible:

| Category | Pool (active) | Why eligible |
|---|---|---|
| `pattern` | 580 | Generic engineering patterns — "Confused Deputy Problem", "Multi-Stage Docker Build", "pgvector Extension". Textbook-adjacent. |
| `architecture` | 94 | Design-shape notes about our own systems, already described publicly in the BBB READMEs. |
| `convention` | 34 | Team conventions — already public in `CONTRIBUTING.md` / commit standards. |
| `decision` | 48 | ADR-shaped records; the corresponding DRs are already public in `000-docs/`. |
| `onboarding` | 15 | Written for outsiders by definition. |

**`reference` (16,219 memories — 94% of the brain) is REFUSED wholesale.** It is the session-note
and scratch bulk: the highest-volume, lowest-curation, highest-risk stratum. No content-level scan
is trustworthy enough to release 16k unreviewed session notes on. Excluding it costs nothing — the
eval needs ~80 documents, and the 733 non-`reference` actives are more than sufficient.

Only `lifecycle = 'active'` is eligible. `superseded` / `deprecated` / `archived` memories are
excluded: publishing a frozen corpus of knowledge the brain has already retired would make the eval
measure retrieval against claims we no longer stand behind.

## Rule 2 — risk-marker refusal (content)

A memory is refused if its `title` or `content` matches **any** pattern below. These are refusal
rules, not redaction rules: the script does **not** attempt to scrub a match and keep the document.
Redaction invites the "we thought we caught it" failure; refusal cannot partially fail.

| Marker | Regex intent | Why refuse |
|---|---|---|
| `ip_address` | dotted quad | VPS / tailnet addressing. |
| `email` | address form | PII. |
| `abs_home_path` | `/home/<user>` | Leaks operator username + local layout. |
| `secret_kw` | `api[_-]?key`, `token`, `passphrase`, `password`, `secret`, `credential` | Refuse the *neighbourhood* of a secret, not just a matched secret — the words co-occur with the values. |
| `long_hex_or_b64` | `[A-Za-z0-9+/]{32,}={0,2}` | Shape of a key, hash, or token. |
| `person_name` | named individuals | PII; also partner-name discipline (DR-004 S1Q2). |
| `private_host` | internal hostnames, tailnet CIDR, hosting vendor | Infrastructure topology. |

Measured against the 733-memory eligible pool (2026-07-22): **608 carry zero markers**;
refusals are `secret_kw` 87, `private_host` 28, `long_hex_or_b64` 11, `person_name` 11,
`ip_address` 7, `abs_home_path` 2, `email` 0.

The marker list is deliberately **over-broad**. A false refusal costs one document out of a 608-deep
pool. A false accept is unrecoverable — published, and if it reaches a signed row, anchored in an
append-only transparency log that cannot be un-logged.

## Rule 3 — never write what was not matched

`derive-corpus.ts` emits a document **only** if it passed Rule 1 and Rule 2 explicitly. There is no
default-accept branch and no "unknown → include" path. Every emitted file is accompanied by its
decision record in `derivation-report.json`, so any published document can be traced to the rules
that admitted it.

## Rule 4 — hand review is mandatory and is not the script's job

The script's output is a **candidate set**. Sign-off means a human read every candidate. The count
is chosen so this is actually possible: ~80 documents averaging well under 1 KB (the gold-cited
subset measures 285–1,227 bytes) is roughly 60 KB of prose — an hour's careful reading, not a
rubber stamp.

## What the public corpus is FOR — and what it is not

`bbb-seed-v1` exists so that a stranger can reproduce a number we publish. It is a **frozen,
pinned, sanitized** artifact. It is not a mirror of the brain, not a backup, and not kept in sync.
The live-brain arm of every A/B axis runs against `~/.teamkb` directly and its rows land in
`site-internal/` only — that arm is where regressions on the real brain surface, and it is never
published.
