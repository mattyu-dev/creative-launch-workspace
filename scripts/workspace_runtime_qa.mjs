#!/usr/bin/env node

import { execFile, execFileSync } from "node:child_process";
import { createReadStream, existsSync, realpathSync, statSync } from "node:fs";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { createServer } from "node:http";
import { homedir } from "node:os";
import { basename, dirname, extname, join, normalize, relative } from "node:path";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";

import puppeteer from "puppeteer-core";

const root = normalize(join(dirname(fileURLToPath(import.meta.url)), ".."));
const workspace = join(root, "runs/fake_agency_creatives_v2/workspace.html");
const assetsDir = normalize(process.env.QA_ASSETS_DIR || join(root, "docs/assets"));
const evidenceDir = normalize(process.env.QA_EVIDENCE_DIR || join(root, "docs/evidence"));
const runFile = promisify(execFile);
const chromePath = [
  process.env.CODEX_HEADLESS_CHROME_PATH,
  process.env.CHROME_PATH,
  process.env.PUPPETEER_EXECUTABLE_PATH,
  join(homedir(), ".local/bin/chrome-headless-shell"),
  "/usr/bin/chrome-headless-shell",
  "/usr/bin/chromium-headless-shell",
  "/usr/bin/google-chrome",
  "/usr/bin/google-chrome-stable",
  "/usr/bin/chromium",
  "/usr/bin/chromium-browser"
]
  .filter((candidate) => candidate && existsSync(candidate))
  .map((candidate) => realpathSync(candidate))
  .find((candidate) => {
    if (candidate.includes(".app/")) return false;
    const executable = basename(candidate);
    return /^(chrome|chromium)-headless-shell$/.test(executable)
      || (process.platform !== "darwin" && /^(chrome|google-chrome(?:-stable)?|chromium(?:-browser)?)$/.test(executable));
  });

if (!chromePath) {
  throw new Error(
    "No focus-safe browser was found. macOS requires standalone chrome-headless-shell via CODEX_HEADLESS_CHROME_PATH."
  );
}

execFileSync(
  "python3",
  [
    "-m",
    "meta_importer.cli",
    "plan",
    "fixtures/fake_agency_creatives/manifest_v2.csv",
    "--out",
    "runs/fake_agency_creatives_v2/launch_plan.json",
    "--review",
    "runs/fake_agency_creatives_v2/review_packet.md",
    "--html",
    "runs/fake_agency_creatives_v2/workspace.html",
    "--html-audit",
    "runs/fake_agency_creatives_v2/workspace_audit.json",
    "--state",
    "runs/fake_agency_creatives_v2/review_state.json"
  ],
  { cwd: root, stdio: "inherit" }
);

await mkdir(assetsDir, { recursive: true });
await mkdir(evidenceDir, { recursive: true });

const mimeTypes = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".svg": "image/svg+xml",
  ".woff2": "font/woff2",
  ".webp": "image/webp",
  ".avif": "image/avif"
};

const server = createServer((request, response) => {
  const rawPath = decodeURIComponent(new URL(request.url || "/", "http://127.0.0.1").pathname);
  if (rawPath === "/favicon.ico") {
    response.writeHead(204).end();
    return;
  }
  let requested = normalize(join(root, rawPath));
  if (relative(root, requested).startsWith("..") || !existsSync(requested)) {
    response.writeHead(404).end("Not found");
    return;
  }
  if (statSync(requested).isDirectory()) requested = join(requested, "index.html");
  response.writeHead(200, { "Content-Type": mimeTypes[extname(requested)] || "application/octet-stream" });
  createReadStream(requested).pipe(response);
});

await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
const address = server.address();
const baseUrl = `http://127.0.0.1:${address.port}`;
const url = `${baseUrl}/runs/fake_agency_creatives_v2/workspace.html`;

const browser = await puppeteer.launch({ executablePath: chromePath, headless: true });
const page = await browser.newPage();
const consoleErrors = [];
const guidedRequests = [];
let recordGuidedRequests = false;
page.on("console", (message) => {
  if (["error", "warning"].includes(message.type())) consoleErrors.push(message.text());
});
page.on("pageerror", (error) => consoleErrors.push(error.message));
page.on("request", (request) => {
  if (recordGuidedRequests) guidedRequests.push({ url: request.url(), method: request.method() });
});

const viewports = [];
for (const width of [320, 375, 390, 760, 1023, 1024, 1440]) {
  await page.setViewport({ width, height: width >= 1024 ? 1000 : 844 });
  await page.goto(url, { waitUntil: "load" });
  const layout = await page.evaluate(() => ({
    innerWidth,
    scrollWidth: document.documentElement.scrollWidth,
    tableScrollWidth: document.querySelector(".table-wrap").scrollWidth,
    tableClientWidth: document.querySelector(".table-wrap").clientWidth,
    focusHeight: Math.round(document.querySelector(".focus-panel").getBoundingClientRect().height),
    firstRowTop: Math.round(document.querySelector("#review-rows tr")?.getBoundingClientRect().top || 0),
    rowMode: getComputedStyle(document.querySelector("#review-rows")).display
  }));
  viewports.push({ width, ...layout, noDocumentOverflow: layout.scrollWidth <= layout.innerWidth });
}

if (viewports.some((item) => !item.noDocumentOverflow)) {
  throw new Error("A tested viewport has document-level horizontal overflow.");
}

await page.setViewport({ width: 1280, height: 900 });
await page.goto(url, { waitUntil: "load" });
await page.evaluate(() => localStorage.clear());
recordGuidedRequests = true;
await page.goto(`${url}?guided=1`, { waitUntil: "load" });
const guidedStepOne = await page.evaluate(() => ({
  open: document.querySelector("#guided-dialog")?.open,
  progress: document.querySelector("#guided-progress")?.textContent,
  selectedRow: document.querySelector('tr[aria-selected="true"]')?.dataset?.sourceRow,
  issue: document.querySelector("#guided-issue")?.textContent,
  owner: document.querySelector("#guided-owner")?.textContent,
  fix: document.querySelector("#guided-fix")?.textContent,
  focused: document.activeElement?.id,
  decisionActionsVisible: getComputedStyle(document.querySelector("#guided-step-two")).display !== "none"
}));
await page.screenshot({ path: join(assetsDir, "guided-review-step-1.png") });
await page.click("#guided-next");
const guidedStepTwo = await page.evaluate(() => ({
  progress: document.querySelector("#guided-progress")?.textContent,
  confirmVisible: !document.querySelector("#guided-step-two")?.hidden
    && getComputedStyle(document.querySelector("#guided-step-two")).display !== "none",
  confirmLabel: document.querySelector("#guided-confirm")?.textContent
}));
await page.click("#guided-confirm");
const guidedStepThree = await page.evaluate(() => {
  const data = JSON.parse(document.querySelector("#workspace-data").textContent);
  const saved = JSON.parse(localStorage.getItem(data.local_storage_key));
  return {
    progress: document.querySelector("#guided-progress")?.textContent,
    state: document.querySelector("#guided-result-state")?.textContent,
    role: document.querySelector("#guided-result-role")?.textContent,
    event: document.querySelector("#guided-result-event")?.textContent,
    creative: document.querySelector("#guided-result-creative")?.textContent,
    occurredAt: document.querySelector("#guided-result-time")?.textContent,
    summary: document.querySelector("#guided-result-copy")?.textContent,
    brandHref: document.querySelector(".brand")?.getAttribute("href"),
    returnHref: document.querySelector("#guided-return")?.getAttribute("href"),
    returnLabel: document.querySelector("#guided-return")?.textContent.trim(),
    primaryBeforeReturn: Boolean(document.querySelector("#guided-explore")?.compareDocumentPosition(document.querySelector("#guided-return")) & Node.DOCUMENT_POSITION_FOLLOWING),
    persistedStatus: saved.rows[8]?.review_status,
    latestAudit: saved.audit[0]
  };
});
await page.screenshot({ path: join(assetsDir, "guided-review-step-3.png") });
const guidedRequestViolations = guidedRequests.filter((item) => !item.url.startsWith(baseUrl) || item.method !== "GET");
await page.click("#guided-explore");
const guidedExit = await page.evaluate(() => ({
  open: document.querySelector("#guided-dialog")?.open,
  activeFilter: document.querySelector('button[data-filter][aria-pressed="true"]')?.dataset?.filter,
  visibleRows: document.querySelectorAll("#review-rows tr[tabindex]").length,
  guidedParam: new URLSearchParams(location.search).get("guided"),
  focusedRow: document.activeElement?.dataset?.sourceRow,
  focusedId: document.activeElement?.id
}));
await page.goto(`${url}?guided=1`, { waitUntil: "load" });
const guidedPersistence = await page.evaluate(() => ({
  selectedRow: document.querySelector('tr[aria-selected="true"]')?.dataset?.sourceRow,
  progress: document.querySelector("#guided-progress")?.textContent
}));
await page.setViewport({ width: 390, height: 844 });
await page.goto(`${url}?guided=1`, { waitUntil: "load" });
const guidedMobile = await page.evaluate(() => ({
  open: document.querySelector("#guided-dialog")?.open,
  noDocumentOverflow: document.documentElement.scrollWidth <= innerWidth,
  dialogWithinViewport: document.querySelector("#guided-dialog")?.getBoundingClientRect().width <= innerWidth,
  progress: document.querySelector("#guided-progress")?.textContent
}));

