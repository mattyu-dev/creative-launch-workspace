#!/usr/bin/env node

import { execFile, execFileSync } from "node:child_process";
import { createReadStream, existsSync } from "node:fs";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { createServer } from "node:http";
import { dirname, extname, join, normalize, relative } from "node:path";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";

import puppeteer from "puppeteer-core";

const root = normalize(join(dirname(fileURLToPath(import.meta.url)), ".."));
const workspace = join(root, "runs/fake_agency_creatives_v2/workspace.html");
const assetsDir = normalize(process.env.QA_ASSETS_DIR || join(root, "docs/assets"));
const evidenceDir = normalize(process.env.QA_EVIDENCE_DIR || join(root, "docs/evidence"));
const runFile = promisify(execFile);
const chromePath = [
  process.env.CHROME_PATH,
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  "/usr/bin/google-chrome",
  "/usr/bin/google-chrome-stable",
  "/usr/bin/chromium",
  "/usr/bin/chromium-browser"
].find((candidate) => candidate && existsSync(candidate));

if (!chromePath) {
  throw new Error("Chrome or Chromium was not found. Set CHROME_PATH to its executable.");
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
  ".png": "image/png"
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
page.on("console", (message) => {
  if (["error", "warning"].includes(message.type())) consoleErrors.push(message.text());
});
page.on("pageerror", (error) => consoleErrors.push(error.message));

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
  throw new Error("A certified viewport has document-level horizontal overflow.");
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
if (!bulkConfirmed.progress.startsWith("40 approved locally") || bulkConfirmed.blockedDecision !== "Needs fix") {
  throw new Error("Bulk approval changed a row that still has offline blockers.");
}

await page.click('tr[data-source-row="2"]');
await page.$eval("#undo-action", (element) => element.click());
const bulkUndone = await page.evaluate(() => ({
  progress: document.querySelector("#review-progress").textContent,
  status: document.querySelector("#status-line").textContent
}));
await page.click("#close-detail");

await page.type("#search", "no-row-can-match-this-query");
const emptyFilter = await page.evaluate(() => ({
  caption: document.querySelector("#table-caption").textContent,
  title: document.querySelector("#detail-title").textContent,
  detailFields: document.querySelector("#detail-grid").children.length,
  issueCount: document.querySelector("#issue-list").children.length,
  approveDisabled: document.querySelector("#mark-ready").disabled,
  previewHeadline: document.querySelector("#preview-headline").textContent
}));
await page.$eval("#search", (element) => {
  element.value = "";
  element.dispatchEvent(new Event("input", { bubbles: true }));
});

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
await page.click('button[data-filter="needs_review"]');
await page.evaluate(() => window.scrollTo(0, 0));
await page.screenshot({ path: join(assetsDir, "workspace-mobile.png") });

await page.setViewport({ width: 1440, height: 1000 });
await page.goto(url, { waitUntil: "load" });
await page.screenshot({ path: join(assetsDir, "workspace-desktop.png") });

const evidenceUrl = `${baseUrl}/docs/brief-evidence.html`;
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
const desktopLighthouse = join(evidenceDir, "workspace-lighthouse-accessibility-desktop.json");
const mobileLighthouse = join(evidenceDir, "workspace-lighthouse-accessibility-mobile.json");

for (const [formFactor, outputPath] of [
  ["desktop", desktopLighthouse],
  ["mobile", mobileLighthouse]
]) {
  const args = [
    url,
    `--chrome-path=${chromePath}`,
    "--only-categories=accessibility",
    `--form-factor=${formFactor}`,
    "--output=json",
    `--output-path=${outputPath}`,
    "--quiet"
  ];
  if (formFactor === "desktop") args.push("--screenEmulation.disabled");
  if (process.platform === "linux") {
    args.push("--chrome-flags=--headless=new --no-sandbox --disable-dev-shm-usage");
  }
  await runFile(lighthouseBin, args, { cwd: root, maxBuffer: 10 * 1024 * 1024 });
}

const desktopReport = JSON.parse(await readFile(desktopLighthouse, "utf8"));
const mobileReport = JSON.parse(await readFile(mobileLighthouse, "utf8"));
const accessibility = {
  desktopScore: desktopReport.categories.accessibility.score,
  mobileScore: mobileReport.categories.accessibility.score
};
if (accessibility.desktopScore !== 1 || accessibility.mobileScore !== 1) {
  throw new Error(`Lighthouse accessibility score regressed: ${JSON.stringify(accessibility)}`);
}

const report = {
  contract_version: "workspace_runtime_qa.v3",
  tested_at: new Date().toISOString(),
  source: "scripts/workspace_runtime_qa.mjs",
  viewports,
  mobile_drawer: { opened: drawerOpened, closed: drawerClosed },
  keyboard,
  bulk: { dialog: bulkDialog, cancelled: bulkCancelled, confirmed: bulkConfirmed, undone: bulkUndone },
  empty_filter: emptyFilter,
  filter_reconciliation: filterReconciliation,
  persistence,
  reset,
  evidence_page: evidencePage,
  console_errors: consoleErrors,
  lighthouse_accessibility: accessibility,
  mutation_allowed: false,
  meta_api_compatibility: "not_claimed"
};
await writeFile(join(evidenceDir, "workspace-runtime-qa.json"), `${JSON.stringify(report, null, 2)}\n`);

await new Promise((resolve, reject) => {
  server.close((error) => (error ? reject(error) : resolve()));
});
console.log(JSON.stringify({ status: "pass", accessibility, viewports: viewports.length }, null, 2));
