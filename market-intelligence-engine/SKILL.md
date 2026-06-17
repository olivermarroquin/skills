---
type: skill
skill: market-intelligence-engine
version: 1.1
created: 2026-06-16
updated: 2026-06-16
status: active
substrate: claude-code
gate: G-market-intel
tags: [skill, market-intelligence, competitive-intelligence, orchestrator, multi-arena, config-driven]
---

# Skill — `market-intelligence-engine` v1.1

A **config-driven, multi-arena competitive-intelligence orchestrator** that scores the top competitors
in a client's field across every marketing arena, identifies who wins each arena and why, surfaces
data + tool gaps, and synthesizes the "perfect company profile" to beat them all — plus per-client
gap-to-action plans. Duplicable for any client in any field from config alone.

**Distilled from:** the proven [MI-3]/[MI-3b]/[MI-3c]/[MI-4] electrician-field run (2026-06-14 → 2026-06-16).

**House methodology:** skills are extracted from real runs, not written speculatively. Every phase below
was executed and validated before codification. See `references/worked-example-electrician.md` for the
full provenance.

---

## 0. Config contract (zero hardcoded values)

Every run is parameterized by a config block. The engine has **no** hardcoded client names, domains,
cities, services, or field-specific values.

```yaml
# --- market-intelligence-engine run config ---
field:
  name: ""                    # e.g. "residential-electrician"
  region: ""                  # e.g. "Northern Virginia (NoVA)"
  head_terms: []              # e.g. ["electrician near me", "electrical repair <city>", ...]

clients:                      # 1..N clients sharing this field
  - name: ""
    domain: ""
    slug: ""                  # vault folder slug
    gbp_name: ""              # Google Business Profile name (for DataForSEO lookups)

competitors:
  seed_domains: []            # initial competitor list (organic + AI + local-pack tiers)
  top_n_light: 15             # scored across all arenas at light tier
  top_n_deep: 5               # full site-capture-engine teardown
  retain_incumbents: []       # popular incumbents kept in deep set regardless of rank

arenas_in_scope:              # which arenas to run this phase (default: all standard)
  - V1  # Google organic
  - V2  # Local pack / Maps
  - V3  # AI answer engines
  - V4  # Paid / LSA
  - V5  # Social / video
  - M1  # Reviews / reputation
  - M2  # Conversion / offer
  - A1  # Topical authority / E-E-A-T
  # B2G arenas (add for government-contracting fields — see §3a):
  # - G1  # Contract awards / past performance (USASpending/FPDS/SAM)
  # - G2  # Set-aside / socioeconomic certs (SBA DSBS / certify.SBA.gov)
  # - G3  # Contract vehicles / schedules (GSA eLibrary / agency vehicle lists)
  # - G4  # Capability & compliance positioning (NAICS/PSC, CMMC, clearances)
  # - G5  # Agency relationships / incumbency (USASpending expiring-award queries)
  # - G6  # Teaming / partner network (USASpending sub-award data, JV registrations)

substrate:
  host_side: true             # Claude Code (no timeout cap)
  chrome_connected: false     # set true if Claude-in-Chrome available
  cowork: false               # Cowork sandbox (45s cap, no Chrome)

output_folder: ""             # e.g. "second-brain/_meta/handoffs/market-intelligence/"
data_folder: ""               # e.g. "second-brain/_meta/handoffs/market-intelligence/mi-data/"
```

**Validation rule:** the engine refuses to start if `field.name`, `clients[]`, or `competitors.seed_domains[]`
are empty. No defaults are assumed — the operator must provide them.

---

## 1. Composition map — what this skill orchestrates (spec §2a boundaries)

This skill **composes** existing skills. It does not duplicate their internals. Each composed skill
owns its domain; this engine owns the **cross-arena roll-up, scoring, synthesis, and gap engine**.

