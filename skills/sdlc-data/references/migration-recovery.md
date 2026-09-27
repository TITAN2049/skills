# Migration and recovery worksheet

Use this for a change with deployment overlap, significant data volume, a backfill, or irreversible transformation. Fill only the relevant parts in the project's existing change record or handoff; the worksheet does not require a new document or a multi-stage rollout for every migration.

## Record the facts that affect the plan

- Database engine/version and migration runner/version; evidence for the connection target and whether it is shared.
- Affected tables/indexes, observed size/cardinality, expected concurrent writers, and important long-running transactions.
- Business invariant, invalid existing states, supported app versions, and non-app consumers that can still read/write.
- Authorization covers: files only, local execution, named shared target, backfill, or release action. Do not infer broader execution from preparation work.

Unknown cardinality, lock behavior, or consumer compatibility is a named uncertainty. Do not substitute a convenient assumption when it determines whether a live operation is safe.

## Make the compatibility window explicit

For each proposed phase, record the following:

| Phase | Schema/data state | Old reader/writer | New reader/writer | Authority and consistency rule | Completion evidence | Recovery |
| --- | --- | --- | --- | --- | --- | --- |
| Before | Existing schema and observed data | Current behavior | Not deployed | Existing representation | Baseline invariant checks | Existing operational recovery |
| Expand, if needed | Additive fields/indexes/structures | Can they continue unchanged? | What defaults/fallbacks are valid? | Name the authoritative representation | DDL completed and compatible callers verified | Undo additive change only if no dependent version is running |
| Populate/transition, if needed | Mixed populated and legacy records | Can old writes invalidate new data? | Can new reads tolerate unpopulated data? | Define atomic writes, reconciliation, or capture mechanism | Backfill progress plus invariant/reconciliation checks | Stop/resume or revert application use; account for writes since transition |
| Switch, if needed | New representation complete | Are old consumers retired or still compatible? | New path authoritative | State how old writes are prevented or reconciled | Consumer/version evidence plus data checks | Identify whether switching back preserves all writes |
| Contract, if needed | Obsolete representation removed | Must no longer depend on it | No fallback dependency remains | New representation only | Retirement and recovery prerequisites met | Restore or forward repair if rollback cannot recover data |

Rows are options, not a required recipe. A renamed column on a rolling service usually needs a compatibility plan; an additive local fixture field may not.

## Resolve common failure windows

- **Backfill versus current writes:** a batch computed from an earlier value can overwrite a newer value. Decide whether updates are conditional on the source version, executed atomically from current data, or reconciled through a change log. A progress cursor alone does not solve this race.
- **Progress versus commit:** checkpoint advancement before the batch commits can skip records after a crash. Record progress with the data change when possible, or make overlap/replay safe and detectable.
- **Pagination versus mutation:** offset pagination can miss or repeat rows as data changes. Prefer a stable ordered key when suitable and explicitly handle inserts outside the captured range.
- **Constraint validation versus writes:** cleaning existing duplicates is insufficient if concurrent writers can create more before enforcement. Coordinate the writer/constraint order and verify the engine's enforcement semantics.
- **Dual write partial success:** two successful statements in application code are not necessarily one atomic invariant. Choose a transaction, existing durable workflow, or reconciliation path appropriate to the actual stores.
- **Rollback after new writes:** the old schema or app may not represent data introduced by the new version. Identify the cutoff after which a forward fix or restoration is required.
- **Locking and DDL:** inspect engine-specific operations, transaction support, timeout behavior, and long-lived transactions. An “online” operation can still have brief locks or substantial resource cost.

## Choose verification and stop conditions

Use representative before-data, including the invalid states the migration must transform or reject. Exercise only the failure windows on which the selected design depends.

Record:

1. Local/test migration command and observed resulting schema/data.
2. Invariant and reconciliation queries, expected conditions, and actual outcomes.
3. Relevant old/new application reads and writes during the compatibility window.
4. Interruption, rerun, and concurrency evidence for promised backfill behavior.
5. Recovery command or procedure, prerequisites, data loss limits, and what was actually exercised.
6. For authorized shared execution, thresholds or observations that trigger stopping, plus the owner of the next decision.

Do not invent universal numeric thresholds. Choose limits from the environment's operating constraints and available evidence; if these are missing and necessary for a consequential run, prepare the change and return the missing decision to the parent.

## Return a usable handoff

Provide the phase that was actually reached, artifacts/versions applied, environment identity without credentials, data checks, stop/recovery evidence, and remaining prerequisites. State whether the next action is preparation, local verification, shared application, or deployment. A prepared rollback file is not evidence of recoverable data.
