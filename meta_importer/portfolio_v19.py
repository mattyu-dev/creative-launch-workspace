from __future__ import annotations

VERSION = "1.9.0"
UPDATED_DATE = "2026-07-14"
UPDATED_LABEL = "14 July 2026"
SOCIAL_CARD = "social-card-v1-9.png"


def _shared_styles() -> str:
    return """
    :root {
      color-scheme:dark;
      --background:#090c0b;--foreground:#f2f7f4;
      --card:#101513;--card-foreground:#f2f7f4;--surface:#151c19;--surface-strong:#1b2420;
      --muted:#1b2420;--muted-foreground:#8e9b95;--secondary-foreground:#c6d0cb;
      --primary:#7bd9b0;--primary-hover:#9be8c6;--primary-pressed:#64be98;--primary-foreground:#07120d;
      --border:#24302b;--border-strong:#35443e;--ring:#9be8c6;
      --font-sans:Inter,"SF Pro Display",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
      --font-mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;
      --radius-sm:8px;--radius-md:12px;--radius-lg:16px;
      --ease-out:cubic-bezier(.23,1,.32,1);
    }
    *{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;color:var(--foreground);background:var(--background);font:400 16px/1.6 var(--font-sans);-webkit-font-smoothing:antialiased}body:before{content:"";position:fixed;inset:0;pointer-events:none;background-image:linear-gradient(rgba(255,255,255,.018) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.018) 1px,transparent 1px);background-size:64px 64px;mask-image:linear-gradient(to bottom,black,transparent 42%);opacity:.28}h1,h2,h3,p,a,strong,span,dd,dt,summary{overflow-wrap:anywhere}a{color:inherit}a:focus-visible,summary:focus-visible{outline:2px solid var(--ring);outline-offset:4px}.container{width:min(1200px,calc(100% - 48px));margin-inline:auto}.reading{max-width:720px}.skip-link{position:fixed;left:16px;top:-80px;z-index:80;min-height:44px;display:flex;align-items:center;padding:8px 14px;border-radius:var(--radius-sm);color:var(--primary-foreground);background:var(--primary);font-weight:600}.skip-link:focus{top:14px}
    .site-header{position:sticky;top:0;z-index:50;border-bottom:1px solid rgba(36,48,43,.82);background:rgba(9,12,11,.82);backdrop-filter:blur(18px) saturate(145%)}.site-nav{min-height:64px;display:flex;align-items:center;justify-content:space-between;gap:24px}.brand{min-height:44px;display:inline-flex;align-items:center;gap:11px;text-decoration:none}.brand-mark{width:29px;height:29px;display:grid;place-items:center;border:1px solid var(--border-strong);border-radius:7px;color:var(--primary);background:var(--card);font:600 10px/1 var(--font-mono);letter-spacing:-.03em}.brand-copy{display:grid;line-height:1.15}.brand-copy strong{font-size:13px;font-weight:600}.brand-copy span{margin-top:3px;color:var(--muted-foreground);font-size:11px}.nav-links{display:flex;align-items:center;gap:6px}.nav-links>a{min-height:44px;display:inline-flex;align-items:center;padding:0 10px;border-radius:var(--radius-sm);color:var(--secondary-foreground);font-size:13px;text-decoration:none}.nav-links .button{padding-inline:14px}.button{min-height:44px;display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:9px 15px;border:1px solid transparent;border-radius:var(--radius-sm);font-size:14px;font-weight:600;line-height:1.2;text-decoration:none;transition:transform 140ms var(--ease-out),background-color 160ms ease,color 160ms ease,border-color 160ms ease}.button[data-variant="primary"]{color:var(--primary-foreground);background:var(--primary)}.button[data-variant="secondary"]{border-color:var(--border-strong);color:var(--foreground);background:var(--card)}.button[data-variant="ghost"]{color:var(--secondary-foreground);background:transparent}.button:active{transform:scale(.98)}.text-link{min-height:44px;display:inline-flex;align-items:center;color:var(--secondary-foreground);font-size:14px;font-weight:500;text-underline-offset:5px;transition:color 160ms ease,transform 140ms var(--ease-out)}.text-link:active{transform:scale(.98)}
    main{position:relative;overflow:visible}.section{padding:96px 0;border-top:1px solid var(--border)}.kicker{display:flex;align-items:center;gap:9px;color:var(--primary);font:500 12px/1.4 var(--font-mono);letter-spacing:.045em;text-transform:uppercase}.kicker:before{content:"";width:18px;height:1px;background:currentColor}.display{margin:18px 0 0;font-size:clamp(48px,6.4vw,76px);font-weight:600;line-height:1.01;letter-spacing:-.052em;text-wrap:balance}.section-title{max-width:850px;margin:16px 0 0;font-size:clamp(36px,4.8vw,56px);font-weight:600;line-height:1.06;letter-spacing:-.043em;text-wrap:balance}.lead{max-width:700px;margin:22px 0 0;color:var(--secondary-foreground);font-size:18px;line-height:1.55}.section-lead{max-width:650px;margin:18px 0 0;color:var(--muted-foreground);font-size:16px}.actions{display:flex;flex-wrap:wrap;align-items:center;gap:10px 18px;margin-top:28px}.meta-line{display:flex;flex-wrap:wrap;gap:8px 22px;margin-top:24px;color:var(--muted-foreground);font-size:13px}.meta-line strong{color:var(--secondary-foreground);font-weight:500}.badge{display:inline-flex;align-items:center;min-height:26px;padding:3px 8px;border:1px solid var(--border);border-radius:999px;color:var(--secondary-foreground);background:var(--card);font:500 11px/1.2 var(--font-mono)}
    .product-panel{margin:0;padding:12px;border:1px solid var(--border-strong);border-radius:var(--radius-lg);background:var(--card);box-shadow:0 34px 90px rgba(0,0,0,.3)}.product-window{overflow:hidden;border:1px solid var(--border);border-radius:10px;background:#edf1ee}.product-window a{display:block}.product-window img{width:100%;max-width:100%;height:auto;display:block}.product-panel figcaption{display:flex;justify-content:space-between;gap:18px;padding:11px 3px 0;color:var(--muted-foreground);font-size:12px}.product-panel figcaption strong{color:var(--secondary-foreground);font-weight:500}.proof-rail{display:grid;grid-template-columns:repeat(3,1fr);margin:30px 0 0;padding:0;border-top:1px solid var(--border);border-bottom:1px solid var(--border);list-style:none}.proof-rail li{min-width:0;padding:20px 24px;border-left:1px solid var(--border)}.proof-rail li:first-child{border-left:0;padding-left:0}.proof-rail strong{display:block;color:var(--foreground);font-size:15px;font-weight:600}.proof-rail span{display:block;margin-top:5px;color:var(--muted-foreground);font-size:13px}.panel{border:1px solid var(--border);border-radius:var(--radius-md);background:var(--card)}.split{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:64px;align-items:start}.section-header{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(280px,.55fr);gap:56px;align-items:end}.section-header .section-lead{margin:0}
    .step-list{margin:34px 0 0;padding:0;border-top:1px solid var(--border);list-style:none}.step-list li{display:grid;grid-template-columns:42px minmax(0,1fr);gap:14px;padding:18px 0;border-bottom:1px solid var(--border)}.step-list b{color:var(--primary);font:500 11px/1.6 var(--font-mono)}.step-list strong{display:block;font-size:16px;font-weight:600}.step-list span{display:block;margin-top:3px;color:var(--muted-foreground);font-size:14px}.plain-list{margin:30px 0 0;padding:0;border-top:1px solid var(--border);list-style:none}.plain-list li{padding:18px 0;border-bottom:1px solid var(--border)}.plain-list strong{display:block;font-size:16px;font-weight:600}.plain-list span{display:block;margin-top:4px;color:var(--muted-foreground);font-size:14px}.metric-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:0;margin-top:42px;border-top:1px solid var(--border);border-bottom:1px solid var(--border)}.metric{padding:24px;border-left:1px solid var(--border)}.metric:first-child{border-left:0;padding-left:0}.metric strong{display:block;font-size:32px;font-weight:500;line-height:1;letter-spacing:-.035em}.metric span{display:block;margin-top:9px;color:var(--muted-foreground);font-size:13px}.evidence-links{display:flex;flex-wrap:wrap;gap:8px 22px;margin-top:24px}.evidence-links a{min-height:44px;display:inline-flex;align-items:center;color:var(--secondary-foreground);font-size:14px;text-underline-offset:5px}.disclosure-stack{display:grid;gap:10px;margin-top:28px}.disclosure{border:1px solid var(--border);border-radius:var(--radius-md);background:var(--card)}.disclosure summary{min-height:56px;display:flex;align-items:center;justify-content:space-between;gap:20px;padding:13px 16px;cursor:pointer;color:var(--secondary-foreground);font-weight:500;list-style:none}.disclosure summary::-webkit-details-marker{display:none}.disclosure summary:after{content:"+";color:var(--primary);font:500 18px/1 var(--font-mono)}.disclosure[open] summary:after{content:"−"}.disclosure-content{padding:0 16px 18px;color:var(--muted-foreground);font-size:14px}.disclosure-content p{margin:0}.disclosure-content ul,.disclosure-content ol{margin:12px 0 0;padding-left:20px}.disclosure-content li+li{margin-top:8px}.contact-panel{padding:48px;border:1px solid var(--border-strong);border-radius:var(--radius-lg);background:var(--surface)}.contact-panel .section-title{font-size:clamp(34px,4vw,50px)}
    footer{padding:36px 0 48px;color:var(--muted-foreground);font-size:12px}.footer-row{display:flex;justify-content:space-between;gap:24px}.footer-row a{text-underline-offset:4px}
    @media(hover:hover) and (pointer:fine){.button[data-variant="primary"]:hover{background:var(--primary-hover)}.button[data-variant="secondary"]:hover,.nav-links>a:hover{border-color:var(--border-strong);background:var(--surface)}.text-link:hover,.evidence-links a:hover{color:var(--primary)}.disclosure summary:hover{background:var(--surface)}}
    @media(max-width:900px){.section{padding:80px 0}.split,.section-header{grid-template-columns:1fr;gap:38px}.section-header{align-items:start}.section-header .section-lead{margin-top:0}.nav-links>a:not(.button){display:none}.product-panel{padding:9px}.metric-grid{grid-template-columns:repeat(3,1fr)}}
    @media(max-width:640px){.container{width:calc(100% - 32px)}.site-nav{min-height:58px}.brand-copy span{display:none}.display{font-size:clamp(40px,12.3vw,54px)}.section-title{font-size:clamp(32px,9.5vw,42px)}.lead{font-size:16px}.section{padding:64px 0}.actions{align-items:stretch;flex-direction:column}.actions .button,.actions .text-link{width:100%;text-align:center}.text-link{justify-content:center}.product-panel figcaption{display:grid;gap:3px}.proof-rail{grid-template-columns:1fr}.proof-rail li{padding:15px 0;border-left:0;border-top:1px solid var(--border)}.proof-rail li:first-child{border-top:0}.metric-grid{grid-template-columns:1fr 1fr}.metric{padding:20px 0;border-left:0;border-top:1px solid var(--border)}.metric:nth-child(1),.metric:nth-child(2){border-top:0}.metric:nth-child(even){padding-left:16px;border-left:1px solid var(--border)}.contact-panel{padding:32px 20px}.footer-row{display:grid;gap:8px}}
    @media(max-width:380px){.nav-links .button{padding-inline:10px}.display{font-size:36px}.metric strong{font-size:28px}}
    @media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}.button,.text-link{transition-property:background-color,color,border-color}.button:active,.text-link:active{transform:none}}
    @media(prefers-reduced-transparency:reduce){.site-header{background:var(--background);backdrop-filter:none}.product-panel{box-shadow:none}}
    @media(prefers-contrast:more){.site-header{background:var(--background);backdrop-filter:none}.button,.panel,.product-panel,.disclosure,.contact-panel{border-width:2px}.muted,.section-lead,.lead{color:var(--secondary-foreground)}}
    """


