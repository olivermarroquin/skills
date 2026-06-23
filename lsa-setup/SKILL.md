---
name: lsa-setup
version: 1.0
description: >
  End-to-end SOP for standing up Google Local Services Ads for a local-services
  client. Engine-first: reads a per-client config JSON, zero hardcoded client
  values. Covers eligibility check → document gather → account creation →
  verification → budget/service-area/job-type config → go-live checklist.
  Hands a clean baton to `lsa-management` (B2) at go-live.
triggers:
  - "set up LSA for <client>"
  - "run lsa-setup on <client>"
  - "stand up Local Services Ads for <client>"
  - "start LSA onboarding for <client>"
clients: [ev-electric-services, s-and-h-contracting]
depends-on: []
unblocks: [lsa-management]
created: 2026-06-23
updated: 2026-06-23
tags: [skill, lsa, local-services-ads, google-verified, ads, client-growth, sop]
---

# LSA Setup — operator SOP skill (v1.0)

> **Read this file in full before touching any other file.** Every phase has
> a completion gate, an operator-action list, and a handoff contract to the
> next phase. The skill is only as useful as how strictly it follows them.

## Purpose

Turn a local-services client from "no LSA presence" to "Google Verified badge
live, leads flowing, management process handed off." The economics are grounded
in the 2026-06-06 LSA deep-research report
(`[[research-2026-06-06-lsa-economics-dc-md-va-electrical]]`) and verified
against Google's live documentation on 2026-06-23.

## How it works

1. Load the per-client config at `skills/lsa-setup/configs/lsa-config-<client_slug>.json`.
2. Walk the 6 phases below in order. Each phase has a completion gate.
3. At go-live, hand the baton to `lsa-management` (B2) with a clean state.

**No client value is hardcoded in this file.** Every client-specific fact
(trade, license, service area, budget, job types) comes from the config JSON.
To onboard a new client: copy an existing config, fill it, run the skill.

## Config location + schema

Path: `skills/lsa-setup/configs/lsa-config-<client_slug>.json`

Schema reference: `skills/lsa-setup/references/lsa-config-schema.json`

Required fields (see schema for full shape):

| Field | Type | Example |
|---|---|---|
| `client_slug` | string | `"acme-plumbing"` |
| `business_name_exact` | string | `"Acme Plumbing Solutions LLC"` — must match insurance cert + LSA account exactly |
| `trade` | string | `"plumber"` |
| `owner_name` | string | `"Jane Rodriguez"` |
| `owner_email` | string | Google account email for LSA signup |
| `license.number` | string | License number (operator-gathered) |
| `license.state` | string | `"VA"` (or any US state) |
| `license.issuer` | string | `"State DPOR"` (issuing authority) |
| `license.category` | string | `"Master Plumber"` (trade-specific) |
| `insurance.carrier` | string | Insurance company name |
| `insurance.policy_number` | string | Policy number |
| `insurance.coverage_amount` | string | `"$1,000,000"` minimum |
| `insurance.expiry` | string | `"YYYY-MM-DD"` |
| `insurance.acord25_on_file` | boolean | `true` when ACORD-25 cert collected |
| `insurance.business_name_matches` | boolean | `true` when cert name = `business_name_exact` |
| `technicians` | array | `[{"name": "...", "background_check_status": "pending"}]` |
| `gbp.verified` | boolean | `true` / `false` |
| `gbp.profile_url` | string | Google Maps URL |
| `service_area.zip_codes` | array | `["20814", "20815", ...]` — tight, no sprawl |
| `service_area.description` | string | Human-readable area description |
| `job_types.enabled` | array | `["Panel Upgrade", "EV Charger Installation", ...]` |
| `job_types.high_value` | array | Subset of enabled weighted for premium leads |
| `budget.monthly_usd` | number | `300` |
| `budget.weekly_pacing` | string | `"even"` or `"manual"` |
| `response.who_answers` | string | `"Owner"` or `"Office manager"` etc. |
| `response.target_seconds` | number | Target response time in seconds |
| `hours` | array | Business hours (mirrors client JSON `hours` shape) |

## Phase 1 — Eligibility check

**Goal:** Confirm the client's trade is LSA-eligible in their market, and that
the three prerequisite pillars (license, insurance, GBP) exist or can be
obtained.

### Steps

1. **Confirm trade eligibility.** Google LSA supports ~70 home-service
   categories. Verify `config.trade` is in the supported list for the client's
   country/region. Electricians, plumbers, HVAC, roofers, locksmiths, pest
   control, etc. are all supported. If the trade is not supported, STOP —
   LSA is not available.

