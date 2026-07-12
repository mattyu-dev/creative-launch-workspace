# RFC 0001: Launch Workspace App Architecture

Date: 2026-07-05
Owner: CTO / Architect
Status: proposed local/offline architecture

## Context

The repo currently has a CLI and static HTML output. That proves data flow, but not an operator-grade product surface. This RFC defines the next architecture without crossing into external mutation, private data, or credential handling.

## Decision

Build the next product slice as a local-first app around the existing `meta_importer` domain package.

The domain package remains the source of truth for:

- Manifest parsing.
- Validation.
- Launch-plan construction.
- Idempotency.
- Dry-run export.
- Review packet generation.

The app layer owns:

- Batch selection.
- Row detail and fix queue state.
- Preview and review workflow.
- Local persistence.
- Export and audit display.

## Architecture

```text
fixtures / local manifests
        |
        v
meta_importer domain package
        |
        v
local workspace state store
        |
        +--> app UI: batch list, row detail, fix queue, preview, export
        |
        +--> dry-run artifacts: JSON, Markdown, HTML, audit summary
```

## Interfaces

- Input: CSV manifest using current v1 or v2 fixture shape.
- Domain output: `offline_launch_plan.v2`.
- UI state: local review decisions keyed by batch id, row id, and idempotency key.
- Export: dry-run JSON plus review packet.

## Persistence

First app slice should use local files under `runs/` or a local SQLite store. Persistence must not store private customer data until Security approves a data classification and retention policy.

Future production persistence should store lineage metadata, review state, Meta asset identifiers, and audit events. It should not become durable storage for original creative files; the target asset path is transient validation/upload followed by handoff into Meta creative folders or ad-account media assets.

## Failure Modes

- Manifest parse failure: fail closed with row and column context.
- Partial review state: resume from last saved local state.
- Export collision: require deterministic overwrite or versioned run directory.
- Unknown platform field: mark unsupported rather than dropping silently.
- Fixture drift: golden tests fail.

## Observability

Local logs should record:

- Batch id.
- Source manifest hash.
- Row counts by state.
- Validator version.
- Export artifact paths.
- Error class and source row when available.

No private creative content should be logged without a future redaction policy and HITL approval.

## Alternatives Rejected

- Direct external integration first: rejected because platform, trust, and customer gates are not ready.
- Static HTML only: useful proof, but not enough for operator workflow.
- Spreadsheet-only product: too close to existing native workflows and does not create the review/control surface.

## Review Gates

- CTO / Architect approves domain-app boundary.
- Data Pipeline Lead approves import-plan versioning.
- SRE Lead approves resume and local observability design.
- Security / Secrets Officer approves data storage policy before private data.
