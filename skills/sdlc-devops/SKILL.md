---
name: sdlc-devops
description: "Improve builds, CI/CD, environments, and infrastructure using reproducible artifacts and scoped operations."
---

# SDLC DevOps

Reuse the parent's relevant verified context. Before repeating discovery, use $sdlc-memory's compact index when available; inspect only matching notes and changed evidence.

Make builds, checks, and environments reproducible using the project's existing delivery system.
Separate preparing a configuration change from applying it to a shared environment.

## Discover the system

- Read manifests, lockfiles, tool versions, workflow files, container definitions, and infrastructure modules relevant to the request.
- Identify the supported developer and CI commands, required services, and artifact consumers.
- Determine the failure stage: dependency resolution, build, checks, packaging, configuration, or infrastructure execution.
- Compare local and CI environments before changing application code to compensate for infrastructure drift.
- Preserve the repository's provider and package manager choices unless the task calls for a migration.

## Build reproducibly

- Use supported pinned versions or repository version policy and committed lockfiles.
- Identify every build input that can affect output, including generated code, downloaded tools, platform, and build-time configuration; investigate unexplained clean-versus-cached differences.
- Keep generated artifacts and dependency caches distinct; account for OS, toolchain, and lockfile changes in cache identity.
- Make working directories, required environment variables, and service prerequisites explicit where ambiguity caused failure.
- Avoid embedding credentials in images, repository files, logs, or command arguments.
- Use existing secret references; document required names without supplying real secret values.
- Ensure local instructions and CI commands describe the same build contract where practical.
- Tie artifacts to source revision and producing run. Record immutable identifiers or checksums when downstream consumers need to verify exactly what was tested.

## Engineer CI changes

- Trace workflow triggers, job dependencies, permissions, concurrency, and artifact flow before editing.
- Consider pull requests from untrusted forks when choosing secret access and workflow execution context.
- Trace what code runs under a privileged token, including checked-out pull request code, scripts, plugins, downloaded artifacts, and restored caches; a trusted trigger does not make every input trusted.
- Grant only the permissions the changed job needs, preserving necessary behavior for existing workflows.
- Keep credential scope and lifetime tied to the job or environment that needs it; prefer the repository's existing short-lived identity mechanism where supported.
- Keep required checks meaningful; do not suppress failures or remove protection to obtain a green pipeline.
- Use timeouts, retry rules, and cancellation according to failure behavior and operation idempotency.
- Avoid parallelizing jobs that share mutable state or depend on ordered side effects.
- Verify required jobs still run under path filters and conditional expressions relevant to supported triggers.
- Verify each artifact consumer reads the intended producer's successful output from the correct revision, platform, and environment rather than an ambiguous latest match.

## Engineer environment and infrastructure changes

- Match existing state, provider, workspace, and environment separation conventions.
- Check persistent state locks, concurrent writers, and provider version constraints before changing execution order or running infrastructure commands.
- Inspect plans or diffs for replacements, deletions, access changes, and unexpected resources before any authorized apply.
- Prefer reversible, incremental changes with a recovery path proportionate to impact.
- Treat a build, validation, plan, deployment, and migration as different operations with different side effects.
- Check whether ostensibly diagnostic commands contact live services, acquire locks, or mutate state.
- Complete local configuration, documentation, and validation before seeking any genuinely missing execution authorization.
- Do not deploy, apply shared infrastructure, publish artifacts, or rotate credentials unless the current task already authorizes it.

## Verify the changed path

- Run available syntax, schema, formatter, build, or infrastructure validation relevant to the edit.
- Use the actual workflow or provider validator where available; generic YAML parsing cannot prove workflow correctness.
- Exercise a clean dependency install or container build when that is the failure being repaired and resources permit.
- Check both clean and cache-hit behavior when cache correctness changed; a warm local build cannot establish reproducibility from a clean checkout.
- Distinguish locally validated configuration from a successfully executed remote pipeline.
- If a remote run is authorized, inspect its final result and address failures caused by the change.
- Bound retries and stop when repeated failure requires changed input or external intervention.

## Work with other specialists

Use the [collaboration contract](references/collaboration.md) when infrastructure work feeds another task; direct pipeline repairs need no separate team.
Coordinate shared configuration ownership through `$sdlc-manager`; do not recursively delegate a delivery team.

- Give `$sdlc-testing` the supported command, runtime/service prerequisites, and failing CI evidence when application versus environment failure is unclear; receive a reproducible behavioral result.
- Give `$sdlc-security` the concrete privileged execution path, input provenance, and token permissions when a trust boundary needs assessment.
- Give `$sdlc-release` the immutable candidate artifact, producing revision/run, completed checks, environment prerequisites, and recovery constraints; release coordination retains rollout decisions.
- Give `$sdlc-incident` diagnostic or mitigation results when an active service failure is driving the infrastructure change, including observed health and reversible state.

## Handoff

Describe what now builds or runs, the configuration changed, and checks actually performed.
Identify required environment or secret names, remaining prerequisites, and any unexecuted shared-environment action.
Include recovery considerations when the change affects deployed infrastructure or persistent state.
Distinguish configuration validity, local build success, remote job success, and readiness of the artifact consumed downstream.
