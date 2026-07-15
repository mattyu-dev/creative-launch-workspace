from __future__ import annotations

VERSION = "2.0.0"
UPDATED_DATE = "2026-07-15"
UPDATED_LABEL = "15 July 2026"
SOCIAL_CARD = "social-card-v2-0.png"


def _shared_styles() -> str:
    return """
    :root {
      color-scheme: light;
      --canvas:#f4f1ea;
      --surface:#fbf9f5;
      --raised:#fffdf8;
      --ink:#1d1f1c;
      --body:#454943;
      --muted:#666b64;
      --border:#d7d8d2;
      --border-strong:#b8bbb4;
      --brand:#b83b1f;
      --brand-hover:#972d18;
      --brand-soft:#f4dcd4;
      --brand-foreground:#ffffff;
      --success:#176143;
      --success-soft:#e3eee8;
      --warning:#7a5700;
      --warning-soft:#f7ebc9;
      --danger:#9e342b;
      --danger-soft:#f3e1dd;
      --font-sans:"Avenir Next","SF Pro Text",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
      --font-mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;
      --radius-sm:10px;
      --radius-md:14px;
      --radius-lg:18px;
      --ease-out:cubic-bezier(.23,1,.32,1);
    }
    *{box-sizing:border-box}
    html{scroll-behavior:smooth}
    body{margin:0;color:var(--ink);background:var(--canvas);font:400 16px/1.55 var(--font-sans);letter-spacing:-.006em;-webkit-font-smoothing:antialiased}
    h1,h2,h3,p,a,strong,span,dd,dt,summary{overflow-wrap:anywhere}
    a{color:inherit}
    a:focus-visible,summary:focus-visible{outline:2px solid var(--brand);outline-offset:3px}
    .container{width:min(1240px,calc(100% - 64px));margin-inline:auto}
    .skip-link{position:fixed;left:16px;top:-80px;z-index:80;min-height:44px;display:flex;align-items:center;padding:8px 14px;border-radius:var(--radius-sm);color:var(--brand-foreground);background:var(--brand);font-weight:650}
    .skip-link:focus{top:14px}
    .site-header{position:sticky;top:0;z-index:50;border-bottom:1px solid rgba(184,187,180,.82);background:rgba(244,241,234,.94);backdrop-filter:blur(16px) saturate(130%)}
    .site-nav{min-height:64px;display:flex;align-items:center;justify-content:space-between;gap:24px}
    .brand{min-height:44px;display:inline-flex;align-items:center;gap:11px;text-decoration:none}
    .brand-mark{width:30px;height:30px;position:relative;flex:0 0 auto;border:1px solid var(--ink);border-radius:9px;background:var(--raised)}
    .brand-mark:before,.brand-mark:after{content:"";position:absolute;background:var(--brand)}
    .brand-mark:before{left:7px;top:7px;width:7px;height:7px;border-radius:2px}
    .brand-mark:after{right:7px;bottom:7px;width:7px;height:7px;border-radius:50%}
    .brand-copy{display:grid;line-height:1.12}
    .brand-copy strong{font-size:14px;font-weight:680;letter-spacing:-.015em}
    .brand-copy span{margin-top:3px;color:var(--muted);font-size:11px;letter-spacing:.02em}
    .nav-links{display:flex;align-items:center;gap:4px}
    .nav-links>a:not(.button){min-height:44px;display:inline-flex;align-items:center;padding:0 10px;border-radius:var(--radius-sm);color:var(--muted);font-size:13px;text-decoration:none}
    .nav-links .button{margin-left:5px;padding-inline:15px}
    .button{min-height:44px;display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:10px 16px;border:1px solid transparent;border-radius:var(--radius-sm);font-size:14px;font-weight:650;line-height:1.2;text-decoration:none;transition:transform 140ms var(--ease-out),background-color 160ms ease,color 160ms ease,border-color 160ms ease}
    .button[data-variant="primary"]{color:var(--brand-foreground);background:var(--brand)}
    .button[data-variant="secondary"]{border-color:var(--border-strong);color:var(--ink);background:var(--raised)}
    .button:active{transform:scale(.98)}
    .text-link{min-height:44px;display:inline-flex;align-items:center;color:var(--ink);font-size:14px;font-weight:650;text-underline-offset:5px;transition:color 160ms ease,transform 140ms var(--ease-out)}
    .text-link:active{transform:scale(.98)}
    .section{padding:96px 0;border-top:1px solid var(--border)}
    .kicker{color:var(--brand);font:700 12px/1.4 var(--font-mono);letter-spacing:.08em;text-transform:uppercase}
    .display{margin:18px 0 0;font-size:clamp(50px,5.4vw,76px);font-weight:680;line-height:1.01;letter-spacing:-.055em;text-wrap:balance}
    .section-title{max-width:880px;margin:14px 0 0;font-size:clamp(38px,4.2vw,56px);font-weight:680;line-height:1.06;letter-spacing:-.045em;text-wrap:balance}
    .lead{max-width:680px;margin:22px 0 0;color:var(--body);font-size:19px;line-height:1.5}
    .section-lead{max-width:680px;margin:18px 0 0;color:var(--muted);font-size:16px}
    .actions{display:flex;flex-wrap:wrap;align-items:center;gap:10px 18px;margin-top:28px}
    .microcopy{margin:14px 0 0;color:var(--muted);font-size:12px;letter-spacing:.01em}
    .product-panel{margin:0;padding:12px;border:1px solid var(--border-strong);border-radius:var(--radius-lg);background:var(--raised);box-shadow:0 24px 70px rgba(45,39,29,.12)}
    .product-window{overflow:hidden;border:1px solid var(--border);border-radius:12px;background:var(--surface)}
    .product-window a{display:block}
    .product-window img{width:100%;max-width:100%;height:auto;display:block}
    .product-panel figcaption{display:flex;justify-content:space-between;gap:18px;padding:10px 3px 0;color:var(--muted);font-size:12px}
    .product-panel figcaption strong{color:var(--ink);font-weight:650}
    .sample-metrics{display:grid;grid-template-columns:repeat(4,1fr);margin:38px 0 0;padding:0;border-top:1px solid var(--border);border-bottom:1px solid var(--border);list-style:none}
    .sample-metrics li{min-width:0;padding:21px 22px;border-left:1px solid var(--border)}
    .sample-metrics li:first-child{border-left:0;padding-left:0}
    .sample-metrics strong{display:block;font-size:25px;font-weight:680;line-height:1}
    .sample-metrics span{display:block;margin-top:7px;color:var(--muted);font-size:12px;line-height:1.35}
    .section-header{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(280px,.55fr);gap:64px;align-items:end}
    .section-header .section-lead{margin:0}
    .benefit-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:44px}
    .benefit{min-height:208px;padding:26px;border:1px solid var(--border);border-radius:var(--radius-md);background:var(--surface)}
    .benefit-index{color:var(--brand);font:700 12px/1.4 var(--font-mono)}
    .benefit h3{margin:44px 0 0;font-size:21px;font-weight:680;line-height:1.2;letter-spacing:-.025em}
    .benefit p{margin:9px 0 0;color:var(--muted);font-size:14px}
    .issue-strip{display:flex;flex-wrap:wrap;gap:8px;margin-top:20px}
    .issue-strip span{display:inline-flex;align-items:center;min-height:34px;padding:6px 11px;border:1px solid var(--border);border-radius:999px;color:var(--body);background:var(--raised);font-size:12px}
    .workflow-layout{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(330px,.65fr);gap:64px;align-items:center}
    .step-list{margin:30px 0 0;padding:0;border-top:1px solid var(--border);list-style:none}
    .step-list li{display:grid;grid-template-columns:42px minmax(0,1fr);gap:14px;padding:18px 0;border-bottom:1px solid var(--border)}
    .step-list b{color:var(--brand);font:700 12px/1.6 var(--font-mono)}
    .step-list strong{display:block;font-size:16px;font-weight:680}
    .step-list span{display:block;margin-top:4px;color:var(--muted);font-size:14px}
    .system-flow{display:grid;grid-template-columns:repeat(4,1fr);margin:42px 0 0;padding:0;border:1px solid var(--border);border-radius:var(--radius-md);background:var(--surface);list-style:none}
    .system-flow li{min-width:0;padding:24px;border-left:1px solid var(--border)}
    .system-flow li:first-child{border-left:0}
    .system-flow b{color:var(--brand);font:700 11px/1.4 var(--font-mono);letter-spacing:.04em;text-transform:uppercase}
    .system-flow strong{display:block;margin-top:24px;font-size:16px;font-weight:680}
    .system-flow span{display:block;margin-top:6px;color:var(--muted);font-size:13px}
    .proof-links{display:flex;flex-wrap:wrap;gap:8px 12px;margin-top:24px}
    .proof-links a{min-height:44px;display:inline-flex;align-items:center;padding:7px 12px;border:1px solid var(--border);border-radius:var(--radius-sm);color:var(--body);background:var(--raised);font-size:13px;text-decoration:none}
    .proof-layout{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1.2fr);gap:64px;margin-top:42px}
    .scope-card,.pilot-card{padding:28px;border:1px solid var(--border);border-radius:var(--radius-md);background:var(--surface)}
    .scope-card h3,.pilot-card h3{margin:0;font-size:21px;font-weight:680;letter-spacing:-.025em}
    .scope-card p,.pilot-card p{margin:12px 0 0;color:var(--muted);font-size:14px}
    .pilot-grid{display:grid;grid-template-columns:1fr 1fr;gap:0 28px;margin:22px 0 0;padding:0;border-top:1px solid var(--border);list-style:none}
    .pilot-grid li{padding:13px 0;border-bottom:1px solid var(--border);color:var(--body);font-size:13px}
    .builder-card{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(280px,.65fr);gap:56px;margin-top:22px;padding:38px;border:1px solid var(--border-strong);border-radius:var(--radius-lg);color:var(--raised);background:var(--ink)}
    .builder-card .kicker{color:#ef9a82}
    .builder-card h2{margin:13px 0 0;font-size:clamp(32px,3.7vw,48px);font-weight:680;line-height:1.06;letter-spacing:-.04em}
    .builder-card p{max-width:680px;margin:16px 0 0;color:#c9ccc6}
    .builder-card .button[data-variant="primary"]{color:var(--ink);background:var(--raised)}
    .reference-list{margin:0;padding:0;border-top:1px solid #3b3e39;list-style:none}
    .reference-list li{border-bottom:1px solid #3b3e39}
    .reference-list a{min-height:52px;display:flex;align-items:center;justify-content:space-between;gap:16px;color:#e8e9e6;font-size:13px;text-decoration:none}
    .reference-list a:after{content:"↗";color:#ef9a82}
    .final-cta{display:flex;align-items:end;justify-content:space-between;gap:48px;margin-top:22px;padding:38px;border:1px solid var(--border);border-radius:var(--radius-lg);background:var(--brand-soft)}
    .final-cta .kicker{color:var(--brand-hover)}
    .final-cta h2{max-width:720px;margin:12px 0 0;font-size:clamp(32px,4vw,48px);font-weight:680;line-height:1.06;letter-spacing:-.04em}
    .final-cta .actions{flex:0 0 auto}
    footer{padding:34px 0 42px;color:var(--muted);font-size:12px}
    .footer-row{display:flex;justify-content:space-between;gap:24px}
    .footer-row a{text-underline-offset:4px}
    @media(hover:hover) and (pointer:fine){
      .button[data-variant="primary"]:hover{background:var(--brand-hover)}
      .button[data-variant="secondary"]:hover,.nav-links>a:hover,.proof-links a:hover{border-color:var(--border-strong);background:var(--surface)}
      .text-link:hover{color:var(--brand)}
      .benefit:hover{border-color:var(--border-strong);background:var(--raised)}
      .builder-card .button[data-variant="primary"]:hover{color:var(--raised);background:var(--brand)}
      .reference-list a:hover{color:#ffffff}
    }
    @media(max-width:1179px){.hero-grid,.workflow-layout{grid-template-columns:1fr;gap:40px}.hero-copy{max-width:820px}.hero-product{max-width:980px}.display{font-size:clamp(48px,7vw,70px)}}
    @media(max-width:900px){.section{padding:78px 0}.section-header,.proof-layout,.builder-card{grid-template-columns:1fr;gap:38px}.section-header{align-items:start}.section-header .section-lead{margin-top:0}.nav-links>a:not(.button){display:none}.benefit-grid{grid-template-columns:1fr 1fr}.benefit:last-child{grid-column:1/-1}.system-flow{grid-template-columns:1fr 1fr}.system-flow li:nth-child(3){border-left:0;border-top:1px solid var(--border)}.system-flow li:nth-child(4){border-top:1px solid var(--border)}.final-cta{align-items:start;flex-direction:column}.final-cta .actions{width:100%}}
    @media(max-width:640px){
      .container{width:calc(100% - 32px)}.site-nav{min-height:58px}.brand-copy span{display:none}.nav-links .button{padding-inline:11px}
      .home-hero{padding-top:26px}.display{font-size:clamp(38px,11.8vw,48px);line-height:1.02}.lead{margin-top:17px;font-size:17px;line-height:1.42}.hero-copy .actions{margin-top:21px}.actions{align-items:stretch;flex-direction:column}.actions .button,.actions .text-link{width:100%;text-align:center}.text-link{justify-content:center}.microcopy{margin-top:10px}.hero-product{margin-top:24px}
      .section{padding:62px 0}.section-title{font-size:clamp(32px,9.2vw,42px);line-height:1.08}.product-panel{padding:8px;border-radius:var(--radius-md)}.product-panel figcaption{display:grid;gap:3px}.sample-metrics{grid-template-columns:1fr 1fr;margin-top:26px}.sample-metrics li{padding:17px 0;border-left:0;border-top:1px solid var(--border)}.sample-metrics li:nth-child(1),.sample-metrics li:nth-child(2){border-top:0}.sample-metrics li:nth-child(even){padding-left:16px;border-left:1px solid var(--border)}
      .benefit-grid,.system-flow{grid-template-columns:1fr}.benefit:last-child{grid-column:auto}.benefit{min-height:auto}.benefit h3{margin-top:30px}.system-flow li{border-left:0;border-top:1px solid var(--border)}.system-flow li:first-child{border-top:0}.pilot-grid{grid-template-columns:1fr}.scope-card,.pilot-card{padding:22px 20px}.builder-card,.final-cta{padding:30px 20px}.footer-row{display:grid;gap:8px}
    }
    @media(max-width:380px){.brand-copy strong{font-size:12px}.display{font-size:37px}.sample-metrics strong{font-size:22px}.hero-copy .text-link{display:none}}
    @media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}.button,.text-link{transition-property:background-color,color,border-color}.button:active,.text-link:active{transform:none}}
    @media(prefers-reduced-transparency:reduce){.site-header{background:var(--canvas);backdrop-filter:none}}
    @media(prefers-contrast:more){.site-header{background:var(--canvas)}.button,.product-panel,.benefit,.system-flow,.scope-card,.pilot-card,.builder-card,.final-cta{border-width:2px}.lead,.section-lead{color:var(--ink)}}
    """


