# Contributing

Small, evidence-backed changes are welcome.

Before opening a pull request:

```bash
pip install -e '.[dev]'
ruff check .
mypy meta_importer/ai meta_importer/clock.py meta_importer/review_policy.py meta_importer/fix_lab.py meta_importer/product_page.py
coverage run -m unittest discover -s tests -q
coverage report
npm ci
npm run qa:frontend
```

If a change affects generated fixtures, the brief benchmark, AI evidence, product entry, Fix & Revalidate Lab, or the static workspace, run the corresponding generator and commit the updated artifact:

```bash
python scripts/rebuild_ai_evidence.py
python scripts/rebuild_fix_lab.py
python scripts/rebuild_product_page.py
creative-launch plan fixtures/fake_agency_creatives/manifest_v2.csv --html docs/workspace.html
```

Do not add real campaign data, customer assets, credentials, account IDs, or executable Meta calls.

Model changes need a versioned eval report. A green deterministic baseline is not evidence that a live model is good enough.
