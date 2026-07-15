from __future__ import annotations

VERSION = "4.0.0"
UPDATED_DATE = "2026-07-15"
SOCIAL_CARD = "social-card-v4.png"


def _shared_styles() -> str:
    return r"""
    @font-face{font-family:"Inter";src:url("assets/inter-latin-variable.woff2") format("woff2-variations");font-style:normal;font-weight:100 900;font-display:optional}
    @font-face{font-family:"Instrument Serif";src:url("assets/instrument-serif-latin-italic.woff2") format("woff2");font-style:italic;font-weight:400;font-display:optional}
    :root{
      color-scheme:light;
      --canvas:#ECEDEE;
      --shell:#F4F5F5;
      --surface:#FFFFFF;
      --surface-soft:#F7F7F5;
      --ink:#232427;
      --charcoal:#171719;
      --charcoal-raised:#202024;
      --body:#55575C;
      --muted:#6B6D72;
      --orange:#E34A32;
      --orange-hover:#F05A3C;
      --orange-soft:#FFF0EC;
      --line:rgba(23,23,25,.09);
      --line-strong:rgba(23,23,25,.16);
      --success:#287A4D;
      --danger:#B9382B;
      --warning:#9A5A12;
      --ring:#E34A32;
      --sans:"Inter",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
      --serif:"Instrument Serif",Georgia,serif;
      --mono:"SFMono-Regular",Consolas,"Liberation Mono",monospace;
      --ease-out:cubic-bezier(.22,1,.36,1);
      --ease-ui:cubic-bezier(.2,0,0,1);
      --shadow-shell:0 1px 0 rgba(255,255,255,.9) inset,0 40px 100px -64px rgba(35,36,39,.45);
      --shadow-card:0 1px 0 rgba(255,255,255,.9) inset,0 18px 42px -28px rgba(35,36,39,.35);
      --radius-shell:40px;
      --radius-stage:28px;
      --radius-card:24px;
      --radius-app:16px;
      --radius-control:11px;
    }
    *{box-sizing:border-box}
    html{scroll-behavior:smooth}
    body{margin:0;color:var(--ink);background:var(--canvas);font:400 16px/1.625 var(--sans);letter-spacing:-.012em;-webkit-font-smoothing:antialiased}
    body:before{content:"";position:fixed;z-index:-1;inset:0;background:radial-gradient(circle at 84% 3%,rgba(227,74,50,.12),transparent 32%);pointer-events:none}
    h1,h2,h3,p{margin-top:0}
    h1,h2,h3{letter-spacing:-.035em;text-wrap:balance}
    h1,h2,h3,p,a,strong,span{overflow-wrap:anywhere}
    p{color:var(--body)}
    a{color:inherit}
    button,input{font:inherit}
    button{color:inherit}
    img{max-width:100%}
    [hidden]{display:none!important}
    :focus-visible{outline:3px solid color-mix(in srgb,var(--ring) 72%,white);outline-offset:3px}
    .page{width:min(1440px,calc(100% - 24px));margin:12px auto 0;overflow:hidden;border:1px solid rgba(255,255,255,.68);border-radius:var(--radius-shell);background:var(--shell);box-shadow:var(--shadow-shell)}
    .container{width:min(1240px,calc(100% - 64px));margin-inline:auto}
    .skip-link{position:fixed;z-index:100;left:20px;top:-80px;min-height:44px;display:inline-flex;align-items:center;padding:8px 14px;border-radius:999px;color:white;background:var(--charcoal);font-weight:650;text-decoration:none}
    .skip-link:focus{top:16px}
    .nav-sentinel{height:1px}
    .site-header{position:sticky;z-index:50;top:12px;width:min(1050px,calc(100% - 48px));margin:12px auto 0;border:1px solid rgba(255,255,255,.82);border-radius:999px;background:rgba(255,255,255,.76);backdrop-filter:blur(24px);transition:box-shadow 220ms var(--ease-out),background-color 220ms var(--ease-out)}
    .site-header[data-scrolled="true"]{background:rgba(255,255,255,.91);box-shadow:0 14px 38px -22px rgba(35,36,39,.5)}
    .site-nav{min-height:62px;display:flex;align-items:center;justify-content:space-between;gap:24px;padding:7px 9px 7px 18px}
    .brand{min-height:44px;display:inline-flex;align-items:center;gap:11px;text-decoration:none}
    .brand-mark{width:31px;height:31px;position:relative;flex:none}
    .brand-mark:before,.brand-mark:after{content:"";position:absolute;top:7px;width:19px;height:19px;border-radius:50%}
    .brand-mark:before{left:0;background:var(--charcoal)}
    .brand-mark:after{left:12px;background:var(--orange);box-shadow:0 6px 16px -7px rgba(227,74,50,.9)}
    .brand-copy{display:grid;line-height:1.05}
    .brand-copy strong{font-size:14px;font-weight:680;letter-spacing:-.025em}
    .brand-copy span{margin-top:4px;color:var(--muted);font-size:10px;font-weight:540;letter-spacing:.01em}
    .nav-links{display:flex;align-items:center;gap:2px}
    .nav-links>a:not(.button){min-height:44px;display:inline-flex;align-items:center;padding:0 10px;border-radius:999px;color:var(--body);font-size:12px;font-weight:590;text-decoration:none;transition:color 150ms ease,background-color 150ms ease}
    .button{min-height:44px;display:inline-flex;align-items:center;justify-content:center;gap:9px;padding:10px 16px;border:1px solid transparent;border-radius:999px;font-size:13px;font-weight:650;line-height:1.1;text-decoration:none;cursor:pointer;transition:transform 100ms var(--ease-ui),background-color 160ms ease,border-color 160ms ease,color 160ms ease,box-shadow 180ms var(--ease-out)}
    .button img,.icon{width:16px;height:16px;display:block}
    .button[data-variant="primary"]{color:#fff;background:var(--charcoal);box-shadow:0 14px 28px -15px rgba(23,23,25,.72)}
    .button[data-variant="orange"]{color:#fff;background:#C83C28;box-shadow:0 14px 28px -15px rgba(227,74,50,.65)}
    .button[data-variant="outline"]{border-color:var(--line-strong);background:rgba(255,255,255,.6)}
    .button[data-variant="ghost"]{padding-inline:9px;color:var(--body);background:transparent}
    .button[data-variant="danger"]{color:var(--danger);background:transparent}
    .button:active{transform:scale(.98)}
    .button-arrow{display:inline-block;transition:transform 160ms var(--ease-out)}
    .hero{position:relative;padding:72px 0 0}
    .hero:before{content:"";position:absolute;right:-120px;top:-270px;width:720px;height:720px;border-radius:50%;background:radial-gradient(circle,rgba(227,74,50,.19),transparent 67%);filter:blur(20px);pointer-events:none}
    .hero-main{min-height:510px;position:relative;display:grid;grid-template-columns:minmax(0,1.08fr) minmax(420px,.82fr);gap:46px;align-items:center}
    .hero-copy{min-width:0;position:relative;z-index:2;padding:30px 0 84px}
    .eyebrow{margin-bottom:20px;color:var(--orange);font-size:11px;font-weight:700;letter-spacing:.075em;text-transform:uppercase}
    .display{max-width:860px;margin:0;font-size:clamp(56px,4.45vw,64px);font-weight:600;line-height:.96;letter-spacing:-.052em;text-wrap:wrap;overflow-wrap:anywhere}
    .wchar-word{display:inline-block;white-space:nowrap}
    .wchar{display:inline-block;font-variation-settings:"wght" 600;transition:font-variation-settings 150ms linear}
    .lead{max-width:690px;margin:26px 0 0;color:var(--body);font-size:18px;line-height:1.58}
    .hero-actions{display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin-top:28px}
    .cta-note{width:100%;margin:1px 0 0 4px;color:var(--muted);font-size:11px}
    .hero-motion-host{min-width:0;position:relative;z-index:2;align-self:center}
    .motion-fallback{min-height:430px;display:flex;flex-direction:column;overflow:hidden;border:1px solid var(--line);border-radius:24px;background:rgba(255,255,255,.9);box-shadow:var(--shadow-card)}
    .motion-fallback header{min-height:51px;display:flex;align-items:center;justify-content:space-between;gap:12px;padding:10px 14px;border-bottom:1px solid var(--line);font-size:11px;font-weight:650}
    .motion-fallback header span:last-child{color:var(--muted);font-weight:500}
    .motion-fallback ol{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));margin:0;padding:0 10px;border-bottom:1px solid var(--line);list-style:none}
    .motion-fallback li{min-width:0;min-height:60px;display:flex;align-items:center;gap:8px;padding:8px;color:var(--muted);font-size:11px}
    .motion-fallback li b{width:23px;height:23px;display:grid;place-items:center;border:1px solid rgba(227,74,50,.2);border-radius:50%;color:var(--orange);background:var(--orange-soft);font-size:9px}
    .motion-fallback article{flex:1;display:grid;place-items:center;padding:24px;background:linear-gradient(180deg,#FCFCFB,#F8F8F6)}
    .motion-fallback article div{width:100%;padding:18px;border:1px solid rgba(227,74,50,.17);border-radius:14px;background:#FFF9F7}
    .motion-fallback article small{color:var(--orange);font-size:10px;font-weight:700;letter-spacing:.06em;text-transform:uppercase}
    .motion-fallback article strong{display:block;margin-top:7px;font-size:16px}
    .motion-fallback article span{display:block;margin-top:7px;color:var(--muted);font-size:11px}
    .motion-fallback footer{min-height:64px;display:flex;align-items:center;padding:12px 14px;border-top:1px solid var(--line);color:var(--muted);font-size:10px}
    .app-stage{position:relative;z-index:3;margin-top:-28px;padding:18px;border:1px solid rgba(23,23,25,.07);border-radius:var(--radius-stage);background:rgba(255,255,255,.54);box-shadow:0 1px 0 rgba(255,255,255,.95) inset,0 36px 82px -48px rgba(35,36,39,.5);backdrop-filter:blur(18px)}
    .app-stage:before{content:"";position:absolute;inset:-1px;border-radius:inherit;box-shadow:0 1px 0 rgba(255,255,255,.9) inset;pointer-events:none}
    .app-shell{min-width:0;overflow:hidden;border:1px solid var(--line);border-radius:var(--radius-app);background:#FCFCFB;box-shadow:0 20px 44px -35px rgba(35,36,39,.5)}
    .app-topbar{min-height:54px;display:flex;align-items:center;justify-content:space-between;gap:18px;padding:8px 14px;border-bottom:1px solid var(--line);background:rgba(255,255,255,.88)}
    .app-title{display:flex;align-items:center;gap:10px;font-size:13px;font-weight:670}
    .app-title .brand-mark{width:24px;height:24px}
    .app-title .brand-mark:before,.app-title .brand-mark:after{top:5px;width:15px;height:15px}
    .app-title .brand-mark:after{left:9px}
    .app-meta{display:flex;align-items:center;gap:8px;color:var(--muted);font-size:12px}
    .badge{min-height:28px;display:inline-flex;align-items:center;padding:4px 9px;border:1px solid var(--line);border-radius:999px;color:var(--body);background:var(--surface-soft);font-size:12px;font-weight:580;white-space:nowrap}
    .badge[data-tone="orange"]{border-color:rgba(227,74,50,.18);color:#B93624;background:var(--orange-soft)}
    .product-tabs{position:relative;display:inline-grid;grid-template-columns:repeat(3,1fr);gap:0;margin:10px 14px;padding:4px;border:1px solid var(--line);border-radius:13px;background:#F1F1EF}
    .product-tab{min-width:108px;min-height:44px;position:relative;z-index:1;border:0;border-radius:10px;color:var(--muted);background:transparent;font-size:12px;font-weight:630;cursor:pointer;transition:color 150ms ease}
    .product-tab[aria-selected="true"]{color:var(--ink)}
    .t-tabs-pill{height:44px;position:absolute;z-index:0;top:4px;left:4px;border:1px solid rgba(23,23,25,.07);border-radius:10px;background:white;box-shadow:0 3px 11px -7px rgba(35,36,39,.45);transition:left 250ms cubic-bezier(.22,1,.36,1),width 250ms cubic-bezier(.22,1,.36,1)}
    .app-panel{min-height:575px;border-top:1px solid var(--line)}
    .queue-layout{min-height:575px;display:grid;grid-template-columns:184px minmax(0,1fr)}
    .queue-nav{padding:18px 12px;border-right:1px solid var(--line);background:#F8F8F6}
    .queue-nav strong{display:block;padding:0 9px 11px;color:var(--muted);font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase}
    .queue-filter{width:100%;min-height:44px;display:flex;align-items:center;justify-content:space-between;padding:7px 9px;border:0;border-radius:9px;color:var(--body);background:transparent;font-size:12px;text-align:left;cursor:pointer}
    .queue-filter span{color:var(--muted);font-variant-numeric:tabular-nums}
    .queue-filter[data-active="true"]{color:#A92C1D;background:var(--orange-soft);font-weight:650}
    .queue-filter[data-active="true"] span{color:#A92C1D}
    .queue-main{min-width:0;padding:26px 28px 30px}
    .queue-head{display:flex;align-items:start;justify-content:space-between;gap:24px}
    .queue-head h2{margin:0;font-size:25px;font-weight:650;line-height:1.1}
    .queue-head p{margin:8px 0 0;font-size:14px}
    .run-strip{display:grid;grid-template-columns:30fr 10fr 60fr;gap:3px;margin:24px 0 10px}
    .run-strip span{height:7px;border-radius:999px;background:#D9DAD8}
    .run-strip span:nth-child(1){background:#89B79B}
    .run-strip span:nth-child(2){background:var(--orange)}
    .run-legend{display:flex;gap:18px;margin-bottom:20px;color:var(--muted);font-size:12px}
    .run-legend b{color:var(--ink);font-weight:680}
    .queue-list{overflow:hidden;border:1px solid var(--line);border-radius:13px;background:white}
    .queue-row{width:100%;min-height:74px;display:grid;grid-template-columns:92px minmax(160px,1fr) minmax(150px,.8fr) 118px;gap:18px;align-items:center;padding:12px 16px;border:0;border-bottom:1px solid var(--line);background:#fff;text-align:left;cursor:pointer;transition:background-color 130ms ease,transform 130ms var(--ease-out)}
    .queue-row:last-child{border-bottom:0}
    .queue-row[data-selected="true"]{box-shadow:4px 0 0 var(--orange) inset;background:#FFF9F7}
    .row-id{font:600 12px/1.3 var(--mono)}
    .row-name strong,.row-owner strong{display:block;font-size:13px;font-weight:630}
    .row-name span,.row-owner span{display:block;margin-top:4px;color:var(--muted);font-size:12px}
    .row-status{justify-self:end;color:var(--warning);font-size:12px;font-weight:650;text-align:right}
    .review-layout{min-height:575px;display:grid;grid-template-columns:minmax(0,58fr) minmax(320px,42fr)}
    .review-main{min-width:0;padding:25px 28px 30px}
    .breadcrumb{margin-bottom:18px;color:var(--muted);font-size:12px}
    .review-title{display:flex;align-items:start;justify-content:space-between;gap:20px}
    .review-title h2{margin:0;font-size:25px;font-weight:650}
    .review-title p{margin:6px 0 0;font:500 12px/1.5 var(--mono)}
    .creative-layout{display:grid;grid-template-columns:minmax(180px,.8fr) minmax(210px,1fr);gap:24px;align-items:start;margin-top:22px}
    .creative-preview{aspect-ratio:4/5;min-height:0;position:relative;overflow:hidden;border-radius:14px;color:white;background:#E34A32;box-shadow:0 16px 36px -28px rgba(227,74,50,.7)}
    .creative-preview:before{content:"";position:absolute;width:76%;aspect-ratio:1;right:-18%;top:8%;border:1px solid rgba(255,255,255,.52);border-radius:50%;box-shadow:0 0 0 38px rgba(255,255,255,.08),0 0 0 76px rgba(255,255,255,.06)}
    .preview-chip{position:absolute;left:16px;top:16px;padding:5px 8px;border:1px solid rgba(255,255,255,.35);border-radius:999px;background:rgba(23,23,25,.14);font-size:12px;font-weight:680;letter-spacing:.05em;text-transform:uppercase}
    .preview-copy{position:absolute;z-index:1;left:18px;right:18px;bottom:18px}
    .preview-copy span{font-size:12px;opacity:.84}
    .preview-copy strong{display:block;margin-top:7px;font-size:24px;line-height:.98;letter-spacing:-.04em}
    .facts{margin:0;border-top:1px solid var(--line)}
    .facts div{display:grid;grid-template-columns:105px minmax(0,1fr);gap:14px;padding:10px 0;border-bottom:1px solid var(--line)}
    .facts dt{color:var(--muted);font-size:12px}
    .facts dd{min-width:0;margin:0;font-size:12px;font-weight:570;overflow-wrap:anywhere}
    .inspector{min-width:0;display:flex;flex-direction:column;padding:25px;border-left:1px solid var(--line);background:#F8F8F6}
    .inspector[data-animate="in"]{animation:inspector-in 280ms var(--ease-out) both}
    .inspector-kicker{display:flex;align-items:center;gap:8px;color:var(--orange);font-size:12px;font-weight:700;letter-spacing:.055em;text-transform:uppercase}
    .inspector-kicker img{width:15px;height:15px}
    .inspector h3{margin:16px 0 0;font-size:25px;font-weight:650;line-height:1.05}
    .inspector>p{margin:10px 0 0;font-size:14px;line-height:1.55}
    .decision-card{margin-top:20px;padding:16px;border:1px solid rgba(227,74,50,.16);border-radius:13px;background:#FFF9F7}
    .decision-card strong{font-size:13px}
    .decision-card p{margin:6px 0 0;font-size:13px;line-height:1.5}
    .owner-line{display:flex;justify-content:space-between;gap:16px;margin-top:18px;padding-top:15px;border-top:1px solid var(--line);font-size:12px}
    .owner-line span{color:var(--muted)}
    .inspector-actions{display:grid;gap:8px;margin-top:auto;padding-top:20px}
    .inspector-actions .button{width:100%;border-radius:10px}
    .inspector-foot{margin:11px 0 0!important;color:var(--muted);font-size:12px!important;text-align:center}
    .receipt-panel{min-height:575px;display:grid;place-items:center;padding:36px;background:#F8F8F6}
    .receipt-card{width:min(760px,100%);display:grid;grid-template-columns:minmax(0,.78fr) minmax(260px,1fr);overflow:hidden;border:1px solid var(--line);border-radius:18px;background:white;box-shadow:var(--shadow-card)}
    .receipt-summary{padding:30px}
    .success-icon{width:46px;height:46px;display:grid;place-items:center;border-radius:50%;background:var(--orange-soft)}
    .success-icon img{width:22px;height:22px}
    .receipt-summary h2{margin:18px 0 0;font-size:29px;font-weight:650;line-height:1.04}
    .receipt-summary p{margin:10px 0 0;font-size:13px}
    .timeline{margin:22px 0 0;padding:0;list-style:none}
    .timeline li{position:relative;padding:0 0 16px 23px;font-size:12px;opacity:0;transform:translateY(7px)}
    .receipt-card[data-live="true"] .timeline li{animation:timeline-in 260ms var(--ease-out) forwards}
    .receipt-card[data-live="true"] .timeline li:nth-child(2){animation-delay:60ms}
    .receipt-card[data-live="true"] .timeline li:nth-child(3){animation-delay:120ms}
    .timeline li:before{content:"";position:absolute;left:0;top:5px;width:8px;height:8px;border-radius:50%;background:var(--orange)}
    .timeline li:not(:last-child):after{content:"";position:absolute;left:3px;top:14px;bottom:1px;width:1px;background:rgba(227,74,50,.24)}
    .timeline strong{display:block;font-weight:650}
    .timeline span{color:var(--muted)}
    .receipt-data{padding:26px;border-left:1px solid var(--line);background:#F8F8F6}
    .receipt-data h4{margin:0 0 12px;font-size:12px;letter-spacing:.06em;text-transform:uppercase}
    .receipt-data dl{margin:0}
    .receipt-data div{display:grid;grid-template-columns:92px minmax(0,1fr);gap:10px;padding:7px 0;border-bottom:1px solid var(--line)}
    .receipt-data dt{color:var(--muted);font-size:12px}
    .receipt-data dd{min-width:0;margin:0;font:560 12px/1.45 var(--mono);overflow-wrap:anywhere}
    .receipt-data .receipt-actions{display:flex;flex-wrap:wrap;gap:7px;margin-top:18px}
    .receipt-actions .button{border-radius:10px}
    .live-region{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
    .run-proof{display:grid;grid-template-columns:1.35fr repeat(4,1fr);gap:1px;margin:20px 0 0;border:1px solid var(--line);border-radius:18px;background:var(--line);overflow:hidden;transform:rotate(-.35deg);box-shadow:var(--shadow-card)}
    .run-proof>div{min-height:112px;display:flex;flex-direction:column;justify-content:center;padding:18px 20px;background:white}
    .run-proof .proof-label{background:var(--charcoal);color:white}
    .proof-label span{color:#B7B8BA;font-size:10px;font-weight:700;letter-spacing:.07em;text-transform:uppercase}
    .proof-label strong{margin-top:7px;font-size:16px;line-height:1.15}
    .proof-number strong{font-size:34px;font-weight:620;line-height:1}
    .proof-number span{margin-top:7px;color:var(--muted);font-size:11px}
    .section{padding:128px 0}
    .section-heading{display:grid;grid-template-columns:minmax(0,.9fr) minmax(320px,.55fr);gap:70px;align-items:end;margin-bottom:48px}
    .section-title{max-width:820px;margin:0;font-size:clamp(44px,5vw,70px);font-weight:610;line-height:.98;letter-spacing:-.048em}
    .serif-accent{font-family:var(--serif);font-weight:400;letter-spacing:-.01em}
    .section-lead{max-width:550px;margin:0;font-size:17px}
    .route-line{display:grid;grid-template-columns:1fr auto 1fr auto 1fr auto 1fr;align-items:center;gap:14px;margin:0 0 34px}
    .route-line:before,.route-line:after,.route-segment{content:"";height:1px;background:linear-gradient(90deg,transparent,var(--orange))}
    .route-line:after{background:linear-gradient(90deg,var(--orange),transparent)}
    .route-step{display:flex;align-items:center;gap:9px;color:var(--body);font-size:12px;font-weight:650}
    .route-step b{width:28px;height:28px;display:grid;place-items:center;border:1px solid rgba(227,74,50,.18);border-radius:50%;color:var(--orange);background:var(--orange-soft);font-size:10px}
    .bento{display:grid;grid-template-columns:1.2fr .8fr 1fr;grid-template-rows:300px 290px;gap:16px}
    .feature-card{min-width:0;position:relative;overflow:hidden;padding:30px;border:1px solid var(--line);border-radius:var(--radius-card);background:white;box-shadow:var(--shadow-card)}
    .feature-card h3{margin:15px 0 0;font-size:24px;font-weight:640;line-height:1.05}
    .feature-card p{max-width:460px;margin:11px 0 0;font-size:13px;line-height:1.55}
    .feature-card>.icon{width:20px;height:20px}
    .feature-card[data-card="source"]{grid-column:span 2}
    .feature-card[data-card="route"]{background:var(--charcoal);color:white}
    .feature-card[data-card="route"] p{color:#B7B8BA}
    .feature-card[data-card="route"]>.icon{filter:invert(1)}
    .feature-card[data-card="local"]{grid-column:span 2;background:#F0F0ED}
    .source-map{position:absolute;right:26px;bottom:24px;width:47%;display:grid;gap:8px}
    .source-map span{height:28px;border:1px solid var(--line);border-radius:8px;background:var(--surface-soft)}
    .source-map span:nth-child(2){width:78%;margin-left:auto;border-color:rgba(227,74,50,.22);background:var(--orange-soft)}
    .route-visual{position:absolute;left:30px;right:30px;bottom:28px;display:flex;align-items:center}
    .route-visual span{flex:1;height:1px;background:rgba(255,255,255,.24)}
    .route-visual b{width:38px;height:38px;display:grid;place-items:center;border:1px solid rgba(255,255,255,.2);border-radius:50%;color:#fff;background:var(--orange);font-size:10px}
    .local-window{position:absolute;right:28px;bottom:-40px;width:48%;height:220px;padding:15px;border:1px solid var(--line);border-radius:18px;background:white;box-shadow:0 24px 50px -34px rgba(35,36,39,.5);transform:rotate(1deg)}
    .local-window span{display:block;height:9px;margin:10px 0;border-radius:999px;background:#E4E4E1}
    .local-window span:nth-child(2){width:62%;background:#F6B3A7}
    .local-window span:nth-child(3){width:82%}
    .local-window span:nth-child(4){width:48%}
    .feature-card[data-card="boundary"]{background:var(--orange-soft)}
    .boundary-signal{position:absolute;left:30px;right:30px;bottom:28px;display:grid;grid-template-columns:minmax(0,1fr) auto;gap:12px;padding:14px 16px;border:1px solid rgba(227,74,50,.16);border-radius:14px;background:rgba(255,255,255,.72);font:600 12px/1.3 var(--mono)}
    .boundary-signal span{color:var(--muted);overflow-wrap:anywhere}
    .boundary-signal strong{color:var(--orange)}
    .safeguard{padding:0 0 128px}
    .safeguard-panel{position:relative;overflow:hidden;padding:72px;border-radius:32px;color:white;background:var(--charcoal);box-shadow:0 34px 74px -50px rgba(23,23,25,.8)}
    .safeguard-panel:after{content:"";position:absolute;right:-110px;top:-180px;width:460px;height:460px;border-radius:50%;background:radial-gradient(circle,rgba(227,74,50,.32),transparent 66%);pointer-events:none}
    .safeguard-panel .eyebrow{color:#F58B78}
    .safeguard-panel h2{max-width:920px;margin:0;font-size:clamp(46px,6vw,78px);font-weight:580;line-height:.98;letter-spacing:-.05em}
    .safeguard-panel>p{max-width:640px;margin:22px 0 0;color:#B7B8BA;font-size:17px}
    .guardrails{position:relative;z-index:1;display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:48px}
    .guardrails div{min-height:126px;padding:20px;border:1px solid rgba(255,255,255,.11);border-radius:16px;background:rgba(255,255,255,.04)}
    .guardrails b{display:block;color:#F58B78;font-size:11px}
    .guardrails strong{display:block;margin-top:20px;font-size:18px;font-weight:610}
    .evidence{padding:128px 0;background:#F7F7F5}
    .evidence-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:44px}
    .evidence-link{min-height:190px;display:flex;flex-direction:column;padding:23px;border:1px solid var(--line);border-radius:20px;background:white;text-decoration:none;box-shadow:var(--shadow-card);transition:transform 180ms var(--ease-out),border-color 160ms ease,box-shadow 180ms var(--ease-out)}
    .evidence-link img{width:19px;height:19px}
    .evidence-link strong{margin-top:auto;font-size:17px;font-weight:640}
    .evidence-link span{margin-top:7px;color:var(--muted);font-size:12px}
    .closing{padding:96px 0 40px}
    .app-stage,.section,.safeguard,.evidence{scroll-margin-top:100px}
    .closing-panel{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:54px;align-items:end;padding:58px;border:1px solid rgba(23,23,25,.08);border-radius:30px;background:white;box-shadow:var(--shadow-card)}
    .closing-panel h2{max-width:820px;margin:0;font-size:clamp(42px,5.2vw,68px);font-weight:610;line-height:.98;letter-spacing:-.05em}
    .closing-panel p{margin:17px 0 0;font-size:16px}
    .closing-actions{display:flex;flex-wrap:wrap;gap:9px}
    footer{padding:24px 0 36px;color:var(--muted);font-size:11px}
    .footer-row{display:flex;justify-content:space-between;gap:24px}
    .footer-links{display:flex;gap:18px}
    [data-reveal]{opacity:0;transform:translateY(16px);transition:opacity 620ms var(--ease-out),transform 620ms var(--ease-out)}
    [data-reveal][data-visible="true"]{opacity:1;transform:translateY(0)}
    .hero-copy [data-rise]{opacity:0;transform:translateY(12px);animation:rise-in 620ms var(--ease-out) forwards}
    .hero-copy .display[data-rise]{opacity:1;transform:none;animation:none}
    .hero-copy [data-rise]:nth-child(2){animation-delay:60ms}
    .hero-copy [data-rise]:nth-child(3){animation-delay:120ms}
    .hero-copy [data-rise]:nth-child(4){animation-delay:180ms}
    @keyframes rise-in{to{opacity:1;transform:translateY(0)}}
    @keyframes inspector-in{from{opacity:0;transform:translateX(12px)}to{opacity:1;transform:translateX(0)}}
    @keyframes timeline-in{to{opacity:1;transform:translateY(0)}}
    @media(hover:hover) and (pointer:fine){
      .nav-links>a:not(.button):hover{color:var(--ink);background:rgba(23,23,25,.05)}
      .button[data-variant="primary"]:hover{background:#2C2C30;box-shadow:0 16px 32px -15px rgba(23,23,25,.82)}
      .button[data-variant="orange"]:hover{background:var(--orange-hover)}
      .button[data-variant="outline"]:hover{border-color:var(--line-strong);background:white}
      .button[data-variant="ghost"]:hover{background:rgba(23,23,25,.05)}
      .button:hover .button-arrow{transform:translateX(2px)}
      .queue-row:hover{z-index:1;background:#FFF9F7;transform:translateY(-1px)}
      .evidence-link:hover{z-index:1;transform:translateY(-3px);border-color:rgba(227,74,50,.25);box-shadow:0 20px 44px -27px rgba(35,36,39,.45)}
    }
    @media(max-width:1040px){
      .hero-main{grid-template-columns:minmax(0,1fr) minmax(390px,.82fr);gap:28px}
      .app-panel,.queue-layout,.review-layout,.receipt-panel{min-height:540px}
      .queue-row{grid-template-columns:80px minmax(150px,1fr) minmax(130px,.7fr)}
      .row-status{display:none}
      .bento{grid-template-rows:280px 280px}
      .section-heading{gap:42px}
    }
    @media(max-width:860px){
      .page{border-radius:28px}
      .site-header{width:calc(100% - 32px)}
      .nav-links>a:not(.button){display:none}
      .app-meta .badge{max-width:170px;justify-content:center;white-space:normal;text-align:center}
      .queue-head .badge{max-width:170px;justify-content:center;white-space:normal;text-align:center;overflow-wrap:anywhere}
      .hero-main{grid-template-columns:1fr;min-height:auto}
      .hero-copy{padding-bottom:0}
      .hero-motion-host{width:min(620px,100%);margin:26px auto 0}
      .app-stage{margin-top:-34px}
      .queue-layout{grid-template-columns:150px minmax(0,1fr)}
      .review-layout{grid-template-columns:1fr}
      .inspector{border-top:1px solid var(--line);border-left:0}
      .app-panel,.queue-layout,.review-layout,.receipt-panel{min-height:auto}
      .section-heading{grid-template-columns:minmax(0,1fr);gap:20px}
      .bento{grid-template-columns:1fr 1fr;grid-template-rows:310px 280px 280px}
      .feature-card[data-card="source"]{grid-column:span 2}
      .feature-card[data-card="local"]{grid-column:span 1}
      .guardrails,.evidence-grid{grid-template-columns:1fr 1fr}
      .closing-panel{grid-template-columns:minmax(0,1fr);align-items:start}
    }
    @media(max-width:640px){
      :root{--radius-shell:28px;--radius-stage:19px;--radius-card:19px}
      .page{width:calc(100% - 12px);margin-top:6px}
      .container{width:calc(100% - 32px)}
      .site-header{top:8px;width:calc(100% - 20px);margin-top:8px}
      .site-nav{min-height:56px;padding:5px 6px 5px 13px}
      .brand-copy span{display:none}
      .nav-links .button{min-height:44px;padding-inline:13px;font-size:12px}
      .hero{padding-top:40px}
      .hero-main{gap:10px}
      .hero-copy{padding-top:20px}
      .display{font-size:44px;line-height:.96}
      .lead{margin-top:20px;font-size:16px;line-height:1.5}
      .hero-actions{align-items:stretch;flex-direction:column}
      .hero-actions .button{width:100%}
      .hero-actions .button[data-variant="outline"],.cta-note{display:none}
      .hero-motion-host{margin-top:22px}
      .app-stage{margin-top:16px;padding:7px;backdrop-filter:none}
      .app-topbar{align-items:flex-start;padding:10px}
      .app-title{font-size:12px}
      .app-meta{align-items:flex-end;flex-direction:column;gap:4px}
      .app-meta>span:not(.badge){display:none}
      .product-tabs{width:calc(100% - 16px);margin:8px;padding:4px}
      .product-tab{min-width:0}
      .queue-layout{display:block}
      .queue-nav{display:none}
      .queue-nav strong{display:none}
      .queue-filter{min-width:max-content;padding-inline:9px;gap:8px}
      .queue-main{padding:20px 13px 16px}
      .queue-head{display:block}
      .queue-head h2{font-size:21px}
      .queue-head .badge,.run-legend{display:none}
      .run-strip{margin:16px 0 10px}
      .queue-row{min-height:84px;grid-template-columns:72px minmax(0,1fr);gap:8px 12px;padding:12px}
      .row-owner{grid-column:2}
      .creative-layout{grid-template-columns:1fr;gap:18px}
      .creative-preview{width:min(290px,100%);margin-inline:auto}
      .review-main{padding:20px 14px}
      .review-title{display:block}
      .review-title .badge{margin-top:10px}
      .inspector{padding:20px 14px}
      .inspector-actions{position:sticky;z-index:3;bottom:0;margin:16px -14px -20px;padding:12px 14px 14px;border-top:1px solid var(--line);background:rgba(248,248,246,.96);backdrop-filter:blur(14px)}
      .inspector-foot{order:2;margin-top:14px!important}
      .inspector-actions{order:3}
      .receipt-panel{padding:14px}
      .receipt-card{grid-template-columns:1fr}
      .receipt-summary,.receipt-data{padding:22px}
      .receipt-data{border-top:1px solid var(--line);border-left:0}
      .receipt-data .receipt-actions{align-items:stretch;flex-direction:column}
      .receipt-actions .button{width:100%}
      .run-proof{grid-template-columns:1fr 1fr;transform:none}
      .run-proof .proof-label{grid-column:span 2}
      .run-proof>div{min-height:98px}
      .section{padding:86px 0}
      .section-title{font-size:clamp(41px,12vw,56px)}
      .route-line{grid-template-columns:1fr;gap:8px}
      .route-line:before,.route-line:after,.route-segment{display:none}
      .bento{grid-template-columns:1fr;grid-template-rows:auto}
      .feature-card{min-height:270px;padding:24px}
      .feature-card[data-card="source"],.feature-card[data-card="local"]{grid-column:auto}
      .source-map{right:20px;bottom:20px;width:58%}
      .local-window{right:20px;width:55%}
      .safeguard{padding-bottom:86px}
      .safeguard-panel{padding:42px 24px;border-radius:24px}
      .guardrails,.evidence-grid{grid-template-columns:1fr}
      .guardrails div{min-height:112px}
      .evidence{padding:86px 0}
      .evidence-link{min-height:140px}
      .closing{padding-top:72px}
      .closing-panel{padding:34px 22px}
      .closing-actions{align-items:stretch;flex-direction:column;width:100%}
      .footer-row{display:grid;gap:10px}
      .footer-links{flex-wrap:wrap}
    }
    @media(max-width:360px){
      .brand-copy strong{font-size:12px}
      .nav-links .button{display:none}
      .hero-actions .button-arrow{display:none}
      .display{font-size:39px}
      .run-proof>div{padding:15px}
      .proof-number strong{font-size:29px}
    }
    @media(prefers-reduced-motion:reduce){
      html{scroll-behavior:auto}
      *,*:before,*:after{animation-duration:.01ms!important;animation-delay:0ms!important;transition-duration:.01ms!important;scroll-behavior:auto!important}
      [data-reveal],.hero-copy [data-rise],.timeline li{opacity:1;transform:none}
      .wchar{font-variation-settings:"wght" 600!important}
    }
    @media(prefers-reduced-transparency:reduce){.site-header,.app-stage,.image-label,.inspector-actions{backdrop-filter:none;background:#fff}}
    @media(prefers-contrast:more){
      :root{--body:#343538;--muted:#55575C;--line:rgba(23,23,25,.2);--line-strong:rgba(23,23,25,.36)}
      .app-stage,.feature-card,.evidence-link,.closing-panel{border-width:2px}
    }
    """


