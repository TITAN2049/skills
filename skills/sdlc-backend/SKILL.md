---
name: sdlc-backend
description: Implement and diagnose APIs, services, background jobs, and server integrations with attention to contracts, authorization, consistency, and failure handling. Use when the requested change primarily affects server behavior.
---

# Backend specialist

Deliver the requested server behavior with explicit contracts and predictable failure modes.

## Trace the existing contract

- Read repository instructions, service entry points, dependency manifests, configuration examples, and relevant tests.
- Follow one request or job through validation, authentication, authorization, business rules, storage, and response mapping.
- Identify current callers, schemas, status codes, retry expectations, error formats, and compatibility requirements.
- Separate facts found in code from assumptions about deployed infrastructure or external services.
- Identify whether commands target a disposable local environment, shared staging, or production before executing operations with effects.

## Design the smallest compatible change

- State the input, successful output, failure behavior, and business invariant affected by the request.
- Validate at trust boundaries and enforce authorization on the server, including ownership or tenant scope where applicable.
- Use established service and persistence boundaries. Avoid introducing a new framework or generic repository layer for a narrow change.
- Check absent versus null values, partial updates, pagination, time zones, and numeric precision when relevant to the contract.
- Preserve compatibility for existing consumers, or make an explicitly requested breaking change visible in documentation and migration guidance.
- Keep error responses useful to callers without exposing secrets, internal queries, or sensitive records.

## Handle side effects and consistency

- Define the transaction boundary around the business invariant, not around an arbitrary function boundary.
- Consider duplicate delivery, retries, partial completion, and concurrency for mutations and background jobs.
- Reuse established idempotency and locking mechanisms; add them when a concrete operation can otherwise apply the same effect twice.
- Avoid claiming exactly-once behavior unless the complete processing path actually guarantees it.
- Give outbound calls bounded timeouts and retries appropriate to the operation. Do not retry non-idempotent actions blindly.
- Keep external calls out of long database transactions where the existing architecture permits a safer arrangement.
- For schema changes, inspect rollout order and old/new service compatibility; include a recovery path proportional to the change.
- Distinguish a code change or local dry run from actually sending notifications, charging money, deleting records, or deploying.
- Perform external mutations only within the user's authorized target and effect; existing authorization remains valid.

## Make operation diagnosable

- Use existing structured logs, correlation identifiers, metrics, and error reporting where they help diagnose the changed behavior.
- Never log credentials or full sensitive payloads merely to ease debugging.
- Check query count, bounded work, request size, and resource cleanup for paths whose load could grow with user input.
- Record new configuration keys and defaults without changing unrelated environments or secret values.

## Verify at the right boundary

- Run the checks supported by the repository and justified by the changed behavior.
- Test meaningful contract and invariant cases, especially authorization failures, duplicate execution, and transaction failure when affected.
- Prefer integration evidence for changes whose correctness depends on a real database, queue, or serialization boundary.
- Use mocks for a clear boundary, but do not present mock-only success as evidence of a live integration working.
- Check migration compatibility and rollback or forward recovery without executing unauthorized live changes.
- Report skipped checks and unavailable dependencies explicitly rather than substituting invented commands or results.

## Handoff

Summarize the caller-visible change, compatibility impact, verification evidence, and any deployment or configuration action still needed. For unresolved failures, include the smallest reproducible input and the observed response.
