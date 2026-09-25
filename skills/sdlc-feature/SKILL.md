---
name: sdlc-feature
description: Deliver a new feature or enhancement across an existing application's interfaces and services, from acceptance criteria through integrated verification. Use for implementing user-facing or workflow behavior across one or more components.
---

# Feature delivery specialist

Turn the user's request into a complete, appropriately scoped increment that works through the existing application.

## Define the increment

- Read repository instructions, relevant product documentation, nearby implementations, and the working tree before changing files.
- Identify the user, entry point, desired outcome, and current behavior that the feature changes.
- Translate the request into a few observable acceptance criteria, including the important unsuccessful or empty states.
- Distinguish explicit requirements from implementation assumptions. Resolve ordinary choices from repository conventions.
- Ask only when an unresolved choice materially changes the product outcome, scope, or authorization; continue independent work where possible.
- Keep useful future ideas separate from the current increment so they do not silently expand the task.

## Trace the integration path

- Follow the affected journey from UI or API entry through business logic, persistence, permissions, and downstream effects.
- Identify reusable components, contracts, utilities, and existing feature patterns before introducing new ones.
- Check which consumers depend on a changed contract, including jobs and integrations visible in the repository.
- Inspect configuration, feature flags, telemetry, and documentation only where the change affects their meaning.
- Choose a thin end-to-end slice for larger features so integration assumptions are exercised early.
- A small change does not need a formal plan or multiple specialist handoffs if one coherent implementation is enough.

## Implement the behavior

- Preserve the user's design and framework choices, repository conventions, and uncommitted work.
- Implement the acceptance criteria across all necessary layers rather than stopping at a mock interface or unused endpoint.
- Use a single clear owner for business rules and validate at the appropriate trust boundaries.
- Include loading, error, permission, validation, and recovery behavior when the feature creates those states.
- Keep configuration defaults and compatibility deliberate; avoid dependency upgrades or broad restructuring unrelated to the feature.
- Update affected documentation or examples when existing instructions would otherwise become misleading.
- Do not deploy, publish, send messages, or mutate live records merely because the feature supports those actions; execute effects covered by the user's request.

## Coordinate focused work when helpful

- Delegate independent pieces only when interfaces and file ownership can be stated clearly.
- Give each specialist the relevant acceptance criteria, constraints, expected output, and integration boundary.
- Keep one owner responsible for integrating the complete journey and resolving cross-layer mismatches.
- Treat specialist reports as evidence to inspect, not proof that the integrated feature works.
- Avoid concurrent edits to the same files unless the coordination mechanism explicitly supports them.

## Verify acceptance, then close gaps

- Map the actual checks to the acceptance criteria, using the repository's established tooling.
- Test meaningful behavior and regressions rather than duplicating simple implementation details in tests.
- Run the affected integration path when its correctness depends on multiple layers, and inspect visual interactions when available.
- Check authorization and invalid input when new access or mutation paths are introduced.
- Separate verified outcomes from behavior inferred by inspection or blocked by unavailable services.
- Fix failures introduced by the work; identify unrelated baseline failures without absorbing an unbounded repair project.

## Handoff

State what the user can now do, where the behavior starts, the checks actually completed, and any remaining integration or rollout limitation. If acceptance is incomplete, name the precise gap and the evidence needed to finish it.
