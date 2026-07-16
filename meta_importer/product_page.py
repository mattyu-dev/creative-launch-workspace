from __future__ import annotations

from meta_importer.product_landing_v30 import (
    render_product_landing_v30,
    render_social_card_page_v30,
)


def render_product_page() -> str:
    return render_product_landing_v30()


def render_social_card_page() -> str:
    return render_social_card_page_v30()


def render_robots_txt() -> str:
    return """User-agent: *
Allow: /

Sitemap: https://mattyu-dev.github.io/creative-launch-workspace/sitemap.xml
"""


def render_sitemap() -> str:
    return """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://mattyu-dev.github.io/creative-launch-workspace/</loc></url>
  <url><loc>https://mattyu-dev.github.io/creative-launch-workspace/workspace.html</loc></url>
  <url><loc>https://mattyu-dev.github.io/creative-launch-workspace/brief-evidence.html</loc></url>
  <url><loc>https://mattyu-dev.github.io/creative-launch-workspace/fix-lab.html</loc></url>
</urlset>
"""


def render_not_found_page() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <meta name="theme-color" content="#ECEDEE">
  <meta name="robots" content="noindex">
  <link rel="icon" href="https://mattyu-dev.github.io/creative-launch-workspace/assets/favicon.svg" type="image/svg+xml">
  <link rel="preload" href="https://mattyu-dev.github.io/creative-launch-workspace/assets/inter-latin-variable.woff2" as="font" type="font/woff2" crossorigin>
  <title>Page not found · Launch Control</title>
  <style>
    @font-face{font-family:"Inter";src:url("https://mattyu-dev.github.io/creative-launch-workspace/assets/inter-latin-variable.woff2") format("woff2-variations");font-weight:100 900;font-display:swap}:root{color-scheme:light;--canvas:#ECEDEE;--ink:#232427;--surface:#fff;--muted:#55575C;--orange:#E34A32;--border:rgba(23,23,25,.12);--ring:#E34A32}*{box-sizing:border-box}body{min-height:100vh;display:grid;place-items:center;margin:0;padding:24px;color:var(--ink);background:var(--canvas);font:400 16px/1.5 "Inter",system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}main{width:min(720px,100%);padding:42px;border:1px solid var(--border);border-radius:28px;background:var(--surface);box-shadow:0 1px 0 rgba(255,255,255,.9) inset,0 24px 60px -44px rgba(35,36,39,.5)}.eyebrow{color:var(--orange);font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase}h1{margin:14px 0 16px;font-size:clamp(42px,8vw,68px);font-weight:620;line-height:1;letter-spacing:-.045em}p{max-width:600px;color:var(--muted)}.links{display:flex;flex-wrap:wrap;gap:10px 18px;margin-top:26px}a{min-height:44px;display:inline-flex;align-items:center;color:var(--ink);font-weight:650;text-underline-offset:4px;transition:transform 100ms cubic-bezier(.2,0,0,1),background-color 160ms ease}a:first-child{padding:9px 14px;border-radius:999px;color:#fff;background:#171719;text-decoration:none}a:first-child:hover{background:#2C2C30}a:first-child:active{transform:scale(.98)}a:focus-visible{outline:3px solid var(--ring);outline-offset:3px}@media(max-width:520px){main{padding:30px 20px}.links{align-items:stretch;flex-direction:column}.links a{width:100%}}@media(prefers-reduced-motion:reduce){a{transition:none}a:first-child:active{transform:none}}
  </style>
</head>
<body><main><div class="eyebrow">404 · Launch Control</div><h1>This route does not exist.</h1><p>Return to the product, open the workspace or inspect the source.</p><div class="links"><a href="https://mattyu-dev.github.io/creative-launch-workspace/">Back to the product</a><a href="https://mattyu-dev.github.io/creative-launch-workspace/workspace.html?guided=1">Open the workspace</a><a href="https://github.com/mattyu-dev/creative-launch-workspace">Open the source</a></div></main></body>
</html>
"""
