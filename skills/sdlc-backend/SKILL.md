---
name: sdlc-backend
description: "Implement or diagnose APIs, services, and jobs with resource authorization, consistency, and failure handling."
---

# Backend specialist

Reuse the parent's relevant verified context. Before repeating discovery, use $sdlc-memory's compact index when available; inspect only matching notes and changed evidence.

Deliver server behavior that remains correct at the authorization, persistence, and external-service boundaries. Keep analysis and review requests read-only unless fixes are authorized.

## Establish inputs and runtime facts

- Identify the caller, operation, expected result, business invariant, allowed files, compatibility constraints, and permitted environment/effects.
- Read repository instructions, current changes, entry points, manifests, lockfile resolutions, runtime configuration, and CI/test commands. Discover actual framework, database client, queue, and runtime versions before selecting APIs.
- Trace one request/job through identity, validation, policy, business logic, storage, external effects, and response/acknowledgement.
- Inspect current callers and schemas. Agree input fields, absent-versus-null behavior, successful output, error codes, pagination, and time/number representations where affected.
- Separate repository evidence from assumptions about deployed topology. Verify target environment identity before commands that mutate shared resources.

## Enforce the actual access rule

- Authenticate using the existing trusted identity path. Do not derive ownership or tenant identity from an untrusted body or query field merely because the client supplied it.
- Authorize the operation on the requested resource and fields. Cover list, aggregate, export, batch, and background paths as well as the single-record endpoint.
- Scope reads and writes consistently; checking ownership and later updating by an unrestricted identifier can create a race or bypass.
- Prevent mass assignment by selecting accepted fields or using the established validated schema. Distinguish fields a caller may read from those they may change.
- Preserve deliberate not-found/forbidden behavior and avoid new existence leaks. Reject invalid input before costly or irreversible work where the contract permits.

## Preserve contracts and failure meaning

- Place business rules at a clear owner and use the repository's service boundaries. Do not introduce a new framework or generic abstraction for one endpoint.
- Distinguish validation failure, authorization denial, business conflict, unavailable dependency, and unexpected internal failure using the application's existing error contract.
- Give clients enough stable information to recover without exposing stack traces, credentials, queries, or sensitive records. Keep correlation context in the existing observability path.
- A timeout can mean the remote side committed but the response was lost. Represent an uncertain outcome accurately; do not translate every timeout into permission to repeat the mutation.
- Preserve compatibility for existing consumers, or document and coordinate the explicitly requested breaking change before dependent implementation.

## Make retries and side effects deliberate

- Set a bounded time budget for outbound work. Retry only transient failures for operations whose repeat behavior is safe; respect server retry guidance and use bounded backoff/jitter where the client supports it.
- Avoid retry multiplication across HTTP clients, service code, and queue consumers. Identify the layer responsible for the attempt budget.
- Distinguish naturally idempotent state-setting from operations that need duplicate-effect protection. When idempotency keys are needed, define key scope, lifetime, payload matching, concurrent claims, stored outcome, and behavior after uncertain completion. A request-local flag does not protect two workers.
- Put the transaction boundary around the invariant. Use database constraints or appropriate concurrency control for cross-request guarantees rather than relying on an earlier read.
- Keep external calls out of long transactions where possible. When a durable write must cause a durable message, evaluate the existing outbox/workflow mechanism instead of claiming an in-memory follow-up is atomic.
- For queue work, identify acknowledgement timing, duplicate delivery, poison-message handling, and restart behavior. Do not claim exactly-once processing from an at-least-once transport.
- Cancellation or client disconnect does not prove a side effect was undone. Finish or reconcile according to the operation's contract.
- Separate code/local dry runs from live notifications, charges, deployment, and data mutation; execute only effects covered by existing user authorization.

## Bound cost and make failures diagnosable

- Check query count, batch size, pagination, fan-out, input size, and resource cleanup where user input can multiply work.
- Reuse structured logs, trace context, metrics, and error reporting that can distinguish attempts from completed business operations. Redact sensitive values.
- Record changed configuration and operational defaults. Do not quietly alter unrelated environments, retries, or dependency versions.
- If persistent state changes, settle schema compatibility and service rollout order before presenting the implementation as deployable.

## Work with other specialists

Use the [collaboration contract](references/collaboration.md). Route additional specialist requests through the parent/manager and respect assigned file ownership; do not recursively create a team. In direct use, apply a needed companion workflow sequentially when delegation is unavailable.

| Trigger | Companion and concrete agreement |
| --- | --- |
| Schema, transaction, index, or backfill changes | Ask `$sdlc-data` for invariant enforcement, old/new reader-writer compatibility, migration ordering, and recovery limits. Designate one migration writer. |
| A UI or external consumer depends on the API | Send `$sdlc-react` or `$sdlc-feature` request/response/error examples, authorization behavior, retry semantics, and the status of shared types. |
| A new trust boundary, privilege rule, or sensitive integration appears | Ask `$sdlc-security` to inspect the specific actor/resource/action path and data exposure. |
| Concurrency or integration verification needs independent work | Give `$sdlc-testing` the invariant, failure schedule, service fixtures, and test-file ownership. |
| Deployment/configuration changes are required | Send `$sdlc-devops` and, when release is requested, `$sdlc-release` exact configuration and ordering requirements; this is not an implicit deployment request. |

Return material contract changes before consumers build against obsolete assumptions. Own server correctness; the parent owns acceptance of cross-layer integration.

## Verify and return completion evidence

- Use repository-supported checks at the boundary that enforces correctness. Mocks can establish call behavior but do not prove database constraints, queue delivery, or a live integration.
- Where affected, cover anonymous/denied/permitted access, wrong owner or tenant, field restrictions, conflict, and invalid input.
- Exercise relevant duplicate and failure windows: concurrent claims, same key/different payload, write failure, and committed effect with lost response. Select cases justified by the changed operation.
- Verify caller-visible status/body, persisted invariant, and side-effect count, not only internal calls. Include meaningful negative paths without building every possible test layer.
- Return changed files and contracts, acceptance outcomes, exact checks/results, environment limitations, and migration/configuration dependencies. Distinguish code prepared from live effects applied.
- Delegated work returns assignment ID and evidence for the parent's accepted/needs changes/blocked decision; unresolved integration is a named gap, not a success claim.
