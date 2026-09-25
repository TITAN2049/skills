---
name: sdlc-refactor
description: Improve code structure, remove proven dead code, and perform focused cleanup while preserving existing behavior and public contracts. Use for maintainability work, not unrequested feature changes or broad modernization.
---

# Refactoring and cleanup specialist

Improve a concrete maintenance problem while keeping observable behavior stable unless the user explicitly requests a behavior change.

## Establish the intended improvement

- Read repository instructions, current changes, relevant callers, and the tests or documentation describing existing behavior.
- Name the maintenance problem: duplication, unclear ownership, excessive coupling, dead code, misleading names, or a difficult change path.
- Define the boundaries that must remain stable, such as public APIs, rendered output, error semantics, ordering, stored data, and configuration.
- Identify generated files and their sources; change the source of truth rather than editing generated output by hand.
- Keep user edits intact and avoid absorbing unrelated warnings or style disagreements into the task.
- Prefer a bounded improvement with a clear benefit over broad modernization motivated only by preference.

## Choose the smallest useful transformation

- Inspect all relevant callers before changing a shared helper or moving a module boundary.
- Extract an abstraction when it captures a stable concept or removes meaningful duplication, not simply because two short fragments look similar.
- Prefer clear names and direct control flow to indirection that requires more navigation.
- Keep domain rules near their owner and avoid creating a generic utility layer with unrelated responsibilities.
- Preserve evaluation order, asynchronous timing, exception behavior, and mutation semantics when rearranging logic.
- Do not combine a large rename, formatting sweep, dependency upgrade, and behavior change into one cleanup unless requested.
- Keep performance work evidence-based; changing an algorithm's cost can also change ordering or memory behavior.

## Remove code with evidence

- Search imports, references, route registrations, configuration, scripts, tests, and exports relevant to the removal.
- Account for dynamic loading, reflection, framework conventions, external consumers, and package entry points when they exist.
- An unused local symbol is different from a public API with no in-repository callers.
- Delete a dependency only after checking runtime, build, development, and tooling usage; use the repository's package manager to update its lockfile.
- Do not remove comments, compatibility shims, or migration code until their purpose and remaining callers are understood.
- If evidence is insufficient for deletion, leave the uncertain element intact and report the specific gap.

## Preserve reviewability

- Make connected changes in small enough units that the preserved contract remains easy to inspect.
- Use automated refactoring or formatting tools when they fit the task, but inspect the resulting diff for unintended churn.
- Limit formatting to touched code unless repository tooling requires a broader generated change.
- Keep behavior fixes discovered during cleanup separate unless they are necessary to complete the authorized request.
- Update stale names and references that the refactor directly invalidates.

## Verify preserved behavior

- Run the relevant existing checks before and after a consequential transformation when a baseline is needed.
- Use meaningful characterization tests for complex undocumented behavior that must survive; do not add tests that merely freeze private structure.
- Check changed module exports, imports, build boundaries, and public callers as appropriate.
- Re-run affected integration paths when behavior depends on serialization, storage, concurrency, or side effects.
- Inspect the final diff for accidental contract changes and removed error handling.
- Do not claim full behavioral equivalence from lint or type checks alone; describe the evidence and its limits.

## Handoff

State the maintenance improvement, preserved contracts, checks run, and any uncertain removal candidates left in place. Call out an intentional behavior change explicitly if it was part of the user's request.
