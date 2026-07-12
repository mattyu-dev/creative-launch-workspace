# Trust Architecture v1

Date: 2026-07-05
Owner: Security / Secrets Officer
Status: local/offline trust design

## Threat Model

The product prepares high-volume ad launch plans. The biggest risks are wrong external action, wrong account or client mapping, private creative exposure, secret leakage, silent data corruption, and overconfident readiness claims.

## Assets

- Creative manifest rows.
- Asset paths and hashes.
- Destination URLs and tracking fields.
- Review decisions and approval records.
- Dry-run launch plans.
- Future account mappings and credentials.

## Trust Boundaries

- Current boundary: synthetic fixture data only.
- Local workspace boundary: local files and local app state.
- Future external boundary: any external account, credential, private creative, or spend-related path requires HITL plus Platform and Security review.
- Execution gate boundary: `docs/security/customer_data_trust_gates.md` is the hard matrix for customer data, credentials, sandbox/read-only access, media upload, validate-only execution, live mutation, and production rollout.

## Data Classification

| Class | Examples | Current Handling |
| --- | --- | --- |
| Synthetic | fake fixture rows, `example.invalid` URLs | Allowed in repo and vault |
| Internal design | PRDs, RFCs, gate docs | Allowed in repo |
| Customer private | real creative, real campaign names, real account data | Not allowed without HITL |
| Secret | tokens, app credentials, private keys | Not allowed in repo or vault |

## Security Requirements

- Fail closed on unknown source, unsupported format, or suspicious live-looking identifiers.
- Never store credentials in vault notes, fixtures, generated artifacts, or logs.
- Redact private data before evidence is stored.
- Require two-key Platform plus Security review for any external integration.
- Keep dry-run and mutation-capable code paths separate by design.
- Make readiness claims match evidence tier.
- Enforce the customer-data trust gate before any real data, credential, sandbox, upload, validate-only, live-mutation, or production rollout work.

## Permission Model

Initial local roles:

- Media Buyer: review launch candidates and mapping issues.
- Creative Ops Manager: fix asset, name, variant, and approval blockers.
- Account Manager: review client-facing packet.
- Approver: mark rows approved.
- Admin: configure local workspace settings.

Future role permissions must be enforced in app logic before any private data or external integration.

## Audit Event Schema

Minimum audit event fields:

- event_id
- timestamp
- actor_role
- batch_id
- source_manifest_sha256
- row_id
- action
- before_state
- after_state
- evidence_tier
- artifact_path

## Retention Policy

Synthetic data may stay in repo fixtures. Customer private data requires a separate retention decision before ingestion.

Default future policy should be Meta-native asset handoff:

- original customer creative bytes are streamed or held only in a short approved transient cache;
- successful uploads are stored in the customer's Meta Business creative folder or ad-account media assets;
- Meta Importer keeps only metadata lineage, source checksums, Meta asset identifiers, mapping state, and audit events;
- failed uploads require a G4-approved retry TTL and deletion path;
- vault persistence remains redacted-only.

The required retention, deletion, storage-location, and redaction proof lives in `docs/security/customer_data_trust_gates.md`.

## Blockers Before External Integration

- Threat model reviewed.
- Data retention decision approved.
- Credential storage design approved.
- Permission model implemented.
- Audit event schema implemented.
- Platform contract mapping reviewed.
- Customer-data trust gate approval artifact recorded for the target tier.
- Endpoint, data, secret, retention, audit, rollback, and reviewer scope recorded.
- HITL approval recorded.
