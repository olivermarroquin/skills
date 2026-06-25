---
type: reference
name: LSA management benchmarks
description: Key performance benchmarks for LSA management decisions — CPL, book rate, response time. Sourced from the 2026-06-06 LSA economics research + Blue Grid Media Feb 2026 dataset.
created: 2026-06-25
updated: 2026-06-25
tags: [reference, lsa, benchmarks, cpl, book-rate]
---

# LSA management benchmarks

All figures sourced from `[[research-2026-06-06-lsa-economics-dc-md-va-electrical]]`
and the Blue Grid Media Feb 2026 dataset (888 contractors, $6.72M observed spend)
unless otherwise noted.

## Cost per lead (CPL)

| Scope | CPL | Notes |
|---|---|---|
| National electrical average | ~$39 | Feb 2026 benchmark |
| National home-services average | ~$53 | Feb 2026, all trades |
| Small/easy markets | ~$30 | Low competition |
| Competitive metros (DC/MD/VA) | **$75–$90+** | Planning number for NoVA/DC/MD |
| Premium job types (panel, EV) | Higher end of range | Reflects higher job value |

**Decision rule:** If actual CPL is consistently above $90 for 3+ months,
review job-type weighting and service-area configuration.

## Book rate

| Benchmark | Rate | Source |
|---|---|---|
| National home-services average | **43.9%** | Blue Grid Media, Feb 2026 |
| Healthy range | ≥40% | On or near benchmark |
| Watch zone | 30–39% | Below benchmark — investigate |
| Alert zone | <30% | Trigger tightening (Workflow 4) |

**Decision rule:** Use rolling 4-week book rate, not weekly, because of
small sample sizes at $300/month (~3–4 leads/month).

## Response time

| Metric | Target | Why |
|---|---|---|
| Phone answer time | ≤ 5 minutes (300s) | Google rewards fast responders |
| Message reply time | ≤ 15 minutes | Same signal, different channel |
| Slow-response threshold | ≥30% slow for 2 weeks | Triggers response-path review |

**Decision rule:** Response time is a Google ranking signal. Faster response
→ more leads at the same budget. If chronically slow, adjust who answers
or set up a dedicated response path.

## Budget pacing

| Budget | Weekly target (even) | Expected leads/month | Expected booked/month |
|---|---|---|---|
| $300/mo | ~$75/wk | ~3–4 | ~1–2 (at 43.9%) |
| $500/mo | ~$125/wk | ~5–7 | ~2–3 |
| $1,000/mo | ~$250/wk | ~11–13 | ~5–6 |

**Decision rule:** Weekly spend variance ±20% is normal. Chronic underspend
(Google not delivering) signals a ranking or configuration problem, not a
budget problem.

## ROI context (DC/MD/VA electrical)

| Job type | Typical revenue (DC metro) | CPL at $75–$90 | Leads to break even |
|---|---|---|---|
| Electrical panel upgrade | $2,400–$3,500 | $75–$90 | <1 booked job |
| EV charger install | $1,200–$2,500 | $75–$90 | ~1 booked job |
| General electrical | $200–$800 | $75–$90 | 1–3 booked jobs |

**Key insight:** One booked panel upgrade or EV charger install pays for
several months of LSA spend at $300/month. The math works because the jobs
are high-value, not because the leads are cheap.
