---
name: sdlc-incident
description: "Diagnose operational incidents, coordinate authorized mitigation, and verify recovery with observable signals."
---

# SDLC Incident

Reuse the parent's relevant verified context. Before repeating discovery, use $sdlc-memory's compact index when available; inspect only matching notes and changed evidence.

Reduce user impact while preserving enough evidence to understand what failed.
Separate observed facts, working hypotheses, mitigation, and permanent repair.

## Establish operational context

- Identify the affected service, environment, symptoms, onset, and known user impact.
- Check the request and existing runbooks for authorized actions and operational constraints.
- Start with read-only health, logs, metrics, traces, recent changes, and dependency status available in scope.
- Record timestamps with a timezone and distinguish event time from observation time.
- If information is missing, pursue independent diagnostics while surfacing only questions that block safe progress.
- Do not infer permission to change production from permission to investigate.

## Build a useful timeline

- Capture the first known failure, last known healthy state, relevant changes, and mitigation attempts.
- State which requests, tenants, regions, or components are affected when evidence supports that scope.
- Include the source of each key observation and known clock skew or telemetry delay; absence of recent logs may reflect collection failure rather than recovery.
- Correlate symptoms across dependencies without treating temporal correlation as proof of causation.
- Preserve useful evidence before actions that erase logs, restart processes, or overwrite state.
- Redact credentials and unnecessary personal data from notes and copied diagnostic output.
- Keep notes concise enough to remain useful during an active incident.

## Test hypotheses efficiently

- Prioritize hypotheses by likely impact, supporting evidence, and cost of a discriminating check.
- Maintain competing explanations when the cause is uncertain, including evidence for and against each and the next observation that could distinguish them.
- Use targeted queries and bounded samples rather than repeatedly dumping entire logs.
- Check shared dependencies and recent configuration or rollout changes when the failure pattern points there.
- Separate the primary failure from secondary symptoms caused by retries, timeouts, or overload.
- Avoid probes that materially worsen load or create customer-visible effects outside authorized scope.
- Stop repeating an unchanged diagnostic after it no longer adds evidence.
- Preserve uncertainty when several actions or system changes overlap; a recovery after intervention does not by itself establish root cause.

## Mitigate within authorization

- Prefer a reversible intervention that addresses the observed failure and has an observable success criterion.
- Before an intervention, define the health signal, expected response window, stop or rollback threshold, and how prior state can actually be restored.
- Follow applicable runbooks while checking that their assumptions match the present system.
- Consider rollback compatibility, persistent state, in-flight operations, and dependent consumers before changing traffic or versions.
- Check whether a previous migration, external side effect, or destructive operation makes rollback ineffective; use containment or forward repair when restoration would worsen impact.
- If authorization is missing, prepare a concrete action, expected benefit, risks, and recovery path for the user to review.
- For an authorized intervention, make one causally useful change at a time when incident urgency permits.
- Do not repeatedly retry non-idempotent operations or unknown-result writes; establish state before retrying.
- Bound attempts and stop when the action worsens health, violates a runbook limit, or requires unavailable authority.
- Do not send incident messages, page others, or change shared systems beyond the user's existing authorization.

## Confirm recovery

- Check both infrastructure health and the affected user operation; process uptime alone does not prove recovery.
- Compare errors, latency, throughput, backlog, and data integrity signals relevant to the failure.
- Validate successful work at representative demand and across the affected segments; falling error counts can result from lost traffic or disabled functionality.
- Observe for a period appropriate to the failure mode rather than declaring recovery after a single success.
- State whether recovery is confirmed, partial, temporary, or still uncertain.
- Distinguish immediate mitigation from root-cause repair; complete the latter when it is part of the task.

## Work with other specialists

Use the [collaboration contract](references/collaboration.md) for bounded incident assignments; a direct incident task does not require forming a team.
Route conflicting changes and shared ownership through `$sdlc-manager`; give one owner each intervention and avoid recursive delegation.

- Give `$sdlc-devops` a failing component, timeline, runtime evidence, and authorized mitigation boundary; require the action, resulting state, health evidence, and rollback state back.
- Give `$sdlc-debug` a reproducible post-mitigation defect and relevant timeline to investigate permanent repair without disturbing the active recovery path.
- Give `$sdlc-security` evidence of suspected compromise, or `$sdlc-data` observed integrity/replication damage, when specialist diagnosis changes containment; avoid unsupported attribution.
- Give `$sdlc-release` candidate rollback or forward-fix compatibility and health evidence when a coordinated rollout is already in scope.

## Handoff

Lead with current impact and recovery status, then the evidence-backed timeline and actions taken.
Include exact relevant commands or change references, outcomes, remaining uncertainty, and rollback state.
Recommend follow-up repairs tied to demonstrated causes and detection gaps rather than generic process additions.
Identify whether the immediate recovery acceptance is met separately from whether root cause and permanent repair are complete.
If follow-up monitoring is requested, use available scheduling tools and define meaningful notification conditions; do not claim ongoing observation after the task ends.
