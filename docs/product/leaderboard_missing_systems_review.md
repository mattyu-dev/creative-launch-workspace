# Leaderboard Missing Systems Review

Date: 2026-07-05

## Director Verdict

Meta Importer is a credible offline import candidate. It is not yet a customer-ready SaaS, production-grade workflow, or Meta-integrated publisher.

The current repo proves the Tier 0 spine:

- 100-row synthetic fixture.
- Offline manifest parsing.
- Owner-routed fix queues.
- Dry-run JSON, Markdown review, and static HTML workspace.
- `offline_launch_plan.v2` mapping ledger.
- `workspace_review_state.v1`, `local_batch_store.v1`, `sqlite_workspace_store.v1`, source snapshots, append-only synthetic audit events, and synthetic asset/file-byte validation.
- `workspace_html_static_audit.v1`, generated audit artifacts, headless Chrome/CDP smoke evidence, `workspace_browser_qa.v1`, edge fixture, and golden summary check.
- Official Meta Marketing API contract mapping plus non-executable `meta_platform_payload_preview.v1` drafts.
- Enforced G0-G7 customer-data trust gate matrix.
- Guardrails that avoid live Meta mutation, credentials, spend, and customer data.

The missing work is not mysterious. It clusters into six systems:

1. Operator-usable product app.
2. Production backend import/persistence/audit pipeline.
3. Real asset and expanded QA validation matrix.
4. Meta sandbox/read-only, upload, validate-only, and live-mutation proof.
5. Approved trust unlocks for customer data, credentials, sandbox, upload, validate-only, live mutation, and production rollout.
6. Customer discovery, pricing, pilot, onboarding, and kill/pivot proof.

## Leaderboard Review

| Reviewer | Lane | Verdict |
| --- | --- | --- |
| Laplace | Backend / Data Pipeline | Solid offline fixture proof, now with local batch persistence and audit events; still missing production database choice, row-level app sync, real file validation, adapter execution, and typed import operations. |
| Dewey | Frontend / Product UX | Static workspace is now more useful with local review state and QA smoke, but the next product frontier is still an operator-usable local app. |
| Boole | Platform / Security / SRE | Safe to continue local/offline work. Not safe for customer data, OAuth, sandbox account access, production deploy, or live mutation. |
| Peirce | Customer Discovery / QA / GTM | Worth pursuing, but not sellable until agency rehearsals, willingness-to-pay, buyer proof, onboarding, and kill/pivot gates land. |

## P0 Missing Systems

### Product / Frontend

| Missing system | Current evidence | Disposition |
| --- | --- | --- |
| Real app shell: batch list, row detail, fix queue, preview pane, export panel | Current generated workspace has first-screen metrics, filters, row detail, preview, export, bulk decisions, and guarded state import. | Partially implemented AFK local |
| Interactive row workflow: inspect row, edit fix, confirm duplicate reuse, bulk apply, revalidate | Current HTML has row detail, reviewer notes, single-row decisions, visible-row bulk decisions, and state export/import. | Partially implemented AFK local; revalidate loop remains open |
| Persistent review state and resume | Local browser state, JSON export/import, filesystem store, and SQLite proof store exist. | Partially implemented AFK local; browser-to-backend sync remains open |
| Approval workflow: comments, approve/reject transitions, reviewer history, account-manager/client handoff gate | Approval roles exist in docs and fixture fields, not app behavior. | AFK local until private data |
| Creative preview and diff | Fixture README says asset files are intentionally absent. | AFK with synthetic assets |
| Accessibility and responsive workflow | Static audit and reusable browser QA now cover keyboard hooks, labelled controls, empty/error states, export confirmation, and accessibility proxy checks. Real axe/screen-reader proof remains missing. | AFK local |

### Backend / Data Pipeline

| Missing system | Current evidence | Disposition |
| --- | --- | --- |
| Real asset pipeline: file existence, byte hash, MIME, dimension, duration, size, placement validation | `synthetic_asset_validation.v1` now verifies deterministic synthetic files, checksums, byte sizes, MIME signatures, metadata, and unsupported formats. | Implemented for synthetic files; HITL before customer files |
| Production batch/project persistence: database choice, row-level app sync, versioned exports, migrations | `local_batch_store.v1` plus `sqlite_workspace_store.v1` now persist source snapshots, launch plan, review state, asset validation, synthetic tenants, row decisions, migrations, and audit events. | Partially implemented AFK local; production auth/deploy remains blocked |
| Production audit event implementation | Current code appends synthetic local audit events; no authenticated actor, tenant, or external mutation audit exists. | AFK simulation; HITL before private/external use |
| Strict manifest schema and diagnostics | `ManifestSchemaError` now blocks missing required columns and unknown columns before row-level planning. | Implemented for offline CSV contract |
| Stable issue/preflight taxonomy | Current preflight grouping is derived from issue-code substring matching. | AFK local |
| Customer-ready export handoff | Output is dry-run JSON/Markdown/HTML, not verified Meta bulk sheet, API payload, or approved manual handoff package. | AFK for offline shape, HITL for platform proof |

### Platform / Security / SRE

