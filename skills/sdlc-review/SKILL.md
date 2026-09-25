---
name: sdlc-review
description: Review a pull request, diff, or scoped implementation for actionable correctness, regression, maintainability, and test gaps. Use for review requests; default to evidence-backed findings and apply changes only when the user also requests fixes.
---

# SDLC Review

Find defects that matter to the requested behavior and give the author enough evidence to resolve them.
Review requests produce findings unless the user has also authorized implementation.

## Establish the comparison

- Read repository guidance, the request or issue, and the relevant diff.
- Identify the intended base and head; do not assume every local modification belongs to this change.
- If the comparison is unclear, inspect available branch and commit context before asking.
- Preserve user changes and avoid formatting or refactoring while inspecting a review.
- Read surrounding code, callers, contracts, and related tests needed to understand changed behavior.

## Follow the consequences

- Trace changed values and control flow across important boundaries rather than reviewing lines in isolation.
- Check accepted inputs, rejected inputs, error handling, persisted state, and backward compatibility.
- Inspect authorization, concurrency, lifecycle cleanup, and resource handling when affected by the change.
- Consider schema migrations, configuration defaults, and rollback behavior when those artifacts change.
- Look for test gaps that conceal a specific plausible defect; missing tests alone do not establish a bug.
- Distinguish an introduced regression from pre-existing behavior and intentional product decisions.

## Decide whether to report

- A finding should describe a concrete condition, an observable wrong result, and relevant evidence.
- Verify assumptions using code, a focused reproduction, a test, or authoritative contract documentation.
- Account for upstream validation, caller guarantees, feature flags, and framework behavior before flagging a path.
- Do not report stylistic preferences as defects unless they violate an explicit requirement with a practical cost.
- Avoid speculative chains that require several unsupported assumptions.
- Mark uncertainty explicitly; do not present a suspicion as a reproduced failure.
- Do not duplicate one root cause across several locations when one clear finding is sufficient.

## Prioritize findings

- Blocking: widespread outage, irrecoverable data loss, or a severe exploitable boundary failure under supported use.
- High: a common or important workflow fails, or affected users face substantial impact.
- Medium: a meaningful defect requires narrower conditions or has a contained workaround.
- Low: a concrete but limited issue that is useful to fix without distracting from higher-impact defects.
- Adapt labels to repository conventions; explain the impact rather than relying on a label alone.

## Verify without expanding scope

- Run focused checks when they can resolve uncertainty efficiently and safely.
- Report execution failures accurately, including missing environment prerequisites.
- Do not run expensive or destructive integration actions just because a review is authorized.
- Do not post comments, submit a review, merge, or contact an author unless the task authorizes that external action.
- If asked to fix findings, implement scoped repairs and run checks relevant to those repairs.

## Handoff

Lead with actionable findings in priority order, each tied to a tight file location.
Explain the trigger and consequence in plain language; include reproduction evidence when useful.
State material assumptions or unanswered questions after findings.
Briefly summarize what was inspected and what verification ran.
If no actionable findings remain, say so and note any significant verification limitations.
