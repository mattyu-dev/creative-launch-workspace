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
            f"<td data-label='Value'><code>{html.escape(field['value'])}</code></td>"
            f"<td data-label='Verbatim evidence'>&ldquo;{html.escape(field['evidence_quote'])}&rdquo;</td>"
            "<td data-label='Evidence'><span class='evidence-strength'>Direct</span>"
            f"<small>{html.escape(field['confidence_band']).title()} &middot; uncalibrated</small></td>"
            f"<td data-label='Decision'><span class='accepted'>&#10003; {html.escape(field['review_status']).title()}</span></td>"
            "</tr>"
        )
    summary = materialization["validation_summary"]["batch_states"]
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <meta name="description" content="Inspect the field-level evidence, policy boundary and human decisions behind a synthetic brief mapping proposal.">
  <meta name="author" content="Mathieu Petroni">
  <link rel="canonical" href="https://mattyu-dev.github.io/creative-launch-workspace/brief-evidence.html">
  <link rel="me" href="https://www.linkedin.com/in/mathieu-petroni/">
  <meta property="og:type" content="article">
  <meta property="article:author" content="https://www.linkedin.com/in/mathieu-petroni/">
  <meta property="og:title" content="Governed intake evidence · Mathieu Petroni">
  <meta property="og:description" content="Source evidence, bounded proposals, policy checks and explicit human decisions.">
  <meta property="og:image" content="https://mattyu-dev.github.io/creative-launch-workspace/assets/social-card-v2-2.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="preload" href="assets/mona-sans-latin-variable.woff2" as="font" type="font/woff2" crossorigin>
  <title>Brief mapping evidence · Mathieu Petroni</title>
  <style>
    @font-face{{font-family:"Mona Sans";src:url("assets/mona-sans-latin-variable.woff2") format("woff2-variations");font-weight:200 900;font-display:optional}}
    :root {{ --ink:#1c1422; --body:#4e4652; --muted:#6c6570; --canvas:#f7f6f8; --paper:#ffffff; --line:#d9d3dd; --brand:#24142b; --brand-hover:#36213f; --brand-soft:#eee9ff; --accent:#d91f72; --action:#ffe44d; --action-hover:#efd33b; --success:#176143; --success-soft:#e3eee8; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; color:var(--ink); background:var(--canvas); font:400 15px/1.5 "Mona Sans",ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }}
    header {{ padding:14px max(20px,calc((100vw - 1180px)/2)); border-bottom:1px solid var(--line); background:var(--paper); }}
    header nav {{ min-height:32px; display:flex; align-items:center; justify-content:space-between; gap:18px; }}
    header a {{ color:var(--brand); text-decoration:none; font-weight:700; }} header .product-link {{ font-size:12px; text-decoration:underline; text-underline-offset:3px; }}
    main {{ width:min(1180px,calc(100% - 32px)); margin:0 auto; padding:48px 0 64px; }}
    .eyebrow {{ color:var(--accent); font-size:12px; font-weight:700; letter-spacing:.1em; text-transform:uppercase; }}
    h1 {{ max-width:850px; margin:10px 0 14px; font-size:clamp(34px,5vw,62px); font-weight:760; line-height:1.02; letter-spacing:-.035em; }}
    .lead {{ max-width:760px; color:var(--body); font-size:18px; }}
    .flow {{ display:grid; grid-template-columns:repeat(4,1fr); margin:28px 0; border-block:1px solid var(--line); }}
    .flow div {{ min-width:0; padding:13px 14px 13px 0; border-right:1px solid var(--line); }}
    .flow div + div {{ padding-left:14px; }} .flow div:last-child {{ border-right:0; }}
    .flow b {{ display:block; color:var(--accent); font:700 10px/1.4 ui-monospace,SFMono-Regular,Menlo,monospace; }}
    .flow span {{ display:block; margin-top:3px; font-size:12px; font-weight:700; }}
    .grid {{ display:grid; grid-template-columns:360px minmax(0,1fr); align-items:start; gap:20px; }}
    section {{ border:1px solid var(--line); border-radius:14px; background:var(--paper); overflow:hidden; }}
    .source-rail {{ position:sticky; top:84px; }}
    section h2 {{ margin:0; padding:15px 18px; border-bottom:1px solid var(--line); font-size:14px; }}
    pre {{ margin:0; padding:18px; overflow:auto; color:var(--body); white-space:pre-wrap; font:500 12px/1.7 ui-monospace,SFMono-Regular,Menlo,monospace; }}
    .metadata {{ margin:0; padding:12px 18px 16px; border-top:1px solid var(--line); }}
    .metadata div {{ display:grid; grid-template-columns:76px minmax(0,1fr); gap:8px; padding:5px 0; }}
    .metadata dt {{ color:var(--muted); font-size:10px; text-transform:uppercase; }}
    .metadata dd {{ margin:0; overflow-wrap:anywhere; font:600 10px/1.45 ui-monospace,SFMono-Regular,Menlo,monospace; }}
    .table-wrap {{ overflow:auto; }}
    table {{ width:100%; border-collapse:collapse; font-size:12px; }}
    th,td {{ padding:12px 14px; border-bottom:1px solid var(--line); text-align:left; vertical-align:top; }}
    th {{ min-width:100px; font-weight:700; }}
    code {{ color:var(--brand); font-weight:700; }}
    small {{ display:block; margin-top:4px; color:var(--muted); }}
    .evidence-strength {{ display:inline-block; padding:3px 7px; border-radius:999px; color:var(--brand); background:var(--brand-soft); font-size:10px; font-weight:800; text-transform:uppercase; }}
    .accepted {{ color:var(--success); font-size:11px; font-weight:750; }}
    .guardrail-behavior {{ margin-top:18px; border:1px solid var(--line); background:var(--paper); }}
    .guardrail-behavior h2 {{ margin:0; padding:14px 18px; border-bottom:1px solid var(--line); font-size:13px; }}
    .guardrail-grid {{ display:grid; grid-template-columns:repeat(3,1fr); }}
    .guardrail-grid div {{ padding:15px 18px; border-right:1px solid var(--line); }} .guardrail-grid div:last-child {{ border-right:0; }}
    .guardrail-grid strong {{ display:block; margin-bottom:4px; font-size:12px; }} .guardrail-grid span {{ color:var(--muted); font-size:11px; }}
    .proof {{ display:grid; grid-template-columns:repeat(3,1fr); margin-top:18px; border-block:1px solid var(--line); }}
    .proof div {{ padding:18px; border-right:1px solid var(--line); }} .proof div:last-child {{ border-right:0; }}
    .proof strong {{ display:block; font-size:24px; }}
    .proof span {{ color:var(--muted); font-size:12px; }}
    .boundary {{ margin:20px 0 0; padding:14px 16px; border-left:3px solid var(--accent); background:var(--brand-soft); color:var(--body); }}
    .links {{ display:flex; flex-wrap:wrap; gap:14px; margin-top:20px; }}
    .links a {{ color:var(--brand); font-weight:700; }}
    .creator-cta {{ display:flex; align-items:center; justify-content:space-between; gap:24px; margin-top:30px; padding:20px 22px; border-radius:14px; color:#fff; background:var(--brand); }}
    .creator-cta p {{ margin:0; color:rgba(255,255,255,.82); }} .creator-cta strong {{ display:block; color:#fff; font-size:22px; font-weight:760; line-height:1.2; }}
    .creator-cta a {{ flex:0 0 auto; min-height:44px; display:inline-flex; align-items:center; padding:9px 12px; border:1px solid var(--action); border-radius:8px; color:var(--ink); background:var(--action); text-decoration:none; font-weight:750; }}
    .creator-cta a:hover {{ border-color:var(--action-hover); background:var(--action-hover); }}
    @media(max-width:760px) {{
      main {{ padding-top:30px; }} .grid {{ grid-template-columns:1fr; }} .source-rail {{ position:static; }} h1 {{ font-size:38px; }}
      .flow {{ grid-template-columns:1fr 1fr; }} .flow div:nth-child(2) {{ border-right:0; }} .flow div:nth-child(-n+2) {{ border-bottom:1px solid var(--line); }}
      .proof,.guardrail-grid {{ grid-template-columns:1fr; }} .proof div,.guardrail-grid div {{ border-right:0; border-bottom:1px solid var(--line); }} .proof div:last-child,.guardrail-grid div:last-child {{ border-bottom:0; }}
      .creator-cta {{ align-items:flex-start; flex-direction:column; }}
    }}
    @media(max-width:700px) {{
      thead {{ display:none; }} tbody,tr,td,th {{ display:block; }} tbody tr {{ padding:13px 0; border-bottom:1px solid var(--line); }} tbody tr:last-child {{ border-bottom:0; }}
      tbody th {{ padding:5px 14px; border:0; font-size:14px; }} tbody td {{ display:grid; grid-template-columns:104px minmax(0,1fr); gap:12px; padding:5px 14px; border:0; }}
      tbody td::before {{ content:attr(data-label); color:var(--muted); font-size:9px; font-weight:700; letter-spacing:.05em; text-transform:uppercase; }}
    }}
  </style>
</head>
<body>
  <header><nav aria-label="Product navigation"><a href="index.html">&larr; Creative Launch Workspace</a><a class="product-link" href="workspace.html?guided=1">Open the workspace</a></nav></header>
  <main>
    <div class="eyebrow">Versioned synthetic evidence</div>
    <h1>A proposal you can inspect before you trust it.</h1>
    <p class="lead">The provider suggests mappings. Policy code checks the schema, source evidence, allowlists and risks. A person decides field by field. Only then can a synthetic manifest be materialized and validated.</p>
    <div class="flow"><div><b>01</b><span>Proposal</span></div><div><b>02</b><span>Policy checks</span></div><div><b>03</b><span>Human review</span></div><div><b>04</b><span>Manifest QA</span></div></div>
    <div class="grid">
      <section class="source-rail"><h2>Source brief</h2><pre>{html.escape(brief)}</pre><dl class="metadata"><div><dt>Provider</dt><dd>{html.escape(proposal['provider'])}</dd></div><div><dt>Model</dt><dd>{html.escape(proposal['model'])}</dd></div><div><dt>Contract</dt><dd>{html.escape(proposal['contract_version'])}</dd></div><div><dt>Prompt hash</dt><dd>{html.escape(proposal['prompt_sha256'][:12])}&hellip;</dd></div><div><dt>Schema hash</dt><dd>{html.escape(proposal['schema_sha256'][:12])}&hellip;</dd></div></dl></section>
      <section><h2>Field-level review</h2><div class="table-wrap"><table><colgroup><col style="width:14%"><col style="width:25%"><col style="width:31%"><col style="width:15%"><col style="width:15%"></colgroup><thead><tr><th>Field</th><th>Value</th><th>Verbatim evidence</th><th>Evidence</th><th>Decision</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div></section>
    </div>
    <section class="guardrail-behavior"><h2>Guardrail behavior</h2><div class="guardrail-grid"><div><strong>Missing critical field</strong><span>Abstain instead of inventing a value.</span></div><div><strong>Real destination or sensitive signal</strong><span>Block before a provider call.</span></div><div><strong>Rejected critical field</strong><span>Refuse materialization.</span></div></div></section>
    <div class="proof">
      <div><strong>{len(FIELD_NAMES)}/8</strong><span>fields grounded and reviewed</span></div>
      <div><strong>{materialization['row_count']}</strong><span>synthetic rows materialized</span></div>
      <div><strong>{summary.get('launch_ready', 0)}</strong><span>rows pass deterministic launch QA</span></div>
    </div>
    <p class="boundary"><strong>No live inference occurs on this page.</strong> This is a committed baseline artifact. Confidence bands are explicitly uncalibrated, the browser has no API key, and every export remains non-executable.</p>
    <div class="links"><a href="evidence/brief-proposal-example.json">Raw proposal JSON</a><a href="evidence/brief-review-example.json">Review receipt JSON</a><a href="evidence/reviewed-manifest-validation.json">Validation JSON</a><a href="evidence/brief-mapping-baseline-eval.json">36-case baseline eval</a></div>
    <aside class="creator-cta"><p><strong>Continue in the product</strong>Return to launch control or open the full review queue.</p><a href="index.html">Back to product</a></aside>
  </main>
</body>
</html>
"""