await page.setViewport({ width: 320, height: 568 });
await page.goto(`${url}?guided=1`, { waitUntil: "load" });
await page.click("#guided-next");
const guidedSmallPhoneStepTwo = await page.evaluate(() => {
  const dialog = document.querySelector("#guided-dialog");
  const body = document.querySelector(".guided-body");
  const header = document.querySelector(".guided-head");
  const actions = document.querySelector("#guided-step-two");
  const caseCard = document.querySelector("#guided-case");
  const buttons = [...actions.querySelectorAll("button")];
  const dialogRect = dialog.getBoundingClientRect();
  const actionsRect = actions.getBoundingClientRect();
  const caseRect = caseCard.getBoundingClientRect();
  const headingStyle = getComputedStyle(document.querySelector("#guided-title"));
  return {
    viewport: { width: innerWidth, height: innerHeight },
    progress: document.querySelector("#guided-progress")?.textContent,
    headerPosition: getComputedStyle(header).position,
    bodyOverflowY: getComputedStyle(body).overflowY,
    bodyScrollable: body.scrollHeight > body.clientHeight,
    actionsBeforeCase: actionsRect.top < caseRect.top,
    everyDecisionVisible: buttons.every((button) => {
      const rect = button.getBoundingClientRect();
      return rect.top >= dialogRect.top && rect.bottom <= dialogRect.bottom;
    }),
    titleUsesCustomFocus: headingStyle.outlineStyle === "none"
      && (headingStyle.boxShadow !== "none" || parseFloat(headingStyle.borderLeftWidth) > 0),
    dialogHeight: Math.round(dialogRect.height),
    bodyClientHeight: body.clientHeight,
    bodyScrollHeight: body.scrollHeight
  };
});
await page.screenshot({ path: join(assetsDir, "guided-review-mobile-step-2.png") });
await page.click("#guided-confirm");
const guidedSmallPhoneStepThree = await page.evaluate(() => {
  const dialog = document.querySelector("#guided-dialog");
  const body = document.querySelector(".guided-body");
  const footer = document.querySelector("#guided-step-three-actions");
  const dialogRect = dialog.getBoundingClientRect();
  const footerRect = footer.getBoundingClientRect();
  return {
    progress: document.querySelector("#guided-progress")?.textContent,
    bodyScrollable: body.scrollHeight > body.clientHeight,
    footerVisible: !footer.hidden
      && footerRect.top >= dialogRect.top
      && footerRect.bottom <= dialogRect.bottom,
    productBuilderHref: document.querySelector("#guided-product-builder")?.getAttribute("href"),
    linkedinHref: document.querySelector("#guided-linkedin")?.getAttribute("href")
  };
});
await page.screenshot({ path: join(assetsDir, "guided-review-mobile-step-3.png") });
await page.addStyleTag({ content: `
  #guided-step-three-actions { display: none !important; }
  .skip-link { display: none !important; }
  .guided-proof { margin-top: 10px !important; }
  .guided-body { overflow: hidden !important; }
  *, *::before, *::after {
    animation: none !important;
    caret-color: transparent !important;
    transition: none !important;
  }
` });
await page.evaluate(() => new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve))));
const guidedReceiptClip = { x: 0, y: 0, width: 320, height: 568, scale: 3 };
await page.screenshot({ path: join(assetsDir, "guided-receipt-mobile.png"), clip: guidedReceiptClip });
const receiptEncoderPage = await browser.newPage();
await receiptEncoderPage.setViewport({ width: 960, height: 1704, deviceScaleFactor: 1 });
await receiptEncoderPage.setContent(
  `<style>
    * { box-sizing: border-box; }
    html, body { margin: 0; width: 960px; height: 1704px; overflow: hidden; }
    img { display: block; width: 960px; height: 1704px; }
  </style>
  <img src="${baseUrl}/docs/assets/guided-receipt-mobile.png" alt="">`,
  { waitUntil: "load" }
);
await receiptEncoderPage.screenshot({
  path: join(assetsDir, "guided-receipt-mobile.webp"),
  type: "webp",
  quality: 90,
  clip: { x: 0, y: 0, width: 960, height: 1704 }
});
await receiptEncoderPage.close();
const guidedReceiptMobile = await page.evaluate(() => ({
  hasReceipt: document.querySelector("#guided-result-state")?.textContent === "Confirmed for dry-run export",
  hasPersonalCta: document.querySelector("#guided-step-three-actions")?.getBoundingClientRect().height > 0,
  dimensions: { width: innerWidth, height: innerHeight }
}));
recordGuidedRequests = false;
await page.evaluate(() => localStorage.clear());