def _finish(template: str) -> str:
    return (
        template.replace("__STYLES__", _shared_styles().strip())
        .replace("__VERSION__", VERSION)
        .replace("__UPDATED_DATE__", UPDATED_DATE)
        .replace("__UPDATED_LABEL__", UPDATED_LABEL)
        .replace("__SOCIAL_CARD__", SOCIAL_CARD)
    )


def render_portfolio_page_v20() -> str:
    return _finish(
        """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <meta name="theme-color" content="#f4f1ea">
  <meta name="description" content="Pre-launch QA for Meta creative teams: check every row, route detected exceptions and record human decisions before campaign build.">
  <meta name="author" content="Mathieu Petroni">
  <link rel="canonical" href="https://mattyu-dev.github.io/creative-launch-workspace/">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
  <link rel="me" href="https://www.linkedin.com/in/mathieu-petroni/">
  <link rel="me" href="https://github.com/mattyu-dev">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Creative Launch Workspace">
  <meta property="og:title" content="Catch launch blockers before Ads Manager">
  <meta property="og:description" content="Check every creative row, route detected exceptions and keep ambiguous decisions human.">
  <meta property="og:url" content="https://mattyu-dev.github.io/creative-launch-workspace/">
  <meta property="og:image" content="https://mattyu-dev.github.io/creative-launch-workspace/assets/__SOCIAL_CARD__">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Creative Launch Workspace pre-launch review queue">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Catch launch blockers before Ads Manager">
  <meta name="twitter:description" content="Pre-launch QA for high-volume Meta creative teams.">
  <meta name="twitter:image" content="https://mattyu-dev.github.io/creative-launch-workspace/assets/__SOCIAL_CARD__">
  <meta name="twitter:image:alt" content="Creative Launch Workspace pre-launch review queue">
  <title>Creative Launch Workspace | Pre-launch QA for Meta creative teams</title>
  <script type="application/ld+json">
  {"@context":"https://schema.org","@graph":[{"@type":"Person","@id":"https://mattyu-dev.github.io/creative-launch-workspace/#mathieu","name":"Mathieu Petroni","jobTitle":"AI Automation Builder","url":"https://www.linkedin.com/in/mathieu-petroni/","sameAs":["https://www.linkedin.com/in/mathieu-petroni/","https://github.com/mattyu-dev"]},{"@type":"SoftwareApplication","@id":"https://mattyu-dev.github.io/creative-launch-workspace/#software","name":"Creative Launch Workspace","applicationCategory":"BusinessApplication","operatingSystem":"Web","description":"Pre-launch review workflow for high-volume Meta creative operations.","softwareVersion":"__VERSION__","author":{"@id":"https://mattyu-dev.github.io/creative-launch-workspace/#mathieu"}},{"@type":"WebSite","@id":"https://mattyu-dev.github.io/creative-launch-workspace/#website","name":"Creative Launch Workspace","url":"https://mattyu-dev.github.io/creative-launch-workspace/","dateModified":"__UPDATED_DATE__","about":{"@id":"https://mattyu-dev.github.io/creative-launch-workspace/#software"}}]}
  </script>
  <style>__STYLES__
    .home-hero{padding:62px 0 0}.hero-grid{display:grid;grid-template-columns:minmax(390px,5fr) minmax(0,7fr);gap:54px;align-items:center}.hero-copy{min-width:0}.hero-product{min-width:0}.home-hero .sample-metrics{margin-bottom:0}
    @media(max-width:1179px){.hero-grid{grid-template-columns:1fr;gap:40px}.hero-copy{max-width:820px}.hero-product{max-width:980px}.display{font-size:clamp(48px,7vw,70px)}}
    @media(max-width:640px){.home-hero{padding-top:26px}.hero-grid{gap:0}.display{font-size:clamp(38px,11.8vw,48px)}.hero-product{margin-top:24px}}
    @media(max-width:380px){.home-hero{padding-top:18px}.hero-product{margin-top:18px}}
  </style>
</head>
<body>
  <a class="skip-link" href="#main">Skip to the product</a>
  <header class="site-header"><nav class="container site-nav" aria-label="Primary navigation"><a class="brand" href="#top"><span class="brand-mark" aria-hidden="true"></span><span class="brand-copy"><strong>Creative Launch Workspace</strong><span>Pre-launch creative QA</span></span></a><div class="nav-links"><a href="#outcomes">Product</a><a href="#workflow">How it works</a><a href="#architecture">Controls</a><a href="#proof">Proof</a><a class="button" data-variant="primary" href="workspace.html?guided=1">Review a sample</a></div></nav></header>
  <main id="main">
    <section class="container home-hero" id="top" aria-labelledby="hero-title">
      <div class="hero-grid">
        <div class="hero-copy"><div class="kicker">Pre-launch QA for Meta creative teams</div><h1 class="display" id="hero-title">Catch launch blockers before Ads Manager.</h1><p class="lead">Check each row in a creative batch for approval, destination, placement, UTM, format and naming issues. Creative Launch Workspace routes every detected exception to an owner and records the decisions that remain human.</p><div class="actions"><a class="button" data-variant="primary" href="workspace.html?guided=1">Review a sample batch</a><a class="text-link" href="workspace.html">Explore the full workspace →</a></div><p class="microcopy">Sample data · No signup · No publishing permissions.</p></div>
        <div class="hero-product"><figure class="product-panel"><div class="product-window"><a href="workspace.html?guided=1"><picture><source media="(max-width:720px)" type="image/webp" srcset="assets/workspace-mobile-hero.webp 780w" sizes="calc(100vw - 50px)"><source media="(max-width:720px)" type="image/png" srcset="assets/workspace-mobile-hero.png 780w" sizes="calc(100vw - 50px)"><source type="image/avif" srcset="assets/workspace-desktop.avif 1440w" sizes="(max-width:1240px) calc(100vw - 80px), 720px"><source type="image/webp" srcset="assets/workspace-desktop.webp 1440w" sizes="(max-width:1240px) calc(100vw - 80px), 720px"><img src="assets/workspace-desktop.png" width="1440" height="1000" alt="Creative review queue with detected exceptions, owners and human decision controls" decoding="async" fetchpriority="high"></picture></a></div><figcaption><strong>Review the exception, not another spreadsheet</strong><span>Real interactive sample</span></figcaption></figure></div>
      </div>
      <ul class="sample-metrics" aria-label="Inside the interactive sample workspace"><li><strong>100</strong><span>creative rows in one review queue</span></li><li><strong>30</strong><span>pass the current offline checks</span></li><li><strong>60</strong><span>concrete fixes with owner and action</span></li><li><strong>10</strong><span>human decisions to accept, return or block</span></li></ul>
    </section>

    <section class="section" id="outcomes" aria-labelledby="outcomes-title"><div class="container"><div class="section-header"><div><div class="kicker">One accountable launch path</div><h2 class="section-title" id="outcomes-title">Turn a scattered handoff into an owned review.</h2></div><p class="section-lead">Briefs, trackers, folders and approval threads each hold part of launch truth. The workspace brings their exceptions into one operating view before campaign build.</p></div><div class="benefit-grid"><article class="benefit"><span class="benefit-index">01 · RECONCILE</span><h3>Check every row against the launch plan.</h3><p>Bring campaign intent, creative metadata and evidence into one repeatable preflight.</p></article><article class="benefit"><span class="benefit-index">02 · ROUTE</span><h3>Give every detected exception an owner.</h3><p>Keep the issue, responsible role and required next action together.</p></article><article class="benefit"><span class="benefit-index">03 · DECIDE</span><h3>Stop automation at the judgment call.</h3><p>Ambiguous cases wait for a person and finish with a recorded decision.</p></article></div><div class="issue-strip" aria-label="Current checks"><span>Missing approval</span><span>Destination mismatch</span><span>UTM drift</span><span>Naming error</span><span>Format and placement</span><span>Possible duplicate</span></div></div></section>

    <section class="section" id="workflow" aria-labelledby="workflow-title"><div class="container workflow-layout"><figure class="product-panel"><div class="product-window"><picture><source media="(max-width:720px)" type="image/webp" srcset="assets/guided-receipt-mobile.webp 960w" sizes="calc(100vw - 50px)"><source media="(max-width:720px)" type="image/png" srcset="assets/guided-receipt-mobile.png 960w" sizes="calc(100vw - 50px)"><img src="assets/guided-review-step-3.png" width="1280" height="900" loading="lazy" decoding="async" alt="Completed review with owner, decision state and local audit receipt"></picture></div><figcaption><strong>One decision closes the loop</strong><span>Owner, state and receipt stay inspectable</span></figcaption></figure><div><div class="kicker">Scan → Route → Decide</div><h2 class="section-title" id="workflow-title">Find the issue. Route the fix. Record the call.</h2><ol class="step-list"><li><b>01</b><div><strong>Scan</strong><span>Offline rules separate passing rows from detected exceptions.</span></div></li><li><b>02</b><div><strong>Route</strong><span>The issue, owner and next action travel together.</span></div></li><li><b>03</b><div><strong>Decide</strong><span>A reviewer accepts, returns or blocks the ambiguous case.</span></div></li></ol><div class="actions"><a class="button" data-variant="primary" href="workspace.html?guided=1">Make one decision</a></div></div></div></section>

    <section class="section" id="architecture" aria-labelledby="architecture-title"><div class="container"><div class="section-header"><div><div class="kicker">Controlled by design</div><h2 class="section-title" id="architecture-title">The model proposes. Rules verify. People decide.</h2></div><p class="section-lead">No stage inherits the authority of the next one. The model cannot validate, approve or publish, and the public workspace has no platform credentials.</p></div><ol class="system-flow" aria-label="Governed review architecture"><li><b>01 · Evidence</b><strong>Ground the input</strong><span>Values link to source evidence or remain empty.</span></li><li><b>02 · Proposal</b><strong>Assist, never approve</strong><span>The model proposes a bounded typed mapping.</span></li><li><b>03 · Policy</b><strong>Fail closed in code</strong><span>Schema, evidence and allowlists own the state.</span></li><li><b>04 · Decision</b><strong>Keep authority human</strong><span>Ambiguity waits for an explicit local receipt.</span></li></ol><div class="proof-links"><a href="brief-evidence.html">Inspect field-level evidence</a><a href="https://github.com/mattyu-dev/creative-launch-workspace/blob/main/docs/architecture/system.md">Read the architecture</a><a href="https://github.com/mattyu-dev/creative-launch-workspace/blob/main/docs/security/threat_model.md">Review the threat model</a><a href="https://github.com/mattyu-dev/creative-launch-workspace/actions">Open tests and CI</a></div></div></section>

    <section class="section" id="proof" aria-labelledby="proof-title"><div class="container"><div class="section-header"><div><div class="kicker">Proof without theatre</div><h2 class="section-title" id="proof-title">Inspect what works. Measure what matters next.</h2></div><p class="section-lead">The sample proves the review loop, trust boundaries and browser behavior. It does not manufacture customer impact.</p></div><div class="proof-layout"><article class="scope-card"><h3>What is proven today</h3><p>A 100-row synthetic sample, 64 automated tests, seven responsive browser widths, a deterministic public flow and 100/100 Lighthouse accessibility on desktop and mobile.</p><p><strong>Scope:</strong> browser-local review state, no customer data, no Meta credentials and no publishing path.</p></article><article class="pilot-card"><h3>What a real pilot should measure</h3><p>Operational value belongs in production telemetry, not in invented ROI claims.</p><ul class="pilot-grid"><li>Review cycle time, median and p90</li><li>Late exception rate</li><li>First-pass readiness</li><li>Decision and assignment latency</li><li>False-positive and reversal rate</li><li>Reviewer effort per 100 creatives</li></ul></article></div><div class="builder-card" id="about"><div><div class="kicker">Built end to end</div><h2>Product judgment and implementation, in one system.</h2><p>Mathieu Petroni combined growth and performance marketing experience since 2017 with product strategy, AI safeguards, Python contracts, browser interactions, accessibility and CI to build the complete review workflow.</p><div class="actions"><a class="button" data-variant="primary" href="https://www.linkedin.com/in/mathieu-petroni/" rel="me external">Contact Mathieu on LinkedIn</a></div></div><ul class="reference-list" aria-label="Project references"><li><a href="https://github.com/mattyu-dev/creative-launch-workspace">Source repository</a></li><li><a href="https://github.com/mattyu-dev/creative-launch-workspace/actions">Tests and CI</a></li><li><a href="https://github.com/mattyu-dev/creative-launch-workspace/tree/main/docs">Engineering documentation</a></li><li><a href="https://github.com/mattyu-dev" rel="me external">GitHub profile</a></li></ul></div><div class="final-cta"><div><div class="kicker">Open the product</div><h2>Review the sample batch in two minutes.</h2></div><div class="actions"><a class="button" data-variant="primary" href="workspace.html?guided=1">Review a sample batch</a><a class="text-link" href="workspace.html">Explore the full workspace →</a></div></div></div></section>
  </main>
  <footer><div class="container footer-row"><span>Creative Launch Workspace · v__VERSION__ · Built by <a href="https://www.linkedin.com/in/mathieu-petroni/" rel="me external">Mathieu Petroni</a></span><span>MIT licensed · Sample workspace · Updated <time datetime="__UPDATED_DATE__">__UPDATED_LABEL__</time></span></div></footer>
</body>
</html>
"""
    )


