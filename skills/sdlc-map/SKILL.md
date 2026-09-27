---
name: sdlc-map
description: Map an unfamiliar repository or changed subsystem into a compact, evidence-backed guide to flows, ownership, commands, and risks.
---

# Repository Map

Help the next specialist find the right code and understand the boundaries relevant to the task.
Map when the repository is unfamiliar or its structure has materially changed; do not remap everything before routine work.
Produce a scoped guide, not a complete source export. Make no source-code changes.

## Start from the task and existing evidence

- State the question the map must answer and the component or journey in scope.
- Read applicable repository instructions, the relevant README, and manifests that establish actual entrypoints and tooling.
- Check a compact saved index through `$sdlc-memory`; load only notes relevant to the question, not every stored body.
- Record repository identity, branch/HEAD when available, and relevant working-tree changes; do not imply that HEAD describes uncommitted code.
- Treat old notes as leads to verify. Existing code, current instructions, and the user's task take precedence over remembered claims.

## Discover without bulk context

- Begin with a bounded `rg --files` inventory using relevant paths or filename globs; respect repository ignores.
- Narrow further by module, manifest, symbol, or caller before reading source. Record omitted areas when they limit a conclusion.
- Do not bulk-read source trees, logs, vendor/generated output, `.env*`, credentials, or datasets. Use explicit exclusions when an inventory would include them.
- Inspect hidden configuration only through an identified relevant path; do not disable ignores across the repository to find it.
- Discover the package/runtime and operational commands from actual manifests or scripts rather than assuming a framework.
- Record each command's working directory, prerequisites, and effects. Verify scope and target before executing it; mapping alone does not authorize setup, migrations, or deployment.
- Stop expanding when the map explains the requested boundary and remaining unknowns can be assigned a focused follow-up.

## Trace architecture, not just folders

- Trace one representative flow from a real entrypoint through transformations, authorization, storage or external calls, and its observable result.
- Cite paths and symbols for the steps. Label observed behavior, inference, and unresolved assumptions distinctly.
- Identify relevant modules and their responsibilities, public contracts, state ownership, and coupling across components.
- Mark data/auth trust boundaries and where validation, permission checks, transactions, retries, or error translation actually occur.
- Locate tests that exercise the flow, build/configuration inputs, generated artifacts, and their source or generator owners.
- Note demonstrated hotspots, important invariants, and failure-sensitive seams; do not turn the map into an unsolicited whole-repository audit.
- A directory name or dependency declaration suggests intent; it does not prove runtime use, ownership, or architecture.

## Deliver and preserve the useful subset

- Keep the main map under roughly 1,500 words and its navigation index under 300 words; shorter is preferable when it answers the task.
- Use [the focused map template](references/map-template.md) when a structured artifact helps. Omit irrelevant sections; deepen individual components only on demand.
- Prefer paths/symbols and concise conclusions over copied source or terminal output. Describe command checks as inspected, executed, or unverified.
- Give `$sdlc-memory` explicit curated notes, evidence-file paths, branch/HEAD and working-state provenance, plus any external-source freshness limit.
- Split the report into focused saved notes: each body is limited to 4,000 characters and each summary to 180. Keep a compact index of their IDs rather than storing the entire map as one note.
- The memory helper stores local notes in `.sdlc/knowledge.json` with source hashes and a configurable TTL (30 days by default). Use its `list` and `read ID` operations before proposing a new or updated entry.
- To persist through the helper, pass `--repo PATH save ID --title TITLE --summary SUMMARY --body-file FILE` with repeatable `--evidence PATH` and `--ttl-days DAYS` when needed; obtain the helper location from `$sdlc-memory`.
- Save only stable routing knowledge, decisions, and evidenced pitfalls useful to future tasks. Exclude secrets, raw transcripts, transient command output, and speculative conclusions presented as facts.

## Reuse with bounded freshness checks

- Stale note bodies are withheld by the helper by default; refresh their evidence before relying on them.
- Unchanged evidence hashes validate cited files only. They do not prove there are no new files, entrypoints, packages, or configuration.
- On reuse, check a bounded inventory of the relevant area and its manifests alongside source evidence; revisit only the affected portion of the map.
- Preserve provenance across branch/HEAD changes and note uncommitted evidence. A branch name alone is not a stable revision identifier.
- Date external claims and attach authoritative source references and a suitable TTL; repository hashes cannot validate external service or tool behavior.

## Work with other specialists

Use the [collaboration contract](references/collaboration.md) for delegated mapping or handoffs; direct mapping needs no team.
Route shared-note ownership and unresolved interface decisions through `$sdlc-manager`; do not recursively start another team.

- Give `$sdlc-architecture` the traced flow and concrete coupling questions when a design decision is needed; a map does not prescribe a redesign.
- Give `$sdlc-feature` or `$sdlc-debug` entrypoints, contracts, likely owning files, relevant checks, and confirmed risks for the requested change.
- Give `$sdlc-memory` a compact index and only the evidence-backed notes worth retaining; report what was saved or left unsaved.

## Handoff

State the mapped scope, representative flow, key findings, and evidence paths; distinguish unexplored areas from absent capabilities.
List actionable unknowns with their next owner and explain any limit on freshness or confidence.
Include the compact index or saved note IDs, commands actually checked, and enough provenance for the next specialist to revalidate efficiently.
