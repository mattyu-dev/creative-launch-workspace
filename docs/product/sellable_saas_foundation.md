# Sellable SaaS Foundation Slice

Date: 2026-07-05

## Goal

Turn the offline importer from an artifact generator into the first SaaS-shaped workspace agencies could plausibly rehearse: batch review, role-owned fixes, row decisions, local persistence, audit seed, and explicit export state.

This is still not a sellable production SaaS. It is a local, synthetic-only foundation that proves the workflow shape without customer data, credentials, live Meta account IDs, or Marketing API mutation.

## What Shipped

- `workspace_review_state.v1` state contract with deterministic batch ID, row review statuses, role ownership, audit seed, guardrails, and export policy.
- `local_batch_store.v1` backend slice now persists source snapshot, launch plan, review state, asset validation report, and append-only audit log.
- `workspace_html_static_audit.v1` now checks required workspace panels, labelled controls, keyboard hooks, local persistence hooks, responsive CSS, and absence of external network-call tokens.
- `meta_platform_payload_preview.v1` now creates blocked, validate-only, Meta-shaped draft payload previews without API calls.
- `docs/platform/meta_native_asset_handoff.md` now defines the target storage posture: upload originals into the customer's Meta Business creative folder or ad-account media assets, retain only metadata lineage, and keep real upload blocked until G1-G4 proof.
- `docs/security/customer_data_trust_gates.md` now blocks customer data, credentials/OAuth, sandbox/read-only calls, media uploads, validate-only execution, live mutation, and production rollout until gate-specific approval artifacts exist.
- CLI `--state` output that writes `review_state.json` beside the dry-run plan, Markdown packet, and HTML workspace.
- Static app workbench with:
  - batch filters, search, and owner filter
  - selectable row detail
  - creative copy/headline/final URL preview
  - issue and proposed-fix panel
  - reviewer role and note capture
  - Ready, Needs Fix, and Blocked decisions
  - browser persistence through `localStorage`
  - state download/copy/reset controls
- Unit coverage for the new review-state contract and CLI state export.

## Why This Matters

The earlier prototype answered "what would launch?" and "what is blocked?".

This slice starts answering the agency SaaS questions:

- Can an operator resume a batch without losing decisions?
- Can each fix be owned by the right role?
- Can clean rows, warning rows, and blocked rows stay in one reviewable workspace?
- Can the product export an auditable state package without touching Meta?
- Can this become a backend contract later instead of a one-off HTML table?

## Current Boundary

- Evidence tier: fixture test proof.
- Data: synthetic fixture only by default.
- Mutation scope: local files and browser local state only.
- Meta compatibility: not claimed.
- Customer readiness: not claimed.
- Sellability: not yet claimed.

## Shipped Sellable-SaaS Foundation Gates

- Backend persistence store with versioned batches and append-only synthetic audit events.
- Real-ish synthetic asset metadata validation.
- Static HTML audit plus headless Chrome/CDP smoke.
- Reusable browser-behavior QA script in CI, empty/error states, export confirmation, edge fixture, and golden artifact check.
- Official Meta Marketing API contract mapping from current primary sources.
- Non-executable Meta-shaped payload preview.
- Customer-data, credential, OAuth, sandbox, upload, validate-only, live-mutation, and production rollout gate design.

## Remaining Sellable-SaaS Gates

- Production database choice, row-level app-to-backend sync, migrations, and tenant/account isolation.
- Real synthetic file validation with bytes, MIME, dimensions, duration, size, hashes, and richer malformed fixture coverage.
- Real axe/screen-reader accessibility proof and browser-runtime save/resume coverage beyond the no-dependency browser QA proxy.
- HITL-approved sandbox/read-only proof, upload proof, validate-only proof, and live-mutation approval artifacts.
- Three agency rehearsals with time-saved, willingness-to-pay, and buyer-role evidence.

## Rehearsal Command

```bash
python3 -m meta_importer.cli plan fixtures/fake_agency_creatives/manifest_v2.csv --out runs/fake_agency_creatives_v2/launch_plan.json --review runs/fake_agency_creatives_v2/review_packet.md --html runs/fake_agency_creatives_v2/workspace.html --html-audit runs/fake_agency_creatives_v2/workspace_audit.json --state runs/fake_agency_creatives_v2/review_state.json --platform-preview runs/fake_agency_creatives_v2/platform_preview.json --store-dir runs/fake_agency_creatives_v2/store --asset-metadata fixtures/fake_agency_creatives/asset_metadata.csv
```
