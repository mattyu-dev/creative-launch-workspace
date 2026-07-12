# Start Selling Readiness Plan

Date: 2026-07-06
Owner: Director / GM
Status: active launch-readiness plan

## Verdict

Meta Importer's goal is to become the best SaaS for agencies and companies managing high creative volume: import creative batches, map each creative to the right campaign and ad set, catch launch-readiness issues, preserve lineage, and make the operator's life easier before and during Meta launch.

The storage posture should be Meta-native, not Meta Importer as a creative warehouse: after approval, assets should be uploaded into the customer's Meta Business creative folders or ad-account media assets, while Meta Importer keeps only metadata lineage, mappings, statuses, and audit events.

The current implementation is not ready to sell as production SaaS, customer-data workflow, or live Meta publisher.

It is ready to start selling only as the first low-risk commercial motion on the way there: paid workflow discovery or a synthetic rehearsal using the offline launch workspace. That lets agencies react to the real workflow, proves whether the mapping/import/QA path saves time, and keeps the project from quietly crossing customer-data or platform gates before the SaaS foundation is ready.

Current allowed tier is still G0 synthetic/offline. Customer data, credentials/OAuth, sandbox/read-only calls, media uploads, validate-only execution, live mutation, spend changes, and production rollout remain blocked until the relevant approval artifacts exist.

## What Exists Now

- Synthetic 100-row fixture and v2 mapping ledger.
- Offline launch plan with ready, needs-review, and blocked rows.
- Static review workspace with filters, row detail, preview, local reviewer notes, decisions, and state export.
- Static review workspace with filters, row detail, preview, local reviewer notes, decisions, visible-row bulk actions, guarded state import, review progress, and state export.
- Local batch store with source snapshot, review state, synthetic asset/file-byte validation, SQLite proof persistence, and append-only synthetic audit events.
- Static HTML audit, browser-behavior QA proxy, edge fixture, golden summary, bulk workflow checks, and strict manifest diagnostics.
- Current public market and competitor scan in `docs/research/market_and_competitor_scan_2026-07-06.md`.
- Official-source Meta Marketing API mapping and non-executable blocked payload preview.
- Meta-native asset handoff design in `docs/platform/meta_native_asset_handoff.md`: preferred Business Creative Asset Management folders, fallback ad-account media assets, and zero-retention original-file posture after upload proof.
- G0-G7 customer-data trust gate matrix.

## What Can Be Sold First

The first offer should be a paid workflow rehearsal around the SaaS workflow, not production software access yet:

1. Use only synthetic or explicitly redacted sample data.
2. Walk through the generated workspace and review packet with an agency operator.
3. Measure current batch prep process, time spent, error sources, buyer role, and budget owner.
4. Capture whether safe export without direct publishing is valuable.
5. Leave with a written findings memo and a recommended pilot path.

This can be positioned as:

> "We help paid social teams import high-volume Meta creative batches, map every creative to the right campaign and ad set, catch launch blockers, and keep the launch handoff clean."

## Full Missing Plan

| Track | Missing before paid product sale | Safe local start now | Blocked by |
| --- | --- | --- | --- |
| Positioning and ICP | direct agency proof, buyer role, willingness-to-pay range, budget source | current web/competitor scan plus `docs/gtm/pilot_offer_and_sales_motion.md` | external agency conversations |
| Demo product | timed demo script, operator first-run proof, app workflow beyond static HTML, preview-quality inspection | generated workspace with bulk workflow, state import/export, and review progress | agency rehearsal feedback |
| Pilot offer | pilot scope, success metric, LOI/payment signal, acceptance criteria | pilot package and price hypotheses | buyer conversation |
| Trust/legal/privacy | G1 customer-data approval, retention/deletion, redaction, DPA/privacy posture, tenant isolation model | privacy and approval packet | HITL plus legal/security review |
| Meta platform | credential design, sandbox/read-only proof, upload proof, validate-only proof, access-tier path | platform readiness doc | HITL plus Meta app/account setup |
| Asset storage posture | proof that originals can be uploaded into Meta-owned creative folders/media assets and deleted from our side | zero-retention handoff design doc plus blocked payload preview | G1/G2/G3/G4 approval and sandbox/test account proof |
| Production engineering | production auth, production tenant isolation, row-level sync from browser to backend, observability | SQLite proof store, local store, readiness checker | production deployment decision |
| QA/accessibility | axe or screen-reader proof, runtime save/resume, manifest fuzzing | current QA gates plus synthetic file-byte fixtures | runtime/tooling choice |
| Onboarding/support | pilot checklist, support path, deletion/incident runbook, weekly feedback cadence | onboarding runbook | first pilot schedule |

## Sellability Gates

### Gate S0: Synthetic Rehearsal Offer

Status: start now.

Required proof:

- demo script;
- synthetic fixture and workspace generated;
- interview capture sheet;
- no customer data or credentials;
- report template;
- clear "does not publish to Meta" statement.

### Gate S1: Paid Pilot Candidate

Status: external proof needed.

Unlock proof:

- three agency rehearsals completed;
- at least two operators confirm material time or QA value;
- buyer role and budget source identified;
- safe-export value confirmed or rejected;
- pilot success metric documented.

### Gate S2: Customer-Data Pilot

Status: HITL blocked.

Unlock proof:

- G1 approval artifact;
- data classification;
- retention/deletion decision;
- redaction plan;
- customer approval;
- storage and access model.

### Gate S3: Platform Proof

Status: HITL blocked.

Unlock proof:

- G2 credential/OAuth design;
- G3 sandbox/read-only scope;
- Business Creative Asset Management or ad-account media upload destination proof;
- redacted response evidence;
- endpoint allowlist;
- rate-limit and error taxonomy.

### Gate S4: Production SaaS

Status: blocked.

Unlock proof:

- production persistence and tenant isolation;
- auth and permission model;
- support and incident runbook;
- pricing proof;
- trust/privacy posture;
- production rollout approval.

## Started This Pass

- Added `start_selling_readiness.v1`, a local readiness report contract.
- Added CLI `python3 -m meta_importer.cli sales-readiness`.
- Added pilot offer and sales motion packet.
- Added onboarding and support runbook.
- Added privacy and approval packet.
- Added Meta sandbox/app review readiness packet.
- Added tests so the selling plan remains offline and gate-aware.
- Added current public market/competitor scan.
- Added operator-visible bulk review actions, guarded state import, and review progress.
- Added deterministic synthetic file-byte fixtures and validation.
- Added SQLite persistence proof with synthetic tenant guardrails, migrations, row decisions, and audit events.

## Director Disposition

Start selling conversations now only as the first gate toward the agency SaaS: workflow discovery or synthetic rehearsals around high-volume creative import, campaign/ad set mapping, QA, approval, lineage, and export. Do not sell production access, direct Meta publishing, customer-data processing, credential handling, or live account automation until the corresponding gate evidence exists.
