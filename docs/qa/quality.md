# Quality gates

The repository treats evidence as build output, not README decoration.

## Python

- installable package and `creative-launch` console entry point;
- Ruff static checks;
- mypy on the AI, clock, and review-policy boundaries;
- branch coverage with an 80% floor;
- unit and negative-path tests;
- a 48-case repo-native benchmark split between deterministic-contract and natural-prose live-provider suites;
- adversarial tests for missing risk flags, evidence/value mismatch, URL userinfo, proposal tampering and receipt tampering;
- deterministic regeneration checks.

## Browser

The generated workspace is exercised in Chrome at seven widths, plus a dedicated 320×568 guided-review contract. QA covers filtering, row selection, bulk confirmation, undo, local persistence, guarded state import, keyboard navigation, the mobile decision sheet, and no-network behavior. It also completes the three-step guided review, verifies the selected ambiguous row and owner, records a real local decision, inspects its audit event, rejects any non-GET or external request, confirms the next pending case after reload, and exits to all 100 rows.

The same runtime suite checks the portfolio entry metadata and responsive layout, replays the Fix & Revalidate Lab from blocked to launch-ready and back, and verifies the field-level evidence page contract. Social, desktop and mobile screenshots are generated from those tested pages.

Lighthouse accessibility must remain 100/100 on desktop and mobile for both the task-first workspace and the portfolio landing. In addition, the runtime gate enumerates every failed Lighthouse audit and rejects any serious or critical WCAG-tagged failure so rounding cannot hide a regression. The committed screenshots and JSON reports are rebuilt by the same script used in CI.

The portfolio additionally enforces reproducible local Lighthouse budgets: performance at least 90, best practices and SEO at least 95, LCP no more than 2.5 seconds, CLS no more than 0.1 and total blocking time no more than 200 milliseconds. These are laboratory checks against the locally served static build, not production real-user monitoring.

## Media fixtures

Synthetic image and video files are real decodable JPEG and MP4 containers. The validator checks checksums, size, MIME signature, decoded JPEG dimensions, MP4 core boxes and duration metadata. The 64px media are decoder fixtures, not ad-quality creative.
