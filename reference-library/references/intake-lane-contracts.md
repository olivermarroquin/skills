---
type: reference
status: active
created: 2026-06-18
updated: 2026-06-18
skill: reference-library
tags: [reference, reference-library, intake-lanes, contracts]
---

# Intake lane contracts

> Two lanes, two bars, two output depths. The lane determines the inclusion bar, the upstream
> skill depth, and the output format. Both lanes share the same dedup/queue/review/graduation
> infrastructure — they differ only in what clears the bar and how much detail the output carries.

---

## Lane 1 — High-performing (full dossier)

### Purpose

References verified to excel at BOTH quality AND performance in their domain. These are the
load-bearing references whose patterns get lifted into builds with confidence that the pattern
correlates with real-world success.

### Inclusion bar

All criteria must be met (config-driven per profile — these are the website-design defaults):

1. **Performance evidence** — ranks in the top positions for high-intent queries in its niche,
   or has comparable visibility evidence. Specific evidence cited in the dossier.
2. **Technical quality** — meets the domain's quality threshold (e.g., Core Web Vitals "Good"
   for websites: LCP < 2.5s, CLS < 0.1, INP < 200ms).
3. **Content/depth** — demonstrates depth appropriate to the domain (e.g., service pages,
   location pages, FAQs, schema markup for websites).
4. **Visual/output quality** — at or above the bar we'd be comfortable shipping to a client.

If a reference clears 1 and 3 but flunks 2 or 4 → design-only lane (if visually strong) or
no entry at all.

### Upstream pipeline

```
site-capture-engine --design-capture → design-fingerprint (depth: full) → this lane
```

### Required inputs

- `design-fingerprint` full dossier: `dossier-<slug>.md` (8 sections)
- `design-fingerprint` trait sidecar: `_traits-<slug>.yaml`
- Performance evidence (rankings, CWV, content depth metrics, conversion proxies)

### Output

- **File:** `<high-performing-dir>/dossier-<slug>.md`
- **Sidecar:** `<high-performing-dir>/_traits-<slug>.yaml`
- **Status flow:** `draft` → (operator review) → `verified`
- **Frontmatter:** `type: design-dossier`, `status: verified`, `sector:`, `archetype:`,
  `performance-verified-date:`

### Filing rules

1. Verify all 4 inclusion bars are met with cited evidence. No vibes-based claims.
2. If performance data is incomplete, file as `status: draft` with a note on what's missing.
   Do not stamp `verified` until all bars are cleared.
3. Cross-sector tags (`sector:`, `archetype:`) are mandatory.
4. The legal-boundary section (§7) must be present and non-empty.

---

## Lane 2 — Design-only (swipe file)

### Purpose

References whose visual/output quality is at the bar we want to lift patterns from, regardless
of performance. Often out-of-niche references — a SaaS hero pattern, an architect portfolio's
motion design, a fintech dashboard's information density. The point: capture visual ideas before
they decay from memory.

### Inclusion bar

Single criterion: **visual/output quality at or above the bar we'd ship.** Subjective but real.
Performance is not verified, not relevant, not claimed.

### Upstream pipeline

```
site-capture-engine (lightweight) → design-fingerprint (depth: light) → this lane
```

For the interim path (before full capture tooling is available): screenshots + a hand-written
light note are acceptable. The bar is quality of the captured patterns, not process formality.

### Required inputs

- `design-fingerprint` light note: `inspiration-<slug>.md` (or hand-written equivalent)
- `design-fingerprint` trait sidecar: `_traits-<slug>.yaml` (when available)
- Screenshots (saved alongside the note, or referenced)

### Output

- **File:** `<design-only-dir>/inspiration-<slug>.md`
- **Sidecar:** `<design-only-dir>/_traits-<slug>.yaml` (when available)
- **Status flow:** `draft` → (operator review) → `captured`
- **Frontmatter:** `type: design-inspiration`, `status: captured`, `sector:`, `archetype:`

### Filing rules

1. 2-5 named liftable patterns, each with a `→ catalog/<category>/<slug>` pointer.
2. Visible tooling/libraries noted.
3. One-paragraph "why this matters" — what this reference teaches that isn't already in the catalog.
4. Brevity is correct. A 200-word note with good patterns beats a 2,000-word note.
5. Cross-sector tags are mandatory even for out-of-niche references (use the reference's own
   sector, not the consuming project's sector).

---

## Shared infrastructure (both lanes)

### Dedup

Before filing via either lane:
1. Grep `<library-root>/` for the domain/identifier
2. Grep `<queue-file>` for the domain/identifier
3. If found → surface to operator, do not silently overwrite

### Queue update

On successful filing:
1. Strike through the queue entry
2. Append `→ [[result-slug]]`
3. Update candidates registry status to `in-library` if applicable

### Review gate

- **Training mode (default):** surface the draft for operator approval before promoting status
- **Auto mode:** only on explicit `--review auto` from operator

### Graduation eligibility

Both lanes produce patterns eligible for catalog graduation. The trigger is the same regardless
of lane: used in a real build OR verified via `design-emulation-verify`. The source lane affects
confidence (high-performing patterns have performance correlation; design-only patterns have
visual-quality correlation only) but not graduation eligibility.
