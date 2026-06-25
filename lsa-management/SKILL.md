---
name: lsa-management
version: 1.0
description: >
  Recurring operating discipline for a live Google Local Services Ads account.
  Engine-first: reads per-client config from lsa-setup, zero hardcoded client
  values. Covers weekly lead review (bad-lead rating as the only credit lever),
  response-time tracking, book-rate vs benchmark, service-area/job-type
  tightening, budget pacing, and monthly metrics that compose into the
  monthly-client-report SOP.
triggers:
  - "run lsa weekly review for <client>"
  - "lsa management review for <client>"
  - "pull lsa metrics for <client>"
  - "lsa monthly report for <client>"
  - "tighten lsa targeting for <client>"
clients: [ev-electric-services, s-and-h-contracting]
depends-on: [lsa-setup]
unblocks: []
created: 2026-06-25
updated: 2026-06-25
tags: [skill, lsa, local-services-ads, management, lead-rating, reporting, ads, client-growth, sop]
---

# LSA Management — operator SOP skill (v1.0)

> **Read this file in full before touching any other file.** This skill is the
> recurring operating discipline that keeps an LSA account performing after
> go-live. It picks up the clean baton from `lsa-setup` (B1) and runs
> indefinitely.

## Purpose

Keep a live LSA account healthy and ROI-positive through disciplined weekly
lead review, active bad-lead rating, response-time monitoring, and tight
service-area/job-type configuration. The economics are grounded in the
2026-06-06 LSA deep-research report
(`[[research-2026-06-06-lsa-economics-dc-md-va-electrical]]`).

## How it works

1. Load the per-client config at `skills/lsa-setup/configs/lsa-config-<client_slug>.json`.
   This skill **reuses** the lsa-setup config — no separate config file.
2. Run the recurring workflows below on their cadences.
3. At month-end, produce the LSA metrics section that **composes into** the
   monthly client report (see Workflow 6).

**No client value is hardcoded in this file.** Every client-specific fact
(trade, service area, budget, job types, response path) comes from the
lsa-setup config JSON. To manage a new client: fill their lsa-setup config,
complete lsa-setup Phase 6 (go-live), then start running these workflows.

## Config dependency

This skill reads from `skills/lsa-setup/configs/lsa-config-<client_slug>.json`.
The fields it consumes at runtime:

| Field | Used by | Purpose |
|---|---|---|
| `client_slug` | All workflows | File naming, log paths |
| `business_name_exact` | Monthly report | Client-facing label |
| `budget.monthly_usd` | Workflow 5 (pacing) | Budget cap |
| `budget.weekly_pacing` | Workflow 5 (pacing) | Pacing strategy |
| `service_area.zip_codes` | Workflow 4 (tightening) | Area audit baseline |
| `service_area.description` | Monthly report | Human-readable area |
| `job_types.enabled` | Workflow 4 (tightening) | Job-type audit baseline |
| `job_types.high_value` | Workflow 4 (tightening) | Weighting reference |
| `response.target_seconds` | Workflow 2 (response time) | SLA threshold |
| `response.who_answers` | Workflow 2 (response time) | Accountability |
| `lsa_account.url` | Workflow 1 (lead review) | LSA dashboard URL |
| `lsa_account.go_live_date` | All workflows | Week/month numbering |

## Per-client tracking

Each managed client gets a tracking file at:
`skills/lsa-management/templates/tracking-<client_slug>.md`

This file is the running ledger for the client's LSA performance. It is
initialized from the template at `skills/lsa-management/templates/weekly-lead-review.md`
at go-live and updated weekly. See the template for the full schema.

---

## The six recurring workflows

### Workflow 1 — Weekly lead review (EVERY WEEK — the most important workflow)

> **This is the single most important workflow in LSA management.** Google
> removed manual lead disputes in 2024. The **only** credit lever remaining
> is rating a bad lead "Very dissatisfied." Every unrated bad lead is money
> lost with no recourse.

**Cadence:** Weekly (every Monday, or the first business day after go-live
then weekly thereafter).

