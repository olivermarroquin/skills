---
type: operator-checklist
status: active
created: 2026-06-23
updated: 2026-06-23
client: ev-electric-services
skill: lsa-setup
tags: [checklist, lsa, ev-electric-services, operator]
---

# LSA Setup — Operator Checklist: EV Electric Services

**Client:** EV Electric Services
**Owner:** Ahmad Shaban
**Trade:** Electrician (Master Electrician, Virginia)
**Config:** `skills/lsa-setup/configs/lsa-config-ev-electric-services.json`

---

## Phase 1 — Eligibility check

- [x] Trade eligible for LSA: **Electrician** — supported in all US markets
- [x] License exists: Master Electrician, Commonwealth of Virginia DPOR
- [ ] License number gathered from Ahmad: `__________`
- [ ] Insurance confirmed ≥$1M GL: carrier `__________`, policy # `__________`
- [ ] Insurance expiry date: `__________`
- [x] GBP verified: **Yes** (both EV and S&H already verified)

## Phase 2 — Document gather

| # | Document | Status | Notes |
|---|----------|--------|-------|
| 1 | Virginia Master Electrician license (digital copy) | [ ] Collected | Ask Ahmad for license number + PDF/photo |
| 2 | $1M GL insurance certificate (ACORD-25 format) | [ ] Collected | Business name on cert MUST say exactly **"EV Electric Services"** — if it says "EV Electric Services LLC" or any variant, have insurer reissue (same-day, free) |
| 3 | Owner government ID (Ahmad Shaban) | [ ] Collected | Driver's license or passport |
| 4 | Technician roster for background checks | [ ] Collected | List every tech who will do LSA jobs. Each needs individual background check |

**Technicians identified:**
- [ ] `__________`
- [ ] `__________`
- [ ] (add rows as needed)

**Questions for Ahmad:**
- What Google account email should the LSA be created under? (Should match the GBP owner account)
- How many technicians besides Ahmad will do jobs under this account?
- What is the fastest realistic response time to a new lead? (Target: under 5 minutes)

## Phase 3 — Account creation

- [ ] LSA account created at ads.google.com/local-services-ads
- [ ] Google account used: `__________`
- [ ] Business category selected: **Electrician**
- [ ] Job types selected (from config):
  - [x] Electrical Panel Upgrade (**high-value**)
  - [x] EV Charger Installation (**high-value**)
  - [x] Electrical Wiring (**high-value**)
  - [x] Electrical Troubleshooting
  - [x] Outlet Installation & Repair
  - [x] Light Fixture Installation
  - [x] Smoke & Carbon Monoxide Detector
  - [x] Emergency Electrical Service
- [ ] Service area set: 16 ZIPs covering Fairfax, Vienna, McLean, Oakton, Tysons, Falls Church, Burke, Annandale
- [ ] GBP linked
- [ ] LSA account URL: `__________`

## Phase 4 — Verification

- [ ] License uploaded to LSA dashboard
- [ ] Insurance certificate (ACORD-25) uploaded
- [ ] Owner background check triggered (Ahmad Shaban)
  - [ ] Ahmad received email from Evident/Checkr
  - [ ] Ahmad completed the background check
- [ ] Technician background checks triggered:
  - [ ] `__________` — status: `__________`
  - [ ] `__________` — status: `__________`
- [ ] All items approved in LSA dashboard
- [ ] **Google Verified badge live**
- [ ] Verification complete date: `__________`

**Expected timeline:** 1–4 weeks from complete document submission.

## Phase 5 — Configuration

- [ ] Budget set: **$300/month**, even weekly pacing (~$75/week)
- [ ] Service area reviewed (16 ZIPs — tight, no sprawl)
- [ ] Job types reviewed (8 enabled, 3 high-value weighted)
- [ ] Hours confirmed: Mon–Fri 8am–6pm, Sat 9am–4pm
- [ ] Response path documented:
  - Who answers: **Ahmad Shaban (owner)**
  - Target response time: **5 minutes (300 seconds)**
  - Notification method: `__________` (phone call / LSA app / email)

### Budget expectations (honest)

| Metric | Value | Source |
|--------|-------|--------|
| Metro CPL (DC/MD/VA) | $75–$90 per lead | 2026-06-06 research |
| Leads/month at $300 | ~3–4 | Calculated |
| Average book rate | ~44% | Industry benchmark |
| Booked jobs/month | ~1–2 | Calculated |
| Panel upgrade value | $2,400–$3,500 | Fairfax market |
| EV charger value | $1,200–$2,500 | Fairfax market |

## Phase 6 — Go-live

- [ ] Google Verified badge confirmed live
- [ ] Business hours accurate
- [ ] Service area = only the 16 configured ZIPs
- [ ] Job types = only the 8 configured categories
- [ ] Budget = $300/month with even pacing
- [ ] Response path documented and Ahmad briefed
- [ ] Ahmad knows to expect lead notifications
- [ ] Ahmad briefed on lead-rating workflow:
  - Rate every lead
  - **"Very dissatisfied" for bad leads** (only rating that triggers credit review)
  - Do this promptly — don't let bad leads sit unrated
- [ ] **LSA campaign activated**
- [ ] Go-live date: `__________`
- [ ] **Handoff to B2 (`lsa-management`) complete**

---

## Notes

- EV and S&H are **direct competitors** in overlapping service areas. Separate configs, separate accounts, never cross-contaminate data.
- Both configs share some ZIP codes (22031, 22101, 22102, 22124, 22003) — this is expected. They compete in the same market.
