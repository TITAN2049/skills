---
name: sdlc-testing
description: Design, implement, and run risk-based software tests, diagnose failing or flaky tests, and assess acceptance evidence using the repository's actual stack. Use for testing work or meaningful verification gaps, not to add tests to every edit.
---

# SDLC Testing

Turn acceptance criteria and credible failure risks into checks of observable behavior.
Use the existing test stack unless it cannot exercise the behavior that matters.

## Establish the test target

- Read the request, affected code, existing tests, package scripts, and CI commands.
- Identify the contract: inputs, outputs, persisted effects, errors, and permissions.
- Clarify only acceptance criteria whose ambiguity changes expected behavior.
- Distinguish new behavior, a reproduced defect, a flaky check, and an environment failure.
- Choose the smallest useful verification set based on impact and likelihood of failure.

## Choose the right boundary

- Unit checks suit isolated rules with meaningful input partitions or invariants.
- Integration checks suit database constraints, serialization, permissions, and service contracts.
- End-to-end checks suit critical user journeys and boundaries that lower layers cannot represent.
- Exercise negative paths when rejection, recovery, or access control is part of the contract.
- Cover empty, boundary, duplicate, concurrent, or interrupted operations when the implementation makes them credible risks.
- Avoid adding every test layer for the same assertion or choosing a coverage percentage as the objective.

## Implement meaningful checks

- Match existing fixtures, helpers, naming, and test isolation conventions.
- Assert public results and important side effects rather than private implementation details.
- Prefer a regression test that fails on the original defect when practical.
- Use realistic data at the relevant boundary; keep fixtures small enough to explain.
- Mock unstable external dependencies at their boundary without mocking away the behavior under test.
- Control clocks, randomness, concurrency, and external services where they cause nondeterminism.
- Clean up test resources without deleting unrelated data or relying on execution order.
- Use an isolated local or test environment; do not run destructive checks against shared data.

## Investigate failures

- Capture the exact failing command, error, and relevant environment before changing code.
- Establish whether the failure reproduces independently of unrelated pending changes.
- Separate product defects from incorrect expectations, broken fixtures, and missing prerequisites.
- For a flaky test, identify the race or unstable dependency; retries alone are not a repair.
- Do not weaken assertions, skip checks, or change production behavior merely to obtain a green run.
- If behavior is intentionally changing, update the expectation and explain the changed contract.

## Verify proportionally

- Run targeted checks first, then affected integration or CI checks required by the repository.
- Broaden testing when a failure, shared dependency, or architectural change justifies it.
- State when a test was inspected but not executed, or execution was blocked by an environment issue.
- When a required tool is missing, use available evidence and report the gap rather than claiming success.
- After meaningful checks pass, stop repeating the same suite without new evidence or changes.

## Handoff

Report the behaviors covered, any product or test changes, and the commands actually run.
Distinguish passed checks, failed checks, and checks not run; include actionable failure details.
Name remaining acceptance risks or environment gaps without implying complete correctness.
If the request is an assessment, provide findings; if it requests fixes, complete the authorized fixes and verification.
