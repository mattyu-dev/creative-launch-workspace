from __future__ import annotations

import json
from typing import Any

from .demo_payload import build_demo_payload

VERSION = "4.0.0"
UPDATED_DATE = "2026-07-16"
SOCIAL_CARD = "social-card-v5.png"


def _shared_styles() -> str:
    return r"""
    @font-face{font-family:"Inter";src:url("assets/inter-latin-variable.woff2") format("woff2-variations");font-style:normal;font-weight:100 900;font-display:optional}
    @font-face{font-family:"Inter Fallback";src:local("Arial");size-adjust:101.75%;ascent-override:97%;descent-override:24%;line-gap-override:0%}
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
      --orange-copy:#A93625;
      --orange-soft:#FFF0EC;
      --line:rgba(23,23,25,.09);
      --line-strong:rgba(23,23,25,.16);
      --success:#287A4D;
      --danger:#B9382B;
      --warning:#9A5A12;
      --ring:#E34A32;
      --sans:"Inter","Inter Fallback",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
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
    :focus-visible{outline:3px solid var(--ring);outline-offset:3px}
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
    .hero-main{min-height:510px;position:relative;display:grid;grid-template-columns:minmax(0,1.25fr) minmax(420px,.75fr);gap:46px;align-items:center}
    .hero-copy{min-width:0;position:relative;z-index:2;padding:30px 0 84px}
    .eyebrow{margin-bottom:20px;color:var(--orange-copy);font-size:11px;font-weight:700;letter-spacing:.075em;text-transform:uppercase}
    .display{max-width:860px;margin:0;font-size:clamp(52px,4vw,56px);font-weight:600;line-height:.96;letter-spacing:-.052em;text-wrap:wrap;overflow-wrap:anywhere}
    .wchar-word{display:inline-block;white-space:nowrap}
    .wchar{display:inline-block;font-variation-settings:"wght" 600;transition:font-variation-settings 150ms linear}
    .lead{max-width:690px;margin:26px 0 0;color:var(--body);font-size:18px;line-height:1.58}
    .hero-actions{display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin-top:28px}
    .hero-motion-host{min-width:0;position:relative;z-index:2;align-self:center}
    .motion-fallback{min-height:430px;display:flex;flex-direction:column;overflow:hidden;border:1px solid var(--line);border-radius:24px;background:rgba(255,255,255,.9);box-shadow:var(--shadow-card)}
    .motion-fallback header{min-height:51px;display:flex;align-items:center;justify-content:space-between;gap:12px;padding:10px 14px;border-bottom:1px solid var(--line);font-size:11px;font-weight:650}
    .motion-fallback header span:last-child{color:var(--muted);font-weight:500}
    .motion-fallback ol{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));margin:0;padding:0 10px;border-bottom:1px solid var(--line);list-style:none}
    .motion-fallback li{min-width:0;min-height:60px;display:flex;align-items:center;gap:8px;padding:8px;color:var(--muted);font-size:11px}
    .motion-fallback li b{width:23px;height:23px;display:grid;place-items:center;border:1px solid rgba(227,74,50,.2);border-radius:50%;color:var(--orange-copy);background:var(--orange-soft);font-size:9px}
    .motion-fallback article{flex:1;display:grid;place-items:center;padding:24px;background:linear-gradient(180deg,#FCFCFB,#F8F8F6)}
    .motion-fallback article div{width:100%;padding:18px;border:1px solid rgba(227,74,50,.17);border-radius:14px;background:#FFF9F7}
    .motion-fallback article small{color:var(--orange-copy);font-size:10px;font-weight:700;letter-spacing:.06em;text-transform:uppercase}
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
    .inspector-kicker{display:flex;align-items:center;gap:8px;color:var(--orange-copy);font-size:12px;font-weight:700;letter-spacing:.055em;text-transform:uppercase}
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
    .receipt-empty{max-width:430px;padding:34px;border:1px dashed var(--line-strong);border-radius:18px;background:white;text-align:center}
    .receipt-empty h2{margin:0;font-size:23px;font-weight:650}
    .receipt-empty p{margin:10px 0 18px;font-size:13px}
    .queue-row[data-static="true"]{cursor:default}
    .queue-more{min-height:52px;display:flex;align-items:center;justify-content:center;gap:7px;color:var(--orange-copy);background:#FFFDFC;font-size:13px;font-weight:640;text-decoration:none}
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
    .cta-note{margin:12px 0 0;color:var(--muted);font-size:13px}
    .hero-copy [data-rise]:nth-child(5){animation-delay:240ms}
    .tabs-hint{margin:-4px 14px 10px;color:var(--muted);font-size:12px}
    .stakes{padding:118px 0 0}
    .stakes-heading{margin-bottom:40px}
    .stakes-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
    .stake-card{padding:26px;border:1px solid var(--line);border-radius:var(--radius-card);background:white;box-shadow:var(--shadow-card)}
    .stake-card h3{margin:0;font-size:22px;font-weight:640}
    .stake-card p{margin:10px 0 0;font-size:14px;line-height:1.55}
    .closing-note{grid-column:1/-1;margin:0;color:var(--muted);font-size:13px}
    .closing-note a{font-weight:640;text-underline-offset:3px}
    .section{padding:128px 0}
    .section-heading{display:grid;grid-template-columns:minmax(0,.9fr) minmax(320px,.55fr);gap:70px;align-items:end;margin-bottom:48px}
    .section-title{max-width:820px;margin:0;font-size:clamp(44px,5vw,70px);font-weight:610;line-height:.98;letter-spacing:-.048em}
    .serif-accent{font-family:var(--serif);font-weight:400;letter-spacing:-.01em}
    .section-lead{max-width:550px;margin:0;font-size:17px}
    .product-flow{display:grid;grid-template-columns:minmax(0,1fr) 34px minmax(0,1.18fr) 34px minmax(0,1fr);align-items:stretch;gap:8px;margin:0 0 34px;padding:9px;border:1px solid var(--line);border-radius:22px;background:rgba(255,255,255,.72);box-shadow:var(--shadow-card);list-style:none}
    .product-flow li{min-width:0;display:flex;flex-direction:column;justify-content:center;padding:17px 18px;border-radius:15px;background:var(--surface-soft)}
    .product-flow li[data-core]{color:white;background:var(--charcoal)}
    .product-flow li>span{color:var(--orange-copy);font-size:10px;font-weight:720;letter-spacing:.07em;text-transform:uppercase}
    .product-flow li[data-core]>span{color:#F58B78}
    .product-flow strong{margin-top:5px;color:var(--ink);font-size:16px;font-weight:650;line-height:1.2}
    .product-flow li[data-core] strong{color:#FFFFFF}
    .product-flow small{margin-top:6px;color:var(--muted);font-size:11px;line-height:1.4}
    .product-flow li[data-core] small{color:#D0D1D2}
    .product-flow .flow-arrow{display:grid;place-items:center;color:var(--orange-copy);font-size:20px;font-weight:500}
    .bento{display:grid;grid-template-columns:1.2fr .8fr 1fr;grid-template-rows:300px 290px;gap:16px}
    .feature-card{min-width:0;position:relative;overflow:hidden;padding:30px;border:1px solid var(--line);border-radius:var(--radius-card);background:white;box-shadow:var(--shadow-card)}
    .feature-card h3{margin:15px 0 0;font-size:24px;font-weight:640;line-height:1.05}
    .feature-card p{max-width:460px;margin:11px 0 0;font-size:13px;line-height:1.55}
    .feature-card>.icon{width:20px;height:20px}
    .feature-card[data-card="source"]{grid-column:span 2}
    .feature-card[data-card="route"]{background:var(--charcoal);color:white}
    .feature-card[data-card="route"] h3{color:#FFFFFF}
    .feature-card[data-card="route"] p{color:#B7B8BA}
    .feature-card[data-card="route"]>.icon{filter:invert(1)}
    .feature-card[data-card="local"]{grid-column:span 2;background:#F0F0ED}
    .feature-card[data-card="local"] p{max-width:calc(50% - 14px)}
    .source-map{position:absolute;right:26px;bottom:24px;width:47%;display:grid;gap:8px}
    .source-map span{height:28px;border:1px solid var(--line);border-radius:8px;background:var(--surface-soft)}
    .source-map span:nth-child(2){width:78%;margin-left:auto;border-color:rgba(227,74,50,.22);background:var(--orange-soft)}
    .route-visual{position:absolute;left:30px;right:30px;bottom:28px;display:flex;align-items:center}
    .route-visual span{flex:1;height:1px;background:rgba(255,255,255,.24)}
    .route-visual b{width:38px;height:38px;display:grid;place-items:center;border:1px solid rgba(255,255,255,.2);border-radius:50%;color:#171719;background:var(--orange);font-size:10px}
    .local-window{position:absolute;right:28px;bottom:-40px;width:48%;height:220px;padding:15px;border:1px solid var(--line);border-radius:18px;background:white;box-shadow:0 24px 50px -34px rgba(35,36,39,.5);transform:rotate(1deg)}
    .local-window span{display:block;height:9px;margin:10px 0;border-radius:999px;background:#E4E4E1}
    .local-window span:nth-child(2){width:62%;background:#F6B3A7}
    .local-window span:nth-child(3){width:82%}
    .local-window span:nth-child(4){width:48%}
    .feature-card[data-card="boundary"]{background:var(--orange-soft)}
    .boundary-signal{position:absolute;left:30px;right:30px;bottom:28px;display:grid;grid-template-columns:minmax(0,1fr) auto;gap:12px;padding:14px 16px;border:1px solid rgba(227,74,50,.16);border-radius:14px;background:rgba(255,255,255,.72);font:600 12px/1.3 var(--mono)}
    .boundary-signal span{color:var(--muted);overflow-wrap:anywhere}
    .boundary-signal strong{color:var(--orange-copy)}
    .safeguard{padding:0 0 128px}
    .safeguard-panel{position:relative;overflow:hidden;padding:72px;border-radius:32px;color:white;background:var(--charcoal);box-shadow:0 34px 74px -50px rgba(23,23,25,.8)}
    .safeguard-panel:after{content:"";position:absolute;right:-110px;top:-180px;width:460px;height:460px;border-radius:50%;background:radial-gradient(circle,rgba(227,74,50,.32),transparent 66%);pointer-events:none}
    .safeguard-panel .eyebrow{color:#F58B78}
    .safeguard-panel h2,.safeguard-panel h2 .serif-accent{max-width:920px;margin:0;color:#FFFFFF;font-size:clamp(46px,6vw,78px);font-weight:580;line-height:.98;letter-spacing:-.05em}
    .safeguard-panel>p{max-width:700px;margin:22px 0 0;color:#D0D1D2;font-size:17px}
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
    .app-stage,.section,.safeguard,.evidence,.stakes{scroll-margin-top:100px}
    .closing-panel{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:54px;align-items:end;padding:58px;border:1px solid rgba(23,23,25,.08);border-radius:30px;background:white;box-shadow:var(--shadow-card)}
    .closing-panel h2{max-width:820px;margin:0;font-size:clamp(42px,5.2vw,68px);font-weight:610;line-height:.98;letter-spacing:-.05em}
    .closing-panel p{margin:17px 0 0;font-size:16px}
    .closing-actions{display:flex;flex-wrap:wrap;gap:9px}
    footer{padding:24px 0 36px;color:var(--body);font-size:11px}
    .footer-row{display:flex;justify-content:space-between;gap:24px}
    .footer-links{display:flex;gap:18px}
    [data-reveal]{transition:transform 620ms var(--ease-out)}
    .js [data-reveal]:not([data-visible="true"]){transform:translateY(16px)}
    @media print{[data-reveal]{transform:none!important}}
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
      .queue-row[data-open-review]:hover{z-index:1;background:#FFF9F7;transform:translateY(-1px)}
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
      .app-stage{margin-top:8px}
      .queue-layout{grid-template-columns:150px minmax(0,1fr)}
      .review-layout{grid-template-columns:1fr}
      .inspector{border-top:1px solid var(--line);border-left:0}
      .app-panel,.queue-layout,.review-layout,.receipt-panel{min-height:auto}
      .section-heading{grid-template-columns:minmax(0,1fr);gap:20px}
      .bento{grid-template-columns:1fr 1fr;grid-template-rows:310px 280px 280px}
      .feature-card[data-card="source"]{grid-column:span 2}
      .feature-card[data-card="local"]{grid-column:span 1}
      .guardrails,.evidence-grid{grid-template-columns:1fr 1fr}
      .stakes-grid{grid-template-columns:1fr}
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
      .hero-actions .button[data-variant="outline"]{display:none}
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
      .product-flow{grid-template-columns:1fr;margin-bottom:24px}
      .product-flow .flow-arrow{min-height:22px;font-size:0;transform:none}
      .product-flow .flow-arrow:before{content:"↓";font-size:20px}
      .bento{grid-template-columns:1fr;grid-template-rows:auto}
      .feature-card{min-height:270px;padding:24px}
      .feature-card[data-card="source"],.feature-card[data-card="local"]{grid-column:auto}
      .source-map{right:20px;bottom:20px;width:58%}
      .local-window{right:20px;width:55%}
      .stakes{padding-top:80px}
      .stake-card{padding:22px}
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
      .cta-note{display:none}
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


def _queue_row_html(entry: dict[str, Any], interactive: bool) -> str:
    sub = entry["issue_title"] or "Passes offline checks"
    owner_line = (
        f'<span class="row-owner"><strong>{entry["owner"]}</strong><span>Decision required</span></span>'
        if entry["batch_state"] == "needs_review"
        else f'<span class="row-owner"><strong>{entry["owner"] or "Validator"}</strong><span>{entry["status_label"]}</span></span>'
    )
    status = "Review now" if entry["batch_state"] == "needs_review" else entry["status_label"]
    selected = ' data-selected="true"' if interactive and entry["creative_id"] == "cr_007" else ""
    if interactive:
        return (
            f'<button class="queue-row"{selected} data-open-review data-source-row="{entry["source_row"]}" type="button">'
            f'<span class="row-id">{entry["creative_id"]}</span>'
            f'<span class="row-name"><strong>{entry["name"]}</strong><span>{sub}</span></span>'
            f'{owner_line}<span class="row-status">{status}</span></button>'
        )
    return (
        f'<div class="queue-row" data-static="true">'
        f'<span class="row-id">{entry["creative_id"]}</span>'
        f'<span class="row-name"><strong>{entry["name"]}</strong><span>{sub}</span></span>'
        f'{owner_line}<span class="row-status">{status}</span></div>'
    )


def _product_shell(payload: dict[str, Any]) -> str:
    counts = payload["counts"]
    exception = payload["walkthrough"]["exception"]
    facts = exception["facts"]
    initial_rows = "\n                ".join(
        _queue_row_html(entry, True) for entry in payload["queue"]["needs_decision"][:4]
    )
    sha = payload["source_manifest_sha256"]
    return f"""
    <div class="app-stage" id="product">
      <div class="app-shell">
        <div class="app-topbar">
          <div class="app-title"><span class="brand-mark" aria-hidden="true"></span><span>Launch Control</span></div>
          <div class="app-meta"><span>Launch / 14 Jul</span><span class="badge" data-tone="orange">Demo data · stays on this device</span></div>
        </div>
        <div class="product-tabs" role="tablist" aria-label="Interactive demo: queue, review, receipt">
          <span class="t-tabs-pill" aria-hidden="true"></span>
          <button class="product-tab" id="tab-queue" type="button" role="tab" aria-selected="true" aria-controls="panel-queue" tabindex="0">Queue</button>
          <button class="product-tab" id="tab-review" type="button" role="tab" aria-selected="false" aria-controls="panel-review" tabindex="-1">Review</button>
          <button class="product-tab" id="tab-receipt" type="button" role="tab" aria-selected="false" aria-controls="panel-receipt" tabindex="-1">Receipt</button>
        </div>
        <p class="tabs-hint">Click any row to review it.</p>
        <section class="app-panel" id="panel-queue" role="tabpanel" aria-labelledby="tab-queue">
          <div class="queue-layout">
            <nav class="queue-nav" aria-label="Queue filters">
              <strong>Creative rows</strong>
              <button class="queue-filter" data-filter="all" type="button">All <span>{counts["total"]}</span></button>
              <button class="queue-filter" data-filter="ready" type="button">Ready <span>{counts["ready"]}</span></button>
              <button class="queue-filter" data-filter="needs_decision" data-active="true" type="button">Needs decision <span>{counts["needs_decision"]}</span></button>
              <button class="queue-filter" data-filter="blocked" type="button">Blocked <span>{counts["blocked"]}</span></button>
            </nav>
            <div class="queue-main">
              <div class="queue-head"><div><h2 id="queue-title">{counts["needs_decision"]} creatives need a decision</h2><p id="queue-sub">One owner and one next action for every exception.</p></div><span class="badge">Batch {payload["batch_id"]}</span></div>
              <div class="run-strip" role="img" aria-label="{counts["ready"]} ready, {counts["needs_decision"]} need a human decision, {counts["blocked"]} blocked"><span></span><span></span><span></span></div>
              <div class="run-legend"><span><b>{counts["ready"]}</b> ready</span><span><b>{counts["needs_decision"]}</b> need a decision</span><span><b>{counts["blocked"]}</b> blocked</span></div>
              <div class="queue-list" id="queue-list" aria-label="Creative rows for the active filter">
                {initial_rows}
              </div>
            </div>
          </div>
        </section>
        <section class="app-panel" id="panel-review" role="tabpanel" aria-labelledby="tab-review" hidden>
          <div class="review-layout">
            <div class="review-main">
              <div class="breadcrumb">Review queue / <span id="review-crumb">{exception["creative_id"]}</span></div>
              <div class="review-title"><div><h2 id="review-name">{exception["name"]}</h2><p id="review-meta">{exception["creative_id"]} / row {exception["source_row"]} / {exception["format"]} / feed</p></div><span class="badge" id="review-owner-badge">{exception["owner"]}</span></div>
              <div class="creative-layout">
                <div class="creative-preview" role="img" aria-label="Synthetic orange creative preview" id="review-preview"><span class="preview-chip">Prospecting US</span><div class="preview-copy"><span id="preview-hook">{exception["primary_text"]}</span><strong id="preview-name">{exception["name"]}</strong></div></div>
                <dl class="facts">
                  <div><dt>Campaign</dt><dd id="fact-campaign">{facts["campaign"]}</dd></div><div><dt>Ad set</dt><dd id="fact-adset">{facts["adset"]}</dd></div><div><dt>Market</dt><dd id="fact-market">{facts["market"]}</dd></div><div><dt>Post mode</dt><dd id="fact-post-mode">{facts["post_mode"]}</dd></div><div><dt>Post ID</dt><dd id="fact-post-id">{facts["post_id"]}</dd></div><div><dt>Destination</dt><dd id="fact-destination">{facts["destination"]}</dd></div>
                </dl>
              </div>
            </div>
            <aside class="inspector" data-animate="in" aria-labelledby="decision-title">
              <div class="inspector-kicker"><img src="assets/icons/circle-alert.svg" alt=""> Human decision required</div>
              <h3 id="decision-title">{exception["issue_title"]}</h3>
              <p id="decision-message">{exception["issue_message"]}</p>
              <div class="decision-card"><strong>Proposed fix</strong><p id="decision-fix">{exception["proposed_fix"]}</p><div class="owner-line"><span>Owner</span><strong id="decision-owner">{exception["owner"]}</strong></div></div>
              <div class="inspector-actions"><button class="button" data-variant="orange" id="confirm-decision" type="button">Confirm intentional reuse</button><button class="button" data-variant="outline" id="return-decision" type="button">Return for replacement</button><button class="button" data-variant="danger" id="block-decision" type="button">Block row</button></div>
              <p class="inspector-foot">Saved on this device only. Nothing is sent to Meta.</p>
            </aside>
          </div>
        </section>
        <section class="app-panel" id="panel-receipt" role="tabpanel" aria-labelledby="tab-receipt" hidden>
          <div class="receipt-panel">
            <div class="receipt-empty" id="receipt-empty">
              <h2>No decision recorded yet.</h2>
              <p>Review an exception and record one. The receipt appears here.</p>
              <button class="button" data-variant="primary" data-open-review data-source-row="{exception["source_row"]}" type="button">Review {exception["creative_id"]}</button>
            </div>
            <div class="receipt-card" id="receipt-card" data-live="false" hidden>
              <div class="receipt-summary"><div class="success-icon"><img src="assets/icons/check-circle-2.svg" alt=""></div><h2 id="receipt-title"></h2><p id="receipt-sub"></p><ol class="timeline"><li><strong id="timeline-issue"></strong><span>System validator</span></li><li><strong id="timeline-decision"></strong><span id="timeline-owner"></span></li><li><strong>Review state updated</strong><span>This device</span></li></ol><p id="decision-count"></p></div>
              <div class="receipt-data"><h3>Decision receipt</h3><dl><div><dt>State</dt><dd id="receipt-state"></dd></div><div><dt>Event</dt><dd>row_decision_updated</dd></div><div><dt>Creative</dt><dd id="receipt-creative"></dd></div><div><dt>Source</dt><dd id="receipt-source"></dd></div><div><dt>Reviewer</dt><dd id="receipt-reviewer"></dd></div><div><dt>Dataset</dt><dd title="{payload["data_classification"]}">synthetic fixture</dd></div><div><dt>Storage</dt><dd>This device</dd></div><div><dt>Mutation allowed</dt><dd>false</dd></div><div><dt>External mutation</dt><dd>false</dd></div><div><dt>Batch</dt><dd>{payload["batch_id"]}</dd></div><div><dt>Manifest SHA</dt><dd title="{sha}">{sha[:12]}…</dd></div></dl><div class="receipt-actions"><a class="button" data-variant="primary" id="receipt-bridge" href="workspace.html?guided=1"></a><button class="button" data-variant="outline" id="export-review" type="button">Export JSON</button></div></div>
            </div>
          </div>
        </section>
        <p class="live-region" id="decision-live" aria-live="polite"></p>
      </div>
    </div>
    """


def render_product_landing_v30(payload: dict[str, Any] | None = None) -> str:
    payload = payload or build_demo_payload()
    exception = payload["walkthrough"]["exception"]
    counts = payload["counts"]
    return _finish(
        r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <meta name="theme-color" content="#ECEDEE">
  <meta name="description" content="Catch creative launch mistakes before Ads Manager. Validate every row, route exceptions and keep ambiguous decisions human.">
  <link rel="canonical" href="https://mattyu-dev.github.io/creative-launch-workspace/">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
  <link rel="preload" href="assets/inter-latin-variable.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="me" href="https://github.com/mattyu-dev">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Launch Control">
  <meta property="og:title" content="Catch creative launch mistakes before Ads Manager">
  <meta property="og:description" content="Check every creative row, route each failure to its owner and record the human decision before upload.">
  <meta property="og:url" content="https://mattyu-dev.github.io/creative-launch-workspace/">
  <meta property="og:image" content="https://mattyu-dev.github.io/creative-launch-workspace/assets/__SOCIAL_CARD__">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Launch Control pre-launch QA interface for Meta Ads">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Catch creative launch mistakes before Ads Manager">
  <meta name="twitter:description" content="Check every creative row, route each failure to its owner and record the human decision before upload.">
  <meta name="twitter:image" content="https://mattyu-dev.github.io/creative-launch-workspace/assets/__SOCIAL_CARD__">
  <meta name="twitter:image:alt" content="Launch Control pre-launch QA interface for Meta Ads">
  <title>Launch Control | Pre-launch QA for Meta Ads</title>
  <script>document.documentElement.classList.add('js')</script>
  <style>__STYLES__</style>
  <script type="application/ld+json">{"@context":"https://schema.org","@graph":[{"@type":"SoftwareApplication","name":"Launch Control","alternateName":"Creative Launch Workspace","applicationCategory":"BusinessApplication","operatingSystem":"Web","softwareVersion":"__VERSION__","description":"Pre-launch QA and exception routing for Meta Ads creative operations.","url":"https://mattyu-dev.github.io/creative-launch-workspace/","author":{"@type":"Organization","@id":"https://mattyu-dev.github.io/creative-launch-workspace/#org","name":"Launch Control"}},{"@type":"WebSite","name":"Launch Control","url":"https://mattyu-dev.github.io/creative-launch-workspace/","dateModified":"__UPDATED_DATE__","author":{"@id":"https://mattyu-dev.github.io/creative-launch-workspace/#org"}}]}</script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to product</a>
  <div class="nav-sentinel" aria-hidden="true"></div>
  <header class="site-header" data-scrolled="false">
    <nav class="site-nav" aria-label="Product navigation">
      <a class="brand" href="index.html"><span class="brand-mark" aria-hidden="true"></span><span class="brand-copy"><strong>Launch Control</strong><span>Pre-launch QA for Meta Ads</span></span></a>
      <div class="nav-links"><a href="#product">Product</a><a href="#workflow">Workflow</a><a href="#safeguards">Safeguards</a><a href="#evidence">Evidence</a><a class="button" data-variant="primary" href="workspace.html?guided=1">Try the live workspace <span class="button-arrow" aria-hidden="true">→</span></a></div>
    </nav>
  </header>
  <div class="page">
    <main id="main">
      <section class="hero" aria-labelledby="hero-title">
        <div class="container">
          <div class="hero-main">
            <div class="hero-copy"><div class="eyebrow" data-rise>Pre-launch QA for Meta Ads</div><h1 class="display" id="hero-title" data-rise data-wchar>Catch creative launch mistakes before Ads Manager.</h1><p class="lead" data-rise>Launch Control checks every creative row before upload, routes each problem to a named owner and records the human decision.</p><div class="hero-actions" data-rise><a class="button" data-variant="primary" href="workspace.html?guided=1">Try the live workspace <span class="button-arrow" aria-hidden="true">→</span></a><a class="button" data-variant="outline" href="#workflow">See how it works <span aria-hidden="true">↓</span></a></div><p class="cta-note" data-rise>Inspect the queue, decide one exception, export the receipt. Local demo, no Meta writes.</p></div>
            <div class="hero-motion-host" id="hero-motion-root" aria-label="Looping product walkthrough from detection to receipt"><div class="motion-fallback"><header><span>Recorded product walkthrough</span></header><ol><li><b>01</b>Detect</li><li><b>02</b>Route</li><li><b>03</b>Prove</li></ol><article><div><small>Human decision recorded</small><strong>__FALLBACK_STRONG__</strong><span>__FALLBACK_SPAN__</span></div></article><footer>Checks one row, routes the issue and records the decision.</footer></div></div>
          </div>
          __PRODUCT_SHELL__
          <div class="run-proof" aria-label="Current synthetic run summary" data-reveal><div class="proof-label"><span>Current synthetic run</span><strong>Same input, same verdicts, every run.</strong></div><div class="proof-number"><strong>__COUNT_TOTAL__</strong><span>rows checked</span></div><div class="proof-number"><strong>__COUNT_BLOCKED__</strong><span>blocked, each with a named fix</span></div><div class="proof-number"><strong>__COUNT_NEEDS__</strong><span>held for a human decision</span></div><div class="proof-number"><strong>0</strong><span>writes to Meta</span></div></div>
        </div>
      </section>

      <section class="stakes" id="stakes" aria-labelledby="stakes-title">
        <div class="container">
          <div class="stakes-heading" data-reveal><div class="eyebrow">What a bad row costs</div><h2 class="section-title" id="stakes-title">One bad row costs more than the review.</h2></div>
          <div class="stakes-grid">
            <article class="stake-card" data-reveal><h3>Wrong destination.</h3><p>The row ships with a URL its ad set never intended. The spend still delivers.</p></article>
            <article class="stake-card" data-reveal><h3>Broken UTM.</h3><p>The campaign delivers, but its results no longer line up with the campaign they report to.</p></article>
            <article class="stake-card" data-reveal><h3>Missing approval.</h3><p>A creative that never passed review is one upload away from going live.</p></article>
          </div>
        </div>
      </section>

      <section class="section" id="workflow" aria-labelledby="workflow-title">
        <div class="container">
          <div class="section-heading" data-reveal><h2 class="section-title" id="workflow-title">From launch sheet to a reviewed <span class="serif-accent">launch plan.</span></h2><p class="section-lead">Import your launch sheet. Launch Control reads it as a manifest, checks every row, groups each failure with its evidence and assigns a named owner.</p></div>
          <ol class="product-flow" aria-label="What goes into Launch Control and what comes out" data-reveal><li><span>Input</span><strong>Launch sheet</strong><small>Assets, approvals, placements, URLs, names and UTM fields.</small></li><li class="flow-arrow" aria-hidden="true">→</li><li data-core><span>Launch Control</span><strong>Detect, route, decide</strong><small>Deterministic validation first. A named person decides every ambiguous case.</small></li><li class="flow-arrow" aria-hidden="true">→</li><li><span>Output</span><strong>Reviewed launch plan</strong><small>An owner, a next action and a decision receipt for every exception. You upload the reviewed plan through your normal Ads Manager process. Launch Control never needs access to your account.</small></li></ol>
          <div class="bento">
            <article class="feature-card" data-card="source" data-reveal><img class="icon" src="assets/icons/scan-line.svg" alt=""><h3>Check every launch field</h3><p>Each asset, approval, placement, destination, name and UTM stays connected to its source row.</p><div class="source-map" aria-hidden="true"><span></span><span></span><span></span></div></article>
            <article class="feature-card" data-card="route" data-reveal><img class="icon" src="assets/icons/route.svg" alt=""><h3>Route each failure to a named owner</h3><p>The issue, its evidence and the next action travel together.</p><div class="route-visual" aria-hidden="true"><span></span><b>ROUTE</b><span></span></div></article>
            <article class="feature-card" data-card="local" data-reveal><img class="icon" src="assets/icons/file-json.svg" alt=""><h3>Record the human decision</h3><p>Every review saves the decision on your device and stamps it into an exportable receipt.</p><div class="local-window" aria-hidden="true"><span></span><span></span><span></span><span></span></div></article>
            <article class="feature-card" data-card="boundary" data-reveal><img class="icon" src="assets/icons/shield-check.svg" alt=""><h3>Plans, not publishes.</h3><p>Launch Control produces a reviewed plan and an exportable receipt. It never calls Meta, never uploads assets, never touches spend.</p><div class="boundary-signal"><span>external_mutation</span><strong>false</strong></div></article>
          </div>
        </div>
      </section>

      <section class="safeguard" id="safeguards" aria-labelledby="safeguard-title">
        <div class="container"><div class="safeguard-panel" data-reveal><div class="eyebrow">Human in the loop by design</div><h2 id="safeguard-title">AI prepares the review. <span class="serif-accent">Only people approve.</span></h2><p>Launch Control can organize source context, suggest structured fixes and rerun deterministic validators. It cannot approve a field, bypass a rule or publish to Meta.</p><div class="guardrails"><div><b>Proposal</b><strong>AI suggests a structured fix with evidence from the imported launch sheet.</strong></div><div><b>Verification</b><strong>Deterministic rules block invalid approvals, placements, URLs, names and UTMs.</strong></div><div><b>Decision</b><strong>A named reviewer chooses the final action and saves the decision.</strong></div></div></div></div>
      </section>

      <section class="evidence" id="evidence" aria-labelledby="evidence-title">
        <div class="container"><div class="section-heading" data-reveal><h2 class="section-title" id="evidence-title">Proof you can inspect.</h2><p class="section-lead">Every claim on this page is checkable: versioned contracts, replayable validation runs and automated quality gates.</p></div><div class="evidence-grid"><a class="evidence-link" href="brief-evidence.html" data-reveal><img src="assets/icons/file-json.svg" alt=""><strong>Contracts</strong><span>Inspect field evidence and review state.</span></a><a class="evidence-link" href="fix-lab.html" data-reveal><img src="assets/icons/route.svg" alt=""><strong>Deterministic replay</strong><span>Re-run the same scenarios, get the same verdicts.</span></a><a class="evidence-link" href="https://github.com/mattyu-dev/creative-launch-workspace/actions" target="_blank" rel="noopener" data-reveal><img src="assets/icons/shield-check.svg" alt=""><strong>CI quality gates</strong><span>See tests, browser QA and accessibility checks.</span></a><a class="evidence-link" href="https://github.com/mattyu-dev/creative-launch-workspace/blob/main/docs/architecture/system.md" target="_blank" rel="noopener" data-reveal><img src="assets/icons/external-link.svg" alt=""><strong>Architecture</strong><span>Trace the trust boundaries end to end.</span></a></div></div>
      </section>

      <section class="closing" aria-labelledby="closing-title"><div class="container"><div class="closing-panel" data-reveal><div><div class="eyebrow">Launch with control</div><h2 id="closing-title">Review the launch sheet before it reaches Meta.</h2><p>Open the workspace to inspect the queue, decide one exception and export the receipt.</p></div><div class="closing-actions"><a class="button" data-variant="primary" href="workspace.html?guided=1">Try the live workspace <span class="button-arrow" aria-hidden="true">→</span></a><a class="button" data-variant="outline" href="https://github.com/mattyu-dev/creative-launch-workspace">View source</a></div><p class="closing-note">Running real launches? <a href="https://github.com/mattyu-dev/creative-launch-workspace/discussions/24" target="_blank" rel="noopener">Tell us what your preflight needs →</a></p></div></div></section>
    </main>
    <footer><div class="container footer-row"><span>© Launch Control</span><span class="footer-links"><a href="https://github.com/mattyu-dev/creative-launch-workspace">Source</a><a href="brief-evidence.html">Evidence</a><a href="fix-lab.html">Fix lab</a></span></div></footer>
  </div>
  <script id="demo-payload" type="application/json">__DEMO_PAYLOAD__</script>
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

      const demo=JSON.parse(document.getElementById('demo-payload').textContent);
      const tablist=document.querySelector('[role="tablist"]');
      const tabs=[...tablist.querySelectorAll('[role="tab"]')];
      const pill=tablist.querySelector('.t-tabs-pill');
      function movePill(tab,instant=false){const old=pill.style.transition;pill.style.transition=instant?'none':old;pill.style.left=`${tab.offsetLeft}px`;pill.style.width=`${tab.offsetWidth}px`;if(instant)requestAnimationFrame(()=>pill.style.transition='')}
      function activateTab(tab,focus=false){tabs.forEach((item)=>{const active=item===tab;item.setAttribute('aria-selected',String(active));item.tabIndex=active?0:-1;document.getElementById(item.getAttribute('aria-controls')).hidden=!active});movePill(tab);if(focus)tab.focus()}
      movePill(tabs[0],true);
      tabs.forEach((tab,index)=>{tab.addEventListener('click',()=>activateTab(tab));tab.addEventListener('keydown',(event)=>{if(!['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;event.preventDefault();let next=index;if(event.key==='ArrowLeft')next=(index-1+tabs.length)%tabs.length;if(event.key==='ArrowRight')next=(index+1)%tabs.length;if(event.key==='Home')next=0;if(event.key==='End')next=tabs.length-1;activateTab(tabs[next],true)})});
      new ResizeObserver(()=>movePill(tabs.find((tab)=>tab.getAttribute('aria-selected')==='true'),true)).observe(tablist);

      const landingKey=`launch-control-demo:${demo.batch_id}`;
      let decisions={};
      try{decisions=JSON.parse(localStorage.getItem(landingKey)||'{}')||{}}catch(_e){decisions={}}
      const rowsBySource={};
      ['ready','needs_decision','blocked'].forEach((group)=>demo.queue[group].forEach((entry)=>{rowsBySource[entry.source_row]=entry}));
      const SHORT_LABEL={confirm:'Confirmed',return:'Returned',block:'Blocked'};
      const queueList=document.getElementById('queue-list');
      const filters=[...document.querySelectorAll('.queue-filter')];
      const receiptEmpty=document.getElementById('receipt-empty');
      const receipt=document.getElementById('receipt-card');
      const live=document.getElementById('decision-live');
      let activeFilter='needs_decision';
      let currentRow=demo.walkthrough.exception.source_row;
      let lastDecided=null;

      function remainingCount(){return demo.counts.needs_decision-Object.keys(decisions).length}
      function rowsFor(filter){if(filter==='all')return[...demo.queue.needs_decision.slice(0,2),demo.queue.ready[0],demo.queue.blocked[0]];return demo.queue[filter]||[]}
      function rowHtml(entry){
        const interactive=entry.batch_state==='needs_review';
        const decided=decisions[entry.source_row];
        const sub=entry.issue_title||'Passes offline checks';
        const ownerStrong=entry.owner||'Validator';
        const ownerSub=interactive?(decided?`${SHORT_LABEL[decided.kind]} in this session`:'Decision required'):entry.status_label;
        const status=interactive?(decided?SHORT_LABEL[decided.kind]:'Review now'):entry.status_label;
        const selected=entry.source_row===currentRow?' data-selected="true"':'';
        const tag=interactive?'button':'div';
        const attrs=interactive?` data-open-review data-source-row="${entry.source_row}" type="button"`:' data-static="true"';
        return `<${tag} class="queue-row"${selected}${attrs}><span class="row-id">${entry.creative_id}</span><span class="row-name"><strong>${entry.name}</strong><span>${sub}</span></span><span class="row-owner"><strong>${ownerStrong}</strong><span>${ownerSub}</span></span><span class="row-status">${status}</span></${tag}>`;
      }
      function renderQueue(){const list=rowsFor(activeFilter);const shown=list.slice(0,4);const more=list.length>4?`<a class="queue-more" href="workspace.html?guided=1">${list.length-4} more in the workspace <span aria-hidden="true">→</span></a>`:'';queueList.innerHTML=shown.map(rowHtml).join('')+more}
      filters.forEach((button)=>button.addEventListener('click',()=>{activeFilter=button.dataset.filter;filters.forEach((item)=>{if(item===button){item.dataset.active='true'}else{delete item.dataset.active}});renderQueue()}));

      function openReview(sourceRow){
        const entry=rowsBySource[sourceRow];
        if(!entry||entry.batch_state!=='needs_review')return;
        currentRow=entry.source_row;
        document.getElementById('review-crumb').textContent=entry.creative_id;
        document.getElementById('review-name').textContent=entry.name;
        document.getElementById('review-meta').textContent=`${entry.creative_id} / row ${entry.source_row} / ${entry.format} / feed`;
        document.getElementById('review-owner-badge').textContent=entry.owner;
        document.getElementById('preview-hook').textContent=entry.primary_text;
        document.getElementById('preview-name').textContent=entry.name;
        document.getElementById('fact-campaign').textContent=entry.facts.campaign;
        document.getElementById('fact-adset').textContent=entry.facts.adset;
        document.getElementById('fact-market').textContent=entry.facts.market;
        document.getElementById('fact-post-mode').textContent=entry.facts.post_mode;
        document.getElementById('fact-post-id').textContent=entry.facts.post_id;
        document.getElementById('fact-destination').textContent=entry.facts.destination;
        document.getElementById('decision-title').textContent=entry.issue_title;
        document.getElementById('decision-message').textContent=entry.issue_message;
        document.getElementById('decision-fix').textContent=entry.proposed_fix;
        document.getElementById('decision-owner').textContent=entry.owner;
        renderQueue();
        activateTab(tabs[1],true);
      }
      document.addEventListener('click',(event)=>{const trigger=event.target.closest('[data-open-review]');if(trigger)openReview(Number(trigger.dataset.sourceRow))});

      function buildWorkspaceState(){
        const rows={};
        const audit=[];
        Object.keys(decisions).forEach((sourceRow)=>{
          const entry=rowsBySource[sourceRow];
          const meta=demo.decisions[decisions[sourceRow].kind];
          const at=decisions[sourceRow].updated_at;
          rows[sourceRow]={review_status:meta.review_status,decision:meta.decision,note:'',updated_by_role:entry.owner,updated_at:at};
          audit.unshift({event_id:`evt_local_${Date.parse(at)}_${sourceRow}`,event_type:'row_decision_updated',actor_role:entry.owner,source_row:Number(sourceRow),creative_id:entry.creative_id,decision:meta.decision,occurred_at:at});
        });
        return {product:'Launch Control',mode:'local_review_state_only',contract_version:demo.workspace_contract_version,batch_id:demo.batch_id,source_manifest:demo.source_manifest,source_manifest_sha256:demo.source_manifest_sha256,data_classification:demo.data_classification,mutation_allowed:false,meta_api_compatibility:'not_claimed',external_mutation:false,rows,audit};
      }
      function syncWorkspaceState(){localStorage.setItem(demo.workspace_storage_key,JSON.stringify(buildWorkspaceState(),null,2))}

      const RECEIPT_SUBS={
        confirm:(entry)=>`${entry.creative_id} is ready for dry-run export, the plan file you download instead of publishing.`,
        return:(entry)=>`${entry.creative_id} goes back to its owner for a replacement asset.`,
        block:(entry)=>`${entry.creative_id} stays out of the dry-run export.`
      };
      function renderReceipt(entry,kind,fromDecision){
        const meta=demo.decisions[kind];
        document.getElementById('receipt-title').textContent=meta.receipt_title;
        document.getElementById('receipt-sub').textContent=RECEIPT_SUBS[kind](entry);
        document.getElementById('timeline-issue').textContent=`${entry.issue_title} flagged`;
        document.getElementById('timeline-decision').textContent=meta.timeline;
        document.getElementById('timeline-owner').textContent=entry.owner;
        document.getElementById('receipt-state').textContent=meta.review_status;
        document.getElementById('receipt-creative').textContent=entry.creative_id;
        document.getElementById('receipt-source').textContent=`row_${String(entry.source_row).padStart(3,'0')}`;
        document.getElementById('receipt-reviewer').textContent=entry.owner;
        const remaining=remainingCount();
        document.getElementById('decision-count').textContent=`${remaining} decisions remaining`;
        const bridge=document.getElementById('receipt-bridge');
        bridge.innerHTML=remaining>0?`Decide the ${remaining} remaining in the workspace <span class="button-arrow" aria-hidden="true">→</span>`:'Open the workspace <span class="button-arrow" aria-hidden="true">→</span>';
        receiptEmpty.hidden=true;
        receipt.hidden=false;
        receipt.dataset.live=fromDecision?'true':'false';
      }
      function decide(kind){
        const entry=rowsBySource[currentRow];
        if(!entry)return;
        decisions[entry.source_row]={kind,updated_at:new Date().toISOString()};
        localStorage.setItem(landingKey,JSON.stringify(decisions));
        syncWorkspaceState();
        lastDecided={sourceRow:entry.source_row,kind};
        renderReceipt(entry,kind,true);
        live.textContent=`Decision saved locally. ${remainingCount()} decisions remaining.`;
        renderQueue();
        activateTab(tabs[2],true);
      }
      document.getElementById('confirm-decision').addEventListener('click',()=>decide('confirm'));
      document.getElementById('return-decision').addEventListener('click',()=>decide('return'));
      document.getElementById('block-decision').addEventListener('click',()=>decide('block'));
      document.getElementById('export-review').addEventListener('click',()=>{const link=document.createElement('a');link.href=URL.createObjectURL(new Blob([JSON.stringify(buildWorkspaceState(),null,2)],{type:'application/json'}));link.download='review_state.json';link.click();setTimeout(()=>URL.revokeObjectURL(link.href),0)});

      renderQueue();
      const savedRows=Object.keys(decisions);
      if(savedRows.length){const sourceRow=Number(savedRows[savedRows.length-1]);lastDecided={sourceRow,kind:decisions[sourceRow].kind};renderReceipt(rowsBySource[sourceRow],decisions[sourceRow].kind,false)}

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
""".replace("__PRODUCT_SHELL__", _product_shell(payload).strip())
        .replace("__DEMO_PAYLOAD__", json.dumps(payload, sort_keys=True, separators=(",", ":")).replace("</", "<\\/"))
        .replace("__FALLBACK_STRONG__", f"{exception['creative_id']} · {exception['issue_title']}")
        .replace(
            "__FALLBACK_SPAN__",
            f"The issue is routed to {exception['owner']}, then recorded with a receipt after review.",
        )
        .replace("__COUNT_TOTAL__", str(counts["total"]))
        .replace("__COUNT_READY__", str(counts["ready"]))
        .replace("__COUNT_NEEDS__", str(counts["needs_decision"]))
        .replace("__COUNT_BLOCKED__", str(counts["blocked"]))
    )


