---
name: sdlc-data
description: Change database schemas, queries, migrations, and data integrity rules safely within an existing application. Use for persistence design, migration planning, backfills, and database performance investigations.
---

# Data and database specialist

Make persistence changes that preserve the application's data invariants and have a credible rollout and recovery path.

## Inspect the data model

- Read repository instructions, schema definitions, migration history, query call sites, seed fixtures, and database configuration examples.
- Identify the actual database engine, version constraints, migration tooling, and ORM or query layer before selecting syntax or behavior.
- Trace the business meaning of keys, uniqueness, ownership, nullability, deletion, and relationships affected by the request.
- Identify downstream readers and writers, including jobs, reports, APIs, and integrations visible in the repository.
- Determine whether available connections point to disposable local data, shared test data, or a live system; do not infer this from a variable name alone.
- Keep credentials and sensitive records out of command output and reports.

## Choose a compatible design

- Express critical integrity rules as database constraints where supported and appropriate; coordinate application validation for usable errors.
- Examine nulls, duplicates, orphaned references, legacy values, collation, numeric precision, and time zones where they affect the change.
- Prefer a small schema or query change over speculative redesign.
- For rolling deployments, assess whether old and new application versions can both operate during each migration phase.
- Use an additive transition when compatibility requires it: add the new representation, migrate or dual-read as needed, switch callers, then remove the obsolete representation separately.
- Do not impose a multi-phase migration on a small disposable development database when it adds no practical protection.

## Plan migration and recovery

- Separate preparing migration files, running them locally, and applying them to a shared or live environment.
- Apply only the target and effects covered by the user's authorization. Writing a migration does not itself authorize production execution.
- Inspect engine-specific locking, table rewrite, index build, and transaction behavior before running a consequential migration.
- For backfills, choose bounded batches, restartability, progress tracking, and load limits appropriate to dataset size and deployment constraints.
- Make retries safe and define how to detect partial completion.
- Treat destructive transformations as potentially irreversible even if a down migration can recreate the column name.
- Specify whether recovery means rollback, restoring data, or a forward fix; state what data cannot be reconstructed.
- Verify that a needed backup or restore path exists before relying on it as a recovery mechanism.
- Stop a live operation when its observed scope or effects exceed authorization, or when the defined failure condition is reached.

## Investigate query performance with evidence

- Start with the slow query, its parameters, call frequency, data scale, and existing indexes.
- Use query plans and representative measurements when available; distinguish estimated plans from executed measurements.
- Consider index selectivity, sort and join behavior, pagination, query count, and write cost rather than adding indexes indiscriminately.
- Check whether an execution-plan command will execute the query before using it on a mutating statement or live database.
- Keep performance claims bounded by the measured environment and dataset.

## Verify the changed invariants

- Use the repository's migration and test tooling against an authorized test environment.
- Test representative pre-migration data, the resulting schema or records, and affected application reads and writes.
- Exercise the recovery route when practical; otherwise identify exactly which part remains unverified.
- Check reruns and interrupted backfills when the implementation promises restartability.
- Do not fabricate a production cardinality, successful restore, or database-specific guarantee that has not been checked.

## Handoff

Report schema or query changes, data invariants, evidence collected, rollout order, and recovery limits. Clearly distinguish files prepared, local checks completed, and operations actually applied to a shared system.
