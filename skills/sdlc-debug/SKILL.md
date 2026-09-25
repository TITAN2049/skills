---
name: sdlc-debug
description: Reproduce, diagnose, and fix broken application behavior using concrete evidence and targeted regression verification. Use for bugs, crashes, failing checks, inconsistent behavior, and production symptom investigations.
---

# Debugging specialist

Find the causal failure and repair it with the smallest change that restores the intended behavior.

## Establish what failed

- Read repository instructions, the relevant working tree changes, the report, and the affected execution path.
- Capture expected behavior, observed behavior, inputs, environment, frequency, and the last known working state when available.
- Preserve the original error and useful stack context; avoid exposing credentials or sensitive user data in logs or reports.
- Identify whether the report concerns a code defect, configuration issue, dependency failure, bad data, or an unclear expectation.
- Do not assume a recent commit caused the problem simply because it is recent.
- Check whether reproducing the problem can send messages, incur charges, delete data, or affect a live service before doing it.

## Build a useful reproduction

- Reproduce with the smallest input and environment that still demonstrates the reported failure.
- Prefer a disposable fixture or local environment when it can reproduce the same causal path.
- For intermittent failures, record timing, concurrency, relevant state, and a repeatable observation method.
- If reproduction is unavailable, state that limit and seek the narrowest existing evidence that separates plausible causes.
- Use existing logs, tests, traces, and version history before adding broad instrumentation.
- If temporary instrumentation is useful, keep it focused and remove it once it has served its purpose.

## Test explanations rather than guessing

- Maintain a short set of plausible causes grounded in observed behavior.
- Choose a check that distinguishes those causes; avoid changing several independent variables at once.
- Trace the first incorrect state or violated invariant, not only the final visible exception.
- Inspect callers and contracts before fixing a callee that may be receiving invalid inputs.
- Consider stale state, ordering, caching, race conditions, time zones, and retries only when the symptoms support them.
- Do not add retries, broad exception swallowing, arbitrary delays, or null fallbacks merely to hide the symptom.
- When a workaround is the authorized practical solution, label it and explain what underlying cause remains.

## Repair the causal path

- Prefer a bounded fix that restores the intended invariant and fits nearby code.
- Preserve valid behavior for existing callers; check whether the same faulty assumption occurs in adjacent paths.
- Avoid unrelated formatting, dependency upgrades, architectural changes, and speculative cleanup.
- Keep existing user changes intact, including changes in files involved in the failure.
- For incidents, distinguish a safe mitigation from a durable fix and stay within the authorized environment and actions.
- Do not run live destructive repair steps merely because the same command is safe on a local fixture.

## Verify the fix

- Re-run the original reproduction or the nearest faithful substitute after the change.
- Add a focused regression check when the defect involves meaningful behavior that could recur and the repository supports it.
- Where practical, demonstrate that the regression check detects the original defect and passes with the fix.
- Run relevant neighboring checks to catch compatibility regressions, without expanding into unrelated test suites without reason.
- For intermittent failures, report the observation window or number of attempts rather than claiming certainty from one passing run.
- Separate evidence for root cause from confidence in the fix, especially when full reproduction was impossible.

## Handoff

Report the root cause or best-supported explanation, changed behavior, reproduction and verification evidence, and any remaining uncertainty. Include exact failing commands or minimal inputs when the issue remains unresolved.
