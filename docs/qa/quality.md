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

The generated workspace is exercised in Chrome at seven widths. QA covers filtering, row selection, bulk confirmation, undo, local persistence, guarded state import, keyboard navigation, the mobile decision sheet, and no-network behavior.

The same runtime suite checks the portfolio entry metadata and responsive layout, replays the Fix & Revalidate Lab from blocked to launch-ready and back, and verifies the field-level evidence page contract. Social, desktop and mobile screenshots are generated from those tested pages.

Lighthouse accessibility must remain 100/100 on desktop and mobile. The committed screenshots and JSON reports are rebuilt by the same script used in CI.

## Media fixtures

Synthetic image and video files are real decodable JPEG and MP4 containers. The validator checks checksums, size, MIME signature, decoded JPEG dimensions, MP4 core boxes and duration metadata. The 64px media are decoder fixtures, not ad-quality creative.
