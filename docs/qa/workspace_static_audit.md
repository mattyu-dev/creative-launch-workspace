# Workspace Static And Browser Audit

Date: 2026-07-11
Owner: QA / Evidence Lead
Status: active local/offline QA slice

## Goal

Add deterministic local QA for the static launch workspace so UI regressions are caught before the project claims operator usability.

This is not a replacement for a full Playwright/axe/screen-reader suite. It is a fixture-backed guard plus a local headless Chrome smoke check that keeps the workspace from losing core accessibility and workflow affordances.

## Contract

`workspace_html_static_audit.v1` now runs 28 checks. It covers:

- workspace title;
- row detail, preview, and export panels;
- an `aria-live` region;
- filter buttons with `aria-pressed` state;
- table caption;
- labelled controls;
- Enter and Space keyboard row-selection hooks;
- `localStorage` read/write hooks;
- empty-filter and persistence-error states;
- local export confirmation, guarded bulk actions, confirmation, and undo;
- strict imported-state validation;
- a mobile decision drawer with focus return;
- roving row tabindex plus arrow-key navigation;
- truthful synthetic versus operator-supplied copy;
- skip navigation, active-row semantics, reduced-motion support, and mobile row labels;
- the Editorial Operations design contract and anti-slop rules;
- responsive CSS;
- no external network-call tokens.

## Rehearsal Command

```bash
python3 -m meta_importer.cli plan fixtures/fake_agency_creatives/manifest_v2.csv --out runs/fake_agency_creatives_v2/launch_plan.json --review runs/fake_agency_creatives_v2/review_packet.md --html runs/fake_agency_creatives_v2/workspace.html --html-audit runs/fake_agency_creatives_v2/workspace_audit.json --state runs/fake_agency_creatives_v2/review_state.json --store-dir runs/fake_agency_creatives_v2/store --asset-metadata fixtures/fake_agency_creatives/asset_metadata.csv
```

## Current Result

- Contract: `workspace_html_static_audit.v1`.
- Status: `pass`.
- Checks passing: 28 of 28.
- Browser contract: 13 of 13.
- Runtime viewport proof: 320, 375, 390, 760, 1023, 1024, and 1440 px all have `scrollWidth <= innerWidth`.
- Runtime interaction proof: drawer open/close and focus return, one roving tab stop, arrow-key selection, exact-count bulk confirmation, cancel, confirm, undo, stale-selection reconciliation, localStorage persistence after reload, and reset.
- Runtime console: zero warnings or errors during the interaction pass.
- Lighthouse accessibility: 100/100 desktop and 100/100 mobile.
- Browser desktop screenshot: `docs/assets/workspace-desktop.png`, 1440 x 1000.
- Browser mobile queue screenshot: `docs/assets/workspace-mobile.png`, 390 x 844.
- Browser mobile decision screenshot: `docs/assets/workspace-mobile-detail.png`, 390 x 844.
- Runtime artifact: `docs/evidence/workspace-runtime-qa.json`.
- Lighthouse artifacts: `docs/evidence/workspace-lighthouse-accessibility-desktop.json` and `docs/evidence/workspace-lighthouse-accessibility-mobile.json`.
- Reproducible frontend gate: `npm ci && npm run qa:frontend`.
- Data classification: synthetic fixture only.
- Mutation scope: local files only.

## Claim boundary

Lighthouse and browser interaction proof do not equal a manual screen-reader certification. Cross-browser and assisted-technology testing remain production gates if this standalone prototype becomes a served application.
