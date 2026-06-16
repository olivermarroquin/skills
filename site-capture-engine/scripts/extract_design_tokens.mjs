#!/usr/bin/env node
/**
 * extract_design_tokens.mjs — computed-style design token extractor for the design-capture context.
 *
 * Extracts design tokens from the LIVE RENDERED DOM (getComputedStyle), not source CSS.
 * Source CSS lies; rendered style doesn't. (Lesson from hub-and-nav-build.)
 *
 * Also captures: motion/interaction inventory, component inventory, a11y/contrast snapshot.
 *
 * Setup:  npm i playwright && npx playwright install chromium
 * Run:    node extract_design_tokens.mjs <url> <out-dir> [--full-motion]
 *
 * Output:
 *   <out-dir>/design-tokens.json       — machine-readable token set
 *   <out-dir>/design-tokens.md         — human-readable token summary (matches AJ Long example format)
 *   <out-dir>/motion-inventory.json    — CSS transitions, keyframes, animation libraries
 *   <out-dir>/component-inventory.json — detected recurring visual components
 *   <out-dir>/a11y-snapshot.json       — WCAG contrast, heading hierarchy, alt-text coverage
 */
import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';

const url = process.argv[2];
const outDir = process.argv[3];
const fullMotion = process.argv.includes('--full-motion');

if (!url || !outDir) {
  console.error('usage: node extract_design_tokens.mjs <url> <out-dir> [--full-motion]');
  process.exit(1);
}

fs.mkdirSync(outDir, { recursive: true });

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function rgbToHex(rgb) {
  if (!rgb || rgb === 'transparent' || rgb === 'rgba(0, 0, 0, 0)') return null;
  const m = rgb.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
  if (!m) return null;
  return '#' + [m[1], m[2], m[3]].map(x => parseInt(x).toString(16).padStart(2, '0')).join('');
}

function relativeLuminance(hex) {
  const r = parseInt(hex.slice(1, 3), 16) / 255;
  const g = parseInt(hex.slice(3, 5), 16) / 255;
  const b = parseInt(hex.slice(5, 7), 16) / 255;
  const toLinear = c => c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  return 0.2126 * toLinear(r) + 0.7152 * toLinear(g) + 0.0722 * toLinear(b);
}

function contrastRatio(hex1, hex2) {
  const l1 = relativeLuminance(hex1);
  const l2 = relativeLuminance(hex2);
  const lighter = Math.max(l1, l2);
  const darker = Math.min(l1, l2);
  return (lighter + 0.05) / (darker + 0.05);
}

// ---------------------------------------------------------------------------
// Main extraction (runs in Playwright page context)
// ---------------------------------------------------------------------------