if (
  !guidedStepOne.open
  || guidedStepOne.progress !== "1 of 3 · Find"
  || guidedStepOne.selectedRow !== "8"
  || guidedStepOne.issue !== "Possible duplicate"
  || guidedStepOne.owner !== "Creative Ops Manager"
  || !guidedStepOne.fix?.includes("Confirm the duplicate")
  || guidedStepOne.focused !== "guided-title"
  || guidedStepOne.decisionActionsVisible
  || guidedStepTwo.progress !== "2 of 3 · Decide"
  || !guidedStepTwo.confirmVisible
  || guidedStepTwo.confirmLabel !== "Confirm reuse for dry-run export"
  || guidedStepThree.progress !== "3 of 3 · Verify"
  || guidedStepThree.state !== "Confirmed for dry-run export"
  || guidedStepThree.role !== "Creative Ops Manager"
  || !guidedStepThree.event?.includes("row_decision_updated")
  || guidedStepThree.creative !== "cr_007"
  || !guidedStepThree.occurredAt?.includes("T")
  || !guidedStepThree.summary?.includes("No external system was changed. Technical receipt: mutation_allowed:false.")
  || guidedStepThree.brandHref !== "index.html"
  || guidedStepThree.returnHref !== "index.html"
  || guidedStepThree.returnLabel !== "Back to the product"
  || !guidedStepThree.primaryBeforeReturn
  || guidedStepThree.persistedStatus !== "confirmed_ready"
  || guidedStepThree.latestAudit?.source_row !== 8
  || guidedRequestViolations.length
  || guidedExit.open
  || guidedExit.activeFilter !== "all"
  || guidedExit.visibleRows !== 100
  || guidedExit.guidedParam !== null
  || (guidedExit.focusedRow !== "8" && guidedExit.focusedId !== "review-workspace")
  || guidedPersistence.selectedRow !== "18"
  || guidedPersistence.progress !== "1 of 3 · Find"
  || !guidedMobile.open
  || !guidedMobile.noDocumentOverflow
  || !guidedMobile.dialogWithinViewport
  || guidedSmallPhoneStepTwo.progress !== "2 of 3 · Decide"
  || guidedSmallPhoneStepTwo.headerPosition !== "sticky"
  || !["auto", "scroll"].includes(guidedSmallPhoneStepTwo.bodyOverflowY)
  || !guidedSmallPhoneStepTwo.actionsBeforeCase
  || !guidedSmallPhoneStepTwo.everyDecisionVisible
  || !guidedSmallPhoneStepTwo.titleUsesCustomFocus
  || guidedSmallPhoneStepThree.progress !== "3 of 3 · Verify"
  || !guidedSmallPhoneStepThree.footerVisible
  || guidedSmallPhoneStepThree.productBuilderHref !== "index.html#about"
  || guidedSmallPhoneStepThree.linkedinHref !== "https://www.linkedin.com/in/mathieu-petroni/"
  || !guidedReceiptMobile.hasReceipt
  || guidedReceiptMobile.hasPersonalCta
) {
  throw new Error(`Guided review contract failed: ${JSON.stringify({ guidedStepOne, guidedStepTwo, guidedStepThree, guidedRequestViolations, guidedExit, guidedPersistence, guidedMobile, guidedSmallPhoneStepTwo, guidedSmallPhoneStepThree, guidedReceiptMobile })}`);
}

await page.setViewport({ width: 390, height: 844, deviceScaleFactor: 2 });
await page.goto(url, { waitUntil: "load" });
await page.click('tr[data-source-row="8"]');
await page.waitForFunction(() => {
  const shell = document.querySelector(".detail-shell");
  return shell.classList.contains("open") && getComputedStyle(shell).opacity === "1" && shell.getBoundingClientRect().top === 0;
});
const drawerOpened = await page.evaluate(() => ({
  open: document.querySelector(".detail-shell").classList.contains("open"),
  focused: document.activeElement?.id,
  inert: document.querySelector(".detail-shell").inert,
  ariaHidden: document.querySelector(".detail-shell").getAttribute("aria-hidden")
}));
await page.screenshot({ path: join(assetsDir, "workspace-mobile-detail.png") });
await page.addStyleTag({ content: `
  .detail-shell { padding: 12px 14px 18px !important; }
  .detail-heading { margin-bottom: 9px !important; padding-bottom: 9px !important; }
  .decision-card { margin-bottom: 8px !important; padding: 11px 12px !important; }
  .decision-card h2 { margin-bottom: 4px !important; }
  .issue-list { margin: 4px 0 0 !important; }
  .review-form, .detail-disclosure, .detail-shell > .status-line { display: none !important; }
  .detail-shell > .actions { margin: 0 !important; }
` });
const mobileHeroCapture = await page.evaluate(() => ({
  selectedRow: document.querySelector('tr[aria-selected="true"]')?.dataset?.sourceRow,
  creative: document.querySelector("#detail-title")?.textContent,
  issue: document.querySelector("#issue-list .issue strong")?.textContent,
  ownerVisible: document.querySelector("#issue-list")?.textContent.includes("Creative Ops Manager"),
  detailOpen: document.querySelector(".detail-shell")?.classList.contains("open"),
  actionLabels: [...document.querySelectorAll(".detail-shell > .actions button")].map((item) => item.textContent.trim()),
  actionBottom: Math.round(document.querySelector(".detail-shell > .actions")?.getBoundingClientRect().bottom || 0),
  captureWidth: innerWidth
}));
if (
  mobileHeroCapture.selectedRow !== "8"
  || mobileHeroCapture.creative !== "cr_007 · row 8"
  || !mobileHeroCapture.issue?.includes("Possible duplicate")
  || !mobileHeroCapture.ownerVisible
  || !mobileHeroCapture.detailOpen
  || !mobileHeroCapture.actionLabels.includes("Confirm reuse for dry-run export")
  || !mobileHeroCapture.actionLabels.includes("Return for fix")
  || !mobileHeroCapture.actionLabels.includes("Block from dry-run export")
  || mobileHeroCapture.actionBottom > 360
  || mobileHeroCapture.captureWidth !== 390
) {
  throw new Error(`Mobile hero composition contract failed: ${JSON.stringify(mobileHeroCapture)}`);
}
const mobileHeroClip = { x: 0, y: 0, width: 390, height: 360 };
await page.screenshot({ path: join(assetsDir, "workspace-mobile-hero.png"), clip: mobileHeroClip });
await page.screenshot({ path: join(assetsDir, "workspace-mobile-hero.webp"), type: "webp", quality: 88, clip: mobileHeroClip });
await page.setViewport({ width: 390, height: 844, deviceScaleFactor: 1 });
await page.click("#close-detail");
await page.waitForFunction(() => {
  const shell = document.querySelector(".detail-shell");
  return !shell.classList.contains("open") && getComputedStyle(shell).visibility === "hidden";
});
const drawerClosed = await page.evaluate(() => ({
  open: document.querySelector(".detail-shell").classList.contains("open"),
  focusedRow: document.activeElement?.dataset?.sourceRow,
  inert: document.querySelector(".detail-shell").inert,
  ariaHidden: document.querySelector(".detail-shell").getAttribute("aria-hidden")
}));

await page.focus('tr[data-source-row="8"]');
await page.keyboard.press("ArrowDown");
const keyboard = await page.evaluate(() => ({
  focusedRow: document.activeElement?.dataset?.sourceRow,
  selectedRow: document.querySelector('tr[aria-selected="true"]')?.dataset?.sourceRow,
  tabStopCount: document.querySelectorAll('#review-rows tr[tabindex="0"]').length
}));

await page.click('button[data-filter="all"]');
await page.click(".secondary-actions > summary");
await page.click("#bulk-ready");
const bulkDialog = await page.evaluate(() => ({
  open: document.querySelector("#confirm-panel").open,
  copy: document.querySelector("#confirm-copy").textContent,
  focused: document.activeElement?.id
}));
if (
  !bulkDialog.open
  || bulkDialog.copy !== "Confirm 40 visible rows for dry-run export? 60 blocked rows will stay unchanged. This only changes local review state."
  || bulkDialog.focused !== "confirm-action"
) {
  throw new Error(`Bulk confirmation copy failed: ${JSON.stringify(bulkDialog)}`);
}
await page.keyboard.press("Escape");
const bulkCancelled = await page.evaluate(() => ({
  open: document.querySelector("#confirm-panel").open,
  focused: document.activeElement?.id,
  status: document.querySelector("#status-line").textContent
}));

