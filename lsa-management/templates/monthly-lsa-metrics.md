---
type: template
name: Monthly LSA metrics section
description: >
  Client-facing LSA performance section for the monthly report. Designed to
  compose into the monthly-client-report SOP — paste this section into the
  report's paid-channels area. Not a standalone report.
created: 2026-06-25
updated: 2026-06-25
tags: [template, lsa, monthly-report, metrics, compose]
---

<!--
  COMPOSITION INSTRUCTIONS:
  This template produces one Markdown section ("## LSA Performance").
  It slots into the monthly client report under "Paid Channels" or equivalent.
  Fill values from the per-client tracking file at:
    skills/lsa-management/templates/tracking-<client_slug>.md

  When the monthly-client-report SOP (S11) ships, this template's output
  becomes one input to that SOP's composition. Until then, the operator
  can use this section directly as a client-facing LSA summary.
-->

## LSA Performance — {month} {year}

**Account:** {business_name} | **Budget:** ${monthly_usd}/mo | **Market:** {service_area_description}

### Key metrics

| Metric | This month | Last month | Trend | Benchmark |
|---|---|---|---|---|
| Leads received | {leads} | {leads_prev} | {trend_arrow} | ~3–4/mo at ${monthly_usd} |
| Leads booked | {booked} | {booked_prev} | {trend_arrow} | — |
| Book rate | {book_rate}% | {book_rate_prev}% | {trend_arrow} | 43.9% (industry avg) |
| Total spend | ${spend} | ${spend_prev} | {trend_arrow} | ≤ ${monthly_usd} |
| Credits received | ${credits} | ${credits_prev} | — | — |
| Net spend | ${net_spend} | ${net_spend_prev} | {trend_arrow} | — |
| Cost per lead | ${cpl} | ${cpl_prev} | {trend_arrow} | $75–$90 (DC/MD/VA) |
| Cost per booked job | ${cpb} | ${cpb_prev} | {trend_arrow} | — |
| Avg response time | {response_avg}s | {response_avg_prev}s | {trend_arrow} | ≤ {target_seconds}s |

### What's working

- {positive_1}
- {positive_2}

### What needs attention

- {attention_1}
- {attention_2}

### Actions for next month

- {action_1}
- {action_2}

### Important context

At ${monthly_usd}/month, your LSA account receives a small number of leads
(~3–4). This means month-to-month swings are normal and not necessarily
a sign of a problem. We look at rolling 3-month trends for reliable
patterns. The 43.9% book-rate benchmark is a national average across 888
home-service contractors (Feb 2026) — your market (DC/MD/VA) may perform
differently due to higher competition and higher job values.
