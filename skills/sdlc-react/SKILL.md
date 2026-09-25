---
name: sdlc-react
description: Build, fix, or review React interfaces, including state, effects, component boundaries, accessibility, and rendering behavior. Use for React-specific implementation work, not framework migration unless requested.
---

# React specialist

Deliver a working interface that fits the application's existing architecture and the user's requested behavior.

For review requests, inspect and return actionable findings; change files only when fixes are requested or already authorized.

## Establish the constraints

- Read repository instructions, package manifests, lockfiles, the touched route, and nearby components before choosing APIs or dependencies.
- Identify the actual React version, framework, rendering model, styling approach, and test tools. Do not assume a particular router or component library.
- Trace where data originates, who owns it, and which components need to change it. Distinguish local interaction state, URL state, and server state.
- Turn the request into observable behavior, including relevant loading, empty, error, success, and permission states.
- Preserve established design tokens and interaction patterns unless the request changes them.

## Make component and state decisions

- Keep state near its consumers; lift it only when coordination requires a shared owner.
- Derive values during rendering when possible. Avoid storing copies of props or computed state that can drift.
- Use effects to synchronize with external systems, not to orchestrate ordinary event handling or derive render values.
- Inspect effect dependencies, subscription cleanup, cancellation, and stale responses when asynchronous behavior changes.
- Prefer existing data fetching, form, and cache conventions. Introduce a new abstraction only when it solves a concrete requirement.
- Keep stable identity for list items and stateful children. Check whether conditional rendering unintentionally resets state.
- Make mutation ownership clear so pending actions, duplicate submissions, retries, and failures have deliberate behavior.
- Treat memoization as a response to measured or evident rendering cost; do not scatter it through small components by default.

## Respect rendering and trust boundaries

- Where server and client components exist, keep secrets and privileged access on the server and interactive state in the appropriate client boundary.
- Verify serialization, hydration, browser-only APIs, and initial render consistency when changing a rendering boundary.
- Do not make an entire subtree client-rendered simply to support one interactive leaf without checking the impact.
- Handle untrusted content through the application's approved escaping or sanitization path.
- Use existing authorization checks for UI decisions, while recognizing that hiding a control does not enforce access on the server.

## Complete the interaction

- Use semantic controls, associated labels, meaningful accessible names, and keyboard support.
- Preserve focus through dialogs, async updates, and navigation; communicate important status changes accessibly.
- Check disabled, pending, validation, and recovery states rather than implementing only the successful path.
- Check narrow layouts and long or missing content using existing responsive conventions.
- Avoid unrelated component rewrites, styling churn, dependency upgrades, or broad design changes.

## Verify the relevant behavior

- Use the repository's actual type, lint, build, and test commands, selecting those justified by the change.
- For changed interaction logic, prefer tests of user-visible outcomes over internal hook calls or component structure.
- Cover the failure, race, or state transition that motivated the change when it could regress.
- For visual or keyboard behavior, inspect the running interface if available; report clearly when runtime inspection was unavailable.
- Do not invent test results or add tests that only mirror simple markup or styles.

## Handoff

Report the resulting behavior, affected entry points, checks actually run, and any remaining limitations. Mention server integration or browser verification that still needs evidence. Keep unrelated cleanup ideas separate from the completed scope.
