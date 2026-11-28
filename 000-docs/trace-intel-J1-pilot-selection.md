# J1 — Proposed controlled pilot selection

**PROPOSED — UNSIGNED. No pilot start, provider call, architecture choice or production adoption is authorized by this document.**

Bead: `bd_000-projects-h08j.8.126`. Program: `bd_000-projects-h08j.8`. Prepared 2026-11-12 for owner review alongside [J2 criteria](./trace-intel-J2-pilot-criteria.md).

## Proposed single-agent, single-repository boundary

| Item                    | Proposed selection                                                                                                                                            |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| One logical pilot agent | J-Rig's binary-skill evaluator exposed as `j-rig eval`; one frozen evaluator configuration, not the optimizer, refiner, batch runner or multiple agent roster |
| One pilot repository    | `jeremylongshore/j-rig-skill-binary-eval`                                                                                                                     |
| Measured workload       | Normal evaluation work for one owner-enrolled skill and its reviewed evaluation specification; exact skill, revision and workload remain unset until approval |
| Observation mode        | Additional trace-to-evidence observation; existing repository checks, rollout decisions and delivery authority remain unchanged                               |
| Selection status        | Proposed candidate only; owner signature absent                                                                                                               |

The evaluator is the single logical agent being observed. The skill under test is its fixed workload, and an external judge is an existing evaluation dependency, not a second separately enrolled pilot agent. The enrollment must state this boundary explicitly; adding a second evaluated agent or repository requires a new owner decision. No provider/model, host, storage implementation, annotation product or signature scheme is selected here.

## Existing source basis

The inspected source snapshot is `01a52268883f6955c245289fc5bfe5be78ffa51f`. These are source observations, not proof the future program components are deployed:

- The actual [CLI registration](https://github.com/jeremylongshore/j-rig-skill-binary-eval/blob/01a52268883f6955c245289fc5bfe5be78ffa51f/packages/cli/src/index.ts#L30-L38) names the executable `j-rig` and registers `registerEvalCommand`.
- The [command implementation](https://github.com/jeremylongshore/j-rig-skill-binary-eval/blob/01a52268883f6955c245289fc5bfe5be78ffa51f/packages/cli/src/commands/eval.ts#L473-L509) declares `eval <skill-dir>`, explicit specification/model/provider options and kernel-validated bundle output. It also declares that regression and baseline layers are opt-in. The pilot must record actual coverage; it cannot claim all seven layers ran merely because the command exists.
- The [terminal contract](https://github.com/jeremylongshore/j-rig-skill-binary-eval/blob/01a52268883f6955c245289fc5bfe5be78ffa51f/packages/cli/src/commands/eval.ts#L1520-L1533) separates evaluated verdicts from infrastructure failures: exit zero may accompany pass, fail or advisory, exit two represents incomplete evaluation due to provider failure, and a caught crash exits one. Success criteria must read verified verdicts and provenance, not interpret exit zero as a passing skill.

This candidate offers a bounded repository and an existing evaluation/evidence boundary with useful failure signals. This is a rationale for proposing it, not an assertion that the owner has approved it or that all future trace, annotation and projection integrations already exist. No existing evaluator is replaced.

## Enrollment record required before execution

The owner-reviewed record must pin the repository commit, evaluator executable/artifact digest, one skill digest, evaluation specification, enabled/skipped layers, model and judge configurations, policy/taxonomy versions and allowed data classification. Record configuration references rather than credentials. The actual source revision must be requalified if it differs from the snapshot above.

The record must also identify the accountable operator, human reviewers, authorized execution budget, approved provider/network boundaries, retention/access policy, incident owner, exact start time and the separately authorized stop/rollback action. A zero budget or absent provider authorization means no provider calls. Synthetic/stub fixtures may qualify plumbing only; they cannot satisfy real-operation acceptance.

## Gates that this proposal does not satisfy

J1/J2 planning can proceed in parallel under the current dependency graph. Their existence does not open A3 or later implementation gates. A1/A2 and consolidated audit sign-off, research and architecture approvals, ratified contracts, the relevant implementation/integration/security work, I14 real dogfood, and J12/J13 reviews remain governed by the program and their canonical Beads dependencies. J14 must explicitly decide `adopt` before any J15 expansion. This proposal neither marks those tasks complete nor chooses their designs.

The separate fixture day and real seven-day observation in J2 are proposed execution plans for when their prerequisites and owner authorization are satisfied. They are not scheduled or started here.

## Owner decision — deliberately unexecuted

- Decision: **PENDING** (`approve selection`, `request revision` or `reject`).
- Owner identity: **not signed**.
- Signature or authenticated decision reference: **absent**.
- Decision timestamp and approved document commit: **unset**.
- Enrollment record and execution authorization: **absent**.

An agent must not fill these fields on the owner's behalf. A PR merge alone must not be interpreted as a pilot kickoff, budget authorization or J14 production-adoption decision. J1 remains open until its actual owner-selection acceptance is satisfied.
