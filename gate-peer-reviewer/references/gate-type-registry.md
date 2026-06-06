---
type: reference
skill: gate-peer-reviewer
skill-version: 2.1
created: 2026-06-03
updated: 2026-06-06
tags: [reference, gate-type-registry, substrate-agnostic, future-orchestrator-friendly, page-build, client-seo-onboarding]
---

# Gate-type registry

The peer-reviewer reads this registry to know what to expect at any gate type — making the skill substrate-agnostic and future-orchestrator-friendly without hard-coding any single orchestrator's gates.

**v2 scope.** v1 seeded the registry with vault-orchestrator Mode 6 EXECUTE's 5 research-brief gates as the canonical instance + documented the registration shape. v2 (Build wave 4, 2026-06-05) adds client-seo-onboarding's 5 page-build gates as the second registered instance + 3 reusable named verification procedures that any gate type can reference. Two orchestrators, two artifact classes (research briefs + built pages), one engine.

## Registration shape

Each gate type entry has this YAML-friendly shape:

```yaml
- orchestrator: <skill-name>
  mode: <mode-name>
  gate_id: <Gate N <name>>
  fires_at: <when-in-the-orchestrator-flow>
  emits: <one-line description of what the gate outputs>
  contract_source: <path to the SKILL.md section that defines the contract>
  is_closing_gate: <true | false>
  expects:
    check_1_satisfaction_targets:
      - <numbered ask from kickoff>
      - <required deliverable>
    check_2_calibration_metrics:
      - <metric: cost_usd>
      - <metric: wall_clock_seconds>
      - <metric: sub_agent_count>
      - <metric: iteration_count>
    check_3_domain_probe_classes:
      - <jurisdiction-specific?>
      - <brand-currency-specific?>
      - <time-specific?>
    check_4_cross_wave_artifact_type: <Gate-4-dispatch-prompts | JSON-return-contract | quality-loop-contract | state-write-contract | none>
    check_4_within_wave_prior_gate: <Gate N-1 or null>
  registered_by: <chat-id of the registration>
  registered_at: <YYYY-MM-DD>
```

## Cross-mode reality (vault-orchestrator v1.2 architecture)

The 5 conceptual gates this registry models DO NOT all live inside Mode 6 EXECUTE in vault-orchestrator v1.2. They distribute across Modes 5 + 3 + 6:

| Conceptual gate | Actual orchestrator location | v1.0 hook? |
|---|---|---|
| Gate 1 RESUME | Mode 5 RESUME Step 11 confirmation | No (v1.1 deferred) |
| Gate 2 PROVISION | Mode 3 PROVISION Step 9 single review gate | No (v1.1 deferred) |
| Gate 3 dispatch plan + Gate 4 dispatch prompts (combined) | Mode 6 EXECUTE Step 6/7 single review gate | **YES — v1.0 ships here** |
| Gate 5 wave-close | Mode 6 EXECUTE Step 10 wave-close (auto-closes in v1.2) | No (v1.1 deferred) |
| Conditional sub-agent gates | Routed via `operator-gate-routing` | No (separate channel) |

v1.0 ships with the single Mode 6 Step 6/7 hook because it covers Gates 3 + 4 (combined dispatch plan + prompts emission) — the single existing operator-attended gate where the catches from waves A2-A6 fired. The registry models all 5 conceptual gates so future hooks at v1.1 expand without registry refactoring; the gate entries below remain authoritative regardless of which mode actually emits each gate.

## v1 seed registry — vault-orchestrator Mode 6 EXECUTE (5 conceptual gates, distributed across modes)

