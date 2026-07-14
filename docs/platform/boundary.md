# Meta platform boundary

The current release does not call the Meta Marketing API.

The platform preview maps local concepts to a future campaign, ad set, media, creative and ad sequence, but every payload remains `draft_blocked`. It contains no real account IDs, page identities, tokens, uploads, budgets, or executable endpoint requests.

Its data classification is derived from the same launch-plan rows as the plan and browser state. An explicitly allowed operator manifest therefore remains labelled `operator_supplied_manifest_no_live_mutation`; the preview never relabels it as a synthetic fixture.

A future adapter would require separate proof for app review, permissions, identity resolution, media upload, validate-only behavior, idempotency, retries, and audit. Live mutation would still require explicit human approval.

The intended asset architecture is zero-retention by default: customer-owned creative storage, transient processing, durable hashes and lineage only. That design has not been exercised with customer data.