| Composed skill | Version | What it owns (engine calls it) | What stays OUT of this engine |
|---|---|---|---|
| `competitor-deep-research` | v1.4 | Organic/content landscape: Tier-2 15-column scan (incl. cols 11-15: V3/V2/V4/M1/V5 arena-presence flags), Tier-1 deep briefs, cross-competitor synthesis | The raw signal capture. Engine interprets the flags into 0-5 scores. |
| `site-capture-engine` | v2.2 | Deep-N forensic teardown: full site anatomy, tech stack, what ranks, local-pack snapshot (Pass 3 step 6), review-velocity snapshot (Pass 4 step 2) | Point-in-time snapshots. Engine owns trend analysis + geo-grid coverage. |
| `seo-tooling-landscape-research` | v2.0 | Tool-gap engine: `_data-gap-register` append, discovery mode (emerging tools), intake mode (digest a tool), tool-eval rubric | Tool adoption decisions stay there. Engine reads the register, routes tool-gap findings. |
| `multi-source-synthesis` | v1.0 | Perfect-profile synthesis (Output A) + per-client gap plan (Output B) via cross-cluster or client-driven shape | Engine feeds it structured arena data; synthesis skill produces the document. |
| `service-seo-research` / `city-base-research` / `intersection-research` / `client-fact-research` | latest | Data-gathering layer (service taxonomies, city lists, intersection pages, client facts) | Input to scoring. Engine consumes their outputs, does not re-implement. |
| `perplexity-research-suite` (Sonar) | latest | AI-surface probes (V3), general deep-research | Engine calls Sonar for V3 probes; does not wrap the suite. |
| `ad-intelligence` module (from [MI-3c]) | v1.0 | Paid-arena (V4) ad-creative capture via Google Ads Transparency Center + optional Meta Ad Library | Chrome-dependent. Engine routes V4 to this module. See `references/ad-intelligence-module.md`. |

### Boundaries against sibling programs (spec §2a)

| Sibling | Boundary |
|---|---|
| `opportunity-radar` / [OR-1] | OR scans *products/offers* → `idea-factory`. MI scans *competitive marketing* → `website-factory` + `local-seo-growth`. Different input (market vs product), different output. If OR-1 lands a shared "opportunity-teardown substrate," reuse its scoring/registry shape. |
| [T2-G2] website-research generalization | T2-G2 = *per-site report* generalization. MI = *whole-market multi-arena roll-up*. MI can consume T2-G2 per-site reports as input. |
| `local-seo-growth` [G1]-[G7] | LSG *executes* local-pack + reviews arenas (GBP optimization, review engine, citations). MI *measures* competitors in those arenas and feeds gaps in. MI does not re-implement the doing. |
| `website-factory` | Consumes MI's page/content ideas + new-page ideas. MI produces ideas; factory builds them. |
| `design-inspiration-system` [DI-7] | Design-quality discovery. MI's M2 conversion/UX arena references it for the design dimension rather than re-scoring aesthetics. |

---

## 2. Phases — the engine execution flow

### Phase 0 — Substrate preflight

1. Parse and validate config (all required fields non-empty).
2. **Per-client provisioning preflight** (added v1.1, MI-8):
   - For each client in `clients[]`, verify:
     - Tool account access: DataForSEO credentials live, Local Falcon location added (if V2 in scope),
       BrightLocal location added (if M1 in scope), Otterly workspace configured (if V3 in scope).
     - For B2G fields (G-arenas in scope): SAM.gov API key or Chrome access confirmed,
       USASpending API reachable (public, no key needed).
     - Chrome profile logged in to required services (SAM.gov, GSA eLibrary, SBA DSBS, LinkedIn)
       if Chrome-dependent arenas are in scope.
   - Emit a **provisioning checklist** per client: `✅ ready` / `⚠️ needs setup` / `❌ blocked` per tool.
   - **Do not silently skip a blocked tool.** Flag it, name the owning follow-up, and proceed with
     the available substrate.
