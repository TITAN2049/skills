# Specialist handoff

Use the [collaboration contract](collaboration.md) for the packet and acceptance
rules. This example shows how a receiver evaluates a cross-role handoff.

```text
Task: export-api | State: ready for review
Outcome: owner-scoped report download
Acceptance: AC1 -> denied-access test; AC2 -> allowed download content test
Artifacts: report route and authorization helper; current working-tree diff
Interfaces: contract v2, GET response is a file; failure is structured JSON
Checks: project's focused test command -> passed; browser flow -> not run
Risks: UI consumer still implements contract v1
Next owner: React owner updates the consumer; tester checks integrated download
```

The manager cannot accept the integrated feature while the consumer still uses
v1. Send the React owner the changed contract and relevant criteria, then inspect
the integrated failure and success paths. Preserve valid backend evidence while
rechecking assumptions affected by any further changes.

For findings, give a reproducible trigger, affected location, consequence, confidence, and a proportionate remedy. Keep hypotheses separate from confirmed defects. Avoid repeating the whole task history.
