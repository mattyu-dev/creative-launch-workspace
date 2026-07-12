# Brief mapping model card

## Intended use

Extract explicit campaign mapping fields from a synthetic, unstructured brief into a review-only proposal.

## Not intended for

- publishing or editing ads;
- choosing budgets, audiences, or spend;
- processing credentials, account IDs, customer data, or real destinations;
- replacing a reviewer;
- treating confidence labels as probabilities.

## Inputs and outputs

The input is capped at 20,000 characters. The output schema fixes eight fields: campaign, ad set, objective, country, language, placement, destination, and UTM campaign. Every proposed value needs a verbatim evidence quote. Missing or conflicting critical fields produce an abstained proposal.

External inference is restricted to SHA-256 hashes in the versioned synthetic fixture registry. A matching declaration alone is not sufficient. Sensitive-pattern and parsed-hostname checks still run before the request.

## Confidence

The contract exposes `high`, `medium`, `low`, and `abstain` bands for review ergonomics. `confidence_calibrated` is hard-coded to `false`. A future model may only claim calibrated confidence after repeated holdout runs establish per-band precision.

## Providers

- `deterministic_baseline / label_parser_v1`: CI contract baseline, not AI.
- `openai_responses / configurable model`: optional live provider. No live model benchmark is committed because this repository does not ship credentials.

The CLI currently defaults to `gpt-5.6-terra`, the quality/cost-balanced GPT-5.6 variant in the current [OpenAI model guide](https://developers.openai.com/api/docs/models). Pin or override the model for any reproducible evaluation.

## Failure behavior

The system fails closed. It returns no executable manifest when a provider fails, the schema is invalid, evidence is ungrounded, a value is outside an allowlist, critical information is absent, or a safety signal is detected.

Review revalidates the original brief hash, current schema, canonical output hash, evidence policy, risk flags, release status and proposal identity. The materialization command takes the decisions directly, performs review in the same process, and then runs the resulting rows through the offline launch validators. Persisted receipts are evidence only. Their checksum detects accidental edits; it is not an authenticity signature, and this prototype does not authenticate reviewer identity.