```yaml
- orchestrator: vault-orchestrator
  mode: Mode 6 EXECUTE
  gate_id: Gate 1 RESUME
  fires_at: orchestrator initialization, after Mode 5 RESUME state-file read
  emits: wave plan recap + carry-forward framing inherited from prior wave close + sub-agent slot count + cost ceiling + wall-clock ceiling
  contract_source: skills/vault-orchestrator/SKILL.md § Mode 6 EXECUTE § Gate 1 RESUME
  is_closing_gate: false
  expects:
    check_1_satisfaction_targets:
      - wave_id named
      - sub-agent slot count consistent with state-file planned_remaining_waves
      - carry-forward framing from prior wave present (if not first wave)
      - cost ceiling + wall-clock ceiling stated
    check_2_calibration_metrics:
      - cost_usd_ceiling_prediction
      - wall_clock_seconds_prediction
      - sub_agent_count
    check_3_domain_probe_classes:
      - jurisdiction-specific (if waves touch VA/MD/DC municipalities)
    check_4_cross_wave_artifact_type: none
    check_4_within_wave_prior_gate: null
  registered_by: gate-peer-reviewer-skill-v1-build-202606031400
  registered_at: 2026-06-03

- orchestrator: vault-orchestrator
  mode: Mode 6 EXECUTE
  gate_id: Gate 2 PROVISION
  fires_at: after Gate 1 RESUME operator approval
  emits: per-sub-agent provisioning data (city briefs, intersection briefs, service briefs) including utility tables, demographic data, identity blocks
  contract_source: skills/vault-orchestrator/SKILL.md § Mode 6 EXECUTE § Gate 2 PROVISION
  is_closing_gate: false
  expects:
    check_1_satisfaction_targets:
      - per-sub-agent identity block populated
      - utility/demographic/regulatory data field-complete
      - jurisdiction-anomaly check applied (per city-base-research v1.1)
    check_2_calibration_metrics:
      - sonar_query_count_prediction
    check_3_domain_probe_classes:
      - jurisdiction-specific (utility companies + regulatory bodies + brand currency)
      - time-specific (recent legislation, recent rebrands)
    check_4_cross_wave_artifact_type: none
    check_4_within_wave_prior_gate: Gate 1 RESUME
  registered_by: gate-peer-reviewer-skill-v1-build-202606031400
  registered_at: 2026-06-03

- orchestrator: vault-orchestrator
  mode: Mode 6 EXECUTE
  gate_id: Gate 3 dispatch plan
  fires_at: after Gate 2 PROVISION operator approval
  emits: dispatch plan — parallel-vs-sequential, sub-agent ordering, shared-Sonar-budget allocation, wall-clock estimates per sub-agent
  contract_source: skills/vault-orchestrator/SKILL.md § Mode 6 EXECUTE § Gate 3 dispatch plan
  is_closing_gate: false
  expects:
    check_1_satisfaction_targets:
      - dispatch shape (parallel/sequential) stated
      - sub-agent ordering justified (if sequential)
      - shared Sonar budget allocated per sub-agent
      - close-conditions listed (current memory states 8-item KCA — verify item count)
    check_2_calibration_metrics:
      - cost_usd_per_sub_agent
      - wall_clock_seconds_per_sub_agent
    check_3_domain_probe_classes:
      - none (Gate 3 is process-shape, not domain-content)
    check_4_cross_wave_artifact_type: dispatch-plan-shape
    check_4_within_wave_prior_gate: Gate 2 PROVISION
  registered_by: gate-peer-reviewer-skill-v1-build-202606031400
  registered_at: 2026-06-03

- orchestrator: vault-orchestrator
  mode: Mode 6 EXECUTE
  gate_id: Gate 4 dispatch prompts
  fires_at: after Gate 3 dispatch plan operator approval
  emits: per-sub-agent dispatch prompts — the actual prompts each sub-agent receives
  contract_source: skills/vault-orchestrator/SKILL.md § Mode 6 EXECUTE § Gate 4 dispatch prompts
  is_closing_gate: false
  expects:
    check_1_satisfaction_targets:
      - per-sub-agent prompt populated, no <TODO> placeholders
      - 5 required template blocks present (wrapper + state-writes + four-substep quality loop + structured JSON return + operator gate routing) — LOAD-BEARING per A4→A5 carry-forward drift catches
    check_2_calibration_metrics:
      - none (Gate 4 is structural, not metric-emitting)
    check_3_domain_probe_classes:
      - none
    check_4_cross_wave_artifact_type: Gate-4-dispatch-prompts
    check_4_within_wave_prior_gate: Gate 3 dispatch plan
  registered_by: gate-peer-reviewer-skill-v1-build-202606031400
  registered_at: 2026-06-03

- orchestrator: vault-orchestrator
  mode: Mode 6 EXECUTE
  gate_id: Gate 5 wave-close
  fires_at: after all sub-agent dispatches complete + sub-agent returns processed
  emits: wave-close summary + Knowledge Capture Audit self-report + state-file updates + git-commit proposal
  contract_source: skills/vault-orchestrator/SKILL.md § Mode 6 EXECUTE § Gate 5 wave-close
  is_closing_gate: true
  expects:
    check_1_satisfaction_targets:
      - wave-close summary covers all sub-agent outcomes
      - KCA self-report claims explicit PASS/FAIL per the 8-item current spec
      - state-file updates listed
      - git-commit proposal staged by name
    check_2_calibration_metrics:
      - cost_usd_actual_vs_prediction
      - wall_clock_seconds_actual_vs_prediction
      - iteration_count_actual_vs_prediction
    check_3_domain_probe_classes:
      - none (Gate 5 is process-close, not domain-content)
    check_4_cross_wave_artifact_type: wave-close-shape
    check_4_within_wave_prior_gate: Gate 4 dispatch prompts
  registered_by: gate-peer-reviewer-skill-v1-build-202606031400
  registered_at: 2026-06-03
```