await page.click("#bulk-ready");
await page.click("#confirm-action");
const bulkConfirmed = await page.evaluate(() => ({
  progress: document.querySelector("#review-progress").textContent,
  status: document.querySelector("#status-line").textContent,
  blockedDecision: document.querySelector('tr[data-source-row="4"] td:last-child')?.textContent.trim()
}));
if (!bulkConfirmed.progress.startsWith("40 confirmed for dry-run export") || bulkConfirmed.blockedDecision !== "Return for fix") {
  throw new Error("Bulk dry-run confirmation changed a row that still has offline blockers.");
}

await page.click('tr[data-source-row="2"]');
await page.$eval("#undo-action", (element) => element.click());
const bulkUndone = await page.evaluate(() => ({
  progress: document.querySelector("#review-progress").textContent,
  status: document.querySelector("#status-line").textContent
}));
await page.click("#close-detail");

await page.click("#filter-disclosure > summary");
await page.type("#search", "no-row-can-match-this-query");
const emptyFilter = await page.evaluate(() => ({
  caption: document.querySelector("#table-caption").textContent,
  title: document.querySelector("#detail-title").textContent,
  detailFields: document.querySelector("#detail-grid").children.length,
  issueCount: document.querySelector("#issue-list").children.length,
  approveDisabled: document.querySelector("#mark-ready").disabled,
  previewHeadline: document.querySelector("#preview-headline").textContent
}));
if (
  emptyFilter.caption !== "0 creatives in this view"
  || emptyFilter.title !== "No row selected"
  || emptyFilter.detailFields !== 0
  || emptyFilter.issueCount !== 0
  || !emptyFilter.approveDisabled
  || emptyFilter.previewHeadline !== "No row selected"
) {
  throw new Error(`Empty filter contract failed: ${JSON.stringify(emptyFilter)}`);
}
await page.$eval("#search", (element) => {
  element.value = "";
  element.dispatchEvent(new Event("input", { bubbles: true }));
});
await page.click("#filter-disclosure > summary");

await page.click('button[data-filter="blocked"]');
const filterReconciliation = await page.evaluate(() => ({
  selectedRow: document.querySelector('tr[aria-selected="true"]')?.dataset?.sourceRow,
  selectedState: document.querySelector('tr[aria-selected="true"]')?.dataset?.state,
  detailTitle: document.querySelector("#detail-title").textContent,
  visibleRows: document.querySelectorAll("#review-rows tr[tabindex]").length
}));
await page.click('button[data-filter="all"]');

await page.click('tr[data-source-row="2"]');
await page.$eval("#mark-ready", (element) => element.click());
await page.reload({ waitUntil: "load" });
await page.click('button[data-filter="all"]');
const persistence = await page.evaluate(() => ({
  rowTwoDecision: document.querySelector('tr[data-source-row="2"] td:last-child')?.textContent.trim(),
  readyState: document.readyState
}));
await page.click('tr[data-source-row="2"]');
await page.$eval("#reset-state", (element) => element.click());
await page.click("#confirm-action");
const reset = await page.evaluate(() => ({
  rowTwoDecision: document.querySelector('tr[data-source-row="2"] td:last-child')?.textContent.trim(),
  status: document.querySelector("#status-line").textContent
}));
await page.click("#close-detail");
await page.evaluate(() => {
  document.documentElement.style.scrollBehavior = "auto";
});
await page.click('button[data-filter="needs_review"]');
await page.evaluate(() => window.scrollTo(0, 0));
await page.waitForFunction(() => window.scrollY === 0);
const workspaceMobileClip = { x: 0, y: 0, width: 390, height: 844, scale: 2 };
await page.screenshot({ path: join(assetsDir, "workspace-mobile.png"), clip: workspaceMobileClip });
await page.screenshot({ path: join(assetsDir, "workspace-mobile.webp"), type: "webp", quality: 90, clip: workspaceMobileClip });

await page.setViewport({ width: 1440, height: 1000 });
await page.goto(url, { waitUntil: "load" });
await page.screenshot({ path: join(assetsDir, "workspace-desktop.png") });

