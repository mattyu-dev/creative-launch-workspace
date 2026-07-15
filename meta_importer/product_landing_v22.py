from __future__ import annotations

VERSION = "2.2.0"
UPDATED_DATE = "2026-07-15"
SOCIAL_CARD = "social-card-v2-2.png"


def _shared_styles() -> str:
    return """
    @font-face{font-family:"Mona Sans";src:url("assets/mona-sans-latin-variable.woff2") format("woff2-variations");font-style:normal;font-weight:200 900;font-display:optional}
    @font-face{font-family:"Geist Mono";src:url("assets/geist-mono-latin-variable.woff2") format("woff2");font-style:normal;font-weight:100 900;font-display:swap}
    :root{
      color-scheme:light;
      --canvas:oklch(97.5% .006 315);
      --surface:oklch(100% 0 0);
      --surface-tint:oklch(95.5% .014 315);
      --ink:oklch(19% .032 315);
      --plum:oklch(21% .055 315);
      --plum-raised:oklch(26% .062 315);
      --plum-muted:oklch(77% .025 315);
      --lemon:oklch(91% .17 100);
      --lemon-hover:oklch(86% .17 100);
      --lemon-pressed:oklch(80% .16 100);
      --fuchsia:oklch(57% .216 4);
      --fuchsia-text:oklch(44% .17 4);
      --lavender:oklch(82% .08 292);
      --lavender-soft:oklch(94% .035 292);
      --muted:oklch(49% .02 315);
      --border:oklch(87% .016 315);
      --border-strong:oklch(73% .026 315);
      --success:oklch(46% .11 155);
      --warning:oklch(54% .12 77);
      --danger:oklch(48% .16 28);
      --sans:"Mona Sans",system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
      --mono:"Geist Mono",ui-monospace,"SFMono-Regular",Consolas,monospace;
      --ease:cubic-bezier(.23,1,.32,1);
      --radius-control:9px;
      --radius-panel:14px;
      --radius-stage:20px;
    }
    *{box-sizing:border-box}
    html{scroll-behavior:smooth}
    body{margin:0;color:var(--ink);background:var(--canvas);font:400 16px/1.58 var(--sans);letter-spacing:-.01em;-webkit-font-smoothing:antialiased}
    h1,h2,h3,p,a,strong,span,li,dd,dt{overflow-wrap:anywhere}
    h1,h2,h3,p{margin-top:0}
    a{color:inherit}
    a:focus-visible,button:focus-visible{outline:3px solid var(--fuchsia);outline-offset:3px}
    button{font:inherit}
    [hidden]{display:none!important}
    .container{width:min(1248px,calc(100% - 64px));margin-inline:auto}
    .skip-link{position:fixed;left:16px;top:-80px;z-index:100;min-height:44px;display:flex;align-items:center;padding:8px 14px;border-radius:var(--radius-control);color:var(--ink);background:var(--lemon);font-weight:760}
    .skip-link:focus{top:14px}
    .site-header{position:sticky;top:0;z-index:30;border-bottom:1px solid color-mix(in oklch,var(--border) 82%,transparent);background:color-mix(in oklch,var(--canvas) 94%,transparent);backdrop-filter:blur(14px)}
    .site-nav{min-height:68px;display:flex;align-items:center;justify-content:space-between;gap:24px}
    .brand{min-height:44px;display:inline-flex;align-items:center;gap:11px;text-decoration:none}
    .brand-mark{width:34px;height:34px;position:relative;flex:0 0 auto;border:1px solid var(--border-strong);border-radius:8px;background:var(--surface)}
    .brand-mark:before,.brand-mark:after{content:"";position:absolute;left:6px;width:9px;height:1px;background:var(--plum)}
    .brand-mark:before{top:9px;box-shadow:0 7px 0 var(--plum),0 14px 0 var(--plum)}
    .brand-mark:after{left:19px;top:13px;width:8px;box-shadow:0 8px 0 var(--plum)}
    .brand-checkpoint{position:absolute;left:14px;top:13px;width:7px;height:8px;background:var(--lemon);border:1px solid var(--plum)}
    .brand-copy{display:grid;line-height:1.08}
    .brand-copy strong{font-size:14px;font-weight:770;letter-spacing:-.02em}
    .brand-copy span{margin-top:4px;color:var(--muted);font-size:11px}
    .nav-links{display:flex;align-items:center;gap:2px}
    .nav-links>a:not(.button){min-height:44px;display:inline-flex;align-items:center;padding:0 10px;border-radius:var(--radius-control);color:var(--muted);font-size:13px;font-weight:620;text-decoration:none}
    .nav-links .button{margin-left:8px}
    .button{min-height:44px;display:inline-flex;align-items:center;justify-content:center;gap:9px;padding:10px 16px;border:1px solid transparent;border-radius:var(--radius-control);font-size:14px;font-weight:760;line-height:1.15;text-decoration:none;transition:transform 140ms var(--ease),background-color 160ms ease,color 160ms ease,border-color 160ms ease}
    .button-arrow{display:inline-block;transition:transform 160ms var(--ease)}
    .button[data-variant="primary"]{border-color:color-mix(in oklch,var(--plum) 22%,transparent);color:var(--ink);background:var(--lemon)}
    .button[data-variant="outline"]{border-color:var(--border-strong);color:var(--ink);background:transparent}
    .button[data-on-dark="true"]{border-color:color-mix(in oklch,var(--surface) 32%,transparent);color:var(--surface)}
    .button:active{transform:scale(.97)}
    .button[data-variant="primary"]:active{background:var(--lemon-pressed)}
    .text-link{min-height:44px;display:inline-flex;align-items:center;gap:8px;color:var(--ink);font-size:14px;font-weight:720;text-underline-offset:5px;transition:transform 140ms var(--ease),color 160ms ease}
    .text-link:active{transform:scale(.97)}
    .hero{padding:48px 0 64px;overflow:hidden}
    .hero-grid{display:grid;grid-template-columns:minmax(390px,.78fr) minmax(0,1fr);gap:52px;align-items:center}
    .hero-copy{min-width:0;animation:hero-enter 320ms var(--ease) both}
    .eyebrow{margin-bottom:18px;color:var(--fuchsia-text);font:650 11px/1.4 var(--mono);letter-spacing:.075em;text-transform:uppercase}
    .display{max-width:580px;margin:0;font-size:clamp(52px,5.25vw,72px);font-weight:760;line-height:.97;letter-spacing:-.035em;text-wrap:balance}
    .lead{max-width:610px;margin:24px 0 0;color:var(--muted);font-size:18px;line-height:1.54}
    .actions{display:flex;flex-wrap:wrap;align-items:center;gap:10px 18px;margin-top:30px}
    .hero-stage{min-width:0;position:relative;padding:36px 18px 18px;border-radius:var(--radius-stage);background:var(--plum);box-shadow:0 28px 80px color-mix(in oklch,var(--plum) 20%,transparent);animation:stage-enter 360ms 50ms var(--ease) both}
    .route-track{height:16px;position:absolute;left:24px;right:24px;top:13px;display:grid;grid-template-columns:1fr 14px 1fr;align-items:center}
    .route-track:before,.route-track:after{content:"";height:1px;background:color-mix(in oklch,var(--surface) 25%,transparent)}
    .route-track span{width:10px;height:10px;justify-self:center;border:1px solid color-mix(in oklch,var(--surface) 60%,transparent);background:var(--lemon);transform:rotate(45deg)}
    .stage-label{position:absolute;right:28px;top:10px;color:var(--plum-muted);font:560 10px/1.3 var(--mono);letter-spacing:.04em}
    .product-window{height:510px;overflow:hidden;border:1px solid color-mix(in oklch,var(--surface) 24%,transparent);border-radius:12px;background:var(--surface)}
    .product-window a{height:100%;display:block}
    .product-window picture{width:100%;display:block}
    .product-window img{width:100%;height:auto;display:block}
    .stage-footer{display:flex;justify-content:space-between;gap:18px;padding:12px 3px 0;color:var(--plum-muted);font:520 11px/1.4 var(--mono)}
    .stage-footer strong{color:var(--surface);font-weight:650}
    .section{padding:112px 0;border-top:1px solid var(--border)}
    .section-title{max-width:720px;margin:0;font-size:clamp(42px,4.4vw,58px);font-weight:750;line-height:1;letter-spacing:-.035em;text-wrap:balance}
    .section-lead{max-width:660px;margin:22px 0 0;color:var(--muted);font-size:18px}
    .handoff-grid{display:grid;grid-template-columns:minmax(320px,.72fr) minmax(0,1fr);gap:96px;align-items:start}
    .handoff-copy{position:sticky;top:104px}
    .handoff-list{margin:0;padding:0;border-top:1px solid var(--border-strong);list-style:none}
    .handoff-list li{position:relative;padding:28px 0;border-bottom:1px solid var(--border)}
    .handoff-list h3{margin:0;font-size:24px;font-weight:720;letter-spacing:-.025em}
    .handoff-list p{max-width:540px;margin:8px 0 0;color:var(--muted)}
    .workflow{color:var(--surface);background:var(--plum)}
    .workflow .section-title{max-width:880px}
    .workflow .section-lead{color:var(--plum-muted)}
    .workflow-steps{display:grid;grid-template-columns:repeat(4,1fr);margin:48px 0 0;padding:0;border-top:1px solid color-mix(in oklch,var(--surface) 24%,transparent);list-style:none;counter-reset:workflow}
    .workflow-steps li{min-width:0;position:relative;padding:22px 28px 26px 0;border-bottom:1px solid color-mix(in oklch,var(--surface) 24%,transparent);counter-increment:workflow}
    .workflow-steps li:not(:last-child):after{content:"";position:absolute;right:13px;top:28px;width:24px;height:1px;background:var(--lemon)}
    .workflow-steps b{color:var(--lemon);font:650 11px/1.4 var(--mono)}
    .workflow-steps b:before{content:"0" counter(workflow) "  ";color:var(--plum-muted)}
    .workflow-steps strong{display:block;margin-top:17px;font-size:18px;font-weight:720}
    .workflow-steps span{display:block;margin-top:7px;color:var(--plum-muted);font-size:13px;line-height:1.5}
    .product-demo{display:grid;grid-template-columns:230px minmax(0,1fr);gap:20px;margin-top:56px;padding:18px;border:1px solid color-mix(in oklch,var(--surface) 25%,transparent);border-radius:var(--radius-stage);background:var(--plum-raised)}
    .product-tabs{display:flex;flex-direction:column;gap:8px;padding:6px}
    .product-tab{min-height:64px;display:grid;grid-template-columns:34px 1fr;align-items:center;gap:10px;padding:10px 12px;border:1px solid transparent;border-radius:10px;color:var(--plum-muted);background:transparent;text-align:left;cursor:pointer;transition:background-color 160ms ease,color 160ms ease,border-color 160ms ease}
    .product-tab span:first-child{font:650 11px/1 var(--mono)}
    .product-tab span:last-child{font-size:14px;font-weight:690}
    .product-tab[aria-selected="true"]{border-color:color-mix(in oklch,var(--lemon) 45%,transparent);color:var(--surface);background:color-mix(in oklch,var(--surface) 7%,transparent)}
    .demo-panel{min-width:0}
    .demo-frame{height:520px;overflow:hidden;border:1px solid color-mix(in oklch,var(--surface) 25%,transparent);border-radius:12px;background:var(--canvas)}
    .demo-frame img{width:100%;height:auto;display:block}
    .demo-frame[data-view="queue"] img{width:130%;transform:translate(-6%,-1%)}
    .demo-frame[data-view="review"] img,.demo-frame[data-view="receipt"] img{width:116%;transform:translate(-7%,-1%)}
    .demo-caption{display:flex;justify-content:space-between;gap:24px;margin:12px 3px 0;color:var(--plum-muted);font-size:12px}
    .demo-caption strong{color:var(--surface)}
    .controls-grid{display:grid;grid-template-columns:minmax(310px,.68fr) minmax(0,1fr);gap:86px;align-items:start}
    .control-system{margin-top:4px;border-top:1px solid var(--border-strong)}
    .control-row{display:grid;grid-template-columns:46px minmax(150px,.42fr) minmax(0,1fr);gap:18px;padding:22px 0;border-bottom:1px solid var(--border)}
    .control-row>span{width:32px;height:32px;display:grid;place-items:center;border:1px solid var(--border-strong);border-radius:8px;background:var(--surface);font:650 11px/1 var(--mono)}
    .control-row:nth-child(2)>span{background:var(--lavender-soft)}
    .control-row:nth-child(3)>span{background:var(--lemon)}
    .control-row h3{margin:4px 0 0;font-size:18px;font-weight:720}
    .control-row p{margin:3px 0 0;color:var(--muted);font-size:14px}
    .evidence-layout{display:grid;grid-template-columns:minmax(0,1fr) minmax(300px,.58fr);gap:72px;align-items:start;margin-top:48px}
    .evidence-frame{height:570px;overflow:hidden;border:1px solid var(--border-strong);border-radius:var(--radius-panel);background:var(--surface)}
    .evidence-frame img{width:100%;height:auto;display:block}
    .evidence-list{margin:0;padding:0;border-top:1px solid var(--border-strong);list-style:none}
    .evidence-list li{padding:22px 0;border-bottom:1px solid var(--border)}
    .evidence-list strong{display:block;font-size:17px;font-weight:720}
    .evidence-list p{margin:6px 0 0;color:var(--muted);font-size:14px}
    .evidence-links{display:flex;flex-wrap:wrap;gap:8px 20px;margin-top:24px}
    .evidence-links a{min-height:44px;display:inline-flex;align-items:center;font-weight:700;text-underline-offset:5px}
    .closing{padding:96px 0 56px}
    .closing-panel{position:relative;overflow:hidden;display:grid;grid-template-columns:minmax(0,1fr) auto;gap:56px;align-items:end;padding:56px;border-radius:var(--radius-stage);color:var(--surface);background:var(--plum)}
    .closing-panel:after{content:"";position:absolute;right:-36px;top:-44px;width:150px;height:150px;border:26px solid var(--fuchsia);transform:rotate(24deg);opacity:.75}
    .closing-panel h2{max-width:760px;margin:0;font-size:clamp(40px,4.6vw,62px);font-weight:750;line-height:.98;letter-spacing:-.035em;text-wrap:balance}
    .closing-panel p{max-width:620px;margin:18px 0 0;color:var(--plum-muted);font-size:17px}
    .closing-panel .actions{position:relative;z-index:1;margin-top:0}
    footer{padding:28px 0 40px;color:var(--muted);font-size:12px}
    .footer-row{display:flex;justify-content:space-between;gap:24px}
    .footer-row a{text-underline-offset:4px}
    @keyframes hero-enter{from{transform:translateY(8px)}to{transform:translateY(0)}}
    @keyframes stage-enter{from{transform:translateY(10px)}to{transform:translateY(0)}}
    @media(hover:hover) and (pointer:fine){
      .button[data-variant="primary"]:hover{background:var(--lemon-hover)}
      .button:hover .button-arrow{transform:translateX(2px)}
      .button[data-variant="outline"]:hover,.nav-links>a:not(.button):hover{border-color:var(--border-strong);background:var(--surface-tint)}
      .button[data-on-dark="true"]:hover{background:color-mix(in oklch,var(--surface) 8%,transparent)}
      .text-link:hover,.evidence-links a:hover{color:var(--fuchsia-text)}
      .product-tab:hover{color:var(--surface);background:color-mix(in oklch,var(--surface) 6%,transparent)}
    }
    @media(max-width:1120px){
      .hero-grid{grid-template-columns:minmax(360px,.76fr) minmax(0,1fr);gap:32px}
      .product-window{height:460px}
      .display{font-size:clamp(50px,5.8vw,66px)}
      .handoff-grid,.controls-grid{gap:56px}
      .product-demo{grid-template-columns:190px minmax(0,1fr)}
    }
    @media(max-width:900px){
      .section{padding:88px 0}
      .nav-links>a:not(.button){display:none}
      .hero-grid,.handoff-grid,.controls-grid,.evidence-layout{grid-template-columns:1fr}
      .hero-grid{gap:40px}
      .hero-copy{max-width:720px}
      .hero-stage{max-width:760px}
      .handoff-copy{position:static}
      .workflow-steps{grid-template-columns:1fr 1fr}
      .workflow-steps li:nth-child(2):after{display:none}
      .product-demo{grid-template-columns:1fr}
      .product-tabs{display:grid;grid-template-columns:repeat(3,1fr)}
      .product-tab{min-height:52px;grid-template-columns:1fr;padding:8px;text-align:center}
      .product-tab span:first-child{display:none}
      .closing-panel{grid-template-columns:1fr;gap:30px;align-items:start}
      .closing-panel .actions{margin-top:0}
    }
    @media(max-width:640px){
      .container{width:calc(100% - 32px)}
      .site-nav{min-height:60px;gap:8px}
      .brand-copy span{display:none}
      .brand-copy strong{font-size:12px}
      .brand-mark{width:30px;height:30px}
      .nav-links .button{display:none}
      .hero{padding:28px 0 48px}
      .display{font-size:clamp(42px,12.5vw,50px);line-height:.98}
      .lead{margin-top:18px;font-size:17px;line-height:1.45}
      .actions{align-items:stretch;flex-direction:column;margin-top:22px}
      .actions .button,.actions .text-link{width:100%;justify-content:center;text-align:center}
      .hero-grid{gap:24px}
      .hero-stage{padding:28px 8px 10px;border-radius:var(--radius-panel)}
      .route-track{left:15px;right:15px;top:9px}
      .stage-label{display:none}
      .product-window{height:260px;border-radius:8px}
      .stage-footer{display:grid;gap:2px;padding:8px 2px 0;font-size:9px}
      .section{padding:68px 0}
      .section-title{font-size:clamp(38px,11vw,46px)}
      .section-lead{margin-top:18px;font-size:17px}
      .handoff-list li{padding:22px 0}
      .handoff-list h3{font-size:21px}
      .workflow-steps{grid-template-columns:1fr}
      .workflow-steps li{padding-right:0}
      .workflow-steps li:not(:last-child):after{left:5px;right:auto;top:auto;bottom:-9px;width:1px;height:18px}
      .product-demo{margin-top:38px;padding:8px;border-radius:var(--radius-panel)}
      .product-tabs{gap:4px;padding:2px}
      .product-tab{font-size:12px}
      .demo-frame{height:280px;border-radius:8px}
      .demo-frame[data-view="queue"] img{width:175%;transform:translate(-18%,-1%)}
      .demo-frame[data-view="review"] img,.demo-frame[data-view="receipt"] img{width:150%;transform:translate(-17%,-1%)}
      .demo-caption{display:grid;gap:3px;margin:8px 3px 2px;font-size:10px}
      .control-row{grid-template-columns:38px minmax(0,1fr);gap:10px}
      .control-row p{grid-column:2}
      .evidence-layout{gap:32px;margin-top:34px}
      .evidence-frame{height:360px}
      .closing{padding:68px 0 34px}
      .closing-panel{padding:32px 22px}
      .closing-panel:after{width:100px;height:100px;border-width:18px;right:-40px;top:-45px}
      .closing-panel h2{font-size:clamp(38px,11vw,48px)}
      .footer-row{display:grid;gap:8px}
    }
    @media(max-width:360px){
      .brand-copy strong{max-width:150px;line-height:1.05}
      .display{font-size:41px}
      .hero-copy .actions{margin-top:18px}
      .hero-copy .text-link{display:none}
      .hero-grid{gap:18px}
      .product-window{height:230px}
    }
    @media(prefers-reduced-motion:reduce){
      html{scroll-behavior:auto}
      .hero-copy,.hero-stage{animation:none}
      .button,.button-arrow,.text-link,.product-tab{transition:none}
      .button:active,.text-link:active{transform:none}
    }
    @media(prefers-reduced-transparency:reduce){.site-header{background:var(--canvas);backdrop-filter:none}}
    @media(prefers-contrast:more){
      .site-header{background:var(--canvas);backdrop-filter:none}
      .button,.hero-stage,.product-demo,.closing-panel,.evidence-frame{border-width:2px}
      .lead,.section-lead,.handoff-list p,.control-row p,.evidence-list p{color:var(--ink)}
      .workflow .section-lead,.workflow-steps span,.demo-caption{color:var(--surface)}
    }
    """


