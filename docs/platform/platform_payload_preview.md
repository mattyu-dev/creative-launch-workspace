# Platform Payload Preview

Date: 2026-07-05
Owner: Meta Ads API / Platform Lead
Status: implemented offline contract preview

## Goal

Turn the official Meta API contract mapping into a local artifact agencies and platform reviewers can inspect without touching Meta.

The preview is intentionally non-executable. It does not resolve real accounts, load tokens, upload media, create creatives, create ads, or call validate-only endpoints. Every payload remains blocked until HITL, Platform, and Security gates approve a sandbox path.

## Contract

`meta_platform_payload_preview.v1` exports:

- `mutation_allowed: false`;
- `meta_api_compatibility: mapped_not_executed`;
- `asset_storage_policy` for Meta-native zero-retention handoff design;
- `execution_options: ["validate_only"]` on draft write steps;
- draft sequence for Campaign, Ad Set, Meta business-folder or ad-account media upload, Ad Creative, and Ad;
- blocked fields for unresolved account, Business ID, creative folder, Page/Instagram identity, upload response, non-launch-ready rows, existing post reuse, unsupported formats, and unmapped values;
- local-only status for idempotency and approval records.

## Rehearsal Command

```bash
python3 -m meta_importer.cli plan fixtures/fake_agency_creatives/manifest_v2.csv --out runs/fake_agency_creatives_v2/launch_plan.json --review runs/fake_agency_creatives_v2/review_packet.md --html runs/fake_agency_creatives_v2/workspace.html --html-audit runs/fake_agency_creatives_v2/workspace_audit.json --state runs/fake_agency_creatives_v2/review_state.json --platform-preview runs/fake_agency_creatives_v2/platform_preview.json --store-dir runs/fake_agency_creatives_v2/store --asset-metadata fixtures/fake_agency_creatives/asset_metadata.csv
```

## Current Result

- Rows: 100.
- Readiness: all payloads `draft_blocked`.
- No real `act_<AD_ACCOUNT_ID>` values.
- Asset storage policy is `meta_native_zero_retention_candidate`, with durable local storage limited to metadata lineage.
- Media steps prefer `/<BUSINESS_ID>/images` or `/<BUSINESS_ID>/videos` with `creative_folder_id`, falling back to `/act_<AD_ACCOUNT_ID>/adimages` or `/act_<AD_ACCOUNT_ID>/advideos`.
- Campaign objective mapping includes `traffic -> OUTCOME_TRAFFIC` and `sales -> OUTCOME_SALES`.
- Placement targeting is draft-only and marked as needing sandbox validation.
- Existing post reuse is blocked until ownership and compatibility are proven.

## Remaining Platform Gates

- Add a sandbox-approved validate-only lane.
- Verify Business Creative Asset Management folder creation, folder upload visibility, placement values, creative object story specs, existing-post reuse, and media upload behavior against a sandbox or approved test account.
- Prove transient original deletion and upload-response lineage before claiming customer zero-retention behavior.
- Add app/token/permission flow after Security approval.
- Add preview-result ingestion before any mutation-capable path.
