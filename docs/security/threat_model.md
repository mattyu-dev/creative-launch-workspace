# Threat model

## Protected assets

- campaign and client boundaries;
- creative files and destinations;
- approvals and reviewer identity;
- credentials and platform identifiers;
- mapping lineage and audit history.

## Primary failure modes

- a blocked row is approved through a secondary storage path;
- model output invents or misquotes a mapping value;
- an injected brief changes system behavior;
- real data is sent to an external model;
- a fixture-looking relative path traverses or follows a symlink outside the synthetic asset root;
- an operator-supplied manifest is mislabeled as synthetic in a downstream preview;
- a local preview is mistaken for an executable Meta payload;
- stale generated evidence passes CI.

## Controls in this release

- synthetic-only defaults, `.invalid` destinations and canonical asset containment checks that reject absolute paths, parent traversal and symlink escapes;
- one data-classification function shared by launch plans, review state and non-executable platform previews;
- credential, account-ID and customer-data preflight before external providers;
- strict model schema and field allowlists;
- verbatim evidence grounding;
- abstention on missing, conflicting or unsafe inputs;
- mandatory field-level human review;
- review and materialization execute in one process against the original brief and proposal; persisted receipts are never accepted as authorization input;
- shared fail-closed review policy in SQLite and the browser;
- no Meta client, token loader, upload path or mutation endpoint;
- CodeQL, locked npm and Python dependency audits, coverage, static checks and reproducible artifacts.

The receipt checksum detects accidental edits; it is not presented as a cryptographic signature. The local operator is inside this prototype's trust boundary, and reviewer identity is not authenticated. Same-process review, source binding, deterministic revalidation and the absence of a platform mutation path are the effective controls. This is not a production security certification.
