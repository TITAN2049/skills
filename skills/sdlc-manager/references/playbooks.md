# Delivery playbooks

Choose the relevant shape, then scale it to the actual task. These are dependency
patterns, not mandatory lists of agents. Every handoff follows the collaboration
contract; the manager is responsible for accepting the integrated outcome.

Reuse current task context and relevant verified knowledge before discovery. Map
only the affected area when structure is unfamiliar. Save a durable finding once
through its assigned knowledge owner; never send every specialist to reread or
rewrite the project memory.

## Feature across UI, API, and data

1. Product establishes observable acceptance and exclusions. Architecture resolves
   only consequential uncertainties; a known local pattern does not need an ADR.
2. Agree on the interface, authorization, error states, and migration compatibility.
   Give shared types and migrations explicit owners.
3. React, backend, and data owners can implement disjoint files once their shared
   contract is stable. Feature engineering may own a whole small slice instead.
4. Testing derives user scenarios and boundary cases from acceptance, independently
   of implementation details. Run affected integration checks once producers and
   consumers are ready. Security or UX checks are included where relevant.
5. Docs consume verified behavior. Marketing consumes a claim ledger grounded in
   implemented availability. Release consumes artifact-specific check evidence.

Example: AC1 says only the account owner can export saved reports. Backend owns
the access check and response contract; React owns pending/error/download behavior;
testing verifies cross-account refusal and the permitted path. UI button visibility
is not sufficient evidence for AC1. A payload change returns to affected owners
before the parent accepts the slice.

## Broken behavior or a failing pipeline

Have debugging establish the trigger, observed failure, and plausible causal path.
Use a domain specialist when the failure crosses a boundary or requires deeper
knowledge. Give one owner the repair. Testing proves the original failure is gone
and consequential nearby behavior remains. DevOps contributes runtime/build inputs
for environment-specific failures. A flaky rerun is evidence to investigate, not
a repair. Keep unrelated cleanup out of the patch.

## Cleanup or performance

Refactoring starts with observable behavior and callers to preserve. Performance
starts with a representative workload and baseline measurement. Domain owners make
bounded changes; tests and measurements compare the same behavior and conditions.
Do not claim a performance improvement from fewer lines of code or turn a cleanup
request into a feature change. Docs change only if public usage or operations change.

## Review and remediation

Give a reviewer the requested baseline, candidate, original criteria, and relevant
context. Security or testing can independently inspect specific risks. Findings
identify trigger, consequence, location, and confidence. If repair is authorized,
assign each finding to one owner; the reviewer reassesses the changed path after
its evidence is updated. Review alone does not authorize rewriting the branch.

## Compliance assessment

Compliance establishes the applicable instrument, version, product role, and scope
before deriving requirements. Security and data owners supply concrete control
evidence; docs distinguish implemented behavior from promises. The register records
present, partial, missing, or unknown evidence plus owner and next check. Regulatory
interpretation and certifications cannot be inferred from code or a passing test.
Revalidate cached requirements against current authoritative sources and scope.

## Release and launch

Release verifies the actual candidate, environment, compatibility, and recovery
path. DevOps supplies immutable artifact/deployment evidence. Data supplies migration
order and recovery limits. Docs and marketing reflect verified feature availability
and rollout restrictions. Deploy or publish when that action is already authorized;
readiness work alone is not permission. Check resulting behavior and state after
any authorized external mutation.

## Incident

Incident coordination establishes impact, timeline, and success/failure signals for
authorized mitigation. Debugging, DevOps, security, or data investigate separate
hypotheses while a single owner controls each operational mutation. Inspect state
before retrying uncertain actions. After recovery, route prevention work to the
appropriate owners with evidence; do not imply an observation period has elapsed
or send incident messages to other people without authorization.