**Who:** Operator (reviews leads in the LSA dashboard).

**Steps:**

1. **Open the LSA dashboard** for `config.client_slug` at `config.lsa_account.url`.

2. **Pull every lead from the past 7 days.** For each lead, record in the
   tracking file:
   - Date received
   - Lead type (phone call / message / booking)
   - Job type requested
   - ZIP code / area (if visible)
   - Outcome: booked / not booked / spam / wrong job / wrong area / no answer
   - Charge amount (what Google charged for this lead)

3. **Rate every bad lead "Very dissatisfied" immediately.** A bad lead is any
   lead that falls into these categories:
   - **Spam / robocall / wrong number** — not a real customer
   - **Wrong job type** — customer wants a service you don't offer
   - **Wrong area** — customer is outside your service area
   - **No answer / hung up** — no opportunity to book
   - **Duplicate** — same customer, same request, already charged

   > ⚠️ **Critical:** "Very dissatisfied" is the ONLY rating that triggers
   > Google's automated credit review. Selecting "dissatisfied" or any other
   > rating does NOT trigger a credit review. This is not intuitive — it is
   > the post-2024 reality documented in the 06-06 research.

   For each bad lead rated "Very dissatisfied," record:
   - The reason category (spam / wrong-job / wrong-area / no-answer / duplicate)
   - Whether Google auto-credited it (check ~72 hours later; credits appear
     within ~30 days)

4. **Rate good leads too.** Rate booked leads "Very satisfied" or "Satisfied."
   This builds the response-quality signal Google uses for ranking.

5. **Update the tracking file** with this week's entries. Calculate:
   - Total leads this week
   - Bad leads rated "Very dissatisfied" (count + % of total)
   - Credits received (from leads rated in prior weeks)
   - Net spend this week (charged − credits)

**Completion gate:** Every lead from the past 7 days has been reviewed and
rated. The tracking file is updated. Bad leads are rated "Very dissatisfied"
with a reason.

### Workflow 2 — Response-time tracking

> Google rewards fast responders with more leads and better placement.
> Slow response = fewer leads = higher effective CPL.

**Cadence:** Weekly (runs as part of the weekly lead review).

**Steps:**

1. For each lead received this week, record the **time-to-first-contact**:
   - Phone leads: how quickly was the call answered? (seconds)
   - Message leads: how quickly was the first reply sent? (minutes)
   - Booking leads: how quickly was the booking confirmed? (minutes)

2. Compare against `config.response.target_seconds`:
   - ✅ Within target: note as on-time
   - ❌ Over target: flag as slow, note the actual response time

3. Calculate the weekly response-time metrics:
   - Average response time (all leads)
   - % of leads answered within target
   - Slowest response time

4. If **≥30% of leads are slow** (over target) for two consecutive weeks:
   - Surface to the operator as a response-path problem
   - Recommend: adjust `config.response.who_answers` or
     `config.response.target_seconds`, or brief the answering person

**Completion gate:** Response times logged for all leads. Slow-response
flag raised if threshold breached.

### Workflow 3 — Book-rate tracking

> The Feb 2026 benchmark across 888 home-service contractors is **43.9%
> book rate** (leads → booked jobs). Tracking against this benchmark is the
> early-warning system for lead-quality erosion — the problem 67% of
> contractors reported in 2025.

**Cadence:** Weekly (calculated during lead review) + monthly (trend).

**Steps:**

1. From this week's lead review data, calculate:
   - **Booked leads** (leads that became a scheduled job)
   - **Total leads** (all leads received, excluding credits)
   - **Book rate** = booked / total × 100%

2. Compare against the **43.9% benchmark**:
   - ✅ **≥40%:** Healthy. On or near benchmark.
   - ⚠️ **30–39%:** Watch. Below benchmark — check if bad leads are being
     rated, if job types are too broad, or if service area is too wide.
   - 🔴 **<30%:** Alert. Significantly below benchmark — trigger Workflow 4
     (service-area / job-type tightening) and review lead quality patterns.

