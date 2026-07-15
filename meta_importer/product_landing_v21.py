from __future__ import annotations

VERSION = "2.1.0"
UPDATED_DATE = "2026-07-15"
UPDATED_LABEL = "15 July 2026"
SOCIAL_CARD = "social-card-v2-1.png"


def _shared_styles() -> str:
    return """
    @font-face{font-family:"Geist";src:url("assets/geist-latin-variable.woff2") format("woff2");font-style:normal;font-weight:100 900;font-display:swap}
    @font-face{font-family:"Geist Mono";src:url("assets/geist-mono-latin-variable.woff2") format("woff2");font-style:normal;font-weight:100 900;font-display:swap}
    :root{
      color-scheme:light;
      --background:#f6f7f5;
      --card:#ffffff;
      --surface:#eef0ed;
      --foreground:#151817;
      --body:#3e4541;
      --muted-foreground:#636b66;
      --border:#d8ddd9;
      --border-strong:#b8c0ba;
      --primary:#c83b24;
      --primary-hover:#ae311d;
      --primary-pressed:#8d2414;
      --primary-soft:#fbe8e2;
      --primary-foreground:#ffffff;
      --success:#1f6b4c;
      --success-soft:#e4f0e9;
      --warning:#8b6100;
      --warning-soft:#f7edcf;
      --danger:#7f2d28;
      --danger-soft:#f5e4e1;
      --font-sans:"Geist",system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
      --font-mono:"Geist Mono",ui-monospace,"SFMono-Regular",Consolas,monospace;
      --radius-control:8px;
      --radius-card:14px;
      --radius-product:18px;
      --ease-out:cubic-bezier(.23,1,.32,1);
    }
    *{box-sizing:border-box}
    html{scroll-behavior:smooth}
    body{margin:0;color:var(--foreground);background:var(--background);font:400 16px/1.55 var(--font-sans);letter-spacing:-.008em;-webkit-font-smoothing:antialiased}
    h1,h2,h3,p,a,strong,span,dd,dt,summary{overflow-wrap:anywhere}
    h1,h2,h3,p{margin-top:0}
    a{color:inherit}
    a:focus-visible,summary:focus-visible{outline:2px solid var(--primary);outline-offset:3px}
    .container{width:min(1240px,calc(100% - 64px));margin-inline:auto}
    .skip-link{position:fixed;left:16px;top:-80px;z-index:80;min-height:44px;display:flex;align-items:center;padding:8px 14px;border-radius:var(--radius-control);color:var(--primary-foreground);background:var(--primary);font-weight:650}
    .skip-link:focus{top:14px}
    .site-header{position:sticky;top:0;z-index:20;border-bottom:1px solid rgba(216,221,217,.88);background:rgba(246,247,245,.94);backdrop-filter:blur(16px) saturate(125%)}
    .site-nav{min-height:64px;display:flex;align-items:center;justify-content:space-between;gap:20px}
    .brand{min-height:44px;display:inline-flex;align-items:center;gap:10px;text-decoration:none}
    .brand-mark{width:30px;height:30px;position:relative;flex:0 0 auto;border:1px solid var(--border-strong);border-radius:var(--radius-control);background:var(--card)}
    .brand-mark:before{content:"";position:absolute;inset:7px;border:2px solid var(--primary);border-right-color:transparent}
    .brand-copy{display:grid;line-height:1.12}
    .brand-copy strong{font-size:14px;font-weight:680;letter-spacing:-.018em}
    .brand-copy span{margin-top:3px;color:var(--muted-foreground);font-size:11px;letter-spacing:.01em}
    .nav-links{display:flex;align-items:center;gap:4px}
    .nav-links>a:not(.button){min-height:44px;display:inline-flex;align-items:center;padding:0 10px;border-radius:var(--radius-control);color:var(--muted-foreground);font-size:13px;font-weight:540;text-decoration:none}
    .nav-links .button{margin-left:6px}
    .button{min-height:44px;display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:10px 16px;border:1px solid transparent;border-radius:var(--radius-control);font-size:14px;font-weight:650;line-height:1.15;white-space:nowrap;text-decoration:none;transition:transform 130ms var(--ease-out),background-color 160ms ease,color 160ms ease,border-color 160ms ease}
    .button[data-variant="primary"]{color:var(--primary-foreground);background:var(--primary)}
    .button[data-variant="outline"]{border-color:var(--border-strong);color:var(--foreground);background:var(--card)}
    .button[data-variant="ghost"]{color:var(--foreground);background:transparent}
    .button:active{transform:scale(.97);background:var(--primary-pressed)}
    .button[data-variant="outline"]:active,.button[data-variant="ghost"]:active{background:var(--surface)}
    .text-link{min-height:44px;display:inline-flex;align-items:center;color:var(--foreground);font-size:14px;font-weight:620;text-underline-offset:5px;transition:transform 130ms var(--ease-out),color 160ms ease}
    .text-link:active{transform:scale(.97)}
    .section{padding:104px 0;border-top:1px solid var(--border)}
    .eyebrow{color:var(--primary);font:650 12px/1.4 var(--font-mono);letter-spacing:.06em;text-transform:uppercase}
    .display{max-width:820px;margin:16px 0 0;font-size:clamp(48px,5.6vw,72px);font-weight:660;line-height:1;letter-spacing:-.055em;text-wrap:balance}
    .section-title{max-width:850px;margin:0;font-size:clamp(40px,4.4vw,54px);font-weight:650;line-height:1.06;letter-spacing:-.047em;text-wrap:balance}
    .lead{max-width:640px;margin:20px 0 0;color:var(--body);font-size:18px;line-height:1.5}
    .section-lead{max-width:680px;margin:18px 0 0;color:var(--muted-foreground);font-size:16px}
    .actions{display:flex;flex-wrap:wrap;align-items:center;gap:10px 18px;margin-top:26px}
    .product-frame{min-width:0;margin:0;padding:12px;border:1px solid var(--border-strong);border-radius:var(--radius-product);background:var(--card);box-shadow:0 24px 72px rgba(21,24,23,.11)}
    .product-window{overflow:hidden;border:1px solid var(--border);border-radius:12px;background:var(--surface)}
    .product-window a{display:block}
    .product-window img{width:100%;max-width:100%;height:auto;display:block}
    .product-frame figcaption{display:flex;justify-content:space-between;gap:20px;padding:10px 3px 0;color:var(--muted-foreground);font-size:12px}
    .product-frame figcaption strong{color:var(--foreground);font-weight:630}
    .hero{padding:56px 0 0}
    .hero-intro{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(260px,.55fr);gap:72px;align-items:end}
    .hero-copy{min-width:0;animation:enter-copy 320ms var(--ease-out) both}
    .hero-context{margin:0;border-top:1px solid var(--border)}
    .hero-context div{padding:13px 0;border-bottom:1px solid var(--border)}
    .hero-context dt{color:var(--muted-foreground);font:520 12px/1.4 var(--font-mono)}
    .hero-context dd{margin:4px 0 0;color:var(--body);font-size:14px;font-weight:560}
    .hero-product{margin-top:40px;animation:enter-product 400ms 80ms var(--ease-out) both}
    .sample-metrics{display:grid;grid-template-columns:repeat(4,1fr);margin:28px 0 0;padding:0;border-top:1px solid var(--border);border-bottom:1px solid var(--border);list-style:none}
    .sample-metrics li{min-width:0;padding:20px 22px;border-left:1px solid var(--border)}
    .sample-metrics li:first-child{border-left:0;padding-left:0}
    .sample-metrics strong{display:block;font:660 27px/1 var(--font-mono);letter-spacing:-.04em}
    .sample-metrics span{display:block;margin-top:7px;color:var(--muted-foreground);font-size:12px;line-height:1.4}
    .problem-layout{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(320px,.65fr);gap:88px;align-items:start}
    .problem-list{margin:0;padding:0;border-top:1px solid var(--border);list-style:none}
    .problem-list li{padding:19px 0;border-bottom:1px solid var(--border)}
    .problem-list h3{margin:0;font-size:19px;font-weight:640;letter-spacing:-.025em}
    .problem-list p{margin:6px 0 0;color:var(--muted-foreground);font-size:14px}
    .workflow-layout{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(300px,.6fr);gap:64px;align-items:center}
    .workflow-layout>*{min-width:0}
    .workflow-copy .section-title{font-size:clamp(38px,4vw,50px)}
    .step-list{margin:28px 0 0;padding:0;border-top:1px solid var(--border);list-style:none}
    .step-list li{display:grid;grid-template-columns:minmax(76px,.3fr) minmax(0,1fr);gap:18px;padding:17px 0;border-bottom:1px solid var(--border)}
    .step-list strong{font-size:15px;font-weight:650}
    .step-list span{color:var(--muted-foreground);font-size:14px}
    .controls-copy{max-width:840px}
    .controls-copy .eyebrow{margin-bottom:15px}
    .system-flow{display:grid;grid-template-columns:repeat(4,1fr);margin:40px 0 0;padding:0;border:1px solid var(--border);border-radius:var(--radius-card);background:var(--card);list-style:none}
    .system-flow li{min-width:0;padding:24px;border-left:1px solid var(--border)}
    .system-flow li:first-child{border-left:0}
    .system-flow b{color:var(--primary);font:620 12px/1.4 var(--font-mono)}
    .system-flow strong{display:block;margin-top:22px;font-size:16px;font-weight:650;letter-spacing:-.02em}
    .system-flow span{display:block;margin-top:6px;color:var(--muted-foreground);font-size:13px}
    .boundary-alert{display:grid;grid-template-columns:minmax(150px,.34fr) minmax(0,1fr);gap:24px;margin-top:18px;padding:18px 20px;border:1px solid #e3c1ba;border-radius:var(--radius-card);color:var(--danger);background:var(--danger-soft)}
    .boundary-alert strong{font-size:14px;font-weight:680}
    .boundary-alert p{margin:0;font-size:14px}
    .accordion{display:grid;gap:10px;margin-top:18px}
    .accordion details{border:1px solid var(--border);border-radius:var(--radius-card);background:var(--card)}
    .accordion summary{min-height:56px;display:flex;align-items:center;justify-content:space-between;gap:20px;padding:13px 16px;cursor:pointer;color:var(--foreground);font-weight:620;list-style:none;transition:background-color 160ms ease}
    .accordion summary::-webkit-details-marker{display:none}
    .accordion summary:after{content:"+";color:var(--primary);font:600 18px/1 var(--font-mono)}
    .accordion details[open] summary:after{content:"−"}
    .accordion-content{padding:0 16px 18px;color:var(--muted-foreground);font-size:14px}
    .receipt-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
    .receipt{padding:18px;border:1px solid var(--border);border-radius:var(--radius-control);background:var(--background)}
    .badge{display:inline-flex;align-items:center;min-height:26px;padding:4px 8px;border:1px solid currentColor;border-radius:999px;font:620 11px/1.2 var(--font-mono)}
    .badge[data-status="supported"]{color:var(--success);background:var(--success-soft)}
    .badge[data-status="review"]{color:var(--warning);background:var(--warning-soft)}
    .receipt dl{margin:14px 0 0}
    .receipt dl div{display:grid;grid-template-columns:minmax(110px,.6fr) minmax(0,1fr);gap:16px;padding:9px 0;border-top:1px solid var(--border)}
    .receipt dt{color:var(--muted-foreground)}
    .receipt dd{margin:0;color:var(--body)}
    .proof-links{display:flex;flex-wrap:wrap;gap:8px 18px;margin-top:16px}
    .proof-links a{min-height:44px;display:inline-flex;align-items:center;color:var(--foreground);font-weight:610;text-underline-offset:5px}
    .proof-grid{display:grid;grid-template-columns:repeat(12,1fr);gap:16px;margin-top:40px}
    .proof-cell{padding:26px;border:1px solid var(--border);border-radius:var(--radius-card);background:var(--card)}
    .proof-cell h3{margin:0;font-size:22px;font-weight:650;letter-spacing:-.03em}
    .proof-cell>p{margin:10px 0 0;color:var(--muted-foreground);font-size:14px}
    .proof-primary{grid-column:span 7;grid-row:span 2}
    .proof-limits,.proof-pilot{grid-column:span 5}
    .proof-limits{border-color:#e3c1ba;background:var(--danger-soft)}
    .proof-limits h3,.proof-limits p{color:var(--danger)}
    .test-metrics{display:grid;grid-template-columns:repeat(3,1fr);margin:22px 0 20px;padding:0;border-top:1px solid var(--border);border-bottom:1px solid var(--border);list-style:none}
    .test-metrics li{padding:17px;border-left:1px solid var(--border)}
    .test-metrics li:first-child{border-left:0;padding-left:0}
    .test-metrics strong{display:block;font:650 24px/1 var(--font-mono)}
    .test-metrics span{display:block;margin-top:6px;color:var(--muted-foreground);font-size:12px}
    .evidence-shot{overflow:hidden;border:1px solid var(--border);border-radius:var(--radius-control);background:var(--surface)}
    .evidence-shot img{width:100%;height:auto;display:block}
    .pilot-list{display:grid;grid-template-columns:1fr 1fr;gap:0 18px;margin:18px 0 0;padding:0;border-top:1px solid var(--border);list-style:none}
    .pilot-list li{padding:11px 0;border-bottom:1px solid var(--border);color:var(--body);font-size:13px}
    .founder{display:grid;grid-template-columns:minmax(280px,.7fr) minmax(0,1.3fr);gap:76px;padding-bottom:48px;border-bottom:1px solid var(--border)}
    .founder h2{margin:0;font-size:clamp(32px,3.8vw,46px);font-weight:650;line-height:1.08;letter-spacing:-.043em}
    .founder-copy p{max-width:680px;margin:0;color:var(--muted-foreground)}
    .reference-links{display:flex;flex-wrap:wrap;gap:8px 20px;margin-top:18px}
    .reference-links a{min-height:44px;display:inline-flex;align-items:center;color:var(--foreground);font-size:14px;font-weight:610;text-underline-offset:5px}
    .final-cta{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:48px;align-items:end;margin-top:24px;padding:38px;border:1px solid #e3c1ba;border-radius:var(--radius-product);background:var(--primary-soft)}
    .final-cta>*{min-width:0}
    .final-cta h2{max-width:720px;margin:0;font-size:clamp(34px,4vw,50px);font-weight:660;line-height:1.04;letter-spacing:-.045em}
    .final-cta p{max-width:620px;margin:14px 0 0;color:var(--body)}
    .final-cta .actions{margin-top:0}
    footer{padding:34px 0 42px;color:var(--muted-foreground);font-size:12px}
    .footer-row{display:flex;justify-content:space-between;gap:24px}
    .footer-row a{text-underline-offset:4px}
    @keyframes enter-copy{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
    @keyframes enter-product{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
    @media(hover:hover) and (pointer:fine){
      .button[data-variant="primary"]:hover{background:var(--primary-hover)}
      .button[data-variant="outline"]:hover,.button[data-variant="ghost"]:hover,.nav-links>a:not(.button):hover{border-color:var(--border-strong);background:var(--surface)}
      .text-link:hover,.proof-links a:hover,.reference-links a:hover{color:var(--primary)}
      .accordion summary:hover{background:var(--surface)}
    }
    @media(max-width:1179px){
      .hero-intro{grid-template-columns:minmax(0,1fr) minmax(240px,.48fr);gap:48px}
      .display{font-size:clamp(48px,6.4vw,68px)}
      .workflow-layout{grid-template-columns:1fr;gap:38px}
      .workflow-layout .product-frame{max-width:980px}
    }
    @media(max-width:900px){
      .section{padding:80px 0}
      .nav-links>a:not(.button){display:none}
      .problem-layout,.founder{grid-template-columns:1fr;gap:38px}
      .system-flow{grid-template-columns:1fr 1fr}
      .system-flow li:nth-child(3){border-left:0;border-top:1px solid var(--border)}
      .system-flow li:nth-child(4){border-top:1px solid var(--border)}
      .proof-primary{grid-column:span 12;grid-row:auto}
      .proof-limits,.proof-pilot{grid-column:span 6}
      .final-cta{grid-template-columns:1fr;gap:26px;align-items:start}
      .final-cta .actions{margin-top:0}
    }
    @media(max-width:640px){
      .container{width:calc(100% - 32px)}
      .site-nav{min-height:58px;gap:8px}
      .brand-copy span{display:none}
      .brand-copy strong{font-size:12px}
      .brand-mark{width:28px;height:28px}
      .nav-links .button{margin-left:0;padding-inline:10px;font-size:12px}
      .hero{padding-top:24px}
      .hero-intro{grid-template-columns:1fr;gap:0}
      .hero-context{display:none}
      .display{font-size:clamp(40px,12.2vw,47px);line-height:1.02}
      .lead{margin-top:16px;font-size:17px;line-height:1.42}
      .hero-copy .actions{margin-top:20px}
      .hero-copy .text-link{display:none}
      .hero-product{margin-top:22px}
      .product-frame{padding:8px;border-radius:var(--radius-card)}
      .product-frame figcaption{display:grid;gap:3px}
      .sample-metrics{grid-template-columns:1fr 1fr;margin-top:22px}
      .sample-metrics li{padding:16px 0;border-left:0;border-top:1px solid var(--border)}
      .sample-metrics li:nth-child(1),.sample-metrics li:nth-child(2){border-top:0}
      .sample-metrics li:nth-child(even){padding-left:16px;border-left:1px solid var(--border)}
      .section{padding:66px 0}
      .section-title{font-size:clamp(34px,10.5vw,43px)}
      .workflow-copy .section-title{font-size:clamp(34px,10vw,42px)}
      .system-flow{grid-template-columns:1fr}
      .system-flow li{border-left:0;border-top:1px solid var(--border)}
      .system-flow li:first-child{border-top:0}
      .boundary-alert{grid-template-columns:1fr;gap:7px}
      .receipt-grid,.pilot-list{grid-template-columns:1fr}
      .receipt dl div{grid-template-columns:1fr;gap:3px}
      .proof-limits,.proof-pilot{grid-column:span 12}
      .proof-cell{padding:22px 20px}
      .test-metrics{grid-template-columns:1fr}
      .test-metrics li{padding:14px 0;border-left:0;border-top:1px solid var(--border)}
      .test-metrics li:first-child{border-top:0}
      .actions{align-items:stretch;flex-direction:column}
      .actions .button,.actions .text-link{width:100%;text-align:center}
      .actions .button{white-space:normal}
      .text-link{justify-content:center}
      .founder{padding-bottom:36px}
      .final-cta{padding:28px 20px}
      .footer-row{display:grid;gap:8px}
    }
    @media(max-width:360px){
      .brand-copy strong{max-width:118px;line-height:1.05}
      .display{font-size:39px}
      .nav-links .button{padding-inline:8px}
    }
    @media(prefers-reduced-motion:reduce){
      html{scroll-behavior:auto}
      .hero-copy,.hero-product{animation:none}
      .button,.text-link{transition-property:background-color,color,border-color}
      .button:active,.text-link:active{transform:none}
    }
    @media(prefers-reduced-transparency:reduce){.site-header{background:var(--background);backdrop-filter:none}}
    @media(prefers-contrast:more){
      .site-header{background:var(--background);backdrop-filter:none}
      .button,.product-frame,.system-flow,.proof-cell,.final-cta,.accordion details{border-width:2px}
      .lead,.section-lead,.problem-list p,.step-list span{color:var(--foreground)}
    }
    """


