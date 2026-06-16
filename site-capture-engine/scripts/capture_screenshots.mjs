#!/usr/bin/env node
/**
 * capture_screenshots.mjs — automated, repeatable screenshots for site capture.
 *
 * WHY a host script (not the Cowork sandbox): the sandbox can't finish Chromium's ~185MB download
 * inside its short command window. Run this on the host (Mac via Claude Code) or any CI worker.
 *
 * Setup (once):  npm i playwright && npx playwright install chromium
 * Run:           node capture_screenshots.mjs <domain> <out-dir> [urls.txt] [--design-capture]
 *   - <domain>   e.g. https://example.com
 *   - <out-dir>  e.g. .../<slug>-teardown/raw/screenshots   (a dated subfolder is created automatically)
 *   - urls.txt   optional: one URL or path per line. If omitted, a default tier set is derived.
 *   - --design-capture  enables the design-capture context extensions (v2.1):
 *       + tablet viewport (768px)
 *       + per-major-section crops with fold-line marking
 *       + scroll-stop screenshots (captures scroll-triggered reveals)
 *       + component bounding-box screenshots
 *       + screenshot manifest (maps each image → section/component/viewport)
 *
 * Standard output: <out-dir>/<YYYY-MM-DD>/<tier>__<device>__<full|fold>.png
 *   - desktop (1440x900) + mobile (iPhone 390x844)
 *   - above-the-fold + full-page for each
 *
 * Design-capture additions:
 *   - tablet (768x1024) viewport screenshots
 *   - <out-dir>/<YYYY-MM-DD>/sections/<tier>__<device>__section-<N>.png
 *   - <out-dir>/<YYYY-MM-DD>/scroll-stops/<tier>__<device>__scroll-<N>.png
 *   - <out-dir>/<YYYY-MM-DD>/components/<tier>__<component-type>.png
 *   - <out-dir>/<YYYY-MM-DD>/screenshot-manifest.json
 *
 * The dated folder makes BEFORE/AFTER tracking trivial: re-run on a HeyTony change alert; diff folders.
 */
import { chromium, devices } from 'playwright';
import fs from 'fs'; import path from 'path';

const args = process.argv.slice(2);
const designCapture = args.includes('--design-capture');
const positionalArgs = args.filter(a => !a.startsWith('--'));

const domain = (positionalArgs[0] || '').replace(/\/$/, '');
const outRoot = positionalArgs[1];
const urlsFile = positionalArgs[2];
if (!domain || !outRoot) { console.error('usage: node capture_screenshots.mjs <domain> <out-dir> [urls.txt] [--design-capture]'); process.exit(1); }

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

// Standard viewports (always)
const viewports = [
  ['desktop', { viewport: { width: 1440, height: 900 } }],
  ['mobile', { ...devices['iPhone 13'] }],
];

// Design-capture adds tablet
if (designCapture) {
  viewports.push(['tablet', { viewport: { width: 768, height: 1024 } }]);
  fs.mkdirSync(path.join(outDir, 'sections'), { recursive: true });
  fs.mkdirSync(path.join(outDir, 'scroll-stops'), { recursive: true });
  fs.mkdirSync(path.join(outDir, 'components'), { recursive: true });
  console.log('Design-capture mode enabled: +tablet viewport, +section crops, +scroll-stops, +component shots');
}

const manifest = []; // screenshot manifest entries

