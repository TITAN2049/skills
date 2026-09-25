---
name: sdlc-architecture
description: "Design and review software architecture, data contracts, integrations, and migration plans for a concrete change. Use when boundaries, compatibility, scaling, or system tradeoffs need a decision."
---

# Architecture specialist

Choose a design that fits the current system and the requested outcome.
The deliverable is an implementable decision, not a diagram collection.

## Inspect before designing

- Read repository instructions, entry points, dependency manifests, existing
  abstractions, data models, tests, and deployment configuration relevant to the change.
- Trace a representative request or event through the actual system. Record
  discovered boundaries and conventions rather than inferring them from names.
- Identify constraints on deployment, data ownership, latency, tenancy, cost,
  operational capacity, and backward compatibility when they affect this decision.
- Separate observed constraints from forecasts. Do not assume hypothetical scale
  requires a new service, queue, database, or framework.

## Make the decision

- Start with extending the existing design. Propose a new abstraction or service
  when a concrete boundary, repeated need, or demonstrated constraint justifies it.
- Compare credible alternatives when the tradeoff is consequential. Explain why
  the recommended option fits and what cost or limitation it accepts.
- Prefer reversible choices for uncertain requirements. Avoid combining a feature
  with an unrelated rewrite, dependency migration, or infrastructure replacement.
- Define ownership of data and responsibilities at boundaries. Specify relevant
  contracts, validation, authorization, errors, and consistency expectations.
- For concurrent or asynchronous work, consider duplicate delivery, retry bounds,
  idempotency, ordering, timeouts, and partial failure where applicable.

## Plan compatibility and operations

- Check readers, writers, clients, and downstream consumers before changing a
  schema or contract. Make breaking behavior explicit.
- For live migrations, consider mixed application versions and partially migrated
  data. Use staged expansion and later cleanup when compatibility requires it.
- Specify how to detect failure and recover. A code rollback may not reverse data
  changes; describe restoration or forward repair when that distinction matters.
- Include logs, metrics, traces, or alerts only for actionable operational questions.
  Avoid adding observability without an owner or a useful response.
- Distinguish capacity estimates from measured performance. Propose a targeted
  measurement or experiment when evidence is needed to choose the design.

## Turn design into work

- Map the design to concrete modules, contracts, migrations, and deployment steps.
- Identify a small first slice that validates the riskiest assumption early.
- State the tests needed to protect cross-boundary behavior and compatibility.
- Implement the agreed scope when asked to build or fix; do not stop at a design
  document when implementation is already authorized.

## Deliver

Summarize the current constraint, decision, rationale, affected boundaries, and
remaining uncertainty. Add a compact diagram when it clarifies a data flow or
ownership boundary. Use the project's existing decision-record convention when
there is a durable decision worth recording; a small change may need only prose.
Report which conclusions come from code inspection, execution, or assumptions.
