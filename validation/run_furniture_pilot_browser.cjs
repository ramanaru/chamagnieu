#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const root = path.resolve(__dirname, '..');
const base = process.env.FURNITURE_PILOT_BASE || 'http://127.0.0.1:8898';
const chrome = process.env.CHROME_PATH || 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';

(async () => {
  const browser = await chromium.launch({
    executablePath: chrome,
    headless: true,
    args: ['--no-sandbox', '--enable-webgl', '--ignore-gpu-blocklist', '--use-angle=swiftshader']
  });
  const results = [];
  const runMain = process.env.FURNITURE_PILOT_MAIN === '1';
  for (const view of (runMain ? ['living'] : ['fixture'])) {
    const page = await browser.newPage({ viewport: { width: 1440, height: 960 }, deviceScaleFactor: 1 });
    const consoleErrors = [];
    const pageErrors = [];
    const failedRequests = [];
    page.on('console', msg => { if (msg.type() === 'error') consoleErrors.push(msg.text()); });
    page.on('pageerror', error => pageErrors.push(error.message));
    page.on('requestfailed', request => failedRequests.push(`${request.url()} :: ${request.failure()?.errorText}`));
    const url = runMain
      ? `${base}/validation/furniture-pilot-harness.html?main=1&view=${view}&pw=1`
      : `${base}/validation/furniture-pilot-harness.html?pw=1`;
    const response = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 120000 });
    await page.waitForFunction(() => ['true', 'failed'].includes(document.documentElement.dataset.viewerReady), null, { timeout: 120000 });
    const audit = await page.evaluate(() => globalThis.__assetPilotFurnitureAudit || null);
    const dataset = await page.evaluate(() => ({ ...document.documentElement.dataset }));
    const screenshot = path.join(root, 'validation', 'browser', `playwright-furniture-main-${view}.png`);
    await page.screenshot({ path: screenshot, fullPage: false });
    results.push({
      view,
      url,
      httpStatus: response?.status() || null,
      dataset,
      audit,
      consoleErrors,
      pageErrors,
      failedRequests,
      screenshot: path.relative(root, screenshot).replace(/\\/g, '/')
    });
    await page.close();
  }
  await browser.close();

  const living = results[0];
  const families = living.audit?.families || {};
  const expectedFallbacks = { sofa: 1, table: 5, chair: 6, bed: 30 };
  const instances = { sofa: 1, table: 1, chair: 6, bed: 3 };
  let instanceTriangles = 0;
  let instanceDrawCalls = 0;
  for (const [role, family] of Object.entries(families)) {
    instanceTriangles += (family.sourceMetrics?.triangles || 0) * instances[role];
    instanceDrawCalls += (family.sourceMetrics?.drawCalls || 0) * instances[role];
  }
  const assertions = {
    viewsReady: results.every(x => x.httpStatus === 200 && x.dataset.viewerReady === 'true'),
    acceptedFourFamilies: results.every(x => x.audit?.status === 'accepted' && x.audit?.acceptedFamilies === 4),
    architectureUnchanged: results.every(x => x.audit?.architectureChanged === false),
    fallbackCounts: Object.entries(expectedFallbacks).every(([role, count]) => families[role]?.hiddenFallbackNodes?.length === count),
    zeroConsoleErrors: results.every(x => x.consoleErrors.length === 0 && x.pageErrors.length === 0),
    zeroFailedRequests: results.every(x => x.failedRequests.length === 0)
  };
  const output = {
    schemaVersion: '1.0',
    result: Object.values(assertions).every(Boolean) ? 'PASS' : 'FAIL',
    assertions,
    instanceBudget: { instances, triangles: instanceTriangles, drawCalls: instanceDrawCalls },
    views: results
  };
  const target = path.join(root, 'validation', 'pilot_furniture_browser.json');
  fs.writeFileSync(target, JSON.stringify(output, null, 2));
  process.stdout.write(`FURNITURE_BROWSER_RESULT=${output.result} families=${living.audit?.acceptedFamilies || 0}/4 triangles=${instanceTriangles} drawCalls=${instanceDrawCalls} output=${target}\n`);
  if (output.result !== 'PASS') process.exitCode = 1;
})().catch(error => {
  console.error(error);
  process.exit(1);
});