const productUrl = `${baseUrl}/docs/index.html`;
await page.setViewport({ width: 1366, height: 768 });
await page.goto(productUrl, { waitUntil: "load" });
const productHoverState = await page.evaluate(() => {
  const styles = [...document.querySelectorAll("style")].map((item) => item.textContent).join("\n");
  return {
    exactHoverRule: styles.includes('.button[data-variant="primary"]:hover{background:var(--primary-hover)}'),
    exactPressedRule: styles.includes('.button:active{transform:scale(.97)'),
    primary: getComputedStyle(document.documentElement).getPropertyValue("--primary").trim(),
    hover: getComputedStyle(document.documentElement).getPropertyValue("--primary-hover").trim(),
    foreground: getComputedStyle(document.documentElement).getPropertyValue("--primary-foreground").trim()
  };
});
const productPage = await page.evaluate(() => ({
  title: document.querySelector("h1")?.textContent,
  canonical: document.querySelector('link[rel="canonical"]')?.href,
  ogImage: document.querySelector('meta[property="og:image"]')?.content,
  hasWorkspaceCta: Boolean(document.querySelector('a[href="workspace.html?guided=1"]')),
  hasCaseStudyLink: Boolean(document.querySelector('a[href="case-study.html"]')),
  mainSectionCount: document.querySelectorAll("main > section").length,
  visibleWordCount: document.body.innerText.trim().split(/\s+/).length,
  scrollHeight: document.body.scrollHeight,
  copyFreeze: {
    mutationBoundary: document.body.textContent.includes("no Meta credentials and no publishing path"),
    reviewScope: document.body.textContent.includes("approval, destination, placement, UTM, format and naming issues"),
    reviewState: document.body.textContent.includes("Route each detected exception"),
    boundedAuthority: document.body.textContent.includes("AI proposes. Rules verify. People decide."),
    heroSecondaryCta: document.querySelector(".hero-copy .text-link")?.textContent.trim(),
    experienceSince: document.body.textContent.includes("since 2017"),
    structuredJobTitle: JSON.parse(document.querySelector('script[type="application/ld+json"]')?.textContent || "{}")["@graph"]?.find((item) => item["@type"] === "Person")?.jobTitle
  },
  humanizedCopy: {
    noLongDash: !/[—–]/.test(`${document.title}\n${document.body.innerText}`),
    concreteHero: document.body.textContent.includes("Catch launch blockers before Ads Manager"),
    concreteProblem: document.body.textContent.includes("Every blocker needs evidence, an owner and a decision"),
    plainAiBoundary: document.body.textContent.includes("AI proposes. Rules verify. People decide."),
    concreteProductionBoundary: document.body.textContent.includes("no Meta credentials and no publishing path"),
    productBuilder: document.body.textContent.includes("Designed by a performance marketer. Implemented end to end.")
  },
  exactTokens: Object.fromEntries([
    "--background", "--card", "--foreground", "--body", "--muted-foreground", "--border",
    "--border-strong", "--primary", "--primary-hover", "--primary-pressed", "--primary-soft"
  ].map((token) => [token, getComputedStyle(document.documentElement).getPropertyValue(token).trim()])),
  noAtmosphericEffects: !document.querySelector("style")?.textContent.includes("linear-gradient")
    && !document.querySelector("style")?.textContent.includes("body:before"),
  productFirst: !document.querySelector("main")?.innerHTML.split('id="about"')[0].includes("Mathieu")
    && !document.querySelector("main")?.innerHTML.split('id="about"')[0].includes("I built")
    && !document.querySelector("main")?.innerHTML.split('id="about"')[0].includes("Personal project")
    && !document.querySelector("main")?.innerHTML.split('id="about"')[0].toLowerCase().includes("case study")
    && !document.querySelector("main")?.innerHTML.toLowerCase().includes("portfolio")
    && !document.querySelector("main")?.innerHTML.toLowerCase().includes("hiring"),
  hasContact: Boolean(document.querySelector('a[href="https://www.linkedin.com/in/mathieu-petroni/"]')),
  structuredTypes: JSON.parse(document.querySelector('script[type="application/ld+json"]')?.textContent || "{}")["@graph"]?.map((item) => item["@type"]) || [],
  workflowStepCount: document.querySelectorAll(".workflow-layout .step-list li").length,
  controlCount: document.querySelectorAll(".system-flow li").length,
  evidenceCount: document.querySelectorAll(".sample-metrics li").length,
  proofCellCount: document.querySelectorAll(".proof-grid > .proof-cell").length,
  eyebrowCount: document.querySelectorAll(".eyebrow").length,
  aiAbsentFromHero: !document.querySelector(".hero")?.innerText.includes("AI"),
  ownership: document.body.textContent.includes("Mathieu Petroni brought growth and performance marketing experience"),
  primaryCtaVisible: document.querySelector(".hero-copy .button")?.getBoundingClientRect().top < innerHeight,
  heroProductVisible: document.querySelector(".product-window")?.getBoundingClientRect().top < innerHeight,
  heroProductTop: Math.round(document.querySelector(".product-window")?.getBoundingClientRect().top || 0),
  heroImageLoaded: document.querySelector(".product-window img")?.naturalWidth > 0,
  heroImageSource: document.querySelector(".product-window img")?.currentSrc,
  sectionNavTargetsResolve: [...document.querySelectorAll('.nav-links a[href^="#"]')].every((link) => document.querySelector(link.getAttribute("href"))),
  noDocumentOverflow: document.documentElement.scrollWidth <= innerWidth
}));
if (
  !productPage.title?.includes("Catch launch blockers before Ads Manager")
  || !productPage.canonical?.endsWith("/creative-launch-workspace/")
  || !productPage.ogImage?.endsWith("/assets/social-card-v2-1.png")
  || !productPage.hasWorkspaceCta
  || productPage.hasCaseStudyLink
  || productPage.mainSectionCount !== 6
  || productPage.visibleWordCount > 850
  || productPage.scrollHeight > 9000
  || !productPage.copyFreeze.mutationBoundary
  || !productPage.copyFreeze.reviewState
  || !productPage.copyFreeze.boundedAuthority
  || productPage.copyFreeze.heroSecondaryCta !== "See how it works"
  || !productPage.copyFreeze.experienceSince
  || productPage.copyFreeze.structuredJobTitle !== "AI Automation Builder"
  || !Object.values(productPage.humanizedCopy).every(Boolean)
  || JSON.stringify(productPage.exactTokens) !== JSON.stringify({
    "--background": "#f6f7f5",
    "--card": "#ffffff",
    "--foreground": "#151817",
    "--body": "#3e4541",
    "--muted-foreground": "#636b66",
    "--border": "#d8ddd9",
    "--border-strong": "#b8c0ba",
    "--primary": "#c83b24",
    "--primary-hover": "#ae311d",
    "--primary-pressed": "#8d2414",
    "--primary-soft": "#fbe8e2"
  })
  || !productPage.noAtmosphericEffects
  || !productPage.productFirst
  || !productPage.hasContact
  || !["Person", "SoftwareApplication", "WebSite"].every((item) => productPage.structuredTypes.includes(item))
  || productPage.workflowStepCount !== 3
  || productPage.controlCount !== 4
  || productPage.evidenceCount !== 4
  || productPage.proofCellCount !== 3
  || productPage.eyebrowCount !== 2
  || !productPage.aiAbsentFromHero
  || !productPage.ownership
  || !productPage.primaryCtaVisible
  || !productPage.heroProductVisible
  || !productPage.heroImageLoaded
  || !productPage.sectionNavTargetsResolve
  || !productPage.noDocumentOverflow
  || !productHoverState.exactHoverRule
  || !productHoverState.exactPressedRule
  || productHoverState.primary !== "#c83b24"
  || productHoverState.hover !== "#ae311d"
  || productHoverState.foreground !== "#ffffff"
) {
  throw new Error(`Product entry contract failed: ${JSON.stringify({ productPage, productHoverState })}`);
}
await page.evaluate(async () => {
  for (const image of document.images) {
    image.scrollIntoView({ block: "center" });
    await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  }
  await Promise.all([...document.images].map((image) => image.decode().catch(() => undefined)));
  if (document.activeElement instanceof HTMLElement) document.activeElement.blur();
  window.scrollTo(0, 0);
  await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
});
await page.addStyleTag({ content: ".skip-link{display:none!important}.site-header{position:static!important}" });
await page.screenshot({ path: join(assetsDir, "product-desktop.png"), fullPage: true });

await page.setViewport({ width: 390, height: 844 });
await page.goto(productUrl, { waitUntil: "load" });
const productMobile = await page.evaluate(async () => {
  const heroImage = document.querySelector(".product-window img");
  const heroAsset = await createImageBitmap(await (await fetch(heroImage.currentSrc)).blob());
  const heroCta = document.querySelector(".hero-copy .button");
  const heroProduct = document.querySelector(".hero-product");
  const result = {
    noDocumentOverflow: document.documentElement.scrollWidth <= innerWidth,
    documentWidth: document.documentElement.scrollWidth,
    viewportWidth: innerWidth,
    scrollY,
    overflowers: [...document.querySelectorAll("body *")]
      .filter((element) => {
        const rect = element.getBoundingClientRect();
        return getComputedStyle(element).display !== "none" && rect.width > 0
          && (rect.left < -1 || rect.right > innerWidth + 1);
      })
      .slice(0, 8)
      .map((element) => {
        const rect = element.getBoundingClientRect();
        return { selector: `${element.tagName.toLowerCase()}.${[...element.classList].join(".")}`, left: Math.round(rect.left), right: Math.round(rect.right) };
      }),
    headingVisible: document.querySelector("h1")?.getBoundingClientRect().top < innerHeight,
    primaryCtaVisible: heroCta?.getBoundingClientRect().top >= 0
      && heroCta?.getBoundingClientRect().bottom <= innerHeight,
    ctaBeforeProduct: Boolean(heroCta?.compareDocumentPosition(heroProduct) & Node.DOCUMENT_POSITION_FOLLOWING),
    productTop: Math.round(document.querySelector(".product-window")?.getBoundingClientRect().top || 0),
    heroImageSource: heroImage.currentSrc,
    heroAssetWidth: heroAsset.width,
    heroAssetHeight: heroAsset.height,
    scrollHeight: document.body.scrollHeight,
    bodyFontPx: parseFloat(getComputedStyle(document.body).fontSize),
    evidenceColumns: getComputedStyle(document.querySelector(".sample-metrics")).gridTemplateColumns.split(" ").length
  };
  heroAsset.close();
  return result;
});
if (
  !productMobile.noDocumentOverflow
  || !productMobile.headingVisible
  || !productMobile.primaryCtaVisible
  || !productMobile.ctaBeforeProduct
  || !productMobile.heroImageSource?.endsWith("/assets/workspace-mobile-hero.webp")
  || productMobile.heroAssetWidth !== 780
  || productMobile.heroAssetHeight !== 720
  || productMobile.scrollHeight > 8000
  || productMobile.bodyFontPx < 16
  || productMobile.evidenceColumns !== 2
) {
  throw new Error(`Product mobile contract failed: ${JSON.stringify(productMobile)}`);
}
await page.evaluate(async () => {
  for (const image of document.images) {
    image.scrollIntoView({ block: "center" });
    await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  }
  await Promise.all([...document.images].map((image) => image.decode().catch(() => undefined)));
  if (document.activeElement instanceof HTMLElement) document.activeElement.blur();
  window.scrollTo(0, 0);
  await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
});
await page.addStyleTag({ content: ".skip-link{display:none!important}.site-header{position:static!important}" });
await page.screenshot({ path: join(assetsDir, "product-mobile.png"), fullPage: true });

