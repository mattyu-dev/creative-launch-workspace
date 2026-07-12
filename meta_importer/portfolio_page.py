from __future__ import annotations


def render_portfolio_page() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <meta name="description" content="A governed AI automation case study for catching approval, mapping, destination and placement errors before a large Meta creative launch reaches Ads Manager.">
  <link rel="canonical" href="https://mattyu-dev.github.io/creative-launch-workspace/">
  <meta property="og:type" content="website">
  <meta property="og:title" content="Creative Launch Workspace · AI automation case study">
  <meta property="og:description" content="AI proposes the mapping. Deterministic rules verify every row. A person decides every ambiguous case.">
  <meta property="og:url" content="https://mattyu-dev.github.io/creative-launch-workspace/">
  <meta property="og:image" content="https://mattyu-dev.github.io/creative-launch-workspace/assets/social-card.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Creative Launch Workspace review queue and governed AI workflow">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Creative Launch Workspace · AI automation case study">
  <meta name="twitter:description" content="Catch launch errors before they reach Ads Manager.">
  <meta name="twitter:image" content="https://mattyu-dev.github.io/creative-launch-workspace/assets/social-card.png">
  <title>Creative Launch Workspace · AI automation case study</title>
  <style>
    :root {
      --canvas:#f7f5ef; --surface:#fffefa; --surface-soft:#f1efe8;
      --ink:#1c211e; --body:#48504b; --muted:#6e756f;
      --line:#d8d3c8; --line-strong:#b8b2a6; --forest:#113e31;
      --forest-dark:#0b2d24; --oxide:#a9472e; --sand:#f2e7d2; --mint:#cfe2d7;
      --font-sans:Inter,ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
      --font-serif:"Iowan Old Style",Charter,Georgia,serif;
      --font-mono:ui-monospace,SFMono-Regular,Menlo,monospace;
    }
    * { box-sizing:border-box; }
    html { scroll-behavior:smooth; }
    body { margin:0; color:var(--ink); background:var(--canvas); font:400 15px/1.55 var(--font-sans); -webkit-font-smoothing:antialiased; }
    a { color:inherit; }
    a:focus-visible { outline:2px solid #275fb8; outline-offset:3px; }
    .page { width:min(1240px,calc(100% - 48px)); margin-inline:auto; }
    header { border-bottom:1px solid var(--line); background:rgba(247,245,239,.96); }
    nav { min-height:58px; display:flex; align-items:center; justify-content:space-between; gap:24px; }
    .brand { display:flex; align-items:center; gap:10px; text-decoration:none; font-weight:650; }
    .mark { width:22px; height:22px; position:relative; border-left:2px solid var(--oxide); border-top:2px solid var(--oxide); }
    .mark::after { content:""; width:7px; height:7px; position:absolute; right:1px; bottom:1px; background:var(--forest); }
    .nav-links { display:flex; align-items:center; gap:18px; color:var(--body); font-size:13px; }
    .nav-links a { text-underline-offset:3px; }
    .nav-links span { color:var(--muted); }
    main { overflow:hidden; }
    .hero { padding:58px 0 34px; }
    .eyebrow { color:var(--oxide); font-size:11px; font-weight:750; letter-spacing:.11em; text-transform:uppercase; }
    h1 { max-width:1020px; margin:13px 0 20px; font:500 clamp(45px,6.6vw,82px)/.96 var(--font-serif); letter-spacing:-.048em; }
    .hero-grid { display:grid; grid-template-columns:minmax(0,1.5fr) minmax(260px,.62fr); gap:42px; align-items:end; }
    .lead { max-width:760px; margin:0; color:var(--body); font-size:clamp(17px,1.7vw,20px); }
    .hero-side { padding-left:22px; border-left:1px solid var(--line-strong); }
    .hero-side strong { display:block; margin-bottom:8px; font:500 21px/1.25 var(--font-serif); }
    .hero-side p { margin:0 0 18px; color:var(--muted); font-size:13px; }
    .actions { display:flex; flex-wrap:wrap; align-items:center; gap:12px 18px; margin-top:26px; }
    .button { min-height:44px; display:inline-flex; align-items:center; justify-content:center; padding:10px 15px; border:1px solid var(--forest); border-radius:5px; color:#fff; background:var(--forest); text-decoration:none; font-weight:650; }
    .button:hover { background:var(--forest-dark); }
    .text-link { color:var(--forest); font-weight:700; text-underline-offset:4px; }
    .boundary-line { margin-top:16px; color:var(--muted); font:600 11px/1.4 var(--font-mono); }
    .proof-strip { display:grid; grid-template-columns:repeat(3,1fr); margin-top:35px; border-block:1px solid var(--line); }
    .proof-item { padding:18px 20px 18px 0; border-right:1px solid var(--line); }
    .proof-item + .proof-item { padding-left:20px; }
    .proof-item:last-child { border-right:0; }
    .proof-item strong { display:block; font:500 35px/1 var(--font-serif); }
    .proof-item span { display:block; max-width:260px; margin-top:7px; color:var(--muted); font-size:12px; }
    .fixture-note { margin:9px 0 0; color:var(--muted); font-size:11px; }
    .product-figure { margin:30px 0 0; border:1px solid var(--line-strong); border-radius:7px; overflow:hidden; background:var(--surface); }
    .product-figure img { display:block; width:100%; height:auto; }
    .product-figure figcaption { display:flex; justify-content:space-between; gap:20px; padding:11px 14px; border-top:1px solid var(--line); color:var(--muted); font-size:11px; }
    .section { padding:74px 0; border-top:1px solid var(--line); }
    .section-grid { display:grid; grid-template-columns:repeat(12,minmax(0,1fr)); column-gap:24px; }
    .section-copy { grid-column:1 / span 5; }
    .section-detail { grid-column:7 / -1; }
    h2 { margin:8px 0 15px; font:500 clamp(33px,4vw,52px)/1.02 var(--font-serif); letter-spacing:-.035em; }
    .section-copy p { max-width:520px; color:var(--body); }
    .steps { border-bottom:1px solid var(--line); }
    .step { display:grid; grid-template-columns:38px minmax(0,1fr); gap:14px; padding:15px 0; border-top:1px solid var(--line); }
    .step b { color:var(--oxide); font:700 11px/1.4 var(--font-mono); }
    .step strong { display:block; margin-bottom:2px; font-weight:650; }
    .step span { color:var(--muted); font-size:12px; }
    .lab-band { padding:30px; color:#fff; background:var(--forest); }
    .lab-grid { display:grid; grid-template-columns:minmax(0,1.3fr) minmax(280px,.7fr); gap:36px; align-items:end; }
    .lab-band .eyebrow { color:#e7b39f; }
    .lab-band h2 { max-width:760px; margin-bottom:12px; }
    .lab-band p { max-width:720px; margin:0; color:rgba(255,255,255,.72); }
    .lab-band .button { border-color:#fff; color:var(--forest); background:#fff; }
    .lab-band .button:hover { color:#fff; background:transparent; }
    .ownership { display:grid; grid-template-columns:1fr 1fr; border:1px solid var(--line); background:var(--surface); }
    .ownership > div { padding:28px; }
    .ownership > div + div { border-left:1px solid var(--line); }
    .ownership h3 { margin:5px 0 10px; font:500 27px/1.12 var(--font-serif); }
    .ownership p { color:var(--body); }
    .link-row { display:flex; flex-wrap:wrap; gap:12px 18px; margin-top:20px; }
    .link-row a { color:var(--forest); font-weight:700; text-underline-offset:4px; }
    .scope { margin-top:24px; display:grid; grid-template-columns:1fr 1fr; border-block:1px solid var(--line); }
    .scope div { padding:20px 24px 20px 0; }
    .scope div + div { padding-left:24px; border-left:1px solid var(--line); }
    .scope strong { display:block; margin-bottom:6px; }
    .scope p { margin:0; color:var(--muted); font-size:13px; }
    footer { padding:28px 0 40px; border-top:1px solid var(--line); color:var(--muted); font-size:12px; }
    @media(max-width:800px) {
      .page { width:calc(100% - 28px); }
      .nav-links span { display:none; }
      .hero { padding-top:40px; }
      .hero-grid,.lab-grid { grid-template-columns:1fr; }
      .hero-side { padding:18px 0 0; border-left:0; border-top:1px solid var(--line); }
      .proof-strip { grid-template-columns:1fr; }
      .proof-item,.proof-item + .proof-item { padding:14px 0; border-right:0; border-bottom:1px solid var(--line); }
      .proof-item:last-child { border-bottom:0; }
      .product-figure img { width:100%; max-width:100%; transform:none; }
      .product-figure figcaption { display:block; }
      .section { padding:52px 0; }
      .section-copy,.section-detail { grid-column:1 / -1; }
      .section-detail { margin-top:28px; }
      .lab-band { margin-inline:-14px; padding:28px 20px; }
      .ownership,.scope { grid-template-columns:1fr; }
      .ownership > div + div,.scope div + div { border-left:0; border-top:1px solid var(--line); }
      .scope div,.scope div + div { padding:18px 0; }
    }
    @media(max-width:430px) {
      .brand { font-size:13px; }
      .nav-links { gap:10px; font-size:12px; }
      h1 { font-size:43px; }
      .actions { align-items:stretch; flex-direction:column; }
      .actions .button,.actions .text-link { width:100%; text-align:center; }
    }
    @media(prefers-reduced-motion:reduce) { html { scroll-behavior:auto; } }
  </style>
</head>
<body>
  <header>
    <nav class="page" aria-label="Primary navigation">
      <a class="brand" href="#top"><span class="mark" aria-hidden="true"></span>Creative Launch Workspace</a>
      <div class="nav-links"><span>Built by Mathieu Petroni</span><a href="https://github.com/mattyu-dev/creative-launch-workspace">GitHub</a></div>
    </nav>
  </header>
  <main id="top">
    <section class="page hero">
      <div class="eyebrow">AI automation case study · Creative operations</div>
      <h1>Catch launch errors before they reach Ads Manager.</h1>
      <div class="hero-grid">
        <div>
          <p class="lead">Creative Launch Workspace turns a campaign brief and a 100-row creative batch into a review queue. AI can propose the mapping, deterministic rules verify every row, and a person decides every ambiguous case.</p>
          <div class="actions"><a class="button" href="workspace.html">Try the 60-second demo</a><a class="text-link" href="brief-evidence.html">Inspect governed intake evidence &rarr;</a></div>
          <div class="boundary-line">Synthetic data · Local browser state · No Meta API calls</div>
        </div>
        <aside class="hero-side"><strong>Model proposes.<br>Policy checks.<br>Human decides.</strong><p>Nothing on this site can publish, change spend, load credentials or write to an external system.</p></aside>
      </div>
      <div class="proof-strip" aria-label="Reproducible fixture evidence">
        <div class="proof-item"><strong>100</strong><span>creative rows in a multi-campaign synthetic stress test</span></div>
        <div class="proof-item"><strong>70</strong><span>seeded launch issues surfaced and routed to an owner</span></div>
        <div class="proof-item"><strong>10</strong><span>ambiguous cases held for a human decision</span></div>
      </div>
      <p class="fixture-note">Fixture evidence, not customer, production or business results.</p>
      <figure class="product-figure"><a href="workspace.html"><picture><source media="(max-width:800px)" srcset="assets/workspace-mobile.png"><img src="assets/workspace-desktop.png" width="1440" height="1000" alt="Interactive creative review queue with a selected decision panel"></picture></a><figcaption><span>Task-first review queue · 100-row synthetic fixture</span><span>Click the image to use the workspace</span></figcaption></figure>
    </section>

    <section class="page section">
      <div class="section-grid">
        <div class="section-copy"><div class="eyebrow">System spine</div><h2>Automation with explicit authority.</h2><p>The provider proposes. Policy code checks. The operator decides. The final export remains non-executable.</p></div>
        <div class="section-detail steps">
          <div class="step"><b>01</b><div><strong>Bounded brief proposal</strong><span>Typed fields carry source evidence or abstain.</span></div></div>
          <div class="step"><b>02</b><div><strong>Schema, evidence and risk policy</strong><span>Contradictions, unsafe inputs and unsupported values fail closed.</span></div></div>
          <div class="step"><b>03</b><div><strong>Deterministic launch QA</strong><span>Approval, destination, placement, UTM and lineage checks route concrete issues.</span></div></div>
          <div class="step"><b>04</b><div><strong>Human review and local audit</strong><span>Ambiguous rows wait for an accountable decision; no platform mutation exists.</span></div></div>
        </div>
      </div>
    </section>

    <section class="page lab-band" aria-labelledby="lab-title">
      <div class="lab-grid"><div><div class="eyebrow">Interactive engineering proof</div><h2 id="lab-title">Fix a blocked row. Re-run the exact golden scenarios.</h2><p>A browser rehearsal backed by a versioned synthetic rule pack and cross-checked against the Python validators in CI.</p></div><div><a class="button" href="fix-lab.html">Open Fix &amp; Revalidate Lab</a></div></div>
    </section>

    <section class="page section">
      <div class="ownership">
        <div><div class="eyebrow">Ownership</div><h3>Designed and built end to end by Mathieu Petroni.</h3><p>Product framing, AI orchestration, evaluation design, trust boundaries, deterministic validation and responsive workflow UX.</p><div class="link-row"><a href="https://github.com/mattyu-dev/creative-launch-workspace">View source</a><a href="https://github.com/mattyu-dev/creative-launch-workspace/blob/main/docs/architecture/system.md">Architecture</a><a href="https://github.com/mattyu-dev/creative-launch-workspace/blob/main/docs/ai/evaluation.md">Evaluation protocol</a></div></div>
        <div><div class="eyebrow">Reproducible proof</div><h3>Inspect the evidence, not the promise.</h3><p>48 versioned eval cases, 50+ tests, browser QA across seven widths, and committed accessibility reports. The baseline is deterministic; live model quality is not claimed.</p><div class="link-row"><a href="brief-evidence.html">Governed intake evidence</a><a href="https://github.com/mattyu-dev/creative-launch-workspace/blob/main/docs/security/threat_model.md">Threat model</a></div></div>
      </div>
      <div class="scope">
        <div><strong>What this proves</strong><p>A governed, testable workflow for turning ambiguous campaign inputs into inspectable decisions.</p></div>
        <div><strong>What it does not prove</strong><p>Production Meta compatibility, customer-data safety, model quality or business impact. This release is synthetic, local-first and non-executable.</p></div>
      </div>
    </section>
  </main>
  <footer><div class="page">Creative Launch Workspace · MIT licensed · Synthetic reference implementation</div></footer>
</body>
</html>
"""


def render_social_card_page() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=1200, initial-scale=1">
  <title>Creative Launch Workspace social card</title>
  <style>
    :root { --canvas:#f7f5ef;--ink:#1c211e;--body:#48504b;--muted:#6e756f;--line:#d8d3c8;--forest:#113e31;--oxide:#a9472e;--serif:"Iowan Old Style",Charter,Georgia,serif; }
    * { box-sizing:border-box; }
    body { width:1200px; height:630px; margin:0; overflow:hidden; color:var(--ink); background:var(--canvas); font:400 16px/1.45 Inter,ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }
    main { height:100%; display:grid; grid-template-rows:auto 1fr auto; padding:46px 64px 42px; }
    header { display:flex; align-items:center; justify-content:space-between; padding-bottom:20px; border-bottom:1px solid var(--line); font-size:15px; font-weight:700; }
    .brand { display:flex; align-items:center; gap:11px; }
    .mark { width:24px; height:24px; position:relative; border-left:2px solid var(--oxide); border-top:2px solid var(--oxide); }
    .mark::after { content:""; width:8px; height:8px; position:absolute; right:1px; bottom:1px; background:var(--forest); }
    header span:last-child { color:var(--muted); font-weight:500; }
    .hero { align-self:center; padding:24px 0 18px; }
    .eyebrow { color:var(--oxide); font-size:12px; font-weight:800; letter-spacing:.11em; text-transform:uppercase; }
    h1 { max-width:990px; margin:9px 0 13px; font:500 72px/.94 var(--serif); letter-spacing:-.045em; }
    p { max-width:900px; margin:0; color:var(--body); font-size:20px; }
    .proof { display:grid; grid-template-columns:repeat(3,1fr); border-block:1px solid var(--line); }
    .proof div { padding:13px 20px 12px 0; border-right:1px solid var(--line); }
    .proof div + div { padding-left:20px; } .proof div:last-child { border-right:0; }
    .proof strong { display:inline-block; margin-right:9px; font:500 32px/1 var(--serif); }
    .proof span { color:var(--muted); font-size:13px; }
  </style>
</head>
<body><main>
  <header><span class="brand"><span class="mark"></span>Creative Launch Workspace</span><span>Built by Mathieu Petroni</span></header>
  <section class="hero"><div class="eyebrow">AI automation case study · Creative operations</div><h1>Catch launch errors before they reach Ads Manager.</h1><p>AI proposes the mapping. Deterministic rules verify every row. A person decides every ambiguous case.</p></section>
  <section class="proof"><div><strong>100</strong><span>synthetic creatives</span></div><div><strong>70</strong><span>seeded issues routed</span></div><div><strong>0</strong><span>external writes</span></div></section>
</main></body>
</html>
"""
