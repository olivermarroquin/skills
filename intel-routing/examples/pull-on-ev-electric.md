# Worked example: PULL on EV Electric Services inbox

Regression test 2026-05-28. Tests PULL against an active-engagement, post-launch client project. Reproduces the Phase 2 manual triage outcome (~98 candidates → 6 applies + ~88 keeps + ~5 defers + 0 not-applicable) from a clean slate, validating the batched Gate 1 + bin pre-classification + single-bridge-per-cluster discipline at full inbox scale.

## Test framing

Two test windows:

- **Window A (regression test, today = 2026-05-27 as-if).** PULL runs on what was effectively the first triage of EV's inbox under the new convention. No items have `routed-at:` set yet. This reproduces Phase 2's manual triage outcome and is the primary correctness test.
- **Window B (idempotence test, today = 2026-05-28).** PULL runs the day after Window A. The 6 items applied yesterday have `routed-at: 2026-05-27` and fall inside the default 14-day suppression window. Surface is now ~93 items (99 − 6). This tests that PULL does NOT re-surface freshly-routed items.

Window A is the main test. Window B gets a shorter walkthrough at the end.

## Inputs (Window A — first triage)

**Project:** `ev-electric-services`
**README:** `~/workspace/second-brain/04_projects/clients/_active/ev-electric-services/README.md`
**Inbox:** `~/workspace/second-brain/04_projects/clients/_active/ev-electric-services/_intel-inbox.md`
**Lookback:** 14 days (default)
**Today (as-if):** 2026-05-27

### Project state from README

- **Archetypes:** `[services-business, home-services-trade, electrical-contractor, wordpress-site, post-launch-seo, gbp-dependent]`
- **`applicability-confidence:`** `high`
- **`archived:`** not set
- **Current state signal (body skim):** "active engagement," "Phase 1 in flight," "Core 30 build in progress," WordPress + Elementor (no migration), GBP verified, Phase 2 Next.js pivot candidate around mid-June. Post-launch and actively deploying.

### Inbox state

- **Archetypes:** identical to README (matched on instantiation 2026-05-27)
- **Last triage:** none (first triage)

## PULL execution

### Step 1 — Preconditions

- Project folder resolved ✓
- README has `archetypes:` ✓
- Not archived ✓
- Inbox file exists (instantiated 2026-05-27) ✓
- Convention spec readable ✓

### Step 2 — Inputs

Read README + inbox + convention + bridge-file enumeration (zero existing bridges — first triage). Surface query against 03_domains + 05_shared-intelligence + 00_inbox/decisions-pending with EV's archetype set.

### Step 3a — Sync validation

- README archetypes: `[electrical-contractor, gbp-dependent, home-services-trade, post-launch-seo, services-business, wordpress-site]`
- Inbox archetypes: `[electrical-contractor, gbp-dependent, home-services-trade, post-launch-seo, services-business, wordpress-site]`
- **Match: matched ✓** (inbox was instantiated from README on 2026-05-27 with archetypes copied)

No sync prompt needed.

### Step 3b — Tag surfaced artifacts

