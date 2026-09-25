# SDLC team for Codex in VS Code

19 specialist agents and 19 reusable skills for planning, building, improving, testing, shipping, and supporting software. Start with **SDLC Manager** for coordinated work, or invoke a specialist directly.

The manager chooses the roles a task needs, assigns clear ownership, and checks the integrated result. Small fixes stay small. React is covered in depth; backend, database, infrastructure, and testing skills adapt to the stack already in your repository.

## Set up in VS Code

1. Install the official [Codex IDE extension](https://developers.openai.com/codex/ide), sign in, and open your application repository.
2. Open a terminal in this toolkit folder. Use Python 3.11 or newer (`python3` on macOS/Linux, usually `py -3` on Windows).
3. Install into your application repository, replacing the example path:

   ```sh
   python3 scripts/install.py --project "/absolute/path/to/your-app" --dry-run
   python3 scripts/install.py --project "/absolute/path/to/your-app"
   ```

4. Start a fresh Codex conversation in that repository. Type `$sdlc-manager` or use `/skills` to find it. If it is missing, reload VS Code and start a new Codex conversation.
5. Try this:

   ```text
   $sdlc-manager Inspect this repository and its instructions, identify the
   stack and existing checks, then help me implement [describe the feature].
   Use specialists where useful, give each file one writer, and verify
   the integrated result.
   ```

To use the toolkit across your repositories, choose a personal install instead:

```sh
python3 scripts/install.py --user --dry-run
python3 scripts/install.py --user
```

Choose project or personal scope to avoid duplicate skill entries. For remote VS Code sessions, run the installer in the environment where Codex runs. The installer does not install Python, the Codex extension, or external connectors.

## Your team

| Skill | Specialist | Use it for |
| --- | --- | --- |
| `$sdlc-manager` | Overall manager | Scope, delegation, integration, completion |
| `$sdlc-product` | Product strategist | Requirements, priorities, acceptance criteria |
| `$sdlc-architecture` | Software architect | Boundaries, technical decisions, tradeoffs |
| `$sdlc-ux` | UX and accessibility | Flows, interaction states, keyboard usability |
| `$sdlc-react` | React engineer | Components, hooks, state, rendering, forms |
| `$sdlc-backend` | Backend/API engineer | Services, contracts, validation, authorization |
| `$sdlc-data` | Database engineer | Schemas, migrations, queries, integrity |
| `$sdlc-feature` | Feature engineer | New functionality and enhancements |
| `$sdlc-debug` | Debugging specialist | Broken behavior, regressions, root causes |
| `$sdlc-refactor` | Refactoring specialist | Cleanup, duplication, technical debt |
| `$sdlc-testing` | Test engineer | Behavior tests, regressions, test reliability |
| `$sdlc-security` | Security engineer | Threats, vulnerabilities, remediation |
| `$sdlc-review` | Code reviewer | Independent, actionable change review |
| `$sdlc-performance` | Performance engineer | Profiling, bottlenecks, measured improvement |
| `$sdlc-devops` | DevOps engineer | CI/CD, builds, environments, infrastructure |
| `$sdlc-release` | Release manager | Readiness, rollout, rollback |
| `$sdlc-docs` | Documentation specialist | User guides, developer docs, examples |
| `$sdlc-marketing` | Product marketer | Positioning, launch copy, growth experiments |
| `$sdlc-incident` | Reliability/incident engineer | Incident triage, recovery, prevention |

## How agents and skills fit together

A skill contains the specialist's workflow and can run in your current conversation. A native custom agent supplies a named role for delegated work and loads its companion skill. For example, `$sdlc-react` is paired with `sdlc_react`.

The main conversation normally uses `$sdlc-manager` and delegates to specialists. Merely mentioning a skill does not guarantee a separate agent was spawned. You can explicitly ask:

```text
Use sdlc_security and sdlc_testing as separate agents to review this branch.
Have each inspect a different risk area, wait for both, then summarize
the actionable findings with file references.
```

If custom role selection is unavailable, the manager can give the skill to a general subagent. If delegation itself is unavailable, it performs the workflows sequentially and says so. Installed roles are reusable instructions, not nineteen continuously running processes.

The agent files inherit your selected model, reasoning settings, and permissions. This package does not change your Codex configuration. For an optional concurrency cap, merge this into the appropriate existing `config.toml` rather than adding a duplicate `[agents]` table:

```toml
[agents]
max_concurrent_threads_per_session = 3
```

The cap excludes the parent session. Parallel work uses additional model tokens. These formats and settings follow the [official custom-agent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents).

## Everyday prompts

```text
$sdlc-debug Find and fix why the checkout button stops responding.
Reproduce the failure and verify the fix.

$sdlc-react Add filtering and pagination to this page using its existing
data-fetching approach, including loading, empty, and error states.

$sdlc-refactor Clean up this module while preserving public behavior.
Keep the change focused and verify the affected paths.

$sdlc-manager Implement saved searches. Include the relevant frontend,
API, database, test, and documentation work. Coordinate file ownership.

$sdlc-security Review this authentication change and report concrete
attack paths, affected locations, and proportionate fixes.

$sdlc-marketing Draft positioning and launch copy for the completed
feature using only claims supported by the product.

$sdlc-release Assess the release candidate, report missing evidence,
and prepare rollout and rollback steps.
```

For project-specific conventions, use the optional [project context worksheet](docs/PROJECT-CONTEXT.md). It includes a short snippet you can merge into `AGENTS.md` to request coordination automatically.

## What gets installed

```text
your-project/                     # or your home folder with --user
├── .agents/skills/sdlc-*/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/               # manager handoff and task-brief formats
└── .codex/
    ├── agents/sdlc_*.toml
    └── sdlc-toolkit-manifest.json
```

The skills use [Codex's documented local discovery locations](https://learn.chatgpt.com/docs/build-skills). Source files in this toolkit's `skills/` and `agents/` directories are for editing and packaging; run the installer to put them in discoverable locations. The installer copies files, so editing the source later does not silently change an installed project.

The installer leaves your existing `AGENTS.md`, `config.toml`, VS Code settings, application files, and model choices alone. It previews changes with `--dry-run`, checks conflicts before writing, and refuses differing unowned files or local modifications. Identical files that predate installation remain unowned. It rejects symlinked destination components instead of writing through them.

## Update or remove

After editing toolkit sources or obtaining an updated copy:

```sh
python3 scripts/build.py
python3 scripts/validate.py
python3 scripts/install.py --project "/absolute/path/to/your-app" --update --dry-run
python3 scripts/install.py --project "/absolute/path/to/your-app" --update
```

Updates replace only files recorded by the installer that still match their recorded hashes. When an installed file has local edits, compare and merge it manually; there is no overwrite switch. Use `--user` instead of `--project ...` for a personal installation.

```sh
python3 scripts/install.py --project "/absolute/path/to/your-app" --uninstall --dry-run
python3 scripts/install.py --project "/absolute/path/to/your-app" --uninstall
```

Uninstall removes only unchanged files owned by this installation. Edited or unowned files remain, and empty directories may remain. Keep this toolkit folder available for updates and removal.

## Customize and verify

Edit a specialist's `skills/<name>/SKILL.md` to change its workflow. Edit `catalog.json` for role titles, short descriptions, and example prompts. Regenerate the native agents and skill UI metadata:

```sh
python3 scripts/build.py
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

The package validator uses only Python's standard library and checks this package's intentionally simple frontmatter format, native TOML, role mappings, references, and generated-file consistency. It is not a general YAML validator. The installer tests use temporary folders.

See the [validation record](docs/VALIDATION.md) for completed checks and runtime verification limits.

If skills appear but custom agents do not, update your Codex extension and start a new session. Custom agent formats can differ across older clients. Skill invocation remains the fallback; this package does not modify older clients' legacy configuration automatically.

No MCP server or external service is required. Specialists use tools available in the current session and report when browser access, a service, or verification is unavailable.
# skills
