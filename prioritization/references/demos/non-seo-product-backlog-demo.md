---
type: meta
status: demo
created: 2026-06-06
updated: 2026-06-06
profile: ad-hoc
scoring_mode: weighted-sum
criteria_used: [user_impact, implementation_effort, revenue_signal, technical_risk]
tags: [build-order, prioritization, demo, non-seo, agnostic-proof, product-backlog]
---

# Prioritized backlog — resume-saas feature candidates (non-SEO demo)

This is a demonstration output produced by the `prioritization` skill v1.0 using an **ad-hoc profile** with criteria that have zero overlap with SEO, page-building, or client services. It ranks feature candidates for the resume-saas product to prove the engine works on a genuinely non-SEO domain.

## How this list was built

Scoring mode: **weighted-sum** (criteria trade off; high user impact can compensate for high effort).

| Criterion | Weight | Direction | Description | Values |
|---|---|---|---|---|
| `user_impact` | 0.35 | higher-is-better | How much does this feature improve the core user workflow (paste resume → get proposals → export tailored resume)? | 1-5 scale (5 = transformative improvement to the core loop) |
| `implementation_effort` | 0.25 | lower-is-better | Estimated dev-days to ship | numeric (fewer days = higher normalized score) |
| `revenue_signal` | 0.20 | higher-is-better | Does this feature unlock a pricing tier, reduce churn, or increase conversion? | 1-5 scale (5 = directly unlocks paid tier) |
| `technical_risk` | 0.20 | lower-is-better | Likelihood of hitting unknown unknowns, needing architectural changes, or introducing regressions | 1-5 scale (1 = well-understood, 5 = high uncertainty) |

## Candidate set

| ID | Feature | User impact | Effort (days) | Revenue signal | Technical risk |
|---|---|---|---|---|---|
| format-preserve | Format-preserving resume export (upload DOCX/PDF → apply proposals → download with original formatting) | 5 | 14 | 5 | 4 |
| multi-job-batch | Batch-tailor one resume to multiple job descriptions simultaneously | 4 | 5 | 4 | 2 |
| pdf-template-gallery | Gallery of professional PDF export templates (3-5 styles) | 3 | 3 | 3 | 1 |
| proposal-history | Persistent proposal history across sessions (local storage or account) | 3 | 4 | 2 | 2 |
| ats-score | ATS compatibility score for the tailored resume | 4 | 7 | 4 | 3 |
| cover-letter-gen | Generate a matching cover letter from the same resume+JD pair | 4 | 3 | 3 | 1 |
| linkedin-import | Import resume directly from LinkedIn profile URL | 3 | 6 | 2 | 4 |
| section-reorder | Drag-and-drop section reordering in the editor | 2 | 4 | 1 | 3 |

## Sequence

| # | ID | Total score | User impact | Effort | Revenue | Tech risk | Rationale |
|---|---|---|---|---|---|---|---|
| 01 | cover-letter-gen | **0.82** | 4 (0.75 × 0.35 = 0.26) | 3 (0.85 × 0.25 = 0.21) | 3 (0.50 × 0.20 = 0.10) | 1 (1.00 × 0.20 = 0.20) | High impact, lowest effort + risk combo. Natural extension of the core resume+JD pair — users already have the inputs. Quick win. |
| 02 | multi-job-batch | **0.78** | 4 (0.75 × 0.35 = 0.26) | 5 (0.69 × 0.25 = 0.17) | 4 (0.75 × 0.20 = 0.15) | 2 (0.75 × 0.20 = 0.15) | Strong revenue signal (power-user feature = paid tier). Moderate effort, low risk. Directly multiplies the core workflow's value. |
| 03 | pdf-template-gallery | **0.76** | 3 (0.50 × 0.35 = 0.18) | 3 (0.85 × 0.25 = 0.21) | 3 (0.50 × 0.20 = 0.10) | 1 (1.00 × 0.20 = 0.20) | Low effort + near-zero risk. Moderate impact and revenue. Visual polish that improves perceived quality. |
| 04 | ats-score | **0.64** | 4 (0.75 × 0.35 = 0.26) | 7 (0.54 × 0.25 = 0.13) | 4 (0.75 × 0.20 = 0.15) | 3 (0.50 × 0.20 = 0.10) | High impact + revenue signal, but 7-day effort and moderate technical risk (ATS parsing heuristics are fragile). |
| 05 | proposal-history | **0.62** | 3 (0.50 × 0.35 = 0.18) | 4 (0.62 × 0.25 = 0.15) | 2 (0.25 × 0.20 = 0.05) | 2 (0.75 × 0.20 = 0.15) | Moderate everything. Useful for retention but doesn't directly drive acquisition or revenue. |
| 06 | format-preserve | **0.55** | 5 (1.00 × 0.35 = 0.35) | 14 (0.00 × 0.25 = 0.00) | 5 (1.00 × 0.20 = 0.20) | 4 (0.25 × 0.20 = 0.05) | Highest user impact AND revenue signal, but highest effort (14 days) zeroes the effort score. High technical risk (PDF/DOCX parsing + format reconstruction). The v2 vision — worth building, but not first. |
| 07 | linkedin-import | **0.44** | 3 (0.50 × 0.35 = 0.18) | 6 (0.62 × 0.25 = 0.15) | 2 (0.25 × 0.20 = 0.05) | 4 (0.25 × 0.20 = 0.05) | High technical risk (LinkedIn scraping is fragile, API access is restricted). Low revenue signal. Convenience feature, not core. |
| 08 | section-reorder | **0.42** | 2 (0.25 × 0.35 = 0.09) | 4 (0.62 × 0.25 = 0.15) | 1 (0.00 × 0.20 = 0.00) | 3 (0.50 × 0.20 = 0.10) | Lowest user impact. No revenue signal. Moderate effort and risk for a feature that's nice-to-have at best. |

## Dependency constraints applied

**1 hard constraint:**
- `must_before: [pdf-template-gallery, format-preserve]` — Template gallery should ship before format-preserving export, since format-preserve needs to know which template formats to preserve against. Gallery already ranked higher (score 0.76 vs 0.55), so no displacement needed.

## Cross-project-type proof

This demo ranks **product features for a SaaS application** — a domain with zero overlap to SEO page builds:

- **Items:** software features (cover letter generation, ATS scoring, PDF templates, LinkedIn import) — not pages, cities, or services.
- **Criteria:** user impact, implementation effort, revenue signal, technical risk — none reference SEO, geographic anchors, competitive opportunity, or content reuse.
- **Scoring mode:** weighted-sum — same mode as the handoff-backlog demo, different from the SEO profile's lexicographic mode.
- **Result:** format-preserve (the v2 vision feature) correctly ranks 6th despite having the highest user impact and revenue signal, because its 14-day effort and high technical risk drag the total score down. Cover-letter-gen ranks 1st as the best effort/impact ratio. This matches the kind of judgment a product manager would make.

Zero engine modifications. Zero SEO references. The engine ranked SaaS features from ad-hoc criteria definitions alone.
