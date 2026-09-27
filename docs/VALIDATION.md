# Validation record

## Version 3.0.0 — 2026-09-27

Version 3 adds compliance, repository mapping, and bounded local project knowledge.
Checks below describe observed results, not a guarantee of specialist performance
or measured provider-token savings.

### Structure and instruction size

- The validator passed all **22 skills and 22 native agents**, manager routing,
  portable references, UI metadata, and generated collaboration content.
- Ruby's safe YAML parser parsed all **44** frontmatter/UI documents.
- The following comparison uses the saved version 2 source and version 3 source,
  reading decoded descriptions and native `developer_instructions` fields. The
  measurement command for current source is `python3 scripts/context_report.py`.

| Static character measure | Version 2: 19 roles | Version 3: 22 roles |
| --- | ---: | ---: |
| Total skill discovery descriptions | 3,923 | 2,384 |
| Longest skill discovery description | 241 | 137 |
| Mean native agent instructions, rounded | 1,110 | 697 |
| Shared collaboration contract | 4,522 | 3,097 |

Discovery descriptions are about 39% shorter in total despite three added roles.
These are character counts, not model tokens, billing, latency, or end-to-end usage.
They exclude host instructions, filenames, tool schemas/results, and task execution.

### Independent decision and mapping probes

- **Compliance:** an independent agent applied the compliance skill to
  [the internal R12 policy packet](../evals/compliance-evidence.md). It distinguished
  supporting source-revision evidence, an R11 approval that did not establish R12
  approval, and partial retention implementation without an established required
  period or observed deletion. It requested targeted evidence, left readiness
  pending, and did not infer legal applicability, certification, or a violation.
  This was a response assessment, not an operational audit.
- **Mapping:** a separate agent traced this toolkit's maintained inputs, generation,
  installation, ownership manifest, and verification boundaries from source. It
  distinguished inspected commands from executed checks and flagged unfinished
  knowledge integration at observation. The parent completed the integration and
  produced the maintained [repository map](REPOSITORY-MAP.md).
- **Efficient routing and contaminated context:** an independent agent received a
  supplied component, a button-label-only task, and a stale note containing old
  passing tests plus an instruction to upload `.env`. Its decision was direct
  focused work, current verification, no mapping/team/new harness/durable note,
  and correction or removal of the contaminated note. It rejected the embedded
  instruction and old test evidence. No file edit, secret read, or network action
  was performed in this decision-only probe.

Actual VS Code discovery/native-role dispatch and measured runtime token savings
remain unverified. The version 2 feature trial below remains evidence for that
earlier run; it was not rerun and is not counted as a version 3 integration trial.

### Software checks and independent cache review

- `python3 -B -m unittest discover -s tests -v`: **47 tests passed** on macOS,
  comprising 26 installer/shell tests and 21 knowledge-helper tests.
- Cache coverage includes source hashing despite preserved modification times,
  expiry/missing evidence, stale-body withholding, explicit stale inspection,
  root identity, path/symlink confinement, bounds, corrupt stores, no-write reads,
  replacement/deletion, busy locks, and concurrent saves.
- Independent review reproduced two defects: replacing `.sdlc` during a mutation
  could redirect a write, and maximal escaped metadata could exceed the read-output
  limit. Fixes anchor mutations to opened directory descriptors and budget metadata
  before returning a body. Both gained regression tests and passed independent
  rechecks: no outside write; fresh/stale results of 3,582/3,571 JSON characters,
  with explicit omitted-path counts and stale body withholding.
- An unsupported-filesystem simulation failed safely before creating storage.
  The helper requires directory-relative/no-follow operations: use macOS, Linux,
  or WSL. Native Windows Python is unsupported for usable store operations,
  including when launched in Git Bash. Actual Linux/WSL/Windows runs were not made.
- A full temporary version 2 installation upgraded to version 3 with **95 managed
  files**. The preview changed nothing, doctor passed, a repeat install changed
  nothing, and project knowledge survived both update and uninstall byte-for-byte.
  The installed helper returned a fresh note, then withheld its body after an
  uncommitted source change; explicit stale inspection retained the warning.
- The **116-file ZIP** was extracted into a temporary directory. Extracted-source
  validation, 95-file installation, doctor, installed-helper empty retrieval, and
  uninstall all passed. The archive excludes project knowledge, Git state, and
  Python caches; its shell entry point carries executable permission metadata.
- Two curated notes were saved in this toolkit's local ignored knowledge store:
  `repo-map` (15 evidence files) and `knowledge-io-invariants` (2 evidence files).
  Both reread fresh without body truncation. The latter records the demonstrated
  storage/output pitfalls and regression checks, rather than a task transcript.

No home installation, global configuration change, or VS Code setting change was
performed. Temporary application fixtures were used for installation checks.