await page.setViewport({ width: 320, height: 568 });
await page.goto(productUrl, { waitUntil: "load" });
const productSmallPhone = await page.evaluate(() => {
  const primaryCta = document.querySelector(".hero-copy .button");
  const ctaRect = primaryCta?.getBoundingClientRect();
  const brandName = document.querySelector(".brand-copy strong");
  const brandNameRect = brandName?.getBoundingClientRect();
  const independentTargets = [...document.querySelectorAll(".site-nav a,.hero-copy .button,.hero-copy .text-link")]
    .filter((element) => getComputedStyle(element).display !== "none")
    .map((element) => ({
      label: element.getAttribute("aria-label") || element.textContent.trim().slice(0, 48),
      height: Math.round(element.getBoundingClientRect().height)
    }));
  return {
    noDocumentOverflow: document.documentElement.scrollWidth <= innerWidth,
    primaryCtaVisible: ctaRect?.top >= 0 && ctaRect?.bottom <= innerHeight,
    ctaBeforeProduct: Boolean(primaryCta?.compareDocumentPosition(document.querySelector(".hero-product")) & Node.DOCUMENT_POSITION_FOLLOWING),
    brandNameVisible: getComputedStyle(brandName).display !== "none"
      && brandNameRect?.top >= 0
      && brandNameRect?.bottom <= innerHeight,
    touchTargetFailures: independentTargets.filter((target) => target.height < 44),
    ctaTop: Math.round(ctaRect?.top || 0),
    ctaBottom: Math.round(ctaRect?.bottom || 0),
    headingHeight: Math.round(document.querySelector("h1")?.getBoundingClientRect().height || 0),
    productTop: Math.round(document.querySelector(".hero-product")?.getBoundingClientRect().top || 0)
  };
});
const productBrandHandle = await page.$(".brand");
const productBrandAccessibility = productBrandHandle
  ? await page.accessibility.snapshot({ root: productBrandHandle })
  : null;
productSmallPhone.brandAccessibleName = productBrandAccessibility?.name || "";
await productBrandHandle?.dispose();
const productSmallPhoneFocusOrder = [];
for (let index = 0; index < 3; index += 1) {
  await page.keyboard.press("Tab");
  productSmallPhoneFocusOrder.push(await page.evaluate(() => ({
    className: document.activeElement?.className || "",
    label: document.activeElement?.getAttribute("aria-label") || document.activeElement?.textContent.trim() || ""
  })));
}
productSmallPhone.keyboardFocusOrder = productSmallPhoneFocusOrder;
const productSmallPhoneKeyboardOrder = productSmallPhoneFocusOrder[0]?.className.includes("skip-link")
  && productSmallPhoneFocusOrder[1]?.className.includes("brand")
  && productSmallPhoneFocusOrder[2]?.label.includes("Review sample");
if (
  !productSmallPhone.noDocumentOverflow
  || !productSmallPhone.primaryCtaVisible
  || !productSmallPhone.ctaBeforeProduct
  || !productSmallPhone.brandAccessibleName?.includes("Creative Launch Workspace")
  || !productSmallPhone.brandNameVisible
  || productSmallPhone.touchTargetFailures.length
  || !productSmallPhoneKeyboardOrder
  || productSmallPhone.productTop >= 568
) {
  throw new Error(`Product small-phone contract failed: ${JSON.stringify(productSmallPhone)}`);
}

const productTextResize = [];
for (const width of [320, 768]) {
  await page.setViewport({ width, height: width === 320 ? 568 : 900 });
  await page.goto(productUrl, { waitUntil: "load" });
  const result = await page.evaluate(async () => {
    const textElements = [...document.querySelectorAll("body *")]
      .filter((element) => [...element.childNodes].some((node) => node.nodeType === Node.TEXT_NODE && node.textContent.trim()))
      .map((element) => ({ element, fontSize: parseFloat(getComputedStyle(element).fontSize) }));
    for (const { element, fontSize } of textElements) element.style.fontSize = `${fontSize * 2}px`;
    await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
    const overflowers = [...document.querySelectorAll("body *")]
      .filter((element) => {
        const style = getComputedStyle(element);
        const rect = element.getBoundingClientRect();
        return style.display !== "none"
          && style.visibility !== "hidden"
          && rect.width > 0
          && rect.bottom > 0
          && (rect.left < -1 || rect.right > innerWidth + 1);
      })
      .slice(0, 12)
      .map((element) => {
        const rect = element.getBoundingClientRect();
        return {
          selector: `${element.tagName.toLowerCase()}${element.id ? `#${element.id}` : ""}${element.classList.length ? `.${[...element.classList].join(".")}` : ""}`,
          left: Math.round(rect.left),
          right: Math.round(rect.right)
        };
      });
    return {
      documentWidth: document.documentElement.scrollWidth,
      viewportWidth: innerWidth,
      overflowers
    };
  });
  productTextResize.push({ width, ...result });
}
if (productTextResize.some((result) => result.documentWidth > result.viewportWidth || result.overflowers.length)) {
  throw new Error(`Product 200% text resize overflow: ${JSON.stringify(productTextResize)}`);
}

const removedRouteUrl = `${baseUrl}/docs/case-study.html`;
const removedRoute = {
  fileAbsent: !existsSync(join(root, "docs/case-study.html")),
  excludedFromSitemap: !(await readFile(join(root, "docs/sitemap.xml"), "utf8")).includes("case-study.html")
};
await page.setViewport({ width: 1366, height: 768 });
const removedRouteConsoleStart = consoleErrors.length;
const removedRouteResponse = await page.goto(removedRouteUrl, { waitUntil: "load" });
removedRoute.httpStatus = removedRouteResponse?.status();
removedRoute.destination = page.url();
removedRoute.consoleMessages = consoleErrors.splice(removedRouteConsoleStart);
if (
  !removedRoute.fileAbsent
  || !removedRoute.excludedFromSitemap
  || removedRoute.httpStatus !== 404
  || !removedRoute.destination.endsWith("/docs/case-study.html")
  || removedRoute.consoleMessages.some((message) => !message.includes("status of 404"))
) {
  throw new Error(`Removed route contract failed: ${JSON.stringify(removedRoute)}`);
}

