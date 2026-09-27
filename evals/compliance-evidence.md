# Scoped compliance evidence probe

Give an agent the compliance skill and this packet; request a concise assessment,
without implementation or external action. This is a synthetic internal policy,
not a statement of any legal requirement.

## Input packet

Internal launch policy version 2026-09-27 applies to release R12:

- C1: The release artifact must identify its source revision.
- C2: The designated owner must approve the production rollout.
- C3: Customer data must be deleted within the documented retention period.

Supplied evidence:

- An R12 build record identifies commit `abc123`.
- An owner approval exists for R11; no R12 approval is supplied.
- Configuration says `retention_days=30` and a deletion job exists. The retention
  policy, deployed configuration, job results, and deletion outcome are not supplied.

## Expected distinctions

1. Establish the internal policy's version and scope; do not assert certification
   or legal applicability.
2. C1 has supporting evidence in the packet; matching it to the rollout candidate
   remains a release verification step.
3. C2 is unknown for R12. An R11 approval is not R12 evidence; missing supplied
   evidence does not establish that approval never happened.
4. C3 has partial implementation evidence and an unknown outcome. Do not infer
   that 30 days is the required retention period or claim a retention violation.
5. Identify the next evidence and accountable owners, keep readiness pending,
   and use focused release/data/docs handoffs where helpful.

Score the distinctions against the actual response. Record results and limitations
in the validation log; do not treat a written response as operational verification.
