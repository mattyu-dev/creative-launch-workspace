# Meta Native Asset Handoff

Date: 2026-07-06
Owner: Meta Ads API / Platform Lead
Status: designed offline, not executed

## Verdict

Yes: the product should be designed so customer creative files are handed off to Meta, not retained by Meta Importer.

The strongest product promise is:

> Meta Importer validates, maps, and uploads creative assets into the customer's Meta creative library or ad-account media assets, then keeps only the metadata needed for lineage, QA, and audit.

This is not enabled yet. The current repo still operates at G0 synthetic/offline only. Real customer files, credentials, sandbox/read-only calls, media uploads, validate-only execution, live mutation, spend changes, and production rollout remain blocked until the relevant gate artifacts are approved.

## Meta Destination Options

### Preferred: Business Creative Asset Management Folder

Use Meta Business Creative Asset Management when the customer and app have the right business scope.

Relevant official surfaces:

- Business creative folders: `/<BUSINESS_ID>/creative_folders`.
- Business image upload: `/<BUSINESS_ID>/images` with `creative_folder_id`.
- Business video upload: `/<BUSINESS_ID>/videos` with `creative_folder_id`.
- Permission surface identified by Meta docs: `business_creative_management`.

Why this is best:

- It matches the buyer language: creative folders, media library, reusable assets.
- It can organize images and videos for future Ads Manager or Marketing API use.
- It lets the customer see the imported assets inside Meta-owned surfaces.

### Fallback: Ad Account Media Asset Upload

Use ad-account assets when the workflow is closer to immediate campaign/ad creation.

Relevant official surfaces:

- Image upload: `/act_<AD_ACCOUNT_ID>/adimages`.
- Video upload: `/act_<AD_ACCOUNT_ID>/advideos`.
- Ad Creative reference: `image_hash` or `video_id` in `AdCreative`.

Why this still works:

- It is the standard Marketing API route for ad creation.
- It returns the platform lineage needed to create ad creatives.
- It avoids our app becoming the durable media store.

## Zero-Retention Pipeline

Target production behavior:

1. Customer selects a local folder, Drive folder, DAM export, or structured manifest.
2. Meta Importer computes local validation metadata: checksum, MIME, size, dimensions, duration, naming, destination URL, campaign key, and ad set key.
3. Meta Importer streams the file to the approved Meta destination.
4. Meta returns durable platform identifiers such as business image ID, media library URL, image hash, video ID, or creative folder ID.
5. Meta Importer writes only metadata lineage: source row, source checksum, file name, asset kind, target campaign/ad set mapping, Meta identifier, upload status, reviewer, and audit event.
6. Original bytes are deleted after successful upload. Failed uploads may keep a short, explicitly approved retry cache only if G4 defines the TTL and deletion path.

## Durable Data We Keep

- Source manifest hash.
- Source row id.
- Creative id or deterministic local idempotency key.
- Source checksum/hash.
- Asset metadata: kind, dimensions, duration, size, MIME, validation status.
- Meta platform identifiers: image hash, video id, business image/video id, creative folder id, media library URL when available.
- Mapping to campaign, ad set, placement, post/creative path, and review status.
- Audit events and redacted error taxonomy.

## Data We Should Not Keep By Default

- Original creative files after successful handoff.
- Customer ZIP files after extraction/upload.
- Private creative copy or account IDs in vault notes.
- OAuth tokens, app secrets, page tokens, system-user tokens, or refresh tokens.
- Raw API responses containing private customer/account data unless redacted and approved.

## Required Gates Before Real Use

| Gate | Requirement |
| --- | --- |
| G1 customer data | Customer approves the manifest/file scope, retention/deletion path, storage location, and redaction plan. |
| G2 credentials/OAuth | Token storage, scope inventory, rotation, revocation, and no-secret logging are approved. |
| G3 sandbox/read-only | Business, ad account, page, Instagram identity, and creative folder lookup are allowlisted. |
| G4 media upload | File validation, malware/suspicious metadata handling, transient cache TTL, deletion proof, and upload-response lineage are approved. |
| G5 validate-only | Draft payload diff, idempotency ledger, retry policy, and no-spend guarantee are proven. |
| G6 live mutation | Campaign/ad set/ad creative/ad creation requires explicit operator approval and rollback/pause path. |

## Product Copy Boundary

Allowed now:

> Designed for zero-retention creative handoff: assets can be routed into Meta creative folders or ad-account media assets after approval, while Meta Importer keeps only lineage and audit metadata.

Not allowed yet:

> We already import your real creative files directly into Meta and never store anything.

That claim requires G1-G4 proof at minimum, plus G2/G3 for any account-authenticated workflow.

## Open Proof

- Verify Business Creative Asset Management permissions and folder behavior in a sandbox or approved test business.
- Verify image/video upload response fields and media-library visibility.
- Verify whether folder uploads provide the same IDs/hashes needed for downstream Ad Creative creation or whether ad-account upload remains necessary for some formats.
- Define retry cache TTL, deletion receipt, and customer-facing audit export.
