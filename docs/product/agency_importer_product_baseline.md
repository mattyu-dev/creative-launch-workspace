# Agency Creative Importer Product Baseline

## Objective

Build the fastest safe path for a performance agency to turn a messy batch of Meta creatives into a reviewable, validated, dry-run import plan.

This baseline is intentionally offline-first. It does not require real Meta credentials, real customer assets, customer data, or live account mutation.

## ICP Wedge

Initial wedge: paid social agencies managing 1,000+ Meta creative variants per week across multiple client accounts, campaigns, ad sets, placements, formats, hooks, destinations, and approval states.

Primary pain:

- creative batches arrive in spreadsheets, Drive folders, Figma exports, Airtable views, Slack threads, and naming sheets;
- media buyers spend too much time mapping assets to campaigns and ad sets;
- creative ops spends too much time finding missing approvals, bad names, duplicate assets, wrong dimensions, and destination mismatches;
- importing at scale is risky because a small mapping error can create many wrong ads.

## Agency Roles

| Role | Job In The Workflow | Needs |
| --- | --- | --- |
| Creative Strategist | Defines hooks, variants, copy angles, and creative testing intent | Variant lineage, naming, message consistency |
| Creative Ops Manager | Prepares assets, catches errors, coordinates approvals | Bulk QA, issue queue, pass/fail reasons |
| Media Buyer | Maps creatives to account, campaign, ad set, placement, objective, and destination | Import plan, dry-run diff, Meta object mapping |
| Account Manager | Checks client readiness, approvals, and delivery risk | Review summary, exceptions, approval status |
| Approver | Signs off on launch-ready creative sets | Preview, diffs, issue resolution history |

## RACI

| Stage | Responsible | Accountable | Consulted | Informed |
| --- | --- | --- | --- | --- |
| Intake | Creative Ops Manager | Account Manager | Creative Strategist | Media Buyer |
| Normalize | Creative Ops Manager | Creative Ops Manager | Media Buyer | Account Manager |
| Map | Media Buyer | Media Buyer | Creative Ops Manager | Account Manager |
| Validate | Creative Ops Manager | Creative Ops Manager | Media Buyer, Approver | Account Manager |
| Preview/Diff | Media Buyer | Account Manager | Creative Ops Manager | Approver |
| Approve | Approver | Account Manager | Media Buyer | Creative Strategist |
| Export/Publish Candidate | Media Buyer | Account Manager | Platform/Security for live scope | Creative Ops Manager |
| Audit | Account Manager | COO / Import Ops | Media Buyer | Client team |

## Default Workflow

1. Intake source material from spreadsheet, Drive folder, Figma export, Airtable, naming sheet, or existing creative library.
2. Normalize every creative into a typed manifest row.
3. Map rows to account, campaign, ad set, placement, objective, destination, and naming taxonomy.
4. Validate formats, dimensions, naming, duplicate asset hashes, copy, landing pages, approvals, and missing fields.
5. Build a deterministic dry-run import plan with idempotency keys and lineage.
6. Generate previews and diffs for review.
7. Route issues to the responsible agency role.
8. Approve or revise the batch.
9. Export an offline import plan; live publish remains HITL-gated.
10. Audit the run and preserve object lineage.

## First Manifest Shape

Required fields:

- `creative_id`
- `campaign_key`
- `adset_key`
- `format`
- `asset_path`
- `primary_text`
- `headline`
- `destination_url`
- `approval_status`
- `qa_issue`

Future fields:

- `account_id_alias`
- `objective`
- `placement`
- `asset_hash`
- `variant_group`
- `hook`
- `language`
- `country`
- `idempotency_key`
- `source_system`
- `source_row_id`
- `reviewer`
- `approved_at`

## Fixture Requirements

The first fake fixture pack lives at `fixtures/fake_agency_creatives/` and must remain synthetic:

- 3 campaigns;
- 10 ad sets;
- 100 creative rows;
- image, video, carousel, and story formats;
- naming errors;
- missing approvals;
- duplicate asset references;
- destination mismatches;
- at least one clean passing subset.

## First Local Validation Gate

A fixture is valid for the baseline if:

- the CSV has exactly 100 creative rows plus one header row;
- all campaign and ad set keys are non-empty;
- every `destination_url` uses `example.invalid`;
- every `asset_path` stays under `fixtures/fake_agency_creatives/assets/`;
- `approval_status` is one of `approved`, `pending`, or `rejected`;
- `qa_issue` is either empty or one of the fixture's documented synthetic issue types.

## First Implemented Proof

The first offline launch-workspace proof lives in `meta_importer/` and can be run with:

```bash
python3 -m meta_importer.cli plan fixtures/fake_agency_creatives/manifest.csv --out runs/fake_agency_creatives/launch_plan.json --review runs/fake_agency_creatives/review_packet.md --html runs/fake_agency_creatives/workspace.html --html-audit runs/fake_agency_creatives/workspace_audit.json --state runs/fake_agency_creatives/review_state.json --platform-preview runs/fake_agency_creatives/platform_preview.json --store-dir runs/fake_agency_creatives/store
```

The synthetic fixture rehearsal produces 30 launch-ready candidates, 10 needs-review duplicate rows, and 60 blocked rows with owner-routed fixes. This remains dry-run only and does not call Meta APIs or publish ads.

## Approval Ladder

| Stage | Internal Signoff | Evidence |
| --- | --- | --- |
| Workflow hypothesis | Product plus GTM | ICP wedge, target roles, pain statement |
| Validated workflow | Product, Creative Ops, Implementation / CS | RACI, workflow, failure modes |
| Offline import candidate | Data Pipeline, QA, Creative Ops | Fake manifest, validation checks, dry-run plan |
| API mutation candidate | Platform, Security, SRE, QA | API contract, credential plan, rollback, audit path |
| Live mutation | Director / GM plus HITL | Scoped account, dry-run diff, approval record |
| Customer rollout | CS, Security, GTM, COO | Onboarding, data handling, support path, success metric |

## GTM Hypothesis

Positioning: "Turn a week's worth of Meta creative chaos into a validated import plan before lunch."

Packaging assumption:

- starter: offline QA and import-plan generation;
- team: collaboration, approvals, preview/diff, templates;
- agency scale: multi-client workspaces, audit trails, API-assisted publishing behind explicit approval.

Success metric for first proof:

- reduce manual mapping and QA time for a 100-creative batch by at least 50% in a fake workflow rehearsal before using any real customer data.

## Failure Modes To Catch First

- wrong campaign/ad-set mapping;
- approved creative missing destination;
- destination mismatch inside same ad set;
- duplicate asset accidentally treated as a new variant;
- naming taxonomy mismatch;
- rejected creative included in launch candidate;
- unsupported format routed to publish candidate;
- missing lineage between source row and import plan.
