# Optional project context

Copy the relevant parts into your existing repository instructions or task brief. Fill them from the repository; omit unknowns instead of guessing. This file is a worksheet, not an automatically loaded instruction file.

| Topic | Project facts |
| --- | --- |
| Product and audience | |
| Current outcome and acceptance | |
| Stack, versions, package manager | |
| Entry points and important modules | |
| Development startup | |
| Lint, typecheck, tests, build | |
| Existing test data and local services | |
| Authentication and permission boundaries | |
| Data sensitivity and migration constraints | |
| Browser, accessibility, and compatibility targets | |
| Deployment environment and release process | |
| Operational dashboards and runbooks | |
| Voice, positioning, and substantiated product claims | |

If you want automatic coordination on substantial delivery requests, merge this short instruction into an existing `AGENTS.md`:

```markdown
For substantial tasks spanning multiple areas, use $sdlc-manager. Delegate
independent work to the installed sdlc_* custom agents when it will improve
speed or review quality. Give each file one writer, inspect the returned
evidence, and complete integration and relevant checks. For focused tasks,
use the relevant specialist directly. Preserve the user's scope and existing
authorization; do not turn analysis into implementation or local work into
an external release.
```
