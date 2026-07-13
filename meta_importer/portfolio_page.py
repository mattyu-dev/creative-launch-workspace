from __future__ import annotations


def render_portfolio_page() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <meta name="theme-color" content="#113e31">
  <meta name="description" content="An interactive case study of governed AI brief mapping, deterministic Meta creative launch QA and explicit human decisions.">
  <link rel="canonical" href="https://mattyu-dev.github.io/creative-launch-workspace/">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
  <link rel="me" href="https://www.linkedin.com/in/mathieu-petroni/">
  <link rel="me" href="https://github.com/mattyu-dev">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Mathieu Petroni · AI Automation portfolio">
  <meta property="og:title" content="I built a governed AI workflow for 100-row Meta creative launches">
  <meta property="og:description" content="AI-assisted brief mapping, deterministic launch QA, human review, evaluation design and explicit trust boundaries.">
  <meta property="og:url" content="https://mattyu-dev.github.io/creative-launch-workspace/">
  <meta property="og:image" content="https://mattyu-dev.github.io/creative-launch-workspace/assets/social-card-v1-6.png">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Creative Launch Workspace review queue with governed AI, deterministic QA and human decisions">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="I built a governed AI workflow for 100-row Meta creative launches">
  <meta name="twitter:description" content="AI proposes. Rules verify. A human decides.">
  <meta name="twitter:image" content="https://mattyu-dev.github.io/creative-launch-workspace/assets/social-card-v1-6.png">
  <meta name="twitter:image:alt" content="Creative Launch Workspace review queue with governed AI, deterministic QA and human decisions">
  <title>Creative Launch Workspace — Governed AI for Meta Ads | Mathieu Petroni</title>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "Person",
        "@id": "https://mattyu-dev.github.io/creative-launch-workspace/#mathieu",
        "name": "Mathieu Petroni",
        "jobTitle": "AI Automation Lead",
        "url": "https://www.linkedin.com/in/mathieu-petroni/",
        "sameAs": [
          "https://www.linkedin.com/in/mathieu-petroni/",
          "https://github.com/mattyu-dev"
        ]
      },
      {
        "@type": "SoftwareSourceCode",
        "@id": "https://mattyu-dev.github.io/creative-launch-workspace/#software",
        "name": "Creative Launch Workspace",
        "description": "Governed AI-assisted brief intake and deterministic launch QA for high-volume Meta Ads creative operations.",
        "codeRepository": "https://github.com/mattyu-dev/creative-launch-workspace",
        "programmingLanguage": ["Python", "JavaScript"],
        "license": "https://opensource.org/license/mit",
        "version": "1.6.0",
        "author": { "@id": "https://mattyu-dev.github.io/creative-launch-workspace/#mathieu" }
      },
      {
        "@type": "CreativeWork",
        "@id": "https://mattyu-dev.github.io/creative-launch-workspace/#case-study",
        "name": "Creative Launch Workspace — governed AI case study",
        "dateModified": "2026-07-13",
        "url": "https://mattyu-dev.github.io/creative-launch-workspace/",
        "image": "https://mattyu-dev.github.io/creative-launch-workspace/assets/social-card-v1-6.png",
        "author": { "@id": "https://mattyu-dev.github.io/creative-launch-workspace/#mathieu" },
        "about": { "@id": "https://mattyu-dev.github.io/creative-launch-workspace/#software" }
      }
    ]
  }
  </script>
  <style>
    :root {
      --canvas:#f7f5ef;--surface:#fffefa;--surface-soft:#f0eee6;--ink:#1c211e;
      --body:#454d47;--muted:#626963;--line:#d8d3c8;--line-strong:#aaa397;
      --forest:#113e31;--forest-dark:#0b2d24;--oxide:#a9472e;--sand:#f2e7d2;--mint:#cfe2d7;
      --sans:Inter,ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
      --serif:"Iowan Old Style",Charter,Georgia,serif;--mono:ui-monospace,SFMono-Regular,Menlo,monospace;
    }
    *{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;color:var(--ink);background:var(--canvas);font:400 15px/1.58 var(--sans);-webkit-font-smoothing:antialiased}a{color:inherit}a:focus-visible,button:focus-visible{outline:2px solid #275fb8;outline-offset:3px}.page{width:min(1240px,calc(100% - 48px));margin-inline:auto}.skip-link{position:fixed;left:16px;top:-80px;z-index:30;padding:10px 14px;border-radius:5px;color:#fff;background:var(--forest)}.skip-link:focus{top:12px}
    header{border-bottom:1px solid var(--line);background:rgba(247,245,239,.97)}nav{min-height:60px;display:flex;align-items:center;justify-content:space-between;gap:24px}.brand{display:flex;align-items:center;gap:10px;text-decoration:none;font-weight:700}.mark{width:22px;height:22px;position:relative;border-left:2px solid var(--oxide);border-top:2px solid var(--oxide)}.mark:after{content:"";width:7px;height:7px;position:absolute;right:1px;bottom:1px;background:var(--forest)}.nav-links,.section-links{display:flex;align-items:center;gap:17px}.nav-links{color:var(--body);font-size:13px}.nav-links a{text-underline-offset:4px}.section-links{gap:14px}.section-links a{color:var(--muted);text-decoration:none}.section-links a:hover{text-decoration:underline}.nav-links .nav-cta{padding:7px 10px;border:1px solid var(--forest);border-radius:4px;color:#fff;background:var(--forest);text-decoration:none}
    main{overflow:hidden}.eyebrow{color:var(--oxide);font-size:11px;font-weight:800;letter-spacing:.1em;text-transform:uppercase}.hero{padding:62px 0 46px}.hero-layout{display:grid;grid-template-columns:minmax(0,.93fr) minmax(440px,1.07fr);column-gap:56px;row-gap:0;align-items:center}.hero-copy{grid-column:1;grid-row:1}.hero h1{max-width:700px;margin:13px 0 20px;font:500 clamp(46px,5.65vw,75px)/.97 var(--serif);letter-spacing:-.047em}.lead{max-width:690px;margin:0;color:var(--body);font-size:clamp(17px,1.45vw,20px)}.actions{display:flex;flex-wrap:wrap;align-items:center;gap:12px 18px;margin-top:26px}.button{min-height:46px;display:inline-flex;align-items:center;justify-content:center;padding:10px 16px;border:1px solid var(--forest);border-radius:5px;color:#fff;background:var(--forest);text-decoration:none;font-weight:700}.button:hover{background:var(--forest-dark)}.button-light{color:var(--forest);background:transparent}.button-light:hover{color:#fff}.text-link{color:var(--forest);font-weight:750;text-underline-offset:4px}.hero-byline{grid-column:1;grid-row:2;display:flex;flex-wrap:wrap;gap:6px 12px;margin-top:20px;padding-top:15px;border-top:1px solid var(--line);color:var(--muted);font-size:12px}.hero-byline strong{color:var(--ink)}.hero-byline a{font-weight:700;text-underline-offset:3px}
    .hero-product{grid-column:2;grid-row:1 / span 2;position:relative;min-width:0}.product-frame{margin:0;overflow:hidden;border:1px solid var(--line-strong);border-radius:8px;background:var(--surface)}.product-window{height:445px;overflow:hidden;background:var(--surface-soft)}.product-window img{width:100%;height:100%;display:block;object-fit:cover;object-position:10% top}.product-frame figcaption{display:flex;justify-content:space-between;gap:16px;padding:10px 12px;border-top:1px solid var(--line);color:var(--muted);font-size:11px}.product-frame figcaption strong{color:var(--body)}.annotation{position:absolute;z-index:2;max-width:190px;padding:8px 10px;border:1px solid rgba(255,255,255,.55);border-radius:5px;color:#fff;background:var(--forest);font-size:11px;font-weight:700;line-height:1.35}.annotation b{display:block;color:#efb69f;font:700 11px/1 var(--mono)}.a1{left:-20px;top:16%}.a2{right:-17px;top:49%}.a3{left:13%;bottom:34px}
    .proof-strip{display:grid;grid-template-columns:repeat(3,1fr);margin-top:42px;border-block:1px solid var(--line)}.proof-item{padding:18px 20px 18px 0;border-right:1px solid var(--line)}.proof-item+.proof-item{padding-left:20px}.proof-item:last-child{border-right:0}.proof-item strong{display:block;font:500 35px/1 var(--serif)}.proof-item span{display:block;margin-top:7px;color:var(--muted);font-size:13px}.fixture-note{margin:9px 0 0;color:var(--muted);font-size:11px}
    .section{padding:74px 0;border-top:1px solid var(--line)}.section-head{display:grid;grid-template-columns:minmax(0,.72fr) minmax(300px,.28fr);gap:44px;align-items:end;margin-bottom:32px}.section-head h2{max-width:780px;margin:8px 0 0;font:500 clamp(34px,4.2vw,54px)/1.02 var(--serif);letter-spacing:-.038em}.section-head p{margin:0;color:var(--body)}h3{margin:0;font:500 24px/1.18 var(--serif)}
    .before-after{display:grid;grid-template-columns:1fr 1fr;border:1px solid var(--line);background:var(--surface)}.comparison{padding:26px}.comparison+.comparison{border-left:1px solid var(--line)}.comparison h3{margin-bottom:18px}.comparison.before h3{color:var(--oxide)}.comparison.after h3{color:var(--forest)}.comparison ul{margin:0;padding:0;list-style:none}.comparison li{display:grid;grid-template-columns:18px 1fr;gap:8px;padding:11px 0;border-top:1px solid var(--line);color:var(--body)}.comparison li:before{content:"×";color:var(--oxide);font-weight:800}.comparison.after li:before{content:"✓";color:var(--forest)}.purpose{margin:20px 0 0;padding:16px 18px;border-left:3px solid var(--forest);color:var(--body);background:var(--sand)}
    .guide-grid{display:grid;grid-template-columns:repeat(3,1fr);border-block:1px solid var(--line)}.guide-step{padding:22px 24px 22px 0;border-right:1px solid var(--line)}.guide-step+.guide-step{padding-left:24px}.guide-step:last-child{border-right:0}.guide-step b{color:var(--oxide);font:750 11px/1 var(--mono)}.guide-step h3{margin:10px 0 7px}.guide-step p{margin:0;color:var(--muted);font-size:13px}.guide-action{display:flex;align-items:center;justify-content:space-between;gap:24px;margin-top:24px;padding:20px 22px;color:#fff;background:var(--forest)}.guide-action p{margin:0;color:rgba(255,255,255,.75)}.guide-action .button{border-color:#fff;color:var(--forest);background:#fff}.guide-action .button:hover{color:#fff;background:transparent}
    .difference-grid{display:grid;grid-template-columns:repeat(3,1fr);border:1px solid var(--line);background:var(--surface)}.difference{min-height:190px;padding:23px;border-right:1px solid var(--line)}.difference:last-child{border-right:0}.difference b{display:block;margin-bottom:22px;color:var(--oxide);font:750 10px/1 var(--mono)}.difference h3{font-size:21px}.difference p{margin:7px 0 0;color:var(--muted);font-size:13px}
    .architecture{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(280px,.6fr);gap:28px;align-items:stretch}.diagram{padding:22px;border:1px solid var(--line);background:var(--surface)}.diagram svg{width:100%;height:auto;display:block}.diagram text{font-family:var(--sans);fill:var(--ink)}.diagram .mono-text{font-family:var(--mono);fill:var(--muted);font-size:10px}.diagram .node{fill:var(--canvas);stroke:var(--line-strong)}.diagram .ai{fill:var(--sand);stroke:var(--oxide)}.diagram .rules{fill:var(--mint);stroke:var(--forest)}.diagram .human{fill:var(--forest);stroke:var(--forest)}.diagram .human-text{fill:#fff}.diagram .boundary{stroke:var(--oxide);stroke-dasharray:5 5}.architecture-stack{display:none;margin:0;padding:0;list-style:none;border:1px solid var(--line);background:var(--surface)}.architecture-stack li{position:relative;padding:14px 16px;border-bottom:1px solid var(--line)}.architecture-stack li:last-child{border-bottom:0}.architecture-stack li:not(:last-child):after{content:"↓";position:absolute;left:50%;bottom:-13px;z-index:1;width:24px;height:24px;display:grid;place-items:center;color:var(--oxide);background:var(--canvas);font-weight:800;transform:translateX(-50%)}.architecture-stack strong{display:block}.architecture-stack span{display:block;margin-top:3px;color:var(--muted);font-size:12px}.boundary-list{border-block:1px solid var(--line)}.boundary-item{padding:16px 0;border-bottom:1px solid var(--line)}.boundary-item:last-child{border-bottom:0}.boundary-item b{color:var(--oxide);font:750 10px/1 var(--mono)}.boundary-item strong{display:block;margin:6px 0 3px}.boundary-item span{color:var(--muted);font-size:13px}
    .proof-band{padding:34px;color:#fff;background:var(--forest)}.proof-band .eyebrow{color:#e7b39f}.proof-band h2{max-width:760px;margin:8px 0 12px;font:500 clamp(34px,4vw,50px)/1.03 var(--serif);letter-spacing:-.035em}.proof-band>p{max-width:720px;margin:0;color:rgba(255,255,255,.72)}.proof-paths{display:grid;grid-template-columns:repeat(3,1fr);margin-top:28px;border-block:1px solid rgba(255,255,255,.22)}.proof-path{padding:19px 22px 19px 0;border-right:1px solid rgba(255,255,255,.22)}.proof-path+.proof-path{padding-left:22px}.proof-path:last-child{border-right:0}.proof-path span{display:block;margin-bottom:7px;color:rgba(255,255,255,.62);font:750 10px/1.3 var(--mono);letter-spacing:.06em;text-transform:uppercase}.proof-path a{color:#fff;font:600 19px/1.25 var(--serif);text-underline-offset:5px}.proof-path p{margin:7px 0 0;color:rgba(255,255,255,.76);font-size:13px}
    .evidence-grid{display:grid;grid-template-columns:repeat(4,1fr);border:1px solid var(--line);background:var(--surface)}.evidence{padding:22px;border-right:1px solid var(--line)}.evidence:last-child{border-right:0}.evidence strong{display:block;font:500 29px/1 var(--serif)}.evidence span{display:block;margin-top:8px;color:var(--muted);font-size:13px}.evidence-links{display:flex;flex-wrap:wrap;gap:12px 20px;margin-top:20px}.evidence-links a{color:var(--forest);font-weight:750;text-underline-offset:4px}
    .production-grid{display:grid;grid-template-columns:1fr 1fr;gap:28px}.production-card{padding:26px;border:1px solid var(--line);background:var(--surface)}.production-card h3{margin-bottom:14px}.production-card ol,.production-card ul{margin:0;padding-left:19px;color:var(--body)}.production-card li{padding:5px 0}.production-card.warning{background:var(--surface-soft)}.metrics-label{margin:30px 0 12px;color:var(--oxide);font:750 10px/1 var(--mono);letter-spacing:.06em;text-transform:uppercase}.metrics{display:grid;grid-template-columns:repeat(3,1fr);border:1px solid var(--line);background:var(--surface)}.metric-group{padding:20px;border-right:1px solid var(--line)}.metric-group:last-child{border-right:0}.metric-group strong{display:block;margin-bottom:7px;font:500 21px/1.15 var(--serif)}.metric-group span{display:block;color:var(--muted);font-size:12px}
    .about{display:grid;grid-template-columns:minmax(0,.9fr) minmax(340px,1.1fr);border:1px solid var(--line);background:var(--surface)}.about>div{padding:32px}.about>div+div{border-left:1px solid var(--line)}.about h2{margin:8px 0 14px;font:500 clamp(33px,3.6vw,46px)/1.04 var(--serif);letter-spacing:-.035em}.about p{color:var(--body)}.skills{display:flex;flex-wrap:wrap;gap:7px;margin-top:18px}.skills span{padding:6px 8px;border:1px solid var(--line);background:var(--surface-soft);font-size:11px;font-weight:650}.contribution-list{border-bottom:1px solid var(--line)}.contribution{display:grid;grid-template-columns:110px 1fr;gap:15px;padding:14px 0;border-top:1px solid var(--line)}.contribution b{color:var(--oxide);font:750 10px/1.5 var(--mono);text-transform:uppercase}.contribution span{color:var(--body);font-size:13px}
    .final-cta{padding:54px;color:#fff;background:var(--forest)}.final-cta h2{max-width:840px;margin:8px 0 14px;font:500 clamp(38px,5vw,60px)/1 var(--serif);letter-spacing:-.04em}.final-cta p{max-width:740px;margin:0;color:rgba(255,255,255,.73)}.final-cta .actions{margin-top:25px}.final-cta .button{border-color:#fff;color:var(--forest);background:#fff}.final-cta .button:hover{color:#fff;background:transparent}.final-cta .text-link{color:#fff}
    .final-cta .eyebrow{color:#e7b39f}
    footer{padding:26px 0 40px;border-top:1px solid var(--line);color:var(--muted);font-size:12px}.footer-row{display:flex;justify-content:space-between;gap:24px}.footer-row a{text-underline-offset:3px}
    @media(max-width:1080px){.section-links{display:none}}
    @media(max-width:980px){.hero-layout{grid-template-columns:1fr;gap:24px}.hero-copy,.hero-product,.hero-byline{grid-column:1;grid-row:auto}.hero-product{max-width:760px}.hero-byline{margin-top:0}.product-window{height:420px}.section-head{grid-template-columns:1fr;gap:14px}.architecture{grid-template-columns:1fr}.evidence-grid{grid-template-columns:1fr 1fr}.evidence:nth-child(2){border-right:0}.evidence:nth-child(-n+2){border-bottom:1px solid var(--line)}.about{grid-template-columns:1fr}.about>div+div{border-left:0;border-top:1px solid var(--line)}}
    @media(max-width:700px){.page{width:calc(100% - 28px)}.nav-links>a:not(.nav-cta){display:none}.hero{padding:40px 0 34px}.hero h1{font-size:43px}.product-window{height:310px}.annotation{display:none}.proof-strip,.guide-grid,.difference-grid,.proof-paths,.production-grid,.metrics{grid-template-columns:1fr}.proof-item,.proof-item+.proof-item,.guide-step,.guide-step+.guide-step,.proof-path,.proof-path+.proof-path{padding:15px 0;border-right:0;border-bottom:1px solid var(--line)}.proof-item:last-child,.guide-step:last-child,.proof-path:last-child{border-bottom:0}.before-after{grid-template-columns:1fr}.comparison+.comparison{border-left:0;border-top:1px solid var(--line)}.guide-action{align-items:flex-start;flex-direction:column}.difference{min-height:0;border-right:0;border-bottom:1px solid var(--line)}.difference:last-child{border-bottom:0}.diagram{display:none}.architecture-stack{display:block}.metric-group{border-right:0;border-bottom:1px solid var(--line)}.metric-group:last-child{border-bottom:0}.proof-band{margin-inline:-14px;padding:30px 20px}.proof-path,.proof-path+.proof-path{border-bottom-color:rgba(255,255,255,.22)}.evidence-grid{grid-template-columns:1fr}.evidence,.evidence:nth-child(2){border-right:0;border-bottom:1px solid var(--line)}.evidence:last-child{border-bottom:0}.about>div{padding:24px}.contribution{grid-template-columns:1fr;gap:4px}.final-cta{margin-inline:-14px;padding:42px 20px}.footer-row{flex-direction:column;gap:8px}}
    @media(max-width:430px){.hero h1{font-size:37px}.lead{font-size:16px}.actions{align-items:stretch;flex-direction:column}.actions .button,.actions .text-link{width:100%;text-align:center}.product-window{height:270px}.product-frame figcaption{display:block}}
    @media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
  </style>
</head>
<body>
  <a class="skip-link" href="#main">Skip to case study</a>
  <header>
    <nav class="page" aria-label="Primary navigation">
      <a class="brand" href="#top"><span class="mark" aria-hidden="true"></span>Creative Launch Workspace</a>
      <div class="nav-links"><div class="section-links" aria-label="Case study sections"><a href="#business">Business case</a><a href="#system">System</a><a href="#evidence">Evidence</a><a href="#about">About</a></div><a href="https://www.linkedin.com/in/mathieu-petroni/" rel="me external">LinkedIn</a><a class="nav-cta" href="workspace.html?guided=1">Try the demo</a></div>
    </nav>
  </header>
  <main id="main">
    <section class="page hero" id="top">
      <div class="hero-layout">
        <div class="hero-copy">
          <div class="eyebrow">AI automation case study · Paid media operations</div>
          <h1>Catch creative launch errors before they delay campaigns or waste spend.</h1>
          <p class="lead">I built a governed AI workflow that turns an ambiguous campaign brief and a 100-row Meta creative batch into a clear decision queue. Rows that pass the defined offline checks are separated from exceptions; blockers return to the right owner, and ambiguous cases stay with a human.</p>
          <div class="actions"><a class="button" href="workspace.html?guided=1">Try the guided demo</a><a class="text-link" href="#system">Explore architecture and evidence &rarr;</a></div>
        </div>
        <div class="hero-product">
          <figure class="product-frame">
            <div class="product-window"><a href="workspace.html?guided=1" aria-label="Open the guided interactive review workspace">
              <picture>
                <source media="(max-width:700px)" type="image/avif" srcset="assets/workspace-mobile.avif 390w" sizes="calc(100vw - 28px)">
                <source media="(max-width:700px)" type="image/webp" srcset="assets/workspace-mobile.webp 390w" sizes="calc(100vw - 28px)">
                <source type="image/avif" srcset="assets/workspace-desktop.avif 1440w" sizes="(max-width:980px) calc(100vw - 48px), 54vw">
                <source type="image/webp" srcset="assets/workspace-desktop.webp 1440w" sizes="(max-width:980px) calc(100vw - 48px), 54vw">
                <img src="assets/workspace-desktop.png" width="1440" height="1000" alt="Creative review queue showing an ambiguous row, its owner and available human decisions" decoding="async" fetchpriority="high">
              </picture>
            </a></div>
            <figcaption><strong>Interactive product · no signup</strong><span>Local-first reference implementation</span></figcaption>
          </figure>
          <span class="annotation a1"><b>DEFINED CHECKS</b> passing rows separated</span>
          <span class="annotation a2"><b>OWNED EXCEPTIONS</b> blocker + owner + fix</span>
          <span class="annotation a3"><b>HUMAN AUTHORITY</b> ambiguity stays visible</span>
        </div>
        <div class="hero-byline"><strong>Mathieu Petroni · AI Automation Lead</strong><span>AI automation, product systems and growth operations</span><a href="https://www.linkedin.com/in/mathieu-petroni/" rel="me external">LinkedIn</a><a href="https://github.com/mattyu-dev" rel="me external">GitHub</a></div>
      </div>
      <div class="proof-strip" aria-label="Reproducible fixture evidence">
        <div class="proof-item"><strong>100</strong><span>synthetic creatives in the reproducible fixture</span></div>
        <div class="proof-item"><strong>70</strong><span>seeded exceptions separated for routing or review</span></div>
        <div class="proof-item"><strong>0</strong><span>external writes available in this implementation</span></div>
      </div>
      <p class="fixture-note">Reproducible evidence from a 100-row synthetic fixture. These are test outcomes and implementation boundaries, not customer or business results.</p>
    </section>

    <section class="page section" id="business" aria-labelledby="problem-title">
      <div class="section-head"><div><div class="eyebrow">The operational problem</div><h2 id="problem-title">Launch risk accumulates in the handoff.</h2></div><p>Briefs, spreadsheets, chat approvals and trafficking checks fragment one launch decision across too many places.</p></div>
      <div class="before-after">
        <div class="comparison before"><h3>Without the workspace</h3><ul><li>QA is spread across briefs, sheets and chats.</li><li>Operators manually inspect every row.</li><li>Errors have unclear ownership.</li><li>Ambiguity is silently resolved or ignored.</li><li>Problems surface during trafficking.</li></ul></div>
        <div class="comparison after"><h3>With the workspace</h3><ul><li>One decision queue holds the launch state.</li><li>Rows that pass offline QA require no exception review.</li><li>Every issue names an owner and proposed fix.</li><li>Ambiguity requires an explicit human decision.</li><li>Problems surface before platform handoff.</li></ul></div>
      </div>
      <p class="purpose">I designed this workflow from the perspective of someone who has spent nine years across growth, performance marketing and the operational handoffs behind campaign launches. Its purpose is to reduce repetitive inspection, make exceptions visible and preserve human authority over ambiguous or high-risk decisions.</p>
    </section>

    <section class="page section" aria-labelledby="demo-title">
      <div class="section-head"><div><div class="eyebrow">Guided interactive demo</div><h2 id="demo-title">Make one local decision, then inspect the evidence.</h2></div><p>The guide uses the same local state and audit path as the full 100-row workspace.</p></div>
      <div class="guide-grid"><div class="guide-step"><b>01 · FIND</b><h3>See the ambiguous row.</h3><p>The guide selects a possible duplicate and names the issue, owner and proposed fix.</p></div><div class="guide-step"><b>02 · DECIDE</b><h3>Exercise human authority.</h3><p>Confirm for dry-run export, return for a fix or block from the dry-run export.</p></div><div class="guide-step"><b>03 · VERIFY</b><h3>Inspect the local audit event.</h3><p>See what changed, which reviewer role was recorded and the resulting authority boundary.</p></div></div>
      <div class="guide-action"><p><strong>Nothing to configure.</strong><br>Synthetic fixture, browser-local state and an explicit completion receipt.</p><a class="button" href="workspace.html?guided=1">Start the guided review &rarr;</a></div>
    </section>

    <section class="page section" aria-labelledby="spreadsheet-title">
      <div class="section-head"><div><div class="eyebrow">Why not another launch spreadsheet?</div><h2 id="spreadsheet-title">Rows are easy. Governed decisions are harder.</h2></div><p>A spreadsheet can store data. This reference architecture makes evidence, abstention, validation, ownership and human decisions explicit and testable.</p></div>
      <div class="difference-grid"><div class="difference"><b>01</b><h3>Governed intake</h3><p>Typed contracts, grounded evidence and explicit abstention replace unstructured assumptions.</p></div><div class="difference"><b>02</b><h3>Deterministic control</h3><p>Policy checks validate every row, fail closed and return exceptions to a named owner.</p></div><div class="difference"><b>03</b><h3>Auditable delivery</h3><p>Versioned evaluation, human decisions and review-only export keep the handoff inspectable.</p></div></div>
    </section>

    <section class="page section" id="system" aria-labelledby="system-title">
      <div class="section-head"><div><div class="eyebrow">How the system works</div><h2 id="system-title">AI proposes. Rules verify. A human decides.</h2></div><p>Each boundary has a deliberately narrower authority than the one before it.</p></div>
      <div class="architecture">
        <div class="diagram">
          <svg viewBox="0 0 720 530" role="img" aria-labelledby="diagram-title diagram-desc">
            <title id="diagram-title">Creative Launch Workspace trust-boundary architecture</title><desc id="diagram-desc">A campaign brief moves through an AI mapping proposal, schema and evidence policy, human field review, deterministic row validation, a decision queue and a review-only export.</desc>
            <defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#626963"/></marker></defs>
            <rect class="node" x="180" y="16" width="360" height="52" rx="5"/><text x="360" y="38" text-anchor="middle" font-weight="700">Campaign brief + creative manifest</text><text class="mono-text" x="360" y="55" text-anchor="middle">synthetic input in this release</text>
            <path d="M360 68V102" stroke="#626963" marker-end="url(#arrow)"/>
            <rect class="ai" x="180" y="106" width="360" height="62" rx="5"/><text x="360" y="132" text-anchor="middle" font-weight="700">AI mapping proposal</text><text class="mono-text" x="360" y="151" text-anchor="middle">typed value + evidence + abstention</text>
            <line class="boundary" x1="95" y1="186" x2="625" y2="186"/><text class="mono-text" x="102" y="180">MODEL BOUNDARY</text>
            <path d="M360 168V211" stroke="#626963" marker-end="url(#arrow)"/>
            <rect class="rules" x="180" y="215" width="360" height="62" rx="5"/><text x="360" y="241" text-anchor="middle" font-weight="700">Schema, evidence and risk policy</text><text class="mono-text" x="360" y="260" text-anchor="middle">invalid, unsupported or unsafe input fails closed</text>
            <path d="M360 277V311" stroke="#626963" marker-end="url(#arrow)"/>
            <rect class="human" x="180" y="315" width="360" height="58" rx="5"/><text class="human-text" x="360" y="340" text-anchor="middle" font-weight="700">Human field review</text><text class="human-text" x="360" y="358" text-anchor="middle" font-size="10">explicit accept, override or reject</text>
            <line class="boundary" x1="95" y1="391" x2="625" y2="391"/><text class="mono-text" x="102" y="385">HUMAN-AUTHORITY BOUNDARY</text>
            <path d="M360 373V416" stroke="#626963" marker-end="url(#arrow)"/>
            <rect class="rules" x="90" y="420" width="255" height="64" rx="5"/><text x="217" y="446" text-anchor="middle" font-weight="700">Deterministic row QA</text><text class="mono-text" x="217" y="465" text-anchor="middle">approval · placement · UTM · lineage</text>
            <path d="M345 452H393" stroke="#626963" marker-end="url(#arrow)"/>
            <rect class="node" x="397" y="420" width="235" height="64" rx="5"/><text x="514" y="446" text-anchor="middle" font-weight="700">Decision queue</text><text class="mono-text" x="514" y="465" text-anchor="middle">local audit state</text>
            <path d="M514 484V510" stroke="#626963" marker-end="url(#arrow)"/>
            <text class="mono-text" x="514" y="527" text-anchor="middle">REVIEW-ONLY EXPORT · NO META WRITE PATH</text>
          </svg>
        </div>
        <ol class="architecture-stack" aria-label="Creative Launch Workspace architecture on mobile">
          <li><strong>Campaign brief + creative manifest</strong><span>Synthetic input in this release</span></li>
          <li><strong>AI mapping proposal</strong><span>Typed value, evidence and abstention</span></li>
          <li><strong>Policy checks</strong><span>Schema, evidence and risk rules fail closed</span></li>
          <li><strong>Human field review</strong><span>Explicit accept, override or reject</span></li>
          <li><strong>Deterministic row QA</strong><span>Approval, placement, UTM and lineage checks</span></li>
          <li><strong>Decision queue</strong><span>Browser-local review and audit state</span></li>
          <li><strong>Review-only export</strong><span>No external mutation authority</span></li>
        </ol>
        <div class="boundary-list"><div class="boundary-item"><b>MODEL</b><strong>Proposal only</strong><span>The provider cannot validate, approve or publish.</span></div><div class="boundary-item"><b>POLICY</b><strong>Deterministic authority</strong><span>Schema, evidence, risk and row checks remain code-controlled.</span></div><div class="boundary-item"><b>HUMAN</b><strong>Explicit decision</strong><span>Ambiguous fields and rows wait for an explicit reviewer-role action.</span></div><div class="boundary-item"><b>PLATFORM</b><strong>No mutation surface</strong><span>No API call, credential, upload, budget change or live publish path exists.</span></div></div>
      </div>
    </section>

    <section class="page proof-band" aria-labelledby="proof-title">
      <div class="eyebrow">Explore the project</div><h2 id="proof-title">Choose the evidence you want to challenge.</h2><p>No signup, account, token or setup. Each path opens a real, bounded artifact.</p>
      <div class="proof-paths"><div class="proof-path"><span>Experience the workflow</span><a href="workspace.html?guided=1">Review a human decision &rarr;</a><p>Use the guided path, then explore the full 100-row queue.</p></div><div class="proof-path"><span>Inspect the system</span><a href="fix-lab.html">Fix and revalidate a row &rarr;</a><p>Replay Python-generated golden scenarios and inspect the audit event.</p></div><div class="proof-path"><span>Review engineering evidence</span><a href="https://github.com/mattyu-dev/creative-launch-workspace">Open the source &rarr;</a><p>Architecture, evaluations, tests, security assumptions and reproducible artifacts.</p></div></div>
    </section>

    <section class="page section" id="evidence" aria-labelledby="evidence-title">
      <div class="section-head"><div><div class="eyebrow">Engineering evidence</div><h2 id="evidence-title">Inspect the evidence, not the promise.</h2></div><p>The deterministic baseline is tested and reproducible. Live model quality is not claimed.</p></div>
      <div class="evidence-grid"><div class="evidence"><strong>36 + 12</strong><span>deterministic contract cases plus cases reserved for repeated live-provider evaluation</span></div><div class="evidence"><strong>50+</strong><span>unit, negative-path and integration tests</span></div><div class="evidence"><strong>7</strong><span>tested viewport widths with real interaction QA</span></div><div class="evidence"><strong>100/100</strong><span>in committed desktop and mobile Lighthouse accessibility runs</span></div></div>
      <div class="evidence-links"><a href="brief-evidence.html">See how the AI is governed</a><a href="https://github.com/mattyu-dev/creative-launch-workspace/blob/main/docs/architecture/system.md">Architecture</a><a href="https://github.com/mattyu-dev/creative-launch-workspace/blob/main/docs/ai/evaluation.md">Evaluation protocol</a><a href="https://github.com/mattyu-dev/creative-launch-workspace/blob/main/docs/security/threat_model.md">Threat model</a><a href="https://github.com/mattyu-dev/creative-launch-workspace/actions">CI evidence</a></div>
    </section>

    <section class="page section" id="production" aria-labelledby="production-title">
      <div class="section-head"><div><div class="eyebrow">Production path</div><h2 id="production-title">A reference implementation with a serious next-proof plan.</h2></div><p>These boundaries define the order in which production risk should be reduced.</p></div>
      <div class="production-grid"><div class="production-card warning"><h3>What this does not prove</h3><ul><li>Production Meta API compatibility</li><li>Customer-data and tenant isolation</li><li>Representative live-model quality</li><li>Measured operator or business impact</li></ul></div><div class="production-card"><h3>What I would validate next</h3><ol><li>Read-only Meta sandbox compatibility</li><li>Authentication, tenancy and secrets handling</li><li>Privacy, redaction and retention</li><li>Persistent concurrent review and replay</li><li>Representative model evaluation</li><li>Gradual permissions with approval gates</li></ol></div></div>
      <div class="metrics-label">Proposed production pilot metrics · not measured results</div><div class="metrics"><div class="metric-group"><strong>Efficiency</strong><span>Operator minutes per 100 creatives · time to readiness · rework loops · rows separated from exception review</span></div><div class="metric-group"><strong>Quality</strong><span>Defects found before trafficking · blocker precision and false negatives · correct-owner routing</span></div><div class="metric-group"><strong>Governance</strong><span>Human overrides · model abstentions · audit completeness</span></div></div>
    </section>

    <section class="page section" id="about" aria-labelledby="about-title">
      <div class="about"><div><div class="eyebrow">About Mathieu</div><h2 id="about-title">I build governed AI workflows for operational teams.</h2><p>I designed and implemented this project end to end, combining nine years of growth and performance marketing experience with product thinking, automation and data systems.</p><div class="skills"><span>Python</span><span>JavaScript</span><span>Structured Outputs</span><span>AI evaluations</span><span>Human-in-the-loop systems</span><span>Threat modelling</span><span>CI/CD</span><span>Paid-media operations</span></div><div class="actions"><a class="button" href="https://www.linkedin.com/in/mathieu-petroni/" rel="me external">Message me on LinkedIn</a><a class="text-link" href="https://github.com/mattyu-dev" rel="me external">Explore my GitHub &rarr;</a></div></div><div><div class="eyebrow">My contribution</div><div class="contribution-list"><div class="contribution"><b>Product</b><span>Problem framing, workflow design and business-to-technical translation</span></div><div class="contribution"><b>AI system</b><span>Provider isolation, grounded proposals, abstention and evaluation design</span></div><div class="contribution"><b>Engineering</b><span>Typed contracts, deterministic validators, local persistence and audit state</span></div><div class="contribution"><b>Trust</b><span>Threat model, fail-closed policy and explicit platform boundaries</span></div><div class="contribution"><b>Quality</b><span>Responsive UX, accessibility, browser QA, CI and reproducible artifacts</span></div></div></div></div>
    </section>

    <section class="page final-cta" aria-labelledby="contact-title"><div class="eyebrow">Let’s talk</div><h2 id="contact-title">Building an AI workflow where trust matters?</h2><p>I would be happy to discuss the product decisions, architecture, evaluation strategy or how this approach could apply to another operational workflow.</p><div class="actions"><a class="button" href="https://www.linkedin.com/in/mathieu-petroni/" rel="me external">Message me on LinkedIn</a><a class="text-link" href="https://github.com/mattyu-dev/creative-launch-workspace">Explore the source &rarr;</a></div></section>
  </main>
  <footer><div class="page footer-row"><span>Creative Launch Workspace · v1.6.0 · Updated <time datetime="2026-07-13">13 July 2026</time></span><span>MIT licensed · Synthetic reference implementation · <a href="https://github.com/mattyu-dev/creative-launch-workspace">Source</a></span></div></footer>
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
    :root{--canvas:#f7f5ef;--ink:#1c211e;--body:#48504b;--muted:#666d67;--line:#d8d3c8;--forest:#113e31;--oxide:#a9472e;--serif:"Iowan Old Style",Charter,Georgia,serif}
    *{box-sizing:border-box}body{width:1200px;height:630px;margin:0;overflow:hidden;color:var(--ink);background:var(--canvas);font:400 16px/1.42 Inter,ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}main{height:100%;display:grid;grid-template-columns:55% 45%}section{min-width:0}.copy{display:flex;flex-direction:column;padding:42px 42px 36px 58px}.brand{display:flex;align-items:center;gap:10px;font-weight:750}.mark{width:23px;height:23px;position:relative;border-left:2px solid var(--oxide);border-top:2px solid var(--oxide)}.mark:after{content:"";width:7px;height:7px;position:absolute;right:1px;bottom:1px;background:var(--forest)}.hero{margin:auto 0}.eyebrow{color:var(--oxide);font-size:12px;font-weight:800;letter-spacing:.1em;text-transform:uppercase}h1{max-width:610px;margin:12px 0 15px;font:500 54px/.96 var(--serif);letter-spacing:-.045em}p{max-width:590px;margin:0;color:var(--body);font-size:18px}.proof{display:flex;gap:22px;margin-top:25px;padding-top:15px;border-top:1px solid var(--line)}.proof span{color:var(--muted);font-size:13px}.proof b{margin-right:5px;color:var(--ink);font:500 27px/1 var(--serif)}footer{display:flex;justify-content:space-between;gap:18px;color:var(--muted);font-size:13px}.visual{position:relative;overflow:hidden;border-left:1px solid var(--line);background:var(--forest)}.visual img{width:830px;height:630px;display:block;object-fit:cover;object-position:7% top;opacity:.93}.visual:after{content:"AI proposes · Rules verify · A human decides";position:absolute;left:26px;right:26px;bottom:28px;padding:13px 15px;border:1px solid rgba(255,255,255,.28);color:#fff;background:rgba(17,62,49,.94);font-size:15px;font-weight:700}.badge{position:absolute;top:26px;right:24px;padding:7px 9px;color:var(--forest);background:#fff;font-size:11px;font-weight:800;letter-spacing:.04em;text-transform:uppercase}
  </style>
</head>
<body><main><section class="copy"><div class="brand"><span class="mark"></span>Creative Launch Workspace</div><div class="hero"><div class="eyebrow">AI automation case study · Paid media operations</div><h1>Catch launch errors before Ads Manager.</h1><p>A governed workflow for 100-row Meta creative launches.</p><div class="proof"><span><b>100</b> fixture rows</span><span><b>70</b> seeded exceptions</span><span><b>0</b> external writes</span></div></div><footer><strong>Mathieu Petroni</strong><span>AI Automation · Product Systems</span></footer></section><section class="visual"><img src="assets/workspace-desktop.png" alt=""><span class="badge">Interactive case study</span></section></main></body>
</html>
"""
