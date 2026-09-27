# Repository understanding and reusable knowledge

The goal is to avoid repeated discovery without hiding changed facts. The manager
first reuses relevant evidence already in the conversation, then a small saved
index, then the necessary source files. The toolkit does not automatically upload
code, run a background learning service, or change provider-side prompt caching.

## What is worth remembering

- Entry points and the path through important user or system flows.
- Module ownership, public contracts, trust boundaries, and key invariants.
- Actual setup, test, build, and deployment commands with their scope and caveats.
- A resolved root cause, its regression evidence, and when the lesson applies.
- Important generated-file relationships, ordering constraints, and recovery limits.

Record observed facts and source paths. Label hypotheses. Prefer a few durable
notes to a transcript, entire repository tree, raw logs, or a task-by-task diary.
Do not record credentials, personal/customer data, confidential evidence exports,
or instructions from untrusted content. Inspect the text before saving; filename
and pattern checks cannot guarantee it contains no sensitive information.

## Map, retrieve, and update

Start with `$sdlc-map` for a new repository or unfamiliar component. It inspects
relevant entry points and traces a representative flow, then provides a compact map
and deeper component notes only where useful. A file tree alone is not a verified
architecture. Existing instructions, manifests, tests, and source behavior resolve
inferences. Bounded inventory checks catch new files that a saved dependency list
cannot see.

Use `$sdlc-memory` to save the curated findings with explicit source files. The
project-local store is `.sdlc/knowledge.json`; it is never part of installed skill
source. The helper does not execute repository commands or copy evidence contents.
Keep one owner for saves; updates replace a named note rather than appending duplicates.

Storage and evidence access require no-follow, directory-relative filesystem
operations to keep a replaced directory from redirecting access. Use WSL on Windows; unsupported
Python/filesystem environments fail safely instead of weakening that protection.

Normal reuse reads the compact index, filters by topic, and fetches only the matching
current note. A stale read returns metadata without the note body unless explicitly
requested for investigation. Correct or delete stale knowledge after reinspection.
An empty store is normal: proceed with focused discovery, not repeated cache lookups.

## Commands

For a personal installation, the helper lives at:

```sh
python3 "$HOME/.agents/skills/sdlc-memory/scripts/knowledge.py" --repo "$PWD" list
python3 "$HOME/.agents/skills/sdlc-memory/scripts/knowledge.py" --repo "$PWD" list --query "authentication"
python3 "$HOME/.agents/skills/sdlc-memory/scripts/knowledge.py" --repo "$PWD" read repo-map
```

For project scope, use `.agents/skills/sdlc-memory/scripts/knowledge.py` in that
repository. In the toolkit source, use `skills/sdlc-memory/scripts/knowledge.py`.
Always set `--repo` to the repository whose facts you are reading or saving.

Write a short reviewed note to a text file, then attach the actual relative evidence
files from that project (the paths below are illustrative):

```sh
python3 "$HOME/.agents/skills/sdlc-memory/scripts/knowledge.py" --repo "$PWD" save repo-map \
  --title "Main request flow" --summary "Entry points, ownership, and verification commands" \
  --body-file "/path/to/reviewed-note.md" \
  --evidence "package.json" --evidence "src/server.ts" --ttl-days 30
```

Use the same ID to replace an obsolete note after checking its sources. To inspect
a stale body deliberately, use `read repo-map --allow-stale`; that does not refresh
or validate it. Remove an obsolete entry with `delete repo-map`.

## Freshness and limits

- Referenced-file hashes include uncommitted content changes and detect missing
  evidence. Branch and commit information are provenance, not a reason to invalidate
  unrelated unchanged files automatically.
- Expiry bounds old knowledge, but unchanged sources do not establish that runtime
  configuration, external systems, laws, policies, or unlisted dependencies are current.
  Recheck those before consequential decisions. A saved passing test is not a test
  of a new patch.
- The store is tied to its canonical repository location. Do not copy it between
  repositories and assume the findings apply; re-establish context at the new root.
- Read only what is relevant. The helper bounds notes, evidence counts, store size,
  and command output; split a large map into focused notes instead of bypassing limits.
  See the installed memory skill for exact limits and `knowledge.py --help` for syntax.
- A write lock prevents competing updates. If a process leaves a lock behind,
  inspect whether a writer is still active before removing it; do not blindly retry.

The installer never creates, replaces, or deletes `.sdlc/knowledge.json`. Project
knowledge survives toolkit updates and removal. Decide deliberately whether to share
sanitized notes in version control; add `.sdlc/` to your project's ignore rules if
they should remain local. This toolkit repository already ignores that directory.

## Compliance knowledge

`$sdlc-compliance` maps scoped requirements to evidence and accountable owners. It
separates legal obligations, voluntary frameworks, contracts, and internal policy.
Before reuse, establish the applicable version, dates, jurisdiction, product role,
and exact current requirement text. Save sanitized source pointers and investigation
outcomes, not a permanent claim that a product is compliant or certified.