| Missing system | Current evidence | Disposition |
| --- | --- | --- |
| Official Meta Marketing API contract mapping: object model, API version, fields, unsupported/manual fields | `docs/platform/meta_marketing_api_contract_mapping.md` and `meta_platform_payload_preview.v1` now exist, still non-executable. | Implemented for AFK mapping; HITL/external proof remains |
| Sandbox or read-only account proof | No Meta API client, no sandbox, no token flow, no account proof. | HITL/external |
| OAuth/token design: storage, rotation, scopes, redaction | `customer_data_trust_gates.md` blocks OAuth/token work until a G2 approval artifact defines secret handling. | HITL before implementation |
| Customer-data retention, deletion, and redaction policy | `customer_data_trust_gates.md` blocks real customer data until a G1 approval artifact defines retention, deletion, redaction, storage, and access. | HITL before real data |
| Tenant/account isolation and permission enforcement | Roles are labels in issue ownership, not app permissions. | AFK simulation; HITL before private/external use |
| Mutation-capable path separation, kill switch, rollback, two-key signoff | Current implementation has only dry-run output and blocked payload previews; G6 defines required live-mutation approval. | AFK design; HITL for live mutation |
| Rate-limit, retry, timeout, partial-failure, reconciliation semantics | PRD/RFC name these, implementation does not contain them. | AFK mock design; external validation later |

### QA / GTM / Operations

| Missing system | Current evidence | Disposition |
| --- | --- | --- |
| Three agency workflow rehearsals with operators | Rehearsal plan exists in [agency_workflow_rehearsal_plan.md](../research/agency_workflow_rehearsal_plan.md); rehearsals have not happened. | External |
| Willingness-to-pay, buyer role, budget source, safe-export value | Current evidence is public market research and hypothesis-tier GTM. | External |
| Paid pilot or LOI gate | No pilot scope, success metric, legal/data boundary, or agency acceptance criteria yet. | External plus HITL if real data |
| Expanded fixture matrix: real-ish assets, dimensions, malformed CSVs, duplicate/review-state fixtures, golden exports | `manifest_edge_cases.csv` and `golden_edge_summary.json` now cover parser/mapping/idempotency/reviewer edge cases; real file-byte fixtures and property-style fuzzing remain open. | AFK local |
| Browser/UI QA with screenshots, accessibility, persistence/reload, export confirmation | Static audit, headless Chrome/CDP smoke, reusable `workspace_browser_qa.v1`, empty/error states, export confirmation, and CI lane now exist; real axe/screen-reader and browser-runtime save/resume proof remain open. | AFK local |
| Competitive battlecard and onboarding plan | Current web scan exists in [market_and_competitor_scan_2026-07-06.md](../research/market_and_competitor_scan_2026-07-06.md); pricing and current competitor proof are still not customer validation. | AFK current scan plus external proof |
| Kill/pivot review after discovery | Operating cadence defines the trigger, but no discovery evidence has landed yet. | External |

## P1 Missing Systems

- Search, sort, group, owner tabs, saved filters, and pagination/virtualization for 1,000-row batches.
- Naming taxonomy configuration and customer-specific mapping tables.
- Import-plan schema versioning, migrations, retry state, and artifact collision policy.
- `validate`, `schema`, `diff`, `inspect`, `--fail-on-blockers`, and machine-readable summary CLI modes.
- Secret scanning, dependency scanning, mocked platform contract tests, and deeper browser/accessibility QA beyond the current CI proxy.
- Structured logging, SLOs, support runbooks, and failure taxonomy.
- Customer feedback decision log and staffed ownership calendar.
- Meta app review, business verification, and compliance plan.

## P2 Missing Systems

- Production SaaS packaging, deployment, rollback, branch protection, and release approvals.
- More import sources beyond CSV: Google Sheets, Drive, Figma, Airtable, asset folders, Slack handoff.
- Multi-client/admin settings and template library for agency naming rules.
- API-assisted or live publishing path with OAuth, scopes, policy approval, spend safety, rollback, and production upload QA.
- Broader channel evidence beyond the initial Reddit/web/last30days research.

## Ranking

| Rank | Frontier | Why |
| ---: | --- | --- |
| 1 | Operator-usable local app | Converts static proof into something an agency operator can use without docs. This unlocks rehearsals. |
| 2 | Production persistence, row-level sync, and real file validation | Builds on the local batch store and gives the app real state, review history, reproducibility, and visual QA. |
| 3 | Agency rehearsals and pricing proof | Decides whether the product is worth continuing toward pilots. |
| 4 | Sandbox/read-only and validate-only proof after HITL | Turns official-source mapping and blocked payload preview into real external proof without live mutation. |
| 5 | Approved customer-data and credential unlocks | The AFK gate matrix exists; real agency data or credentials require approval artifacts. |
| 6 | Deeper accessibility and browser-runtime verification | Raises confidence that the workflow survives real use beyond the current static/CDP/proxy gates. |

## Director Disposition

Safe local work has now advanced operator bulk workflow, SQLite persistence proof, current market/competitor scan, and real synthetic file-byte validation. Remaining safe local work should focus on browser-to-backend review-state sync, revalidation loops, richer accessibility proof, and manifest fuzzing. External work should focus on three agency rehearsals and buyer/pricing proof. Platform execution, credentials, sandbox account access, customer data, production deploy, and live Meta mutation remain blocked until HITL, gate-specific approval artifacts, and two-key Platform/Security review.