def _finish(template: str) -> str:
    return (
        template.replace("__STYLES__", _shared_styles().strip())
        .replace("__VERSION__", VERSION)
        .replace("__UPDATED_DATE__", UPDATED_DATE)
        .replace("__SOCIAL_CARD__", SOCIAL_CARD)
    )


def render_product_landing_v22() -> str:
    return _finish(
        """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <meta name="theme-color" content="#24142b">
  <meta name="description" content="Check every creative row, route each exception and keep uncertain launch decisions human before Ads Manager.">
  <meta name="author" content="Mathieu Petroni">
  <link rel="canonical" href="https://mattyu-dev.github.io/creative-launch-workspace/">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
  <link rel="preload" href="assets/mona-sans-latin-variable.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="me" href="https://www.linkedin.com/in/mathieu-petroni/">
  <link rel="me" href="https://github.com/mattyu-dev">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Creative Launch Workspace">
  <meta property="og:title" content="The launch control layer before Ads Manager">
  <meta property="og:description" content="Validate every creative row, route each exception and keep uncertain calls human.">
  <meta property="og:url" content="https://mattyu-dev.github.io/creative-launch-workspace/">
  <meta property="og:image" content="https://mattyu-dev.github.io/creative-launch-workspace/assets/__SOCIAL_CARD__">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Creative Launch Workspace launch control interface">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="The launch control layer before Ads Manager">
  <meta name="twitter:description" content="Check creative rows, route exceptions and keep uncertain calls human.">
  <meta name="twitter:image" content="https://mattyu-dev.github.io/creative-launch-workspace/assets/__SOCIAL_CARD__">
  <meta name="twitter:image:alt" content="Creative Launch Workspace launch control interface">
  <title>Creative Launch Workspace | Pre-launch QA for Meta creative operations</title>
  <style>__STYLES__</style>
  <script type="application/ld+json">
  {"@context":"https://schema.org","@graph":[{"@type":"Person","@id":"https://mattyu-dev.github.io/#person","name":"Mathieu Petroni","jobTitle":"AI Automation Builder","url":"https://www.linkedin.com/in/mathieu-petroni/","sameAs":["https://github.com/mattyu-dev","https://www.linkedin.com/in/mathieu-petroni/"]},{"@type":"SoftwareApplication","name":"Creative Launch Workspace","applicationCategory":"BusinessApplication","operatingSystem":"Web","softwareVersion":"__VERSION__","description":"Pre-launch QA and exception routing for Meta creative operations.","url":"https://mattyu-dev.github.io/creative-launch-workspace/","author":{"@id":"https://mattyu-dev.github.io/#person"}},{"@type":"WebSite","name":"Creative Launch Workspace","url":"https://mattyu-dev.github.io/creative-launch-workspace/","dateModified":"__UPDATED_DATE__","author":{"@id":"https://mattyu-dev.github.io/#person"}}]}
  </script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to product</a>
  <header class="site-header">
    <nav class="container site-nav" aria-label="Product navigation">
      <a class="brand" href="index.html">
        <span class="brand-mark" aria-hidden="true"><span class="brand-checkpoint"></span></span>
        <span class="brand-copy"><strong>Creative Launch Workspace</strong><span>Pre-launch control</span></span>
      </a>
      <div class="nav-links">
        <a href="#product">Product</a><a href="#workflow">Workflow</a><a href="#controls">Controls</a><a href="#evidence">Evidence</a>
        <a class="button" data-variant="primary" href="workspace.html?guided=1">Open the workspace <span class="button-arrow" aria-hidden="true">→</span></a>
      </div>
    </nav>
  </header>

  <main id="main">
    <section class="hero" id="product" aria-labelledby="hero-title">
      <div class="container">
        <div class="hero-grid">
          <div class="hero-copy">
            <div class="eyebrow">Pre-launch QA for Meta creative operations</div>
            <h1 class="display" id="hero-title">The launch control layer before Ads Manager.</h1>
            <p class="lead">Check every creative row for approval, placement, destination, naming and UTM issues. Route each exception to the right owner. Keep uncertain calls human.</p>
            <div class="actions"><a class="button" data-variant="primary" href="workspace.html?guided=1">Open the workspace <span class="button-arrow" aria-hidden="true">→</span></a><a class="text-link" href="#workflow">See the workflow <span aria-hidden="true">↓</span></a></div>
          </div>
          <figure class="hero-stage">
            <div class="route-track" aria-hidden="true"><span></span></div><span class="stage-label">INPUT / CHECKPOINT / ROUTE</span>
            <div class="product-window"><a href="workspace.html?guided=1"><picture><source type="image/webp" srcset="assets/workspace-mobile-hero.webp"><img src="assets/workspace-mobile-hero.png" width="780" height="720" alt="Creative review showing the issue, owner and next action" decoding="async" fetchpriority="high"></picture></a></div>
            <figcaption class="stage-footer"><strong>Interactive synthetic fixture</strong><span>No Meta publishing</span></figcaption>
          </figure>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="handoff-title">
      <div class="container handoff-grid">
        <div class="handoff-copy"><h2 class="section-title" id="handoff-title">A clean creative is not a clean launch.</h2><p class="section-lead">The risky part is the handoff between approval and campaign build. That is where context drops and small errors become expensive delays.</p></div>
        <ol class="handoff-list"><li><div><h3>The brief drifts</h3><p>Placements, destinations and naming move across documents, messages and spreadsheets.</p></div></li><li><div><h3>Exceptions lose owners</h3><p>A blocker without a named next action waits until the deadline exposes it.</p></div></li><li><div><h3>Ambiguity gets automated</h3><p>Possible duplicates and unclear approvals need accountable judgment, not a silent default.</p></div></li></ol>
      </div>
    </section>

    <section class="section workflow" id="workflow" aria-labelledby="workflow-title">
      <div class="container">
        <h2 class="section-title" id="workflow-title">Turn the handoff into a controlled route.</h2>
        <p class="section-lead">Each row moves through the same visible sequence, from source context to an owned decision.</p>
        <ol class="workflow-steps"><li><b>MAP</b><strong>Map the brief</strong><span>Turn approved source context into typed launch fields.</span></li><li><b>CHECK</b><strong>Check every row</strong><span>Run placement, destination, naming, format and UTM rules.</span></li><li><b>ROUTE</b><strong>Route exceptions</strong><span>Attach the issue, owner and proposed next action.</span></li><li><b>RECORD</b><strong>Record the decision</strong><span>Keep human judgment and the local receipt together.</span></li></ol>
        <div class="product-demo">
          <div class="product-tabs" role="tablist" aria-label="Product views">
            <button class="product-tab" type="button" id="tab-queue" role="tab" aria-selected="true" aria-controls="panel-queue" tabindex="0"><span>01</span><span>Queue</span></button>
            <button class="product-tab" type="button" id="tab-review" role="tab" aria-selected="false" aria-controls="panel-review" tabindex="-1"><span>02</span><span>Review</span></button>
            <button class="product-tab" type="button" id="tab-receipt" role="tab" aria-selected="false" aria-controls="panel-receipt" tabindex="-1"><span>03</span><span>Receipt</span></button>
          </div>
          <div class="demo-panel" id="panel-queue" role="tabpanel" aria-labelledby="tab-queue"><div class="demo-frame" data-view="queue"><picture><source type="image/avif" srcset="assets/workspace-desktop.avif"><source type="image/webp" srcset="assets/workspace-desktop.webp"><img src="assets/workspace-desktop.png" width="1440" height="1000" alt="Launch review queue with routed exceptions" loading="lazy" decoding="async"></picture></div><div class="demo-caption"><strong>Scan the full launch state</strong><span>Filter by decision, blocker or owner</span></div></div>
          <div class="demo-panel" id="panel-review" role="tabpanel" aria-labelledby="tab-review" hidden><div class="demo-frame" data-view="review"><picture><source type="image/avif" srcset="assets/guided-review-step-1.avif"><source type="image/webp" srcset="assets/guided-review-step-1.webp"><img src="assets/guided-review-step-1.png" width="1280" height="900" alt="Guided review showing the issue, owner and proposed fix" loading="lazy" decoding="async"></picture></div><div class="demo-caption"><strong>Find the ambiguous row</strong><span>Issue, owner and proposed fix stay together</span></div></div>
          <div class="demo-panel" id="panel-receipt" role="tabpanel" aria-labelledby="tab-receipt" hidden><div class="demo-frame" data-view="receipt"><picture><source type="image/avif" srcset="assets/guided-review-step-3.avif"><source type="image/webp" srcset="assets/guided-review-step-3.webp"><img src="assets/guided-review-step-3.png" width="1280" height="900" alt="Local audit receipt after a human launch decision" loading="lazy" decoding="async"></picture></div><div class="demo-caption"><strong>Keep the decision inspectable</strong><span>Local receipt, no external write</span></div></div>
        </div>
      </div>
    </section>

    <section class="section" id="controls" aria-labelledby="controls-title">
      <div class="container controls-grid">
        <div><h2 class="section-title" id="controls-title">Automation proposes. Control stays explicit.</h2><p class="section-lead">The model can structure ambiguous prose. It cannot approve a field, bypass a rule or publish a campaign.</p></div>
        <div class="control-system"><div class="control-row"><span>P</span><h3>AI proposes</h3><p>Typed fields include source evidence, confidence and an abstention path.</p></div><div class="control-row"><span>V</span><h3>Rules verify</h3><p>Schema, allowlists and deterministic launch checks fail closed.</p></div><div class="control-row"><span>H</span><h3>People decide</h3><p>Ambiguous fields and possible duplicates remain with accountable reviewers.</p></div></div>
      </div>
    </section>

    <section class="section" id="evidence" aria-labelledby="evidence-title">
      <div class="container">
        <h2 class="section-title" id="evidence-title">Every decision leaves inspectable evidence.</h2>
        <p class="section-lead">The public product is backed by generated contracts, browser checks and a reproducible synthetic launch.</p>
        <div class="evidence-layout"><a class="evidence-frame" href="brief-evidence.html"><picture><source type="image/avif" srcset="assets/brief-evidence.avif"><source type="image/webp" srcset="assets/brief-evidence.webp"><img src="assets/brief-evidence.png" width="1440" height="1794" alt="Field-level mapping evidence and review state" loading="lazy" decoding="async"></picture></a><div><ul class="evidence-list"><li><strong>Versioned contracts</strong><p>Proposal, review and materialization formats stay explicit and testable.</p></li><li><strong>Deterministic replay</strong><p>Fixes re-run the same Python validators used to build the workspace.</p></li><li><strong>Browser quality gates</strong><p>Responsive, keyboard, accessibility and performance checks run in CI.</p></li></ul><div class="evidence-links"><a href="brief-evidence.html">Open evidence</a><a href="fix-lab.html">Replay a fix</a><a href="https://github.com/mattyu-dev/creative-launch-workspace/actions">Inspect CI</a><a href="https://github.com/mattyu-dev/creative-launch-workspace">View source</a></div></div></div>
      </div>
    </section>

    <section class="closing" aria-labelledby="closing-title">
      <div class="container"><div class="closing-panel"><div><h2 id="closing-title">Put every launch exception on a controlled route.</h2><p>Open the workspace and follow one decision from issue to receipt.</p></div><div class="actions"><a class="button" data-variant="primary" href="workspace.html?guided=1">Open the workspace <span class="button-arrow" aria-hidden="true">→</span></a><a class="button" data-variant="outline" data-on-dark="true" href="https://github.com/mattyu-dev/creative-launch-workspace/blob/main/docs/architecture/system.md">View the architecture</a></div></div></div>
    </section>
  </main>
  <footer><div class="container footer-row"><span>Creative Launch Workspace. Built by <a href="https://www.linkedin.com/in/mathieu-petroni/" rel="me external">Mathieu Petroni</a>.</span><span><a href="https://github.com/mattyu-dev/creative-launch-workspace">MIT licensed source</a>.</span></div></footer>
  <script>
    const tabs=[...document.querySelectorAll('[role="tab"]')];
    function activateTab(tab){
      tabs.forEach((item)=>{
        const active=item===tab;
        item.setAttribute('aria-selected',String(active));
        item.tabIndex=active?0:-1;
        document.getElementById(item.getAttribute('aria-controls')).hidden=!active;
      });
    }
    tabs.forEach((tab,index)=>{
      tab.addEventListener('click',()=>activateTab(tab));
      tab.addEventListener('keydown',(event)=>{
        if(!['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;
        event.preventDefault();
        let next=index;
        if(event.key==='ArrowLeft')next=(index-1+tabs.length)%tabs.length;
        if(event.key==='ArrowRight')next=(index+1)%tabs.length;
        if(event.key==='Home')next=0;
        if(event.key==='End')next=tabs.length-1;
        activateTab(tabs[next]);
        tabs[next].focus();
      });
    });
  </script>
</body>
</html>
"""
    )


