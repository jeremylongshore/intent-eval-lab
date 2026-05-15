# Known Issues

Operational issues affecting the IEP ecosystem that are not platform-spec concerns. Moved out of the canonical glossary so the glossary surface stays focused on platform terminology.

## bd auto-flush JSONL drift (upstream `bd` tool bug)

**Status:** Open, tracked at `bd_000-projects-ufc`.

**Behavior:** `bd`'s auto-export step fails on `git-add` when `.beads/` is gitignored, silently losing in-memory writes between sessions.

**Workaround:** Apply the `bd export → cp → bd import` cycle atomically when state changes need to be persisted across the auto-flush boundary. Wrap in a shell function with an `EXIT` trap rather than relying on operator memory:

```bash
bd-safe() {
  (
    trap 'bd export > /tmp/bd-snapshot.jsonl && \cp -f /tmp/bd-snapshot.jsonl .beads/issues.jsonl && bd import .beads/issues.jsonl' EXIT
    "$@"
  )
}
```

The subshell wrapper `( ... )` is load-bearing: a bare `trap ... EXIT` inside a function fires when the shell *session* exits (not when the function returns) and also clobbers any existing `EXIT` trap. The subshell scopes the trap so it fires immediately after `"$@"` completes, regardless of the parent shell's other traps.

**Audit-trail caveat:** until the upstream fix lands, the workaround is operator-dependent. A session that crashes after a bead state mutation but before the trap fires will leave the canonical bd state behind the GH/Plane mirrors. For audit-grade reconstruction, treat any bead state change made after the most recent successful `bd export → cp → bd import` cycle as provisional until manually verified.

**Upstream:** https://github.com/steveyegge/beads (file the bug there when the draft email at `/home/jeremy/.claude/projects/-home-jeremy-000-projects-intent-eval-platform/memory/` is ready to send)
