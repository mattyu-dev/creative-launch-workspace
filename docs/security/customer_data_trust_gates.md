# Customer Data Trust Gates

Date: 2026-07-05
Owner: Security / Secrets Officer
Status: enforced local/offline gate design

This document turns the trust boundary into an execution contract. Meta Importer may keep building local, synthetic, offline workflow proof. It must not ingest customer data, handle credentials, call sandbox APIs, upload media, run validate-only writes, or mutate live Meta objects until the matching gate is unlocked with explicit evidence.

## Current Allowed Tier

Only Gate G0 is currently allowed.

- Allowed: synthetic fixtures, offline launch plans, local review state, local batch store, static/browser QA, official-source contract mapping, and non-executable payload previews.
- Blocked: real agency manifests, real creative files, real account IDs, OAuth tokens, sandbox calls, upload calls, validate-only write calls, previews fetched from Meta, live campaign/ad/ad set/ad creative mutations, spend changes, and production tenant deployment.
- Current evidence tier: `fixture_test_proof`.
- Current mutation scope: none.

## Gate Matrix

| Gate | Scope | Current Status | Unlock Proof | Required Review |
| --- | --- | --- | --- | --- |
| G0 synthetic offline | Fake fixtures, local artifacts, dry-run review, payload preview | Allowed now | Tests, generated artifacts, `mutation_allowed: false`, no network calls | Product, QA |
| G1 customer data import | Real manifests, real creative names, customer URLs, customer campaign data | Blocked | Data classification, retention/deletion decision, redaction plan, storage location, access model, customer approval artifact | Security, Product, Customer Success |
| G2 credential and OAuth | Access tokens, app credentials, OAuth setup, scopes, refresh/rotation | Blocked | Secret storage design, scope inventory, rotation/revocation runbook, no-secret logging test, redaction proof | Security, Platform |
| G3 sandbox/read-only account access | Account lookup, page/IG identity lookup, read-only API calls | Blocked | Operator-approved account scope, endpoint allowlist, expected responses, rate-limit plan, redaction plan, sandbox audit log | Platform, Security |
| G4 media upload | Business creative folders, `images`, `videos`, `adimages`, `advideos`, creative file transfer, upload response lineage | Blocked | Asset retention policy, malware/file validation plan, hash lineage, upload-response storage design, deletion path | Security, Platform, Creative Ops |
| G5 validate-only execution | Validate-only create requests or preview calls against Meta | Blocked | Payload diff review, idempotency ledger, error taxonomy, retry policy, sandbox response capture, no-spend guarantee | Platform, QA, Security |
| G6 live mutation | Campaign, ad set, ad creative, ad creation, status changes, budget/spend changes | Blocked | Two-key Platform/Security signoff, explicit operator approval, dry-run diff, rollback/pause path, spend guard, post-run audit | Director, Platform, Security |
| G7 production/customer rollout | Multi-client SaaS use, tenant data, support workflows | Blocked | Tenant isolation, production DB decision, DPA/privacy posture, support runbook, incident response, pricing/pilot proof | Director, Security, GTM, SRE |

## Required Approval Artifact

Any move from one gate to the next requires a durable approval artifact. The artifact must include:

- gate_id and requested capability
- operator approver and date
- customer or account scope
- data classification and retention decision
- credential and secret-surface statement
- allowed endpoints or file operations
- expected outputs and blocked outputs
- audit log location
- rollback or deletion path
- reviewers and signoff result
- expiry or revisit date

Approvals cannot be implied by code changes, CLI flags, docs, or a passing fixture test.

## Customer Data Rules

- Real customer data is blocked until G1 is approved.
- Real customer evidence must stay out of the vault unless redacted and explicitly approved.
- Customer manifests must use a storage location outside repo fixtures unless Security approves a sanitized fixture.
- Generated evidence must redact customer names, URLs, account IDs, audience names, and private creative copy by default.
- Delete/export behavior must be defined before import.

## Credential And OAuth Rules

- Tokens, app secrets, refresh tokens, private keys, and OAuth callback secrets must never be stored in the repo, vault, generated artifacts, browser localStorage, test fixtures, or logs.
- OAuth work is blocked until G2 defines scope, storage, rotation, revocation, and redaction.
- Any code path that can make authenticated Meta calls must require an explicit non-default execution mode and a gate-approved credential provider.
- Logs must prove secret redaction before any credential is introduced.

## Sandbox And Validate-Only Rules

- Sandbox/read-only work is blocked until G3 is approved.
- Validate-only write or preview work is blocked until G5 is approved.
- The allowlist must name exact object families and endpoint types before execution.
- Response artifacts must be redacted before entering the repo or vault.
- A local payload preview is not sandbox proof.

## Media Upload And Asset Retention Rules

- Uploads are blocked until G4 is approved.
- The target product posture is zero-retention asset handoff: originals are streamed or temporarily cached only long enough to validate and upload into Meta, then deleted after a successful response.
- The project must know whether failed or retrying uploads are retained locally, deleted immediately, or stored with customer approval.
- Upload response IDs, hashes, and file lineage must be tied to the local audit ledger.
- Business Creative Asset Management folders are the preferred customer-visible destination when access is approved; ad-account `adimages` and `advideos` remain the fallback upload path.
- A customer-facing "we do not keep your creative files" claim requires deletion receipt design, retry TTL, and upload-response lineage proof.
- Unsupported formats and suspicious media metadata must fail closed.

## Live Mutation Rules

- Live mutation is blocked until G6 is approved.
- G6 requires explicit operator approval for the target account, date, budget/spend boundary, mutation type, and rollback path.
- The default product mode must remain dry-run or validate-only until a gate-approved execution mode is selected.
- Every mutation-capable path must emit an audit event before and after execution.
- Budget or spend changes require Director, Platform, and Security approval even after G6.

## Evidence And Audit Requirements

- Every gate transition must produce an evidence note or approval artifact with reviewer names and validation commands.
- The append-only audit log must record actor, source manifest hash, row id, action, before/after state, evidence tier, and artifact path.
- Evidence must state what it does not prove.
- Fixture success cannot be used as customer-data, sandbox, or live-mutation proof.

## Current Product Disposition

Meta Importer is an offline import candidate only. The next safe work may improve local UX, local persistence, static/browser QA, docs, synthetic fixtures, or non-executable platform mapping. Customer data, credentials, sandbox execution, uploads, validate-only execution, and live mutation remain blocked by this gate matrix.