3. **Small-sample caveat:** At $300/month and $75–90 CPL, the client
   receives ~3–4 leads per month. Weekly book rate on 0–1 leads is not
   statistically meaningful. **Use the rolling 4-week (monthly) book rate**
   as the primary trend indicator, not individual weeks. Flag the small
   sample explicitly in any report.

4. Record in the tracking file:
   - This week: leads / booked / book rate
   - Rolling 4-week: leads / booked / book rate
   - Trend arrow: ↑ improving / → stable / ↓ declining

**Completion gate:** Book rate calculated and compared to benchmark.
Trend recorded. Alert raised if below 30% on a rolling 4-week basis.

### Workflow 4 — Service-area / job-type tightening

> Since 2024, Google no longer credits leads from outside your service area
> or for job types you don't service. Every extra ZIP or job type is a lead
> category you pay for with no recourse if it's wrong. Tightening is the
> primary defense.

**Cadence:** Monthly review, or triggered by Workflow 3 alert (book rate <30%).

**Steps:**

1. **Analyze bad-lead patterns** from the past 4 weeks of lead reviews:
   - Group bad leads by **reason category** (wrong-job / wrong-area / spam /
     no-answer / duplicate).
   - For wrong-area leads: which ZIPs are generating them?
   - For wrong-job leads: which job types are generating them?

2. **ZIP tightening decision:**
   - If a ZIP has generated ≥2 wrong-area leads in the past month with
     0 booked leads → recommend removing it from `config.service_area.zip_codes`.
   - Apply the B1 rule: "if you wouldn't drive there for a $300 job, drop it."
   - Present the recommendation to the operator; do not remove ZIPs
     without explicit approval.

3. **Job-type tightening decision:**
   - If a job type has generated ≥2 wrong-job leads in the past month with
     0 booked leads → recommend disabling it from `config.job_types.enabled`.
   - Check whether the job type is in `config.job_types.high_value` — if so,
     flag the conflict (high-value but generating bad leads) and let the
     operator decide.
   - Present the recommendation; do not change job types without approval.

4. **If changes are approved:**
   - Update `skills/lsa-setup/configs/lsa-config-<client_slug>.json` with the
     new ZIP codes or job types.
   - Make the corresponding change in the LSA dashboard.
   - Note the change in the tracking file with date and reason.

**Completion gate:** Bad-lead patterns analyzed. Recommendations presented
(if any). Config updated if changes approved.

### Workflow 5 — Budget pacing

> At $300/month with $75–90 metro CPL, the budget buys ~3–4 leads/month.
> Overspend is unlikely at this level, but underspend (Google not serving
> enough ads) signals a ranking or configuration problem.

**Cadence:** Weekly check (during lead review) + monthly reconciliation.

**Steps:**

1. **Weekly pacing check:**
   - Read `config.budget.monthly_usd` (e.g., $300) and
     `config.budget.weekly_pacing` (e.g., "even" → ~$75/week).
   - Check actual spend this week from the LSA dashboard.
   - Compare:
     - ✅ Within ±20% of weekly target: on pace
     - ⚠️ >20% over: approaching budget cap early — may run out before month-end
     - ⚠️ >20% under: Google is not serving enough ads — check ranking, reviews,
       responsiveness signals

2. **Monthly reconciliation:**
   - Total spend for the month vs `config.budget.monthly_usd`
   - Total leads received
   - **Actual CPL** = total spend / total leads
   - **Cost per booked job** = total spend / booked leads
   - Compare actual CPL against the **$75–$90 metro planning band**:
     - ✅ Within band: expected for DC/MD/VA
     - ⚠️ Above $90: higher than expected — check if high-value job types are
       being weighted
     - ✅ Below $75: good — client is getting above-average value

3. **Record in tracking file:**
   - Weekly: spend / target / variance
   - Monthly: total spend / leads / CPL / cost-per-booked / budget utilization %

**Completion gate:** Pacing checked. Monthly reconciliation complete at
month-end. Anomalies flagged.

### Workflow 6 — Monthly LSA metrics (composes into monthly client report)