def _finish(template: str) -> str:
    return (
        template.replace("__STYLES__", _shared_styles().strip())
        .replace("__VERSION__", VERSION)
        .replace("__UPDATED_DATE__", UPDATED_DATE)
        .replace("__UPDATED_LABEL__", UPDATED_LABEL)
        .replace("__SOCIAL_CARD__", SOCIAL_CARD)
    )


def render_portfolio_page_v19() -> str:
    return _finish("""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="dark">
  <meta name="theme-color" content="#090c0b">
  <meta name="description" content="Mathieu Petroni designed and built a governed AI-assisted review system that catches creative launch errors before Ads Manager.">
  <meta name="author" content="Mathieu Petroni">
  <link rel="canonical" href="https://mattyu-dev.github.io/creative-launch-workspace/">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
  <link rel="me" href="https://www.linkedin.com/in/mathieu-petroni/">
  <link rel="me" href="https://github.com/mattyu-dev">
  <meta property="og:type" content="article">
  <meta property="article:author" content="https://www.linkedin.com/in/mathieu-petroni/">
  <meta property="article:published_time" content="2026-07-13">
  <meta property="article:modified_time" content="__UPDATED_DATE__">
  <meta property="og:site_name" content="Mathieu Petroni · AI automation portfolio">
  <meta property="og:title" content="A governed AI workflow for creative launches | Mathieu Petroni">
  <meta property="og:description" content="One review queue, deterministic checks and explicit human decisions before Ads Manager.">
  <meta property="og:url" content="https://mattyu-dev.github.io/creative-launch-workspace/">
  <meta property="og:image" content="https://mattyu-dev.github.io/creative-launch-workspace/assets/__SOCIAL_CARD__">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Mathieu Petroni's Creative Launch Workspace with a governed review queue">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="A governed AI workflow for creative launches | Mathieu Petroni">
  <meta name="twitter:description" content="One review queue, deterministic checks and explicit human decisions before Ads Manager.">
  <meta name="twitter:image" content="https://mattyu-dev.github.io/creative-launch-workspace/assets/__SOCIAL_CARD__">
  <meta name="twitter:image:alt" content="Mathieu Petroni's Creative Launch Workspace with a governed review queue">
  <title>Mathieu Petroni | AI automation for growth operations</title>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@graph": [
      {"@type":"Person","@id":"https://mattyu-dev.github.io/creative-launch-workspace/#mathieu","name":"Mathieu Petroni","jobTitle":"AI Automation Builder","url":"https://www.linkedin.com/in/mathieu-petroni/","sameAs":["https://www.linkedin.com/in/mathieu-petroni/","https://github.com/mattyu-dev"]},
      {"@type":"SoftwareSourceCode","@id":"https://mattyu-dev.github.io/creative-launch-workspace/#software","name":"Creative Launch Workspace","description":"AI-assisted brief intake and deterministic launch QA for high-volume Meta Ads creative operations.","codeRepository":"https://github.com/mattyu-dev/creative-launch-workspace","programmingLanguage":["Python","JavaScript"],"license":"https://opensource.org/license/mit","version":"__VERSION__","author":{"@id":"https://mattyu-dev.github.io/creative-launch-workspace/#mathieu"}},
      {"@type":"CreativeWork","@id":"https://mattyu-dev.github.io/creative-launch-workspace/#case-study","name":"Creative Launch Workspace portfolio case study","dateModified":"__UPDATED_DATE__","url":"https://mattyu-dev.github.io/creative-launch-workspace/","image":"https://mattyu-dev.github.io/creative-launch-workspace/assets/__SOCIAL_CARD__","author":{"@id":"https://mattyu-dev.github.io/creative-launch-workspace/#mathieu"},"about":{"@id":"https://mattyu-dev.github.io/creative-launch-workspace/#software"}}
    ]
  }
  </script>
  <style>__STYLES__
    .home-hero{padding:64px 0 0}.hero-intro{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(300px,.55fr);gap:72px;align-items:end}.hero-copy{min-width:0}.hero-context{padding-left:24px;border-left:1px solid var(--border)}.hero-context p{margin:0;color:var(--muted-foreground);font-size:14px}.hero-context p+p{margin-top:16px}.hero-context strong{display:block;margin-bottom:3px;color:var(--foreground);font-weight:600}.hero-product{margin-top:44px}.home-hero>.hero-product{max-width:1120px;margin-inline:auto}.home-hero .proof-rail{margin-bottom:0}.workflow-layout{display:grid;grid-template-columns:minmax(320px,.72fr) minmax(0,1.28fr);gap:72px;align-items:center}.workflow-layout .product-panel{order:2}.workflow-copy{order:1}.governance-layout{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:72px}.role-card{padding:32px}.role-card p{margin:16px 0 0;color:var(--muted-foreground)}.role-card .actions{margin-top:22px}.role-label{color:var(--primary);font:500 11px/1.4 var(--font-mono);letter-spacing:.04em;text-transform:uppercase}.role-card h2{margin:12px 0 0;font-size:clamp(30px,3.4vw,44px);font-weight:600;line-height:1.08;letter-spacing:-.04em}.governance-copy h2{margin:14px 0 0;font-size:clamp(32px,4vw,48px);font-weight:600;line-height:1.08;letter-spacing:-.04em}.evidence-section .section-header{align-items:end}.contact-section{padding-top:0;border-top:0}
    @media(max-width:900px){.hero-intro,.workflow-layout,.governance-layout{grid-template-columns:1fr;gap:38px}.hero-context{max-width:700px}.workflow-layout .product-panel,.workflow-copy{order:initial}}
    @media(max-width:640px){.home-hero{padding-top:36px}.hero-product{margin-top:34px}.hero-context{padding-left:16px}.role-card{padding:24px 20px}.workflow-layout,.governance-layout{gap:32px}.contact-section{padding-top:0}}
  </style>
</head>
<body>
  <a class="skip-link" href="#main">Skip to the project</a>
  <header class="site-header">
    <nav class="container site-nav" aria-label="Primary navigation">
      <a class="brand" href="#top"><span class="brand-mark" aria-hidden="true">MP</span><span class="brand-copy"><strong>Mathieu Petroni</strong><span>Creative Launch Workspace</span></span></a>
      <div class="nav-links"><a href="#workflow">Workflow</a><a href="#role">My role</a><a href="case-study.html">Case study</a><a class="button" data-variant="primary" href="workspace.html?guided=1">Try the demo</a></div>
    </nav>
  </header>
  <main id="main">
    <section class="container home-hero" id="top">
      <div class="hero-intro">
        <div class="hero-copy">
          <div class="kicker">Personal project · AI automation × growth operations</div>
          <h1 class="display">I built an AI workflow that catches creative launch errors before Ads Manager.</h1>
          <p class="lead">It turns briefs, spreadsheets and asset folders into one decision queue, while people keep control of ambiguous cases.</p>
          <div class="actions"><a class="button" data-variant="primary" href="workspace.html?guided=1">Try the 2-minute review</a><a class="text-link" href="case-study.html">Read the case study →</a></div>
          <div class="meta-line"><span><strong>Built end to end</strong> Product, AI safeguards, engineering and QA</span><span><strong>Prototype boundary</strong> Synthetic data, browser-local, no Meta connection</span></div>
        </div>
        <aside class="hero-context" aria-label="About Mathieu and the project">
          <p><strong>Mathieu Petroni</strong>AI Automation Builder. Growth and performance marketing since 2017.</p>
          <p><strong>Open to conversations</strong><a class="text-link" href="https://www.linkedin.com/in/mathieu-petroni/" rel="me external">Connect on LinkedIn →</a></p>
        </aside>
      </div>
      <div class="hero-product">
        <figure class="product-panel">
          <div class="product-window"><a href="workspace.html?guided=1">
            <picture>
              <source media="(max-width:720px)" type="image/webp" srcset="assets/workspace-mobile-hero.webp 390w" sizes="calc(100vw - 50px)">
              <source media="(max-width:720px)" type="image/png" srcset="assets/workspace-mobile-hero.png 390w" sizes="calc(100vw - 50px)">
              <source type="image/avif" srcset="assets/workspace-desktop.avif 1440w" sizes="(max-width:1248px) calc(100vw - 72px), 1176px">
              <source type="image/webp" srcset="assets/workspace-desktop.webp 1440w" sizes="(max-width:1248px) calc(100vw - 72px), 1176px">
              <img src="assets/workspace-desktop.png" width="1440" height="1000" alt="Creative review queue showing an ambiguous row, its owner and the available human decisions" decoding="async" fetchpriority="high">
            </picture>
          </a></div>
          <figcaption><strong>Interactive product · no signup</strong><span>Review-only export · no live write path</span></figcaption>
        </figure>
      </div>
      <ul class="proof-rail" aria-label="Prototype evidence"><li><strong>100-row fixture</strong><span>Synthetic creative batch</span></li><li><strong>70 seeded exceptions</strong><span>Blockers and ambiguity routes</span></li><li><strong>0 write paths</strong><span>Cannot publish or change spend</span></li></ul>
    </section>

    <section class="section" id="workflow" aria-labelledby="workflow-title">
      <div class="container workflow-layout">
        <div class="workflow-copy"><div class="kicker">The workflow</div><h2 class="section-title" id="workflow-title">Find the blocker. Route the fix. Keep the decision human.</h2><ol class="step-list"><li><b>01</b><div><strong>Find</strong><span>Checks separate passes from exceptions.</span></div></li><li><b>02</b><div><strong>Route</strong><span>Each issue names an owner and action.</span></div></li><li><b>03</b><div><strong>Decide</strong><span>Ambiguity waits for a reviewer.</span></div></li></ol><div class="actions"><a class="button" data-variant="secondary" href="workspace.html?guided=1">Make one decision</a></div></div>
        <figure class="product-panel"><div class="product-window"><img src="assets/guided-review-step-3.png" width="1280" height="900" loading="lazy" decoding="async" alt="Guided review completion receipt showing the local decision, reviewer role and audit event"></div><figcaption><strong>A local receipt closes the loop</strong><span>The system records the choice without gaining publish authority</span></figcaption></figure>
      </div>
    </section>

    <section class="section" id="role" aria-labelledby="governance-title">
      <div class="container governance-layout">
        <div class="governance-copy"><div class="kicker">Governance by design</div><h2 id="governance-title">The model proposes. Code verifies. A person decides.</h2><p class="section-lead">The model can propose or abstain. It cannot validate, approve or publish.</p><ul class="plain-list"><li><strong>Evidence-backed input</strong><span>Fields link to evidence or stay empty.</span></li><li><strong>Deterministic authority</strong><span>Python owns validation rules.</span></li><li><strong>Explicit human control</strong><span>Reviewers accept, return or block.</span></li></ul><a class="text-link" href="case-study.html#system">Inspect the system →</a></div>
        <article class="panel role-card"><div class="role-label">My role</div><h2>I built the operating model and the product.</h2><p>I defined the review flow, then built the interface, contracts, validators, evaluation fixtures and browser QA.</p><ul class="step-list"><li><b>01</b><div><strong>Product strategy</strong><span>Problem, states and ownership</span></div></li><li><b>02</b><div><strong>AI system and safeguards</strong><span>Grounding, abstention and risk boundaries</span></div></li><li><b>03</b><div><strong>Engineering and QA</strong><span>Python, JavaScript, accessibility and CI</span></div></li></ul><div class="actions"><a class="button" data-variant="primary" href="https://www.linkedin.com/in/mathieu-petroni/" rel="me external">Connect on LinkedIn</a><a class="text-link" href="https://github.com/mattyu-dev" rel="me external">GitHub →</a></div></article>
      </div>
    </section>

    <section class="section evidence-section" id="evidence" aria-labelledby="evidence-title">
      <div class="container"><div class="section-header"><div><div class="kicker">Engineering proof</div><h2 class="section-title" id="evidence-title">Inspectable, reproducible and honest about its limits.</h2></div><p class="section-lead">Implementation and test outcomes are not business results. Live model quality and Meta compatibility remain unproven.</p></div><div class="metric-grid"><div class="metric"><strong>64</strong><span>automated tests across supported Python versions</span></div><div class="metric"><strong>7</strong><span>responsive widths with browser interaction QA</span></div><div class="metric"><strong>100/100</strong><span>desktop and mobile Lighthouse accessibility</span></div></div><div class="evidence-links"><a href="case-study.html">Full case study →</a><a href="https://github.com/mattyu-dev/creative-launch-workspace/blob/main/docs/architecture/system.md">Architecture</a><a href="https://github.com/mattyu-dev/creative-launch-workspace/actions">Source and CI</a></div></div>
    </section>

    <section class="container section contact-section" aria-labelledby="contact-title"><div class="contact-panel"><div class="kicker">Hiring or project conversation</div><h2 class="section-title" id="contact-title">Turn messy operations into a controllable AI workflow.</h2><p class="section-lead">I can explain the decisions here and adapt the approach to a real operating environment.</p><div class="actions"><a class="button" data-variant="primary" href="https://www.linkedin.com/in/mathieu-petroni/" rel="me external">Connect with Mathieu</a><a class="button" data-variant="secondary" href="https://github.com/mattyu-dev/creative-launch-workspace">Explore the source</a></div></div></section>
  </main>
  <footer><div class="container footer-row"><span>Built by <a href="https://www.linkedin.com/in/mathieu-petroni/" rel="me external">Mathieu Petroni</a> · Creative Launch Workspace · v__VERSION__</span><span>MIT licensed · Synthetic reference implementation · <a href="case-study.html">Technical case study</a></span></div></footer>
</body>
</html>
""")


