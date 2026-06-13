---
type: reference
status: active
skill: website-design
description: Input contract — the minimum viable set of inputs for a website-design run
created: 2026-06-12
updated: 2026-06-12
tags: [reference, website-design, input-contract]
---

# Input contract — website-design skill

The skill requires these inputs before a design run begins. Missing required inputs produce a
mockup that argues no one's claim — stop and ask before proceeding.

## Required inputs

### 1. Client brief

**Source:** `prospect-intake` output, `client-fact-research` output, or operator-provided.

**Minimum fields:**

| Field | Example | Why it matters |
|---|---|---|
| Business name | (confirmed correct spelling) | Correct spelling — existing sites often misspell their own name |
| Owner/contact | (first name + role) | Founder-presence section needs a name |
| What they do | (trade + service lines) | Service cards + hero copy |
| Target buyer | (job titles of the people who buy) | Copy voice + fear identification |
| Scale claims | (revenue, years, partners, project count) | Proof-point spine content |
| Certifications | (e.g., MBE, WOSB, 8(a), license #) | Credibility section + transactional framing |
| Service area | (corridor + HQ location) | Service-area section, schema |
| Verticals | (industry segments served) | Verticals section |
| Phone | (confirmed primary number) | Sticky nav, CTAs, schema |
| Address | (confirmed current address) | Footer, schema |

### 2. Content inventory

**Source:** Extracted from existing site, provided by client, or drafted from brief.

| Content type | What's needed | Fallback if absent |
|---|---|---|
| Service descriptions | 2-3 sentences per service + differentiators | Draft from brief + research |
| Stats/proof points | Hard numbers (revenue, years, projects, certs) | Use brief's claims with `<confirm>` |
| Portfolio items | 3-4 projects with scope, challenge, outcome | Draft realistic placeholders from brief |
| Brand partners | Logo list or partner names | List names, use text + CSS styling |
| Testimonials | 1-3 quotes with attribution | Omit section or use "What our clients say" placeholder |
| Team/founder info | Bio, photo, role | Draft from brief; photo = Higgsfield hook |
| Contact info | Phone, email, address, hours | From brief; hours = `<confirm>` |

### 3. Design direction (at least ONE)

| Source | What it provides | Example |
|---|---|---|
| Teardown dossier | Design tokens, layout patterns, section conventions | AJ Long teardown → design-tokens.md |
| Reference URL | Visual bar to match or exceed | "At the level of ajlongelectric.com" |
| Brand guidelines | Colors, fonts, logo, imagery rules | Client-provided style guide |
| Positioning statement | Implies visual direction | "Government-grade + premium contractor" |

## Optional inputs

| Input | Default if absent |
|---|---|
| Existing brand assets (logo, photos) | Derive palette from positioning; use constraint-as-asset for imagery |
| Page scope | Homepage |
| Imagery constraints | Constraint-as-asset (no photography, no AI) |
| Reference patterns | Derive from brief + niche conventions |

## Validation checklist (run before starting Step 2)

- [ ] Business name confirmed spelled correctly
- [ ] At least 3 proof points with numbers
- [ ] Target buyer identified (not just "customers")
- [ ] At least one design direction source present
- [ ] Phone number confirmed
- [ ] Service list complete (not "and more")
