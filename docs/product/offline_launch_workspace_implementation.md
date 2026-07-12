# Offline Launch Workspace Implementation

Date: 2026-07-05

## Product Slice

The first implementation slice is an offline **Meta Creative Launch Workspace** for the synthetic 100-row agency fixture.

It is not a live Meta publisher. It does not load credentials, call Meta APIs, mutate ad accounts, import customer assets, change budgets, or claim Marketing API compatibility.

## What It Builds

- CSV manifest reader with a synthetic-data guardrail.
- Typed row, issue, ad candidate, and launch-plan objects.
- Deterministic idempotency key per proposed ad candidate.
- Role-owned fix queue for Approver, Creative Ops Manager, and Media Buyer.
- Dry-run export JSON with source row lineage and guardrail copy.
- Markdown review packet for agency review.
- Static HTML workspace with first-screen counts, owner queue, issue mix, searchable row table, owner filters, row detail, preview panel, issue panel, review decisions, browser persistence, and state export controls.
- Local `workspace_review_state.v1` JSON with deterministic batch ID, role-owned review statuses, audit seed, and offline export policy.
- Local `local_batch_store.v1` filesystem backend with source snapshot, persisted plan/state, asset validation report, and append-only audit events.
- Static `workspace_html_static_audit.v1` JSON covering required panels, labelled controls, keyboard hooks, browser persistence hooks, responsive CSS, and external-network-token absence.
- Non-executable `meta_platform_payload_preview.v1` JSON that maps launch candidates to Meta-shaped draft payload sequences without credentials or external calls.
- Unit tests for fixture counts, guardrails, dry-run payload shape, review copy, HTML controls, review-state export, and CLI state output.

## Fixture Rehearsal Result

Command:

```bash
python3 -m meta_importer.cli plan fixtures/fake_agency_creatives/manifest.csv --out runs/fake_agency_creatives/launch_plan.json --review runs/fake_agency_creatives/review_packet.md --html runs/fake_agency_creatives/workspace.html --html-audit runs/fake_agency_creatives/workspace_audit.json --state runs/fake_agency_creatives/review_state.json --platform-preview runs/fake_agency_creatives/platform_preview.json --store-dir runs/fake_agency_creatives/store
```

Result:

- 100 rows loaded.
- 30 launch-ready candidates.
- 10 needs-review rows.
- 60 blocked rows.
- 60 blockers.
- 10 warnings.
- Issue mix: 30 `missing_approval`, 10 `naming_error`, 10 `duplicate_asset`, 10 `destination_mismatch`, 10 `unsupported_format`.

## V2 Mapping Ledger

The follow-up slice is documented in [bulk_launch_mapping_ledger.md](bulk_launch_mapping_ledger.md). It adds an additive `offline_launch_plan.v2` contract, a generated `manifest_v2.csv`, mapping-ledger columns in the HTML workspace, and validators for account aliases, placements, UTMs, post lineage, source lineage, approval handoff, and idempotency collisions.

## Acceptance Criteria

- Agencies can answer: what can launch, what is blocked, who owns each fix, and what would be exported.
- The 30 clean rows remain launch candidates.
- Every fixture issue is assigned to the right owner.
- Operators can save and resume local row decisions in the browser.
- The review-state JSON can seed a later backend without granting Meta mutation power.
- The local batch store can persist a source snapshot and audit event trail without customer data.
- The static HTML audit can fail the build path if required accessibility/workflow hooks disappear.
- Headless Chrome/CDP smoke can verify desktop/mobile rendering, basic filter behavior, keyboard row selection, and local decision persistence on the generated workspace.
- The platform preview can show draft Campaign, Ad Set, media upload, Ad Creative, and Ad payloads while keeping every payload blocked and non-executable.
- Generated exports stay offline and dry-run only.
- Non-synthetic destinations or asset paths are blocked by default.
- Repeated runs produce deterministic row identities and review artifacts.

## Boundary

This implementation proves a local workflow rehearsal only. Live Meta publishing, OAuth, access-token handling, real ad-account IDs, real customer data, policy approval, delivery readiness, and spend safety require later Platform, Security, QA, and HITL gates.