2. **Check license status.** Read `config.license`. If `number` is populated,
   confirm the license type matches the LSA category the client will select.
   If `number` is blank → flag for operator to gather from client.
   - **Scope match rule:** if the state license covers a specific scope
     (residential only, low voltage), it must match the LSA service categories
     selected. A residential-only license + "commercial electrical" LSA
     category = rejection.

3. **Check insurance status.** Read `config.insurance`.
   - Minimum: **$1,000,000 general liability per occurrence.**
   - Format: **ACORD-25 certificate of insurance.**
   - **Business name on cert must exactly match `config.business_name_exact`.**
     If the cert says "Acme Plumbing Solutions" but the LSA account is
     "Acme Plumbing Solutions LLC" → rejection. Insurer can reissue same-day, free.
   - If any field is blank or `acord25_on_file: false` → flag for operator.

4. **Check GBP status.** Read `config.gbp.verified`.
   - Must be `true`. GBP verification became mandatory Nov 2024.
   - If `false` → STOP. GBP verification is a prerequisite; handle separately
     before continuing LSA setup.

### Phase 1 gate

All three pillars confirmed present (or operator has a clear action list to
obtain them). Document any gaps in the operator checklist.

**Output:** Updated checklist with eligibility status per pillar.

---

## Phase 2 — Document gather

**Goal:** Collect every document Google will request during verification, in
the exact format they require. This is the long-pole prep step.

### Documents required

