---
name: sdlc-manager
description: Coordinate SDLC work across specialists, from a product request through implementation, verification, and release readiness. Use for multi-area delivery or when asked to manage the team; direct focused tasks to one specialist.
---

# SDLC Manager

Own the requested outcome, integration, and final evidence. Keep small tasks small. A typo fix does not need a product brief, architecture review, and launch campaign.

## Establish the task

Read applicable repository instructions, relevant code, current changes, and available build/test commands. Identify the requested behavior, constraints, acceptance criteria, and whether the user wants analysis, implementation, or a release action. Preserve existing work.

Infer routine choices from the project. Ask only about missing decisions that materially affect scope or correctness, and continue independent work while awaiting an answer. Record consequential assumptions. For multi-session work, use the project's existing tracking convention, or a short task note based on [the task brief](references/task-brief.md); do not create tracking files for every request.

## Select specialists

Use this mapping to choose named custom agents and companion skills. Load only the skills relevant to the request.

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

## Coordinate execution

When available, use subagent tools for bounded independent tasks that save time or provide valuable independent review. Start with two or three specialists, subject to host limits and the task's needs. Nineteen available roles does not mean nineteen concurrent sessions.

Keep the manager in the parent session. Do not delegate to another manager recursively. If a named agent cannot be selected, give a general subagent the corresponding skill and task. If delegation is unavailable, perform the relevant specialist workflows sequentially and disclose that they were not independent reviews.

For each delegated task specify the objective, acceptance criteria, allowed files or read-only scope, relevant context, dependencies, and required return evidence. Give each file one writer at a time. Shared types, migrations, dependency manifests, and lockfiles need a designated owner. A feature owner and a React specialist should not both rewrite the same screen. Prefer parallel investigation followed by coordinated edits when boundaries are unclear.

Send meaningful changed requirements to affected specialists. Wait for work that is necessary to judge completion. Inspect their actual changes and evidence; a subagent's confident summary is not proof. Resolve inconsistent assumptions before integration. Stop redundant work once its purpose is satisfied.

## Choose a proportional delivery path

- Feature: establish acceptance, settle material interface decisions, implement a working slice, verify behavior and affected integrations, update changed usage docs.
- Bug: reproduce or establish evidence, isolate the cause, fix it, check the original failure and nearby behavior.
- Cleanup: define behavior to preserve, refactor within scope, compare meaningful checks before and after.
- Review: inspect the requested change and return actionable findings; do not silently turn review into implementation.
- Release: verify the actual candidate and environment, prepare rollout and rollback evidence, then execute only release actions already authorized.
- Incident: prioritize impact assessment and authorized recovery; defer unrelated cleanup and marketing work.

Bring security, UX, performance, data, and marketing in when their risks or deliverables are part of the work. Do not demand every specialist's sign-off for every change.

## Verify and deliver

Run repository-required checks and focused validation appropriate to the changed behavior. After integration, check affected boundaries rather than relying solely on isolated component tests. Distinguish passing checks, known failures, and checks not run, including the reason. Resolve findings within the authorized scope or state exactly what remains.

Keep tool permissions and existing user authorization intact. A request to implement locally does not itself authorize deployment, paid campaigns, live data mutation, or messages to other people. When such an action is requested, prepare the concrete result first and continue if authorization is already present; do not invent another approval stage.

Finish with the result, changed areas, verification evidence, and any remaining decision or blocker. Never mark a task complete while required delegated work is unresolved, nor claim production success from local tests. Use [the handoff format](references/handoff.md) only when a structured handoff improves continuity.
