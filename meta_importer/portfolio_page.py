from __future__ import annotations

from meta_importer.portfolio_v19 import (
    render_case_study_page_v19,
    render_portfolio_page_v19,
    render_social_card_page_v19,
)


def render_portfolio_page() -> str:
    return render_portfolio_page_v19()


def render_case_study_page() -> str:
    return render_case_study_page_v19()


def render_social_card_page() -> str:
    return render_social_card_page_v19()


def render_robots_txt() -> str:
    return """User-agent: *
Allow: /

Sitemap: https://mattyu-dev.github.io/creative-launch-workspace/sitemap.xml
"""


def render_sitemap() -> str:
    return """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://mattyu-dev.github.io/creative-launch-workspace/</loc></url>
  <url><loc>https://mattyu-dev.github.io/creative-launch-workspace/case-study.html</loc></url>
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
  <meta name="color-scheme" content="dark">
  <meta name="theme-color" content="#090c0b">
  <meta name="robots" content="noindex">
  <meta name="author" content="Mathieu Petroni">
  <link rel="icon" href="https://mattyu-dev.github.io/creative-launch-workspace/assets/favicon.svg" type="image/svg+xml">
  <title>Page not found · Mathieu Petroni</title>
  <style>
    :root{color-scheme:dark;--background:#090c0b;--foreground:#f2f7f4;--card:#101513;--secondary:#c6d0cb;--muted:#8e9b95;--primary:#7bd9b0;--primary-foreground:#07120d;--border:#35443e;--ring:#9be8c6}*{box-sizing:border-box}body{min-height:100vh;display:grid;place-items:center;margin:0;padding:24px;color:var(--foreground);background:var(--background);font:400 16px/1.6 Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}main{width:min(720px,100%);padding:42px;border:1px solid var(--border);border-radius:16px;background:var(--card)}.eyebrow{color:var(--primary);font:500 12px/1.4 ui-monospace,"SF Mono",Menlo,monospace;letter-spacing:.05em;text-transform:uppercase}h1{margin:14px 0 16px;font-size:clamp(42px,8vw,68px);font-weight:600;line-height:1;letter-spacing:-.05em}p{max-width:600px;color:var(--secondary)}.links{display:flex;flex-wrap:wrap;gap:10px 18px;margin-top:26px}a{min-height:44px;display:inline-flex;align-items:center;color:var(--secondary);font-weight:600;text-underline-offset:4px}a:first-child{padding:9px 14px;border-radius:8px;color:var(--primary-foreground);background:var(--primary);text-decoration:none}a:focus-visible{outline:2px solid var(--ring);outline-offset:4px}@media(max-width:520px){main{padding:30px 20px}.links{align-items:stretch;flex-direction:column}.links a{width:100%}}
  </style>
</head>
<body><main><div class="eyebrow">404 · Creative Launch Workspace</div><h1>This route does not exist.</h1><p>Return to Mathieu Petroni's portfolio, open the interactive review or inspect the source.</p><div class="links"><a href="https://mattyu-dev.github.io/creative-launch-workspace/">Back to the portfolio</a><a href="https://mattyu-dev.github.io/creative-launch-workspace/workspace.html?guided=1">Try the guided demo</a><a href="https://github.com/mattyu-dev/creative-launch-workspace">Open the source</a><a href="https://www.linkedin.com/in/mathieu-petroni/" rel="me external">Connect on LinkedIn</a></div></main></body>
</html>
"""