def _finish(template: str) -> str:
    return (
        template.replace("__STYLES__", _shared_styles().strip())
        .replace("__VERSION__", VERSION)
        .replace("__UPDATED_DATE__", UPDATED_DATE)
        .replace("__SOCIAL_CARD__", SOCIAL_CARD)
    )


def _product_shell() -> str:
    return r"""
    <div class="app-stage" id="product">
      <div class="app-shell">
        <div class="app-topbar">
          <div class="app-title"><span class="brand-mark" aria-hidden="true"></span><span>Launch Control</span></div>
          <div class="app-meta"><span>Launch / 14 Jul</span><span class="badge" data-tone="orange">Demo data / local only</span></div>
        </div>
        <div class="product-tabs" role="tablist" aria-label="Live product walkthrough">
          <span class="t-tabs-pill" aria-hidden="true"></span>
          <button class="product-tab" id="tab-queue" type="button" role="tab" aria-selected="true" aria-controls="panel-queue" tabindex="0">Queue</button>
          <button class="product-tab" id="tab-review" type="button" role="tab" aria-selected="false" aria-controls="panel-review" tabindex="-1">Review</button>
          <button class="product-tab" id="tab-receipt" type="button" role="tab" aria-selected="false" aria-controls="panel-receipt" tabindex="-1">Receipt</button>
        </div>
        <section class="app-panel" id="panel-queue" role="tabpanel" aria-labelledby="tab-queue">
          <div class="queue-layout">
            <nav class="queue-nav" aria-label="Queue filters">
              <strong>Creative rows</strong>
              <button class="queue-filter" type="button">All <span>100</span></button>
              <button class="queue-filter" type="button">Ready <span>30</span></button>
              <button class="queue-filter" data-active="true" type="button">Needs decision <span>10</span></button>
              <button class="queue-filter" type="button">Needs fix <span>60</span></button>
            </nav>
            <div class="queue-main">
              <div class="queue-head"><div><h2>10 creatives need a decision</h2><p>One owner and one next action for every exception.</p></div><span class="badge">Batch 78f20843aea8a367</span></div>
              <div class="run-strip" role="img" aria-label="30 ready, 10 need a human decision, 60 blocked"><span></span><span></span><span></span></div>
              <div class="run-legend"><span><b>30</b> ready</span><span><b>10</b> human decision</span><span><b>60</b> blocked</span></div>
              <div class="queue-list" aria-label="Rows requiring a decision">
                <button class="queue-row" data-selected="true" data-open-review type="button"><span class="row-id">cr_007</span><span class="row-name"><strong>Launch offer 07</strong><span>Possible duplicate</span></span><span class="row-owner"><strong>Creative Ops Manager</strong><span>Decision required</span></span><span class="row-status">Review now</span></button>
                <button class="queue-row" data-open-review type="button"><span class="row-id">cr_017</span><span class="row-name"><strong>Launch offer 17</strong><span>Possible duplicate</span></span><span class="row-owner"><strong>Creative Ops Manager</strong><span>Decision required</span></span><span class="row-status">Review now</span></button>
                <button class="queue-row" data-open-review type="button"><span class="row-id">cr_027</span><span class="row-name"><strong>Launch offer 27</strong><span>Possible duplicate</span></span><span class="row-owner"><strong>Creative Ops Manager</strong><span>Decision required</span></span><span class="row-status">Review now</span></button>
                <button class="queue-row" data-open-review type="button"><span class="row-id">cr_037</span><span class="row-name"><strong>Launch offer 37</strong><span>Possible duplicate</span></span><span class="row-owner"><strong>Creative Ops Manager</strong><span>Decision required</span></span><span class="row-status">Review now</span></button>
              </div>
            </div>
          </div>
        </section>
        <section class="app-panel" id="panel-review" role="tabpanel" aria-labelledby="tab-review" hidden>
          <div class="review-layout">
            <div class="review-main">
              <div class="breadcrumb">Review queue / cr_007</div>
              <div class="review-title"><div><h2>Launch offer 07</h2><p>cr_007 / row 8 / image / feed</p></div><span class="badge">Creative Ops Manager</span></div>
              <div class="creative-layout">
                <div class="creative-preview" role="img" aria-label="Synthetic orange creative preview for Launch offer 07"><span class="preview-chip">Prospecting US</span><div class="preview-copy"><span>Hook 07 for prospecting US</span><strong>Launch<br>offer 07</strong></div></div>
                <dl class="facts">
                  <div><dt>Campaign</dt><dd>camp_launch</dd></div><div><dt>Ad set</dt><dd>as_prospecting_us</dd></div><div><dt>Market</dt><dd>US</dd></div><div><dt>Post mode</dt><dd>reuse_existing_post</dd></div><div><dt>Post ID</dt><dd>post_c30fe8f1d4</dd></div><div><dt>Destination</dt><dd>example.invalid/launch-us</dd></div>
                </dl>
              </div>
            </div>
            <aside class="inspector" data-animate="in" aria-labelledby="decision-title">
              <div class="inspector-kicker"><img src="assets/icons/circle-alert.svg" alt=""> Human decision required</div>
              <h3 id="decision-title">Possible duplicate</h3>
              <p>Asset appears to be reused and needs intent confirmed.</p>
              <div class="decision-card"><strong>Proposed fix</strong><p>Confirm intentional reuse or return the row for replacement.</p><div class="owner-line"><span>Owner</span><strong>Creative Ops Manager</strong></div></div>
              <div class="inspector-actions"><button class="button" data-variant="orange" id="confirm-decision" type="button">Confirm intentional reuse</button><button class="button" data-variant="outline" type="button">Return for replacement</button><button class="button" data-variant="danger" type="button">Block row</button></div>
              <p class="inspector-foot">Saves browser-local state / No Meta API call</p>
            </aside>
          </div>
        </section>
        <section class="app-panel" id="panel-receipt" role="tabpanel" aria-labelledby="tab-receipt" hidden>
          <div class="receipt-panel">
            <div class="receipt-card" id="receipt-card" data-live="false">
              <div class="receipt-summary"><div class="success-icon"><img src="assets/icons/check-circle-2.svg" alt=""></div><h2>Intentional reuse confirmed</h2><p>cr_007 is ready for dry-run export.</p><ol class="timeline"><li><strong>Duplicate flagged</strong><span>System validator</span></li><li><strong>Reuse confirmed</strong><span>Creative Ops Manager</span></li><li><strong>Review state updated</strong><span>Browser-local</span></li></ol><p id="decision-count">Decision saved locally.</p></div>
              <div class="receipt-data"><h4>Decision receipt</h4><dl><div><dt>State</dt><dd>confirmed_ready</dd></div><div><dt>Event</dt><dd>row_decision_updated</dd></div><div><dt>Creative</dt><dd>cr_007</dd></div><div><dt>Source</dt><dd>row_007</dd></div><div><dt>Reviewer</dt><dd>Creative Ops Manager</dd></div><div><dt>Dataset</dt><dd title="synthetic_fixture_only">synthetic fixture</dd></div><div><dt>Storage</dt><dd>Browser local</dd></div><div><dt>Mutation allowed</dt><dd>false</dd></div><div><dt>External mutation</dt><dd>false</dd></div><div><dt>Batch</dt><dd>78f20843aea8a367</dd></div><div><dt>Manifest SHA</dt><dd title="4b09268ddcb1f49020f66777d0bcdd734e22add2e77657578d68201ad38ccabf">4b09268ddcb1…</dd></div></dl><div class="receipt-actions"><button class="button" data-variant="primary" id="back-to-queue" type="button">Back to queue</button><button class="button" data-variant="outline" id="export-review" type="button">Export JSON</button></div></div>
            </div>
          </div>
        </section>
        <p class="live-region" id="decision-live" aria-live="polite"></p>
      </div>
    </div>
    """


