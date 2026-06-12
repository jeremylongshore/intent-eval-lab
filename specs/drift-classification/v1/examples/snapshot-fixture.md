# Fixture — vendored snapshot stand-in (offline self-test corpus)

A miniature stand-in for a tier-2 vendored snapshot
(`specs/_vendor/<surface-id>/snapshot.md`), used by
`scripts/classifier-walls.py --self-test` to exercise the literal-substring
pre-wall deterministically and offline. Shaped like the agentskills.io
frontmatter field table the projection differ parses.

## Frontmatter fields

| Field | Required | Constraints |
|---|---|---|
| `name` | Yes | max 64 characters |
| `description` | Yes | max 1024 characters |
| `allowed-tools` | No | experimental — space-separated list |
| `version` | No | semantic version string |
| `license` | No | SPDX identifier |