3. **Substrate check:**
   - If any Chrome-dependent arena is in scope (V4 ad-intelligence, M2 JS-rendered sites, V2 geo-grid tools,
     G2 SBA DSBS, G3 GSA eLibrary, G4 SAM.gov entity detail):
     confirm Chrome is connected. If not → **STOP and tell the operator.** Do not silently substitute WebFetch.
   - If running in Cowork: flag 45s timeout cap. Route slow/batch calls (DataForSEO `my_business_info` batch,
     geo-grid, multi-competitor SERP sweeps) to host-side. Emit a limitations block.
4. **Substrate routing rule** (from standing rule from MI-3 lessons — see `[[mi3-limitations-and-lessons-2026-06-14]]` §E):
   - Host-side (Claude Code): slow batches, DataForSEO bulk calls, USASpending/FPDS API, any call >20s.
   - Chrome: JS-rendered competitor sites, Google Ads Transparency Center, Local Falcon, BrightLocal,
     SAM.gov, GSA eLibrary, SBA DSBS, LinkedIn, GovWin.
   - Cowork: synthesis, scoring, writing — never heavy collection.
   - **Verify substrate before run.** If a planned source requires a substrate that isn't available,
     skip it with reason + owning follow-up — never silently substitute.
   - **Escalate WebFetch-empty to Chrome.** A JS-rendered page returning empty from WebFetch is not
     a "no data" result — it's a substrate limitation. Escalate to Chrome, or mark as residual with
     the correct root cause.

### Phase 1 — Competitor set confirmation

1. Ingest `competitors.seed_domains[]` from config.
   - For B2G fields: if `seed_domains[]` is empty, **generate the seed set** from USASpending API
     (`spending_by_category/recipient` filtered by field NAICS codes + relevant set-aside types).
     Pull top awardees by volume → these become the seed competitors.
2. Cross-reference with `competitor-deep-research` Tier-2 scan results if available.
3. Add local-pack-seeded tier: competitors that dominate Maps on review volume but have near-zero
   organic presence (discovered in MI-3b). These are scored in a reference tier, promoted to main
   set if they also appear in paid/organic.
   - **For B2G fields:** this tier is typically empty (local pack is N/A). Instead, add a
     **set-aside-seeded tier:** firms that win heavily in restricted set-aside pools (8(a), SDVOSB,
     WOSB, HUBZone) but have low open-market visibility. Promoted to main set if they also appear
     in vehicle-based competition.
4. Confirm the final set with the operator before scoring. Target: `top_n_light` (default 15) + clients.

### Phase 2 — Arena-source enumeration (mandatory — from `[[mi-arena-source-checklist]]`)

For each arena in scope, **before any data collection**:

1. Load the per-arena source checklist from `references/arena-source-checklist.md`.
2. For each arena, list every source (primary, secondary, public registries).
3. Mark each source as:
   - **PLANNED** — will be queried this run (with substrate noted).
   - **SKIPPED** — with reason (e.g., "Chrome not connected", "tool not subscribed") + owning follow-up.
4. Emit the filled enumeration as a run artifact (table per arena).
5. **No silent single-sourcing.** If an arena has only 1 planned source, flag it explicitly.

This phase operationalizes spec §7 check #5: per-arena source checklist filled.

### Phase 3 — Data collection (routed by substrate)

For each arena, collect data from all PLANNED sources per Phase 2:

