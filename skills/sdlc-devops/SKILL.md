---
name: sdlc-devops
description: Build or repair CI pipelines, reproducible development environments, build systems, containers, and infrastructure configuration. Use for delivery infrastructure engineering; release decisions and deployment execution require their own applicable task scope and authorization.
---

# SDLC DevOps

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
- Keep generated artifacts and dependency caches distinct; account for OS, toolchain, and lockfile changes in cache identity.
- Make working directories, required environment variables, and service prerequisites explicit where ambiguity caused failure.
- Avoid embedding credentials in images, repository files, logs, or command arguments.
- Use existing secret references; document required names without supplying real secret values.
- Ensure local instructions and CI commands describe the same build contract where practical.

## Engineer CI changes

- Trace workflow triggers, job dependencies, permissions, concurrency, and artifact flow before editing.
- Consider pull requests from untrusted forks when choosing secret access and workflow execution context.
- Grant only the permissions the changed job needs, preserving necessary behavior for existing workflows.
- Keep required checks meaningful; do not suppress failures or remove protection to obtain a green pipeline.
- Use timeouts, retry rules, and cancellation according to failure behavior and operation idempotency.
- Avoid parallelizing jobs that share mutable state or depend on ordered side effects.
- Verify required jobs still run under path filters and conditional expressions relevant to supported triggers.

## Engineer environment and infrastructure changes

- Match existing state, provider, workspace, and environment separation conventions.
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
- Distinguish locally validated configuration from a successfully executed remote pipeline.
- If a remote run is authorized, inspect its final result and address failures caused by the change.
- Bound retries and stop when repeated failure requires changed input or external intervention.

## Handoff

Describe what now builds or runs, the configuration changed, and checks actually performed.
Identify required environment or secret names, remaining prerequisites, and any unexecuted shared-environment action.
Include recovery considerations when the change affects deployed infrastructure or persistent state.