async function extractFromPage(page) {
  return page.evaluate(() => {
    const allElements = document.querySelectorAll('body *');
    const visible = [];

    for (const el of allElements) {
      const rect = el.getBoundingClientRect();
      const style = window.getComputedStyle(el);
      if (rect.width === 0 && rect.height === 0) continue;
      if (style.display === 'none' || style.visibility === 'hidden') continue;
      visible.push({ el, rect, style, tag: el.tagName.toLowerCase() });
    }

    // --- Colors ---
    const colorMap = {}; // hex → { count, roles: Set }
    function trackColor(hex, role) {
      if (!hex || hex === '#000000' && role === 'border') return; // skip default borders
      if (!colorMap[hex]) colorMap[hex] = { count: 0, roles: [] };
      colorMap[hex].count++;
      if (!colorMap[hex].roles.includes(role)) colorMap[hex].roles.push(role);
    }

    for (const { style } of visible) {
      const bg = style.backgroundColor;
      const fg = style.color;
      const border = style.borderColor;

      // Convert to hex
      const bgHex = (() => {
        if (!bg || bg === 'transparent' || bg === 'rgba(0, 0, 0, 0)') return null;
        const m = bg.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
        if (!m) return null;
        return '#' + [m[1], m[2], m[3]].map(x => parseInt(x).toString(16).padStart(2, '0')).join('');
      })();
      const fgHex = (() => {
        if (!fg) return null;
        const m = fg.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
        if (!m) return null;
        return '#' + [m[1], m[2], m[3]].map(x => parseInt(x).toString(16).padStart(2, '0')).join('');
      })();
      const borderHex = (() => {
        if (!border || border === 'transparent' || border === 'rgba(0, 0, 0, 0)') return null;
        const m = border.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
        if (!m) return null;
        return '#' + [m[1], m[2], m[3]].map(x => parseInt(x).toString(16).padStart(2, '0')).join('');
      })();

      if (bgHex) trackColor(bgHex, 'background');
      if (fgHex) trackColor(fgHex, 'text');
      if (borderHex && borderHex !== bgHex) trackColor(borderHex, 'border');
    }

    // --- Typography ---
    const typeByRole = {};
    const roleMap = { h1: 'h1', h2: 'h2', h3: 'h3', h4: 'h4', h5: 'h5', h6: 'h6',
      p: 'body', span: 'body', li: 'body', td: 'body', dd: 'body',
      button: 'button', a: 'link', figcaption: 'caption', small: 'caption',
      label: 'label', input: 'input' };

    for (const { tag, style } of visible) {
      const role = roleMap[tag] || null;
      if (!role) continue;
      const key = `${role}|${style.fontFamily.split(',')[0].trim().replace(/['"]/g, '')}|${style.fontWeight}|${style.fontSize}|${style.lineHeight}`;
      if (!typeByRole[key]) {
        typeByRole[key] = {
          role,
          fontFamily: style.fontFamily.split(',')[0].trim().replace(/['"]/g, ''),
          fontFamilyFull: style.fontFamily,
          fontWeight: style.fontWeight,
          fontSize: style.fontSize,
          lineHeight: style.lineHeight,
          count: 0,
        };
      }
      typeByRole[key].count++;
    }

    // --- Spacing ---
    const spacingValues = [];
    for (const { style } of visible) {
      for (const prop of ['marginTop', 'marginRight', 'marginBottom', 'marginLeft',
                          'paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft']) {
        const val = parseFloat(style[prop]);
        if (val > 0 && val < 500) spacingValues.push(Math.round(val));
      }
    }
    // Histogram
    const spacingHist = {};
    for (const v of spacingValues) {
      spacingHist[v] = (spacingHist[v] || 0) + 1;
    }

    // --- Border radius ---
    const radiusSet = {};
    for (const { style } of visible) {
      const r = style.borderRadius;
      if (r && r !== '0px') {
        radiusSet[r] = (radiusSet[r] || 0) + 1;
      }
    }

    // --- Shadows ---
    const shadowSet = {};
    for (const { style } of visible) {
      const s = style.boxShadow;
      if (s && s !== 'none') {
        shadowSet[s] = (shadowSet[s] || 0) + 1;
      }
    }

    // --- Transitions + animations ---
    const transitions = [];
    const animations = [];
    for (const { tag, style, el } of visible) {
      const t = style.transition;
      if (t && t !== 'all 0s ease 0s' && t !== 'none 0s ease 0s' && t !== 'none') {
        transitions.push({ element: `${tag}${el.className ? '.' + String(el.className).split(' ').filter(Boolean)[0] : ''}`, transition: t });
      }
      const a = style.animationName;
      if (a && a !== 'none') {
        animations.push({ element: `${tag}${el.className ? '.' + String(el.className).split(' ').filter(Boolean)[0] : ''}`, animation: a, duration: style.animationDuration, timing: style.animationTimingFunction });
      }
    }

    // --- Detect animation libraries ---
    const libs = [];
    const scripts = Array.from(document.querySelectorAll('script[src]')).map(s => s.src);
    const inlineScripts = Array.from(document.querySelectorAll('script:not([src])')).map(s => s.textContent).join(' ');
    const allScriptText = scripts.join(' ') + ' ' + inlineScripts;

    if (allScriptText.includes('framer-motion') || allScriptText.includes('motion.div') || document.querySelector('[data-framer-component-type]')) libs.push('Framer Motion');
    if (allScriptText.includes('gsap') || allScriptText.includes('TweenMax') || allScriptText.includes('ScrollTrigger')) libs.push('GSAP');
    if (allScriptText.includes('aos') || document.querySelector('[data-aos]')) libs.push('AOS');
    if (allScriptText.includes('lottie') || document.querySelector('lottie-player')) libs.push('Lottie');
    if (allScriptText.includes('animateOnScroll') || allScriptText.includes('IntersectionObserver')) libs.push('Intersection Observer (scroll triggers)');

    // --- Keyframe animations from stylesheets ---
    const keyframes = [];
    try {
      for (const sheet of document.styleSheets) {
        try {
          for (const rule of sheet.cssRules) {
            if (rule instanceof CSSKeyframesRule) {
              keyframes.push({ name: rule.name, keyframeCount: rule.cssRules.length });
            }
          }
        } catch (e) { /* cross-origin sheet */ }
      }
    } catch (e) { /* no access */ }

    // --- Component inventory ---
    const components = [];

    // Hero detection
    const firstSection = document.querySelector('main > section, main > div, [class*="hero"], [class*="Hero"], [id*="hero"]');
    if (firstSection) {
      const r = firstSection.getBoundingClientRect();
      components.push({ type: 'hero', selector: firstSection.tagName + (firstSection.className ? '.' + String(firstSection.className).split(' ')[0] : ''), bounds: { top: r.top, left: r.left, width: r.width, height: r.height } });
    }

    // Nav detection
    const nav = document.querySelector('nav, header nav, [role="navigation"]');
    if (nav) {
      const r = nav.getBoundingClientRect();
      components.push({ type: 'primary-nav', selector: 'nav', bounds: { top: r.top, left: r.left, width: r.width, height: r.height } });
    }

    // Footer detection
    const footer = document.querySelector('footer, [role="contentinfo"]');
    if (footer) {
      const r = footer.getBoundingClientRect();
      components.push({ type: 'footer', selector: 'footer', bounds: { top: r.top, left: r.left, width: r.width, height: r.height } });
    }

    // Card grid detection
    const cardGrids = document.querySelectorAll('[class*="grid"], [class*="card"], [class*="Grid"]');
    const seenGrids = new Set();
    for (const g of cardGrids) {
      const cs = window.getComputedStyle(g);
      if ((cs.display === 'grid' || cs.display === 'flex') && g.children.length >= 3) {
        const key = `${g.tagName}.${String(g.className).split(' ')[0]}`;
        if (!seenGrids.has(key)) {
          seenGrids.add(key);
          const r = g.getBoundingClientRect();
          components.push({ type: 'card-grid', selector: key, childCount: g.children.length, bounds: { top: r.top, left: r.left, width: r.width, height: r.height } });
        }
      }
    }

    // FAQ accordion detection
    const faqEls = document.querySelectorAll('[class*="faq"], [class*="FAQ"], [class*="accordion"], details, [itemtype*="FAQPage"]');
    if (faqEls.length > 0) {
      const first = faqEls[0];
      const r = first.getBoundingClientRect();
      components.push({ type: 'faq-accordion', selector: first.tagName + (first.className ? '.' + String(first.className).split(' ')[0] : ''), count: faqEls.length, bounds: { top: r.top, left: r.left, width: r.width, height: r.height } });
    }

    // CTA detection
    const ctas = document.querySelectorAll('a[class*="cta"], a[class*="CTA"], button[class*="cta"], a[class*="btn"], button[class*="btn"], [class*="call-to-action"]');
    if (ctas.length > 0) {
      components.push({ type: 'cta-block', count: ctas.length, samples: Array.from(ctas).slice(0, 5).map(c => ({ text: c.textContent.trim().slice(0, 80), href: c.href || null })) });
    }

    // Testimonial detection
    const testimonials = document.querySelectorAll('[class*="testimonial"], [class*="review"], [class*="Testimonial"], blockquote');
    if (testimonials.length > 0) {
      components.push({ type: 'testimonial', count: testimonials.length });
    }

    // --- A11y: heading hierarchy ---
    const headings = [];
    for (const h of document.querySelectorAll('h1, h2, h3, h4, h5, h6')) {
      headings.push({ level: parseInt(h.tagName[1]), text: h.textContent.trim().slice(0, 120) });
    }

    // --- A11y: alt-text coverage ---
    const images = document.querySelectorAll('img');
    let imgsWithAlt = 0, imgsWithoutAlt = 0, imgsDecorativeAlt = 0;
    for (const img of images) {
      const alt = img.getAttribute('alt');
      if (alt === null || alt === undefined) imgsWithoutAlt++;
      else if (alt === '') imgsDecorativeAlt++;
      else imgsWithAlt++;
    }

    // --- A11y: top text/bg contrast pairs ---
    const contrastPairs = [];
    const pairsSeen = new Set();
    for (const { style } of visible.slice(0, 500)) {
      const fg = style.color;
      const bg = style.backgroundColor;
      if (!fg || !bg || bg === 'transparent' || bg === 'rgba(0, 0, 0, 0)') continue;
      const fgM = fg.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
      const bgM = bg.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
      if (!fgM || !bgM) continue;
      const fgHex = '#' + [fgM[1], fgM[2], fgM[3]].map(x => parseInt(x).toString(16).padStart(2, '0')).join('');
      const bgHex = '#' + [bgM[1], bgM[2], bgM[3]].map(x => parseInt(x).toString(16).padStart(2, '0')).join('');
      if (fgHex === bgHex) continue;
      const key = `${fgHex}|${bgHex}`;
      if (pairsSeen.has(key)) continue;
      pairsSeen.add(key);

      // Compute contrast ratio inline
      function lum(hex) {
        const r = parseInt(hex.slice(1, 3), 16) / 255;
        const g = parseInt(hex.slice(3, 5), 16) / 255;
        const b = parseInt(hex.slice(5, 7), 16) / 255;
        const lin = c => c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
        return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
      }
      const l1 = lum(fgHex), l2 = lum(bgHex);
      const ratio = (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
      const passAA = ratio >= 4.5;
      const passAAA = ratio >= 7;
      const passAALarge = ratio >= 3;
      contrastPairs.push({ foreground: fgHex, background: bgHex, ratio: Math.round(ratio * 100) / 100, passAA, passAAA, passAALarge });
    }
    contrastPairs.sort((a, b) => a.ratio - b.ratio); // worst first

    return {
      colors: colorMap,
      typography: typeByRole,
      spacing: { histogram: spacingHist, sampleCount: spacingValues.length },
      borderRadius: radiusSet,
      shadows: shadowSet,
      motion: { transitions: transitions.slice(0, 50), animations: animations.slice(0, 50), keyframes, libraries: libs },
      components,
      a11y: {
        headingHierarchy: headings,
        altText: { total: images.length, withAlt: imgsWithAlt, withoutAlt: imgsWithoutAlt, decorative: imgsDecorativeAlt, coveragePercent: images.length > 0 ? Math.round((imgsWithAlt + imgsDecorativeAlt) / images.length * 100) : 100 },
        contrastPairs: contrastPairs.slice(0, 20),
      },
      meta: { elementCount: visible.length, url: window.location.href, title: document.title },
    };
  });
}

// ---------------------------------------------------------------------------
// Run
// ---------------------------------------------------------------------------

console.log(`Extracting design tokens from: ${url}`);
console.log(`Output: ${outDir}`);

const browser = await chromium.launch();
const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
const page = await context.newPage();

try {
  await page.goto(url, { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(2000); // let hydration + animations settle
} catch (e) {
  console.error(`Navigation error: ${e.message}`);
  await browser.close();
  process.exit(1);
}

const data = await extractFromPage(page);
await browser.close();

// ---------------------------------------------------------------------------
// Post-process: infer color roles (brand/accent) from frequency
// ---------------------------------------------------------------------------

const colors = Object.entries(data.colors)
  .map(([hex, info]) => ({ hex, ...info }))
  .sort((a, b) => b.count - a.count);

// Infer roles: top bg = page bg, top text = primary text, highest-count non-bg/text = brand/accent
const bgColors = colors.filter(c => c.roles.includes('background'));
const textColors = colors.filter(c => c.roles.includes('text'));
const brandCandidates = colors.filter(c => {
  // Not a gray/near-gray
  const r = parseInt(c.hex.slice(1, 3), 16);
  const g = parseInt(c.hex.slice(3, 5), 16);
  const b = parseInt(c.hex.slice(5, 7), 16);
  const max = Math.max(r, g, b), min = Math.min(r, g, b);
  return (max - min) > 30; // has some saturation
});

for (const c of colors) {
  c.inferredRole = c.roles.join(' / ');
}
if (bgColors[0]) bgColors[0].inferredRole = 'page-background';
if (textColors[0]) textColors[0].inferredRole = 'primary-text';
if (brandCandidates[0]) brandCandidates[0].inferredRole = 'brand / accent';
if (brandCandidates[1]) brandCandidates[1].inferredRole = 'secondary-accent';

// ---------------------------------------------------------------------------
// Infer spacing base unit
// ---------------------------------------------------------------------------

const spacingEntries = Object.entries(data.spacing.histogram)
  .map(([v, c]) => [parseInt(v), c])
  .sort((a, b) => b[1] - a[1]);

let baseUnit = 4; // default
if (spacingEntries.length > 0) {
  // Find GCD of top spacing values
  const topValues = spacingEntries.slice(0, 10).map(e => e[0]).filter(v => v > 0);
  if (topValues.length > 0) {
    const gcd = (a, b) => b === 0 ? a : gcd(b, a % b);
    baseUnit = topValues.reduce((a, b) => gcd(a, b));
    if (baseUnit < 2) baseUnit = 4; // fallback
  }
}

// ---------------------------------------------------------------------------
// Write design-tokens.json
// ---------------------------------------------------------------------------

const tokensJson = {
  url: data.meta.url,
  title: data.meta.title,
  capturedAt: new Date().toISOString(),
  engineVersion: '2.1',
  palette: colors.slice(0, 20).map(c => ({
    hex: c.hex,
    count: c.count,
    roles: c.roles,
    inferredRole: c.inferredRole,
  })),
  typography: Object.values(data.typography)
    .sort((a, b) => b.count - a.count)
    .slice(0, 30)
    .map(t => ({
      role: t.role,
      fontFamily: t.fontFamily,
      fontWeight: t.fontWeight,
      fontSize: t.fontSize,
      lineHeight: t.lineHeight,
      count: t.count,
    })),
  spacing: {
    baseUnit: `${baseUnit}px`,
    topValues: spacingEntries.slice(0, 15).map(([v, c]) => ({ px: v, count: c })),
  },
  borderRadius: Object.entries(data.borderRadius)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .map(([v, c]) => ({ value: v, count: c })),
  shadows: Object.entries(data.shadows)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .map(([v, c]) => ({ value: v, count: c })),
};

fs.writeFileSync(path.join(outDir, 'design-tokens.json'), JSON.stringify(tokensJson, null, 2));
console.log('Wrote design-tokens.json');

// ---------------------------------------------------------------------------
// Write design-tokens.md (human-readable, matches AJ Long example format)
// ---------------------------------------------------------------------------

let md = `---
type: design-tokens
source: ${data.meta.url} (computed-style extraction)
captured: ${new Date().toISOString().slice(0, 10)}
engine-version: "2.1"
tags: [design-tokens, design-capture, site-capture-engine]
---

# ${data.meta.title || new URL(url).hostname} — design tokens (computed-style extraction)

Extracted from the live rendered DOM via \`getComputedStyle\`. These are the tokens that
**actually apply** — not what the source CSS declares.

## Palette (by usage frequency)
| Hex | Uses | Roles | Inferred Role |
|---|---|---|---|
`;
for (const c of colors.slice(0, 15)) {
  md += `| \`${c.hex}\` | ${c.count} | ${c.roles.join(', ')} | ${c.inferredRole} |\n`;
}

md += `\n## Typography\n`;
const typeGroups = {};
for (const t of Object.values(data.typography)) {
  if (!typeGroups[t.role]) typeGroups[t.role] = [];
  typeGroups[t.role].push(t);
}
for (const [role, entries] of Object.entries(typeGroups).sort()) {
  const top = entries.sort((a, b) => b.count - a.count)[0];
  md += `- **${role}:** ${top.fontFamily} ${top.fontWeight} ${top.fontSize}/${top.lineHeight} (${top.count} instances)\n`;
}

md += `\n## Spacing\n`;
md += `- **Inferred base unit:** ${baseUnit}px\n`;
md += `- **Top values:** ${spacingEntries.slice(0, 10).map(([v, c]) => `${v}px (×${c})`).join(', ')}\n`;

md += `\n## Border radius\n`;
for (const [v, c] of Object.entries(data.borderRadius).sort((a, b) => b[1] - a[1]).slice(0, 8)) {
  md += `- \`${v}\` (×${c})\n`;
}

md += `\n## Shadows\n`;
const shadowEntries = Object.entries(data.shadows).sort((a, b) => b[1] - a[1]).slice(0, 5);
if (shadowEntries.length === 0) {
  md += `- No box-shadows detected\n`;
} else {
  for (const [v, c] of shadowEntries) {
    md += `- \`${v.slice(0, 80)}${v.length > 80 ? '…' : ''}\` (×${c})\n`;
  }
}

md += `\n## Motion / animation\n`;
md += `- **Animation libraries detected:** ${data.motion.libraries.length > 0 ? data.motion.libraries.join(', ') : 'None detected'}\n`;
md += `- **Keyframe animations:** ${data.motion.keyframes.length > 0 ? data.motion.keyframes.map(k => k.name).join(', ') : 'None'}\n`;
md += `- **CSS transitions:** ${data.motion.transitions.length} elements with transitions\n`;
md += `- **CSS animations:** ${data.motion.animations.length} elements with animations\n`;

md += `\n## Reproduction note\n`;
md += `For the website factory: reproduce by shipping the palette (top 3-5 colors), the primary font `;
md += `(self-hosted via \`next/font\`), the spacing base unit (${baseUnit}px), and the motion patterns `;
md += `listed above. Swap \`--color-primary\` for the client's brand color. Pair with the visual-composition `;
md += `capture (screenshots) for layout/hierarchy/art-direction.\n`;

fs.writeFileSync(path.join(outDir, 'design-tokens.md'), md);
console.log('Wrote design-tokens.md');

// ---------------------------------------------------------------------------
// Write motion-inventory.json
// ---------------------------------------------------------------------------

fs.writeFileSync(path.join(outDir, 'motion-inventory.json'), JSON.stringify({
  url: data.meta.url,
  capturedAt: new Date().toISOString(),
  libraries: data.motion.libraries,
  keyframes: data.motion.keyframes,
  transitions: data.motion.transitions,
  animations: data.motion.animations,
}, null, 2));
console.log('Wrote motion-inventory.json');

// ---------------------------------------------------------------------------
// Write component-inventory.json
// ---------------------------------------------------------------------------

fs.writeFileSync(path.join(outDir, 'component-inventory.json'), JSON.stringify({
  url: data.meta.url,
  capturedAt: new Date().toISOString(),
  components: data.components,
}, null, 2));
console.log('Wrote component-inventory.json');

// ---------------------------------------------------------------------------
// Write a11y-snapshot.json
// ---------------------------------------------------------------------------

fs.writeFileSync(path.join(outDir, 'a11y-snapshot.json'), JSON.stringify({
  url: data.meta.url,
  capturedAt: new Date().toISOString(),
  headingHierarchy: data.a11y.headingHierarchy,
  altText: data.a11y.altText,
  contrastPairs: data.a11y.contrastPairs,
}, null, 2));
console.log('Wrote a11y-snapshot.json');

// ---------------------------------------------------------------------------
// Write design-capture-manifest.json (top-level index for downstream consumers)
// ---------------------------------------------------------------------------

const date = new Date().toISOString().slice(0, 10);
fs.writeFileSync(path.join(outDir, 'design-capture-manifest.json'), JSON.stringify({
  capturedAt: new Date().toISOString(),
  engineVersion: '2.1',
  url: data.meta.url,
  title: data.meta.title,
  viewports: ['desktop-1440', 'tablet-768', 'mobile-390'],
  artifacts: {
    designTokens: { json: 'design-tokens.json', md: 'design-tokens.md' },
    screenshots: { manifest: `${date}/screenshot-manifest.json`, dir: `${date}/` },
    motionInventory: 'motion-inventory.json',
    componentInventory: 'component-inventory.json',
    a11ySnapshot: 'a11y-snapshot.json',
  },
  captureConfig: {
    designCapture: true,
    scrollStopsPerPage: 10,
    maxSectionsPerPage: 20,
    tokenExtractionMethod: 'getComputedStyle (live DOM)',
  },
}, null, 2));
console.log('Wrote design-capture-manifest.json');

console.log(`\nDone — ${data.meta.elementCount} visible elements analyzed.`);
console.log(`  Palette: ${colors.length} unique colors`);
console.log(`  Typography: ${Object.keys(data.typography).length} font combinations`);
console.log(`  Transitions: ${data.motion.transitions.length}, Animations: ${data.motion.animations.length}`);
console.log(`  Components: ${data.components.length} detected`);
console.log(`  A11y: ${data.a11y.contrastPairs.length} contrast pairs, ${data.a11y.altText.coveragePercent}% alt-text coverage`);