| Arena | Collection method | Substrate |
|---|---|---|
| V1 Google organic | DataForSEO `domain_rank_overview` + `ranked_keywords` per competitor | Host-side |
| V2 Local pack | DataForSEO SERP `local_pack` + Local Falcon geo-grid (if Chrome) + manual map check. **Geo-grid anchor fallback (v1.1, from `[[pattern-geo-grid-anchor-on-located-competitor-for-misgeocoded-SAB]]`):** if the client is a service-area business (SAB, no map pin) or has a mis-geocoded GBP, anchor the geo-grid on a correctly-located competitor in the target service area instead. The client will appear (or not) in the Competitor Report's ranked list — their absence/deep-rank quantifies the local cost of the GBP problem. Do NOT scan the wrong geocode; recognize the anomaly first. | Host-side + Chrome |
| V3 AI engines | Perplexity Sonar probes + Otterly/AI-citation monitor + manual probes | Host-side + Chrome |
| V4 Paid / LSA | Google Ads Transparency Center (Chrome) + live SERP ads sweep (mobile+desktop × geos) | Chrome + Host-side |
| V5 Social / video | Direct channel visits (IG/TikTok/YT/FB) + competitor site embed check | Chrome |
| M1 Reviews | DataForSEO `my_business_info` batch + BrightLocal + SERP local_pack rating | Host-side |
| M2 Conversion | `site-capture-engine` homepage capture + tech detection | Chrome (JS sites) |
| A1 Authority | DataForSEO `backlinks/summary` + `referring_domains` + entity/KG probe | Host-side |
| **G1 Awards** (B2G) | USASpending API `spending_by_category/recipient` by NAICS + set-aside filters; FPDS for granular award detail | Host-side |
| **G2 Set-aside certs** (B2G) | SBA DSBS / certify.SBA.gov (Chrome) + SAM.gov entity reps & certs (Chrome) + USASpending set-aside inference | Chrome + Host-side |
| **G3 Contract vehicles** (B2G) | GSA eLibrary SIN search (Chrome) + agency vehicle lists + web search for OASIS+/GWAC holdings | Chrome + Host-side |
| **G4 Capability/compliance** (B2G) | Competitor websites (WebFetch or Chrome) + SAM.gov NAICS/PSC detail (Chrome) + CMMC marketplace | Host-side + Chrome |
| **G5 Agency/incumbency** (B2G) | USASpending `spending_by_category/awarding_agency` + expiring-award queries + GovWin (Chrome) | Host-side + Chrome |
| **G6 Teaming** (B2G) | USASpending sub-award data + web search for JV/mentor-protégé announcements + SAM.gov JV registrations | Host-side + Chrome |

**Ad-intelligence module (V4 deep pass):** When Chrome is connected and V4 is in scope, invoke the
ad-intelligence module (see `references/ad-intelligence-module.md`) for the full creative capture:
per-advertiser Transparency Center scrape → themed swipe file → synthesis + per-client ad-angle
recommendations.

### Phase 4 — Completion-vs-plan diff (mandatory — spec §7 check #7)

After collection, for every arena:

1. Diff **planned units** (from Phase 2) vs **collected units** (verified against RAW artifacts, not prose).
2. Report: "X of Y collected" per arena per source.
3. An arena may **NOT** be marked "closed" below its coverage threshold without naming the gap.
4. Early-stop or empty-result must be stated explicitly with root cause.
5. Emit the completion ledger as a run artifact.

**Precipitating event:** MI-3b marked DG-9 done at ~17% (2 of 12 grid-terms) and DG-7 "closed" after
10 of 17 competitors. The gate passed because every cell that existed was sourced — but completeness
was never checked.

### Phase 5 — No-undefended-zero guard (mandatory — spec §7 check #4)

For every arena cell about to be scored 0 or "absent":

1. Check: does this zero meet the three completeness rules from `[[mi-arena-source-checklist]]`?
   - **Rule 1:** ≥2 independent sources checked AND breadth across the arena's dimensions.
   - **Rule 2:** Source enumeration (Phase 2) shows the sources were used, not just planned.
   - **Rule 3:** Adversarial pass (Phase 6) attempted to disprove it.
2. If all three rules are met → **defended zero** (label: "0 — defended: [sources] × [dimensions]").
3. If any rule is unmet → the cell reads **"unknown / under-sampled"**, not 0. Flag as a residual.