def render_case_study_page_v19() -> str:
    return _finish("""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="dark">
  <meta name="theme-color" content="#090c0b">
  <meta name="description" content="How Mathieu Petroni built a governed AI-assisted review workflow for creative launches.">
  <meta name="author" content="Mathieu Petroni">
  <link rel="canonical" href="https://mattyu-dev.github.io/creative-launch-workspace/case-study.html">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
  <link rel="me" href="https://www.linkedin.com/in/mathieu-petroni/">
  <link rel="me" href="https://github.com/mattyu-dev">
  <meta property="og:type" content="article">
  <meta property="article:author" content="https://www.linkedin.com/in/mathieu-petroni/">
  <meta property="article:published_time" content="2026-07-13">
  <meta property="article:modified_time" content="__UPDATED_DATE__">
  <meta property="og:site_name" content="Mathieu Petroni · AI automation portfolio">
  <meta property="og:title" content="Creative Launch Workspace case study | Mathieu Petroni">
  <meta property="og:description" content="From scattered campaign inputs to one accountable creative review.">
  <meta property="og:url" content="https://mattyu-dev.github.io/creative-launch-workspace/case-study.html">
  <meta property="og:image" content="https://mattyu-dev.github.io/creative-launch-workspace/assets/__SOCIAL_CARD__">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Mathieu Petroni's Creative Launch Workspace case study">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Creative Launch Workspace case study | Mathieu Petroni">
  <meta name="twitter:description" content="From scattered campaign inputs to one accountable creative review.">
  <meta name="twitter:image" content="https://mattyu-dev.github.io/creative-launch-workspace/assets/__SOCIAL_CARD__">
  <title>Creative Launch Workspace case study | Mathieu Petroni</title>
  <script type="application/ld+json">
  {"@context":"https://schema.org","@graph":[{"@type":"Person","@id":"https://mattyu-dev.github.io/creative-launch-workspace/#mathieu","name":"Mathieu Petroni","jobTitle":"AI Automation Builder","url":"https://www.linkedin.com/in/mathieu-petroni/"},{"@type":"SoftwareSourceCode","@id":"https://mattyu-dev.github.io/creative-launch-workspace/#software","name":"Creative Launch Workspace","codeRepository":"https://github.com/mattyu-dev/creative-launch-workspace","programmingLanguage":["Python","JavaScript"],"license":"https://opensource.org/license/mit","version":"__VERSION__","author":{"@id":"https://mattyu-dev.github.io/creative-launch-workspace/#mathieu"}},{"@type":"CreativeWork","@id":"https://mattyu-dev.github.io/creative-launch-workspace/case-study.html#case-study","name":"Creative Launch Workspace technical case study","dateModified":"__UPDATED_DATE__","url":"https://mattyu-dev.github.io/creative-launch-workspace/case-study.html","image":"https://mattyu-dev.github.io/creative-launch-workspace/assets/__SOCIAL_CARD__","author":{"@id":"https://mattyu-dev.github.io/creative-launch-workspace/#mathieu"},"about":{"@id":"https://mattyu-dev.github.io/creative-launch-workspace/#software"}}]}
  </script>
  <style>__STYLES__
    .case-hero{padding:72px 0 0}.case-hero~.section{padding:76px 0}.case-intro{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(280px,.5fr);gap:72px;align-items:end}.case-hero .display{max-width:900px}.case-meta{display:grid;gap:0;border-top:1px solid var(--border)}.case-meta div{padding:14px 0;border-bottom:1px solid var(--border)}.case-meta dt{color:var(--muted-foreground);font:500 11px/1.4 var(--font-mono);text-transform:uppercase}.case-meta dd{margin:4px 0 0;color:var(--secondary-foreground);font-size:14px}.hero-cta{margin-top:28px}.hero-product{max-width:1100px;margin:44px auto 0}.case-hero .proof-rail{margin-bottom:0}.failure-rail{display:grid;grid-template-columns:repeat(3,1fr);gap:30px;margin-top:40px}.failure{padding-top:18px;border-top:1px solid var(--border)}.failure b{color:var(--primary);font:500 11px/1.4 var(--font-mono)}.failure strong{display:block;margin-top:9px;font-size:16px}.failure span{display:block;margin-top:5px;color:var(--muted-foreground);font-size:14px}.experience-layout{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(300px,.55fr);gap:64px;align-items:center}.experience-copy .section-title{font-size:clamp(34px,4vw,50px)}.experience-copy .actions{margin-top:22px}.system-flow{display:grid;grid-template-columns:repeat(4,1fr);margin:42px 0 0;padding:0;border:1px solid var(--border);border-radius:var(--radius-md);background:var(--card);list-style:none}.system-flow li{position:relative;min-width:0;padding:24px;border-left:1px solid var(--border)}.system-flow li:first-child{border-left:0}.system-flow li:not(:last-child):after{content:"→";position:absolute;right:-10px;top:25px;z-index:2;width:20px;height:20px;display:grid;place-items:center;color:var(--primary);background:var(--card);font:500 13px/1 var(--font-mono)}.system-flow b{color:var(--primary);font:500 11px/1.4 var(--font-mono)}.system-flow strong{display:block;margin-top:10px;font-size:15px}.system-flow span{display:block;margin-top:5px;color:var(--muted-foreground);font-size:13px}.receipt-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}.receipt{padding:18px;border:1px solid var(--border);border-radius:var(--radius-sm);background:var(--background)}.receipt .badge{margin-bottom:14px}.receipt dl{margin:0}.receipt dl div{display:grid;grid-template-columns:minmax(120px,.7fr) minmax(0,1fr);gap:16px;padding:9px 0;border-top:1px solid var(--border)}.receipt dt{color:var(--muted-foreground)}.receipt dd{margin:0;color:var(--secondary-foreground)}.role-layout{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1.2fr);gap:72px}.role-layout .plain-list{margin-top:0}.limits{margin-top:28px;padding:18px 20px;border-left:2px solid var(--primary);color:var(--muted-foreground);background:var(--card);font-size:14px}.limits strong{color:var(--foreground)}.evidence-contact{margin-top:48px}
    @media(max-width:900px){.case-intro,.experience-layout,.role-layout{grid-template-columns:1fr;gap:38px}.system-flow{grid-template-columns:1fr 1fr}.system-flow li:nth-child(3){border-left:0;border-top:1px solid var(--border)}.system-flow li:nth-child(4){border-top:1px solid var(--border)}.system-flow li:after{display:none}}
    @media(max-width:640px){.case-hero{padding-top:46px}.case-hero~.section{padding:52px 0}.hero-product{margin-top:34px}.failure-rail,.receipt-grid,.system-flow{grid-template-columns:1fr}.failure-rail{gap:18px}.system-flow li{border-left:0;border-top:1px solid var(--border)}.system-flow li:first-child{border-top:0}.receipt dl div{grid-template-columns:1fr;gap:3px}.experience-layout,.role-layout{gap:30px}.evidence-contact{margin-top:32px}}
  </style>
</head>
<body>
  <a class="skip-link" href="#main">Skip to case study</a>
  <header class="site-header"><nav class="container site-nav" aria-label="Case study navigation"><a class="brand" href="index.html"><span class="brand-mark" aria-hidden="true">MP</span><span class="brand-copy"><strong>Mathieu Petroni</strong><span>Creative Launch Workspace</span></span></a><div class="nav-links"><a href="#system">System</a><a href="#proof">Evidence</a><a class="button" data-variant="primary" href="workspace.html?guided=1">Try the demo</a></div></nav></header>
  <main id="main">
    <section class="container case-hero" id="top">
      <div class="case-intro"><div class="hero-copy"><div class="kicker">Case study · Personal project · 2026</div><h1 class="display">From scattered campaign inputs to one accountable creative review.</h1><p class="lead">I designed and built a workflow that grounds AI proposals in evidence, checks every row in code and leaves ambiguous decisions to a person.</p><div class="hero-cta"><div class="actions"><a class="button" data-variant="primary" href="workspace.html?guided=1">Open the guided demo</a><a class="button" data-variant="secondary" href="https://github.com/mattyu-dev/creative-launch-workspace">View source</a></div></div></div><dl class="case-meta"><div><dt>Role</dt><dd>Product, AI safeguards and engineering end to end</dd></div><div><dt>Scope</dt><dd>Browser-local reference implementation</dd></div><div><dt>Fixture</dt><dd>100 synthetic creatives, 70 seeded exceptions</dd></div><div><dt>Boundary</dt><dd>0 live write paths</dd></div></dl></div>
      <div class="hero-product"><figure class="product-panel"><div class="product-window"><a href="workspace.html?guided=1"><picture><source media="(max-width:720px)" type="image/webp" srcset="assets/workspace-mobile-hero.webp 390w" sizes="calc(100vw - 50px)"><source media="(max-width:720px)" type="image/png" srcset="assets/workspace-mobile-hero.png 390w" sizes="calc(100vw - 50px)"><source type="image/avif" srcset="assets/workspace-desktop.avif 1440w" sizes="(max-width:1248px) calc(100vw - 72px), 1176px"><source type="image/webp" srcset="assets/workspace-desktop.webp 1440w" sizes="(max-width:1248px) calc(100vw - 72px), 1176px"><img src="assets/workspace-desktop.png" width="1440" height="1000" alt="Creative review queue showing an ambiguous row, its owner and available human decisions" decoding="async" fetchpriority="high"></picture></a></div><figcaption><strong>Interactive product · no signup</strong><span>Committed deterministic fixture · no live inference in this demo · no Meta write path</span></figcaption></figure></div>
      <ul class="proof-rail" aria-label="Project facts"><li><strong>Model role</strong><span>Evidence-backed proposal with explicit abstention</span></li><li><strong>Code role</strong><span>Schema, policy and row validation</span></li><li><strong>Human role</strong><span>Accept, return or block ambiguity</span></li></ul>
    </section>

    <section class="section" id="problem" aria-labelledby="problem-title"><div class="container"><div class="reading"><div class="kicker">The operational problem</div><h2 class="section-title" id="problem-title">The hard part was not generating rows. It was knowing which ones needed a decision.</h2><p class="section-lead">A campaign brief, spreadsheet and chat thread each hold part of launch truth. A spreadsheet can store the rows, but it does not preserve the evidence, owner and decision behind every exception.</p></div><div class="failure-rail"><div class="failure"><b>01</b><strong>Fragmented evidence</strong><span>Inputs disagree and source context gets lost.</span></div><div class="failure"><b>02</b><strong>Unclear ownership</strong><span>Errors surface without a named next action.</span></div><div class="failure"><b>03</b><strong>Hidden ambiguity</strong><span>Uncertain cases are silently guessed or ignored.</span></div></div></div></section>

    <section class="section" id="experience" aria-labelledby="experience-title"><div class="container experience-layout"><figure class="product-panel"><div class="product-window"><img src="assets/guided-review-step-3.png" width="1280" height="900" loading="lazy" decoding="async" alt="Guided review completion receipt with a recorded local decision and reviewer role"></div><figcaption><strong>One accountable review loop</strong><span>The decision ends with an inspectable local receipt</span></figcaption></figure><div class="experience-copy"><div class="kicker">The experience</div><h2 class="section-title" id="experience-title">Find the blocker. Route the fix. Keep the decision human.</h2><ol class="step-list"><li><b>01</b><div><strong>Find</strong><span>Checks separate passing rows from exceptions.</span></div></li><li><b>02</b><div><strong>Route</strong><span>The issue, owner and required fix stay together.</span></div></li><li><b>03</b><div><strong>Decide</strong><span>A reviewer makes the ambiguous call and records it.</span></div></li></ol><div class="actions"><a class="button" data-variant="secondary" href="workspace.html?guided=1">Try the 2-minute review</a></div></div></div></section>

    <section class="section" id="system" aria-labelledby="system-title"><div class="container"><div class="section-header"><div><div class="kicker">Key design decision</div><h2 class="section-title" id="system-title">The model proposes. Code verifies. A person decides.</h2></div><p class="section-lead">No stage inherits the authority of the next one. The model cannot validate, approve or publish.</p></div><ol class="system-flow" aria-label="Governed AI review flow"><li><b>01 · INPUT</b><strong>Evidence-backed proposal</strong><span>Typed values link to the brief or abstain.</span></li><li><b>02 · POLICY</b><strong>Deterministic checks</strong><span>Schema, evidence and risk rules fail closed.</span></li><li><b>03 · DECISION</b><strong>Human authority</strong><span>Ambiguity waits for an explicit choice.</span></li><li><b>04 · OUTPUT</b><strong>Review-only export</strong><span>No Meta credentials or platform mutation path exists.</span></li></ol><div class="disclosure-stack"><details class="disclosure"><summary>See a supported proposal and an abstention</summary><div class="disclosure-content"><div class="receipt-grid"><div class="receipt"><span class="badge">SUPPORTED PROPOSAL</span><dl><div><dt>Objective</dt><dd><code>traffic</code></dd></div><div><dt>Source evidence</dt><dd>“traffic”</dd></div><div><dt>Review</dt><dd>Accepted by reviewer</dd></div></dl></div><div class="receipt"><span class="badge">MISSING CRITICAL FIELD</span><dl><div><dt>Destination URL</dt><dd>Not found in source</dd></div><div><dt>Provider output</dt><dd>No value proposed</dd></div><div><dt>Required action</dt><dd>Human input before materialization</dd></div></dl></div></div></div></details><details class="disclosure"><summary>Explore the technical architecture</summary><div class="disclosure-content"><p>The full field-level receipt, architecture, evaluation protocol and threat model remain inspectable.</p><div class="evidence-links"><a href="brief-evidence.html">Field-level receipt</a><a href="https://github.com/mattyu-dev/creative-launch-workspace/blob/main/docs/architecture/system.md">Architecture</a><a href="https://github.com/mattyu-dev/creative-launch-workspace/tree/main/docs">Engineering docs</a></div></div></details></div></div></section>

    <section class="section" id="role" aria-labelledby="role-title"><div class="container role-layout"><div><div class="kicker">My contribution</div><h2 class="section-title" id="role-title">I built the operating model and the product.</h2><p class="section-lead">I have worked in growth and performance marketing since 2017. I used that context to define a realistic review flow, then implemented and tested it myself.</p></div><ul class="plain-list"><li><strong>Product strategy</strong><span>Defined the problem, decision states, ownership and guided experience.</span></li><li><strong>AI system and safeguards</strong><span>Kept proposals behind evidence, abstention and deterministic policy.</span></li><li><strong>Engineering and QA</strong><span>Built typed Python contracts, browser-local state, audit records, responsive QA and CI.</span></li></ul></div></section>

    <section class="section" id="proof" aria-labelledby="proof-title"><div class="container"><div class="section-header"><div><div class="kicker">Proof and limits</div><h2 class="section-title" id="proof-title">Reproducible evidence, without pretending the prototype is production.</h2></div><p class="section-lead">These are implementation and test outcomes, not customer or business results.</p></div><div class="metric-grid"><div class="metric"><strong>64</strong><span>automated tests across Python 3.9, 3.11 and 3.13</span></div><div class="metric"><strong>7</strong><span>responsive widths with real browser interaction QA</span></div><div class="metric"><strong>100/100</strong><span>Lighthouse accessibility on desktop and mobile</span></div></div><p class="limits"><strong>What this does not prove:</strong> representative live-model quality, production Meta API compatibility, customer-data isolation or measured operator impact. The prototype uses synthetic data and has no platform mutation path.</p><div class="disclosure-stack"><details class="disclosure"><summary>What I would validate next</summary><div class="disclosure-content"><ol><li>Read-only Meta sandbox compatibility.</li><li>Authentication, tenancy, privacy and retention.</li><li>Representative repeated model evaluation.</li><li>Persistent review, replay and gradual approval gates.</li></ol><div class="evidence-links"><a href="https://github.com/mattyu-dev/creative-launch-workspace/actions">CI evidence</a><a href="https://github.com/mattyu-dev/creative-launch-workspace">Source repository</a></div></div></details></div><div class="contact-panel evidence-contact"><div class="kicker">Hiring or project conversation</div><h2 class="section-title">Need someone who can turn messy operations into a governed AI workflow?</h2><p class="section-lead">I can walk you through the tradeoffs in this system and how I would test the approach in a real operating environment.</p><div class="actions"><a class="button" data-variant="primary" href="https://www.linkedin.com/in/mathieu-petroni/" rel="me external">Connect with Mathieu</a><a class="button" data-variant="secondary" href="index.html">Back to portfolio</a></div></div></div></section>
  </main>
  <footer><div class="container footer-row"><span>Built by <a href="https://www.linkedin.com/in/mathieu-petroni/" rel="me external">Mathieu Petroni</a> · Creative Launch Workspace · v__VERSION__ · Updated <time datetime="__UPDATED_DATE__">__UPDATED_LABEL__</time></span><span>MIT licensed · Synthetic reference implementation · <a href="https://github.com/mattyu-dev/creative-launch-workspace">Source</a></span></div></footer>
</body>
</html>
""")