| # | Document | Format | Key requirement | Config field |
|---|----------|--------|-----------------|--------------|
| 1 | State/local trade license | Digital copy (PDF/image) | Number + issuer + scope match | `license.*` |
| 2 | General liability insurance certificate | **ACORD-25** | ≥$1M per occurrence; business name **exact match** | `insurance.*` |
| 3 | Owner government-issued ID | Photo ID (driver's license, passport) | Matches `config.owner_name` | `owner_name` |
| 4 | Technician roster | Name list | Every tech who performs jobs under the account | `technicians[]` |

### Operator actions

- Request documents from client. Use the per-client operator checklist at
  `skills/lsa-setup/checklists/checklist-<client_slug>.md`.
- For insurance: if the cert business name doesn't match, ask the client to
  have their insurer reissue with the exact name. Usually same-day, no cost.
- For technicians: emphasize that **every technician** needs an individual
  background check. Missing a tech = that tech can't do LSA jobs.

### Phase 2 gate

All 4 documents on file (digital copies in operator's possession).
`config.insurance.acord25_on_file: true` and
`config.insurance.business_name_matches: true`.

**Output:** Config JSON updated with all document fields populated.

---

## Phase 3 — Account creation

**Goal:** Create the LSA account in Google, link the business profile, and
select the correct trade category + job types.

### Steps

1. **Sign up at ads.google.com/local-services-ads** using the client's Google
   account (the same one that owns the GBP).
   - If the client doesn't have a Google account or uses a different one for
     GBP → coordinate with operator. LSA account should be under the same
     Google account as the verified GBP.

2. **Select the business category.** Match to `config.trade`:
   - Electrician → "Electrician"
   - Plumber → "Plumber"
   - HVAC → "HVAC"
   - etc.

3. **Select job types.** From `config.job_types.enabled`. Weight the selection
   toward `config.job_types.high_value` items. These are the job types that
   will appear in the ad and that Google will match leads against.
   - **Be selective, not exhaustive.** Every enabled job type is a lead
     category. Off-target job types generate leads you pay for but can't serve
     well. Tight = better ROI.

4. **Set the service area.** Enter `config.service_area.zip_codes`.
   - **Tight ZIP targeting is critical.** Since 2024, Google **no longer
     credits leads from outside your service area.** Every ZIP you add is a
     ZIP you'll pay for leads from. Only include ZIPs you can actually serve
     profitably.

5. **Link the Google Business Profile.** The GBP at `config.gbp.profile_url`
   should auto-detect if the LSA account uses the same Google account.

### Phase 3 gate

LSA account created. Trade category, job types, service area, and GBP all
configured. Account is in "pending verification" state.

**Output:** LSA account URL saved. Config updated with account creation date.

---

## Phase 4 — Verification

**Goal:** Submit all documents, trigger background checks, and track the
multi-day verification process to completion.

### Steps

1. **Upload license.** Submit the digital copy through the LSA dashboard.
   Google verifies against state/local licensing databases.

2. **Upload insurance certificate.** Submit the ACORD-25 cert. Google verifies:
   - Coverage ≥ $1M per occurrence
   - Business name exact match
   - Policy is current (not expired)

3. **Trigger owner background check.** Google's partner (Evident or Checkr)
   runs an identity + criminal history check on the owner. This includes:
   - Cross-check against national sex offender registry
   - Cross-check against terrorist/sanctions registries
   - Criminal history research
   - The owner will receive a separate email from the background check provider
     with instructions. Ensure `config.owner_name` is aware and expecting it.

4. **Trigger technician background checks.** For each entry in
   `config.technicians[]`:
   - Submit the technician's information through the LSA dashboard.
   - Each tech receives their own background check email.
   - Track status per technician in the config: `"background_check_status"`:
     `"pending"` → `"in_progress"` → `"passed"` / `"failed"`.
   - **Annual renewal:** these checks renew every 12 months. Note the
     anniversary date.

5. **Track verification status.** The LSA dashboard shows per-item status.
   Check daily until all items show approved.
   - **Expected timeline: 1–4 weeks** (conservative; depends on background
     check provider throughput and document quality).
   - Common rejection reasons:
     - Insurance business name mismatch (fix: reissue cert)
     - License scope doesn't match selected categories (fix: adjust categories
       or obtain broader license)
     - Background check issue (escalate to operator)

### Phase 4 gate

All verification items approved. The **"Google Verified" badge** is live on the
client's LSA listing.

> **Badge context (Oct 2025 change):** Google retired "Google Guaranteed,"
> "Google Screened," and "License Verified by Google" badges on Oct 20, 2025
> and replaced them with a unified **"Google Verified"** badge. The consumer
> money-back guarantee tied to the old "Google Guaranteed" badge was
> **discontinued Oct 20, 2025.** Verification requirements (license, insurance,
> background checks) are unchanged. The badge is now purely a trust signal,
> not a financial guarantee.

**Output:** Verification completion date recorded. Badge confirmed live.

---

## Phase 5 — Configuration

**Goal:** Optimize the account settings for maximum ROI within the budget
constraint before turning on lead flow.

### Budget

- **Monthly budget:** `config.budget.monthly_usd` (default: $300/month).
- **Weekly pacing:** `config.budget.weekly_pacing`.
  - `"even"` = Google distributes ~$75/week (on a $300/mo budget).
  - `"manual"` = operator sets custom weekly caps.

### Honest expectations at $300/month

At metro-DC CPL of **$75–$90 per lead** (the realistic planning number for
DC/MD/VA — see research report), $300/month buys **~3–4 leads per month.**

That sounds small, but the math works because electrical jobs are high-value:
- Electrical panel replacement (metro DC): $2,400–$3,500
- EV charger install (metro DC): $1,200–$2,500
- At ~44% average book rate → ~1–2 booked jobs/month
- **One booked panel job pays for several months of ad spend.**

Two levers make $300 go further:
1. **Fast response.** Google rewards fast responders with more leads. Target:
   answer within `config.response.target_seconds` seconds.
2. **High-value job-type weighting.** Enabled via `config.job_types.high_value`.

### Service area

Review `config.service_area.zip_codes` one final time before go-live.

**Rule: if you wouldn't drive there for a $300 job, don't include the ZIP.**
Off-area leads are no longer creditable (2024 policy change). Every extra ZIP
is potential waste.

### Job types

Review `config.job_types.enabled` and `config.job_types.high_value`.

**Weighting strategy:** enable the full set of job types you can serve, but
weight toward high-value categories. Google's algorithm doesn't let you set
explicit weights, but you can influence lead mix by:
- Enabling fewer low-value categories (e.g., skip "light bulb replacement")
- Keeping high-value categories active (panel upgrades, EV chargers, rewiring)
- Responding faster to high-value lead types (the response-time signal)

### Hours + response path

- Set business hours from `config.hours`. LSA shows "Open now" / "Closed"
  based on these hours. Accurate hours = fewer wasted leads during off-hours.
- Confirm `config.response.who_answers` and `config.response.target_seconds`.
  Document the response path: lead comes in → [who sees it] → [how fast they
  respond] → [what they say].

### Phase 5 gate

Budget, service area, job types, hours, and response path all configured and
reviewed. Account is ready to go live.

**Output:** Config JSON fully populated. Account settings screenshot for
operator records.

---

## Phase 6 — Go-live checklist

**Goal:** Final pre-launch verification, then activate lead flow and hand off
to the management process.

### Pre-launch checks

- [ ] Google Verified badge confirmed live on the listing
- [ ] Business hours accurate and matching `config.hours`
- [ ] Service area = only the ZIPs in `config.service_area.zip_codes`
- [ ] Job types = only the categories in `config.job_types.enabled`
- [ ] Budget set to `config.budget.monthly_usd` with correct pacing
- [ ] Response path documented: who answers, target response time
- [ ] Owner knows to expect lead notifications (phone call / LSA app / email)
- [ ] Owner briefed on lead-rating workflow (rate every lead; "Very
      dissatisfied" is the only rating that triggers credit review)

### Activate

Turn on the LSA campaign in the dashboard. Leads begin flowing.

### Handoff to B2 (`lsa-management`)

At go-live, the `lsa-management` skill takes over. The handoff contract:

| Item | Value | Source |
|---|---|---|
| Client slug | `config.client_slug` | Config JSON |
| LSA account URL | (recorded at Phase 3) | Operator |
| Go-live date | (today) | Phase 6 |
| Monthly budget | `config.budget.monthly_usd` | Config JSON |
| Expected leads/month | ~3–4 at metro CPL | Research report |
| Expected book rate | ~44% (industry benchmark) | Research report |
| Response path | `config.response.*` | Config JSON |
| Lead-rating workflow | Rate every lead; "Very dissatisfied" for bad leads | SOP |
| First weekly review due | Go-live date + 7 days | Calculated |

### Phase 6 gate

LSA campaign live. First lead notification pathway tested (operator confirms
they received a test or real lead notification). Management handoff complete.

**Output:** Go-live date recorded. B2 management process activated.

---

## Lead quality context (load-bearing — read before configuring)

Google made significant changes to LSA lead quality protections in 2024–2025
that directly affect how you configure and manage the account:

1. **Manual lead disputes removed (mid-2024).** You can no longer manually
   dispute individual leads. The automated system reviews leads within ~72
   hours and applies credits within ~30 days when warranted.

2. **"Job type not serviced" and "geo not serviced" leads are no longer
   creditable.** If you get a lead for a job type you don't do or an area you
   don't serve, you pay for it with no recourse. This is why Phase 5's
   service area and job type configuration is so important.

3. **The only operator lever is the "Rate this lead" tool.** Selecting **"Very
   dissatisfied"** is the only rating that triggers a credit review. Rate
   every bad lead promptly. This is a weekly habit managed by `lsa-management`.

4. **67% of contractors reported lead quality declined** over the prior 18
   months (2025 survey). Tight configuration + active lead rating is the
   defense.

## Duplicability

This skill is trade-agnostic. The 6-phase SOP applies identically to any
LSA-eligible trade. To set up LSA for a non-electrician client:

1. Copy any existing config to `lsa-config-<new_client_slug>.json`.
2. Change `trade` to the new trade (e.g., `"plumber"`, `"hvac"`).
3. Update license fields to match that trade's licensing requirements.
4. Update job types to that trade's LSA categories.
5. Update service area ZIPs for that client's market.
6. Run the 6 phases. Nothing in the phases assumes electrician.

See `configs/lsa-config-example-plumber.json` for a non-electrician proof.

## Sources (verified 2026-06-23)

- Google Local Services Help — Business screening and verification requirements (US): https://support.google.com/localservices/answer/12174778
- Google Local Services Help — How providers qualify: https://support.google.com/localservices/answer/6230381
- Google Local Services Help — Screening and verification process: https://support.google.com/localservices/answer/6226575
- Coalmarch — Google LSA Updates 2024-2025: https://www.coalmarch.com/resources/blog/google-lsa-automated-credits-verified-badge-updates
- PinPoint Promote — LSA for Electricians: https://pinpointpromote.com/resources/electrician-local-service-ads-guide
- Widewail — LSA Eligibility & Verification: https://www.widewail.com/blog/google-local-service-ads-eligibility-verification-and-best-practices
- SearchEn — Google Verified badge Oct 2025: https://www.searchen.com/2025/09/30/google-unifies-trust-signals-all-local-services-ads-to-show-google-verified-badge-starting-october-2025/
- `[[research-2026-06-06-lsa-economics-dc-md-va-electrical]]` (vault economics research)
- `[[lsa-plain-language-guide]]` (vault plain-language reference)

## See also

- `[[handoff-2026-06-23-b1-lsa-setup-skill]]` — the handoff that spawned this skill
- `[[handoff-2026-06-23-b2-lsa-management-skill]]` — the downstream management skill
- `[[handoff-2026-06-23-b3-lsa-verification-gate-start]]` — operator verification gate
- `[[research-2026-06-06-lsa-economics-dc-md-va-electrical]]` — full economics report
