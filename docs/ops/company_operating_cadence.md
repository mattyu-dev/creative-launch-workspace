# Company Operating Cadence

Date: 2026-07-05
Owner: Chief of Staff / Loop OS Owner
Status: active operating cadence

## Cadence

Every broad loop must run this cadence:

1. Director / GM opens intake and names the customer, product, and evidence objective.
2. Executive council routes the work to Product, Engineering, Platform, Security, QA, GTM, and Ops as needed.
3. Managers create bounded slices with owner, artifact, gate, and merge-back path.
4. Work lands in code, docs, fixtures, or vault notes.
5. Manager review checks acceptance criteria.
6. Leader review checks strategy and risk.
7. QA / Evidence runs the narrowest sufficient proof.
8. Director / GM reopens the frontier and disposes remaining safe work.

## Required Reviews

| Surface | Required Review |
| --- | --- |
| Product workflow | Product plus Creative Ops |
| Import contract | Data Pipeline plus CTO |
| Reliability path | SRE plus Data Pipeline |
| External integration | Platform plus Security plus HITL |
| Customer claims | GTM plus QA / Evidence |
| Readiness claim | Director / GM plus QA / Evidence |

## Kill/Pivot Review

Run a kill/pivot review when any of these happens:

- Three agency rehearsals fail to prove meaningful time savings.
- Operators say safe export has no value without direct external publishing.
- Existing tools already satisfy review, QA, and launch workflow needs.
- Platform contract research shows core workflow fields cannot be mapped cleanly.
- Trust architecture makes the first paid workflow too heavy for the expected buyer.

## Branch And CI Discipline

- Keep work in small slices.
- Run local validation before claiming readiness.
- Keep generated vault surfaces fresh.
- CI must run product tests, gate checks, vault checks, and whitespace checks.
- Do not stage or commit unrelated local work.

## Decision Hygiene

Every material decision needs:

- Decision owner.
- Evidence path.
- Rejected alternatives.
- Revisit trigger.
- Claim tier.
- Merge-back surface.
