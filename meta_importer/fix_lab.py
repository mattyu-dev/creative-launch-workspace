from __future__ import annotations

import hashlib
import html
import itertools
import json
from dataclasses import replace
from pathlib import Path
from typing import Any

from .launch_workspace import ManifestRow, build_launch_plan

CONTRACT_VERSION = "fix_lab_rule_pack.v1"
EDITABLE_VALUES = {
    "placement": ("feed", "story"),
    "approval_status": ("pending", "approved"),
    "utm_campaign": ("camp_launch", "camp_sale"),
}


def _base_row() -> ManifestRow:
    return ManifestRow(
        source_row=1,
        creative_id="cr_lab_001",
        campaign_key="camp_sale",
        adset_key="as_sale_us",
        format="story",
        asset_path="fixtures/fake_agency_creatives/assets/sale_story_069.jpg",
        primary_text="A synthetic launch rehearsal",
        headline="Synthetic summer sale",
        destination_url="https://example.invalid/sale-us",
        approval_status="pending",
        qa_issue="",
        account_id_alias="acct_fixture_us",
        objective="sales",
        placement="feed",
        asset_hash="lab-fixture-hash",
        variant_group="camp_sale_as_sale_us",
        hook="lab_hook",
        language="en",
        country="US",
        utm_source="facebook",
        utm_medium="paid_social",
        utm_campaign="camp_launch",
        utm_content="cr_lab_001",
        post_id_type="new",
        source_system="synthetic_lab",
        source_row_id="row_lab_001",
    )


def _scenario_key(values: dict[str, str]) -> str:
    return "|".join(values[name] for name in EDITABLE_VALUES)


