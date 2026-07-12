# Pilot Onboarding And Support Runbook

Date: 2026-07-06
Owner: Implementation / Customer Success Lead
Status: started local/offline runbook

## Boundary

This runbook supports synthetic rehearsals and future approved pilots. It does not authorize customer data import, credentials, OAuth, sandbox calls, uploads, validate-only execution, live mutation, or production rollout.

## Pre-Call Checklist

- Confirm participant role and weekly creative volume.
- Generate the synthetic v2 workspace.
- Confirm no customer files or account IDs will be imported.
- Prepare interview capture notes.
- Prepare the kill/pivot criteria.
- Confirm the operator understands the demo does not publish to Meta.

## Rehearsal Command

```bash
python3 -m meta_importer.cli plan fixtures/fake_agency_creatives/manifest_v2.csv --out runs/fake_agency_creatives_v2/launch_plan.json --review runs/fake_agency_creatives_v2/review_packet.md --html runs/fake_agency_creatives_v2/workspace.html --html-audit runs/fake_agency_creatives_v2/workspace_audit.json --state runs/fake_agency_creatives_v2/review_state.json --platform-preview runs/fake_agency_creatives_v2/platform_preview.json --store-dir runs/fake_agency_creatives_v2/store --asset-metadata fixtures/fake_agency_creatives/asset_metadata.csv
```

## Call Agenda

1. Current workflow baseline.
2. Synthetic workspace walkthrough.
3. Operator tries the review flow.
4. Trust and handoff questions.
5. Pricing and buyer discovery.
6. Pilot fit decision.

## Support Loop

For each rehearsal:

- log confusing product moments;
- log missing fields or previews;
- log trust objections;
- log what the operator would still do manually;
- log whether safe export alone has value;
- convert repeated issues into product backlog items.

## Incident And Deletion Placeholder

If customer data is accidentally offered or shared before G1:

1. Stop the rehearsal.
2. Do not store the data in the repo, vault, fixtures, logs, or generated artifacts.
3. Ask the operator to send only redacted or synthetic examples.
4. Record the incident as a trust finding without private details.
5. Resume only after Security and Product review.

## Exit Criteria

A rehearsal is complete when:

- the operator has reviewed the synthetic workspace;
- time-saved and pain evidence are captured;
- buyer role and budget path are captured or marked unknown;
- safe-export value is yes, no, or unclear;
- next gate is selected: no-fit, more discovery, G1 customer-data approval, or product-app work.
