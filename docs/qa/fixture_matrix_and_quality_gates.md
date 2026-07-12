# Fixture Matrix And Quality Gates

Date: 2026-07-05
Owner: QA / Evidence Lead
Status: active local/offline QA plan

## Fixture Matrix

| Fixture | Purpose | Required Result |
| --- | --- | --- |
| `manifest.csv` | v1 baseline workflow | 100 rows, 30 ready, 10 needs-review, 60 blocked |
| `manifest_v2.csv` | mapping-ledger workflow | v1 counts plus account, placement, UTM, source, post, approval, and idempotency blocks |
| `workspace_audit.json` | static workspace accessibility and workflow audit | required panels, labelled controls, keyboard hooks, persistence hooks, responsive CSS, and no external network-call tokens pass |
| `platform_preview.json` | non-executable Meta-shaped payload preview | 100 draft payloads, all blocked, validate-only, no real account id |
| `runs/browser_qa/workspace_v2_mobile_cdp.png` | headless Chrome mobile render smoke | 390px viewport has no horizontal overflow and visible first-screen panels |
| `runs/browser_qa/workspace_v2_cdp_interaction.json` | headless Chrome interaction smoke | filter, keyboard row selection, decision persistence, and local audit storage work |
| `manifest_edge_cases.csv` | malformed and edge-case synthetic workflow | unsupported mappings, idempotency collisions, lineage gaps, and reviewer timestamp gaps are explicit |
| `golden_edge_summary.json` | golden artifact comparison | edge fixture summary cannot drift without an intentional golden update |
| `runs/browser_qa/workspace_v2_browser_qa.json` | reusable browser-behavior QA | filter/search/owner/keyboard/export/empty/error/accessibility-proxy contract passes |
| manifest header guard | schema diagnostics | missing required columns and unknown columns fail before row-level planning |

## Quality Gates

Current gates:

```bash
python3 scripts/enrich_fixture_v2.py
python3 -m unittest discover -s tests -q
python3 -m py_compile meta_importer/*.py scripts/*.py
python3 -m meta_importer.cli plan fixtures/fake_agency_creatives/manifest.csv --out runs/fake_agency_creatives/launch_plan.json --review runs/fake_agency_creatives/review_packet.md --html runs/fake_agency_creatives/workspace.html --html-audit runs/fake_agency_creatives/workspace_audit.json --state runs/fake_agency_creatives/review_state.json --platform-preview runs/fake_agency_creatives/platform_preview.json --store-dir runs/fake_agency_creatives/store
python3 -m meta_importer.cli plan fixtures/fake_agency_creatives/manifest_v2.csv --out runs/fake_agency_creatives_v2/launch_plan.json --review runs/fake_agency_creatives_v2/review_packet.md --html runs/fake_agency_creatives_v2/workspace.html --html-audit runs/fake_agency_creatives_v2/workspace_audit.json --state runs/fake_agency_creatives_v2/review_state.json --platform-preview runs/fake_agency_creatives_v2/platform_preview.json --store-dir runs/fake_agency_creatives_v2/store --asset-metadata fixtures/fake_agency_creatives/asset_metadata.csv
python3 scripts/workspace_browser_qa.py runs/fake_agency_creatives_v2/workspace.html --out runs/browser_qa/workspace_v2_browser_qa.json
python3 scripts/check_golden_artifacts.py
npm ci
QA_ASSETS_DIR=/tmp/creative-launch-workspace/assets QA_EVIDENCE_DIR=/tmp/creative-launch-workspace/evidence npm run qa:frontend
git diff --check
```

## Browser/UI QA

Static HTML must show:

- Batch summary counts.
- Owner queue.
- Issue mix.
- Row table.
- Mapping columns for v2.
- Filters for all, ready, needs-review, and blocked.
- Static audit contract `workspace_html_static_audit.v1` with required accessibility/workflow checks passing.
- Headless Chrome desktop/mobile screenshots.
- CDP smoke for horizontal overflow, blocked filter, keyboard row selection, decision persistence, and local audit storage.

Current local browser QA now includes:

- Reusable browser-behavior QA script in CI.
- Empty states.
- Error states.
- Export confirmation.

Future app must add:

- Save/resume proof in a browser automation runtime.
- Real axe or screen-reader pass before claiming full accessibility readiness.

## Evidence Rules

- Every readiness claim maps to an evidence artifact.
- Fixture proof does not imply platform proof.
- Static HTML proof does not imply app usability proof.
- Static audit proof does not imply real browser or screen-reader proof.
- Headless Chrome smoke does not imply full cross-browser, screen-reader, or manual agency usability proof.
- The reusable browser QA script is an accessibility proxy and does not imply a real axe or screen-reader pass.
- App usability proof does not imply customer willingness to pay.
- Customer rehearsal proof does not imply external integration safety.
