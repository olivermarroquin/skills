---
type: reference
status: active
created: 2026-06-23
updated: 2026-06-23
skill: reference-finder
tags: [reference, vetting-rubric, reference-finder, quality-gate, design-inspiration-system]
---

# Vetting rubric — reference-finder v1.0

The quality gate between discovery and the candidates registry. Every candidate clears this
pipeline before entering the registry — no unvetted dumps. Rejects are logged with reasons
in the rejection log, not silently dropped.

---

## Step 1 — Dedup check

**Before any vetting work,** grep three stores for the candidate's domain:

| Store | Path (website-design profile) | What to grep |
|---|---|---|
| Library (high-performing) | `inspiration/high-performing/` | Domain in frontmatter `domain:` or filename |
| Library (design-only) | `inspiration/design-only/` | Domain in frontmatter `domain:` or filename |
| Candidates registry | `inspiration/candidates-registry.md` | Domain column |
| Ingestion queue | `insights/_ingestion-queue.md` | URL in queue entries |

**If found:**
- `in-library` → "Already in library at [path]. Skip." (unless operator wants to re-evaluate)
- `queued` or `ingested` → "Already queued/in-progress at registry row [N]. Skip."
- `candidate` → "Already a candidate. Update with new provenance? Or skip?"
- In rejection log → "Previously rejected on [date]: [reason]. Re-evaluate? Or skip?"

**Never silently re-surface** what's already tracked. Surface the match and let the operator
decide.

---

## Step 2 — Automated pre-screen

Run these checks in parallel where possible. Each produces a score or flag.

### 2a. Accessibility check

Before investing in capture + fingerprint, verify the site is reachable:

- HTTP GET the domain → must return 200 (follow redirects).
- If 4xx/5xx or timeout → `reject` with reason "Site unreachable ([status code])."
- If behind a login wall (detected by redirect to `/login` or similar) → `reject` with reason
  "Auth-walled — not publicly accessible."

### 2b. Lightweight capture

Invoke `site-capture-engine` in quick mode (homepage only, desktop viewport, fold screenshot +
basic design tokens). This is NOT the full `--design-capture` package — just enough for the
fingerprint to produce a design-quality score.

**Output:** Fold screenshot + `design-tokens.json` (palette, typography, spacing basics).

**Time:** ~10-15 seconds per site.

### 2c. Light fingerprint → design-quality score

Invoke `design-fingerprint` with `depth: light` on the quick capture output.

**Output:** `inspiration-<slug>.md` (light note) + `_traits-<slug>.yaml` (trait sidecar).

From the fingerprint output, derive a **design-quality score (1-10)**:

| Score | Meaning | Typical traits |
|---|---|---|
| 9-10 | Exceptional — portfolio/award-level | Deliberate palette, custom typography, meaningful motion, strong hierarchy |
| 7-8 | Strong — worth lifting patterns from | Good palette, readable typography, some motion/interaction, clear layout |
| 5-6 | Adequate — functional but unremarkable | Template-ish, stock imagery, minimal custom design |
| 3-4 | Below bar — obvious template or dated | Default theme, poor typography choices, no motion |
| 1-2 | Poor — broken or actively ugly | Layout issues, clashing colors, readability problems |

**Scoring inputs from the trait sidecar:**

- `palette.strategy` — `custom-coherent` or `limited-focused` → +2; `default-framework` → 0
- `typography.primary_classification` — non-system font → +1; system-only → 0
- `motion.personality` — `expressive` or `subtle-functional` → +1; `none` → 0
- `layout.grid_strategy` — `custom` or `asymmetric` → +1; `single-column-basic` → 0
- `overall_archetype` — recognized sophisticated archetype → +1
- Subtract 1 for each: poor contrast (a11y), missing alt text >50%, broken layout indicators

**Time:** ~30 seconds per site (mostly model analysis time).

### 2d. CWV performance check

Query PageSpeed Insights API for the candidate's homepage:

```
https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy=mobile&category=performance
```

**Output:** LCP, CLS, INP scores + overall assessment (Good / Needs Improvement / Poor).

**Classification mapping:**

| CWV assessment | Performance score |
|---|---|
| All three Good (LCP < 2.5s, CLS < 0.1, INP < 200ms) | 9-10 |
| Two Good, one Needs Improvement | 7-8 |
| Mixed or all Needs Improvement | 5-6 |
| Any Poor | 3-4 |
| Multiple Poor or site fails to load | 1-2 |

**Cost:** Free (PageSpeed Insights API has generous rate limits).

**Time:** ~5-10 seconds per site.

### 2e. Visibility check (performance-led candidates only)

For candidates from Lane 1 (performance-led), the visibility data comes from the
`competitor-deep-research` Tier-2 scan that sourced them — no additional API call needed.

For candidates from other lanes that are being evaluated for high-performing classification,
run a DataForSEO `ranked_keywords` query:

- Estimated organic keywords
- Estimated monthly organic traffic
- Top-ranking keywords (first 5)

**Cost:** ~$0.01-0.02 per domain.

**Skip if:** Candidate is clearly design-only (no performance claim) or DataForSEO budget is
constrained. Note "visibility not checked" in the evidence card.