def render_case_study_page_v20() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex,follow">
  <meta name="theme-color" content="#f4f1ea">
  <link rel="canonical" href="https://mattyu-dev.github.io/creative-launch-workspace/">
  <meta http-equiv="refresh" content="0; url=./#architecture">
  <title>Creative Launch Workspace</title>
  <script>window.location.replace("./#architecture");</script>
  <style>*{box-sizing:border-box}body{min-height:100vh;display:grid;place-items:center;margin:0;padding:24px;color:#1d1f1c;background:#f4f1ea;font:400 16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}main{max-width:620px;padding:32px;border:1px solid #d7d8d2;border-radius:14px;background:#fffdf8}a{color:#b83b1f;font-weight:700;text-underline-offset:4px}</style>
</head>
<body><main><h1>This page has moved.</h1><p>The product story, interactive proof and architecture now live on one page.</p><a href="./#architecture">Continue to Creative Launch Workspace</a></main></body>
</html>
"""


def render_social_card_page_v20() -> str:
    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=1200, initial-scale=1"><meta name="author" content="Mathieu Petroni"><style>
*{box-sizing:border-box}html,body{margin:0;width:1200px;height:630px;overflow:hidden}body{color:#1d1f1c;background:#f4f1ea;font-family:"Avenir Next","SF Pro Display",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}main{width:1200px;height:630px;display:grid;grid-template-columns:500px 700px}.copy{padding:54px 36px 42px 56px;display:flex;flex-direction:column}.brand{display:flex;align-items:center;gap:12px}.mark{width:31px;height:31px;position:relative;border:1px solid #1d1f1c;border-radius:9px;background:#fffdf8}.mark:before,.mark:after{content:"";position:absolute;width:7px;height:7px;background:#b83b1f}.mark:before{left:7px;top:7px;border-radius:2px}.mark:after{right:7px;bottom:7px;border-radius:50%}.brand strong{font-size:16px;font-weight:700}.eyebrow{margin-top:66px;color:#b83b1f;font:700 12px/1.4 ui-monospace,"SF Mono",monospace;letter-spacing:.07em;text-transform:uppercase}.hero h1{margin:15px 0 0;font-size:53px;line-height:1.01;letter-spacing:-2.7px;font-weight:700}.hero p{max-width:400px;margin:20px 0 0;color:#545850;font-size:17px;line-height:1.45}.copy footer{display:flex;justify-content:space-between;margin-top:auto;color:#666b64;font-size:11px}.visual{padding:48px 48px 48px 0;display:flex;align-items:center}.frame{width:100%;padding:12px;border:1px solid #b8bbb4;border-radius:18px;background:#fffdf8;box-shadow:0 24px 70px rgba(45,39,29,.14)}.frame img{width:100%;height:auto;display:block;border:1px solid #d7d8d2;border-radius:12px}.frame p{display:flex;justify-content:space-between;margin:10px 2px 0;color:#666b64;font-size:10px}.frame strong{color:#1d1f1c;font-weight:650}
</style></head><body><main><section class="copy"><div class="brand"><span class="mark"></span><strong>Creative Launch Workspace</strong></div><div class="hero"><div class="eyebrow">Pre-launch QA for Meta creative teams</div><h1>Catch launch blockers before Ads Manager.</h1><p>Check every row, route detected exceptions and keep ambiguous decisions human.</p></div><footer><strong>Interactive sample</strong><span>Built by Mathieu Petroni</span></footer></section><div class="visual"><div class="frame"><img src="assets/workspace-desktop.png" alt=""><p><strong>100-row sample workspace</strong><span>No publishing permissions</span></p></div></div></main></body></html>
"""
