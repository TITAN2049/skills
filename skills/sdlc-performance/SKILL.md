---
name: sdlc-performance
description: Diagnose latency, throughput, resource usage, rendering, or scalability problems and implement measured performance improvements. Use for performance symptoms or optimization requests, not speculative rewrites without a relevant bottleneck.
---

# SDLC Performance

Connect a user-visible or operational performance problem to a measured cause.
Preserve behavior and use comparable evidence to judge an optimization.

## Define the target

- Identify the slow operation, affected users, representative workload, and relevant environment.
- Choose a metric that reflects the complaint: latency, throughput, memory, CPU, render delay, or another concrete measure.
- Discover existing benchmarks, tracing, profiling, monitoring, and performance budgets.
- If no budget exists, establish a baseline and state the objective without inventing a promised percentage gain.
- Record workload size, concurrency, warm-up state, build mode, and important environment limits.

## Locate the bottleneck

- Reproduce with realistic data scale and the repository's supported execution path.
- Use profiling, timings, query plans, traces, or browser tools available for the actual stack.
- Separate CPU work, waiting on I/O, contention, allocation pressure, and redundant work.
- Follow the critical path; a frequently called function is not necessarily the limiting factor.
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
- Do not claim stable tail latency from a sample too small to support that percentile.
- Keep cold-start and steady-state results distinct when they answer different questions.
- Check the resource or failure mode that the optimization may have shifted elsewhere.
- Use bounded local or explicitly authorized test workloads; do not generate unapproved load against shared services.
- If production-scale testing is unavailable, label the result as a limited benchmark or hypothesis.

## Check behavior

- Run existing checks for affected contracts and a focused regression test when meaningful.
- Verify error handling, cancellation, and representative boundary conditions affected by the optimization.
- Remove temporary probes unless useful instrumentation is intentionally part of the deliverable.
- Retain a benchmark only when it can detect a meaningful regression at reasonable maintenance cost.

## Handoff

Report the identified bottleneck, change, and comparable before/after evidence with units.
Include measurement conditions, actual validation commands, and limitations on generalizing the result.
Explain important correctness or resource tradeoffs and any remaining bottleneck.
For an investigation-only request, provide supported recommendations rather than silently changing architecture.
