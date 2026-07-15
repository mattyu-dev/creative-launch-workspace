from __future__ import annotations

from meta_importer.product_landing_v22 import (
    render_product_landing_v22,
    render_social_card_page_v22,
)


def render_product_page() -> str:
    return render_product_landing_v22()


def render_social_card_page() -> str:
    return render_social_card_page_v22()


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
  <meta name="theme-color" content="#24142b">
  <meta name="robots" content="noindex">
  <meta name="author" content="Mathieu Petroni">
  <link rel="icon" href="https://mattyu-dev.github.io/creative-launch-workspace/assets/favicon.svg" type="image/svg+xml">
  <link rel="preload" href="https://mattyu-dev.github.io/creative-launch-workspace/assets/mona-sans-latin-variable.woff2" as="font" type="font/woff2" crossorigin>
  <title>Page not found · Mathieu Petroni</title>
  <style>
    @font-face{font-family:"Mona Sans";src:url("https://mattyu-dev.github.io/creative-launch-workspace/assets/mona-sans-latin-variable.woff2") format("woff2-variations");font-weight:200 900;font-display:swap}:root{color-scheme:light;--canvas:#f7f6f8;--ink:#1c1422;--plum:#24142b;--surface:#fff;--muted:#6c6570;--lemon:#ffe44d;--lemon-hover:#efd33b;--lemon-pressed:#d8bd26;--border:#d9d3dd;--ring:#d91f72}*{box-sizing:border-box}body{min-height:100vh;display:grid;place-items:center;margin:0;padding:24px;color:var(--ink);background:var(--canvas);font:400 16px/1.5 "Mona Sans",system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}main{width:min(720px,100%);padding:42px;border:1px solid var(--border);border-radius:14px;background:var(--surface)}.eyebrow{color:#a40c50;font-size:13px;font-weight:700;letter-spacing:.03em}h1{margin:14px 0 16px;font-size:clamp(42px,8vw,68px);font-weight:760;line-height:1;letter-spacing:-.035em}p{max-width:600px;color:var(--muted)}.links{display:flex;flex-wrap:wrap;gap:10px 18px;margin-top:26px}a{min-height:44px;display:inline-flex;align-items:center;color:var(--ink);font-weight:700;text-underline-offset:4px;transition:transform 130ms cubic-bezier(.23,1,.32,1),background-color 160ms ease}a:first-child{padding:9px 14px;border-radius:8px;color:var(--ink);background:var(--lemon);text-decoration:none}a:first-child:hover{background:var(--lemon-hover)}a:first-child:active{transform:scale(.97);background:var(--lemon-pressed)}a:focus-visible{outline:3px solid var(--ring);outline-offset:3px}@media(max-width:520px){main{padding:30px 20px}.links{align-items:stretch;flex-direction:column}.links a{width:100%}}@media(prefers-reduced-motion:reduce){a{transition:none}a:first-child:active{transform:none}}
  </style>
</head>
<body><main><div class="eyebrow">404 · Creative Launch Workspace</div><h1>This route does not exist.</h1><p>Return to the product, open the workspace or inspect the source.</p><div class="links"><a href="https://mattyu-dev.github.io/creative-launch-workspace/">Back to the product</a><a href="https://mattyu-dev.github.io/creative-launch-workspace/workspace.html?guided=1">Open the workspace</a><a href="https://github.com/mattyu-dev/creative-launch-workspace">Open the source</a><a href="https://www.linkedin.com/in/mathieu-petroni/" rel="me external">Contact Mathieu</a></div></main></body>
</html>
"""
