---
type: execution-log
status: draft
created: 2026-06-19
updated: 2026-06-19
venture: design-inspiration-system
tags: [execution-log, design-emulation-verify, diff-engine, DI-4]
---

## 2026-06-19 — Implement design-emulation-verify diff engine (DI-4)

**What was built:** Playwright-based diff engine that compares any rendered build against a reference design across three axes (structural, stylistic, pattern-presence) plus a legal-boundary check. Framework-agnostic — works on any build Playwright can render (Next.js, WordPress, static HTML, etc.).

**Decision made:** Removed the original "do not use for WordPress / non-React" restriction. Gate is now "is it renderable + capturable?" — not "is it React."

**Alternatives considered:** (1) Source CSS analysis instead of getComputedStyle — rejected because the hub-and-nav-build lesson proved "present ≠ applying" (a stripped style block passes every CSS-presence check while the rule fails to apply). (2) Puppeteer instead of Playwright — rejected because Playwright is already installed for the site-capture-engine (DI-1 composition).

**Why this approach:** Rendering both sides in a real browser and extracting computed styles is the only reliable way to detect whether styles actually apply. The hub-and-nav-build verification-gate reference file documents this lesson explicitly.

**Reusable for future apps?:** Yes — the diff engine is a general-purpose visual QA tool. Any "does my build match the intended design" check can use it. The three-axis structure (structural, stylistic, pattern) maps to the three pillars of the website-design strategy but is applicable beyond it.

### Artifacts produced

| File | Purpose |
|---|---|
| `scripts/diff_build_vs_reference.mjs` | Playwright-based diff engine (~880 LOC) |
| `references/gap-report-contract.md` | Output contract (markdown + JSON sidecar schema) |
| `SKILL.md` | Flipped spec-only → active v1.0 |
| `scripts/test-build.html` | Test page with 3 deliberate mismatches |

### Proof runs

1. **Injected-mismatch catch:** test-build.html (Arial font, #00ff00 accent, missing FAQ) vs AJ Long Electric — all 3 mismatches caught. 40 gaps, 21 critical. Exit 1.
2. **WordPress proof:** developer.wordpress.org vs AJ Long Electric — engine rendered PHP-based WordPress, extracted computed styles, produced gap report. 51 gaps, 20 critical. Exit 1.
3. **Independent reviewer ran 4 additional tests** on different inputs — all code paths verified (PASS/NEEDS-WORK/fatal).

### Peer review findings (3 minor, all fixed)

1. Font extractor picked up non-font strings (`next/font`, `<details>`) — fixed with non-font token filter.
2. Pattern names had trailing punctuation (`Motion personality:`) — fixed with trailing-punctuation strip.
3. `file://` URLs produced empty hostname → double-dash filenames — fixed with basename fallback.

### Key insight

The pattern extractor initially pulled 38 "patterns" from the dossier because it matched `###` headings across all sections (including "Spacing system", "Border-radius", etc. from section 4). Tightening the extraction to only section 5 ("Patterns worth lifting") reduced to 12 real patterns. Lesson: dossier section boundaries matter for downstream consumption — extractors must be section-aware, not just heading-aware.