> This workflow does NOT produce a standalone report. It produces the **LSA
> section** that feeds into the monthly client report SOP
> (`[[handoff-2026-06-22-monthly-client-report-sop]]`). When that SOP ships,
> this section slots into its "Paid channels" or equivalent section. Until
> then, the operator can use the output directly as a client-facing LSA
> summary.

**Cadence:** Monthly (first business day after month-end).

**Steps:**

1. **Compile the month's data** from the tracking file. Produce the metrics
   block using the template at `skills/lsa-management/templates/monthly-lsa-metrics.md`.

2. **The metrics block contains:**

   | Metric | Source | Benchmark |
   |---|---|---|
   | Total leads | Tracking file | ~3–4/mo at $300 budget |
   | Bad leads rated "Very dissatisfied" | Tracking file | Lower is better |
   | Credits received | LSA dashboard | Tracks bad-lead recovery |
   | Net spend (charged − credits) | Calculated | ≤ `budget.monthly_usd` |
   | Book rate (booked / total) | Tracking file | 43.9% benchmark |
   | Actual CPL | spend / leads | $75–$90 metro band |
   | Cost per booked job | spend / booked | Lower is better |
   | Average response time | Tracking file | ≤ `response.target_seconds` |
   | % leads answered within target | Tracking file | Higher is better |

3. **Honest caveats (include in every report):**
   - At $300/month, sample sizes are small (~3–4 leads). Monthly trends are
     directional, not statistically significant. Use rolling 3-month trends
     for reliable patterns.
   - The 43.9% benchmark is a national home-services average (Feb 2026, 888
     contractors). DC/MD/VA performance may differ due to market density.
   - CPL varies by job type and competition. Panel upgrades and EV chargers
     carry premium CPLs vs general electrical.

4. **Recommendations section** (plain language, client-facing):
   - What's working (leads booked, response time, ROI)
   - What needs attention (bad-lead patterns, slow response, book-rate drift)
   - Specific actions for next month (ZIP changes, job-type changes, budget
     adjustment, response-path fix)

5. **Composition point:** The output of this workflow is a Markdown section
   titled `## LSA Performance — {month} {year}` with the metrics table +
   caveats + recommendations. This section is designed to be copy-pasted
   (or programmatically inserted) into the monthly client report. It does
   NOT duplicate the report's structure (client info header, SEO section,
   GBP section, etc.) — it only provides the LSA-specific content.

**Completion gate:** Monthly metrics block produced. Ready to compose into
the monthly client report.

---

## Cadence summary

