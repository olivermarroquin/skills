#!/usr/bin/env node
/**
 * capture_screenshots.mjs — automated, repeatable screenshots for an SEO site teardown.
 *
 * WHY a host script (not the Cowork sandbox): the sandbox can't finish Chromium's ~185MB download
 * inside its short command window. Run this on the host (Mac via Claude Code) or any CI worker.
 *
 * Setup (once):  npm i playwright && npx playwright install chromium
 * Run:           node capture_screenshots.mjs <domain> <out-dir> [urls.txt]
 *   - <domain>   e.g. https://ajlongelectric.com
 *   - <out-dir>  e.g. .../<slug>-teardown/raw/screenshots   (a dated subfolder is created automatically)
 *   - urls.txt   optional: one URL or path per line. If omitted, a default tier set is derived.
 *
 * Output: <out-dir>/<YYYY-MM-DD>/<tier>__<device>__<full|fold>.png
 *   - desktop (1440x900) + mobile (iPhone 390x844)
 *   - above-the-fold + full-page for each
 * The dated folder makes BEFORE/AFTER tracking trivial: re-run on a HeyTony change alert; diff folders.
 */
import { chromium, devices } from 'playwright';
import fs from 'fs'; import path from 'path';

const domain = (process.argv[2] || '').replace(/\/$/, '');
const outRoot = process.argv[3];
const urlsFile = process.argv[4];
if (!domain || !outRoot) { console.error('usage: node capture_screenshots.mjs <domain> <out-dir> [urls.txt]'); process.exit(1); }

// Default tier-representative pages — generic paths that work for most sites.
// Override by passing a urls.txt with one URL per line (recommend: 1 per tier + top rankers).
// When running on a specific site, a urls.txt is almost always better than these defaults.
const defaults = [
  ['home', '/'],
  ['about', '/about'],
  ['services', '/services'],
  ['blog', '/blog'],
  ['contact', '/contact'],
];
let targets = defaults;
if (urlsFile && fs.existsSync(urlsFile)) {
  targets = fs.readFileSync(urlsFile, 'utf8').split('\n').map(s => s.trim()).filter(Boolean)
    .map((u, i) => [`url${i + 1}`, u.startsWith('http') ? u.replace(domain, '') : u]);
}

const date = new Date().toISOString().slice(0, 10);
const outDir = path.join(outRoot, date);
fs.mkdirSync(outDir, { recursive: true });

const viewports = [
  ['desktop', { viewport: { width: 1440, height: 900 } }],
  ['mobile', { ...devices['iPhone 13'] }],
];

const browser = await chromium.launch();
for (const [label, ctxOpts] of viewports) {
  const ctx = await browser.newContext(ctxOpts);
  const page = await ctx.newPage();
  for (const [tier, p] of targets) {
    const url = domain + p;
    try {
      await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
      await page.waitForTimeout(1200); // let RSC hydrate + animations settle
      const base = path.join(outDir, `${tier}__${label}`);
      await page.screenshot({ path: `${base}__fold.png` });             // above-the-fold
      await page.screenshot({ path: `${base}__full.png`, fullPage: true }); // full page
      console.log(`ok  ${tier} ${label}  ${url}`);
    } catch (e) { console.error(`ERR ${tier} ${label}  ${url}  ${e.message}`); }
  }
  await ctx.close();
}
await browser.close();
console.log(`\nDone → ${outDir}`);
