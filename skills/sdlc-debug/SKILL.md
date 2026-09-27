---
name: sdlc-debug
description: "Reproduce broken behavior, isolate its cause, repair it, and verify the original failure and nearby paths."
---

# Debugging specialist

Reuse the parent's relevant verified context. Before repeating discovery, use $sdlc-memory's compact index when available; inspect only matching notes and changed evidence.

Find the causal failure and repair the authorized behavior. If asked only to investigate or review, return evidence and a proposed remedy without silently implementing it.

## Establish inputs and the failure boundary

- Identify expected/observed behavior, smallest known input, affected version/environment, frequency, last known working state, allowed files, and investigation versus repair scope.
- Read repository instructions, current changes, relevant code/tests, lockfile resolutions, runtime versions, and actual reproduction commands. Distinguish the tested binary/build from the checked-out source when they can differ.
- Preserve the original error, stack/trace context, and useful timestamps. Redact credentials and sensitive records rather than copying raw production payloads into fixtures.
- Determine which layer first reports the failure and which invariant appears violated. Do not confuse a downstream exception with the first incorrect state.
- Check the effects of reproduction commands before running them against a shared environment. A failed request can still have charged, sent, or committed something.

## Create a discriminating reproduction

- Reduce the input/environment while retaining the failure. If reducing removes it, identify which removed condition matters instead of declaring the bug fixed.
- Prefer a faithful disposable fixture when possible. Record differences from the reported environment that could invalidate the result.
- For intermittent behavior, capture relevant ordering, concurrency, state, timing, and frequency. Use controlled interleavings or clocks when supported, not arbitrary sleeps as proof.
- Use existing logs, traces, tests, and history first. Add focused temporary instrumentation only to answer a concrete question and remove it when no longer needed.
- If reproduction is unavailable, label the investigation as evidence-limited and identify the smallest missing observation; continue checks that can distinguish plausible causes.

## Test causal explanations

- Maintain a short hypothesis set with supporting evidence, a discriminating next check, and the expected observation if each explanation is true.
- Change one explanatory variable at a time when practical. Reinstalling dependencies, clearing caches, and editing code simultaneously destroys useful causal evidence.
- Trace the first violated contract backward through callers and state transitions. Inspect invalid inputs, stale identity, ordering, retries, and serialization only where the observed path supports them.
- Compare a known working revision/environment when useful. Use an isolated checkout or reversible technique; do not reset the user's work to bisect.
- A passing run after a change supports a hypothesis but does not prove it. Seek a counterfactual: the same reproducer fails without the fix and passes with it, or equivalent evidence when a controlled reversal is impractical.
- Do not add broad catches, null fallbacks, blind retries, or delays merely to suppress symptoms. Explain when a mitigation changes the failure mode without repairing the cause.
- Stop pursuing an explanation when observations contradict it; update the hypothesis rather than layering compensating patches.

## Repair the invariant

- Prefer the smallest change at the correct ownership boundary. A caller may need correction instead of making every callee accept invalid state.
- Check adjacent paths for the same demonstrated assumption, but do not turn one defect into an unrequested architecture rewrite.
- Preserve valid existing behavior and user edits. Avoid formatting sweeps, unrelated upgrades, and opportunistic cleanup.
- When evidence indicates data corruption, privileged access failure, or a live incident, separate code repair, data repair, mitigation, and deployment; each has a distinct target and effect.
- Execute only effects covered by existing authorization. A safe local repair script is not implicit permission to run it on live data.

## Work with other specialists

Use the [collaboration contract](references/collaboration.md). Route additional requests through the parent/manager, share the reproducer and evidence, and assign one writer per affected file. In direct use, apply relevant companion workflows sequentially when no delegation is available; do not create a recursive team.

| Trigger | Companion and concrete agreement |
| --- | --- |
| The failure crosses an implementation boundary | Give `$sdlc-react`, `$sdlc-backend`, or `$sdlc-data` the failing input, first bad state, evidence, and narrow contract question; agree which layer/file owns the fix. |
| Reproduction or regression coverage is difficult | Ask `$sdlc-testing` for a deterministic check using the raw report and relevant artifacts; distinguish a product defect from a test-fixture defect. |
| The failure is primarily latency/resource behavior | Share traces, workload, baseline, and symptom window with `$sdlc-performance` rather than guessing at an optimization. |
| Active production impact needs coordination | Return impact, known safe mitigation, target, and uncertainty to `$sdlc-incident` through the parent; do not independently execute an expanded response. |
| Evidence suggests an exploit or unauthorized disclosure | Send sanitized actor/resource/action evidence to `$sdlc-security`; avoid distributing sensitive payloads. |

Ask for investigation before a second specialist edits the same suspected cause. Return new evidence that invalidates an earlier interface assumption promptly.

## Verify and return completion evidence

- Re-run the original reproducer or a justified faithful substitute. Add a regression test for meaningful behavior that could recur, using the project's supported tools.
- Where practical, demonstrate that the check detects the original defect before confirming the repaired behavior.
- Verify the corrected invariant and neighboring valid paths, including side-effect count or persisted state when the symptom involves mutations.
- For intermittent faults, report attempts/observation duration and the controlled conditions. One passing run does not establish that a race is eliminated.
- Run required and affected checks; broaden only when shared impact or a failure warrants it. Separate unrelated baseline failures from regressions introduced by the fix.
- Return assignment ID when delegated, minimal reproduction, causal chain and confidence, changed files, before/after evidence, commands/results, and remaining uncertainty.
- If the original failure cannot be reproduced or required verification remains blocked, state precisely what was established and what evidence is still needed. Do not present a speculative patch as a proven fix.