def render_product_landing_v30() -> str:
    return _finish(
        r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <meta name="theme-color" content="#ECEDEE">
  <meta name="description" content="Catch creative launch mistakes before Ads Manager. Validate every row, route exceptions and keep ambiguous decisions human.">
  <meta name="author" content="Mathieu Petroni">
  <link rel="canonical" href="https://mattyu-dev.github.io/creative-launch-workspace/">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
  <link rel="preload" href="assets/inter-latin-variable.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="me" href="https://www.linkedin.com/in/mathieu-petroni/">
  <link rel="me" href="https://github.com/mattyu-dev">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Creative Launch Workspace">
  <meta property="og:title" content="Catch creative launch mistakes before Ads Manager">
  <meta property="og:description" content="Validate every creative row, route exceptions and keep ambiguous decisions human.">
  <meta property="og:url" content="https://mattyu-dev.github.io/creative-launch-workspace/">
  <meta property="og:image" content="https://mattyu-dev.github.io/creative-launch-workspace/assets/__SOCIAL_CARD__">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Launch Control pre-launch QA interface for Meta Ads">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Catch creative launch mistakes before Ads Manager">
  <meta name="twitter:description" content="Validate every creative row, route exceptions and keep ambiguous decisions human.">
  <meta name="twitter:image" content="https://mattyu-dev.github.io/creative-launch-workspace/assets/__SOCIAL_CARD__">
  <meta name="twitter:image:alt" content="Launch Control pre-launch QA interface for Meta Ads">
  <title>Launch Control | Pre-launch QA for Meta Ads</title>
  <style>__STYLES__</style>
  <script type="application/ld+json">{"@context":"https://schema.org","@graph":[{"@type":"Person","@id":"https://mattyu-dev.github.io/#person","name":"Mathieu Petroni","jobTitle":"AI Automation Builder","url":"https://www.linkedin.com/in/mathieu-petroni/","sameAs":["https://github.com/mattyu-dev","https://www.linkedin.com/in/mathieu-petroni/"]},{"@type":"SoftwareApplication","name":"Launch Control","alternateName":"Creative Launch Workspace","applicationCategory":"BusinessApplication","operatingSystem":"Web","softwareVersion":"__VERSION__","description":"Pre-launch QA and exception routing for Meta Ads creative operations.","url":"https://mattyu-dev.github.io/creative-launch-workspace/","author":{"@id":"https://mattyu-dev.github.io/#person"}},{"@type":"WebSite","name":"Creative Launch Workspace","url":"https://mattyu-dev.github.io/creative-launch-workspace/","dateModified":"__UPDATED_DATE__","author":{"@id":"https://mattyu-dev.github.io/#person"}}]}</script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to product</a>
  <div class="nav-sentinel" aria-hidden="true"></div>
  <header class="site-header" data-scrolled="false">
    <nav class="site-nav" aria-label="Product navigation">
      <a class="brand" href="index.html"><span class="brand-mark" aria-hidden="true"></span><span class="brand-copy"><strong>Launch Control</strong><span>Pre-launch QA for Meta Ads</span></span></a>
      <div class="nav-links"><a href="#product">Product</a><a href="#workflow">Workflow</a><a href="#safeguards">Safeguards</a><a href="#evidence">Evidence</a><a class="button" data-variant="primary" href="workspace.html?guided=1">Try the live workspace <span class="button-arrow" aria-hidden="true">↗</span></a></div>
    </nav>
  </header>
  <div class="page">
    <main id="main">
      <section class="hero" aria-labelledby="hero-title">
        <div class="container">
          <div class="hero-main">
            <div class="hero-copy"><div class="eyebrow" data-rise>Pre-launch QA for Meta Ads</div><h1 class="display" id="hero-title" data-rise data-wchar>Catch creative launch mistakes before Ads Manager.</h1><p class="lead" data-rise>Validate approvals, placements, destinations, naming and UTMs across every creative row. Route exceptions to the right owner. Keep ambiguous decisions human.</p><div class="hero-actions" data-rise><a class="button" data-variant="primary" href="workspace.html?guided=1">Try the live workspace <span class="button-arrow" aria-hidden="true">↗</span></a><a class="button" data-variant="outline" href="#workflow">See how it works <span aria-hidden="true">↓</span></a><span class="cta-note">Interactive demo / no signup</span></div></div>
            <div class="hero-motion-host" id="hero-motion-root" aria-label="Recorded product trace from detection to receipt"><div class="motion-fallback"><header><span>Recorded synthetic run</span><span>Read-only replay</span></header><ol><li><b>01</b>Detect</li><li><b>02</b>Route</li><li><b>03</b>Prove</li></ol><article><div><small>Recorded decision</small><strong>cr_007 · Possible duplicate</strong><span>Routed to Creative Ops Manager, then saved locally after human review.</span></div></article><footer>One exception. One owner. One receipt.</footer></div></div>
          </div>
          __PRODUCT_SHELL__
          <div class="run-proof" aria-label="Current synthetic run summary" data-reveal><div class="proof-label"><span>Current synthetic run</span><strong>Fixture data, no external writes</strong></div><div class="proof-number"><strong>100</strong><span>creative rows</span></div><div class="proof-number"><strong>70</strong><span>issues routed</span></div><div class="proof-number"><strong>10</strong><span>human reviews</span></div><div class="proof-number"><strong>0</strong><span>external writes</span></div></div>
        </div>
      </section>

      <section class="section" id="workflow" aria-labelledby="workflow-title">
        <div class="container">
          <div class="section-heading" data-reveal><h2 class="section-title" id="workflow-title">Detect the quiet failures. <span class="serif-accent">Route the decision.</span></h2><p class="section-lead">The product keeps source context, deterministic checks and accountable review in one continuous path.</p></div>
          <div class="route-line" aria-label="Detect, Route, Prove" data-reveal><span class="route-step"><b>01</b>Detect</span><span class="route-segment"></span><span class="route-step"><b>02</b>Route</span><span class="route-segment"></span><span class="route-step"><b>03</b>Prove</span></div>
          <div class="bento">
            <article class="feature-card" data-card="source" data-reveal><img class="icon" src="assets/icons/scan-line.svg" alt=""><h3>Source fidelity stays visible</h3><p>Approvals, placements, destinations, naming and UTMs are checked against the same typed launch context.</p><div class="source-map" aria-hidden="true"><span></span><span></span><span></span></div></article>
            <article class="feature-card" data-card="route" data-reveal><img class="icon" src="assets/icons/route.svg" alt=""><h3>Every exception gets an owner</h3><p>Issue, owner and next action travel together.</p><div class="route-visual" aria-hidden="true"><span></span><b>ROUTE</b><span></span></div></article>
            <article class="feature-card" data-card="local" data-reveal><img class="icon" src="assets/icons/file-json.svg" alt=""><h3>Decisions remain inspectable</h3><p>Each human review produces browser-local state and an exportable receipt without calling Meta.</p><div class="local-window" aria-hidden="true"><span></span><span></span><span></span><span></span></div></article>
            <article class="feature-card" data-card="boundary" data-reveal><img class="icon" src="assets/icons/shield-check.svg" alt=""><h3>The write boundary stays closed</h3><p>The demo can record local review state. It cannot call Meta, upload assets or change spend.</p><div class="boundary-signal"><span>external_mutation</span><strong>false</strong></div></article>
          </div>
        </div>
      </section>

      <section class="safeguard" id="safeguards" aria-labelledby="safeguard-title">
        <div class="container"><div class="safeguard-panel" data-reveal><div class="eyebrow">Guardrails by design</div><h2 id="safeguard-title">Automation proposes. Rules verify. <span class="serif-accent">People decide.</span></h2><p>The system can structure source context and suggest a correction. It cannot approve a field, bypass a rule or publish a campaign.</p><div class="guardrails"><div><b>01</b><strong>AI proposes typed fields with source evidence.</strong></div><div><b>02</b><strong>Deterministic validators fail closed.</strong></div><div><b>03</b><strong>Ambiguous intent stays with a named reviewer.</strong></div></div></div></div>
      </section>

      <section class="evidence" id="evidence" aria-labelledby="evidence-title">
        <div class="container"><div class="section-heading" data-reveal><h2 class="section-title" id="evidence-title">Proof you can inspect.</h2><p class="section-lead">The product surface is backed by versioned contracts, reproducible validators and browser quality gates.</p></div><div class="evidence-grid"><a class="evidence-link" href="brief-evidence.html" data-reveal><img src="assets/icons/file-json.svg" alt=""><strong>Contracts</strong><span>Inspect field evidence and review state.</span></a><a class="evidence-link" href="fix-lab.html" data-reveal><img src="assets/icons/route.svg" alt=""><strong>Deterministic replay</strong><span>Run the same golden scenarios again.</span></a><a class="evidence-link" href="https://github.com/mattyu-dev/creative-launch-workspace/actions" data-reveal><img src="assets/icons/shield-check.svg" alt=""><strong>CI quality gates</strong><span>See tests, browser QA and accessibility checks.</span></a><a class="evidence-link" href="https://github.com/mattyu-dev/creative-launch-workspace/blob/main/docs/architecture/system.md" data-reveal><img src="assets/icons/external-link.svg" alt=""><strong>Architecture</strong><span>Trace the trust boundaries end to end.</span></a></div></div>
      </section>

      <section class="closing" aria-labelledby="closing-title"><div class="container"><div class="closing-panel" data-reveal><div><div class="eyebrow">Launch with control</div><h2 id="closing-title">Catch the mistake while it is still a row.</h2><p>Open the live workspace and follow one creative from exception to receipt.</p></div><div class="closing-actions"><a class="button" data-variant="primary" href="workspace.html?guided=1">Try the live workspace <span class="button-arrow" aria-hidden="true">↗</span></a><a class="button" data-variant="outline" href="https://github.com/mattyu-dev/creative-launch-workspace">View source</a></div></div></div></section>
    </main>
    <footer><div class="container footer-row"><span>Launch Control. Built by <a href="https://www.linkedin.com/in/mathieu-petroni/" rel="me external">Mathieu Petroni</a>.</span><span class="footer-links"><a href="https://github.com/mattyu-dev/creative-launch-workspace">MIT source</a><a href="brief-evidence.html">Evidence</a><a href="fix-lab.html">Fix lab</a></span></div></footer>
  </div>
  <script>
    (()=>{
      const reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
      const header=document.querySelector('.site-header');
      const sentinel=document.querySelector('.nav-sentinel');
      if('IntersectionObserver' in window){
        const navObserver=new IntersectionObserver(([entry])=>header.dataset.scrolled=String(!entry.isIntersecting),{threshold:0});
        navObserver.observe(sentinel);
        const revealObserver=new IntersectionObserver((entries,observer)=>entries.forEach((entry)=>{if(entry.isIntersecting){entry.target.dataset.visible='true';observer.unobserve(entry.target)}}),{rootMargin:'0px 0px -8% 0px',threshold:.08});
        document.querySelectorAll('[data-reveal]').forEach((item)=>revealObserver.observe(item));
      }else{document.querySelectorAll('[data-reveal]').forEach((item)=>item.dataset.visible='true')}

      const tablist=document.querySelector('[role="tablist"]');
      const tabs=[...tablist.querySelectorAll('[role="tab"]')];
      const pill=tablist.querySelector('.t-tabs-pill');
      function movePill(tab,instant=false){const old=pill.style.transition;pill.style.transition=instant?'none':old;pill.style.left=`${tab.offsetLeft}px`;pill.style.width=`${tab.offsetWidth}px`;if(instant)requestAnimationFrame(()=>pill.style.transition='')}
      function activateTab(tab,focus=false){tabs.forEach((item)=>{const active=item===tab;item.setAttribute('aria-selected',String(active));item.tabIndex=active?0:-1;document.getElementById(item.getAttribute('aria-controls')).hidden=!active});movePill(tab);if(focus)tab.focus()}
      movePill(tabs[0],true);
      tabs.forEach((tab,index)=>{tab.addEventListener('click',()=>activateTab(tab));tab.addEventListener('keydown',(event)=>{if(!['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;event.preventDefault();let next=index;if(event.key==='ArrowLeft')next=(index-1+tabs.length)%tabs.length;if(event.key==='ArrowRight')next=(index+1)%tabs.length;if(event.key==='Home')next=0;if(event.key==='End')next=tabs.length-1;activateTab(tabs[next],true)})});
      new ResizeObserver(()=>movePill(tabs.find((tab)=>tab.getAttribute('aria-selected')==='true'),true)).observe(tablist);
      document.querySelectorAll('[data-open-review]').forEach((row)=>row.addEventListener('click',()=>activateTab(tabs[1],true)));

      const storageKey='launch-control-v3-demo';
      const receipt=document.getElementById('receipt-card');
      const live=document.getElementById('decision-live');
      const count=document.getElementById('decision-count');
      const confirmed=()=>localStorage.getItem(storageKey)==='confirmed';
      function showReceipt(fromDecision=false){receipt.dataset.live='true';count.textContent=fromDecision?'9 decisions remaining':'Decision saved locally.';activateTab(tabs[2],true)}
      document.getElementById('confirm-decision').addEventListener('click',()=>{localStorage.setItem(storageKey,'confirmed');live.textContent='Decision saved locally. 9 decisions remaining.';showReceipt(true)});
      document.getElementById('back-to-queue').addEventListener('click',()=>activateTab(tabs[0],true));
      document.getElementById('export-review').addEventListener('click',()=>{const data={state:'confirmed_ready',event:'row_decision_updated',creative:'cr_007',source:'row_007',reviewer:'Creative Ops Manager',dataset:'synthetic_fixture_only',storage:'Browser local',mutation_allowed:false,external_mutation:false,batch:'78f20843aea8a367',manifest_sha:'4b09268ddcb1f49020f66777d0bcdd734e22add2e77657578d68201ad38ccabf'};const link=document.createElement('a');link.href=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));link.download='review_state.json';link.click();setTimeout(()=>URL.revokeObjectURL(link.href),0)});
      tabs[2].addEventListener('click',()=>{receipt.dataset.live=confirmed()?'true':'false';count.textContent='Decision saved locally.'});

      const title=document.querySelector('[data-wchar]');
      if(title&&!reduced.matches&&!window.matchMedia('(max-width: 360px)').matches){title.addEventListener('pointerenter',()=>{const label=title.textContent;title.setAttribute('aria-label',label);const fragment=document.createDocumentFragment();label.split(' ').forEach((word,index)=>{if(index)fragment.append(document.createTextNode(' '));const wordNode=document.createElement('span');wordNode.className='wchar-word';wordNode.setAttribute('aria-hidden','true');[...word].forEach((letter)=>{const charNode=document.createElement('span');charNode.className='wchar';charNode.textContent=letter;wordNode.append(charNode)});fragment.append(wordNode)});title.replaceChildren(fragment);const chars=[...title.querySelectorAll('.wchar')];let point=null;let raf=0;title.addEventListener('pointermove',(event)=>{point={x:event.clientX,y:event.clientY};if(raf)return;raf=requestAnimationFrame(()=>{chars.forEach((char)=>{const rect=char.getBoundingClientRect();const d=Math.hypot(point.x-(rect.left+rect.width/2),point.y-(rect.top+rect.height/2));const weight=d<200?600+(1-d/200)*300:600;char.style.fontVariationSettings=`'wght' ${Math.round(weight)}`});raf=0})});title.addEventListener('pointerleave',()=>chars.forEach((char)=>char.style.fontVariationSettings="'wght' 600"))},{once:true})}
    })();
  </script>
  <script type="module">
    const loadLaunchControlMotion=()=>import("./assets/launch-control-motion.js");
    requestAnimationFrame(()=>setTimeout(loadLaunchControlMotion,0));
  </script>
</body>
</html>
""".replace("__PRODUCT_SHELL__", _product_shell().strip())
    )


def render_social_card_page_v30() -> str:
    return r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=1200, initial-scale=1"><meta name="author" content="Mathieu Petroni"><style>
@font-face{font-family:"Inter";src:url("assets/inter-latin-variable.woff2") format("woff2-variations");font-weight:100 900;font-display:swap}@font-face{font-family:"Instrument Serif";src:url("assets/instrument-serif-latin-italic.woff2") format("woff2");font-style:italic;font-weight:400;font-display:swap}*{box-sizing:border-box}html,body{width:1200px;height:630px;margin:0;overflow:hidden}body{padding:18px;color:#232427;background:#ECEDEE;font-family:"Inter",sans-serif}main{width:1164px;height:594px;position:relative;overflow:hidden;display:grid;grid-template-columns:535px 629px;border:1px solid rgba(255,255,255,.75);border-radius:40px;background:#F4F5F5;box-shadow:0 1px 0 rgba(255,255,255,.9) inset}.copy{z-index:2;display:flex;flex-direction:column;padding:43px 18px 40px 48px}.brand{display:flex;align-items:center;gap:11px}.mark{width:31px;height:31px;position:relative}.mark:before,.mark:after{content:"";position:absolute;top:6px;width:19px;height:19px;border-radius:50%}.mark:before{left:0;background:#171719}.mark:after{left:12px;background:#E34A32}.brand-copy{display:grid;line-height:1}.brand-copy strong{font-size:15px}.brand-copy span{margin-top:6px;color:#7B7D82;font-size:10px}.hero{margin-top:65px}.eyebrow{color:#E34A32;font-size:11px;font-weight:700;letter-spacing:.07em;text-transform:uppercase}.hero h1{max-width:500px;margin:15px 0 0;font-size:56px;font-weight:620;line-height:.94;letter-spacing:-.05em}.hero p{max-width:455px;margin:20px 0 0;color:#55575C;font-size:15px;line-height:1.5}.copy footer{display:flex;justify-content:space-between;margin-top:auto;color:#7B7D82;font-size:10px}.visual{position:relative}.trace{position:absolute;left:18px;right:50px;top:92px;height:112px;padding:18px 22px;border:1px solid rgba(23,23,25,.08);border-radius:18px;background:rgba(255,255,255,.82);box-shadow:0 22px 50px -36px rgba(35,36,39,.65)}.trace-line{height:2px;position:absolute;left:54px;right:54px;top:54px;background:linear-gradient(90deg,rgba(227,74,50,.2),#E34A32,rgba(227,74,50,.2))}.trace-node{width:34px;height:34px;position:absolute;top:38px;display:grid;place-items:center;border:2px solid #E34A32;border-radius:50%;color:#E34A32;background:#FFF9F7;font-size:9px;font-weight:760}.trace-node:nth-child(2){left:38px}.trace-node:nth-child(3){left:50%;transform:translateX(-50%)}.trace-node:nth-child(4){right:38px}.trace-labels{display:flex;justify-content:space-between;margin-top:52px;color:#55575C;font-size:8px;font-weight:650;text-transform:uppercase}.app{position:absolute;left:-12px;right:30px;bottom:34px;height:245px;overflow:hidden;border:8px solid rgba(255,255,255,.68);border-radius:22px;background:#FCFCFB;box-shadow:0 26px 60px -36px rgba(35,36,39,.7)}.bar{height:34px;display:flex;align-items:center;justify-content:space-between;padding:0 13px;border-bottom:1px solid rgba(23,23,25,.09);font-size:8px;font-weight:650}.bar span:last-child{padding:3px 7px;border-radius:999px;color:#B93624;background:#FFF0EC}.tabs{display:flex;gap:5px;padding:7px 11px;border-bottom:1px solid rgba(23,23,25,.09)}.tabs b{padding:5px 12px;border-radius:7px;color:#777;font-size:8px}.tabs b:first-child{color:#232427;background:#F0F0EE}.window{display:grid;grid-template-columns:100px 1fr;height:176px}.side{padding:12px 10px;border-right:1px solid rgba(23,23,25,.09);background:#F8F8F6}.side span{display:block;height:8px;margin-bottom:8px;border-radius:5px;background:#E4E4E1}.side span:nth-child(2){background:#FFF0EC}.rows{padding:13px}.rows h2{margin:0 0 12px;font-size:15px}.row{height:32px;display:grid;grid-template-columns:55px 1fr 110px;align-items:center;border-top:1px solid rgba(23,23,25,.08);font-size:7px}.row:first-of-type{box-shadow:3px 0 0 #E34A32 inset;background:#FFF9F7}.row b{font-family:monospace}.route{position:absolute;right:50px;top:45px;color:#E34A32;font-size:9px;font-weight:720;letter-spacing:.06em}
</style></head><body><main><section class="copy"><div class="brand"><span class="mark"></span><span class="brand-copy"><strong>Launch Control</strong><span>Pre-launch QA for Meta Ads</span></span></div><div class="hero"><div class="eyebrow">Detect / Route / Prove</div><h1>Catch creative launch mistakes before Ads Manager.</h1><p>Validate every creative row. Route exceptions to the right owner. Keep ambiguous decisions human.</p></div><footer><strong>Interactive product</strong><span>Mathieu Petroni</span></footer></section><section class="visual"><span class="route">RECORDED DECISION TRACE</span><div class="trace"><div class="trace-line"></div><b class="trace-node">01</b><b class="trace-node">02</b><b class="trace-node">✓</b><div class="trace-labels"><span>Detect</span><span>Route</span><span>Prove</span></div></div><div class="app"><div class="bar"><span>Launch Control</span><span>Demo data / local only</span></div><div class="tabs"><b>Queue</b><b>Review</b><b>Receipt</b></div><div class="window"><div class="side"><span></span><span></span><span></span><span></span></div><div class="rows"><h2>10 creatives need a decision</h2><div class="row"><b>cr_007</b><span>Possible duplicate</span><span>Creative Ops Manager</span></div><div class="row"><b>cr_017</b><span>Possible duplicate</span><span>Creative Ops Manager</span></div><div class="row"><b>cr_027</b><span>Possible duplicate</span><span>Creative Ops Manager</span></div></div></div></div></section></main></body></html>"""
