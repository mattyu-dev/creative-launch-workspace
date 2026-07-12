# Local Batch Store Backend Slice

Date: 2026-07-05

## Goal

Promote the next safe backend gap after the local SaaS workbench: durable local persistence, append-only audit events, source snapshots, and synthetic asset validation.

This is still a local filesystem backend, not a production database or customer-data system. It does not call Meta, load credentials, mutate ad accounts, or store real agency assets.

## What Shipped

- `local_batch_store.v1` filesystem store under a deterministic batch ID.
- Source manifest snapshot at `snapshots/source_manifest.csv`.
- Persisted `launch_plan.json`, `review_state.json`, and `asset_validation.json`.
- Append-only audit log at `audit/events.jsonl`.
- `synthetic_asset_validation.v1` report backed by `fixtures/fake_agency_creatives/asset_metadata.csv`.
- Deterministic synthetic asset files under `fixtures/fake_agency_creatives/assets/`, materialized by `scripts/materialize_synthetic_assets.py`, so file-byte presence, checksum, size, and MIME-signature checks are exercised locally.
- `sqlite_workspace_store.v1` proof store with migrations, synthetic tenant IDs, persisted batch rows, row-level decisions, and local audit events.
- CLI `--store-dir` and `--asset-metadata` options.
- CLI rehearsals also emit `workspace_html_static_audit.v1` when `--html-audit` is provided, so backend and static UI evidence stay generated together.
- Headless Chrome/CDP smoke evidence now lives under `runs/browser_qa/` for desktop/mobile rendering and basic browser interaction proof.
- Tests proving:
  - metadata and file-byte validation route asset readiness issues;
  - missing metadata blocks rows;
  - missing asset bytes block supported rows;
  - the local store persists snapshots;
  - audit events append instead of being overwritten;
  - SQLite persists tenant-scoped batches and row-level decisions;
  - SQLite rejects non-fixture tenant IDs in the offline proof store;
  - CLI can write the store.

## Asset Validation Result

The v2 fixture now has 100 synthetic metadata-backed rows and 90 materialized unique asset files. The validation report is intentionally `blocked` because 10 fixture rows use unsupported `collection` format examples. That is the correct preflight outcome: the store records the issue instead of pretending those assets are launchable.

## Rehearsal Command

```bash
python3 scripts/enrich_fixture_v2.py
python3 scripts/materialize_synthetic_assets.py
python3 -m meta_importer.cli plan fixtures/fake_agency_creatives/manifest_v2.csv --out runs/fake_agency_creatives_v2/launch_plan.json --review runs/fake_agency_creatives_v2/review_packet.md --html runs/fake_agency_creatives_v2/workspace.html --html-audit runs/fake_agency_creatives_v2/workspace_audit.json --state runs/fake_agency_creatives_v2/review_state.json --platform-preview runs/fake_agency_creatives_v2/platform_preview.json --store-dir runs/fake_agency_creatives_v2/store --sqlite-db runs/fake_agency_creatives_v2/workspace.sqlite3 --asset-metadata fixtures/fake_agency_creatives/asset_metadata.csv
```

## Boundary

- Evidence tier: fixture test proof.
- Data: synthetic fixture only by default.
- Mutation scope: local files only.
- Meta compatibility: not claimed.
- Customer readiness: not claimed.

## Remaining Backend Gates

- Promote or reject SQLite as the local-first store after browser-runtime row sync is connected to the backend.
- Add signed export manifests and source snapshot versioning policy.
- Connect browser-imported review state into backend audit events.
- Add retry/recovery semantics for partial batch writes.
- Add retention/deletion policy before customer data import.
