# PRD: Meta Creative Launch Workspace

Date: 2026-07-05
Owner: Product & Agency Workflow Lead
Status: v0 local/offline PRD

## Problem

Agencies launching high-volume Meta creative lose time translating sheets, asset folders, approvals, naming rules, tracking rules, and placement requirements into launch-ready ads. The current offline prototype proves that a synthetic 100-row batch can be converted into ready, needs-review, and blocked rows with owner-routed fixes.

The next product leap is to make that workflow understandable and repeatable for an operator without reading implementation docs.

## Customer

Primary user: agency media buyer or creative ops manager preparing batches of 30 to 1,000 creative variants.

Supporting users:

- Account manager: needs client-safe review packet.
- Creative ops manager: owns asset, naming, variant, and approval fixes.
- Approver: signs off before external handoff.
- Strategist: cares about taxonomy, destination, UTM, and test design.

## Jobs To Be Done

- Import a creative batch from a structured manifest.
- See what is launch-ready, needs review, or blocked.
- Understand who owns each fix.
- Review the proposed launch plan before any external action.
- Hand creative assets off to the customer's Meta creative folders or ad-account media assets instead of becoming a durable creative warehouse.
- Export a dry-run plan with deterministic lineage and idempotency.

## Acceptance Tiers

### Tier 0: Offline Proof, Already Achieved

- Parse 100 synthetic rows.
- Preserve 30 launch-ready candidates in the existing fixture.
- Route blocked and warning rows to the right owner.
- Generate JSON, Markdown, and static HTML artifacts.
- Make no external platform compatibility claim.

### Tier 1: Operator-Usable Local App

- Batch list, row detail, fix queue, preview pane, and export panel exist in one app surface.
- Operator can complete a review of the synthetic 100-row batch without reading docs.
- Every blocked row has owner, reason, proposed fix, and source-row lineage.
- Review state persists locally.
- Golden fixture and browser QA pass.

### Tier 2: Platform-Ready Contract

- Offline plan maps to a versioned platform contract table.
- Asset storage contract models Meta-native handoff with local original retention limited to approved transient processing.
- Unsupported fields and manual handoff fields are explicit.
- Rate-limit, retry, and idempotency rules are documented.
- Read-only or sandbox proof is planned after HITL approval.
- Platform and Security two-key review passes.

### Tier 3: Customer Pilot Candidate

- Three agency operators complete a synthetic rehearsal.
- At least two operators say the workflow would reduce launch-prep or QA time materially.
- Buying role, willingness-to-pay range, and onboarding blockers are captured.
- Threat model, retention policy, permission model, and audit event schema exist.
- No private or external integration is implemented without HITL.

## Non-Goals

- No external account writes.
- No private customer creative ingestion.
- No credential setup.
- No spend-related behavior.
- No platform compatibility claim beyond documented, evidence-backed contract mapping.

## Metrics

- Batch review time for 100 rows.
- Percentage of rows with clear owner and proposed fix.
- Number of ambiguous blockers.
- Operator confidence score after demo.
- Export reproducibility across repeated runs.

## Open Risks

- Agencies may only pay for direct publishing.
- Existing tools may already cover enough launch QA for some teams.
- Platform object mapping may make some desired workflows manual-only.
- Operator UX may need previews before the data model is fully mature.

## Review Gates

- Product plus Creative Ops: workflow and owner routing.
- Data Pipeline plus SRE: contract, idempotency, persistence, and retries.
- Platform plus Security: external integration, credential, and private-data gates.
- QA / Evidence: fixture, browser, and closeout proof before readiness claims.