---

## Step 3 — Classification

Apply the library's inclusion bars (from the `reference-library` config profile) to classify
each candidate.

### High-performing candidate

ALL four bars must be met:

| Bar | Threshold | Evidence source |
|---|---|---|
| 1. Rankings / visibility | Top-5 organic for high-intent queries in its sector, OR estimated organic keywords ≥ 100, OR strong AI-citation presence | Lane 1 SERP data or Step 2e visibility check |
| 2. Core Web Vitals | Overall "Good" range (LCP < 2.5s, CLS < 0.1, INP < 200ms) — all three | Step 2d CWV check |
| 3. Content depth | Visible service pages + location pages + FAQ or similar structured content + schema markup present | Quick capture observation |
| 4. Design quality | Score ≥ 7/10 from light fingerprint | Step 2c design-quality score |

**If all four pass:** classify as `high-performing-candidate` → registry lane: `high-performing`.

### Design-only candidate

The visual-quality bar only:

| Bar | Threshold | Evidence source |
|---|---|---|
| Design quality | Score ≥ 7/10 from light fingerprint | Step 2c design-quality score |

Performance bars (1-3) are not required. A beautiful site with poor SEO or unknown performance
is still valuable as a design reference.

**If design bar passes but performance bars fail or are unchecked:** classify as
`design-only-candidate` → registry lane: `design-only`.

### Reject

| Condition | Action |
|---|---|
| Design-quality score < 7/10 | Reject — below the visual bar |
| Site unreachable (Step 2a failed) | Reject — can't evaluate |
| Auth-walled | Reject — not publicly accessible |
| Obvious template / page builder default | Reject — no patterns worth lifting |

**All rejects are logged** in the rejection log with: domain, date, lane, reason, scores.
Never silently dropped.

---

## Step 4 — Composite ranking

Rank surviving candidates by composite score:

```
composite = (design_quality × 0.4) + (performance × 0.3) + (novelty × 0.2) + (taste_fit × 0.1)
```

### Component scores (all normalized to 0-10)

**design_quality (weight 0.4):** Direct from Step 2c. The dominant factor.

**performance (weight 0.3):** From Step 2d CWV + Step 2e visibility. If visibility not checked,
use CWV score alone (rescaled). If CWV not checked (design-only candidates), this component
scores 5/10 (neutral — unknown, not penalized).

**novelty (weight 0.2):** Derived from the sector coverage map.

| Library coverage for this sector | Novelty score |
|---|---|
| 0 entries (new sector) | 10 |
| 1-2 entries | 8 |
| 3-5 entries | 5 |
| 6+ entries | 3 |

Also boosted (+2, capped at 10) if the candidate's `archetype` trait is not yet represented
in the library.

**taste_fit (weight 0.1):** From the taste profile.

| Match | Score |
|---|---|
| ≥2 boosted traits present | 9-10 |
| 1 boosted trait present | 7-8 |
| No boost or penalize matches | 5 (neutral) |
| 1 penalized trait present | 3-4 |
| ≥2 penalized traits present | 1-2 |

### Multi-lane bonus

Candidates discovered by 2+ independent lanes get a +1 bonus to composite score (capped at 10).
Cross-lane confirmation is strong signal.

### Shortlist cap

Default: 10 candidates per run. Configurable per profile. Present in descending composite
score order.

---

## Step 5 — Operator triage

Surface the ranked shortlist with per-candidate evidence cards (format in SKILL.md).

**Operator actions per candidate:**

| Action | Effect |
|---|---|
| **Approve** | Registry status → `vetted`. This skill writes the registry row. The operator (or a subsequent run) moves `vetted→queued` when ready for ingestion. |
| **Reject** | Rejection-log entry written with domain, date, lane, reason, scores, `rejected-by: operator`. |
| **Defer** | Candidate stays `candidate` in registry (if already there) or is noted in the run log for re-evaluation. Not rejected — just not decided yet. |

**Batch triage shortcut:** Operator can say "approve all high-performing, reject all below 7"
or similar batch rules. The skill applies and surfaces any edge cases.

---

## Threshold tuning

All thresholds are in the config profile and can be adjusted per operator feedback:

| Threshold | Default | Where to change |
|---|---|---|
| Design-quality bar | ≥ 7/10 | Profile `inclusion_bars.design_quality_min` |
| CWV assessment bar | All three Good | Profile `inclusion_bars.cwv_min` |
| Visibility bar | ≥ 100 organic keywords | Profile `inclusion_bars.visibility_min_keywords` |
| Shortlist cap | 10 | Profile `shortlist_cap` |
| Ranking weights | 0.4 / 0.3 / 0.2 / 0.1 | Profile `ranking_weights` |

After 3+ runs with operator feedback, review whether thresholds need adjustment. Surface to
operator: "You've rejected 80% of design-quality 7s — raise the bar to 8?"

---

## Related

- [[discovery-lanes]] — the lanes that feed candidates into this rubric
- [[finder-config-profiles]] — threshold values per profile
- [[reference-library]] — the library whose inclusion bars this enforces
- [[_taste-profile]] — biases the ranking step
- [[_rejection-log]] — where rejects land
