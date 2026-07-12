# Fake Agency Creative Fixture

Synthetic fixture for the first Meta Importer product baseline.

Contents:

- `manifest.csv`: 100 fake creative rows across 3 campaigns and 10 ad sets.
- `manifest_v2.csv`: generated 100-row mapping-ledger fixture with account aliases, placements, UTMs, post decisions, source lineage, and approval records.
- `asset_metadata.csv`: generated synthetic asset metadata for format, media kind, MIME signature, dimensions, duration, file size, checksum, and hash validation.
- `manifest_edge_cases.csv`: 10-row synthetic edge fixture for parser, mapping, idempotency, and review-state regressions.
- `golden_edge_summary.json`: locked expected summary for the edge fixture.
- `assets/`: deterministic synthetic image/video-like bytes used for file-byte validation. These are not real customer assets.

The fixture intentionally includes:

- clean approved creatives;
- pending approvals;
- rejected creatives;
- naming errors;
- missing approvals;
- duplicate asset references;
- destination mismatches;
- unsupported format examples.

No real customer names, real ad account IDs, production URLs, or real assets are included. All destinations use `example.invalid`.

## Rehearsal Command

```bash
python3 -m meta_importer.cli plan fixtures/fake_agency_creatives/manifest.csv --out runs/fake_agency_creatives/launch_plan.json --review runs/fake_agency_creatives/review_packet.md --html runs/fake_agency_creatives/workspace.html --html-audit runs/fake_agency_creatives/workspace_audit.json --state runs/fake_agency_creatives/review_state.json --platform-preview runs/fake_agency_creatives/platform_preview.json --store-dir runs/fake_agency_creatives/store
```

Expected dry-run result:

- 100 rows loaded.
- 30 launch-ready rows.
- 10 needs-review rows.
- 60 blocked rows.
- 70 total fixture issues assigned to agency owners.

## V2 Mapping Ledger

Generate and rehearse the enriched mapping fixture:

```bash
python3 scripts/enrich_fixture_v2.py
python3 scripts/materialize_synthetic_assets.py
python3 -m meta_importer.cli plan fixtures/fake_agency_creatives/manifest_v2.csv --out runs/fake_agency_creatives_v2/launch_plan.json --review runs/fake_agency_creatives_v2/review_packet.md --html runs/fake_agency_creatives_v2/workspace.html --html-audit runs/fake_agency_creatives_v2/workspace_audit.json --state runs/fake_agency_creatives_v2/review_state.json --platform-preview runs/fake_agency_creatives_v2/platform_preview.json --store-dir runs/fake_agency_creatives_v2/store --sqlite-db runs/fake_agency_creatives_v2/workspace.sqlite3 --asset-metadata fixtures/fake_agency_creatives/asset_metadata.csv
```

Expected v2 mapping coverage:

- 100 account aliases.
- 100 placement mappings.
- 100 UTM mappings.
- 100 source-lineage mappings.
- 100 post decisions.
- 10 existing post references.
- 100 asset metadata-backed validation rows with deterministic synthetic file-byte checksums and MIME signatures.
- Static workspace audit status `pass` for required panels, labelled controls, keyboard row selection hooks, browser persistence hooks, responsive CSS, and no external network-call tokens.
- 100 non-executable `meta_platform_payload_preview.v1` draft payloads with `execution_options: ["validate_only"]` and local account/media/page blocks.
- 10 intentionally blocked unsupported `collection` assets.

## Edge Fixture And Golden Artifact

```bash
python3 scripts/check_golden_artifacts.py
```

The edge fixture covers missing creative IDs, unsupported objectives, incompatible placement, partial UTM mapping, missing existing-post lineage, reviewer timestamp gaps, idempotency collision, duplicate asset detection, unsupported placement, and unsupported post ID type. It is synthetic-only and still cannot prove customer-data or live Meta safety.

## Issue Types

Allowed `qa_issue` values:

- empty string for a clean row;
- `naming_error`;
- `missing_approval`;
- `duplicate_asset`;
- `destination_mismatch`;
- `unsupported_format`.
