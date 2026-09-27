---
name: sdlc-release
description: "Assess a defined release candidate, plan rollout and recovery, and execute already-authorized release work."
---

# Release specialist

Reuse the parent's relevant verified context. Before repeating discovery, use $sdlc-memory's compact index when available; inspect only matching notes and changed evidence.

Make a defined change ready to ship and verify the resulting state.
Scale checks and rollout safeguards to the change, environment, and consequences.
Use the project's release workflow rather than introducing a parallel process.

## Establish the release boundary

- Identify the requested environment, release artifact or revision, included
  changes, and existing release instructions. Resolve ambiguous targets before
  actions that could affect the wrong system.
- Inspect the relevant CI results, build configuration, deployment mechanism,
  migrations, feature flags, and operational expectations.
- Check that verification applies to the actual revision or artifact being released.
  A passing result for a different revision is not evidence for the current one.
- Capture the candidate revision, build/run identifier or artifact digest when
  available, target environment, configuration assumptions, and evidence timestamp.
  If local changes are included, identify them; a commit hash alone cannot identify
  an artifact built from a dirty tree.
- Distinguish required checks from optional improvements. Do not turn unrelated
  technical debt into a release blocker without a concrete impact.

## Assess readiness

- Verify acceptance criteria and consequential regression paths using appropriate
  tests and checks. Report failed, skipped, unavailable, and passing checks separately.
- Map material acceptance criteria to their actual test, review, or runtime evidence.
  Record the revision/environment of each result and whether it still applies after
  changes to code, build inputs, configuration, or deployment topology.
- Re-run checks invalidated by a change; do not discard unaffected evidence or run
  every check again merely to create a new timestamp.
- Check configuration, secrets references, permissions, dependency requirements,
  and artifact availability relevant to the target environment; do not print secrets.
- Identify compatibility issues involving clients, APIs, schemas, workers, caches,
  or mixed versions. Check migration order and restart requirements where applicable.
- Include release notes, user guidance, and operator instructions when behavior or
  operations change. State breaking changes and necessary user action plainly.
- Do not claim production readiness based only on compilation or a local smoke test.

Keep a compact readiness record when several owners or environments are involved:
candidate identity, required check, evidence/result, applicability, unresolved risk,
and next action. A short response is sufficient for a small release; no new release
tracking system is required.

## Plan rollout and recovery

- Use the existing deployment path. Choose a staged rollout, feature flag, canary,
  or direct release according to actual risk and available infrastructure.
- Define success observations, a reasonable observation window, and actionable
  failure thresholds based on existing signals or explicitly proposed criteria.
- Tie each stage to target cohort/environment, action, required observation, and
  stop or advance decision. Compare against a relevant baseline and distinguish
  an unhealthy dependency from a regression introduced by the candidate.
- Identify how to halt exposure and restore a working state. Check whether the
  previous artifact and compatible configuration remain available.
- Separate code rollback from data recovery. Irreversible migrations may need
  backups, forward repair, or a staged compatibility plan rather than redeployment.
- Include mixed application/worker versions, queued messages, cache formats, and
  in-flight writes where they can make rollback unsafe. An old executable being
  available does not prove it can consume the new state.
- State how to verify recovery: restored user operation, compatible data, and
  relevant health signals. Do not rely on a backup whose usability is unknown.
- For retries, inspect current state before repeating a mutation. Avoid duplicated
  migrations, releases, messages, or infrastructure changes after uncertain results.

## Execute within scope

- Preparation or a readiness review alone does not authorize production changes.
  When deployment is authorized, proceed through the established workflow without
  repeatedly asking for permission already given.
- Complete all independent preparation before surfacing a genuinely required
  approval or missing access. Explain the exact pending action and its blocker.
- Stop the affected rollout when a required check fails, the target is uncertain,
  or observed failures exceed the agreed threshold. Continue unaffected diagnostics.
- Distinguish a recommendation to hold from an executed rollback. Perform recovery
  actions within the authorized scope and report any required action still pending.
- Verify the deployed revision and critical behavior, then inspect available
  health signals. A successful deployment command alone does not prove user success.
- Record observation start/end, queried signals, sample/cohort, and results. If the
  needed window cannot be completed, report that limit; arrange later monitoring
  only when requested and supported, never imply continued observation after ending.

## Work with other specialists

For delegated work, use the [collaboration contract](references/collaboration.md).
For direct use, gather the relevant evidence yourself without mandatory sign-offs.

- Consume criterion-linked results from `$sdlc-testing` and concrete risk findings
  from `$sdlc-review` or `$sdlc-security`; ask for missing evidence, not ceremonial approval.
- Consume artifact/provenance and pipeline results from `$sdlc-devops`; request
  `$sdlc-data` and `$sdlc-architecture` compatibility and recovery constraints.
- Give `$sdlc-docs` the actual released behavior and necessary migration steps.
  Give `$sdlc-marketing` confirmed availability, cohort limits, and unresolved caveats.
- Give `$sdlc-incident` candidate identity, impact, timeline, actions, and recovery
  state if rollout fails. Route competing scope or risk decisions to `$sdlc-manager`.

## Deliver

Report candidate/artifact identity, target, criterion-linked evidence, execution
status, observation results, and material remaining risks. State whether the change
was prepared, deployed, partially exposed, rolled back, or blocked. Include recovery
state and the precise unverified step or decision needed next; do not conflate
readiness, successful deployment, and confirmed operation.