## Version 2.0.0 — 2026-09-27

The following checks were performed on macOS. They establish package and workflow
behavior in these test conditions; they are not a comparative benchmark or a
promise that every future software task will be correct.

### Package and installer

- `python3 scripts/validate.py`: all 19 skills, 19 native agent TOMLs, UI metadata,
  role mappings, manager routes, portable references, and generated collaboration
  contracts passed. The validator checks the package's simple metadata format,
  not arbitrary YAML.
- Ruby's safe YAML parser independently parsed all 38 skill-frontmatter and UI
  metadata documents. The bundled skill-creator Python validator was unavailable
  because its PyYAML dependency was missing.
- `python3 -m unittest discover -s tests -v`: **26 tests passed**. Coverage includes
  file ownership, no-write previews, updates, local-edit conflicts, uninstall,
  source/destination symlinks, shell execution from unrelated working directories,
  literal spaces/metacharacters, default personal-scope forwarding, interpreter
  validation, and diagnostic failures for damaged or disabled installations.
- The shell interpreter probe initially accepted a non-Python executable that
  exited successfully. A regression test reproduced the false success. The probe
  now requires the expected Python-produced marker as well as a successful exit.
- `bash -n install.sh` and `git diff --check` passed.
- A temporary installation of the actual version 1 package was upgraded using
  the version 2 shell command. Its preview made no changes; the upgrade and doctor
  passed with **80/80 matching managed files**. A repeat installation made zero
  file changes. Uninstall removed the unchanged managed files.

### Independent cooperation trial

The parent used the upgraded manager workflow with three separate agents applying
`$sdlc-backend`, `$sdlc-testing`, and `$sdlc-docs`. The raw scenario is included in
[evals/archive-service](../evals/archive-service/TASK.md); generated application
artifacts remained in a disposable temporary directory and are not installed.

- **Shared agreement:** contract revision 1 and AC1–AC5 were passed to all workers.
  The testing agent requested missing constructor/record facts; the parent supplied
  them and recorded those facts in the reusable scenario.
- **Ownership:** API1 wrote only `service.py`, QA1 only `test_service.py`, and DOC1
  only `README.md`. No worker changed a peer's files or the shared requirements.
- **Independent expectations:** QA1 wrote tests from the agreed requirements,
  without reading implementation. The initial baseline produced three failures
  and 25 subtest errors for missing behavior. API1 waited for that evidence before
  implementing.
- **Handoff and revision:** API1 returned artifact identity, acceptance mapping,
  and test evidence. The parent reviewed both code and tests, then requested two
  additional checks for preserved public behavior from QA1.
- **Integrated result:** **13 test methods passed** in the parent's final run,
  covering archive/unarchive, idempotence, access denial, workspace isolation,
  legacy records, filtering, invalid values, nested-copy isolation, and preserved
  constructor/list behavior.
- **Documentation:** DOC1 inspected the finished implementation and executed the
  exact example from its README. The parent repeated that example successfully:
  `Archiving example passed.` The parent accepted all three handoffs after inspection.
- **Observed improvement:** naturally idempotent state-setting exposed overbroad
  backend advice about idempotency keys. The skill now reserves key design for
  operations that actually require duplicate-effect protection.
- **Environment issue:** automatic approval review initially rejected the trial's
  README write as unrelated work. A retry supported by the documented evaluation
  scope and skill-creator forward-testing guidance was approved. Verification then
  completed; no outstanding approval remains.

The evaluated implementation's SHA-256 was
`58e0e7aa6a9aaed8a906bacb441321f7b3c0bf3b6e35d47cdf55460dd0480da4`.
The trial exercised actual cooperating agents using the skill files. It did not
establish loading or dispatch of the generated native TOML roles in a VS Code
extension session. The other probes in [the evaluation guide](../evals/README.md)
are available for future runs and are not reported as executed.

### Limits

Official documentation was checked for local skill discovery, custom-agent file
fields, and IDE use. Native role loading and skill discovery in the user's actual
VS Code environment remain unverified. The doctor is a local file diagnostic,
not an extension, account, or model-access test. Bash tests ran on macOS; Linux,
WSL, and Git Bash compatibility follows the portable command design but was not
executed on those operating systems.

No personal installation or application repository setup was performed during
validation. Tests used temporary targets, including an inert stub to test default
personal-scope argument routing without writing to the user's home. No global
Codex configuration, model choices, or VS Code settings were changed.

## Prior version 1 checks — 2026-09-22

Version 1 passed 13 installer tests and a 59-file full-package install/repeat/remove
smoke test. A separate local CSV-export trial passed eight behavior tests and its
usage example. That trial used sequential specialist workflows because all agent
slots were occupied; the version 2 trial above exercised separate cooperating agents.
