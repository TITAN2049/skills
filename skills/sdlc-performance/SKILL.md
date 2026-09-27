---
name: sdlc-performance
description: "Measure bottlenecks and verify performance changes under representative, comparable conditions."
---

# SDLC Performance

Reuse the parent's relevant verified context. Before repeating discovery, use $sdlc-memory's compact index when available; inspect only matching notes and changed evidence.

Connect a user-visible or operational performance problem to a measured cause.
Preserve behavior and use comparable evidence to judge an optimization.

## Define the target

- Identify the slow operation, affected users, representative workload, and relevant environment.
- Choose a metric that reflects the complaint: latency, throughput, memory, CPU, render delay, or another concrete measure.
- Discover existing benchmarks, tracing, profiling, monitoring, and performance budgets.
- If no budget exists, establish a baseline and state the objective without inventing a promised percentage gain.
- Record workload size, concurrency, warm-up state, build mode, and important environment limits.
- Include relevant input distributions and user/device or request classes; an average-sized fixture can miss the expensive case that prompted the task.

## Locate the bottleneck

- Reproduce with realistic data scale and the repository's supported execution path.
- Use profiling, timings, query plans, traces, or browser tools available for the actual stack.
- Separate CPU work, waiting on I/O, contention, allocation pressure, and redundant work.
- Follow the critical path; a frequently called function is not necessarily the limiting factor.
- Form a falsifiable explanation of the observed cost and choose a measurement that distinguishes it from competing causes before changing code.
- For frontend work, distinguish network transfer, main-thread work, rendering, layout, and interaction delay.
- For backend work, inspect query count, access patterns, downstream latency, serialization, and concurrency when relevant.
- Investigate production symptoms with read-only evidence unless live intervention is authorized.

## Select an intervention

- Prefer eliminating unnecessary work or improving access patterns before adding infrastructure.
- Evaluate the effect on correctness, freshness, ordering, memory, complexity, and operational cost.
- For caches, define key scope, invalidation, lifetime, size bounds, and authorization isolation.
- For batching or concurrency, respect ordering, service limits, cancellation, and resource bounds.
- For database changes, consider representative query plans, write cost, and migration impact.
- For frontend memoization or virtualization, measure the relevant workload and preserve interaction and accessibility behavior.
- Do not substitute large architectural rewrites for a demonstrated local bottleneck without task justification.

## Measure fairly

- Compare the same operation, dataset, environment, build mode, and measurement method before and after.
- Include enough repetitions to distinguish a change from noise; report variability where material.
- Keep the harness, input generation, tool versions, machine limits, and source revision reproducible. Save raw observations when needed to reassess a noisy conclusion.
- Record offered load, completed work, failures, and timeouts; rejecting or dropping more work must not masquerade as a latency improvement.
- Do not claim stable tail latency from a sample too small to support that percentile.
- Keep cold-start and steady-state results distinct when they answer different questions.
- Account for setup, warm-up, instrumentation overhead, background activity, and cache state; alternate or repeat baseline/candidate runs when drift could explain the difference.
- Check the resource or failure mode that the optimization may have shifted elsewhere.
- For throughput claims, check saturation, queue growth, and error behavior; report the tested load range rather than extrapolating capacity from one run.
- Use bounded local or explicitly authorized test workloads; do not generate unapproved load against shared services.
- If production-scale testing is unavailable, label the result as a limited benchmark or hypothesis.

## Check behavior

- Run existing checks for affected contracts and a focused regression test when meaningful.
- Verify error handling, cancellation, and representative boundary conditions affected by the optimization.
- Remove temporary probes unless useful instrumentation is intentionally part of the deliverable.
- Retain a benchmark only when it can detect a meaningful regression at reasonable maintenance cost.

## Work with other specialists

Use the [collaboration contract](references/collaboration.md) for bounded investigations; a direct performance task can finish independently.
Route shared-file ownership and changes to performance acceptance through `$sdlc-manager`; do not launch another recursive team.

- Give `$sdlc-react`, `$sdlc-backend`, or `$sdlc-data` the measured hot path, representative workload, baseline, and proposed constraint; benchmark a returned implementation under the same conditions.
- Give `$sdlc-devops` evidence of resource throttling or environment drift and request comparable runtime facts before attributing the result to code.
- Give `$sdlc-testing` the semantic risks of caching, batching, ordering, or concurrency changes when independent behavior checks are needed.

## Handoff

Report the identified bottleneck, change, and comparable before/after evidence with units.
Include measurement conditions, actual validation commands, and limitations on generalizing the result.
Explain important correctness or resource tradeoffs and any remaining bottleneck.
State whether the measured target was met, missed, or remains inconclusive; distinguish an observed improvement from a proven cause.
For an investigation-only request, provide supported recommendations rather than silently changing architecture.