def _finish(template: str) -> str:
    return (
        template.replace("__STYLES__", _shared_styles().strip())
        .replace("__VERSION__", VERSION)
        .replace("__UPDATED_DATE__", UPDATED_DATE)
        .replace("__UPDATED_LABEL__", UPDATED_LABEL)
        .replace("__SOCIAL_CARD__", SOCIAL_CARD)
    )


def render_product_landing_v21() -> str:
    return _finish(
        """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <meta name="theme-color" content="#f6f7f5">
  <meta name="description" content="Catch approval, destination, placement, UTM, format and naming issues before a Meta creative launch reaches Ads Manager.">
  <meta name="author" content="Mathieu Petroni">
  <link rel="canonical" href="https://mattyu-dev.github.io/creative-launch-workspace/">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
  <link rel="preload" href="assets/geist-latin-variable.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="me" href="https://www.linkedin.com/in/mathieu-petroni/">
  <link rel="me" href="https://github.com/mattyu-dev">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Creative Launch Workspace">
  <meta property="og:title" content="Catch launch blockers before Ads Manager">
  <meta property="og:description" content="Check every creative row, route detected exceptions and keep uncertain calls human.">
  <meta property="og:url" content="https://mattyu-dev.github.io/creative-launch-workspace/">
  <meta property="og:image" content="https://mattyu-dev.github.io/creative-launch-workspace/assets/__SOCIAL_CARD__">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Creative Launch Workspace pre-launch review queue">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Catch launch blockers before Ads Manager">
  <meta name="twitter:description" content="Pre-launch QA for Meta creative teams.">
  <meta name="twitter:image" content="https://mattyu-dev.github.io/creative-launch-workspace/assets/__SOCIAL_CARD__">
  <meta name="twitter:image:alt" content="Creative Launch Workspace pre-launch review queue">
  <title>Creative Launch Workspace | Pre-launch QA for Meta creative teams</title>
  <script type="application/ld+json">
  {"@context":"https://schema.org","@graph":[{"@type":"Person","@id":"https://mattyu-dev.github.io/creative-launch-workspace/#mathieu","name":"Mathieu Petroni","jobTitle":"AI Automation Builder","url":"https://www.linkedin.com/in/mathieu-petroni/","sameAs":["https://www.linkedin.com/in/mathieu-petroni/","https://github.com/mattyu-dev"]},{"@type":"SoftwareApplication","@id":"https://mattyu-dev.github.io/creative-launch-workspace/#software","name":"Creative Launch Workspace","applicationCategory":"BusinessApplication","operatingSystem":"Web","description":"Pre-launch review workflow for high-volume Meta creative operations.","softwareVersion":"__VERSION__","author":{"@id":"https://mattyu-dev.github.io/creative-launch-workspace/#mathieu"}},{"@type":"WebSite","@id":"https://mattyu-dev.github.io/creative-launch-workspace/#website","name":"Creative Launch Workspace","url":"https://mattyu-dev.github.io/creative-launch-workspace/","dateModified":"__UPDATED_DATE__","about":{"@id":"https://mattyu-dev.github.io/creative-launch-workspace/#software"}}]}
  </script>
  <style>__STYLES__</style>
</head>
<body>
  <a class="skip-link" href="#main">Skip to the product</a>
  <header class="site-header">
    <nav class="container site-nav" aria-label="Primary navigation">
      <a class="brand" href="#product"><span class="brand-mark" aria-hidden="true"></span><span class="brand-copy"><strong>Creative Launch Workspace</strong><span>Pre-launch creative QA</span></span></a>
      <div class="nav-links"><a href="#product">Product</a><a href="#workflow">How it works</a><a href="#controls">Controls</a><a href="#proof">Proof</a><a class="button" data-variant="primary" href="workspace.html?guided=1">Review sample</a></div>
    </nav>
  </header>
  <main id="main">
    <section class="container hero" id="product" aria-labelledby="hero-title">
      <div class="hero-intro">
        <div class="hero-copy">
          <div class="eyebrow">Pre-launch QA for Meta creative teams</div>
          <h1 class="display" id="hero-title">Catch launch blockers before Ads Manager.</h1>
          <p class="lead">Check every creative row for approval, destination, placement, UTM, format and naming issues. Route each detected exception and hold uncertain calls for human review before campaign build.</p>
          <div class="actions"><a class="button" data-variant="primary" href="workspace.html?guided=1">Review a sample</a><a class="text-link" href="#workflow">See how it works</a></div>
        </div>
        <dl class="hero-context">
          <div><dt>Input</dt><dd>Campaign brief and creative manifest</dd></div>
          <div><dt>Review state</dt><dd>Issue, owner, proposed fix and decision</dd></div>
          <div><dt>Output</dt><dd>Review-only local receipt</dd></div>
        </dl>
      </div>
      <div class="hero-product">
        <figure class="product-frame">
          <div class="product-window"><a href="workspace.html?guided=1"><picture>
            <source media="(max-width:720px)" type="image/webp" srcset="assets/workspace-mobile-hero.webp 780w" sizes="calc(100vw - 50px)">
            <source media="(max-width:720px)" type="image/png" srcset="assets/workspace-mobile-hero.png 780w" sizes="calc(100vw - 50px)">
            <source type="image/avif" srcset="assets/workspace-desktop.avif 1440w" sizes="(max-width:1240px) calc(100vw - 88px), 1216px">
            <source type="image/webp" srcset="assets/workspace-desktop.webp 1440w" sizes="(max-width:1240px) calc(100vw - 88px), 1216px">
            <img src="assets/workspace-desktop.png" width="1440" height="1000" alt="Creative review queue with detected exceptions, owners and human decision controls" decoding="async" fetchpriority="high">
          </picture></a></div>
          <figcaption><strong>Interactive sample workspace</strong><span>Committed deterministic fixture. No live model, Meta credentials or publishing path.</span></figcaption>
        </figure>
      </div>
      <ul class="sample-metrics" aria-label="Inside the interactive sample">
        <li><strong>100</strong><span>creative rows in one review queue</span></li>
        <li><strong>30</strong><span>pass the current offline checks</span></li>
        <li><strong>60</strong><span>blocked with an issue, owner and action</span></li>
        <li><strong>10</strong><span>held for a human decision</span></li>
      </ul>
    </section>

    <section class="section" id="problem" aria-labelledby="problem-title">
      <div class="container problem-layout">
        <div>
          <h2 class="section-title" id="problem-title">Every blocker needs evidence, an owner and a decision.</h2>
          <p class="section-lead">Campaign truth is spread across briefs, manifests and approval threads. When context separates, avoidable issues surface after trafficking starts.</p>
        </div>
        <ul class="problem-list">
          <li><h3>Evidence</h3><p>Destinations, approvals and placement requirements drift across sources.</p></li>
          <li><h3>Ownership</h3><p>An exception becomes visible, but no one owns the next action.</p></li>
          <li><h3>Judgment</h3><p>Uncertain mappings are guessed instead of being routed for review.</p></li>
        </ul>
      </div>
    </section>

    <section class="section" id="workflow" aria-labelledby="workflow-title">
      <div class="container workflow-layout">
        <figure class="product-frame">
          <div class="product-window"><picture>
            <source media="(max-width:720px)" type="image/webp" srcset="assets/guided-receipt-mobile.webp 960w" sizes="calc(100vw - 50px)">
            <source media="(max-width:720px)" type="image/png" srcset="assets/guided-receipt-mobile.png 960w" sizes="calc(100vw - 50px)">
            <img src="assets/guided-review-step-3.png" width="1280" height="900" loading="lazy" decoding="async" alt="Completed human review with owner, decision state and local audit receipt">
          </picture></div>
          <figcaption><strong>One accountable review loop</strong><span>The issue, next action and local receipt stay together.</span></figcaption>
        </figure>
        <div class="workflow-copy">
          <h2 class="section-title" id="workflow-title">Find the blocker. Route the fix. Record the decision.</h2>
          <ol class="step-list">
            <li><strong>Find</strong><span>Checks separate passing rows from detected exceptions.</span></li>
            <li><strong>Route</strong><span>The issue, owner and required fix stay together.</span></li>
            <li><strong>Decide</strong><span>A reviewer makes the uncertain call and records it.</span></li>
          </ol>
          <div class="actions"><a class="button" data-variant="outline" href="workspace.html?guided=1">Review one decision</a></div>
        </div>
      </div>
    </section>

    <section class="section" id="controls" aria-labelledby="controls-title">
      <div class="container">
        <div class="controls-copy">
          <div class="eyebrow">Guardrails built in</div>
          <h2 class="section-title" id="controls-title">AI proposes. Rules verify. People decide.</h2>
          <p class="section-lead">AI is limited to an evidence-backed mapping proposal. Deterministic policy checks every field, and uncertainty cannot advance without a reviewer.</p>
        </div>
        <ol class="system-flow" aria-label="Governed review architecture">
          <li><b>Evidence</b><strong>Ground the input</strong><span>Values link to source evidence or remain empty.</span></li>
          <li><b>Proposal</b><strong>Assist, never approve</strong><span>The model proposes bounded typed values.</span></li>
          <li><b>Policy</b><strong>Fail closed in code</strong><span>Schema, evidence and allowlists own the state.</span></li>
          <li><b>Decision</b><strong>Keep authority human</strong><span>Accept, return or block with a local receipt.</span></li>
        </ol>
        <div class="boundary-alert" role="note" aria-label="Public sample boundary"><strong>Public sample boundary</strong><p>This public sample uses synthetic data and cannot call Meta, load tokens or publish ads.</p></div>
        <div class="accordion" aria-label="Product evidence disclosures">
          <details>
            <summary>Inspect a supported proposal and an abstention</summary>
            <div class="accordion-content">
              <div class="receipt-grid">
                <article class="receipt"><span class="badge" data-status="supported">Supported</span><dl><div><dt>Objective</dt><dd><code>traffic</code></dd></div><div><dt>Source evidence</dt><dd>“traffic”</dd></div><div><dt>Review</dt><dd>Accepted by reviewer</dd></div></dl></article>
                <article class="receipt"><span class="badge" data-status="review">Input required</span><dl><div><dt>Destination URL</dt><dd>Not found in source</dd></div><div><dt>Proposal</dt><dd>No value proposed</dd></div><div><dt>Next action</dt><dd>Human input before materialization</dd></div></dl></article>
              </div>
            </div>
          </details>
          <details>
            <summary>Open the architecture and threat model</summary>
            <div class="accordion-content"><p>The field receipt, system boundaries, evaluation protocol and threat model remain inspectable.</p><div class="proof-links"><a href="brief-evidence.html">Field-level evidence</a><a href="https://github.com/mattyu-dev/creative-launch-workspace/blob/main/docs/architecture/system.md">Architecture</a><a href="https://github.com/mattyu-dev/creative-launch-workspace/blob/main/docs/security/threat_model.md">Threat model</a><a href="https://github.com/mattyu-dev/creative-launch-workspace/actions">Tests and CI</a></div></div>
          </details>
        </div>
      </div>
    </section>

    <section class="section" id="proof" aria-labelledby="proof-title">
      <div class="container">
        <h2 class="section-title" id="proof-title">Inspect the product. Check the evidence.</h2>
        <p class="section-lead">The public workspace proves the interaction, validation contracts and trust boundaries. It does not claim customer or production results.</p>
        <div class="proof-grid">
          <article class="proof-cell proof-primary">
            <h3>Verified in the sample</h3>
            <p>The public flow, validation contracts and browser behavior are reproducibly tested.</p>
            <ul class="test-metrics"><li><strong>64</strong><span>automated tests</span></li><li><strong>7</strong><span>responsive browser widths</span></li><li><strong>100/100</strong><span>local Lighthouse accessibility</span></li></ul>
            <div class="evidence-shot"><img src="assets/brief-evidence.png" width="1440" height="1794" loading="lazy" decoding="async" alt="Field-level evidence receipt with accepted values and source quotes"></div>
          </article>
          <article class="proof-cell proof-limits"><h3>Honest limits</h3><p>Synthetic sample, browser-local review state, no customer data, no Meta credentials and no publishing path. No production telemetry.</p></article>
          <article class="proof-cell proof-pilot"><h3>What a pilot should measure</h3><ul class="pilot-list"><li>Review cycle time</li><li>Late exception rate</li><li>First-pass readiness</li><li>Decision latency</li><li>False-positive reversals</li><li>Reviewer effort per 100 creatives</li></ul></article>
        </div>
      </div>
    </section>

    <section class="section closing" id="about" aria-labelledby="about-title">
      <div class="container">
        <div class="founder">
          <h2 id="about-title">Designed by a performance marketer. Implemented end to end.</h2>
          <div class="founder-copy"><p>Mathieu Petroni brought growth and performance marketing experience since 2017 to the product strategy, AI safeguards, Python contracts, browser experience, accessibility and CI.</p><div class="reference-links"><a href="https://github.com/mattyu-dev/creative-launch-workspace">Source repository</a><a href="https://github.com/mattyu-dev/creative-launch-workspace/actions">Tests and CI</a><a href="https://github.com/mattyu-dev/creative-launch-workspace/tree/main/docs">Engineering docs</a><a href="https://github.com/mattyu-dev" rel="me external">GitHub profile</a></div></div>
        </div>
        <div class="final-cta">
          <div><h2>Review one launch decision in two minutes.</h2><p>Inspect the exception, choose the next action and keep the local receipt.</p></div>
          <div class="actions"><a class="button" data-variant="primary" href="workspace.html?guided=1">Review a sample batch</a><a class="button" data-variant="outline" href="https://www.linkedin.com/in/mathieu-petroni/" rel="me external">Discuss a pilot</a></div>
        </div>
      </div>
    </section>
  </main>
  <footer><div class="container footer-row"><span>Creative Launch Workspace by <a href="https://www.linkedin.com/in/mathieu-petroni/" rel="me external">Mathieu Petroni</a></span><span>MIT licensed. Interactive sample. No publishing path. <a href="https://github.com/mattyu-dev/creative-launch-workspace">Source</a></span></div></footer>
</body>
</html>
"""
    )


