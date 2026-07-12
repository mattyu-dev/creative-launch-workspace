# System architecture

```text
Untrusted synthetic brief
        |
        v
provider contract ── deterministic baseline / optional OpenAI Responses API
        |
        v
strict structured output + evidence grounding + allowlists
        |
        v
brief_mapping_proposal.v1 (pending review or abstained)
        |
        v
field-level human decision
        |
        v
same-process review + deterministic validation + materialization
        |
        v
existing manifest validators
        |
        v
review queue + SQLite audit + non-executable platform preview
```

## Authority model

The provider proposes. It has no tools, credentials, customer data, or write path. Policy code validates every field and fails closed when evidence is missing or the output falls outside an allowlist. Human review can create a manifest draft, but deterministic checks remain authoritative. No layer can publish to Meta.

## Contracts

- `brief_mapping_proposal.v1`: versioned field proposals, evidence, confidence bands, risk flags and provenance.
- `brief_mapping_review.v1`: inspectable field-level accept/reject evidence; never an authorization token.
- `reviewed_mapping_materialization.v1`: same-process review, proposal/brief binding, deterministic mapping validation, synthetic template fill and full offline launch-plan result.
- `offline_launch_plan.v2`: normalized rows, issues, idempotency keys and mapping lineage.
- `workspace_review_state.v1`: local decisions and guarded browser import/export.
- `sqlite_workspace_store.v1`: durable synthetic batch state and append-only audit events.
- `meta_platform_payload_preview.v1`: Meta-shaped, non-executable mapping preview.

## Provider boundary

`DeterministicBaselineProvider` is a transparent label parser for CI. It proves the contract and evaluation harness; it is explicitly not an AI-quality claim.

`OpenAIResponsesProvider` is optional. It uses the Responses API with strict Structured Outputs, `store=False`, a bounded timeout, no tools, a configurable model, a versioned fixture-hash allowlist, and credential/customer-data preflight. Provider errors, refusals, empty output, invalid JSON, schema violations, ungrounded evidence, and disallowed values all fail closed.

Implementation follows OpenAI's current [Structured Outputs guide](https://developers.openai.com/api/docs/guides/structured-outputs). The model remains configurable because availability and recommended defaults change over time.

## Reproducibility

Generated artifacts read `SOURCE_DATE_EPOCH` when supplied. The committed demo and eval evidence can therefore be rebuilt byte-for-byte in CI instead of changing with the wall clock.
