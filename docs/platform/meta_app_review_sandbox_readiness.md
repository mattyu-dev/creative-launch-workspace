# Meta App Review And Sandbox Readiness

Date: 2026-07-06
Owner: Meta Ads API / Platform Lead
Status: started platform-readiness packet, no credentialed proof

## Purpose

This packet records what must be ready before the project asks for Meta sandbox/read-only access, credential work, uploads, validate-only execution, or live mutation.

It does not authorize any Meta API call.

## Current Platform Truth

- The repo has official-source object and field mapping.
- The repo emits non-executable, blocked platform payload previews.
- The repo now models Meta-native asset handoff: Business Creative Asset Management folders are the preferred upload destination, with ad-account `adimages` and `advideos` as fallback media assets.
- No app id, app secret, OAuth token, system-user token, page token, sandbox token, or real account id is stored or used.
- No sandbox/read-only call has been made.
- No upload, validate-only write, or live mutation has been made.

## Current Meta Access Notes

Meta's May 4, 2026 developer update says the former "Ads Management Standard Access" feature is now "Marketing API Access Tier". It also says the upper tier threshold changed to 500+ Marketing API calls in the past 15 days and an error rate below 15% across the last 500 calls.

This matters for the product plan because the platform path is not just code. It requires app setup, permission/access-tier work, redacted evidence, rate-limit awareness, and a safe proof plan.

Primary source: [Meta developer update on Marketing API Access Tier](https://developers.meta.com/blog/updates-to-ads-management-standard-access-feature/)

## Required Before G3 Sandbox/Read-Only

- Operator-approved app and account scope.
- Permission inventory for `ads_read`, `ads_management`, `business_creative_management`, pages, Instagram identity, and any related access.
- Endpoint allowlist.
- Expected response shapes.
- Redaction rules.
- Rate-limit, retry, and timeout plan.
- Audit log location outside the vault if private data appears.
- No-secret logging proof.

## Required Before Upload Or Validate-Only

- G4 asset-retention and file-validation approval.
- Business Creative Asset Management folder creation/lookup proof, or an explicit fallback to ad-account media upload.
- Zero-retention proof for original files: transient cache TTL, deletion receipt, and upload-response lineage.
- G5 payload diff review.
- Idempotency ledger and retry policy.
- Error taxonomy.
- Sandbox or approved test account evidence.
- No-spend guarantee.
- Platform plus Security signoff.

## Required Before Live Mutation

- G6 approval artifact.
- Target account and object scope.
- Dry-run diff.
- Pause/rollback path.
- Spend and budget guard.
- Two-key Platform/Security approval.
- Director approval.

## Local Work Allowed Now

- Keep mapping official sources.
- Expand blocked payload preview.
- Add enum maps and unsupported-field taxonomy.
- Add mocked contract tests.
- Build redaction and no-secret logging tests without tokens.

## Hard Stop

If a task requires a real token, real account, real customer data, sandbox response, upload, validate-only request, or live mutation, stop and request HITL approval with the relevant gate artifact.