## Reusable named verification procedures (project-agnostic)

Named procedures any gate type can reference in `check_1_satisfaction_targets`. Each procedure defines a disk-verification discipline the peer-reviewer runs at Check 1 time. Procedures are ADDITIVE to check-spec.md's Check 1 contract-satisfaction logic — they don't modify the 6-check engine, they feed it.

### Procedure: `full-placeholder-family-sweep`

**Purpose.** Verify an artifact contains zero residual placeholder tokens. A page/draft/data file is clean ONLY when ALL of these regexes return zero matches (minus documented expected exceptions like pre-imagery image-URL FILLs):

```
FILL:
<!-- MISSING
<!-- TBD
\bTBD\b
<TBD
\[.*placeholder.*\]
\{[a-z_]+\}    (unrendered template braces)
```

**Calibration source.** S&H Core 30 peer-review PR-15 (reviewer missed `<TBD>` Q&A bodies because token list only had `FILL:` + `<!-- MISSING -->`) + PR-16 (`{phone_display}` leaked because publish hard-block had the same incomplete family). The full family was codified in `publish-core-30-page.py` `check_placeholder_gate()` during the run.

**How to run.**

1. **Grep the actual artifact files** for each regex. Do not declare counts from memory or by naming the procedure without executing it.
2. **Report real counts per token type.** Output a table: token family | count | locations (file:line). Zero is a valid count — but it must come from an actual grep, not an assumption.
3. **Stage-classify each hit.** For every non-zero count, classify each token as:
   - **expected-at-this-stage** — the token is a known pre-wiring placeholder that a later pipeline step fills (e.g., `hero_image_url FILL` before Step 8 imagery wiring). Must match a named entry in the gate-type's `check_1_expected_exceptions` list.
   - **unexpected** — the token should not be present at this stage. Any unexpected token is a catch.
4. **Clean-gate is G-publish only.** The sweep may report "0 unexpected tokens" at earlier gates (G-data, G-scaffold, G-imagery), but the procedure must NOT declare the artifact "clean" at those gates — only "0 unexpected tokens at this stage; N expected tokens deferred to G-publish." The **clean declaration** (zero tokens of any kind, expected or not) is reserved for G-publish, the final artifact gate. (Calibration: D-02 from wave-2 calibration — reviewer declared "zero blocking tokens in rendered HTML" at G-data when each draft actually had 10-12 FILL/TBD tokens that were expected but uncounted.)

Expected exceptions (e.g., 2 image-URL FILL entries before Step 8 imagery wiring) must be named in the gate-type entry's `check_1_expected_exceptions` field — any token not in the exception list is a catch regardless of stage.

**Applies at gate types.** Any gate reviewing a text artifact that may contain templates, drafts, or data files. Currently: G-data, G-scaffold, G-imagery, G-publish.

---

### Procedure: `source-client-leak-audit`

**Purpose.** Verify that artifacts derived from a prior client's templates carry zero source-client-specific content. Audits 6 surfaces:

