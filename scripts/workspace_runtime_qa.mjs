#!/usr/bin/env node

import { execFile, execFileSync } from "node:child_process";
import { createReadStream, existsSync, realpathSync } from "node:fs";
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
  ".webp": "image/webp",
  ".avif": "image/avif"
};

const server = createServer((request, response) => {
  const rawPath = decodeURIComponent(new URL(request.url || "/", "http://127.0.0.1").pathname);
  if (rawPath === "/favicon.ico") {
    response.writeHead(204).end();
    return;
  }
  const requested = normalize(join(root, rawPath));
  if (relative(root, requested).startsWith("..") || !existsSync(requested)) {
    response.writeHead(404).end("Not found");
    return;
  }
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
  || guidedStepThree.returnLabel !== "Return to the case study"
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
) {
  throw new Error(`Guided review contract failed: ${JSON.stringify({ guidedStepOne, guidedStepTwo, guidedStepThree, guidedRequestViolations, guidedExit, guidedPersistence, guidedMobile })}`);
}

await page.setViewport({ width: 390, height: 844 });
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
await page.screenshot({ path: join(assetsDir, "workspace-mobile.png") });

await page.setViewport({ width: 1440, height: 1000 });
await page.goto(url, { waitUntil: "load" });
await page.screenshot({ path: join(assetsDir, "workspace-desktop.png") });

const portfolioUrl = `${baseUrl}/docs/index.html`;
await page.setViewport({ width: 1366, height: 768 });
await page.goto(portfolioUrl, { waitUntil: "load" });
const portfolioPage = await page.evaluate(() => ({
  title: document.querySelector("h1")?.textContent,
  canonical: document.querySelector('link[rel="canonical"]')?.href,
  ogImage: document.querySelector('meta[property="og:image"]')?.content,
  hasWorkspaceCta: Boolean(document.querySelector('a[href="workspace.html?guided=1"]')),
  hasLabCta: Boolean(document.querySelector('a[href="fix-lab.html"]')),
  hasBusinessCase: document.body.textContent.includes("One launch review is split across too many tools")
    && document.body.textContent.includes("Without the workspace")
    && document.body.textContent.includes("With the workspace"),
  hasSpreadsheetCase: document.body.textContent.includes("Why not another launch spreadsheet?"),
  hasDemoBoundary: document.body.textContent.includes("The demo begins after governed brief intake."),
  copyFreeze: {
    mutationBoundary: document.body.textContent.includes("live platform mutations. The demo cannot publish or change spend."),
    reviewState: document.body.textContent.includes("One decision queue holds the review state."),
    boundedAuthority: document.body.textContent.includes("No stage can make the next decision on its own."),
    heroSecondaryCta: document.querySelector(".hero-cta .text-link")?.textContent.trim(),
    experienceSince: document.body.textContent.includes("since 2017"),
    structuredJobTitle: JSON.parse(document.querySelector('script[type="application/ld+json"]')?.textContent || "{}")["@graph"]?.find((item) => item["@type"] === "Person")?.jobTitle
  },
  humanizedCopy: {
    noLongDash: !/[—–]/.test(`${document.title}\n${document.body.innerText}`),
    concreteHero: document.body.textContent.includes("leaves ambiguous cases for a person to decide"),
    concreteProblem: document.body.textContent.includes("reviewing large campaign batches"),
    plainAiBoundary: document.body.textContent.includes("Rules check each AI proposal before a person decides."),
    concreteProductionBoundary: document.body.textContent.includes("Before this could touch a production ad account"),
    personalContribution: document.body.textContent.includes("I built the workflow, interface, Python contracts"),
    oldSlogansRemoved: ![
      "Rows are easy. Governed decisions are harder.",
      "Inspect the evidence, not the promise.",
      "A reference implementation with a serious next-proof plan.",
      "AI proposes. Rules verify. A human decides.",
      "Launch risk accumulates in the handoff.",
      "Exercise human authority."
    ].some((copy) => document.body.textContent.includes(copy))
  },
  aiProofCount: document.querySelectorAll(".ai-proof").length,
  hasAcceptedProposal: document.body.textContent.includes("Accepted by reviewer")
    && document.body.textContent.includes("Proposed objective")
    && document.body.textContent.includes("traffic"),
  hasAbstentionProof: document.body.textContent.includes("Not found in source")
    && document.body.textContent.includes("Human input before materialization"),
  hasBoundaries: document.body.textContent.includes("What this does not prove")
    && document.body.textContent.includes("Production Meta API compatibility")
    && document.body.textContent.includes("Measured operator or business impact"),
  hasProductionPath: document.body.textContent.includes("What I would validate next")
    && document.body.textContent.includes("Proposed production pilot metrics"),
  hasContact: Boolean(document.querySelector('a[href="https://www.linkedin.com/in/mathieu-petroni/"]')),
  structuredTypes: JSON.parse(document.querySelector('script[type="application/ld+json"]')?.textContent || "{}")["@graph"]?.map((item) => item["@type"]) || [],
  proofPathCount: document.querySelectorAll(".proof-path").length,
  ownership: document.body.textContent.includes("I build AI workflows for teams that need to see and control each decision"),
  heroProductVisible: document.querySelector(".product-window")?.getBoundingClientRect().top < innerHeight,
  heroProductTop: Math.round(document.querySelector(".product-window")?.getBoundingClientRect().top || 0),
  heroImageLoaded: document.querySelector(".product-window img")?.naturalWidth > 0,
  heroImageSource: document.querySelector(".product-window img")?.currentSrc,
  differenceCount: document.querySelectorAll(".difference").length,
  metricGroupCount: document.querySelectorAll(".metric-group").length,
  sectionNavTargetsResolve: [...document.querySelectorAll(".section-links a")].every((link) => document.querySelector(link.getAttribute("href"))),
  architectureDiagramVisible: getComputedStyle(document.querySelector(".diagram")).display !== "none",
  architectureStackHidden: getComputedStyle(document.querySelector(".architecture-stack")).display === "none",
  noDocumentOverflow: document.documentElement.scrollWidth <= innerWidth
}));
if (
  !portfolioPage.title?.includes("Catch creative launch errors")
  || !portfolioPage.canonical?.endsWith("/creative-launch-workspace/")
  || !portfolioPage.ogImage?.endsWith("/assets/social-card-v1-6.png")
  || !portfolioPage.hasWorkspaceCta
  || !portfolioPage.hasLabCta
  || !portfolioPage.hasBusinessCase
  || !portfolioPage.hasSpreadsheetCase
  || !portfolioPage.hasDemoBoundary
  || !portfolioPage.copyFreeze.mutationBoundary
  || !portfolioPage.copyFreeze.reviewState
  || !portfolioPage.copyFreeze.boundedAuthority
  || portfolioPage.copyFreeze.heroSecondaryCta !== "See how the system works →"
  || !portfolioPage.copyFreeze.experienceSince
  || portfolioPage.copyFreeze.structuredJobTitle !== "AI Automation Lead"
  || !Object.values(portfolioPage.humanizedCopy).every(Boolean)
  || portfolioPage.aiProofCount !== 2
  || !portfolioPage.hasAcceptedProposal
  || !portfolioPage.hasAbstentionProof
  || !portfolioPage.hasBoundaries
  || !portfolioPage.hasProductionPath
  || !portfolioPage.hasContact
  || !["Person", "SoftwareSourceCode", "CreativeWork"].every((item) => portfolioPage.structuredTypes.includes(item))
  || portfolioPage.proofPathCount !== 3
  || !portfolioPage.ownership
  || !portfolioPage.heroProductVisible
  || !portfolioPage.heroImageLoaded
  || portfolioPage.differenceCount !== 3
  || portfolioPage.metricGroupCount !== 3
  || !portfolioPage.sectionNavTargetsResolve
  || !portfolioPage.architectureDiagramVisible
  || !portfolioPage.architectureStackHidden
  || !portfolioPage.noDocumentOverflow
) {
  throw new Error(`Portfolio entry contract failed: ${JSON.stringify(portfolioPage)}`);
}
await page.screenshot({ path: join(assetsDir, "portfolio-desktop.png"), fullPage: true });

await page.setViewport({ width: 390, height: 844 });
await page.goto(portfolioUrl, { waitUntil: "load" });
const portfolioMobile = await page.evaluate(async () => {
  const heroImage = document.querySelector(".product-window img");
  const heroAsset = await createImageBitmap(await (await fetch(heroImage.currentSrc)).blob());
  const result = {
    noDocumentOverflow: document.documentElement.scrollWidth <= innerWidth,
    headingVisible: document.querySelector("h1")?.getBoundingClientRect().top < innerHeight,
    compactAuthorCount: document.querySelectorAll(".hero-mobile-author").length,
    authorBlockCount: document.querySelectorAll(".hero-byline").length,
    authorBlockDisplayed: getComputedStyle(document.querySelector(".hero-byline")).display !== "none",
    authorAfterProduct: Boolean(document.querySelector(".hero-product")?.compareDocumentPosition(document.querySelector(".hero-byline")) & Node.DOCUMENT_POSITION_FOLLOWING),
    ctaAfterProduct: Boolean(document.querySelector(".hero-product")?.compareDocumentPosition(document.querySelector(".hero-cta")) & Node.DOCUMENT_POSITION_FOLLOWING),
    productVisible: document.querySelector(".product-window")?.getBoundingClientRect().top < innerHeight,
    productTop: Math.round(document.querySelector(".product-window")?.getBoundingClientRect().top || 0),
    productVisibleHeight: Math.round(Math.max(0, Math.min(innerHeight, document.querySelector(".product-window")?.getBoundingClientRect().bottom || 0) - Math.max(0, document.querySelector(".product-window")?.getBoundingClientRect().top || 0))),
    heroImageSource: heroImage.currentSrc,
    heroAssetWidth: heroAsset.width,
    heroAssetHeight: heroAsset.height,
    visibleAnnotations: [...document.querySelectorAll(".annotation")].filter((item) => getComputedStyle(item).display !== "none").length,
    architectureDiagramHidden: getComputedStyle(document.querySelector(".diagram")).display === "none",
    architectureStackVisible: getComputedStyle(document.querySelector(".architecture-stack")).display !== "none",
    architectureStepCount: document.querySelectorAll(".architecture-stack li").length,
    architectureMinFontPx: Math.min(...[...document.querySelectorAll(".architecture-stack strong, .architecture-stack span")].map((item) => parseFloat(getComputedStyle(item).fontSize)))
  };
  heroAsset.close();
  return result;
});
if (
  !portfolioMobile.noDocumentOverflow
  || !portfolioMobile.headingVisible
  || portfolioMobile.compactAuthorCount !== 0
  || portfolioMobile.authorBlockCount !== 1
  || !portfolioMobile.authorBlockDisplayed
  || !portfolioMobile.authorAfterProduct
  || !portfolioMobile.ctaAfterProduct
  || !portfolioMobile.productVisible
  || portfolioMobile.productVisibleHeight < 270
  || !portfolioMobile.heroImageSource?.endsWith("/assets/workspace-mobile-hero.webp")
  || portfolioMobile.heroAssetWidth !== 390
  || portfolioMobile.heroAssetHeight !== 360
  || portfolioMobile.visibleAnnotations !== 0
  || !portfolioMobile.architectureDiagramHidden
  || !portfolioMobile.architectureStackVisible
  || portfolioMobile.architectureStepCount !== 7
  || portfolioMobile.architectureMinFontPx < 12
) {
  throw new Error(`Portfolio mobile contract failed: ${JSON.stringify(portfolioMobile)}`);
}
await page.screenshot({ path: join(assetsDir, "portfolio-mobile.png"), fullPage: true });

const portfolioWorkspaceUrl = `${baseUrl}/docs/workspace.html`;
await page.goto(portfolioWorkspaceUrl, { waitUntil: "load" });
await page.evaluate(() => localStorage.clear());
const portfolioNavigation = await page.evaluate(() => ({
  brandHref: document.querySelector(".brand")?.getAttribute("href"),
  returnHref: document.querySelector("#guided-return")?.getAttribute("href")
}));
await Promise.all([
  page.waitForNavigation({ waitUntil: "load" }),
  page.click(".brand")
]);
portfolioNavigation.brandDestination = new URL(page.url()).pathname;
await page.goto(`${portfolioWorkspaceUrl}?guided=1`, { waitUntil: "load" });
await page.evaluate(() => localStorage.clear());
await page.reload({ waitUntil: "load" });
await page.click("#guided-next");
await page.click("#guided-confirm");
await Promise.all([
  page.waitForNavigation({ waitUntil: "load" }),
  page.click("#guided-return")
]);
portfolioNavigation.completionDestination = new URL(page.url()).pathname;
if (
  portfolioNavigation.brandHref !== "index.html"
  || portfolioNavigation.returnHref !== "index.html"
  || !portfolioNavigation.brandDestination.endsWith("/docs/index.html")
  || !portfolioNavigation.completionDestination.endsWith("/docs/index.html")
) {
  throw new Error(`Portfolio navigation contract failed: ${JSON.stringify(portfolioNavigation)}`);
}
await page.setViewport({ width: 390, height: 844 });
await page.goto(portfolioUrl, { waitUntil: "load" });

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
    ["assets/workspace-mobile.png", "assets/workspace-mobile.avif"],
    ["assets/workspace-mobile.png", "assets/workspace-mobile.webp"],
    ["assets/workspace-mobile-hero.png", "assets/workspace-mobile-hero.webp"]
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
await page.screenshot({ path: join(assetsDir, "social-card-v1-6.png"), clip: { x: 0, y: 0, width: 1200, height: 630 } });

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
  { surface: "portfolio", formFactor: "desktop", targetUrl: portfolioUrl, outputPath: join(evidenceDir, "portfolio-lighthouse-accessibility-desktop.json") },
  { surface: "portfolio", formFactor: "mobile", targetUrl: portfolioUrl, outputPath: join(evidenceDir, "portfolio-lighthouse-accessibility-mobile.json") }
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

const accessibility = { workspace: {}, portfolio: {} };
for (const { surface, formFactor, outputPath } of lighthouseTargets) {
  const lighthouseReport = JSON.parse(await readFile(outputPath, "utf8"));
  accessibility[surface][`${formFactor}Score`] = lighthouseReport.categories.accessibility.score;
}
if (Object.values(accessibility).some((surface) => Object.values(surface).some((score) => score !== 1))) {
  throw new Error(`Lighthouse accessibility score regressed: ${JSON.stringify(accessibility)}`);
}

const portfolioQualityTargets = [
  { formFactor: "desktop", outputPath: join(evidenceDir, "portfolio-lighthouse-quality-desktop.json") },
  { formFactor: "mobile", outputPath: join(evidenceDir, "portfolio-lighthouse-quality-mobile.json") }
];
for (const { formFactor, outputPath } of portfolioQualityTargets) {
  const args = [
    portfolioUrl,
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

const portfolioQuality = {};
for (const { formFactor, outputPath } of portfolioQualityTargets) {
  const lighthouseReport = JSON.parse(await readFile(outputPath, "utf8"));
  portfolioQuality[formFactor] = {
    performanceScore: lighthouseReport.categories.performance.score,
    bestPracticesScore: lighthouseReport.categories["best-practices"].score,
    seoScore: lighthouseReport.categories.seo.score,
    lcpMs: Math.round(lighthouseReport.audits["largest-contentful-paint"].numericValue),
    cls: lighthouseReport.audits["cumulative-layout-shift"].numericValue,
    tbtMs: Math.round(lighthouseReport.audits["total-blocking-time"].numericValue)
  };
}
if (Object.values(portfolioQuality).some((result) =>
  result.performanceScore < 0.9
  || result.bestPracticesScore < 0.95
  || result.seoScore < 0.95
  || result.lcpMs > 2500
  || result.cls > 0.1
  || result.tbtMs > 200
)) {
  throw new Error(`Portfolio Lighthouse quality budget regressed: ${JSON.stringify(portfolioQuality)}`);
}

if (consoleErrors.length) {
  throw new Error(`Browser console must stay clean: ${JSON.stringify(consoleErrors)}`);
}

const report = {
  contract_version: "workspace_runtime_qa.v8",
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
    mobile: guidedMobile
  },
  mobile_drawer: { opened: drawerOpened, closed: drawerClosed },
  mobile_hero_capture: mobileHeroCapture,
  keyboard,
  bulk: { dialog: bulkDialog, cancelled: bulkCancelled, confirmed: bulkConfirmed, undone: bulkUndone },
  empty_filter: emptyFilter,
  filter_reconciliation: filterReconciliation,
  persistence,
  reset,
  portfolio_page: portfolioPage,
  portfolio_mobile: portfolioMobile,
  portfolio_navigation: portfolioNavigation,
  responsive_asset_fidelity: responsiveAssetFidelity,
  social_card: socialCard,
  fix_lab: { initial: labInitial, fixed: labFixed, reset: labReset },
  evidence_page: evidencePage,
  console_errors: consoleErrors,
  lighthouse_accessibility: accessibility,
  lighthouse_portfolio_quality: portfolioQuality,
  mutation_allowed: false,
  meta_api_compatibility: "not_claimed"
};
await writeFile(join(evidenceDir, "workspace-runtime-qa.json"), `${JSON.stringify(report, null, 2)}\n`);

await new Promise((resolve, reject) => {
  server.close((error) => (error ? reject(error) : resolve()));
});
console.log(JSON.stringify({ status: "pass", accessibility, portfolioQuality, viewports: viewports.length }, null, 2));
