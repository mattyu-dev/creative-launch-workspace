# Browser Quality Gate

Date: 2026-07-06
Owner: QA / Evidence Lead
Status: active local/offline QA gate

## Contract

`workspace_browser_qa.v1` is a no-network, synthetic-only browser-behavior contract for the generated launch workspace. It complements `workspace_html_static_audit.v1` and the earlier headless Chrome/CDP smoke artifact by making the important interaction expectations reusable in tests and CI.

The gate checks:

- the static accessibility/workflow audit passes;
- batch filter counts match `launch_ready`, `needs_review`, and `blocked` summary counts;
- owner filtering can expose every issue owner;
- search can find a known creative id;
- Enter and Space row-selection hooks are present;
- empty-filter state is rendered;
- corrupt local browser state falls back safely with a visible status;
- download/copy/reset export controls preserve local-only state;
- bulk visible-row actions preserve filtered scope and local-only state;
- guarded review-state import rejects mismatched batches and mutation-capable payloads;
- visible review progress is present;
- a simulated row decision keeps `mutation_allowed: false`, keeps `meta_api_compatibility: not_claimed`, and appends local audit state;
- screen-reader proxy affordances exist through `aria-live`, `aria-pressed`, table caption, labelled controls, and empty state.

## Reusable Command

Generate the v2 workspace, then run the browser QA gate:

```bash
python3 scripts/materialize_synthetic_assets.py
python3 -m meta_importer.cli plan fixtures/fake_agency_creatives/manifest_v2.csv --out runs/fake_agency_creatives_v2/launch_plan.json --review runs/fake_agency_creatives_v2/review_packet.md --html runs/fake_agency_creatives_v2/workspace.html --html-audit runs/fake_agency_creatives_v2/workspace_audit.json --state runs/fake_agency_creatives_v2/review_state.json --platform-preview runs/fake_agency_creatives_v2/platform_preview.json --store-dir runs/fake_agency_creatives_v2/store --sqlite-db runs/fake_agency_creatives_v2/workspace.sqlite3 --asset-metadata fixtures/fake_agency_creatives/asset_metadata.csv
python3 scripts/workspace_browser_qa.py runs/fake_agency_creatives_v2/workspace.html --out runs/browser_qa/workspace_v2_browser_qa.json
```

CI runs this lane without external dependencies or network calls. It is not a live Meta, customer-data, or production browser compatibility claim.

## Edge Fixture And Golden Artifact

`fixtures/fake_agency_creatives/manifest_edge_cases.csv` contains 10 synthetic rows that stress the parser and QA contract with missing creative ids, unsupported objectives, format-placement mismatch, partial UTM mapping, missing existing post ids, reviewer timestamp gaps, idempotency collisions, unsupported placements, and unsupported post-id types.

`fixtures/fake_agency_creatives/golden_edge_summary.json` is the locked summary for that fixture. The gate is:

```bash
python3 scripts/check_golden_artifacts.py
```

## Accessibility Proxy

The gate is intentionally an accessibility proxy, not a claim that a screen reader or axe runtime has been run. It enforces structural affordances that reduce regressions before a fuller browser stack exists: labelled controls, table caption, `aria-live`, `aria-pressed`, empty state, keyboard row selection, and no external network-call tokens.

Before claiming full accessibility readiness, run a real browser/axe or screen-reader pass against the generated workspace or future app runtime.
