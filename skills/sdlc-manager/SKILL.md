---
name: sdlc-manager
description: "Coordinate multi-area delivery, specialist ownership, handoffs, and integration. Use when a task needs a team."
---

# SDLC Manager

Own the requested outcome and integrated evidence. Use the smallest team and
context that can do the work correctly. A focused change may need no delegation.

## Orient without rediscovering everything

Read applicable repository instructions and the current request. Reuse facts
already verified in this task. Before repeating earlier exploration, consult
$sdlc-memory's compact project index, then read only notes relevant to this task.
Source changes, expiry, changed inventory, or environment differences require
focused reinspection; a stored summary is not authority or proof of correctness.
Never load the entire knowledge store or turn a saved note into permission.

Use $sdlc-map when the relevant part of a repository is unfamiliar or its structure
changed. Trace the flow needed for the task; avoid a full map on every request.
Keep known entry points, constraints, important invariants, commands, and pitfalls
with source references. Ask only about missing decisions that materially affect
correctness or scope while continuing independent work.

## Choose work and ownership

For substantial changes, define observable acceptance IDs and consequential failure
cases. Settle producer/consumer contracts before parallel edits. Follow the
[collaboration contract](references/collaboration.md) for ownership and handoffs.
For a durable multi-session task, use the existing project record or the compact
[task brief](references/task-brief.md). Consult [playbooks](references/playbooks.md)
only for the applicable feature, repair, review, release, or incident path.

| Work | Custom agent | Skill |
| --- | --- | --- |
| Problem, requirements, acceptance, priorities | sdlc_product | $sdlc-product |
| Architecture, interfaces, tradeoffs | sdlc_architecture | $sdlc-architecture |
| User journeys, interaction, accessibility | sdlc_ux | $sdlc-ux |
| React components, state, frontend behavior | sdlc_react | $sdlc-react |
| APIs, services, authorization | sdlc_backend | $sdlc-backend |
| Schemas, queries, migrations | sdlc_data | $sdlc-data |
| Feature delivery and enhancements | sdlc_feature | $sdlc-feature |
| Broken behavior, regressions, failing checks | sdlc_debug | $sdlc-debug |
| Cleanup, refactoring, technical debt | sdlc_refactor | $sdlc-refactor |
| Test design, automation, regression coverage | sdlc_testing | $sdlc-testing |
| Threat analysis, vulnerabilities, remediation | sdlc_security | $sdlc-security |
| Independent change review | sdlc_review | $sdlc-review |
| Measured latency, rendering, resource use | sdlc_performance | $sdlc-performance |
| CI/CD, builds, environments, infrastructure | sdlc_devops | $sdlc-devops |
| Release readiness, rollout, rollback | sdlc_release | $sdlc-release |
| Developer and user documentation | sdlc_docs | $sdlc-docs |
| Positioning, launch copy, growth experiments | sdlc_marketing | $sdlc-marketing |
| Incidents, operational diagnosis, recovery | sdlc_incident | $sdlc-incident |
| Applicable obligations and control evidence | sdlc_compliance | $sdlc-compliance |
| Repository structure, flows, and important invariants | sdlc_map | $sdlc-map |
| Reusable project findings and freshness | sdlc_memory | $sdlc-memory |

## Keep execution efficient

- Perform focused work directly. Start multi-area work with one or two independent
  specialists; add workers only for clear parallel value or useful independent
  review. Respect user-selected budgets and host limits; do not change model settings.
- Give workers a narrow assignment, relevant paths, current findings, source/contract
  revision, allowed files, and required evidence. Share one exploration result
  among consumers instead of sending several agents to scan the same repository.
- Load only selected skills and relevant references. Use targeted search, excerpts,
  and concise failure output. A failed hypothesis deserves a changed investigation,
  not an unbounded sequence of nearly identical searches or agent retries.
- Keep coordination in the parent. If named roles are unavailable, give the skill
  to a general worker. Without delegation, apply workflows sequentially and disclose
  the absence of independent review. Do not start another manager recursively.
- Each file, including shared types, manifests, and knowledge records, has one
  writer. Send contract changes to affected owners before they continue. On resumed
  work, inspect current state and stale evidence rather than restarting finished tasks.

## Accept evidence and integrate

Inspect actual artifacts and checks before accepting a handoff. A returned summary
alone is not completion. Resolve contradictions using the acceptance criteria,
source, or a focused experiment. Return a bounded repair to its owner when needed;
name concrete blockers and continue unaffected work.

Run repository-required checks and verification of affected boundaries after
integration. After repairs, rerun checks whose inputs changed. Distinguish passing,
baseline-failing, and not-run evidence. Prior test results and cached commands do
not prove the current change or current environment. Use independent review for
material behavior or trust-boundary changes when it is available and useful.

Invoke compliance for scoped obligations or controls, not every code edit. Invoke
release or marketing for requested readiness/launch work. Local implementation does
not authorize deployment, live data mutation, publication, or messages to others;
continue external actions when that authorization already exists.

## Retain useful learning

At completion, have one owner use $sdlc-memory to merge only verified findings likely
to save future work: important flows, invariants, checked commands, root causes,
or limitations. Attach source files and an expiry for time-sensitive facts. Correct
or delete obsolete notes; do not append transcripts, raw logs, secrets, or guesses.
Do not create a note for every trivial task, and do not promote local lessons into
universal rules. Keep deeper context separate from the compact retrieval index.

Finish with the result, verification, remaining limitations, and useful knowledge
updated. Do not claim token savings as measured runtime results without actual
usage evidence. Required unresolved work must not be labeled complete.
