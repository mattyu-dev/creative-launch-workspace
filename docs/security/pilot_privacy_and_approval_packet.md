# Pilot Privacy And Approval Packet

Date: 2026-07-06
Owner: Security / Secrets Officer
Status: started approval packet template

## Purpose

This packet prevents selling pressure from quietly crossing the trust gates. It is a template for future pilots only. It does not approve customer data, credentials, sandbox calls, uploads, validate-only execution, live mutation, or production rollout.

## Current Default

Allowed:

- synthetic fixtures;
- local dry-run artifacts;
- browser-local review state;
- local batch store;
- non-executable platform payload preview;
- redacted, non-sensitive customer feedback notes.

Blocked until approval:

- real manifests;
- real creative files or private copy;
- customer URLs, account IDs, pixel IDs, audiences, page IDs, or post IDs;
- OAuth tokens, app secrets, system-user tokens, refresh tokens, or private keys;
- sandbox/read-only calls;
- uploads to Meta business creative folders, ad-account `adimages`, or `advideos`;
- validate-only write requests;
- live mutations or spend changes.

## Approval Artifact Template

```yaml
gate_id:
requested_capability:
operator_approver:
date:
customer_or_account_scope:
data_classification:
storage_location:
retention_period:
deletion_path:
redaction_plan:
credential_surface:
allowed_endpoints_or_file_operations:
expected_outputs:
blocked_outputs:
audit_log_location:
rollback_or_deletion_path:
reviewers:
signoff_result:
expiry_or_revisit_date:
```

## Pilot Data Rules

- Prefer synthetic data.
- If the customer wants realism, request a redacted sample first.
- Do not put private customer evidence in the vault.
- Do not store customer data in `fixtures/`.
- Do not store secrets in repo files, generated artifacts, localStorage, tests, logs, or notes.
- For future real uploads, default to zero-retention asset handoff: upload into the customer's approved Meta creative folder or ad-account media assets, retain only metadata lineage, and delete originals after successful upload.
- Capture customer feedback as summarized, redacted findings.

## Required Reviews

| Gate | Required review |
| --- | --- |
| G1 customer data | Security, Product, Customer Success |
| G2 credentials/OAuth | Security, Platform |
| G3 sandbox/read-only | Platform, Security |
| G4 media upload | Security, Platform, Creative Ops |
| G5 validate-only execution | Platform, QA, Security |
| G6 live mutation | Director, Platform, Security |
| G7 production rollout | Director, Security, GTM, SRE |

## Ready-To-Use Statement

"The current rehearsal uses synthetic data only. We are not importing your private creative files, account IDs, credentials, or live Meta data. The production design is to hand assets off into your approved Meta creative folder or ad-account media assets and retain only lineage metadata, but any move beyond synthetic data requires a separate written approval artifact."
