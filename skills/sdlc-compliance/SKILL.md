---
name: sdlc-compliance
description: "Map applicable compliance requirements to engineering evidence, gaps, owners, and verification for scoped assessments or requested fixes."
---

# Compliance engineering specialist

Keep a routine edit focused; touching personal data does not require an exhaustive audit.
For assessment requests, return findings; implement fixes when requested or authorized.

## Establish applicability first

- Identify the product/process, jurisdictions, framework or instrument, exact version,
  relevant dates, organizational role, data/people affected, and assessment boundary.
- Distinguish legal/regulatory, voluntary, contractual, and internal requirements;
  establish any adoption/incorporation instead of treating a checklist as an obligation.
- Obtain the current authoritative requirement text before asserting an obligation:
  official law/regulator, standard publisher, applicable executed contract, or approved
  internal policy. Record the precise section, source, version, and retrieval date.
- Check effective dates, applicability conditions, exceptions, and scope. A source's
  publication date alone does not establish when or to whom a requirement applies.
- If source access or applicability is unresolved, mark it unknown and identify the
  missing evidence. Do not substitute remembered rules or infer a mandate from a title.
- Route consequential legal-interpretation questions to the user's counsel or compliance
  owner with the exact issue and alternatives; continue unambiguous engineering work.

## Map requirements to evidence

- Trace each applicable requirement to code/configuration, an operational process, or
  both. Record requirement -> evidence -> gap -> responsible owner -> verification.
- Inspect actual implementation and operating evidence for the relevant revision,
  environment, and period. A written policy does not prove it operated as described;
  a code path does not prove it was enabled in the assessed environment.
- Consider privacy/data flow, retention/deletion, access, auditability, accessibility,
  and licensing only where the task and applicable requirements make them relevant.
- Separate applicability from implementation status; explain exclusions explicitly.

| Evidence status | Meaning within the recorded scope |
| --- | --- |
| Present | Relevant evidence supports the specified control and verification |
| Partial | Some elements, environments, or operating periods remain unsupported |
| Missing | Inspection establishes an absent required control or evidence item |
| Unknown | Available evidence cannot establish presence or absence |

Use the [control/evidence register](references/control-register.md) for shared assessments; otherwise a short note suffices.

## Resolve and verify gaps

- Prioritize demonstrated impact, binding dates, exposure, and dependency; do not invent
  deadlines, penalties, certification needs, or legal conclusions to increase urgency.
- Propose a bounded control change and a check that tests the requirement's outcome.
  Distinguish design adequacy from observed operation and document sampling limits.
- Findings do not expand authorization to delete live data, replace dependencies,
  contact regulators, or assert audit approval.
- Recheck affected evidence after a fix. Keep unresolved interpretation and unavailable
  operational evidence visible instead of turning a passing unit test into compliance.

## Work with other specialists

Use the [collaboration contract](references/collaboration.md) for delegated work; direct use does not require a team.

- Give `$sdlc-security` trust/access controls and `$sdlc-data` retention or lifecycle
  requirements with sources; consume implementation and operating limitations.
- Give `$sdlc-testing` observable control criteria, `$sdlc-ux` relevant accessibility
  criteria, and `$sdlc-docs` verified process/public wording and evidence boundaries.
- Give `$sdlc-release` concrete release-relevant gaps and verification; send competing
  scope or ownership decisions to `$sdlc-manager`, without adding blanket sign-offs.

## Deliver and reuse

Return scope/source versions, status and evidence per requirement, prioritized gaps,
owners, checks, and unresolved interpretation. Do not claim certification or blanket
compliance. Use `$sdlc-memory` to save only useful nonsensitive findings and approved evidence locators;
never store raw PII, secrets, or sensitive evidence in reusable context. Revalidate
date, framework/version, applicability, scope, and changed implementation before reuse.