def render_social_card_page_v21() -> str:
    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=1200, initial-scale=1"><meta name="author" content="Mathieu Petroni"><style>
@font-face{font-family:"Geist";src:url("assets/geist-latin-variable.woff2") format("woff2");font-weight:100 900;font-display:swap}@font-face{font-family:"Geist Mono";src:url("assets/geist-mono-latin-variable.woff2") format("woff2");font-weight:100 900;font-display:swap}*{box-sizing:border-box}html,body{margin:0;width:1200px;height:630px;overflow:hidden}body{color:#151817;background:#f6f7f5;font-family:"Geist",system-ui,sans-serif}main{width:1200px;height:630px;display:grid;grid-template-columns:510px 690px}.copy{padding:54px 38px 42px 56px;display:flex;flex-direction:column}.brand{display:flex;align-items:center;gap:12px}.mark{width:31px;height:31px;position:relative;border:1px solid #b8c0ba;border-radius:8px;background:#fff}.mark:before{content:"";position:absolute;inset:7px;border:2px solid #c83b24;border-right-color:transparent}.brand strong{font-size:16px;font-weight:680}.eyebrow{margin-top:66px;color:#c83b24;font:650 12px/1.4 "Geist Mono",monospace;letter-spacing:.06em;text-transform:uppercase}.hero h1{margin:15px 0 0;font-size:53px;line-height:1;letter-spacing:-2.8px;font-weight:660}.hero p{max-width:405px;margin:20px 0 0;color:#3e4541;font-size:17px;line-height:1.45}.copy footer{display:flex;justify-content:space-between;margin-top:auto;color:#636b66;font-size:11px}.visual{padding:48px 48px 48px 0;display:flex;align-items:center}.frame{width:100%;padding:12px;border:1px solid #b8c0ba;border-radius:18px;background:#fff;box-shadow:0 24px 72px rgba(21,24,23,.11)}.frame img{width:100%;height:auto;display:block;border:1px solid #d8ddd9;border-radius:12px}.frame p{display:flex;justify-content:space-between;margin:10px 2px 0;color:#636b66;font-size:10px}.frame strong{color:#151817;font-weight:630}
</style></head><body><main><section class="copy"><div class="brand"><span class="mark"></span><strong>Creative Launch Workspace</strong></div><div class="hero"><div class="eyebrow">Pre-launch QA for Meta creative teams</div><h1>Catch launch blockers before Ads Manager.</h1><p>Check every creative row, route each exception and keep uncertain calls human.</p></div><footer><strong>Interactive sample</strong><span>Built by Mathieu Petroni</span></footer></section><div class="visual"><div class="frame"><img src="assets/workspace-desktop.png" alt=""><p><strong>100-row review workspace</strong><span>No publishing path</span></p></div></div></main></body></html>
"""
