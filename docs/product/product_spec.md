# Product specification

## The job

Creative operations teams receive campaign intent as prose, assets as folders, and launch rules as spreadsheets. The last mile is repetitive but risky: one missing approval, wrong destination, unsupported placement, or broken UTM can invalidate a large batch.

Creative Launch Workspace turns that material into a review queue with an explicit owner and fix for every issue.

## Workflow

1. A synthetic brief is converted into a mapping proposal.
2. Every proposed field carries its source evidence and an uncalibrated confidence band.
3. Missing, conflicting, unsafe, or non-synthetic inputs cause abstention.
4. A person accepts or rejects each field.
5. The accepted mapping passes deterministic field validation and can seed a synthetic manifest template.
6. The materialized rows enter the existing manifest validators before the operator reviews or exports local state.
7. A bounded browser lab lets a visitor correct three synthetic fields and replay Python-generated golden validation outcomes.
8. A three-step guided review selects a pending ambiguous row, reuses the normal local decision path, and exposes the resulting audit event before handing the visitor into the full queue.

The system never publishes ads. The final artifact is intentionally non-executable.

## Success criteria

- A reviewer can find and route launch blockers without reading implementation docs.
- Model output cannot bypass schema, allowlist, evidence, review, or deterministic gates.
- A blocked row cannot be approved through either the browser or SQLite path.
- The same synthetic inputs produce byte-stable evidence artifacts.
- All external writes remain impossible in the current release.
- A LinkedIn visitor can understand the business problem, Mathieu's ownership, the authority boundary and the product workflow before opening the operator UI.
- A first-time visitor can complete one real local decision without learning the full 100-row workspace first.

## Current proof

- 100 synthetic creative rows across three campaigns and ten ad sets.
- 70 seeded issues detected and routed: 60 blockers and 10 reviewer decisions.
- 48 synthetic brief cases: 36 baseline contract cases plus 12 natural-prose/adversarial live-provider cases.
- Browser interaction QA at seven viewport widths plus a dedicated 320×568 guided-review contract.
- Lighthouse accessibility 100/100 on desktop and mobile.
- Product landing Lighthouse quality budgets for performance, best practices, SEO, LCP, CLS and total blocking time.
- Eight correction/revalidation scenarios generated from the Python validators and exercised in the browser.

These numbers describe the included fixtures. They are not customer or production results.