const productWorkspaceUrl = `${baseUrl}/docs/workspace.html`;
await page.goto(productWorkspaceUrl, { waitUntil: "load" });
await page.evaluate(() => localStorage.clear());
const productNavigation = await page.evaluate(() => ({
  brandHref: document.querySelector(".brand")?.getAttribute("href"),
  returnHref: document.querySelector("#guided-return")?.getAttribute("href")
}));
await Promise.all([
  page.waitForNavigation({ waitUntil: "load" }),
  page.click(".brand")
]);
productNavigation.brandDestination = new URL(page.url()).pathname;
await page.goto(`${productWorkspaceUrl}?guided=1`, { waitUntil: "load" });
await page.evaluate(() => localStorage.clear());
await page.reload({ waitUntil: "load" });
await page.click("#guided-next");
await page.click("#guided-confirm");
await Promise.all([
  page.waitForNavigation({ waitUntil: "load" }),
  page.click("#guided-return")
]);
productNavigation.completionDestination = new URL(page.url()).pathname;
if (
  productNavigation.brandHref !== "index.html"
  || productNavigation.returnHref !== "index.html"
  || !productNavigation.brandDestination.endsWith("/docs/index.html")
  || !productNavigation.completionDestination.endsWith("/docs/index.html")
) {
  throw new Error(`Product navigation contract failed: ${JSON.stringify(productNavigation)}`);
}
await page.setViewport({ width: 390, height: 844 });
await page.goto(productUrl, { waitUntil: "load" });

const responsiveAssetFidelity = await page.evaluate(async () => {
  const loadImage = (src) => new Promise((resolve, reject) => {
    const item = new Image();
    item.onload = () => resolve(item);
    item.onerror = () => reject(new Error(`Unable to decode ${src}`));
    item.src = src;
  });
  const compare = async (referenceSrc, candidateSrc) => {
    const reference = await loadImage(referenceSrc);
    const candidate = await loadImage(candidateSrc);
    if (reference.naturalWidth !== candidate.naturalWidth || reference.naturalHeight !== candidate.naturalHeight) {
      return { referenceSrc, candidateSrc, dimensionsMatch: false, psnr: 0 };
    }
    const canvas = document.createElement("canvas");
    canvas.width = reference.naturalWidth;
    canvas.height = reference.naturalHeight;
    const context = canvas.getContext("2d", { willReadFrequently: true });
    context.drawImage(reference, 0, 0);
    const referencePixels = context.getImageData(0, 0, canvas.width, canvas.height).data;
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.drawImage(candidate, 0, 0);
    const candidatePixels = context.getImageData(0, 0, canvas.width, canvas.height).data;
    let squaredError = 0;
    let channelCount = 0;
    for (let index = 0; index < referencePixels.length; index += 4) {
      for (let channel = 0; channel < 3; channel += 1) {
        const delta = referencePixels[index + channel] - candidatePixels[index + channel];
        squaredError += delta * delta;
        channelCount += 1;
      }
    }
    const mse = squaredError / channelCount;
    const psnr = mse === 0 ? Infinity : 10 * Math.log10((255 * 255) / mse);
    return {
      referenceSrc,
      candidateSrc,
      dimensionsMatch: true,
      psnr: Math.round(psnr * 100) / 100
    };
  };
  const pairs = [
    ["assets/workspace-desktop.png", "assets/workspace-desktop.avif"],
    ["assets/workspace-desktop.png", "assets/workspace-desktop.webp"],
    ["assets/workspace-mobile.png", "assets/workspace-mobile.webp"],
    ["assets/workspace-mobile-hero.png", "assets/workspace-mobile-hero.webp"],
    ["assets/guided-receipt-mobile.png", "assets/guided-receipt-mobile.webp"]
  ];
  const results = [];
  for (const pair of pairs) results.push(await compare(...pair));
  return results;
});
if (responsiveAssetFidelity.some((item) => !item.dimensionsMatch || item.psnr < 35)) {
  throw new Error(`Responsive product assets are stale or too lossy: ${JSON.stringify(responsiveAssetFidelity)}`);
}

const socialCardUrl = `${baseUrl}/docs/social-card.html`;
await page.setViewport({ width: 1200, height: 630 });
await page.goto(socialCardUrl, { waitUntil: "load" });
const socialCard = await page.evaluate(() => ({
  productImage: document.querySelector(".visual img")?.getAttribute("src"),
  productLoaded: document.querySelector(".visual img")?.naturalWidth > 0,
  noDocumentOverflow: document.documentElement.scrollWidth <= innerWidth && document.documentElement.scrollHeight <= innerHeight
}));
if (socialCard.productImage !== "assets/workspace-desktop.png" || !socialCard.productLoaded || !socialCard.noDocumentOverflow) {
  throw new Error(`Social card contract failed: ${JSON.stringify(socialCard)}`);
}
await page.screenshot({ path: join(assetsDir, "social-card.png"), clip: { x: 0, y: 0, width: 1200, height: 630 } });
await page.screenshot({ path: join(assetsDir, "social-card-v2-1.png"), clip: { x: 0, y: 0, width: 1200, height: 630 } });

const labUrl = `${baseUrl}/docs/fix-lab.html`;
await page.setViewport({ width: 1280, height: 900 });
await page.goto(labUrl, { waitUntil: "load" });
const labInitial = await page.evaluate(() => ({
  state: document.querySelector("#state")?.textContent.trim(),
  issues: document.querySelectorAll("#issues .issue").length,
  rulePack: document.querySelector("#rule-pack")?.textContent.includes("fix_lab_rule_pack.v1"),
  noDocumentOverflow: document.documentElement.scrollWidth <= innerWidth
}));
await page.click("#fix-all");
const labFixed = await page.evaluate(() => ({
  state: document.querySelector("#state")?.textContent.trim(),
  issues: document.querySelectorAll("#issues .issue").length,
  clean: document.querySelector("#issues .clean")?.textContent.includes("All three blockers cleared"),
  audit: document.querySelector("#audit")?.textContent.includes('"external_write": false')
}));
await page.click("#reset");
const labReset = await page.evaluate(() => ({
  state: document.querySelector("#state")?.textContent.trim(),
  issues: document.querySelectorAll("#issues .issue").length
}));
if (
  labInitial.state !== "blocked"
  || labInitial.issues !== 3
  || !labInitial.rulePack
  || !labInitial.noDocumentOverflow
  || labFixed.state !== "launch ready"
  || labFixed.issues !== 0
  || !labFixed.clean
  || !labFixed.audit
  || labReset.state !== "blocked"
  || labReset.issues !== 3
) {
  throw new Error(`Fix lab contract failed: ${JSON.stringify({ labInitial, labFixed, labReset })}`);
}
await page.screenshot({ path: join(assetsDir, "fix-lab.png"), fullPage: true });

const evidenceUrl = `${baseUrl}/docs/brief-evidence.html`;
await page.setViewport({ width: 1440, height: 1000 });
await page.goto(evidenceUrl, { waitUntil: "load" });
const evidencePage = await page.evaluate(() => ({
  title: document.querySelector("h1")?.textContent,
  fieldRows: document.querySelectorAll("tbody tr").length,
  acceptedFields: document.querySelectorAll(".accepted").length,
  noDocumentOverflow: document.documentElement.scrollWidth <= innerWidth,
  launchReadyProof: Array.from(document.querySelectorAll(".proof strong")).at(-1)?.textContent
}));
if (
  evidencePage.fieldRows !== 8
  || evidencePage.acceptedFields !== 8
  || !evidencePage.noDocumentOverflow
  || evidencePage.launchReadyProof !== "2"
) {
  throw new Error(`Brief evidence page contract failed: ${JSON.stringify(evidencePage)}`);
}
await page.screenshot({ path: join(assetsDir, "brief-evidence.png"), fullPage: true });