const browser = await chromium.launch();
for (const [label, ctxOpts] of viewports) {
  const ctx = await browser.newContext(ctxOpts);
  const page = await ctx.newPage();
  for (const [tier, p] of targets) {
    const url = domain + p;
    try {
      await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
      await page.waitForTimeout(1200); // let RSC hydrate + animations settle

      // --- Standard captures (all modes) ---
      const base = path.join(outDir, `${tier}__${label}`);
      await page.screenshot({ path: `${base}__fold.png` });
      manifest.push({ file: `${tier}__${label}__fold.png`, type: 'fold', viewport: label, page: tier, url });
      await page.screenshot({ path: `${base}__full.png`, fullPage: true });
      manifest.push({ file: `${tier}__${label}__full.png`, type: 'full-page', viewport: label, page: tier, url });
      console.log(`ok  ${tier} ${label}  ${url}`);

      // --- Design-capture extensions ---
      if (designCapture) {
        // 1. Per-section crops with fold-line marking
        const sections = await page.evaluate(() => {
          const viewportHeight = window.innerHeight;
          const sectionEls = document.querySelectorAll(
            'main > section, main > div, article > section, [class*="section"], ' +
            '[class*="Section"], header, footer, nav, [role="banner"], [role="main"], [role="contentinfo"]'
          );
          const seen = new Set();
          const results = [];
          for (const el of sectionEls) {
            const rect = el.getBoundingClientRect();
            if (rect.height < 50 || rect.width < 100) continue;
            // Deduplicate overlapping sections
            const key = `${Math.round(rect.top)}:${Math.round(rect.height)}`;
            if (seen.has(key)) continue;
            seen.add(key);
            results.push({
              tag: el.tagName.toLowerCase(),
              className: el.className ? String(el.className).split(' ').filter(Boolean)[0] : '',
              top: rect.top + window.scrollY,
              left: rect.left,
              width: rect.width,
              height: Math.min(rect.height, 3000), // cap extremely tall sections
              isBelowFold: rect.top > viewportHeight,
            });
          }
          return { sections: results.slice(0, 20), foldLine: viewportHeight };
        });

        for (let i = 0; i < sections.sections.length; i++) {
          const s = sections.sections[i];
          const sectionFile = `sections/${tier}__${label}__section-${i + 1}.png`;
          try {
            await page.screenshot({
              path: path.join(outDir, sectionFile),
              fullPage: true,
              clip: { x: Math.max(0, s.left), y: Math.max(0, s.top), width: Math.max(1, s.width), height: Math.max(1, s.height) },
            });
            manifest.push({
              file: sectionFile,
              type: 'section-crop',
              viewport: label,
              page: tier,
              url,
              section: { index: i + 1, tag: s.tag, className: s.className, belowFold: s.isBelowFold },
            });
          } catch (e) { console.error(`  section ${i + 1} crop failed: ${e.message}`); }
        }
        console.log(`  ${sections.sections.length} section crops (fold at ${sections.foldLine}px)`);

        // 2. Scroll-stop screenshots (capture scroll-triggered reveals)
        const pageHeight = await page.evaluate(() => document.documentElement.scrollHeight);
        const viewportH = ctxOpts.viewport ? ctxOpts.viewport.height : 900;
        const scrollStops = [];
        const stopInterval = Math.max(viewportH, 600);
        for (let scrollY = 0; scrollY < pageHeight; scrollY += stopInterval) {
          scrollStops.push(scrollY);
        }
        // Cap at 10 scroll stops to avoid excessive screenshots
        const cappedStops = scrollStops.slice(0, 10);

        for (let i = 0; i < cappedStops.length; i++) {
          await page.evaluate(y => window.scrollTo(0, y), cappedStops[i]);
          await page.waitForTimeout(500); // let scroll-triggered animations fire
          const scrollFile = `scroll-stops/${tier}__${label}__scroll-${i + 1}.png`;
          await page.screenshot({ path: path.join(outDir, scrollFile) });
          manifest.push({
            file: scrollFile,
            type: 'scroll-stop',
            viewport: label,
            page: tier,
            url,
            scrollY: cappedStops[i],
          });
        }
        console.log(`  ${cappedStops.length} scroll-stop captures`);

        // 3. Component bounding-box screenshots (desktop only — most useful viewport)
        if (label === 'desktop') {
          await page.evaluate(() => window.scrollTo(0, 0));
          await page.waitForTimeout(300);

          const componentBounds = await page.evaluate(() => {
            const found = [];

            // Hero
            const hero = document.querySelector('[class*="hero"], [class*="Hero"], main > section:first-child, main > div:first-child');
            if (hero) {
              const r = hero.getBoundingClientRect();
              if (r.height > 100) found.push({ type: 'hero', top: r.top + window.scrollY, left: r.left, width: r.width, height: Math.min(r.height, 2000) });
            }

            // Primary nav
            const nav = document.querySelector('nav, header nav, [role="navigation"]');
            if (nav) {
              const r = nav.getBoundingClientRect();
              found.push({ type: 'primary-nav', top: r.top + window.scrollY, left: r.left, width: r.width, height: r.height });
            }

            // Footer
            const footer = document.querySelector('footer, [role="contentinfo"]');
            if (footer) {
              const r = footer.getBoundingClientRect();
              found.push({ type: 'footer', top: r.top + window.scrollY, left: r.left, width: r.width, height: Math.min(r.height, 1500) });
            }

            // CTA blocks
            const ctas = document.querySelectorAll('[class*="cta"], [class*="CTA"], [class*="call-to-action"]');
            for (const cta of Array.from(ctas).slice(0, 3)) {
              const r = cta.getBoundingClientRect();
              if (r.height > 30) found.push({ type: 'cta-block', top: r.top + window.scrollY, left: r.left, width: r.width, height: r.height });
            }

            // Testimonial / review sections
            const testimonials = document.querySelector('[class*="testimonial"], [class*="review"], [class*="Testimonial"]');
            if (testimonials) {
              const r = testimonials.getBoundingClientRect();
              if (r.height > 50) found.push({ type: 'testimonial', top: r.top + window.scrollY, left: r.left, width: r.width, height: Math.min(r.height, 1500) });
            }

            // FAQ
            const faq = document.querySelector('[class*="faq"], [class*="FAQ"], [class*="accordion"]');
            if (faq) {
              const r = faq.getBoundingClientRect();
              if (r.height > 50) found.push({ type: 'faq-accordion', top: r.top + window.scrollY, left: r.left, width: r.width, height: Math.min(r.height, 2000) });
            }

            return found;
          });

          for (const comp of componentBounds) {
            const compFile = `components/${tier}__${comp.type}.png`;
            try {
              await page.screenshot({
                path: path.join(outDir, compFile),
                fullPage: true,
                clip: { x: Math.max(0, comp.left), y: Math.max(0, comp.top), width: Math.max(1, comp.width), height: Math.max(1, comp.height) },
              });
              manifest.push({
                file: compFile,
                type: 'component',
                viewport: label,
                page: tier,
                url,
                component: comp.type,
              });
            } catch (e) { console.error(`  component ${comp.type} crop failed: ${e.message}`); }
          }
          console.log(`  ${componentBounds.length} component screenshots`);
        }

        // Reset scroll position for next page
        await page.evaluate(() => window.scrollTo(0, 0));
      }
    } catch (e) { console.error(`ERR ${tier} ${label}  ${url}  ${e.message}`); }
  }
  await ctx.close();
}
await browser.close();

// Write screenshot manifest (design-capture mode only, but always written for consistency)
if (designCapture) {
  const manifestData = {
    capturedAt: new Date().toISOString(),
    engineVersion: '2.1',
    domain,
    viewports: viewports.map(([name, opts]) => ({
      name,
      width: opts.viewport ? opts.viewport.width : (opts.screen ? opts.screen.width : null),
      height: opts.viewport ? opts.viewport.height : (opts.screen ? opts.screen.height : null),
    })),
    pages: targets.map(([tier, p]) => ({ tier, path: p, url: domain + p })),
    screenshots: manifest,
    totals: {
      standard: manifest.filter(m => m.type === 'fold' || m.type === 'full-page').length,
      sectionCrops: manifest.filter(m => m.type === 'section-crop').length,
      scrollStops: manifest.filter(m => m.type === 'scroll-stop').length,
      components: manifest.filter(m => m.type === 'component').length,
    },
  };
  fs.writeFileSync(path.join(outDir, 'screenshot-manifest.json'), JSON.stringify(manifestData, null, 2));
  console.log(`\nWrote screenshot-manifest.json (${manifest.length} total screenshots)`);
}

console.log(`\nDone → ${outDir}`);