def build_fix_lab_rule_pack(*, validator_path: Path | None = None) -> dict[str, Any]:
    scenarios: dict[str, Any] = {}
    field_names = tuple(EDITABLE_VALUES)
    for combination in itertools.product(*(EDITABLE_VALUES[name] for name in field_names)):
        values = dict(zip(field_names, combination))
        plan = build_launch_plan(
            [
                replace(
                    _base_row(),
                    placement=values["placement"],
                    approval_status=values["approval_status"],
                    utm_campaign=values["utm_campaign"],
                )
            ],
            source_manifest="fix_lab.v1",
        )
        candidate = plan.candidates[0]
        scenarios[_scenario_key(values)] = {
            "inputs": values,
            "state": candidate.batch_state,
            "idempotency_key": candidate.idempotency_key,
            "issues": [
                {
                    "code": issue.code,
                    "severity": issue.severity,
                    "owner": issue.owner,
                    "message": issue.message,
                    "proposed_fix": issue.proposed_fix,
                }
                for issue in plan.issues
            ],
        }

    source = validator_path or Path(__file__).with_name("launch_workspace.py")
    validator_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    payload: dict[str, Any] = {
        "contract_version": CONTRACT_VERSION,
        "validator_source_sha256": validator_hash,
        "data_classification": "synthetic_fixture_only",
        "execution_mode": "precomputed_python_golden_scenarios",
        "editable_fields": list(EDITABLE_VALUES),
        "editable_values": {name: list(values) for name, values in EDITABLE_VALUES.items()},
        "initial": {
            "placement": "feed",
            "approval_status": "pending",
            "utm_campaign": "camp_launch",
        },
        "target": {
            "placement": "story",
            "approval_status": "approved",
            "utm_campaign": "camp_sale",
        },
        "scenarios": scenarios,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["rule_pack_sha256"] = hashlib.sha256(canonical).hexdigest()
    return payload


def render_fix_lab(rule_pack: dict[str, Any]) -> str:
    embedded = json.dumps(rule_pack, sort_keys=True).replace("</", "<\\/")
    contract = html.escape(str(rule_pack["contract_version"]))
    short_hash = html.escape(str(rule_pack["rule_pack_sha256"])[:12])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#24142b">
  <meta name="description" content="Fix a synthetic blocked creative row and replay Python-generated golden validation scenarios in the browser.">
  <meta name="author" content="Mathieu Petroni">
  <link rel="canonical" href="https://mattyu-dev.github.io/creative-launch-workspace/fix-lab.html">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="me" href="https://www.linkedin.com/in/mathieu-petroni/">
  <meta property="og:type" content="article">
  <meta property="article:author" content="https://www.linkedin.com/in/mathieu-petroni/">
  <meta property="og:title" content="Fix &amp; Revalidate Lab · Mathieu Petroni">
  <meta property="og:description" content="Replay Python-generated validation scenarios in a bounded interactive lab.">
  <meta property="og:image" content="https://mattyu-dev.github.io/creative-launch-workspace/assets/social-card-v2-2.png">
  <link rel="preload" href="assets/mona-sans-latin-variable.woff2" as="font" type="font/woff2" crossorigin>
  <title>Fix &amp; Revalidate Lab · Mathieu Petroni</title>
  <style>
    @font-face{{font-family:"Mona Sans";src:url("assets/mona-sans-latin-variable.woff2") format("woff2-variations");font-weight:200 900;font-display:optional}}
    :root {{ --canvas:#f7f6f8;--surface:#ffffff;--soft:#f1eef3;--ink:#1c1422;--body:#4e4652;--muted:#6c6570;--line:#d9d3dd;--strong:#a99eae;--brand:#24142b;--brand-hover:#36213f;--brand-soft:#eee9ff;--accent:#d91f72;--action:#ffe44d;--action-hover:#efd33b;--success:#176143;--success-soft:#e3eee8;--red:#9e342b;--red-soft:#f3e1dd;--font-mono:ui-monospace,SFMono-Regular,Menlo,monospace;}}
    *{{box-sizing:border-box}} body{{margin:0;color:var(--ink);background:var(--canvas);font:400 14px/1.5 "Mona Sans",ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}} a{{color:var(--brand)}}
    header{{padding:14px max(18px,calc((100vw - 1120px)/2));border-bottom:1px solid var(--line);background:var(--surface)}} header nav{{min-height:32px;display:flex;align-items:center;justify-content:space-between;gap:18px}} header a{{font-weight:700;text-decoration:none}} header .product-link{{font-size:12px;text-decoration:underline;text-underline-offset:3px}}
    main{{width:min(1120px,calc(100% - 32px));margin:auto;padding:46px 0 70px}} .eyebrow{{color:var(--accent);font-size:11px;font-weight:750;letter-spacing:.1em;text-transform:uppercase}} h1{{max-width:860px;margin:10px 0 14px;font-size:clamp(40px,6vw,70px);font-weight:760;line-height:.98;letter-spacing:-.04em}} .lead{{max-width:760px;margin:0;color:var(--body);font-size:18px}}
    .contract{{display:flex;flex-wrap:wrap;gap:8px 18px;margin:25px 0 34px;padding-block:12px;border-block:1px solid var(--line);color:var(--muted);font:600 11px/1.4 var(--font-mono)}}
    .lab{{display:grid;grid-template-columns:minmax(0,.88fr) minmax(0,1.12fr);border:1px solid var(--line);background:var(--surface)}} .editor,.result{{padding:26px}} .result{{border-left:1px solid var(--line);background:#fbfaf6}}
    h2{{margin:0 0 6px;font-size:27px;font-weight:720;line-height:1.1}} .section-copy{{margin:0 0 22px;color:var(--muted);font-size:12px}}
    label{{display:grid;gap:6px;margin-top:14px;color:var(--body);font-weight:650}} label span{{color:var(--muted);font-size:11px;font-weight:500}} select{{width:100%;min-height:44px;padding:9px;border:1px solid var(--strong);border-radius:5px;color:var(--ink);background:var(--surface);font:inherit}}
    .actions{{display:flex;flex-wrap:wrap;gap:8px;margin-top:22px}} button{{min-height:42px;padding:8px 12px;border:1px solid var(--strong);border-radius:7px;color:var(--ink);background:var(--surface);font:inherit;font-size:13px;font-weight:600;line-height:1.2;cursor:pointer}} button.primary{{color:var(--ink);border-color:var(--action);background:var(--action)}} button.primary:hover{{border-color:var(--action-hover);background:var(--action-hover)}} button:hover{{border-color:var(--ink)}} button:focus-visible,select:focus-visible,a:focus-visible{{outline:3px solid var(--accent);outline-offset:3px}}
    .state{{display:inline-flex;padding:5px 8px;border-radius:999px;font-size:10px;font-weight:800;letter-spacing:.05em;text-transform:uppercase}} .state.blocked{{color:var(--red);background:var(--red-soft)}} .state.launch_ready{{color:var(--success);background:var(--success-soft)}}
    .issue-list{{display:grid;gap:8px;margin:18px 0}} .issue{{padding:11px 12px;border-left:3px solid var(--red);background:var(--red-soft)}} .issue strong{{display:block;margin-bottom:3px;font-size:12px}} .issue small{{color:var(--muted)}} .clean{{padding:16px;border-left:3px solid var(--success);background:var(--success-soft);color:var(--success)}}
    details{{margin-top:16px;border-top:1px solid var(--line)}} summary{{padding:13px 0;cursor:pointer;font-weight:650}} pre{{max-height:230px;margin:0;overflow:auto;padding:13px;color:var(--body);background:var(--soft);font:500 11px/1.55 var(--font-mono);white-space:pre-wrap}}
    .boundary{{margin-top:24px;padding:14px 16px;border-left:3px solid var(--accent);background:var(--brand-soft);color:var(--body)}} .links{{display:flex;flex-wrap:wrap;gap:14px;margin-top:22px;font-weight:700}} .creator-cta{{display:flex;align-items:center;justify-content:space-between;gap:24px;margin-top:30px;padding:20px 22px;border-radius:14px;color:#fff;background:var(--brand)}} .creator-cta p{{margin:0;color:rgba(255,255,255,.82)}} .creator-cta strong{{display:block;color:#fff;font-size:22px;font-weight:760;line-height:1.2}} .creator-cta a{{flex:0 0 auto;min-height:44px;display:inline-flex;align-items:center;padding:9px 12px;border:1px solid var(--action);border-radius:8px;color:var(--ink);background:var(--action);text-decoration:none;font-weight:750}}
    @media(max-width:760px){{main{{padding-top:30px}}.lab{{grid-template-columns:1fr}}.result{{border-left:0;border-top:1px solid var(--line)}}.editor,.result{{padding:20px}}.creator-cta{{align-items:flex-start;flex-direction:column}}}}
  </style>
</head>
<body>
  <header><nav aria-label="Product navigation"><a href="index.html">&larr; Creative Launch Workspace</a><a class="product-link" href="workspace.html?guided=1">Open the workspace</a></nav></header>
  <main>
    <div class="eyebrow">Interactive engineering proof</div><h1>Fix a blocked row. Revalidate without hand-waving.</h1>
    <p class="lead">Edit three bounded fields, then replay the exact scenarios generated by the Python validators. The browser does not invent or execute validation rules.</p>
    <div class="contract"><span>{contract}</span><span>rule pack {short_hash}&hellip;</span><span>8 Python golden scenarios</span><span>synthetic fixture only</span></div>
    <section class="lab">
      <div class="editor"><h2>1. Correct the mapping</h2><p class="section-copy">The initial row has three independent blockers.</p>
        <label>Placement <span>A story asset cannot run in feed.</span><select id="placement"><option value="feed">feed</option><option value="story">story</option></select></label>
        <label>Approval status <span>Only an approved creative can clear offline QA.</span><select id="approval_status"><option value="pending">pending</option><option value="approved">approved</option></select></label>
        <label>UTM campaign <span>The UTM must match the mapped campaign key.</span><select id="utm_campaign"><option value="camp_launch">camp_launch</option><option value="camp_sale">camp_sale</option></select></label>
        <div class="actions"><button type="button" class="primary" id="revalidate">Revalidate</button><button type="button" id="fix-all">Apply proposed fixes</button><button type="button" id="reset">Reset</button></div>
      </div>
      <section class="result" aria-live="polite"><h2>2. Inspect the result</h2><p class="section-copy">Only the selected golden scenario is replayed.</p><span class="state blocked" id="state">blocked</span><div class="issue-list" id="issues"></div><details><summary>Audit event preview</summary><pre id="audit"></pre></details></section>
    </section>
    <p class="boundary"><strong>Boundary:</strong> this lab is a deterministic browser rehearsal over eight committed scenarios. It does not persist a patch, call a model, contact Meta or authorize a launch.</p>
    <div class="links"><a href="evidence/interactive-rule-pack.json">Raw rule pack JSON</a><a href="workspace.html">Open the 100-row workspace</a><a href="https://github.com/mattyu-dev/creative-launch-workspace/blob/main/meta_importer/fix_lab.py">Inspect the generator</a></div>
    <aside class="creator-cta"><p><strong>Continue in the product</strong>Return to launch control or open the full review queue.</p><a href="index.html">Back to product</a></aside>
  </main>
  <script type="application/json" id="rule-pack">{embedded}</script>
  <script>
    const pack=JSON.parse(document.querySelector("#rule-pack").textContent); const fields=pack.editable_fields; const initial=pack.initial;
    const read=()=>Object.fromEntries(fields.map(name=>[name,document.querySelector(`#${{name}}`).value]));
    const key=values=>fields.map(name=>values[name]).join("|");
    function render(){{const values=read();const scenario=pack.scenarios[key(values)];const state=document.querySelector("#state");state.textContent=scenario.state.replace("_"," ");state.className=`state ${{scenario.state}}`;const issues=document.querySelector("#issues");issues.replaceChildren();if(!scenario.issues.length){{const clean=document.createElement("div");clean.className="clean";clean.innerHTML="<strong>All three blockers cleared.</strong><br>Python golden state: launch ready.";issues.append(clean)}}else scenario.issues.forEach(item=>{{const node=document.createElement("div");node.className="issue";const title=document.createElement("strong");title.textContent=item.code.replaceAll("_"," ");const copy=document.createElement("div");copy.textContent=item.message;const owner=document.createElement("small");owner.textContent=`Owner: ${{item.owner}}`;node.append(title,copy,owner);issues.append(node)}});const changed=fields.filter(name=>values[name]!==initial[name]);document.querySelector("#audit").textContent=JSON.stringify({{event:"synthetic_row_revalidated",contract_version:pack.contract_version,rule_pack_sha256:pack.rule_pack_sha256,creative_id:"cr_lab_001",changed_fields:changed,before:initial,after:values,result:{{state:scenario.state,issue_codes:scenario.issues.map(item=>item.code),idempotency_key:scenario.idempotency_key}},external_write:false}},null,2)}}
    document.querySelector("#revalidate").addEventListener("click",render);document.querySelector("#fix-all").addEventListener("click",()=>{{fields.forEach(name=>document.querySelector(`#${{name}}`).value=pack.target[name]);render()}});document.querySelector("#reset").addEventListener("click",()=>{{fields.forEach(name=>document.querySelector(`#${{name}}`).value=initial[name]);render()}});render();
  </script>
</body>
</html>"""