Query result: 99 artifacts surfaced (matches Phase 2 manual triage count).
- Slug-named (artifact's `applies-to-projects:` includes `ev-electric-services`): 70
- Archetype-overlap only: 29

Per-artifact tagging proceeds — extracts match type, situational status, existing confidence, routed-at, body summary. Existing-bridge check returns zero matches (no `bridge-*.md` in the EV folder yet at this date — Window F bridges were filed *as* the Phase 2 triage, not before).

### Step 3c — Pre-classify into bins

Pre-classification rules applied. The largest bin is `keep` because EV's `applies-to-projects:` shows 70 direct hits — all relevant to the engagement, most already in flight context, no immediate action beyond what's already happening:

**Pre-classified to APPLY (6 items)** — slug-named + project in active deployment + body-content actionable now:

1. `[[tactic-information-architecture-first-for-new-sites]]` — IA tactic actionable on Phase 2 Next.js pivot scoping
2. `[[tactic-foundationals-first-for-new-sites-link-building]]` — foundationals tactic actionable on current backlink lane
3. `[[tactic-gbp-to-website-alignment-core-30]]` — Core 30 IS the in-flight engagement
4. `[[pattern-core-30-page-design-system]]` — pattern emerged from EV page-1 build, canonical for pages 2-30
5. `[[tactic-services-by-locations-matrix-for-local-seo]]` — driving the Core 30 build geometry
6. `[[cluster-synthesis-ai-era-seo-cluster-2026-05-27]]` — canonical SEO reference for the engagement (filed evening 2026-05-27)

**Pre-classified to KEEP (~88 items)** — slug-named + active engagement + already in context. Examples:
- Source notes Oliver has already extracted from (Greg Isenberg agent-builders, Jono Catliff masterclass, etc.)
- Tactics already deployed (audit-to-AI-fix-loop active, attribute match optimization in flight)
- Tools already adopted (Higgsfield, Claude Code, Site Kit)
- Patterns already in use (Keelworks AIOSEO bridge, no-pricing convention, competitor visual fingerprint)

These are kept rather than re-applied because the engagement context already has them; bridge-noting each would be noise. Friction #4 baked into discipline.

**Pre-classified to DEFER (~5 items)** — slug-named but gated on a future state:
- `[[tactic-featured-com-expert-link-acquisition]]` — link-acquisition lane, gated by Phase-1 SEO foundation audit
- `[[tactic-qwoted-expert-link-acquisition]]` — same
- `[[tactic-image-link-building-for-local-services]]` — same
- `[[tactic-claude-artifact-link-building-pilot]]` — speculative pilot, gated
- `[[tactic-stats-article-link-building-pilot]]` — same

**Pre-classified to NOT APPLICABLE (0 items)** — EV is post-launch + WordPress, no situational conflicts surface against the post-launch-shaped artifact base.

**Pre-classified to ALREADY BRIDGED (0 items)** — first triage; no prior bridges.

## Gate 1 surface

```
PULL TRIAGE — ev-electric-services

Project name: EV Electric Services
Project README: ~/workspace/second-brain/04_projects/clients/_active/ev-electric-services/README.md
Inbox file: ~/workspace/second-brain/04_projects/clients/_active/ev-electric-services/_intel-inbox.md
Lookback window: 14 days (suppressing items with routed-at after 2026-05-13)
Last operator triage: first triage

Sync status:
  README archetypes: [electrical-contractor, gbp-dependent, home-services-trade, post-launch-seo, services-business, wordpress-site]
  Inbox archetypes: [electrical-contractor, gbp-dependent, home-services-trade, post-launch-seo, services-business, wordpress-site]
  Match: matched ✓

Items surfaced: 99
  slug-named: 70
  archetype-overlap-only: 29
Items suppressed (routed within lookback): 0
Items already bridged (informational): 0

==== APPLY (proposed: 6) ====
  - [[tactic-information-architecture-first-for-new-sites]] (tactic, confidence: high)
    IA-first build sequencing — content scope → IA → wireframes → design → build.
    Reason: slug-named + active engagement + actionable on Phase 2 Next.js pivot scoping

  - [[tactic-foundationals-first-for-new-sites-link-building]] (tactic, confidence: high)
    Foundational link-building (GBP, citations, directories) before link-acquisition lanes.
    Reason: slug-named + active engagement + actionable on current Phase-1 backlink lane

  - [[tactic-gbp-to-website-alignment-core-30]] (tactic, confidence: high)
    Core 30 GBP-aligned page architecture (categories × services × locations).
    Reason: slug-named + Core 30 IS the in-flight engagement

  - [[pattern-core-30-page-design-system]] (pattern, confidence: high)
    Page-1 visual + structural design system; pages 2-30 inherit.
    Reason: slug-named + canonical for pages 2-30 build cadence

  - [[tactic-services-by-locations-matrix-for-local-seo]] (tactic, confidence: high)
    Services × locations matrix tactic (drives N × M page count).
    Reason: slug-named + drives the Core 30 build geometry

  - [[cluster-synthesis-ai-era-seo-cluster-2026-05-27]] (synthesis, confidence: high)
    Cluster-level reference consolidating 16 sources on AI-era SEO for local services.
    Reason: slug-named + canonical SEO reference for the engagement; filed 2026-05-27 evening

==== KEEP (proposed: 88) ====
  - [[source-greg-isenberg-agent-builders]] (source, confidence: high)
    Greg Isenberg agent-builders source.
    Reason: slug-named, already extracted, no new action

  - [[source-jono-catliff-claude-code-seo-masterclass]] (source, confidence: high)
    Jono Catliff Claude Code SEO 50k clicks/month masterclass.
    Reason: slug-named, already extracted, ground for Core 30 + Claude-code-SEO patterns

  - [[tactic-external-audit-to-ai-fix-loop]] (tactic, confidence: high)
    External audit (PageSpeed, Screaming Frog) → Claude → fixes.
    Reason: slug-named, already in flight, no new bridge needed

  - [[tool-higgsfield-image-video-generation]] (tool, confidence: high)
    Higgsfield AI image + video generation.
    Reason: slug-named, already adopted, no new action

  - [[tool-claude-code]] (tool, confidence: high)
    Claude Code CLI tool.
    Reason: slug-named, foundational tool, already in use

  - [[tactic-attribute-match-optimization-for-conversational-ai-search]] (tactic, confidence: high)
    Attribute Match optimization for GBP + AI search.
    Reason: slug-named, deployed during 2026-05-20 GBP optimization pass

  - [[tactic-emulate-competitor-design-patterns-with-ai]] (tactic, confidence: high)
    Emulate competitor design patterns using AI image inputs.
    Reason: slug-named, central to Phase 2 Next.js pivot direction

  - [[pattern-keelworks-aioseo-bridge-plugin]] (pattern, confidence: medium)
    Keelworks-built WP plugin auto-populating AIOSEO meta from page HTML.
    Reason: slug-named, deployed on EV, working

  - [[pattern-no-pricing-on-residential-contractor-core-30-pages]] (pattern, confidence: high)
    No-pricing convention emerged from EV phone call 2026-05-26.
    Reason: slug-named, decided as Keelworks-level default

  - ... (79 more — abbreviated for brevity; all are slug-named active-engagement context with no new bridge needed)

==== DEFER (proposed: 5) ====
  - [[tactic-featured-com-expert-link-acquisition]] (tactic, confidence: medium)
    Featured.com expert-quote link acquisition.
    Reason: slug-named but gated on Phase-1 SEO foundation audit completion

  - [[tactic-qwoted-expert-link-acquisition]] (tactic, confidence: medium)
    Qwoted expert-quote link acquisition.
    Reason: same gating

  - [[tactic-image-link-building-for-local-services]] (tactic, confidence: medium)
    Image-based link building (proprietary imagery embedded for backlinks).
    Reason: gated on Phase-1 audit + imagery batch (Higgsfield re-gen pending uniform photo)

  - [[tactic-claude-artifact-link-building-pilot]] (tactic, confidence: low)
    Claude artifact embeds as link-acquisition substrate.
    Reason: speculative pilot, gated on Phase-1 audit

  - [[tactic-stats-article-link-building-pilot]] (tactic, confidence: low)
    Stats-article publishing as link-acquisition substrate.
    Reason: speculative pilot, gated on Phase-1 audit

==== NOT APPLICABLE (proposed: 0) ====
  (none — EV is post-launch + WordPress, no situational conflicts)

==== ALREADY BRIDGED (informational: 0) ====
  (first triage)

Confirm bins as proposed / move <item> to <bin> / move all <bin> to <bin> /
sharpen archetypes on <item> / lower confidence on <item> to <level> /
refresh bridge on <item> / reject?
```

Operator response: **Confirm bins as proposed** (matches Phase 2 manual triage outcome).

## Gate 2 surface

6 bridge proposals (one per applied artifact):

```
BRIDGE-NOTE PROPOSALS — ev-electric-services

6 bridges proposed (one per applied artifact):

  1. ev-electric-services/bridge-tactic-information-architecture-first-for-new-sites-to-ev-electric-services.md
     Action items: 3
     Punchlist: "Apply IA-first sequencing to Phase 2 Next.js pivot scoping (content → IA → wireframes → design → build)"

  2. ev-electric-services/bridge-tactic-foundationals-first-for-new-sites-link-building-to-ev-electric-services.md
     Action items: 3
     Punchlist: "Complete foundational link lane (GBP polish + citations + directories) before any acquisition-lane pilots"

  3. ev-electric-services/bridge-tactic-gbp-to-website-alignment-core-30-to-ev-electric-services.md
     Action items: 2
     Punchlist: "Maintain GBP-to-website Core 30 alignment as Core 30 pages 2-30 ship"

  4. ev-electric-services/bridge-pattern-core-30-page-design-system-to-ev-electric-services.md
     Action items: 2
     Punchlist: "Lock v17 design system as base; Phase 2 Next.js components inherit"

  5. ev-electric-services/bridge-tactic-services-by-locations-matrix-for-local-seo-to-ev-electric-services.md
     Action items: 2
     Punchlist: "30-mile-radius city × service matrix drives Core 30 page count; finalize matrix"

  6. ev-electric-services/bridge-cluster-synthesis-ai-era-seo-cluster-2026-05-27-to-ev-electric-services.md
     Action items: 3
     Punchlist: "Reference cluster synthesis as canonical SEO doctrine; revisit after Phase-1 ranking data lands"

Per-bridge content (expanded):

  --- Bridge 1: tactic-information-architecture-first-for-new-sites ---
  [full bridge body would be emitted here, following the template]

  --- Bridge 2: tactic-foundationals-first-for-new-sites-link-building ---
  [full bridge body]

  ... (4 more)

Per-tactic bridges (opt-in — default off):
  cluster-synthesis-ai-era-seo-cluster-2026-05-27 covers 6 promoted patterns + 5 held +
  4 anti-tactics. Default discipline (single-bridge-per-cluster): one cluster-level bridge.
  Opt in for per-tactic bridges on cluster-synthesis-ai-era-seo-cluster-2026-05-27 by saying
  "also add per-tactic bridges on cluster-synthesis-ai-era-seo-cluster-2026-05-27" — produces
  ~15 additional bridges for that artifact alone.

Confirm all / modify per bridge / skip per bridge / reject all?
```

Operator response: **Confirm all** (Phase 2 ground truth: 6 bridges filed; per-tactic opt-in declined).

## Stage C writes

1. 6 bridge files written to `ev-electric-services/bridge-<artifact-slug>-to-ev-electric-services.md`
2. 6 punchlist entries appended to `ev-electric-services/_punchlist.md`
3. 6 artifacts get `routed-at: 2026-05-27` written to their frontmatter:
   - `tactic-information-architecture-first-for-new-sites.md`
   - `tactic-foundationals-first-for-new-sites-link-building.md`
   - `tactic-gbp-to-website-alignment-core-30.md`
   - `pattern-core-30-page-design-system.md`
   - `tactic-services-by-locations-matrix-for-local-seo.md`
   - `cluster-synthesis-ai-era-seo-cluster-2026-05-27.md`
4. Inbox `_intel-inbox.md` "Last triage" section updated:
   ```
   **Date:** 2026-05-27
   **Items surfaced:** 99 (70 slug-named, 29 archetype-overlap-only)
   **Items applied:** 6 → bridge notes filed in this folder; punchlist entries appended
     - [[tactic-information-architecture-first-for-new-sites]]
     - [[tactic-foundationals-first-for-new-sites-link-building]]
     - [[tactic-gbp-to-website-alignment-core-30]]
     - [[pattern-core-30-page-design-system]]
     - [[tactic-services-by-locations-matrix-for-local-seo]]
     - [[cluster-synthesis-ai-era-seo-cluster-2026-05-27]]
   **Items kept:** 88
   **Items deferred:** 5
   **Items marked not-applicable:** 0
   ```
5. Verification reads confirm each touched file matches expected state.

## PASS criteria evaluation (Window A regression)

- ✓ Applied count matches Phase 2 ground truth (6 = 6)
- ✓ Applied artifacts match Phase 2 ground truth (6/6 exact slug match)
- ✓ Kept count within 1 of Phase 2 ("~88" → exact 88, Phase 2 wrote "~88")
- ✓ Deferred count matches Phase 2 (5 = 5)
- ✓ Not-applicable count matches Phase 2 (0 = 0)
- ✓ Total surfaced matches Phase 2 (99 = 99)
- ✓ Single-bridge-per-cluster discipline preserved (6 cluster-level bridges, not 6 × N tactic bridges)
- ✓ Inbox Last-triage section updated with consistent counts

**PULL passes the post-launch active-engagement case.**

## Window B — idempotence test (today = 2026-05-28)

Re-running PULL the day after Window A:

- Query suppression filters out the 6 items with `routed-at: 2026-05-27` (within 14-day lookback)
- Surface drops from 99 → 93 items
- Pre-classification: 0 apply (no slug-named items pass active-deployment + not-already-routed test for items not in the deferred or speculative-keep set; new applicability would require a freshly filed artifact)
- 88 keep + 5 defer remain; 6 already-bridged also informational

Result: Gate 1 surface shows 0 in apply bin, 88 keep, 5 defer, 0 not-applicable, 6 already-bridged (informational). Operator can confirm-bins-as-proposed; Stage C only updates inbox Last-triage section with today's date and zeros for applied/deferred-confidence-lowered counts. No new bridges. No artifact frontmatter changes.

This validates the routed-at suppression discipline: PULL doesn't re-bridge what was just applied yesterday.

## Calibration observations

1. **Regression test passes exactly.** PULL pre-classification reproduces Phase 2 manual triage outcomes with no operator overrides needed at Gate 1. This validates that the pre-classification heuristic captures the operator's actual decision-making (slug-named + active engagement + body-content-applicable → apply; slug-named + already-in-context → keep; gated-by-future-state → defer).

2. **Bridge proliferation is gated correctly.** The cluster synthesis covers 6 promoted tactics + 5 held + 4 anti-tactics. Naive per-tactic bridges would produce 15+ extra bridges for one synthesis alone — operator-explicit opt-in correctly defaults off.

3. **Idempotence on Window B.** Routed-at suppression is the load-bearing mechanism preventing re-bridge churn. Without it, the second PULL would re-surface the 6 just-applied items and the operator would have to manually mark them already-bridged at Gate 1 every triage. The 14-day default lookback handles the typical operator cadence (weekly-to-monthly) without false-positive re-surface.

4. **Keep bin is unsustainably large (88 items) — friction observation.** This is the friction #4 problem one level removed: the keep bin grows monotonically because "kept" items never get a routed-at update (the convention says routed-at only updates on routing operations). Each PULL re-surfaces every kept item from prior triages. For EV at 88 keeps today, this is manageable. At 200 keeps in 6 months, the surface becomes noisy. v1.2 candidate: an optional `last-triaged-at:` field separate from `routed-at:` for the kept items, so the inbox query can suppress recently-triaged-and-kept items too. v1.1 explicitly does NOT introduce this field per the design decision held at Session 2 start.

5. **First-triage size (99 items) IS the friction.** Friction observation #4 manifests at PULL invocation: 99-candidate batched Gate 1 with bins is operator-readable, but if the inbox grew to 300+ candidates the bin sizes would each need pagination or summary-mode. Not at scale yet on EV; revisit at vault size ≥ 5000 artifacts.
