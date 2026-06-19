#!/usr/bin/env node
/**
 * design-emulation-verify — diff engine (v1.0)
 *
 * Compares a rendered BUILD page against a REFERENCE page across three axes
 * (structural, stylistic, pattern-presence) plus a legal-boundary check.
 *
 * Framework-agnostic: works on anything Playwright can render (Next.js,
 * WordPress, static HTML, app webviews).
 *
 * Composes with:
 *   - [DI-1] site-capture-engine  — capture package (design-capture-manifest.json)
 *   - [DI-2] design-fingerprint   — dossier + trait sidecar (comparison baseline)
 *
 * Usage:
 *   node diff_build_vs_reference.mjs \
 *     --build-url  http://localhost:3000 \
 *     --ref-url    https://ajlongelectric.com \
 *     --dossier    path/to/dossier-aj-long-electric.md \
 *     [--composition  path/to/composition.md] \
 *     [--trait-sidecar path/to/_traits-aj-long-electric.yaml] \
 *     [--output     path/to/output-dir] \
 *     [--mode       full|structural-only|stylistic-only|pattern-only] \
 *     [--policy     strict-match|brand-differentiation-allowed|pattern-only-emulation]
 */

import { chromium } from 'playwright';
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'fs';
import { join, basename } from 'path';
import { parseArgs } from 'util';

// ---------------------------------------------------------------------------
// CLI argument parsing
// ---------------------------------------------------------------------------
const { values: args } = parseArgs({
  options: {
    'build-url':      { type: 'string' },
    'ref-url':        { type: 'string' },
    'dossier':        { type: 'string' },
    'composition':    { type: 'string', default: '' },
    'trait-sidecar':  { type: 'string', default: '' },
    'output':         { type: 'string', default: '.' },
    'mode':           { type: 'string', default: 'full' },
    'policy':         { type: 'string', default: 'brand-differentiation-allowed' },
  },
  strict: true,
});

const MODES = ['full', 'structural-only', 'stylistic-only', 'pattern-only'];
const POLICIES = ['strict-match', 'brand-differentiation-allowed', 'pattern-only-emulation'];

if (!args['build-url'] || !args['ref-url'] || !args['dossier']) {
  console.error('Required: --build-url, --ref-url, --dossier');
  process.exit(1);
}
if (!MODES.includes(args['mode'])) {
  console.error(`--mode must be one of: ${MODES.join(', ')}`);
  process.exit(1);
}
if (!POLICIES.includes(args['policy'])) {
  console.error(`--policy must be one of: ${POLICIES.join(', ')}`);
  process.exit(1);
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/** Parse YAML frontmatter from a markdown file (simple parser, no dep). */
function parseFrontmatter(content) {
  const m = content.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!m) return { meta: {}, body: content };
  const meta = {};
  for (const line of m[1].split('\n')) {
    const idx = line.indexOf(':');
    if (idx > 0) meta[line.slice(0, idx).trim()] = line.slice(idx + 1).trim();
  }
  return { meta, body: m[2] };
}

/** Extract palette entries from a dossier (looks for hex color table). */
function extractDossierPalette(body) {
  const palette = [];
  const hexRe = /`(#[0-9a-fA-F]{3,8})`/g;
  let match;
  while ((match = hexRe.exec(body)) !== null) {
    palette.push(match[1].toLowerCase());
  }
  return [...new Set(palette)];
}

