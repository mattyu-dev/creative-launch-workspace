from __future__ import annotations

import html
from typing import Any

from .contracts import FIELD_NAMES

LABELS = {
    "campaign_key": "Campaign",
    "adset_key": "Ad set",
    "objective": "Objective",
    "country": "Country",
    "language": "Language",
    "placement": "Placement",
    "destination_url": "Destination",
    "utm_campaign": "UTM campaign",
}


def render_evidence_page(
    *,
    brief: str,
    proposal: dict[str, Any],
    receipt: dict[str, Any],
    materialization: dict[str, Any],
) -> str:
    rows = []
    for name in FIELD_NAMES:
        field = receipt["fields"][name]
        rows.append(
            "<tr>"
            f"<th scope='row'>{html.escape(LABELS[name])}</th>"
            f"<td><code>{html.escape(field['value'])}</code></td>"
            f"<td>&ldquo;{html.escape(field['evidence_quote'])}&rdquo;</td>"
            f"<td><span class='band'>{html.escape(field['confidence_band'])}</span>"
            "<small>uncalibrated</small></td>"
            f"<td><span class='accepted'>{html.escape(field['review_status'])}</span></td>"
            "</tr>"
        )
    summary = materialization["validation_summary"]["batch_states"]
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <title>Brief mapping evidence · Creative Launch Workspace</title>
  <style>
    :root {{ --ink:#1c211e; --body:#48504b; --muted:#6e756f; --canvas:#f7f5ef; --paper:#fffefa; --line:#d8d3c8; --forest:#164a3b; --mint:#cfe2d7; --oxide:#a9472e; --peach:#f4ead4; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; color:var(--ink); background:var(--canvas); font:400 15px/1.5 Inter,ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }}
    header {{ padding:20px max(20px,calc((100vw - 1180px)/2)); border-bottom:1px solid var(--line); background:var(--paper); }}
    header a {{ color:var(--forest); text-decoration:none; font-weight:700; }}
    main {{ width:min(1180px,calc(100% - 32px)); margin:0 auto; padding:48px 0 64px; }}
    .eyebrow {{ color:var(--oxide); font-size:12px; font-weight:700; letter-spacing:.1em; text-transform:uppercase; }}
    h1 {{ max-width:850px; margin:10px 0 14px; font:500 clamp(34px,5vw,62px)/1.02 Georgia,serif; letter-spacing:-.035em; }}
    .lead {{ max-width:760px; color:var(--body); font-size:18px; }}
    .flow {{ display:flex; gap:8px; align-items:center; margin:28px 0; overflow:auto; }}
    .flow span {{ padding:9px 11px; border:1px solid var(--line); border-radius:8px; background:var(--paper); font:700 12px ui-monospace,SFMono-Regular,Menlo,monospace; white-space:nowrap; }}
    .flow i {{ color:var(--oxide); font-style:normal; }}
    .grid {{ display:grid; grid-template-columns:minmax(260px,.8fr) minmax(0,1.6fr); gap:18px; }}
    section {{ border:1px solid var(--line); border-radius:12px; background:var(--paper); overflow:hidden; }}
    section h2 {{ margin:0; padding:15px 18px; border-bottom:1px solid var(--line); font-size:14px; }}
    pre {{ margin:0; padding:18px; overflow:auto; color:var(--body); white-space:pre-wrap; font:500 12px/1.7 ui-monospace,SFMono-Regular,Menlo,monospace; }}
    .table-wrap {{ overflow:auto; }}
    table {{ width:100%; border-collapse:collapse; font-size:12px; }}
    th,td {{ padding:12px 14px; border-bottom:1px solid var(--line); text-align:left; vertical-align:top; }}
    th {{ min-width:100px; font-weight:700; }}
    code {{ color:var(--forest); font-weight:700; }}
    small {{ display:block; margin-top:4px; color:var(--muted); }}
    .band,.accepted {{ display:inline-block; padding:3px 7px; border-radius:999px; font-size:10px; font-weight:800; text-transform:uppercase; }}
    .band {{ color:var(--oxide); background:var(--peach); }}
    .accepted {{ color:var(--forest); background:var(--mint); }}
    .proof {{ display:grid; grid-template-columns:repeat(3,1fr); gap:1px; margin-top:18px; border:1px solid var(--line); border-radius:12px; overflow:hidden; background:var(--line); }}
    .proof div {{ padding:18px; background:var(--paper); }}
    .proof strong {{ display:block; font-size:24px; }}
    .proof span {{ color:var(--muted); font-size:12px; }}
    .boundary {{ margin:20px 0 0; padding:14px 16px; border-left:3px solid var(--oxide); background:var(--peach); color:var(--body); }}
    .links {{ display:flex; flex-wrap:wrap; gap:14px; margin-top:20px; }}
    .links a {{ color:var(--forest); font-weight:700; }}
    @media(max-width:760px) {{ main {{ padding-top:30px; }} .grid {{ grid-template-columns:1fr; }} .proof {{ grid-template-columns:1fr; }} h1 {{ font-size:38px; }} }}
  </style>
</head>
<body>
  <header><a href="index.html">&larr; Creative Launch Workspace</a></header>
  <main>
    <div class="eyebrow">Versioned synthetic evidence</div>
    <h1>A proposal you can inspect before you trust it.</h1>
    <p class="lead">The provider suggests mappings. Policy code checks the schema, source evidence, allowlists and risks. A person decides field by field. Only then can a synthetic manifest be materialized and validated.</p>
    <div class="flow"><span>Proposal</span><i>&rarr;</i><span>Policy checks</span><i>&rarr;</i><span>Human review</span><i>&rarr;</i><span>Manifest QA</span></div>
    <div class="grid">
      <section><h2>Source brief</h2><pre>{html.escape(brief)}</pre></section>
      <section><h2>Field-level review</h2><div class="table-wrap"><table><thead><tr><th>Field</th><th>Value</th><th>Verbatim evidence</th><th>Confidence</th><th>Decision</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div></section>
    </div>
    <div class="proof">
      <div><strong>{len(FIELD_NAMES)}/8</strong><span>fields grounded and reviewed</span></div>
      <div><strong>{materialization['row_count']}</strong><span>synthetic rows materialized</span></div>
      <div><strong>{summary.get('launch_ready', 0)}</strong><span>rows pass deterministic launch QA</span></div>
    </div>
    <p class="boundary"><strong>No live inference occurs on this page.</strong> This is a committed baseline artifact. Confidence bands are explicitly uncalibrated, the browser has no API key, and every export remains non-executable.</p>
    <div class="links"><a href="evidence/brief-proposal-example.json">Raw proposal JSON</a><a href="evidence/brief-review-example.json">Review receipt JSON</a><a href="evidence/reviewed-manifest-validation.json">Validation JSON</a><a href="evidence/brief-mapping-baseline-eval.json">36-case baseline eval</a></div>
  </main>
</body>
</html>
"""
