# Validation record

Validated on 2026-09-22 with Python 3.13 on macOS.

- **Package validation:** 19 skill frontmatters, 19 native agent TOML files, 19 UI metadata files, companion mappings, manager routes, and local reference links pass `python3 scripts/validate.py`.
- **YAML parsing:** Ruby's safe YAML parser successfully parsed all 38 skill-frontmatter and UI-metadata documents. The bundled skill-creator Python validator could not run because PyYAML was unavailable; the package validator and independent YAML parse were used instead.
- **Installer tests:** All 13 tests pass with `python3 -m unittest discover -s tests -v`. They cover temporary project and simulated user targets, dry runs, repeat installation, managed updates, conflicts before mutation, local-edit preservation, uninstall ownership, and symlink refusal. An initially missing check for symlinked source skill directories was fixed and its regression test passes.
- **Full package smoke test:** The actual CLI installed 19 skills and 19 native agents (59 managed files) in a temporary project. All installed agent TOMLs parsed. A repeat installation made zero changes. Clean uninstall removed every managed file.
- **Independent content review:** Reviewed role boundaries and routing. Clarified that direct React review requests return findings unless changes are requested or already authorized.
- **Manager workflow trial:** An independent agent used the manager skill in a disposable Node service fixture to add a user's own-notes CSV export, repair CSV escaping, and document usage. The original two tests passed; four new checks failed before implementation; all eight final tests passed. A documented local download command also succeeded. Specialist workflows ran sequentially because all agent slots were occupied, so this trial does not establish concurrent custom-agent dispatch.

Native agent authoring and discovery paths were checked against the official documentation linked in the README. These checks do not establish successful loading in your particular VS Code extension version. The locally available Codex CLI terminated before reporting a version, so native runtime loading was not validated through that executable. Start a new Codex conversation after installation and confirm skill discovery; update the extension if native role selection is unavailable.

No personal or application repository installation was performed as part of validation. All installation and workflow trials used temporary directories. No model settings, global Codex configuration, or VS Code settings were changed.
