---
type: skill-reference
skill: market-intelligence-engine
created: 2026-06-16
updated: 2026-06-16
tags: [skill-reference, market-intelligence, worked-example, electrician]
---

# Worked example — Electrician field (NoVA residential)

This is the provenance document linking the `market-intelligence-engine` skill to the proven run
that it was distilled from. Every phase in the SKILL.md maps to a real execution step.

---

## Run config (as it would be expressed in v1.0)

```yaml
field:
  name: "residential-electrician"
  region: "Northern Virginia (NoVA)"
  head_terms:
    - "electrician near me"
    - "electrical repair <city>"
    - "panel upgrade <city>"
    - "EV charger installation <city>"
    - "residential electrician <city>"
    - "emergency electrician <city>"
    - "whole house rewire <city>"
    - "generator installation <city>"

clients:
  - name: "EV Electric Services"
    domain: "evelectricservices.com"
    slug: "ev-electric-services"
    gbp_name: "EV Electric Services"
  - name: "S&H Contracting"
    domain: "sandhcontracting.com"
    slug: "s-and-h-contracting"
    gbp_name: "S&H Contracting Inc."

competitors:
  seed_domains:
    - "rootelectricservices.com"
    - "ajlongelectric.com"
    - "proelectricllc.com"
    - "kolbelectric.com"
    - "absoluteelectricinc.com"
    - "mrelectricfredericksburg.com"
    - "goudieelectric.com"
    - "rojaselectricva.com"
    - "thesparkerva.com"
    - "vpservicesllc.com"
    - "samandsonselectric.com"
    - "misterrogerselectric.com"
    - "sparkwisesolutions.com"
    - "poppyselectric.com"
    - "lightspeedelectricva.com"
  top_n_light: 15
  top_n_deep: 5
  retain_incumbents:
    - "ajlongelectric.com"  # operator-retained: popular, high-review incumbent

arenas_in_scope: [V1, V2, V3, V4, V5, M1, M2, A1]

substrate:
  host_side: true
  chrome_connected: true   # MI-3b + MI-3c used Chrome
  cowork: true             # MI-3 started in Cowork

output_folder: "second-brain/_meta/handoffs/market-intelligence/"
data_folder: "second-brain/_meta/handoffs/market-intelligence/mi-data/"
```

---

## Phase-to-artifact mapping

| Engine phase | Proven run artifact | Location |
|---|---|---|
| Phase 0: Substrate preflight | MI-3 hit Cowork limits → MI-3b moved host-side | `mi3-limitations-and-lessons-2026-06-14.md` §A |
| Phase 1: Competitor set | 15 organic-seeded + local-pack reference tier | `mi3-composite-scorecard-2026-06-14.md` §1 |
| Phase 2: Arena-source enum | Source checklist created post-MI-3 | `mi-arena-source-checklist.md` |
| Phase 3: Collection | DataForSEO + Sonar + Chrome + Transparency Center | `mi3-composite-scorecard-2026-06-14.md` §Method, `mi3b-composite-scorecard-update-2026-06-15.md` §Method |
| Phase 4: Completion-vs-plan | MI-3b audit found DG-9 at 17%, DG-7 at 10/17 | `mi3-limitations-and-lessons-2026-06-14.md` §L2 |
| Phase 5: No-undefended-zero | V4 "empty" → 7 competitors running 10+ ads | `mi3b-composite-scorecard-update-2026-06-15.md` §2b |
| Phase 6: Adversarial pass | Gap-finder applied to own conclusions | `mi3-limitations-and-lessons-2026-06-14.md` §L1 |
| Phase 7: Scoring | 17 x 8 scorecard, every cell sourced | `mi3b-composite-scorecard-update-2026-06-15.md` §9 (V4-corrected final) |
| Phase 8: Deep-N teardowns | Top-5 + AJ Long (retained) via site-capture-engine | Pre-MI-3 teardown artifacts in per-client `admin-extracts/competitor-research/` folders (e.g., `ev-electric-services/admin-extracts/competitor-research/aj-long-teardown/`, `ev-electric-services/admin-extracts/competitor-research/root-electric-teardown/`). Location varies by client folder; no single canonical path. |
| Phase 9: Gap-discovery | DG-1 through DG-19 accumulated | `_data-gap-register.md` |
| Phase 10: Output A | Field perfect company profile | `mi4-perfect-company-profile-2026-06-16.md` |
| Phase 11: Output B | EV + S&H gap plans | `mi4-per-client-gap-plans-2026-06-16.md` |
| Phase 12: Residuals | 7 focused-run residuals queued | `mi3-residuals-followup-queue-2026-06-16.md` |
| Phase 13: Independent gate | G-market-intel: producer self-check + independent review | `mi4-per-client-gap-plans-2026-06-16.md` §Gate verdict |
| Ad-intelligence module | 142 distinct creatives across 10 advertisers | `mi3c-swipe-file-*.md` + `mi3c-data/ads/*/` manifests |

---

## Key lessons that shaped the skill design

1. **V4 ads miss (MI-3 → MI-3b):** Single-source "empty" was wrong. 7 competitors running 10+ ads.
   → Arena-source-enumeration phase + no-undefended-zero guard + Transparency Center as mandatory V4
   source.

2. **Silent partial completion (MI-3b):** DG-9 "done" at 17%, DG-7 "closed" at 10/17 competitors.
   → Completion-vs-plan diff phase (planned vs collected, verified against raw artifact).

3. **Self-gating (MI-3b):** The run graded its own work. Blind spots invisible.
   → No-self-gating rule: independent review must actually run.

4. **Substrate limitations (MI-3):** Cowork's 45s cap + no Chrome → incomplete collection.
   → Substrate routing rule: heavy collection host-side, JS/web-app via Chrome, Cowork for synthesis only.

5. **Gaps fail loud (MI-3 L0):** Limitations were logged but not surfaced in the summary.
   → Standing rule L0: headline-level limitations block, every run, no exceptions.

6. **Local-pack-seeded tier (MI-3b DG-15):** Companies dominating Maps with zero organic presence
   (Beacon 5,918 reviews, Michael & Son 16,000+) were invisible to organic-only competitor seeding.
   → Phase 1 includes local-pack tier discovery; promote to main set if they also appear in paid/organic.

7. **Review velocity != review count (MI-3b M1):** AJ Long count leader (1,147) but plateaued.
   Absolute velocity leader (~12.8/mo). Different competitive positions.
   → M1 scoring distinguishes count vs velocity; both are scored.

---

## Cost summary (proven run)

| Phase | Spend |
|---|---|
| MI-3 (DataForSEO + Sonar) | ~$1.30 |
| MI-3b (DataForSEO batch + coord-grid + SERP sweep) | ~$1.84 |
| MI-3c (Chrome ad scrape) | $0 |
| MI-4 (synthesis, no API calls) | $0 |
| **Total** | **~$3.14** |

The per-field cost is dominated by DataForSEO API calls. Subsequent runs in the same field
(re-scoring) will be cheaper as competitor sets are already confirmed.
