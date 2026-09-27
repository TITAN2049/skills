---
name: sdlc-security
description: "Assess concrete trust-boundary weaknesses or implement authorized security repairs; distinguish risk from conjecture."
---

# SDLC Security

Reuse the parent's relevant verified context. Before repeating discovery, use $sdlc-memory's compact index when available; inspect only matching notes and changed evidence.

Assess how an attacker could cross a real trust boundary and what that would expose or change.
For review or audit requests, report findings by default; implement fixes when requested or already authorized.

## Bound the assessment

- Identify the requested components, deployed assumptions, data sensitivity, and relevant actor roles.
- State the security invariant being evaluated, such as which actor may read or mutate which resource; do not assume authentication alone grants access.
- Read authentication, authorization, input processing, secret handling, and deployment configuration only as relevant.
- Separate facts observed in code or configuration from deployment assumptions needing confirmation.
- Preserve the requested scope; a finding does not authorize external scanning, production changes, or contacting others.
- Use read-only inspection and safe local fixtures until a consequential action has applicable authorization.

## Trace credible attack paths

- Trace an entry point through validation and authorization to its sensitive operation or data sink.
- Identify attacker-controlled inputs, prerequisites, existing protections, and bypass conditions.
- Check authorization at the resource and operation level, including cross-user or cross-tenant access.
- Include indirect access through caches, background jobs, exports, batch endpoints, and storage URLs when they serve the same protected resource.
- Check that authorization uses the final resolved resource identity after decoding, lookup, aliasing, or canonicalization, rather than trusting a caller-supplied ownership claim.
- Follow data through parsing, transformation, storage, rendering, and outbound requests where relevant.
- Evaluate protections at the relevant sink: validation, output encoding, parameterization, and URL restrictions protect different boundaries and are not interchangeable.
- Consider injections, unsafe file paths, untrusted deserialization, SSRF, session handling, and exposure only where the code supports that path.
- For web state changes, inspect the actual cookie, token, origin, and CSRF design before asserting a weakness.
- Examine retries, races, and replay when they could bypass an important security invariant.

## Evaluate evidence

- Establish whether the vulnerable code executes in the relevant configuration and whether an attacker can reach it.
- For dependency findings, verify the resolved version, advisory conditions, usage, and available mitigations.
- Treat scanner results and dependency alerts as leads to investigate, not automatic confirmed vulnerabilities.
- Consult authoritative advisories or vendor documentation when version-specific behavior matters.
- A missing defensive layer alone is not proof of an exploitable defect; explain its effect in context.
- Classify evidence as reproduced, supported by a complete code path, or unresolved; describe the exact deployment or actor assumption that could change the conclusion.
- Do not invent exposure, affected users, or successful exploitation from code inspection alone.

## Validate safely

- Reproduce with isolated test data and local or explicitly authorized test systems.
- Prefer a minimal proof of the violated boundary over broad payload lists or disruptive traffic.
- Use synthetic secrets and redact any real credentials encountered; do not copy secrets into reports or tests.
- Do not access another person's records to prove an issue when owned fixtures can establish it.
- Keep test volume bounded and avoid persistence, data destruction, or external side effects outside authorized scope.
- When safe reproduction is unavailable, label the finding's uncertainty and identify the evidence needed.

## Repair when authorized

- Fix the vulnerable boundary, preserving legitimate workflows and established APIs where possible.
- Add a focused regression check for the attack condition and a representative allowed path.
- Verify the rejected request cannot produce a partial protected side effect before returning an error; a denial response alone may conceal a write or information leak.
- Avoid replacing authentication, cryptography, or policy architecture when a scoped repair suffices.
- If a credential is exposed, describe containment and rotation needs without silently revoking shared credentials.
- Verify the fix against the original path and nearby bypasses supported by evidence.

## Work with other specialists

Use the [collaboration contract](references/collaboration.md) for scoped handoffs; a direct assessment can finish without delegation.
Route shared ownership or contract changes through `$sdlc-manager`; do not recursively create a security review team.

- Give `$sdlc-backend` or `$sdlc-react` a reachable failure path, affected invariant, and constrained repair proposal; assess the returned fix at the same trust boundary.
- Give `$sdlc-testing` safe actor/resource fixtures and independently defined allow/deny outcomes when a regression check needs deeper test infrastructure.
- Give `$sdlc-devops` observed identity, secret, or pipeline permission facts when exposure depends on configuration; give `$sdlc-incident` confirmed active impact when containment is needed within the task's authority.

## Handoff

For each actionable finding, provide location, attacker prerequisites, execution path, impact, confidence, and a concrete remediation.
Prioritize using exploitability, exposure, impact, and existing controls; separate hardening suggestions from vulnerabilities.
Report verification commands and outcomes, including unresolved assumptions or blocked checks.
For a repaired finding, state whether the exploit condition is closed, legitimate access still works, and any exposure requiring separate containment remains.
If no actionable issue is found, say so with the reviewed scope and limits; do not certify security or compliance.
