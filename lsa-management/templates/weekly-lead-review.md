---
type: template
name: LSA weekly lead review tracking template
description: Per-client running ledger for LSA lead review, response time, book rate, and budget pacing. Initialize one copy per managed client at go-live.
created: 2026-06-25
updated: 2026-06-25
tags: [template, lsa, lead-review, tracking]
---

# LSA tracking — {client_slug}

> **Instructions:** Copy this file to `tracking-<client_slug>.md` at go-live.
> Replace `{client_slug}` and `{business_name}` with values from
> `skills/lsa-setup/configs/lsa-config-<client_slug>.json`.
> Append a new week section every Monday. Never overwrite prior weeks.

**Client:** {business_name}
**Go-live date:** {go_live_date}
**Monthly budget:** ${monthly_usd}
**Weekly pacing target:** ${weekly_target} ({weekly_pacing})
**Response time target:** {target_seconds}s
**Who answers:** {who_answers}

---

## Week of YYYY-MM-DD (Week N since go-live)

### Leads

| # | Date | Type | Job type | ZIP | Outcome | Charge | Rating given | Bad-lead reason | Credit? | Response time |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | | phone/msg/booking | | | booked/not-booked/spam/wrong-job/wrong-area/no-answer/duplicate | $XX | Very satisfied/Satisfied/Dissatisfied/Very dissatisfied | spam/wrong-job/wrong-area/no-answer/duplicate/n-a | pending/yes-$X/no | Xs |

### Weekly summary

- **Total leads:** N
- **Bad leads rated "Very dissatisfied":** N (N%)
- **Credits received (from prior weeks):** $N
- **Booked:** N
- **Book rate this week:** N% (benchmark: 43.9%)
- **Rolling 4-week book rate:** N% (N booked / N total)
- **Spend this week:** $N (target: ${weekly_target})
- **Pacing variance:** +/-N% (within ±20% = on pace)
- **Avg response time:** Ns (target: {target_seconds}s)
- **Leads within response target:** N/N (N%)

### Flags

- [ ] Any slow responses (>target)? → note which leads
- [ ] Any wrong-area leads? → note ZIPs for Workflow 4
- [ ] Any wrong-job leads? → note job types for Workflow 4
- [ ] Book rate below 30% on rolling 4-week? → trigger Workflow 4

### Notes

<!-- Observations, patterns, operator actions taken -->

---

<!-- Copy the "Week of" section above for each new week. Keep all prior weeks for trend analysis. -->

## Monthly rollup — YYYY-MM

> Compiled from weeks N–N. Feeds into Workflow 6 (monthly LSA metrics).

| Metric | Value | Benchmark / Target | Status |
|---|---|---|---|
| Total leads | N | ~3–4 at $300/mo | |
| Bad leads rated | N (N%) | Lower is better | |
| Credits received | $N | — | |
| Net spend | $N | ≤ ${monthly_usd} | |
| Book rate | N% | 43.9% | ✅/⚠️/🔴 |
| Actual CPL | $N | $75–$90 metro | ✅/⚠️ |
| Cost per booked job | $N | Lower is better | |
| Avg response time | Ns | ≤ {target_seconds}s | ✅/❌ |
| % within response target | N% | Higher is better | |

### Tightening review (Workflow 4)

- **Wrong-area leads this month:** N from ZIPs: [list]
- **Wrong-job leads this month:** N for types: [list]
- **Recommendation:** [remove ZIP X / disable job type Y / no changes needed]
- **Operator decision:** [approved / deferred / n/a]

### Month-end notes

<!-- Trends, anomalies, config changes made, recommendations for next month -->