| Workflow | Frequency | Day | Duration | Operator action required? |
|---|---|---|---|---|
| 1. Lead review | Weekly | Monday | ~15 min/client | Yes — review + rate in dashboard |
| 2. Response time | Weekly | Monday (with #1) | ~5 min/client | No — data from #1 |
| 3. Book rate | Weekly + monthly | Monday + month-end | ~5 min/client | No — calculated |
| 4. Tightening | Monthly (or triggered) | Month-end | ~15 min/client | Yes — approval for changes |
| 5. Budget pacing | Weekly + monthly | Monday + month-end | ~5 min/client | No — data from dashboard |
| 6. Monthly metrics | Monthly | 1st business day after month-end | ~20 min/client | No — compiled from tracking |

**Total weekly time per client:** ~25 minutes (Workflows 1–3 + 5 weekly check).
**Total monthly time per client:** ~45 minutes additional (Workflows 4–6).

---

## Per-client tracking file

At go-live, initialize a tracking file for the client:

```
skills/lsa-management/templates/tracking-<client_slug>.md
```

Use the template at `skills/lsa-management/templates/weekly-lead-review.md` as
the starting point. The tracking file is a running ledger — append weekly
entries, never overwrite.

The tracking file schema:

```markdown
## Week of YYYY-MM-DD

### Leads

| # | Date | Type | Job type | ZIP | Outcome | Charge | Rating given | Bad-lead reason | Credit? | Response time |
|---|---|---|---|---|---|---|---|---|---|---|

### Weekly summary

- Total leads: N
- Bad leads rated "Very dissatisfied": N (N%)
- Booked: N
- Book rate: N% (benchmark: 43.9%)
- Spend: $N (target: $N/week)
- Avg response time: Ns (target: Ns)
- Leads within response target: N%

### Notes
[Observations, patterns, operator actions taken]
```

---

## Schedule task (weekly review reminder)

To ensure the weekly review doesn't slip, the operator can set up a recurring
reminder. Suggested approach:

```
# Option A: Claude Code schedule task (if schedule skill is available)
/schedule weekly "Run lsa-management weekly review for ev-electric-services"

# Option B: Calendar reminder
Create a recurring Monday 9:00 AM calendar event:
"LSA Weekly Review — EV Electric + S&H Contracting"
with a link to this SKILL.md and the tracking files.
```

The weekly review covers all managed clients in one session. At 2 clients
× ~25 min = ~50 minutes total.

---

## Duplicability

This skill is trade-agnostic and client-agnostic. It reads everything from
the lsa-setup config JSON. To manage LSA for a new client:

1. Complete `lsa-setup` for that client (fills the config JSON, completes
   go-live).
2. Initialize a tracking file: copy the template, replace `<client_slug>`.
3. Start running the 6 workflows. Nothing in the workflows assumes
   electrician or any specific trade.

**Proof — running for two clients from config:**

| Field | EV Electric Services | S&H Contracting |
|---|---|---|
| `client_slug` | `ev-electric-services` | `s-and-h-contracting` |
| `budget.monthly_usd` | $300 | $300 |
| `budget.weekly_pacing` | even (~$75/wk) | even (~$75/wk) |
| `response.target_seconds` | 300 (5 min) | 300 (5 min) |
| `response.who_answers` | Ahmad Shaban (owner) | Mohammed Salahuddin (owner) |
| `service_area.zip_codes` | 16 ZIPs (Fairfax County core) | 13 ZIPs (NoVA core + extended) |
| `job_types.enabled` | 8 types | 8 types |
| `job_types.high_value` | 3 types (panel, EV, wiring) | 3 types (panel, EV, wiring) |

Both clients run through the same 6 workflows with no skill-level changes.
The tracking files diverge because their lead volumes, response times, and
service areas differ — that's the point of per-client tracking.

**Non-electrician proof:** The example plumber config at
`skills/lsa-setup/configs/lsa-config-example-plumber.json` would also work.
The workflows reference `config.job_types.*`, `config.service_area.*`, etc.
— never "electrician" or any trade-specific term.

---

## Lead quality context (load-bearing — read annually)

This section summarizes the post-2024 lead quality reality. It is the
foundation for why Workflow 1 (weekly lead review) is the most important
workflow.

1. **Manual lead disputes removed (mid-2024).** You cannot manually dispute
   individual leads. The automated system reviews charged leads within ~72
   hours and applies credits within ~30 days.

2. **"Job type not serviced" and "geo not serviced" are NOT creditable.**
   Off-target leads cost you with no recourse. This is why Workflow 4
   (tightening) exists.

3. **The only operator lever is "Rate this lead" → "Very dissatisfied."**
   This is the only rating that triggers a credit review. Rate every bad
   lead promptly.

4. **67% of contractors reported lead quality declined** over 18 months
   (2025 survey). Active management is the defense.

## Sources

- `[[research-2026-06-06-lsa-economics-dc-md-va-electrical]]` — full LSA economics report (CPL, book rate, lead quality)
- `[[lsa-plain-language-guide]]` — plain-language LSA reference
- `[[handoff-2026-06-23-b1-lsa-setup-skill]]` — B1 handoff (upstream setup)
- `[[handoff-2026-06-23-b2-lsa-management-skill]]` — B2 handoff (this skill)
- `[[handoff-2026-06-22-monthly-client-report-sop]]` — monthly report SOP (composition target)
- Blue Grid Media — Feb 2026 CPL benchmarks (43.9% book rate, $53 avg CPL)
- BG Collective — LSA lead dispute changes 2024-2025
