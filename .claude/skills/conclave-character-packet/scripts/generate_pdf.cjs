/* Render the print-shop booklet HTML to a verified PDF with headless Chromium.
 *
 * Usage:
 *   node generate_pdf.cjs [HTML_PATH] [OUT_PDF]
 * Defaults: HTML_PATH=booklet/print-shop.html, OUT_PDF=booklet/Reference-Booklet.pdf
 *
 * Requires Playwright's Chromium. If missing, install once:
 *   node <playwright>/cli.js install chromium
 * The script auto-discovers a global Playwright install.
 *
 * It waits for the engine to paginate, exports at trim+bleed (5.75x8.75in,
 * backgrounds on), then re-opens the PDF to confirm the page count matches
 * the live .print-page count and is a multiple of four (saddle-stitch safe).
 */
const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');

function resolvePlaywright() {
  const candidates = [];
  try { candidates.push(require.resolve('playwright')); } catch (e) {}
  try {
    const root = execSync('npm root -g', { encoding: 'utf8' }).trim();
    candidates.push(path.join(root, 'playwright'));
  } catch (e) {}
  for (const c of candidates) {
    try { return require(c); } catch (e) {}
  }
  throw new Error('Playwright not found. Install with: npm i -g playwright && node $(npm root -g)/playwright/cli.js install chromium');
}

function pdfPageCount(file) {
  const data = fs.readFileSync(file);
  const counts = [...data.toString('latin1').matchAll(/\/Count\s+(\d+)/g)].map(m => +m[1]);
  return counts.length ? Math.max(...counts) : 0;
}

(async () => {
  const htmlPath = path.resolve(process.argv[2] || 'booklet/print-shop.html');
  const outPdf = path.resolve(process.argv[3] || 'booklet/Reference-Booklet.pdf');
  if (!fs.existsSync(htmlPath)) throw new Error('no such HTML: ' + htmlPath);

  const { chromium } = resolvePlaywright();
  const b = await chromium.launch();
  const p = await b.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push('PAGEERR: ' + e.message));

  await p.goto('file://' + htmlPath);
  await p.waitForFunction(
    () => document.querySelectorAll('#mount .print-page').length > 0, { timeout: 30000 });
  await p.waitForTimeout(1500); // let fonts/map settle

  const live = await p.evaluate(() => document.querySelectorAll('#mount .print-page').length);
  await p.pdf({
    path: outPdf, width: '5.75in', height: '8.75in', printBackground: true,
    margin: { top: '0', bottom: '0', left: '0', right: '0' }, preferCSSPageSize: true,
  });
  await b.close();

  const pages = pdfPageCount(outPdf);
  console.log(`live pages: ${live}`);
  console.log(`pdf pages:  ${pages}  -> ${outPdf}`);
  if (errs.length) console.log('page errors:', errs.slice(0, 5));

  const problems = [];
  if (pages !== live) problems.push(`pdf page count ${pages} != live ${live} (export truncated?)`);
  if (pages % 4 !== 0) problems.push(`page count ${pages} is not a multiple of 4 (saddle stitch needs it)`);
  if (problems.length) { console.error('FAIL:\n  ' + problems.join('\n  ')); process.exit(1); }
  console.log('OK: complete booklet, multiple of four.');
})();