/** Extract font families mentioned in the dossier. */
function extractDossierFonts(body) {
  const fonts = new Set();
  // Look for font family mentions in type scale / typography sections
  const fontRe = /\*\*(?:Primary|Secondary|Display|Body|Font)[^*]*\*\*[^`]*`([^`]+)`/gi;
  let m;
  while ((m = fontRe.exec(body)) !== null) fonts.add(m[1]);
  // Also grab font names from common patterns like "Inter", "Roboto", etc.
  const namedRe = /(?:font[- ]?family|typeface|font)\s*[:=]\s*[`"']?([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)/gi;
  while ((m = namedRe.exec(body)) !== null) fonts.add(m[1]);
  // Fallback: look for well-known font names
  const wellKnown = ['Inter', 'Roboto', 'Open Sans', 'Lato', 'Montserrat', 'Poppins',
    'Raleway', 'Oswald', 'Merriweather', 'Playfair Display', 'Source Sans', 'Nunito',
    'Work Sans', 'DM Sans', 'Plus Jakarta Sans', 'Geist', 'system-ui'];
  for (const f of wellKnown) {
    if (body.includes(f)) fonts.add(f);
  }
  // Filter out non-font tokens (HTML tags, markdown artifacts, loader references)
  const nonFontTokens = /^(<[^>]+>|next\/font|details|code|pre|span|div|section|img|href|src|class|style|http)$/i;
  return [...fonts].filter(f => !nonFontTokens.test(f) && f.length > 1);
}

/** Extract "patterns worth lifting/emulating" from dossier or composition doc. */
function extractPatterns(body) {
  const patterns = [];
  const lines = body.split('\n');
  let inLiftSection = false;
  let inSkipSection = false;
  for (const line of lines) {
    // Enter the "patterns worth lifting" section (dossier section 5)
    if (/patterns?\s+worth\s+(lifting|emulating)/i.test(line)) {
      inLiftSection = true;
      inSkipSection = false;
      continue;
    }
    // Enter "patterns to skip" section (dossier section 6) — stop collecting liftable
    if (/patterns?\s+to\s+skip/i.test(line)) {
      inLiftSection = false;
      inSkipSection = true;
      continue;
    }
    // Any ## heading that isn't about patterns ends both sections
    if (/^##\s/.test(line) && !/pattern/i.test(line)) {
      inLiftSection = false;
      inSkipSection = false;
      continue;
    }
    // In composition docs, look for bullet items with bold names
    if (!inLiftSection && !inSkipSection) {
      // Also match bullet items with bold pattern names in composition docs
      const m = line.match(/^[-*\d.]+\s+\*\*([^*]+)\*\*/);
      if (m && /pattern|emulat|lift|implement/i.test(body.slice(Math.max(0, body.indexOf(line) - 200), body.indexOf(line)))) {
        patterns.push(m[1].trim());
      }
      continue;
    }
    if (inLiftSection) {
      // Match ### sub-headers as pattern names (the named patterns in section 5)
      const h = line.match(/^###\s+(?:\d+\.\s*)?(.+)/);
      if (h) patterns.push(h[1].trim().replace(/[:;,.\s]+$/, ''));
    }
    // Skip section patterns are NOT added — they're anti-patterns
  }
  return patterns;
}

/** Normalize a hex color to lowercase 6-digit. */
function normalizeHex(hex) {
  hex = hex.toLowerCase().replace(/^#/, '');
  if (hex.length === 3) hex = hex[0]+hex[0]+hex[1]+hex[1]+hex[2]+hex[2];
  if (hex.length === 8) hex = hex.slice(0, 6); // strip alpha
  return '#' + hex;
}

/** Convert rgb/rgba string to hex. */
function rgbToHex(rgb) {
  const m = rgb.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
  if (!m) return null;
  const r = parseInt(m[1]), g = parseInt(m[2]), b = parseInt(m[3]);
  return '#' + [r, g, b].map(v => v.toString(16).padStart(2, '0')).join('');
}

/** Compute color distance (simple Euclidean in RGB space). */
function colorDistance(hex1, hex2) {
  const parse = h => {
    h = h.replace('#', '');
    return [parseInt(h.slice(0,2),16), parseInt(h.slice(2,4),16), parseInt(h.slice(4,6),16)];
  };
  const [r1,g1,b1] = parse(hex1);
  const [r2,g2,b2] = parse(hex2);
  return Math.sqrt((r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2);
}

/** Classify gap severity for a stylistic diff. */
function styleSeverity(property, refVal, buildVal) {
  if (property === 'color' || property === 'backgroundColor') {
    const rh = rgbToHex(refVal), bh = rgbToHex(buildVal);
    if (!rh || !bh) return 'moderate';
    const dist = colorDistance(rh, bh);
    if (dist > 100) return 'critical';
    if (dist > 30) return 'moderate';
    return 'minor';
  }
  if (property === 'fontFamily') {
    const rf = refVal.split(',')[0].replace(/['"]/g, '').trim().toLowerCase();
    const bf = buildVal.split(',')[0].replace(/['"]/g, '').trim().toLowerCase();
    return rf === bf ? 'minor' : 'critical';
  }
  if (property === 'fontSize' || property === 'lineHeight') {
    const rv = parseFloat(refVal), bv = parseFloat(buildVal);
    if (isNaN(rv) || isNaN(bv)) return 'moderate';
    const diff = Math.abs(rv - bv);
    if (diff > 4) return 'moderate';
    if (diff > 2) return 'minor';
    return 'minor';
  }
  return 'moderate';
}

// ---------------------------------------------------------------------------
// Page extraction (runs inside Playwright browser context)
// ---------------------------------------------------------------------------

/** Extract DOM structure + computed styles from a rendered page. */
async function extractPageData(page) {
  return page.evaluate(() => {
    // --- Structural: section tree ---
    const sections = [];
    const sectionEls = document.querySelectorAll(
      'header, nav, main, section, article, aside, footer, [role="banner"], [role="navigation"], [role="main"], [role="contentinfo"]'
    );
    sectionEls.forEach((el, i) => {
      const tag = el.tagName.toLowerCase();
      const role = el.getAttribute('role') || '';
      const cls = el.className ? (typeof el.className === 'string' ? el.className : '') : '';
      const id = el.id || '';
      const depth = (() => {
        let d = 0, p = el.parentElement;
        while (p) { d++; p = p.parentElement; }
        return d;
      })();
      const childSections = el.querySelectorAll('section, article, aside').length;
      const headings = [...el.querySelectorAll('h1, h2, h3, h4, h5, h6')]
        .slice(0, 3)
        .map(h => ({ level: parseInt(h.tagName[1]), text: h.textContent.trim().slice(0, 80) }));
      sections.push({ index: i, tag, role, className: cls.slice(0, 100), id, depth, childSections, headings });
    });

    // --- Stylistic: computed styles on key elements ---
    const styleProbes = {};
    const probeSelectors = {
      body: 'body',
      h1: 'h1',
      h2: 'h2',
      h3: 'h3',
      bodyText: 'main p, article p, .content p, p',
      primaryNav: 'nav, [role="navigation"]',
      hero: 'section:first-of-type, [class*="hero"], header + section, header + div',
      cta: 'a[class*="btn"], a[class*="button"], button[class*="btn"], button[class*="cta"], .cta a, a[class*="cta"]',
      card: '[class*="card"], [class*="grid"] > div, [class*="grid"] > article',
      footer: 'footer, [role="contentinfo"]',
    };
    const styleProps = [
      'fontFamily', 'fontSize', 'fontWeight', 'lineHeight', 'letterSpacing',
      'color', 'backgroundColor', 'backgroundImage',
      'padding', 'margin', 'borderRadius', 'boxShadow',
      'display', 'gap',
    ];
    for (const [name, selector] of Object.entries(probeSelectors)) {
      const el = document.querySelector(selector);
      if (!el) { styleProbes[name] = null; continue; }
      const cs = getComputedStyle(el);
      const styles = {};
      for (const prop of styleProps) {
        styles[prop] = cs[prop] || '';
      }
      styleProbes[name] = { selector, styles };
    }

    // --- Text content for legal-boundary check ---
    const textBlocks = [];
    const textEls = document.querySelectorAll('p, h1, h2, h3, h4, h5, h6, li, span, a, td, th, blockquote');
    const seen = new Set();
    textEls.forEach(el => {
      // Only direct text, skip deeply nested
      const text = el.textContent.trim();
      if (text.length > 20 && text.length < 2000 && !seen.has(text)) {
        seen.add(text);
        textBlocks.push(text.slice(0, 500));
      }
    });

    // --- Image URLs ---
    const imageUrls = [...document.querySelectorAll('img')]
      .map(img => img.src)
      .filter(Boolean);

    // --- All colors used (for palette comparison) ---
    const usedColors = new Set();
    const allEls = document.querySelectorAll('*');
    const sampleSize = Math.min(allEls.length, 200);
    for (let i = 0; i < sampleSize; i++) {
      const idx = Math.floor(i * allEls.length / sampleSize);
      const cs = getComputedStyle(allEls[idx]);
      if (cs.color) usedColors.add(cs.color);
      if (cs.backgroundColor && cs.backgroundColor !== 'rgba(0, 0, 0, 0)') {
        usedColors.add(cs.backgroundColor);
      }
    }

    return {
      title: document.title,
      sections,
      styleProbes,
      textBlocks: textBlocks.slice(0, 100),
      imageUrls: imageUrls.slice(0, 50),
      usedColors: [...usedColors],
    };
  });
}

// ---------------------------------------------------------------------------
// Diff functions
// ---------------------------------------------------------------------------

function diffStructural(refData, buildData) {
  const gaps = [];

  // Compare section counts
  const refSections = refData.sections;
  const buildSections = buildData.sections;

  if (refSections.length !== buildSections.length) {
    const severity = Math.abs(refSections.length - buildSections.length) > 2 ? 'critical' : 'moderate';
    gaps.push({
      description: `Section count mismatch: reference has ${refSections.length} semantic sections, build has ${buildSections.length}`,
      severity,
      refValue: `${refSections.length} sections`,
      buildValue: `${buildSections.length} sections`,
      fix: refSections.length > buildSections.length
        ? `Add ${refSections.length - buildSections.length} missing section(s) to match reference structure`
        : `Build has ${buildSections.length - refSections.length} extra section(s) vs reference`,
    });
  }

  // Compare section order by tag type
  const refTags = refSections.map(s => s.tag);
  const buildTags = buildSections.map(s => s.tag);

  // Find missing section types
  const refTagCounts = {};
  const buildTagCounts = {};
  refTags.forEach(t => refTagCounts[t] = (refTagCounts[t] || 0) + 1);
  buildTags.forEach(t => buildTagCounts[t] = (buildTagCounts[t] || 0) + 1);

  for (const [tag, count] of Object.entries(refTagCounts)) {
    const buildCount = buildTagCounts[tag] || 0;
    if (buildCount < count) {
      gaps.push({
        description: `Missing <${tag}> elements: reference has ${count}, build has ${buildCount}`,
        severity: tag === 'section' || tag === 'main' ? 'critical' : 'moderate',
        refValue: `${count} <${tag}>`,
        buildValue: `${buildCount} <${tag}>`,
        fix: `Add ${count - buildCount} <${tag}> element(s) to match reference`,
      });
    }
  }

  // Compare heading structure
  const refHeadings = refSections.flatMap(s => s.headings);
  const buildHeadings = buildSections.flatMap(s => s.headings);

  if (refHeadings.length > 0 && buildHeadings.length === 0) {
    gaps.push({
      description: 'Build has no headings in semantic sections; reference has headings',
      severity: 'critical',
      refValue: `${refHeadings.length} headings`,
      buildValue: '0 headings',
      fix: 'Add heading hierarchy (h1-h6) to build sections',
    });
  }

  // Check heading level distribution
  const refH1Count = refHeadings.filter(h => h.level === 1).length;
  const buildH1Count = buildHeadings.filter(h => h.level === 1).length;
  if (refH1Count > 0 && buildH1Count === 0) {
    gaps.push({
      description: 'Build is missing an H1 (reference has one)',
      severity: 'critical',
      refValue: `${refH1Count} H1(s)`,
      buildValue: '0 H1s',
      fix: 'Add an H1 heading to the build page',
    });
  }

  return gaps;
}

function diffStylistic(refData, buildData, dossierPalette, dossierFonts, policy) {
  const gaps = [];
  const probeNames = Object.keys(refData.styleProbes);

  for (const probeName of probeNames) {
    const refProbe = refData.styleProbes[probeName];
    const buildProbe = buildData.styleProbes[probeName];

    if (!refProbe || !buildProbe) {
      if (refProbe && !buildProbe) {
        gaps.push({
          description: `Element "${probeName}" (${refProbe.selector}) exists in reference but not found in build`,
          element: probeName,
          severity: 'moderate',
          refValue: 'present',
          buildValue: 'not found',
          withinPolicy: false,
          fix: `Add a matching "${probeName}" element to the build`,
        });
      }
      continue;
    }

    // Compare key style properties
    const importantProps = ['fontFamily', 'fontSize', 'fontWeight', 'color',
      'backgroundColor', 'borderRadius', 'lineHeight'];

    for (const prop of importantProps) {
      const refVal = refProbe.styles[prop];
      const buildVal = buildProbe.styles[prop];

      if (!refVal || !buildVal || refVal === buildVal) continue;

      const severity = styleSeverity(prop, refVal, buildVal);

      // Apply policy
      let withinPolicy = false;
      if (policy === 'pattern-only-emulation') {
        withinPolicy = true; // all stylistic diffs allowed
      } else if (policy === 'brand-differentiation-allowed') {
        // Color and font-family diffs are allowed if they're "brand choices"
        if (prop === 'color' || prop === 'backgroundColor' || prop === 'fontFamily') {
          withinPolicy = true;
        }
      }
      // strict-match: nothing is within policy

      gaps.push({
        description: `${probeName} ${prop}: reference="${refVal}" vs build="${buildVal}"`,
        element: probeName,
        property: prop,
        severity,
        refValue: refVal,
        buildValue: buildVal,
        withinPolicy,
        fix: withinPolicy
          ? `Intentional or allowed under ${policy} policy`
          : `Update ${probeName} ${prop} to match reference: ${refVal}`,
      });
    }
  }

  // Check build colors against dossier palette
  if (dossierPalette.length > 0) {
    const buildHexColors = buildData.usedColors
      .map(c => rgbToHex(c))
      .filter(Boolean)
      .map(h => normalizeHex(h));

    const offPalette = [];
    for (const buildColor of buildHexColors) {
      const onPalette = dossierPalette.some(dp => colorDistance(normalizeHex(dp), buildColor) < 30);
      // Skip near-black, near-white, transparent-like
      const isNeutral = colorDistance(buildColor, '#000000') < 20 ||
                        colorDistance(buildColor, '#ffffff') < 20;
      if (!onPalette && !isNeutral) {
        offPalette.push(buildColor);
      }
    }

    if (offPalette.length > 0) {
      const withinPolicy = args['policy'] !== 'strict-match';
      gaps.push({
        description: `${offPalette.length} color(s) in build not on reference palette: ${offPalette.slice(0, 5).join(', ')}${offPalette.length > 5 ? '...' : ''}`,
        element: 'global',
        property: 'palette',
        severity: offPalette.length > 3 ? 'moderate' : 'minor',
        refValue: `Palette: ${dossierPalette.join(', ')}`,
        buildValue: `Off-palette: ${offPalette.slice(0, 5).join(', ')}`,
        withinPolicy,
        fix: withinPolicy
          ? 'Review off-palette colors — may be intentional brand differentiation'
          : `Replace off-palette colors with reference palette values`,
      });
    }
  }

  // Check fonts against dossier
  if (dossierFonts.length > 0) {
    const buildFonts = new Set();
    for (const probe of Object.values(buildData.styleProbes)) {
      if (probe?.styles?.fontFamily) {
        const primary = probe.styles.fontFamily.split(',')[0].replace(/['"]/g, '').trim();
        buildFonts.add(primary);
      }
    }
    for (const bf of buildFonts) {
      const matchesDossier = dossierFonts.some(df =>
        df.toLowerCase() === bf.toLowerCase() ||
        bf.toLowerCase().includes(df.toLowerCase())
      );
      if (!matchesDossier && bf !== 'serif' && bf !== 'sans-serif' && bf !== 'monospace') {
        const withinPolicy = args['policy'] !== 'strict-match';
        gaps.push({
          description: `Build uses font "${bf}" not found in reference dossier fonts (${dossierFonts.join(', ')})`,
          element: 'global',
          property: 'fontFamily',
          severity: 'moderate',
          refValue: dossierFonts.join(', '),
          buildValue: bf,
          withinPolicy,
          fix: withinPolicy
            ? `Font "${bf}" may be a brand choice`
            : `Switch to reference font: ${dossierFonts[0]}`,
        });
      }
    }
  }

  return gaps;
}

function diffPatternPresence(buildData, expectedPatterns) {
  const gaps = [];
  if (expectedPatterns.length === 0) return gaps;

  // Pattern detection heuristics based on DOM structure
  const buildSections = buildData.sections;
  const buildHeadings = buildSections.flatMap(s => s.headings);
  const headingTexts = buildHeadings.map(h => h.text.toLowerCase());
  const classNames = buildSections.map(s => s.className.toLowerCase()).join(' ');
  const probeKeys = Object.keys(buildData.styleProbes);

  for (const pattern of expectedPatterns) {
    const pl = pattern.toLowerCase();
    let status = 'missing';
    let notes = '';

    // Check if pattern name (or keywords from it) appears in headings, classes, or probes
    const keywords = pl.split(/[\s-]+/).filter(w => w.length > 3);

    const inHeadings = keywords.some(kw => headingTexts.some(ht => ht.includes(kw)));
    const inClasses = keywords.some(kw => classNames.includes(kw));
    const inProbes = keywords.some(kw => probeKeys.some(pk => pk.toLowerCase().includes(kw)));

    // Common pattern type detection
    if (pl.includes('hero')) {
      const hasHero = buildData.styleProbes.hero !== null ||
        buildSections.some(s => s.className.toLowerCase().includes('hero'));
      status = hasHero ? 'present-correctly' : 'missing';
      if (hasHero) notes = 'Hero section detected in build';
    } else if (pl.includes('faq')) {
      const hasFAQ = classNames.includes('faq') || headingTexts.some(h => h.includes('faq') || h.includes('question'));
      status = hasFAQ ? 'present-correctly' : 'missing';
    } else if (pl.includes('testimonial') || pl.includes('review')) {
      const hasTesti = classNames.includes('testimon') || classNames.includes('review') ||
        headingTexts.some(h => h.includes('review') || h.includes('testimonial'));
      status = hasTesti ? 'present-correctly' : 'missing';
    } else if (pl.includes('cta') || pl.includes('call to action') || pl.includes('call-to-action')) {
      status = buildData.styleProbes.cta !== null ? 'present-correctly' : 'missing';
    } else if (pl.includes('card') || pl.includes('grid')) {
      status = buildData.styleProbes.card !== null ? 'present-correctly' : 'missing';
    } else if (pl.includes('nav')) {
      status = buildData.styleProbes.primaryNav !== null ? 'present-correctly' : 'missing';
    } else if (pl.includes('footer')) {
      status = buildData.styleProbes.footer !== null ? 'present-correctly' : 'missing';
    } else if (inHeadings || inClasses || inProbes) {
      status = 'present-correctly';
      notes = 'Keyword match in headings/classes';
    }

    if (status !== 'present-correctly') {
      gaps.push({
        pattern,
        status,
        severity: status === 'missing' ? 'critical' : 'moderate',
        notes: notes || `Pattern "${pattern}" not detected in build DOM`,
        fix: `Implement the "${pattern}" pattern as specified in the composition doc`,
      });
    }
  }

  return gaps;
}

function checkLegalBoundary(refData, buildData) {
  const findings = [];

  // Text overlap: find exact matches > 20 words
  for (const refText of refData.textBlocks) {
    const refWords = refText.split(/\s+/);
    if (refWords.length < 20) continue;

    for (const buildText of buildData.textBlocks) {
      // Check for substantial overlap
      const refLower = refText.toLowerCase();
      const buildLower = buildText.toLowerCase();

      // Sliding window of 20 words
      for (let i = 0; i <= refWords.length - 20; i++) {
        const window = refWords.slice(i, i + 20).join(' ').toLowerCase();
        if (buildLower.includes(window)) {
          findings.push({
            type: 'text-overlap',
            severity: 'critical',
            description: `Verbatim text match (20+ words): "${window.slice(0, 100)}..."`,
            refSource: refText.slice(0, 100),
            buildLocation: buildText.slice(0, 100),
          });
          break;
        }
      }
    }
  }

  // Deduplicate text findings
  const seenTexts = new Set();
  const dedupedTextFindings = findings.filter(f => {
    const key = f.description.slice(0, 80);
    if (seenTexts.has(key)) return false;
    seenTexts.add(key);
    return true;
  });

  // Image URL carryover
  const refImages = new Set(refData.imageUrls.map(u => {
    try { return new URL(u).pathname; } catch { return u; }
  }));

  for (const buildImg of buildData.imageUrls) {
    let buildPath;
    try { buildPath = new URL(buildImg).pathname; } catch { buildPath = buildImg; }
    if (refImages.has(buildPath)) {
      dedupedTextFindings.push({
        type: 'image-carryover',
        severity: 'critical',
        description: `Image URL from reference found in build: ${buildPath}`,
        refSource: buildPath,
        buildLocation: buildImg,
      });
    }
  }

  return dedupedTextFindings;
}

// ---------------------------------------------------------------------------
// Report generation
// ---------------------------------------------------------------------------

function generateGapReport(opts) {
  const { buildUrl, refUrl, mode, policy, structural, stylistic, patterns, legal, timestamp } = opts;

  const totalGaps = structural.length + stylistic.length + patterns.length;
  const criticalGaps = [...structural, ...stylistic, ...patterns]
    .filter(g => g.severity === 'critical').length;

  // Determine verdicts per axis
  const structuralVerdict = structural.filter(g => g.severity === 'critical').length === 0 ? 'PASS' : 'NEEDS-WORK';
  const stylisticVerdict = stylistic.filter(g => g.severity === 'critical' && !g.withinPolicy).length === 0 ? 'PASS' : 'NEEDS-WORK';
  const patternVerdict = patterns.filter(g => g.status === 'missing').length === 0 ? 'PASS' : 'NEEDS-WORK';
  const legalVerdict = legal.length === 0 ? 'PASS' : 'NEEDS-WORK';

  const overall = (structuralVerdict === 'PASS' && stylisticVerdict === 'PASS' &&
    patternVerdict === 'PASS' && legalVerdict === 'PASS') ? 'PASS' : 'NEEDS-WORK';

  let md = `---
type: verify-report
status: generated
created: ${timestamp.split('T')[0]}
build-url: "${buildUrl}"
ref-url: "${refUrl}"
mode: ${mode}
policy: ${policy}
verdict: ${overall}
tags: [verify-report, design-emulation-verify]
---

# Design Emulation Verify — Gap Report

## 1. Summary

| Field | Value |
|---|---|
| Reference URL | ${refUrl} |
| Build URL | ${buildUrl} |
| Mode | ${mode} |
| Policy | ${policy} |
| Generated | ${timestamp} |

### Verdict

| Axis | Verdict | Gaps |
|---|---|---|
| Structural | **${structuralVerdict}** | ${structural.length} |
| Stylistic | **${stylisticVerdict}** | ${stylistic.length} |
| Pattern presence | **${patternVerdict}** | ${patterns.length} |
| Legal boundary | **${legalVerdict}** | ${legal.length} |
| **Overall** | **${overall}** | **${totalGaps}** (${criticalGaps} critical) |

`;

  // Section 2: Structural
  if (mode === 'full' || mode === 'structural-only') {
    md += `## 2. Structural gaps\n\n`;
    if (structural.length === 0) {
      md += `No structural gaps detected.\n\n`;
    } else {
      for (const gap of structural) {
        md += `### ${gap.severity.toUpperCase()}: ${gap.description}\n\n`;
        md += `- **Reference:** ${gap.refValue}\n`;
        md += `- **Build:** ${gap.buildValue}\n`;
        md += `- **Fix:** ${gap.fix}\n\n`;
      }
    }
  }

  // Section 3: Stylistic
  if (mode === 'full' || mode === 'stylistic-only') {
    md += `## 3. Stylistic gaps\n\n`;
    if (stylistic.length === 0) {
      md += `No stylistic gaps detected.\n\n`;
    } else {
      for (const gap of stylistic) {
        md += `### ${gap.severity.toUpperCase()}: ${gap.description}\n\n`;
        md += `- **Element:** ${gap.element}\n`;
        if (gap.property) md += `- **Property:** ${gap.property}\n`;
        md += `- **Reference:** ${gap.refValue}\n`;
        md += `- **Build:** ${gap.buildValue}\n`;
        md += `- **Within policy:** ${gap.withinPolicy ? 'yes' : 'no'}\n`;
        md += `- **Fix:** ${gap.fix}\n\n`;
      }
    }
  }

  // Section 4: Pattern presence
  if (mode === 'full' || mode === 'pattern-only') {
    md += `## 4. Pattern presence gaps\n\n`;
    if (patterns.length === 0) {
      md += `No pattern gaps detected (all expected patterns present).\n\n`;
    } else {
      for (const gap of patterns) {
        md += `### ${gap.severity.toUpperCase()}: ${gap.pattern}\n\n`;
        md += `- **Status:** ${gap.status}\n`;
        md += `- **Notes:** ${gap.notes}\n`;
        md += `- **Fix:** ${gap.fix}\n\n`;
      }
    }
  }

  // Section 5: Legal boundary
  md += `## 5. Legal boundary check\n\n`;
  if (legal.length === 0) {
    md += `No asset/copy carryover detected. Emulation copies patterns, not assets.\n\n`;
  } else {
    for (const finding of legal) {
      md += `### ${finding.severity.toUpperCase()}: ${finding.type}\n\n`;
      md += `- **Description:** ${finding.description}\n`;
      md += `- **Reference source:** ${finding.refSource}\n`;
      md += `- **Build location:** ${finding.buildLocation}\n\n`;
    }
  }

  return { md, json: {
    version: '1.0',
    timestamp,
    buildUrl, refUrl, mode, policy,
    verdict: { overall, structural: structuralVerdict, stylistic: stylisticVerdict, pattern: patternVerdict, legal: legalVerdict },
    gaps: { structural, stylistic, patterns, legal },
    totals: { structural: structural.length, stylistic: stylistic.length, patterns: patterns.length, legal: legal.length, total: totalGaps, critical: criticalGaps },
  }};
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function main() {
  const buildUrl = args['build-url'];
  const refUrl = args['ref-url'];
  const mode = args['mode'];
  const policy = args['policy'];
  const outputDir = args['output'];
  const timestamp = new Date().toISOString();

  // Load dossier
  console.log(`Loading dossier: ${args['dossier']}`);
  const dossierContent = readFileSync(args['dossier'], 'utf-8');
  const { body: dossierBody } = parseFrontmatter(dossierContent);
  const dossierPalette = extractDossierPalette(dossierBody);
  const dossierFonts = extractDossierFonts(dossierBody);
  console.log(`  Palette: ${dossierPalette.length} colors`);
  console.log(`  Fonts: ${dossierFonts.join(', ') || 'none detected'}`);

  // Load composition doc (optional)
  let expectedPatterns = [];
  if (args['composition']) {
    console.log(`Loading composition doc: ${args['composition']}`);
    const compContent = readFileSync(args['composition'], 'utf-8');
    expectedPatterns = extractPatterns(compContent);
    console.log(`  Expected patterns: ${expectedPatterns.length}`);
  } else {
    // Fall back to dossier's "patterns worth lifting" section
    expectedPatterns = extractPatterns(dossierBody);
    console.log(`  Patterns from dossier: ${expectedPatterns.length}`);
  }

  // Launch browser
  console.log('\nLaunching Playwright...');
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  });

  let refData, buildData;

  try {
    // Render reference page
    console.log(`\nRendering reference: ${refUrl}`);
    const refPage = await context.newPage();
    await refPage.goto(refUrl, { waitUntil: 'networkidle', timeout: 30000 });
    await refPage.waitForTimeout(2000); // let JS finish
    refData = await extractPageData(refPage);
    console.log(`  Sections: ${refData.sections.length}, Text blocks: ${refData.textBlocks.length}, Colors: ${refData.usedColors.length}`);
    await refPage.close();

    // Render build page
    console.log(`Rendering build: ${buildUrl}`);
    const buildPage = await context.newPage();
    await buildPage.goto(buildUrl, { waitUntil: 'networkidle', timeout: 30000 });
    await buildPage.waitForTimeout(2000);
    buildData = await extractPageData(buildPage);
    console.log(`  Sections: ${buildData.sections.length}, Text blocks: ${buildData.textBlocks.length}, Colors: ${buildData.usedColors.length}`);
    await buildPage.close();
  } finally {
    await browser.close();
  }

  // Run diffs
  console.log('\nRunning diffs...');
  const structural = (mode === 'full' || mode === 'structural-only') ? diffStructural(refData, buildData) : [];
  const stylistic = (mode === 'full' || mode === 'stylistic-only') ? diffStylistic(refData, buildData, dossierPalette, dossierFonts, policy) : [];
  const patterns = (mode === 'full' || mode === 'pattern-only') ? diffPatternPresence(buildData, expectedPatterns) : [];
  const legal = checkLegalBoundary(refData, buildData);

  console.log(`  Structural gaps: ${structural.length}`);
  console.log(`  Stylistic gaps: ${stylistic.length}`);
  console.log(`  Pattern gaps: ${patterns.length}`);
  console.log(`  Legal findings: ${legal.length}`);

  // Generate report
  const { md, json } = generateGapReport({
    buildUrl, refUrl, mode, policy, structural, stylistic, patterns, legal, timestamp,
  });

  // Write output
  if (!existsSync(outputDir)) mkdirSync(outputDir, { recursive: true });

  const parsedUrl = new URL(buildUrl);
  const rawSlug = parsedUrl.hostname || basename(parsedUrl.pathname, '.html') || 'local-build';
  const slug = rawSlug.replace(/[^a-z0-9]/gi, '-').toLowerCase();
  const dateSlug = timestamp.split('T')[0];
  const mdPath = join(outputDir, `verify-${slug}-${dateSlug}.md`);
  const jsonPath = join(outputDir, `verify-${slug}-${dateSlug}.json`);

  writeFileSync(mdPath, md);
  writeFileSync(jsonPath, JSON.stringify(json, null, 2));

  console.log(`\n--- VERDICT: ${json.verdict.overall} ---`);
  console.log(`Gap report: ${mdPath}`);
  console.log(`JSON sidecar: ${jsonPath}`);
  console.log(`Total gaps: ${json.totals.total} (${json.totals.critical} critical)`);

  // Exit with non-zero if NEEDS-WORK
  process.exit(json.verdict.overall === 'PASS' ? 0 : 1);
}

main().catch(err => {
  console.error('Fatal error:', err.message);
  process.exit(2);
});
