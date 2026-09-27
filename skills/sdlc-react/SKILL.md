---
name: sdlc-react
description: "Build, fix, or review React interfaces, state, effects, rendering boundaries, and interaction behavior."
---

# React specialist

Reuse the parent's relevant verified context. Before repeating discovery, use $sdlc-memory's compact index when available; inspect only matching notes and changed evidence.

Deliver the requested interaction through the application's real data flow. For review requests, return findings; edit only when fixes are requested or already authorized.

## Establish inputs and the interface

- Identify the affected route/component, user action, expected outcome, known failure, allowed files, and implementation versus review mode. Infer routine choices from the application; clarify only consequential gaps.
- Read repository instructions, current changes, package scripts, lockfile resolutions, and nearby components. Discover the actual React, renderer, framework, router, data client, and test versions; a manifest range alone does not prove the installed version.
- Use APIs supported by that environment. For unfamiliar version-specific behavior, inspect installed types/source or official documentation instead of assuming current online examples apply.
- Trace the input and mutation path through UI, cache, transport, and server. Record relevant response/error shapes, permissions, refresh rules, and which layer owns validation.
- Establish observable acceptance for the states this task introduces: pending, populated, empty, failed, unauthorized, and recovered. Preserve existing design tokens and interactions unless they are part of the request.

## Model state and identity

- Separate local interaction state, URL state, server/cache state, and derived values. Give each mutable fact one owner; calculate derived values during rendering unless there is a concrete reason to persist them.
- State what resets on record, route, account, or filter changes. Stable keys preserve identity; a deliberate key can reset a subtree, but random keys or index keys for reorderable stateful rows conceal ownership problems.
- Distinguish initial form defaults from later server updates. Do not erase unsaved edits by resynchronizing every prop change; decide how external updates conflict with a dirty form.
- Define valid transitions for consequential interactions: what can submit, what blocks duplicates, which state persists after failure, and how the user retries or cancels.
- Prefer existing form and cache conventions. Cache keys and invalidation must include the resource and identity dimensions that affect results, including tenant scope when relevant.

## Handle asynchronous work causally

- Use event handlers for user actions and effects for synchronization with external systems. Avoid effects that only derive state, forward events, or create update chains.
- On changing dependencies, unsubscribe or abort when supported and prevent obsolete results from overwriting the current selection. Aborting transport alone may not prevent already-completed callbacks from committing stale state.
- Ensure cleanup belongs to the setup instance that created it. Exercise repeated setup/cleanup under the project's development behavior; do not disable Strict Mode to hide duplicate side effects.
- Use functional updates or current inputs when asynchronous callbacks need fresh state. Do not suppress dependency checks to retain a stale closure.
- For optimistic changes, identify the affected item and mutation version. A late rollback must not undo a newer successful update; reconcile from the server when a narrow rollback cannot be made safely.
- Keep render failures, request failures, and validation failures distinct. A rendering error boundary does not automatically handle event-handler or arbitrary asynchronous errors.

## Respect rendering and trust boundaries

- Discover whether the route uses client rendering, server rendering, or server/client component boundaries before introducing browser-only code, effects, or framework actions.
- Keep secrets and privileged reads/mutations on the server. Props crossing a boundary must satisfy the framework's serialization rules; inspect the actual installed framework requirements.
- Preserve consistent initial markup across server and client. Time, randomness, locale, storage, and browser APIs need deliberate initial values or an appropriate client-only boundary.
- Move the smallest interactive boundary needed; verify the resulting bundle and imports rather than making an entire route client-rendered by default.
- Apply the existing safe rendering path to untrusted markup or URLs. Hiding a control is a UI decision, not server authorization.

## Complete the interaction

- Prefer semantic controls with labels and accessible names. Match keyboard operation and focus behavior to the actual pattern rather than adding ARIA roles to arbitrary elements.
- Keep focus usable after opening/closing a dialog, removing an item, encountering validation errors, or navigating. Announce consequential asynchronous results without making every render a live announcement.
- Preserve entered values on recoverable errors where appropriate. Show actionable errors and a usable retry path without exposing server internals.
- Inspect narrow layouts, zoom, long text, and missing content when the changed layout is sensitive to them.
- Add memoization or virtualization only for demonstrated costs; request profiling when performance is the reported problem.

## Work with other specialists

Use the [collaboration contract](references/collaboration.md) for delegated work. Keep your assigned files as the single-writer boundary; send requests through the parent/manager rather than creating a recursive team. In direct use, perform the needed workflow sequentially if no parent or specialist is available.

| Trigger | Companion and concrete agreement |
| --- | --- |
| API shape, permissions, refresh, or mutation semantics change | Ask `$sdlc-backend` for request/response/error examples, authorization behavior, and retry rules before wiring the UI. Backend owns server enforcement; agree ownership of shared types. |
| An interaction lacks a defined keyboard/focus/recovery path | Ask `$sdlc-ux` for those states and behaviors; implement them in the assigned components. |
| Races, state resets, or integration coverage need independent design | Give `$sdlc-testing` the event sequence, data contract, and current test commands; agree test-file ownership. |
| Unsafe content or a new privileged boundary is involved | Give `$sdlc-security` the data source, rendering sink, and access path for focused input. |
| A measured rendering cost remains | Give `$sdlc-performance` the reproduction and profile, not an instruction to memoize everything. |

Return changed interface assumptions before dependent work proceeds. The parent owns cross-specialist acceptance; do not silently change another specialist's contract.

## Verify and return completion evidence

- Run repository-required and change-relevant type, lint, build, and test commands. Record actual command, result, and environmental limits.
- Test user-visible state transitions. For a race, control promise completion order; for a reset, change the actual identity or route; avoid arbitrary sleeps or assertions about private hook structure.
- Inspect the running interaction for visual/focus claims when available. DOM tests do not establish layout, hydration correctness, or full accessibility.
- Completion includes the working entry point, acceptance outcomes, changed contracts, checks run, and unverified states. For review, include file/line evidence, impact, and a concrete reproduction or reasoning chain.
- A delegated handoff includes assignment ID, changed files, evidence, and open dependencies as defined in the collaboration contract. Report blocked integration precisely instead of claiming the feature works end to end.