def render_social_card_page_v30() -> str:
    return r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=1200, initial-scale=1"><style>
@font-face{font-family:"Inter";src:url("assets/inter-latin-variable.woff2") format("woff2-variations");font-weight:100 900;font-display:swap}@font-face{font-family:"Instrument Serif";src:url("assets/instrument-serif-latin-italic.woff2") format("woff2");font-style:italic;font-weight:400;font-display:swap}*{box-sizing:border-box}html,body{width:1200px;height:630px;margin:0;overflow:hidden}body{padding:18px;color:#232427;background:#ECEDEE;font-family:"Inter",sans-serif}main{width:1164px;height:594px;position:relative;overflow:hidden;display:grid;grid-template-columns:535px 629px;border:1px solid rgba(255,255,255,.75);border-radius:40px;background:#F4F5F5;box-shadow:0 1px 0 rgba(255,255,255,.9) inset}.copy{z-index:2;display:flex;flex-direction:column;padding:43px 18px 40px 48px}.brand{display:flex;align-items:center;gap:11px}.mark{width:31px;height:31px;position:relative}.mark:before,.mark:after{content:"";position:absolute;top:6px;width:19px;height:19px;border-radius:50%}.mark:before{left:0;background:#171719}.mark:after{left:12px;background:#E34A32}.brand-copy{display:grid;line-height:1}.brand-copy strong{font-size:15px}.brand-copy span{margin-top:6px;color:#7B7D82;font-size:10px}.hero{margin-top:65px}.eyebrow{color:#E34A32;font-size:11px;font-weight:700;letter-spacing:.07em;text-transform:uppercase}.hero h1{max-width:500px;margin:15px 0 0;font-size:56px;font-weight:620;line-height:.94;letter-spacing:-.05em}.hero p{max-width:455px;margin:20px 0 0;color:#55575C;font-size:15px;line-height:1.5}.copy footer{display:flex;justify-content:space-between;margin-top:auto;color:#7B7D82;font-size:10px}.visual{position:relative}.trace{position:absolute;left:18px;right:50px;top:92px;height:112px;padding:18px 22px;border:1px solid rgba(23,23,25,.08);border-radius:18px;background:rgba(255,255,255,.82);box-shadow:0 22px 50px -36px rgba(35,36,39,.65)}.trace-line{height:2px;position:absolute;left:54px;right:54px;top:54px;background:linear-gradient(90deg,rgba(227,74,50,.2),#E34A32,rgba(227,74,50,.2))}.trace-node{width:34px;height:34px;position:absolute;top:38px;display:grid;place-items:center;border:2px solid #E34A32;border-radius:50%;color:#E34A32;background:#FFF9F7;font-size:9px;font-weight:760}.trace-node:nth-child(2){left:38px}.trace-node:nth-child(3){left:50%;transform:translateX(-50%)}.trace-node:nth-child(4){right:38px}.trace-labels{display:flex;justify-content:space-between;margin-top:52px;color:#55575C;font-size:8px;font-weight:650;text-transform:uppercase}.app{position:absolute;left:-12px;right:30px;bottom:34px;height:245px;overflow:hidden;border:8px solid rgba(255,255,255,.68);border-radius:22px;background:#FCFCFB;box-shadow:0 26px 60px -36px rgba(35,36,39,.7)}.bar{height:34px;display:flex;align-items:center;justify-content:space-between;padding:0 13px;border-bottom:1px solid rgba(23,23,25,.09);font-size:8px;font-weight:650}.bar span:last-child{padding:3px 7px;border-radius:999px;color:#B93624;background:#FFF0EC}.tabs{display:flex;gap:5px;padding:7px 11px;border-bottom:1px solid rgba(23,23,25,.09)}.tabs b{padding:5px 12px;border-radius:7px;color:#777;font-size:8px}.tabs b:first-child{color:#232427;background:#F0F0EE}.window{display:grid;grid-template-columns:100px 1fr;height:176px}.side{padding:12px 10px;border-right:1px solid rgba(23,23,25,.09);background:#F8F8F6}.side span{display:block;height:8px;margin-bottom:8px;border-radius:5px;background:#E4E4E1}.side span:nth-child(2){background:#FFF0EC}.rows{padding:13px}.rows h2{margin:0 0 12px;font-size:15px}.row{height:32px;display:grid;grid-template-columns:55px 1fr 110px;align-items:center;border-top:1px solid rgba(23,23,25,.08);font-size:7px}.row:first-of-type{box-shadow:3px 0 0 #E34A32 inset;background:#FFF9F7}.row b{font-family:monospace}.route{position:absolute;right:50px;top:45px;color:#E34A32;font-size:9px;font-weight:720;letter-spacing:.06em}
</style></head><body><main><section class="copy"><div class="brand"><span class="mark"></span><span class="brand-copy"><strong>Launch Control</strong><span>Pre-launch QA for Meta Ads</span></span></div><div class="hero"><div class="eyebrow">Detect / Route / Prove</div><h1>Catch creative launch mistakes before Ads Manager.</h1><p>Validate every creative row. Route exceptions to the right owner. Keep ambiguous decisions human.</p></div><footer><strong>Interactive product</strong><span>Pre-launch QA for Meta Ads</span></footer></section><section class="visual"><span class="route">RECORDED DECISION TRACE</span><div class="trace"><div class="trace-line"></div><b class="trace-node">01</b><b class="trace-node">02</b><b class="trace-node">✓</b><div class="trace-labels"><span>Detect</span><span>Route</span><span>Prove</span></div></div><div class="app"><div class="bar"><span>Launch Control</span><span>Demo data · local only</span></div><div class="tabs"><b>Queue</b><b>Review</b><b>Receipt</b></div><div class="window"><div class="side"><span></span><span></span><span></span><span></span></div><div class="rows"><h2>10 creatives need a decision</h2><div class="row"><b>cr_007</b><span>Possible duplicate</span><span>Creative Ops Manager</span></div><div class="row"><b>cr_017</b><span>Possible duplicate</span><span>Creative Ops Manager</span></div><div class="row"><b>cr_027</b><span>Possible duplicate</span><span>Creative Ops Manager</span></div></div></div></div></section></main></body></html>"""
