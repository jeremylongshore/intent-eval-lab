# `bbb-seed-v1/corpus/` — provenance and sign-off

**This directory is EMPTY and must stay empty until the sign-off below is recorded.**

## Why a sign-off is required

Every document that could go in here originates in the live governed brain, where **all 17,321
curated memories are classified `sensitivity: 'internal'` and none are `'public'`**. Publishing any
of it to `labs.intentsolutions.io` is a decision to release internally-classified content. No
script makes that decision — `scripts/derive-corpus.ts` writes only to the git-ignored `.candidate/`
and has no flag that targets this directory.

It is also effectively irreversible. The corpus feeds signed `gate-result/v1` rows; a signed row is
anchored in an append-only transparency log that **cannot be un-logged**. The retraction protocol
can return 410 at the deep URL and publish a tombstone, but it explicitly does not pretend the
entry never existed. Getting this wrong is not a rollback, it is a disclosure.

## Sign-off record

| Field | Value |
|---|---|
| Status | **NOT SIGNED OFF** |
| Reviewer | — |
| Date | — |
| Candidate set reviewed | — (derivation decision-set sha256: `3bdd76b436156435206059ac1f76c285ddfd4aac3c2f73ccaa0e1834da828837`) |
| Documents promoted | 0 |
| Escalations adjudicated | 0 of 5 |

### What sign-off attests

1. The reviewer **read every promoted document in full** — not sampled, not skimmed. The set is
   sized (~80 documents, ~60 KB) so this is genuinely possible.
2. Each promoted document is safe to publish under the reviewer's own judgement, independent of the
   automated scan. The scan is a filter, not an authority.
3. Each of the 5 escalations was adjudicated **individually and in writing** (table below), or its
   dependent queries were dropped from `questions.yaml`.

### Escalation adjudications

Documents that are gold-cited but were refused by `ALLOWLIST.md` Rule 2. Each needs an explicit
decision. `secret_kw` fires on subject matter here, not on a leaked value — but that judgement has
to be made by a person looking at the actual text, which is exactly why the script refuses to make it.

| Document | Refused by | Decision | Justification | Dependent queries |
|---|---|---|---|---|
| Compile-Then-Govern Architecture | `secret_kw` | *pending* | | q02, q13 |
| Token Passthrough | `secret_kw` | *pending* | | q28, q34 |
| Spool Boundary Threat Model | `secret_kw` | *pending* | | q36 |
| Double-Gate Pattern | `secret_kw` | *pending* | | q41 |
| Team mode is member-proposes / server-disposes | `private_host` | *pending* | | q14 |

Decision must be `ADMIT` (with justification) or `REFUSE` (dependent queries move to `blocked`
permanently, or the corpus gains a hand-written public substitute).

## Promotion procedure

Reviewed documents are promoted by **explicit `git add` of specific files**. Never
`git add .candidate/` — that directory is git-ignored precisely so a reflexive bulk add cannot
publish 80 internally-classified documents in one keystroke.

After promotion, generate `../MANIFEST.json` and confirm
`node ../scripts/verify-manifest.mjs` exits 0.