**Precipitating event:** MI-3 scored V4 "empty" from one tool on 8 desktop queries. PRO Electric was
running Search ads. The full Chrome + Transparency Center sweep in MI-3b found 7 competitors running
10+ ads.

### Phase 6 — Adversarial completeness pass (mandatory — spec §7 check #6)

For every weak/zero/low cell (score 0-1):

1. Ask: "If this competitor were strong in this arena, where would it show?"
2. Check whether those places were looked at.
3. If a plausible signal source was NOT checked → flag as residual, not confirmed zero.
4. Log each adversarial probe and its result.

The gap-finder points at **our own conclusions**, not only at missing data.

### Phase 7 — Scoring

Apply the 0-5 scale to every competitor × every arena:

| Score | Meaning |
|---|---|
| 0 | Absent (must be defended — see Phase 5) |
| 1 | Token presence |
| 2 | Present but weak |
| 3 | Competitive |
| 4 | Strong |
| 5 | Arena leader |

**Rules:**
- Every cell shows its **inline metric** (the number that justifies the score), not just the score.
- Every cell names the **source** (the pull/observation that produced the metric).
- Proxy cells (estimated, not directly measured) are labeled as proxy — never hidden.
- **Composite = sum of 8 arena scores (max 40).** Rank competitors by composite.

### Phase 8 — Deep-N teardowns

1. Select the top `top_n_deep` competitors by composite rank.
2. Add `retain_incumbents[]` from config (popular incumbents kept regardless of rank).
3. Invoke `site-capture-engine` (teardown context) for each.
4. Feed teardown outputs back into scoring for refinement (M2, A1 especially).

### Phase 9 — Gap-discovery pass (self-expanding — spec §6)