def render_social_card_page_v19() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=1200, initial-scale=1">
  <meta name="author" content="Mathieu Petroni">
  <style>
    *{box-sizing:border-box}html,body{margin:0;width:1200px;height:630px;overflow:hidden}body{color:#f2f7f4;background:#090c0b;font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}main{width:1200px;height:630px;display:grid;grid-template-columns:540px 660px;position:relative;background-image:linear-gradient(rgba(255,255,255,.022) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.022) 1px,transparent 1px);background-size:64px 64px}.copy{padding:62px 48px 46px 62px;display:flex;flex-direction:column}.creator{display:flex;align-items:center;gap:13px}.mark{width:34px;height:34px;display:grid;place-items:center;border:1px solid #35443e;border-radius:8px;color:#7bd9b0;background:#101513;font:600 11px/1 ui-monospace,"SF Mono",Menlo,monospace}.creator-copy{display:grid}.creator-copy strong{font-size:17px}.creator-copy span{margin-top:3px;color:#8e9b95;font-size:12px}.eyebrow{margin-top:66px;color:#7bd9b0;font:500 12px/1.3 ui-monospace,"SF Mono",Menlo,monospace;letter-spacing:.05em;text-transform:uppercase}.hero h1{margin:14px 0 0;font-size:49px;line-height:1.01;letter-spacing:-2.3px;font-weight:600}.hero p{max-width:430px;margin:20px 0 0;color:#c6d0cb;font-size:17px;line-height:1.45}.proof{display:flex;gap:8px;margin-top:24px}.proof span{padding:6px 9px;border:1px solid #24302b;border-radius:999px;color:#c6d0cb;background:#101513;font-size:11px}.copy footer{display:flex;justify-content:space-between;margin-top:auto;color:#8e9b95;font-size:11px}.visual{padding:54px 52px 54px 0;display:flex;align-items:center}.frame{width:100%;padding:12px;border:1px solid #35443e;border-radius:16px;background:#101513;box-shadow:0 35px 90px rgba(0,0,0,.45)}.frame img{width:100%;height:auto;display:block;border:1px solid #24302b;border-radius:10px}.frame p{display:flex;justify-content:space-between;margin:10px 2px 0;color:#8e9b95;font-size:10px}.frame strong{color:#c6d0cb;font-weight:500}
  </style>
</head>
<body><main><section class="copy"><div class="creator"><span class="mark">MP</span><div class="creator-copy"><strong>Mathieu Petroni</strong><span>AI automation · Product systems · Growth operations</span></div></div><div class="hero"><div class="eyebrow">Personal product case study</div><h1>A governed AI workflow for creative launches.</h1><p>Evidence-backed proposals. Deterministic checks. Explicit human decisions before Ads Manager.</p><div class="proof"><span>100-row fixture</span><span>64 tests</span><span>0 write paths</span></div></div><footer><strong>Creative Launch Workspace</strong><span>Designed and built end to end</span></footer></section><div class="visual"><div class="frame"><img src="assets/workspace-desktop.png" alt=""><p><strong>Interactive review workspace</strong><span>Browser-local prototype</span></p></div></div></main></body>
</html>
"""
