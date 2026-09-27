# Focused repository map template

Use only sections that help the current task; this is a reporting shape, not a discovery checklist.
Keep the navigation index under 300 words and the complete main map under roughly 1,500 words.
Link to relevant code and deeper component notes instead of copying their contents.

## Scope and provenance

- Question answered and included/excluded components.
- Repository identity, branch, HEAD when available, and material working-tree differences.
- Observation date; external-source dates or expiry where relevant.

## Compact navigation index

- Main entrypoint and the path/symbol that owns the requested behavior.
- Relevant module responsibilities and public boundary or contract.
- Where state, authorization, tests, build/configuration, and generated sources live.
- Important invariant or hotspot and the best next file or saved note to inspect.
- Unresolved question that could change the implementation approach.

## Representative flow

`entrypoint -> validation/authorization -> domain work -> state/external boundary -> result`

For each relevant step, identify its path/symbol and the evidence actually inspected.
Mark facts as **observed**, **inferred**, or **unverified** when the distinction matters.
Include an error or retry path only when it explains a relevant contract or failure mode.

## Boundaries and hotspots

| Boundary or hotspot | Owner/source | Contract or invariant | Evidence and implication |
| --- | --- | --- | --- |

Include meaningful coupling, trust boundaries, generated-file ownership, and data consistency constraints.
Do not populate a table with every directory or describe a possible issue as a confirmed defect.

## Operational pointers

| Purpose | Command and working directory | Prerequisites/effects | Inspected or actual result |
| --- | --- | --- | --- |

Include the relevant build/test/start or diagnostic entrypoints found in the repository.
Do not run them solely to fill this section.

## Open questions and reuse

- Specific unknown, evidence needed, and receiving specialist when applicable.
- Saved note IDs and evidence-file paths; distinguish saved notes from proposed notes. Split persistence into focused bodies of at most 4,000 characters with summaries of at most 180.
- Freshness limits and the bounded inventory to revisit when this map is reused.
- Any deeper component note warranted by the task; avoid exporting a complete repository index.