1. Review what the arena leaders expose that the current schema has no field for.
2. Append newly-spotted gaps to `_data-gap-register.md` — never reset the register.
3. If tool gaps are surfaced, route to `seo-tooling-landscape-research` discovery/intake modes.
4. The engine is **structurally forbidden from declaring full coverage** (enforced by G-market-intel
   check #3 — data-gap + tool-gap sections must always be non-empty).

### Phase 10 — Output A: field-level perfect company profile

Invoke `multi-source-synthesis` (cross-cluster shape) to produce the field-level reusable asset:

Per arena/multiplier/axis:
1. **Winning attributes observed** — what the arena leader actually does (with the competitor named).
2. **Target threshold** — the number/state needed to beat the current leader.
3. **Why it wins** — the mechanism.
4. **Page/content ideas + new-page ideas** it implies for a build.

Plus:
- Top-level **composite scorecard** (all competitors × all arenas).
- Synthesis: **"the profile of the unbeatable company in this field"** — field-level, not client-specific.
- **Limitations block** — headline-level, not buried (standing rule L0).

See `references/output-contract-a.md` for the full template.

### Phase 11 — Output B: per-client gap-to-action plans

For each client in `clients[]`, invoke `multi-source-synthesis` (client-driven shape):

1. Current score per arena → gap vs the perfect profile.
2. **Prioritized action list** (highest-leverage gaps first).
3. Each action routed: `[WF]` website-factory, `[LSG]` local-seo-growth, `[T/D]` tool-or-data change.
4. Cross-client priority summary table (if >1 client).

See `references/output-contract-b.md` for the full template.

### Phase 12 — Residuals queue + limitations

1. Every open gap gets a method + owner + focused-run ticket. Nothing is silently dropped.
2. **Headline-level limitations block** emitted in the summary — gaps fail loud, every time (standing rule L0).
3. New data-gap-register entries appended.

### Phase 13 — Independent gate (spec §7 check #8)

1. The producer (this run) may **NOT** mark its own gate PASS on a data/collection artifact.
2. Dispatch `gate-peer-reviewer` with gate type `G-market-intel`.
3. The independent review must actually run (isolated agent / operator dispatch).
4. Self-attested "PASS" = "unreviewed," not closed.
5. Also invoke `output-quality-loop` on all produced artifacts.

See standing rule from MI-3b lessons — see `[[mi3-limitations-and-lessons-2026-06-14]]` §L2.

---

## 3. The arena model

See `references/arena-model.md` for the full arena definitions, data sources, and scoring criteria.

**Summary:** 5 visibility arenas (V1-V5) + 2 cross-cutting multipliers (M1-M2) + 1 authority/depth
axis (A1). Composite = sum of 8 scores, max 40.

### 3a. B2G arena variant (validated MI-8, v1.1)

For **government-contracting (B2G) fields**, the standard local-services arenas partially apply:
V2 (local pack), V4 (paid/LSA), and M1 (GBP reviews) are typically **defended-zero** because federal
procurement is national/agency-based, RFP/vehicle-driven, and reputation lives in CPARS — not Maps,
ads, or Google reviews. The engine adds 6 **G-arenas** that capture what actually decides B2G
competition:

| ID | B2G arena | What it measures | Primary sources | Scoring 0-5 |
|---|---|---|---|---|
| **G1** | Contract awards / past performance | Who actually wins — $ obligated, # awards, agencies, CPARS | USASpending API, FPDS, SAM.gov | 0=no awards → 5=arena leader by volume |
| **G2** | Set-aside / socioeconomic certs | 8(a), SDVOSB, WOSB/EDWOSB, HUBZone — the eligibility moat | SBA DSBS, certify.SBA.gov, SAM.gov | 0=no certs → 5=dual cert (e.g. 8(a)+SDVOSB) |
| **G3** | Contract vehicles / schedules | GSA MAS, GWACs (OASIS+, CIO-SP4, Alliant), agency IDIQs/BPAs | GSA eLibrary, agency vehicle lists | 0=no vehicles → 5=GSA MAS + ≥1 GWAC |
| **G4** | Capability & compliance | NAICS/PSC coverage, capability statement, CMMC, clearances | Competitor sites, SAM.gov, CMMC marketplace | 0=no govcon framing → 5=modern+CMMC+clearance |
| **G5** | Agency relationships / incumbency | Incumbent positions + recompete targets + agency depth | USASpending agency queries, GovWin | 0=no relationships → 5=multi-agency incumbent |
| **G6** | Teaming / partner network | Prime↔sub relationships, JV/mentor-protégé | USASpending sub-awards, JV registrations | 0=no teaming → 5=large-firm JV (e.g. Deloitte) |

**Composite for B2G runs:** sum of all in-scope arenas. A run with all 14 arenas (V1-V5 + M1-M2 +
A1 + G1-G6) has max 70; several standard arenas will typically score defended-zero. The composite is
**not comparable** across field types (local-services max 40 vs B2G max 70) — compare only within the
same field's run.

**Defended-zero rules for B2G:** V2/V4/M1 must be **explicitly defended** with the B2G reason
(e.g., "M1 GBP reviews — N/A for B2G; reputation lives in CPARS/past-performance, see G1"). Do not
silently drop them — log why each is N/A. V1/V3/V5/M2/A1 carry over with reduced weight (organic
for govcon terms, AI-engine mentions, LinkedIn thought leadership, website conversion, GovCon media
authority).

**Precipitating event:** MI-8 (2026-06-16) proved the B2G variant on federal IT services. The
local-services model missed 6 arenas that dominate B2G competition (awards, certs, vehicles,
capability, incumbency, teaming). Without G1-G6, the scoring was structurally incomplete for B2G.

---

## 4. Self-expanding mechanisms

See `references/self-expanding-mechanisms.md` for the five mechanisms that keep the engine growing:

1. Living data-gap register (`_data-gap-register.md`)
2. Gap-discovery pass (Phase 9)
3. Emerging-tool discovery mode (via `seo-tooling-landscape-research` v2.0)
4. Operator tool-intake pipeline (via `seo-tooling-landscape-research` v2.0)
5. Scheduled cadence ([MI-8]: monthly tool scan + quarterly arena re-score)

**Structural rule:** the engine is forbidden from declaring full coverage. G-market-intel check #3
enforces non-empty data-gap + tool-gap sections on every run.

---

## 5. Quality gate — `G-market-intel`

Registered in `skills/gate-peer-reviewer/references/gate-type-registry.md`. Eight distinctive
market-intelligence checks (MI-1 through MI-8), plus G-default's surface sweep + source-client-leak
audit + link resolution inherited as MI-9 — nine checks total:

1. Every arena score traces to a cited source/pull.
2. Every perfect-profile attribute names the competitor that demonstrated it.
3. Data-gap + tool-gap sections are non-empty (never claims full coverage).
4. No undefended zeros (≥2 sources + breadth for any 0/absent cell).
5. Per-arena source checklist filled (including free public registries).
6. Adversarial completeness pass run (tried to disprove every weak/zero/low cell).
7. Completion-vs-plan (X of Y collected, verified against raw artifact).
8. No self-gating (independent review must actually run).
9. Plus G-default surface sweep + source-client-leak audit + link resolution.

---

## 6. Worked example

See `references/worked-example-electrician.md` for the full provenance pointing at the [MI-3]/[MI-4]
electrician-field run (2026-06-14 → 2026-06-16).

---

## 7. Changelog

### v1.1 (2026-06-16) — B2G arena variant + provisioning preflight + geo-grid fallback

**MI-8 duplicability proof (federal IT services).** Three structural fixes:
1. **B2G arena variant (§3a):** 6 new G-arenas (G1 awards, G2 certs, G3 vehicles, G4 capability,
   G5 incumbency, G6 teaming) with sources, scoring, and defended-zero rules for local-services
   arenas that don't apply to B2G. Config contract updated with G1-G6 in `arenas_in_scope`.
   Phase 3 collection table extended with B2G methods.
2. **Per-client provisioning preflight (Phase 0 step 2):** tool-access + Chrome-login checklist
   per client before run starts, emitting ✅/⚠️/❌ per tool. Prevents silent tool-skip.
3. **Geo-grid anchor fallback (Phase 3 V2):** for SAB or mis-geocoded GBP clients, anchor the
   geo-grid on a correctly-located competitor per
   `[[pattern-geo-grid-anchor-on-located-competitor-for-misgeocoded-SAB]]`.
   Phase 1 updated with B2G seed-set generation from USASpending + set-aside-seeded tier.

### v1.0 (2026-06-16) — Initial release

Distilled from the proven [MI-3]/[MI-3b]/[MI-3c]/[MI-4] electrician-field run. Config-driven,
zero hardcoded values. Composes `competitor-deep-research` v1.4 + `site-capture-engine` v2.2 +
`seo-tooling-landscape-research` v2.0 + `multi-source-synthesis` v1.0 + research skills +
`ad-intelligence` module. Registered `G-market-intel` gate type with 9 checks. Baked in:
arena-source-enumeration, no-undefended-zero guard, adversarial completeness pass, completion-vs-plan,
substrate-routing rule, self-expanding gap engine. Built by [MI-5] (`mi5-engine-skill-202606161900`).

---

## Related

- `[[spec-market-intelligence-engine]]` (canonical design doc)
- `[[mi-arena-source-checklist]]` (completeness rules)
- `[[mi3-limitations-and-lessons-2026-06-14]]` (precipitating events)
- `[[competitor-deep-research]]` v1.4 (organic module)
- `[[site-capture-engine]]` v2.2 (deep-N module)
- `[[seo-tooling-landscape-research]]` v2.0 (tool engine)
- `[[multi-source-synthesis]]` v1.0 (synthesis substrate)
- `[[_data-gap-register]]` (living register)
- `[[gate-type-registry]]` (`G-market-intel` entry)