await browser.close();

const lighthouseBin = join(root, "node_modules/.bin/lighthouse");
const lighthouseChromeFlags = ["--headless=new", "--disable-dev-shm-usage"];
if (process.platform === "linux") lighthouseChromeFlags.push("--no-sandbox");
const lighthouseTargets = [
  { surface: "workspace", formFactor: "desktop", targetUrl: url, outputPath: join(evidenceDir, "workspace-lighthouse-accessibility-desktop.json") },
  { surface: "workspace", formFactor: "mobile", targetUrl: url, outputPath: join(evidenceDir, "workspace-lighthouse-accessibility-mobile.json") },
  { surface: "product", formFactor: "desktop", targetUrl: productUrl, outputPath: join(evidenceDir, "product-lighthouse-accessibility-desktop.json") },
  { surface: "product", formFactor: "mobile", targetUrl: productUrl, outputPath: join(evidenceDir, "product-lighthouse-accessibility-mobile.json") }
];

for (const { formFactor, targetUrl, outputPath } of lighthouseTargets) {
  const args = [
    targetUrl,
    `--chrome-path=${chromePath}`,
    "--only-categories=accessibility",
    `--form-factor=${formFactor}`,
    "--output=json",
    `--output-path=${outputPath}`,
    "--quiet"
  ];
  if (formFactor === "desktop") args.push("--screenEmulation.disabled");
  args.push(`--chrome-flags=${lighthouseChromeFlags.join(" ")}`);
  await runFile(lighthouseBin, args, {
    cwd: root,
    env: { ...process.env, CHROME_PATH: chromePath },
    maxBuffer: 10 * 1024 * 1024
  });
}

const accessibility = { workspace: {}, product: {} };
const seriousAccessibilityFailures = [];
for (const { surface, formFactor, outputPath } of lighthouseTargets) {
  const lighthouseReport = JSON.parse(await readFile(outputPath, "utf8"));
  accessibility[surface][`${formFactor}Score`] = lighthouseReport.categories.accessibility.score;
  for (const [auditId, audit] of Object.entries(lighthouseReport.audits)) {
    const impact = audit.details?.debugData?.impact;
    const tags = audit.details?.debugData?.tags || [];
    if (
      audit.score === 0
      && ["serious", "critical"].includes(impact)
      && tags.some((tag) => String(tag).startsWith("wcag"))
    ) {
      seriousAccessibilityFailures.push({ surface, formFactor, auditId, impact, tags });
    }
  }
}
if (Object.values(accessibility).some((surface) => Object.values(surface).some((score) => score !== 1))) {
  throw new Error(`Lighthouse accessibility score regressed: ${JSON.stringify(accessibility)}`);
}
if (seriousAccessibilityFailures.length) {
  throw new Error(`Serious WCAG audit failures cannot be hidden by a rounded Lighthouse score: ${JSON.stringify(seriousAccessibilityFailures)}`);
}

const productQualityTargets = [
  { surface: "product", formFactor: "desktop", targetUrl: productUrl, outputPath: join(evidenceDir, "product-lighthouse-quality-desktop.json") },
  { surface: "product", formFactor: "mobile", targetUrl: productUrl, outputPath: join(evidenceDir, "product-lighthouse-quality-mobile.json") }
];
for (const { formFactor, targetUrl, outputPath } of productQualityTargets) {
  const args = [
    targetUrl,
    `--chrome-path=${chromePath}`,
    "--only-categories=performance,best-practices,seo",
    `--form-factor=${formFactor}`,
    "--output=json",
    `--output-path=${outputPath}`,
    "--quiet"
  ];
  if (formFactor === "desktop") args.push("--screenEmulation.disabled");
  args.push(`--chrome-flags=${lighthouseChromeFlags.join(" ")}`);
  await runFile(lighthouseBin, args, {
    cwd: root,
    env: { ...process.env, CHROME_PATH: chromePath },
    maxBuffer: 10 * 1024 * 1024
  });
}

const productQuality = {};
for (const { surface, formFactor, outputPath } of productQualityTargets) {
  const lighthouseReport = JSON.parse(await readFile(outputPath, "utf8"));
  productQuality[`${surface}_${formFactor}`] = {
    performanceScore: lighthouseReport.categories.performance.score,
    bestPracticesScore: lighthouseReport.categories["best-practices"].score,
    seoScore: lighthouseReport.categories.seo.score,
    lcpMs: Math.round(lighthouseReport.audits["largest-contentful-paint"].numericValue),
    cls: lighthouseReport.audits["cumulative-layout-shift"].numericValue,
    tbtMs: Math.round(lighthouseReport.audits["total-blocking-time"].numericValue)
  };
}
if (Object.values(productQuality).some((result) =>
  result.performanceScore < 0.9
  || result.bestPracticesScore < 0.95
  || result.seoScore < 0.95
  || result.lcpMs > 2500
  || result.cls > 0.1
  || result.tbtMs > 200
)) {
  throw new Error(`Product Lighthouse quality budget regressed: ${JSON.stringify(productQuality)}`);
}

if (consoleErrors.length) {
  throw new Error(`Browser console must stay clean: ${JSON.stringify(consoleErrors)}`);
}

const report = {
  contract_version: "workspace_runtime_qa.v18",
  tested_at: new Date().toISOString(),
  source: "scripts/workspace_runtime_qa.mjs",
  viewports,
  guided_review: {
    step_one: guidedStepOne,
    step_two: guidedStepTwo,
    step_three: guidedStepThree,
    request_violations: guidedRequestViolations,
    exit: guidedExit,
    persistence: guidedPersistence,
    mobile: guidedMobile,
    small_phone_step_two: guidedSmallPhoneStepTwo,
    small_phone_step_three: guidedSmallPhoneStepThree,
    receipt_mobile: guidedReceiptMobile
  },
  mobile_drawer: { opened: drawerOpened, closed: drawerClosed },
  mobile_hero_capture: mobileHeroCapture,
  keyboard,
  bulk: { dialog: bulkDialog, cancelled: bulkCancelled, confirmed: bulkConfirmed, undone: bulkUndone },
  empty_filter: emptyFilter,
  filter_reconciliation: filterReconciliation,
  persistence,
  reset,
  product_page: productPage,
  product_hover_state: productHoverState,
  product_mobile: productMobile,
  product_small_phone: productSmallPhone,
  product_text_resize: productTextResize,
  removed_route: removedRoute,
  product_navigation: productNavigation,
  responsive_asset_fidelity: responsiveAssetFidelity,
  social_card: socialCard,
  fix_lab: { initial: labInitial, fixed: labFixed, reset: labReset },
  evidence_page: evidencePage,
  console_errors: consoleErrors,
  lighthouse_accessibility: accessibility,
  serious_accessibility_failures: seriousAccessibilityFailures,
  lighthouse_product_quality: productQuality,
  mutation_allowed: false,
  meta_api_compatibility: "not_claimed"
};
await writeFile(join(evidenceDir, "workspace-runtime-qa.json"), `${JSON.stringify(report, null, 2)}\n`);

await new Promise((resolve, reject) => {
  server.close((error) => (error ? reject(error) : resolve()));
});
console.log(JSON.stringify({ status: "pass", accessibility, productQuality, viewports: viewports.length }, null, 2));
