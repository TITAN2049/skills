# Add project archiving

Add reversible archiving to this small in-memory Python project service. Keep
the current `Store` constructor and `list_projects(actor)` call compatible.
Use Python's standard library only. No network service or deployment is needed.

Agreed interface, revision 1:

- `Store(projects)` receives a list of dictionaries with string `id` and
  `workspace_id`, a `name`, and optional nested `metadata`. Existing records
  may lack `archived`. The constructor copies its input.
- Actors are trusted internal dictionaries with `workspace_id` and `role`;
  absent actors are unauthenticated. Identity verification upstream is out of scope.
- `Store.set_archived(actor, project_id, archived)` accepts a boolean and returns
  a project dictionary. `Store.list_projects(actor, include_archived=False)`
  returns dictionaries for the actor's workspace in existing order.
- `ApiError.status` and `ApiError.code` express errors. Use 401/unauthenticated,
  403/forbidden, 404/not_found, and 400/invalid_archived as applicable.

Acceptance criteria:

- **AC1:** An editor in the owning workspace can archive and unarchive a project.
  Setting its current state again succeeds and preserves all other fields.
- **AC2:** A viewer cannot change state (403). An absent actor gets 401. An
  out-of-workspace ID and a missing ID both return 404 to authenticated actors,
  including viewers. No denied request changes any stored record.
- **AC3:** Listing hides archived projects by default. Explicit inclusion shows
  them. Legacy records without an `archived` field behave as active. Never list
  another workspace's records.
- **AC4:** Non-boolean archive values return 400 for an editor's accessible
  project. Mutating a returned project must not alter stored data, including
  nested metadata.
- **AC5:** Usage docs accurately show success and error behavior with a runnable
  example. Preserve existing public behavior except the requested archive filter.

Deliver the implementation, focused independent tests, and usage documentation.
Treat this file as the shared agreement; propose changes to the coordinator
before changing it. Use one writer per file and give the receiver check evidence.