def render_social_card_page_v22() -> str:
    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=1200, initial-scale=1"><meta name="author" content="Mathieu Petroni"><style>
@font-face{font-family:"Mona Sans";src:url("assets/mona-sans-latin-variable.woff2") format("woff2-variations");font-weight:200 900;font-display:swap}@font-face{font-family:"Geist Mono";src:url("assets/geist-mono-latin-variable.woff2") format("woff2");font-weight:100 900;font-display:swap}*{box-sizing:border-box}html,body{margin:0;width:1200px;height:630px;overflow:hidden}body{color:#1c1422;background:#f7f6f8;font-family:"Mona Sans",system-ui,sans-serif}main{width:1200px;height:630px;display:grid;grid-template-columns:520px 680px}.copy{padding:48px 40px 42px 54px;display:flex;flex-direction:column}.brand{display:flex;align-items:center;gap:12px}.mark{width:34px;height:34px;position:relative;border:1px solid #a99eae;border-radius:8px;background:#fff}.mark:before{content:"";position:absolute;left:6px;top:9px;width:9px;height:1px;background:#24142b;box-shadow:0 7px 0 #24142b,0 14px 0 #24142b}.mark:after{content:"";position:absolute;left:19px;top:13px;width:8px;height:1px;background:#24142b;box-shadow:0 8px 0 #24142b}.checkpoint{position:absolute;left:14px;top:13px;width:7px;height:8px;border:1px solid #24142b;background:#ffe44d}.brand strong{font-size:16px;font-weight:760}.eyebrow{margin-top:74px;color:#a40c50;font:650 12px/1.4 "Geist Mono",monospace;letter-spacing:.06em;text-transform:uppercase}.hero h1{margin:16px 0 0;font-size:54px;line-height:.98;letter-spacing:-2px;font-weight:770}.hero p{max-width:415px;margin:20px 0 0;color:#6c6570;font-size:17px;line-height:1.45}.copy footer{display:flex;justify-content:space-between;margin-top:auto;color:#6c6570;font-size:11px}.visual{position:relative;padding:40px 40px 40px 0}.stage{height:550px;padding:32px 14px 14px;border-radius:20px;background:#24142b}.track{position:absolute;left:30px;right:64px;top:55px;height:1px;background:#67596d}.track:after{content:"";position:absolute;left:50%;top:-5px;width:10px;height:10px;border:1px solid #fff;background:#ffe44d;transform:rotate(45deg)}.frame{height:492px;overflow:hidden;border:1px solid #6d6072;border-radius:12px;background:#fff}.frame img{width:100%;height:auto;display:block}.label{position:absolute;right:58px;top:50px;color:#bdb2c1;font:550 10px/1.4 "Geist Mono",monospace}
</style></head><body><main><section class="copy"><div class="brand"><span class="mark"><span class="checkpoint"></span></span><strong>Creative Launch Workspace</strong></div><div class="hero"><div class="eyebrow">Pre-launch QA for Meta creative operations</div><h1>The launch control layer before Ads Manager.</h1><p>Check every creative row, route each exception and keep uncertain calls human.</p></div><footer><strong>Interactive workspace</strong><span>Built by Mathieu Petroni</span></footer></section><div class="visual"><div class="stage"><div class="track"></div><span class="label">CHECK / ROUTE / DECIDE</span><div class="frame"><img src="assets/workspace-mobile-hero.png" alt=""></div></div></div></main></body></html>
"""