| Surface | What to check | Calibration source |
|---|---|---|
| 1. Slug/prefix keys | `page_slug_template` prefix in service JSONs matches THIS client's build-order slug, not the source client's | PR-01 (EV's `ev-charger` prefix vs S&H's `ev-charger-installation`) |
| 2. Related-cards catalog | `related_cards` entries point only to THIS client's services, not the source's | PR-07 (EV's 5-service catalog on S&H pages → dead links) |
| 3. Image-URL domains | `hero_image_url`, `about_image_url`, JSON-LD `image` use THIS client's domain, not the source's | PR-07 (`evelectric.pro` URLs in S&H files) |
| 4. Owner/brand names in prose | Zero occurrences of source client's owner name or business name in rendered text | PR-04 ("Ahmad" in S&H files), PR-37 (maps iframe title + CSS comment) |
| 5. Brand-mark in imagery prompts | Wardrobe/uniform clause names THIS client's mark, not the source's | PR-19a (EV Electric logo hardcoded in S&H imagery prompts — costliest catch) |
| 6. Face reference in imagery | Face-reference path points to THIS client's owner face crop in `reference-photos/`, not `brand_image_url` or other non-face file | PR-19b (`brand_image_url` used instead of owner face crop) |

**How to run.**

1. **Load foreign-client identity strings at runtime.** Glob `data/client-*.json` in the project's data directory. Exclude the current client's JSON (match on `client_slug`). For each foreign-client JSON, extract:
   - `name` (business name)
   - `alternate_name` (if present)
   - `owner_name`
   These are the grep targets. **Never reconstruct owner/business names from memory** — always read from the authoritative JSON files on disk. (Calibration: D-01 from wave-2 calibration — reviewer grepped for "Ahmad Suliman" from memory when the actual owner name in `client-ev-electric-services.json` was "Ahmad Shaban".)
2. Grep the artifact under review for each identity string (case-insensitive). Any hit on any foreign-client identity string = catch.
3. Also verify surfaces 1-3 structurally (prefix match, related_cards membership, domain match). Any hit = catch.

**Applies at gate types.** Any gate reviewing artifacts derived from a prior client template. Currently: G-data (surfaces 1-4), G-imagery (surfaces 4-6), G-scaffold (surfaces 1-4), G-publish (surface 4 via rendered text).

---

### Procedure: `live-rendered-cache-busted-verification`

**Purpose.** Verify a published page renders correctly in the browser, not just in post_content HTML. A grep of HTML source is NOT acceptance — it cannot detect serif fallback, duplicate theme titles, or old-vs-new content structure.

**Verification steps (all required):**

1. Fetch the LIVE published URL with a cache-buster (`?v=<timestamp>`).
2. Verify `modified_time` advanced past the prior value (confirms WP actually updated).
3. Verify H1 matches expected eyebrow + clean-H1 form (not a combined serif H1 or stale content).
4. Verify title visibility: WP page title is hidden (no duplicate theme title above the hero). **Per-client theme adaptation required** — the hide-selectors must match THIS client's theme, not the source client's (PR-17: S&H's theme title element not in EV's selector list).
5. Verify font-family: page renders in sans-serif via `.evp-corepage` styling (serif fallback = style wrapper didn't survive upload → fail).
6. Verify image fill: hero + about images fill containers edge-to-edge (no dashed border / blue frame / placeholder chrome).
7. Verify map fill: Google Maps embed fills its container (not undersized / not a placeholder).
8. Verify zero placeholder text on the RENDERED page (runs `full-placeholder-family-sweep` on the live-fetched content).
9. Compare RENDERED structure to a named known-good sibling page (same client, same template generation).
10. **Cache-purge re-check:** after logged-in render verification, purge page cache + re-fetch public URL logged-out/cache-busted. Anonymous visitors + Googlebot must get the new version.
11. **Fetch-vs-screenshot conflict rule:** when a tool fetch conflicts with an operator screenshot, treat as a cache question first, not a "the other agent lied" conclusion. Never override operator visual evidence with a single anonymous tool fetch.

**Calibration source.** PR-17 (duplicate theme title on S&H — CSS hide-selectors tuned to EV theme missed S&H's title element), EV lesson Issues #26/#27/#28 (live-verification failure modes).

**Applies at gate types.** G-publish (mandatory), any gate that touches live page state.

---

## v2.0 seed registry — client-seo-onboarding page-build gates (5 gates)

Registered by Build wave 4. Calibrated against the S&H Core 30 page-build peer-review corpus (PR-01..PR-40, 2026-06-04/05). The 5 gates map to the artifact-producing steps in client-seo-onboarding v1.3's 11-step pipeline.

```yaml
- orchestrator: client-seo-onboarding
  mode: page-build
  gate_id: G-data
  fires_at: after Step 3 (Author data files) quality-loop exit, before operator gate
  emits: per-client service JSONs, city JSONs, client JSON — the data layer all downstream scaffolding reads
  contract_source: skills/client-seo-onboarding/SKILL.md § Step 3
  is_closing_gate: false
  expects:
    check_1_satisfaction_targets:
      - service JSON page_slug_template prefix matches build-order slug for each service (PR-01 class)
      - related_cards point ONLY to this client's services, not the source client's (PR-07 class)
      - image-URL domains use this client's domain, not the source's (PR-07 class)
      - zero source-client owner/brand names in prose fields (PR-04 class)
      - full-placeholder-family-sweep = 0 (minus expected pre-imagery image-URL FILLs)
      - named procedure: source-client-leak-audit (surfaces 1-4)
      - named procedure: full-placeholder-family-sweep
    check_1_expected_exceptions:
      - hero_image_url FILL (deferred to Step 8 imagery wiring)
      - about_image_url FILL (deferred to Step 8 imagery wiring)
    check_2_calibration_metrics:
      - none (page-build steps do not predict cost/wall-clock)
    check_3_domain_probe_classes:
      - none (data file correctness is structural, not jurisdiction-specific)
    check_4_cross_wave_artifact_type: service-city-client-json
    check_4_within_wave_prior_gate: null
  registered_by: gate-peer-reviewer-build-wave-4-202606051000
  registered_at: 2026-06-05

- orchestrator: client-seo-onboarding
  mode: page-build
  gate_id: G-scaffold
  fires_at: after Step 5 (Bulk scaffold) quality-loop exit, before operator gate
  emits: per-page draft-v1.md + draft-v1-WP-WRAPPED.html — the scaffolded page drafts
  contract_source: skills/client-seo-onboarding/SKILL.md § Step 5
  is_closing_gate: false
  expects:
    check_1_satisfaction_targets:
      - client-override fork actually fired (0 source-client refs in rendered content) — verify on a fork-using page, not just dry-run resolution (PR-07 class)
      - exactly 1 <h1> per page (SEO requirement)
      - hero structure matches a known-good sibling (same generation template)
      - maps iframe carries a real embed key, not a placeholder
      - full-placeholder-family-sweep = 0 (minus expected pre-imagery image-URL FILLs)
      - named procedure: source-client-leak-audit (surfaces 1-4)
      - named procedure: full-placeholder-family-sweep
    check_1_expected_exceptions:
      - hero_image_url FILL (deferred to Step 8 imagery wiring)
      - about_image_url FILL (deferred to Step 8 imagery wiring)
    check_2_calibration_metrics:
      - none
    check_3_domain_probe_classes:
      - none (scaffold structure is template-driven, not domain-claim-driven)
    check_4_cross_wave_artifact_type: page-draft-html
    check_4_within_wave_prior_gate: G-data
  registered_by: gate-peer-reviewer-build-wave-4-202606051000
  registered_at: 2026-06-05

- orchestrator: client-seo-onboarding
  mode: page-build
  gate_id: G-imagery
  fires_at: after Step 6 (Imagery prompts) quality-loop exit, before operator gate
  emits: per-page imagery-prompts-log.md — the prompts Higgsfield/CLI generates from
  contract_source: skills/client-seo-onboarding/SKILL.md § Step 6
  is_closing_gate: false
  expects:
    check_1_satisfaction_targets:
      - brand mark is THIS client's, not the source client's — highest-stakes check (PR-19a: EV Electric logo hardcoded in S&H prompts would have produced 16 pages of competitor-branded owner photos)
      - face reference points to owner face crop in reference-photos/, not brand_image_url or other non-face file (PR-19b)
      - owner name is THIS client's owner, not the source's (PR-04 class)
      - zero source-client brand/owner strings in any prompt text
      - zero unrendered template tokens in prompt text
      - named procedure: source-client-leak-audit (surfaces 4-6)
      - named procedure: full-placeholder-family-sweep
    check_1_expected_exceptions: []
    check_2_calibration_metrics:
      - none
    check_3_domain_probe_classes:
      - none
    check_4_cross_wave_artifact_type: imagery-prompts-log
    check_4_within_wave_prior_gate: G-scaffold
  registered_by: gate-peer-reviewer-build-wave-4-202606051000
  registered_at: 2026-06-05

- orchestrator: client-seo-onboarding
  mode: page-build
  gate_id: G-publish
  fires_at: after Step 8 (Resume per page) substep 3 (wire) completes, BEFORE substep 4 (live-rendered verification)
  emits: published live page at canonical URL — the production artifact visible to customers and Googlebot
  contract_source: skills/client-seo-onboarding/SKILL.md § Step 8
  is_closing_gate: false
  expects:
    check_1_satisfaction_targets:
      - named procedure: live-rendered-cache-busted-verification (all 11 steps)
      - named procedure: full-placeholder-family-sweep (on live-fetched content)
      - named procedure: source-client-leak-audit (surface 4 — brand names in rendered text)
      - Yoast (or AIOSEO) title + meta description + focus keyword populated in page source (PR-11 class)
      - page-options theme meta persists after REST re-publish (PR-17 class — per-client theme config)
      - JSON-LD schema image = page hero, not brand_image_url (PR-25)
      - modified_time advanced (confirms WP actually updated)
    check_1_expected_exceptions: []
    check_2_calibration_metrics:
      - none
    check_3_domain_probe_classes:
      - none (live page correctness is structural + visual, not domain-claim)
    check_4_cross_wave_artifact_type: live-published-page
    check_4_within_wave_prior_gate: G-imagery
  registered_by: gate-peer-reviewer-build-wave-4-202606051000
  registered_at: 2026-06-05

- orchestrator: client-seo-onboarding
  mode: page-build
  gate_id: G-wave-close
  fires_at: at any wave's Closing Protocol (not only Step 11 — intermediate waves close after their scope completes)
  emits: wave-close state writes + wave_log entry + report (Step 11 only) + handoff for next wave
  contract_source: skills/client-seo-onboarding/SKILL.md § Closing Protocol + § Step 11
  is_closing_gate: true
  expects:
    check_1_satisfaction_targets:
      - wave_log entry captures all artifacts produced + verdicts + failures
      - planned_remaining_waves updated (closed wave removed, estimates recomputed)
      - current_wave cleared
      - event-log row appended
      - next-wave handoff spawned (if planned_remaining_waves non-empty)
    check_2_calibration_metrics:
      - none (page-build waves don't predict cost/wall-clock the same way research waves do)
    check_3_domain_probe_classes:
      - none
    check_4_cross_wave_artifact_type: wave-close-shape
    check_4_within_wave_prior_gate: G-publish
    check_6_kca_applies: true
  registered_by: gate-peer-reviewer-build-wave-4-202606051000
  registered_at: 2026-06-05
```

## v3.0 seed registry — research-brief + knowledge-artifact gates (9 gate types)

Registered by the toolkit-wide quality-tool integration audit (2026-06-06). These 9 gate types cover the artifact-producing skills that have explicit operator-review points but were not previously registered. Priority-ordered by cascade risk (a wrong brief propagates to every page that consumes it).

```yaml
# P1: service-seo-research
- orchestrator: service-seo-research
  mode: research
  gate_id: G-service-brief
  fires_at: after Phase 8 knowledge-growth hooks + AI-citation checklist §4.5, before closing
  emits: Tier-1 service base brief at research-briefs/services/<service-slug>.md
  contract_source: skills/service-seo-research/SKILL.md § Phase 8 + §4.5
  is_closing_gate: true
  expects:
    check_1_satisfaction_targets:
      - 15-section template fully populated (no empty sections)
      - AI-citation hardening checklist §4.5 items all addressed (PASS or gap-flagged)
      - sources-cited roll-up at §14 present with 10+ inline citations
      - pricing-visibility matches client policy
    check_2_calibration_metrics: []
    check_3_domain_probe_classes:
      - brand-currency-specific (tool pricing, service pricing)
      - time-specific (legislation, code references)
    check_4_cross_wave_artifact_type: research-brief
    check_4_within_wave_prior_gate: null
  registered_by: quality-tool-integration-audit-202606060000
  registered_at: 2026-06-06

# P2: intersection-research
- orchestrator: intersection-research
  mode: research
  gate_id: G-intersection-brief
  fires_at: after brief authoring, before closing
  emits: Tier-3 intersection brief at research-briefs/intersections/<service>--<city>.md
  contract_source: skills/intersection-research/SKILL.md
  is_closing_gate: true
  expects:
    check_1_satisfaction_targets:
      - parent briefs exist (Tier-1 service + Tier-2 city)
      - live SERP data present with top-3 competitors
      - keyword volume + KD populated
      - localized FAQ themes present
    check_2_calibration_metrics: []
    check_3_domain_probe_classes:
      - jurisdiction-specific (permits, utility companies per city)
    check_4_cross_wave_artifact_type: research-brief
    check_4_within_wave_prior_gate: null
  registered_by: quality-tool-integration-audit-202606060000
  registered_at: 2026-06-06

# P3: city-base-research
- orchestrator: city-base-research
  mode: research
  gate_id: G-city-brief
  fires_at: after jurisdiction anomaly check + brief authoring, before closing
  emits: Tier-2 city base brief at research-briefs/cities/<city-slug>.md
  contract_source: skills/city-base-research/SKILL.md
  is_closing_gate: true
  expects:
    check_1_satisfaction_targets:
      - jurisdiction anomaly check passed (city ↔ county ↔ state alignment)
      - demographics + neighborhoods + housing patterns populated
      - utility companies named (not generic "your utility")
      - permit offices named with jurisdiction
    check_2_calibration_metrics: []
    check_3_domain_probe_classes:
      - jurisdiction-specific (administrative boundaries, utility territory)
    check_4_cross_wave_artifact_type: research-brief
    check_4_within_wave_prior_gate: null
  registered_by: quality-tool-integration-audit-202606060000
  registered_at: 2026-06-06

# P4: client-fact-research
- orchestrator: client-fact-research
  mode: research
  gate_id: G-client-brief
  fires_at: after accounts-ownership verification, before closing
  emits: Tier-3 client-fact brief at research-briefs/clients/<slug>/brief.md + credentials checklist
  contract_source: skills/client-fact-research/SKILL.md
  is_closing_gate: true
  expects:
    check_1_satisfaction_targets:
      - accounts-ownership verification complete (each account classified owned/contested/unknown)
      - NAP data complete and consistent
      - service catalog matches confirmed services list
      - review count + rating populated from live source
    check_2_calibration_metrics: []
    check_3_domain_probe_classes:
      - brand-currency-specific (recent rebrands, acquisitions)
    check_4_cross_wave_artifact_type: client-brief
    check_4_within_wave_prior_gate: null
  registered_by: quality-tool-integration-audit-202606060000
  registered_at: 2026-06-06

# P5: competitor-deep-research
- orchestrator: competitor-deep-research
  mode: research
  gate_id: G-competitor-brief
  fires_at: after per-competitor deep dives + cross-competitor synthesis, before closing
  emits: per-competitor briefs + cross-competitor synthesis
  contract_source: skills/competitor-deep-research/SKILL.md
  is_closing_gate: true
  expects:
    check_1_satisfaction_targets:
      - per-competitor deep dive covers top-5-trafficked-pages analysis
      - cross-competitor synthesis present with structural patterns
      - methodology (DataForSEO vs free-toolkit) documented
    check_2_calibration_metrics: []
    check_3_domain_probe_classes: []
    check_4_cross_wave_artifact_type: competitor-research
    check_4_within_wave_prior_gate: null
  registered_by: quality-tool-integration-audit-202606060000
  registered_at: 2026-06-06

# P6: vis-extraction
- orchestrator: vis-extraction
  mode: extraction
  gate_id: G-extraction
  fires_at: Phase 6 review gate (executor surfaces structured summary before writes)
  emits: source note + supporting artifacts (tactics, patterns, tools)
  contract_source: skills/vis-extraction/SKILL.md § Phase 6
  is_closing_gate: false
  expects:
    check_1_satisfaction_targets:
      - source note follows 7-section structure (Take-away through Pattern candidates)
      - plain-English layer present (top-level + callouts)
      - no fabricated citations (every claim traceable to source)
      - project-applicability frontmatter fields present
    check_2_calibration_metrics: []
    check_3_domain_probe_classes: []
    check_4_cross_wave_artifact_type: source-note
    check_4_within_wave_prior_gate: null
  registered_by: quality-tool-integration-audit-202606060000
  registered_at: 2026-06-06

# P7: intel-routing
- orchestrator: intel-routing
  mode: routing (PUSH/PULL/BOOTSTRAP)
  gate_id: G-routing
  fires_at: Gate 1 (routing decision) + Gate 2 (bridge-note approval), per mode
  emits: frontmatter updates + bridge notes + punchlist entries
  contract_source: skills/intel-routing/SKILL.md
  is_closing_gate: false
  expects:
    check_1_satisfaction_targets:
      - routing decision justified per applicability-confidence threshold
      - bridge note links to parent artifact + target project
      - single-bridge-per-cluster discipline honored
    check_2_calibration_metrics: []
    check_3_domain_probe_classes: []
    check_4_cross_wave_artifact_type: routing-decision
    check_4_within_wave_prior_gate: null
  registered_by: quality-tool-integration-audit-202606060000
  registered_at: 2026-06-06

# P8: multi-chat-coordination
- orchestrator: multi-chat-coordination
  mode: DECOMPOSE
  gate_id: G-decompose
  fires_at: single comprehensive review gate (proposal before writes)
  emits: project subfolder + handoff files + _README.md + tracker rows
  contract_source: skills/multi-chat-coordination/SKILL.md § Mode 1
  is_closing_gate: false
  expects:
    check_1_satisfaction_targets:
      - handoff files have valid frontmatter (status, depends-on, tags)
      - dependency chain is acyclic
      - tracker rows match handoff files 1:1
    check_2_calibration_metrics: []
    check_3_domain_probe_classes: []
    check_4_cross_wave_artifact_type: decomposition-plan
    check_4_within_wave_prior_gate: null
  registered_by: quality-tool-integration-audit-202606060000
  registered_at: 2026-06-06

# P9: multi-source-synthesis
- orchestrator: multi-source-synthesis
  mode: synthesis
  gate_id: G-synthesis
  fires_at: shape-and-destination confirmation gate (before drafting)
  emits: synthesis shape decision + destination path
  contract_source: skills/multi-source-synthesis/SKILL.md
  is_closing_gate: false
  expects:
    check_1_satisfaction_targets:
      - shape matches source topology (cluster/pattern/cross-cluster/client-driven)
      - destination path follows conventions.md folder placement
      - source count meets minimum for chosen shape
    check_2_calibration_metrics: []
    check_3_domain_probe_classes: []
    check_4_cross_wave_artifact_type: synthesis-decision
    check_4_within_wave_prior_gate: null
  registered_by: quality-tool-integration-audit-202606060000
  registered_at: 2026-06-06
```

## How future orchestrators register

When a new orchestrator skill is built (Phase 5 project-surveyor / project-analyst / project-decider; mission-control-dashboard backend operations; Hermes-daemon spawned waves; any future client- or project-specific orchestrator), the orchestrator's build chat appends entries to this registry covering each of its gate types.

Registration entries land at chat close + are validated by the peer-reviewer's next invocation. Invalid entries (missing required fields, contradicting an existing entry without acknowledgment) trigger a Check 4 cross-wave coherence catch on the registration itself.

## Build wave 4 — cross-orchestrator generalization (SHIPPED 2026-06-05)

Build wave 4 expanded this registry to cover client-seo-onboarding's 5 page-build gates (G-data, G-scaffold, G-imagery, G-publish, G-wave-close) + 3 reusable named verification procedures (full-placeholder-family-sweep, source-client-leak-audit, live-rendered-cache-busted-verification). Calibrated against the S&H Core 30 page-build peer-review corpus (PR-01..PR-40, 2026-06-04/05).

**Architecture:** The 6-check engine remained untouched. Page-build gates are a registered instance — the same registry shape v1 designed for vault-orchestrator Mode 6 gates. Named verification procedures are project-agnostic reusable check blocks referenced by `check_1_satisfaction_targets`. Future orchestrators self-register at their build time using the same shape + referencing the same (or new) named procedures.

**Acceptance:** The registered gate types + named procedures independently reproduce catches PR-01 (slug-prefix mismatch), PR-07 (source-client related_cards leak), PR-15 (TBD Q&A bodies), PR-16 (unrendered {phone_display}), PR-17 (duplicate theme title), PR-19a (competitor brand in imagery prompts), PR-19b (wrong face reference) — unprompted, from Check 1 satisfaction targets alone.
