# Toolkit repository map

This map covers the toolkit's source, generation, installation, and verification
flow. Recheck relevant files when changing that flow; this document is orientation,
not evidence that a later revision passed its checks.

## Maintained inputs and generated outputs

| Location | Responsibility |
| --- | --- |
| `catalog.json` | Version, role identities, short descriptions, and starter prompts |
| `skills/<name>/SKILL.md` | Specialist workflow and links to deeper guidance |
| `skills/<name>/references/` | Maintained specialist detail, except generated `collaboration.md` |
| `shared/collaboration.md` | Shared ownership, handoff, evidence, and context-reuse rules |
| `scripts/build.py` | Generates native agent TOMLs, skill UI metadata, and collaboration copies |
| `agents/sdlc_*.toml` | Generated native roles; model and permissions are inherited |

Flow: catalog + shared contract → `generated_files()` → `agents/*.toml`,
`skills/*/agents/openai.yaml`, and `skills/*/references/collaboration.md`.
Maintain the inputs, then run `python3 scripts/build.py`. Skill names use hyphens;
native agent names use underscores. Adding a role also requires manager routing.

## Installation and ownership

`install.sh` validates Python 3.11+, defaults to personal scope, and passes options
to `scripts/install.py`. `payload()` selects catalog-owned content. `run()` checks
conflicts before writing `.agents/skills`, `.codex/agents`, and a content-hash
ownership manifest. Update requires unchanged owned files. Uninstall preserves
local edits and pre-existing identical files. Symlinked destinations are rejected.

Keep changes to installation behavior in `scripts/install.py`; keep shell argument
and interpreter behavior in `install.sh`. Tests separate those responsibilities in
`tests/test_install.py` and `tests/test_shell.py`. `--doctor` checks installed files
and local configuration; extension loading and native role dispatch need a fresh
Codex runtime check.

## Project knowledge flow

`skills/sdlc-memory/scripts/knowledge.py` uses the standard library to maintain
`.sdlc/knowledge.json` in an explicitly selected repository. `list` returns a small
index; `read` rehashes listed evidence and checks expiry before returning a body.
`save` replaces one reviewed note under a write lock using an atomic file replacement.
Notes are data, never authority or executable instructions. Hashes cover only
registered source files; inventory, runtime, and external-policy changes still
require judgment. `tests/test_knowledge.py` checks this behavior.

The manager reuses current task evidence and selected notes. The mapper discovers
only unfamiliar or changed areas. One knowledge owner merges durable findings.
Project knowledge is outside the install manifest and distribution archive.

## Validation and packaging

From this repository root:

```sh
python3 scripts/build.py --check
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 scripts/context_report.py
python3 scripts/package.py
```

`validate.py` checks the package's constrained metadata, portable references,
role/manager consistency, and generated content. `context_report.py` reports static
character counts, not runtime tokens. `package.py` validates before writing
`dist/codex-sdlc-toolkit.zip`. `evals/` contains behavioral scenarios;
`docs/VALIDATION.md` distinguishes executed checks from unverified behavior.
