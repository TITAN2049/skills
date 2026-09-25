---
name: sdlc-security
description: Review software for concrete security weaknesses, threat-model a scoped change, or implement requested security fixes. Use for security assessments and security-sensitive changes; report demonstrated risk without claiming compliance or treating every code change as an audit.
---

# SDLC Security

Assess how an attacker could cross a real trust boundary and what that would expose or change.
For review or audit requests, report findings by default; implement fixes when requested or already authorized.

## Bound the assessment

- Identify the requested components, deployed assumptions, data sensitivity, and relevant actor roles.
- Read authentication, authorization, input processing, secret handling, and deployment configuration only as relevant.
- Separate facts observed in code or configuration from deployment assumptions needing confirmation.
- Preserve the requested scope; a finding does not authorize external scanning, production changes, or contacting others.
- Use read-only inspection and safe local fixtures until a consequential action has applicable authorization.

## Trace credible attack paths

- Trace an entry point through validation and authorization to its sensitive operation or data sink.
- Identify attacker-controlled inputs, prerequisites, existing protections, and bypass conditions.
- Check authorization at the resource and operation level, including cross-user or cross-tenant access.
- Follow data through parsing, transformation, storage, rendering, and outbound requests where relevant.
- Consider injections, unsafe file paths, untrusted deserialization, SSRF, session handling, and exposure only where the code supports that path.
- For web state changes, inspect the actual cookie, token, origin, and CSRF design before asserting a weakness.
- Examine retries, races, and replay when they could bypass an important security invariant.

## Evaluate evidence

- Establish whether the vulnerable code executes in the relevant configuration and whether an attacker can reach it.
- For dependency findings, verify the resolved version, advisory conditions, usage, and available mitigations.
- Treat scanner results and dependency alerts as leads to investigate, not automatic confirmed vulnerabilities.
- Consult authoritative advisories or vendor documentation when version-specific behavior matters.
- A missing defensive layer alone is not proof of an exploitable defect; explain its effect in context.
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
- Avoid replacing authentication, cryptography, or policy architecture when a scoped repair suffices.
- If a credential is exposed, describe containment and rotation needs without silently revoking shared credentials.
- Verify the fix against the original path and nearby bypasses supported by evidence.

## Handoff

For each actionable finding, provide location, attacker prerequisites, execution path, impact, confidence, and a concrete remediation.
Prioritize using exploitability, exposure, impact, and existing controls; separate hardening suggestions from vulnerabilities.
Report verification commands and outcomes, including unresolved assumptions or blocked checks.
If no actionable issue is found, say so with the reviewed scope and limits; do not certify security or compliance.
