# Contributing

Small, evidence-backed changes are welcome.

Before opening a pull request:

```bash
pip install -e '.[dev]'
ruff check .
mypy meta_importer/ai meta_importer/clock.py meta_importer/review_policy.py
coverage run -m unittest discover -s tests -q
coverage report
npm ci
npm run qa:frontend
```

If a change affects generated fixtures, the brief benchmark, AI evidence, or the static workspace, run the corresponding generator and commit the updated artifact. Do not add real campaign data, customer assets, credentials, account IDs, or executable Meta calls.

Model changes need a versioned eval report. A green deterministic baseline is not evidence that a live model is good enough.
