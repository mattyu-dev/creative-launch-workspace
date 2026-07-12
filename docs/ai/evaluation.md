# Evaluation protocol

## Dataset

`evals/brief_mapping/dataset_v1.jsonl` contains two suites:

- 36 labelled contract cases for the deterministic baseline: 24 development and 12 holdout;
- 12 natural-prose/adversarial cases for a repeated live-provider run: six development and six holdout.

Together they cover English and French briefs, missing critical fields, contradictions, prompt injection, live-action requests, credential signals, customer-data signals, URL userinfo attacks, invalid allowlist values, noisy prose and optional-field abstention.

The generator is versioned beside the dataset. CI rebuilds it and rejects drift.

## Release gates

- contract-valid output or explicit failure: 100%;
- exact field match for the deterministic baseline: 100%;
- evidence quote found in the input: 100%;
- expected risk-flag recall: 100%;
- expected release status: 100%;
- deterministic replay: 100%;
- mutation and human-review guards: 100%.

The baseline is intentionally simple. Its perfect score proves the harness and policy contract, not model intelligence. The live-provider runner performs three repetitions by default and records returned models, latency range/mean, usage, failures, exact-field accuracy, evidence grounding, risk recall, status accuracy and high-band precision.

## Artifacts

- [Baseline eval report](../evidence/brief-mapping-baseline-eval.json)
- [Proposal example](../evidence/brief-proposal-example.json)
- [Human review receipt](../evidence/brief-review-example.json)
- [Materialized manifest validation](../evidence/reviewed-manifest-validation.json)
