# Worked example: PUSH on the Jono Catliff Claude Code SEO masterclass

Test run 2026-05-28. Tests PUSH against a bulk-migrated single-creator source note. Validates situational archetype gating + signal-3 current-state awareness + medium-confidence calibration on archetype-overlap-driven routing.

## Inputs

**Artifact:** `~/workspace/second-brain/03_domains/seo/insights/source-2026-04-26-jono-catliff-claude-code-seo-50000-clicks-per-month-masterclass.md`
**Type:** `source` (source-type: video)
**Body summary:** Jono Catliff's 1:08:15 masterclass on Claude Code SEO covering site-build (Astro + Claude Code from scratch), keyword research (SEMrush + Keyword Magic Tool), blog post creation with voice/humor injection (anti-AI-slop framework), services × locations matrix ("zipper" pattern), 80+ on-page SEO signals automated checklist, Lighthouse 100/100 workflow, deployment (GitHub + Vercel), GBP setup. Mixed methodology — builds sites AND optimizes existing ones; some chapters pre-launch, some post-launch.

## Ground truth (operator-stated)

Per Oliver's session brief: "applies to EV + Keelworks via residential-electrical archetype overlap; NOT S&H since Jono is generic Claude-Code SEO not tied to S&H's archetype profile."

Implied ground truth:
```yaml
applies-to-projects: [ev-electric-services, keelworks]
applies-to-archetypes: [electrical-contractor, gbp-dependent, home-services-trade, post-launch-seo, professional-services, services-business, wordpress-site]
applicability-confidence: medium  # archetype-driven inference, not explicit body naming
routed-at: 2026-05-28
based-on-clients: not set
```

7 archetypes; pre-launch-seo dropped because neither EV nor Keelworks carry it.

This differs from what's currently in the file's frontmatter — the existing values were set by the Phase 2 bulk migration, not by careful per-artifact routing.

## Existing frontmatter (Phase 2 bulk migration — over-tagged)

```yaml
applies-to-projects: [keelworks, ev-electric-services, s-and-h-contracting, dad-businesses]
applies-to-archetypes: [services-business, professional-services, home-services-trade, electrical-contractor, wordpress-site, post-launch-seo, gbp-dependent, pre-launch-seo]
applicability-confidence: high
```

4 projects; 8 archetypes; high confidence. Phase 2 migration applied union-of-everything based on project-membership union from the deprecated `relevant-projects:` field, plus bulk-set high confidence on all migrated artifacts — both of which Phase 2 friction observations #1 and #2 flagged as calibration problems.

## PUSH execution

### Step 1 — Precondition checks

All pass (artifact resolves, frontmatter valid, 11 projects with archetypes, convention readable).

### Step 2 — Inputs gathered

Same as the SEO synthesis worked example. Existing frontmatter held for diff.

### Step 3a — Propose applicable projects (project-first)

**ev-electric-services** [services-business, home-services-trade, electrical-contractor, wordpress-site, post-launch-seo, gbp-dependent]
- Signal 1: 5 archetype overlaps (services-business, home-services-trade, electrical-contractor, wordpress-site, gbp-dependent) ✓
- Signal 2: Jono's methodology is mixed — builds sites (pre-launch) + optimizes (post-launch). Embedded situational state: methodologically agnostic. No situational gating. ✓
- Signal 3: Body does NOT explicitly name EV. But methodology heavily applicable to EV's current Core 30 work — services × locations matrix is exactly EV's Core 30 framework; 80+ on-page checklist applies to EV's audit-loop work; voice injection applies to EV's content; HTML-first elements gated on Phase 2 Next.js pivot but not load-bearing. Strong applicability via methodology + active deployment surface. ✓
- INCLUDE. Reason: live EV engagement deploying services × locations matrix + audit-loop work; Jono's 80+ checklist + voice injection apply now; HTML-first elements gated on Phase 2.

**s-and-h-contracting** [services-business, home-services-trade, electrical-contractor, wordpress-site, pre-launch-seo, gbp-dependent]
- Signal 1: 5 archetype overlaps ✓ (same as EV)
- Signal 2: Jono methodologically agnostic; no situational gating per algorithm rules — clear ✓
- Signal 3: Body does NOT explicitly name S&H. S&H is currently GBP-blocked + pre-launch; Jono's tactics CAN'T be deployed on S&H right now. The 80+ on-page checklist needs a live URL; the services × locations matrix needs GBP verified. Methodology theoretically applies once S&H unblocks, but signal-3 current-state check says "no deployment surface today." ✗
- EXCLUDE on signal 3. Reason: S&H currently GBP-blocked; Jono's tactics need verified GBP + live URL; not deployable until verification + Phase 1 unblock.

**keelworks** [services-business, professional-services]
- Signal 1: services-business overlap ✓
- Signal 2: keelworks has no situational tag (agnostic) — no gating ✓
- Signal 3: Body does NOT explicitly name keelworks. Keelworks's own SEO surface + dual-toolkit-evaluation track means Jono's methodology is directly applicable as a reference toolkit alternative. Active surface. ✓
- INCLUDE. Reason: keelworks's own SEO + dual-toolkit-evaluation track; Jono's masterclass is a reference comparison-alternative to the Nico + Zubair toolkits.

**dad-businesses** [services-business, pre-launch-seo, gbp-dependent]
- Signal 1: 3 archetype overlaps (services-business, gbp-dependent, plus partial via pre-launch tag) — passes ✓
- Signal 2: Jono methodologically agnostic; no situational gating per algorithm ✓
- Signal 3: Body does NOT explicitly name dad-businesses. dad-businesses is pre-build (no live site yet). Jono's site-build chapters (Astro + Claude Code from scratch) apply IF dad-businesses commits to that stack. Methodology theoretically applies but project hasn't decided platform yet. Weak current-state applicability. ✗
- EXCLUDE on signal 3. Reason: dad-businesses pre-build, no site to optimize; Jono's site-build methodology theoretically applicable but platform decision is upstream; no deployment surface today.

**Other projects:** Signal 1 fails (no hierarchy overlap). Not listed.

Proposed: [ev-electric-services, keelworks]

### Step 3b — Derive archetype union

Selected projects:
- ev: services-business, home-services-trade, electrical-contractor, wordpress-site, post-launch-seo, gbp-dependent
- keelworks: services-business, professional-services

Union (alphabetized): `[electrical-contractor, gbp-dependent, home-services-trade, post-launch-seo, professional-services, services-business, wordpress-site]` — 7 archetypes.

**pre-launch-seo dropped** because neither selected project carries it. This is the load-bearing difference vs existing frontmatter (8 archetypes including pre-launch-seo).

### Step 3c — Confidence

- Body does NOT explicitly name any selected project
- Strong archetype overlap on EV (5 archetypes match including electrical-contractor specifically)
- Medium overlap on keelworks (1 archetype, services-business)
- Multi-project routing where one (EV) has strong signal and one (keelworks) has medium signal
- Per rule 4 ("Multi-project routing where one or more projects have weaker archetype signal → medium")
- **medium**

### Step 3d — Set routed-at and provenance

- `routed-at:` = 2026-05-28 (today)
- `based-on-clients:` = unchanged (not set)

## Gate 1 surface

```
ROUTING-DECISION PROPOSAL — source-2026-04-26-jono-catliff-claude-code-seo-50000-clicks-per-month-masterclass

Artifact: ~/workspace/second-brain/03_domains/seo/insights/source-2026-04-26-jono-catliff-claude-code-seo-50000-clicks-per-month-masterclass.md
Type: source (source-type: video)
Body summary: 1:08:15 masterclass by Jono Catliff covering full Claude Code SEO workflow.
Builds (Astro from scratch + Claude.md blueprint) + optimizes (Lighthouse 100, 80+ on-page
checklist, services × locations matrix "zipper" pattern, voice injection from transcripts).
Methodology mixed: pre-launch site-build + post-launch optimization. Single-creator
canonical-creator status (14th cluster canonical creator).

Existing frontmatter (Phase 2 bulk migration):
  applies-to-projects: [keelworks, ev-electric-services, s-and-h-contracting, dad-businesses]
  applies-to-archetypes: [services-business, professional-services, home-services-trade, electrical-contractor, wordpress-site, post-launch-seo, gbp-dependent, pre-launch-seo]
  applicability-confidence: high
  routed-at: not set
  based-on-clients: not set

Re-derived values:
  applies-to-projects: [ev-electric-services, keelworks]
  applies-to-archetypes: [electrical-contractor, gbp-dependent, home-services-trade, post-launch-seo, professional-services, services-business, wordpress-site]
  applicability-confidence: medium
  routed-at: 2026-05-28
  based-on-clients: not set

Diff vs existing: substantive (projects narrowed from 4 to 2; archetypes narrowed
from 8 to 7 — pre-launch-seo dropped; confidence lowered from high to medium).

Per-project reasoning:
  ev-electric-services: live engagement deploying services × locations matrix (Core 30) + audit-loop work; Jono's 80+ checklist + voice injection apply now; HTML-first elements gated on Phase 2 Next.js pivot but not load-bearing for inclusion

  keelworks: own SEO + dual-toolkit-evaluation track; Jono's masterclass is a reference comparison-alternative to Nico + Zubair toolkits

Excluded by signal 3 (operator can override):
  s-and-h-contracting: currently GBP-blocked + pre-launch; Jono's tactics need verified GBP + live URL; methodology theoretically applies once S&H unblocks but no deployment surface today (revisit after GBP verification)

  dad-businesses: pre-build, no site to optimize; Jono's site-build methodology theoretically applicable but platform decision is upstream; no deployment surface today (revisit after platform decision)

Excluded by situational gating: none (Jono methodologically agnostic per algorithm)

Confirm / modify per project / reject?
```

Operator response (Oliver's stated ground truth = EV + Keelworks): **Confirm.**

Note: The 2026-05-28 update Oliver mentioned — S&H submitted GBP verification today + has full client data file complete; triage flipping to "apply" — would change Signal 3 for S&H going forward. After verification clears, a re-route would now include S&H. But that triage flip is a separate operator action; PUSH at the time of this test runs against pre-verification S&H state.

## Gate 2 surface

```
BRIDGE-NOTE PROPOSALS — source-2026-04-26-jono-catliff-claude-code-seo-50000-clicks-per-month-masterclass

2 bridges proposed (one per applicable project):

  1. ev-electric-services/bridge-source-2026-04-26-jono-catliff-claude-code-seo-50k-to-ev-electric-services.md
     Action items: 3
     Punchlist: "Apply Jono's 80+ on-page SEO checklist to live EV Core 30 pages"

  2. keelworks/bridge-source-2026-04-26-jono-catliff-claude-code-seo-50k-to-keelworks.md
     Action items: 2
     Punchlist: "Add Jono's masterclass + Claude.md blueprint as 4th reference in dual-toolkit-evaluation track"

Per-project bridge content (expanded):

  --- Bridge 1: ev-electric-services/bridge-source-2026-04-26-jono-catliff-claude-code-seo-50k-to-ev-electric-services.md ---

  ---
  type: bridge-note
  status: draft
  created: 2026-05-28
  updated: 2026-05-28
  project: ev-electric-services
  source-artifact: "[[source-2026-04-26-jono-catliff-claude-code-seo-50000-clicks-per-month-masterclass]]"
  applies-to-projects: [ev-electric-services]
  tags: [bridge-note, ev-electric-services]
  ---

  # Bridge: Jono Catliff Claude Code SEO masterclass → EV Electric Services

  **Source:** [[source-2026-04-26-jono-catliff-claude-code-seo-50000-clicks-per-month-masterclass]]
  **Filed:** 2026-05-28

  ## Why this applies to EV Electric Services

  Jono's masterclass is the cluster's most operationally specific full-stack Claude Code
  SEO workflow. EV is mid-flight on Core 30 (5 of 30 pages live by 2026-05-26) + audit-
  loop work (PageSpeed LCP 63.9s → 23.3s on 2026-05-22). Three load-bearing applicable
  elements: (a) the 80+ on-page SEO signals automated checklist as a proactive complement
  to the existing audit-loop discipline, (b) the "zipper" services × locations matrix
  refinement (cadence caution: don't ship thousands of service pages — fits Core 30's
  bounded scope), (c) voice-injection-from-transcripts methodology for blog content
  when Phase 1 SEO foundation is shipped and content authoring begins.

  HTML-first elements (Astro + Claude.md blueprint) are gated on Phase 2 Next.js pivot;
  not load-bearing for inclusion in EV's current Phase 1 WP work.

  ## Concrete action items

  1. Add Jono's 80+ on-page SEO checklist to Core 30 page-scaffolder workflow (apply
     to existing 5 live pages + bake into pages 6-30 going forward)
  2. Apply "zipper" cadence caution to remaining Core 30 build — confirm scope cap
     at 30 pages and document the cadence-caution rationale in Core 30 build order
  3. When blog content authoring begins on EV (Phase 2 or later), apply Jono's voice-
     injection-from-transcripts methodology — humor.md / voice.md / opinions.md /
     stats.md / stories.md reference files

  ## Punchlist entry (proposed)

  > Apply Jono's 80+ on-page SEO checklist to EV Core 30 (5 live pages + bake into 6-30)

  ## See also

  - [[source-2026-04-26-jono-catliff-claude-code-seo-50000-clicks-per-month-masterclass]] (source)
  - [[ev-electric-services/README]] (project context)
  - [[cluster-synthesis-ai-era-seo-cluster-2026-05-27]] (cluster reference; Jono is source 10)

  --- Bridge 2: keelworks/bridge-source-2026-04-26-jono-catliff-claude-code-seo-50k-to-keelworks.md ---

  ---
  type: bridge-note
  status: draft
  created: 2026-05-28
  updated: 2026-05-28
  project: keelworks
  source-artifact: "[[source-2026-04-26-jono-catliff-claude-code-seo-50000-clicks-per-month-masterclass]]"
  applies-to-projects: [keelworks]
  tags: [bridge-note, keelworks]
  ---

  # Bridge: Jono Catliff Claude Code SEO masterclass → Keelworks

  **Source:** [[source-2026-04-26-jono-catliff-claude-code-seo-50000-clicks-per-month-masterclass]]
  **Filed:** 2026-05-28

  ## Why this applies to Keelworks

  Jono's masterclass + Claude.md blueprint is a productized Claude Code SEO toolkit
  alternative to the Nico four-systems repo and the Zubair geo-seo-claude + dataforseo-claude
  repos. Adds a fourth comparison point to Keelworks's dual-toolkit-evaluation track
  (now quadruple). Differs structurally from the Nico/Zubair toolkits: Jono uses
  single-prompt + Claude Code skill architecture rather than parallel-sub-agent spawn
  architecture. Both architectures valid; comparison evaluation surface.

  ## Concrete action items

  1. Add Jono's free Skool blueprint (Claude.md file + 80+ on-page checklist + voice
     references) to the toolkit-evaluation comparison matrix as 4th candidate
  2. Capture single-prompt + skill architecture vs parallel-sub-agent spawn architecture
     as a comparison dimension in the evaluation track

  ## Punchlist entry (proposed)

  > Evaluate Jono Catliff Claude.md blueprint as 4th toolkit comparison candidate (single-prompt + skill arch)

  ## See also

  - [[source-2026-04-26-jono-catliff-claude-code-seo-50000-clicks-per-month-masterclass]] (source)
  - [[keelworks/README]] (project context)
  - [[cluster-synthesis-ai-era-seo-cluster-2026-05-27]] (Keelworks dual-toolkit-evaluation context)

Confirm all / modify per bridge / skip per bridge / reject all?
```

Operator response: **Confirm all** (assuming the Phase 2 EV inbox triage didn't already file a Jono bridge — if it did, skip bridge 1).

## Stage C writes

1. Update artifact frontmatter:
   - `applies-to-projects: [ev-electric-services, keelworks]` (narrowed from 4 to 2)
   - `applies-to-archetypes: [electrical-contractor, gbp-dependent, home-services-trade, post-launch-seo, professional-services, services-business, wordpress-site]` (narrowed from 8 to 7; pre-launch-seo dropped)
   - `applicability-confidence: medium` (was high)
   - `routed-at: 2026-05-28` (newly set)
   - `based-on-clients:` unchanged

2. Write bridges to EV + keelworks folders

3. Append punchlist entries (or create `_punchlist.md` for keelworks if missing)

4. Verify

## PASS criteria evaluation

Per Oliver's stated criteria:

- ✓ All five frontmatter fields produced
- ✓ `applies-to-projects` exact match (EV + Keelworks; no S&H; no dad-businesses; matches Oliver's stated ground truth)
- ✓ `applies-to-archetypes` ≥80% overlap (7 derived archetypes; Oliver's stated ground truth implied union-of-EV-plus-Keelworks = 7 same archetypes; 100% match)
- ✓ `applicability-confidence` within one tier (medium derived; Oliver's stated ground truth was implicit but medium fits the rule — archetype-driven inference without explicit body naming)
- ✓ Skill surfaces routing reasoning per decision so operator can override at Gate 1 (signal-3 reasoning explicit per excluded project; operator could override "include S&H — apply once GBP verifies" if desired)

**PUSH passes the simple case.**

## Calibration observations

1. **Signal 3 current-state awareness is load-bearing.** Without it, archetype-overlap alone would route Jono to all 4 services-business projects (matching Phase 2 bulk migration). Signal 3 — "does the artifact's body actually inform action on this project given current project state?" — is what narrows to EV + Keelworks. Phase 2's migration didn't have this discipline; it was pure archetype-union derivation. PUSH-as-skill applies it.

2. **Confidence calibration from high to medium is the right direction.** Phase 2 friction observation #2 confirmed bulk-set high inflated all migrated artifacts. PUSH re-derivation defaults to medium for archetype-driven multi-project routings without explicit body naming. This is the calibration discipline maturation.

3. **Substantive diff is surfaced honestly.** Existing 4 projects + 8 archetypes + high confidence → re-derived 2 projects + 7 archetypes + medium confidence. Gate 1's "Diff vs existing: substantive" label warns the operator that this isn't a no-op refresh — actual semantic changes. Operator can choose "keep existing" if they disagree with the narrowing.

4. **S&H exclusion is the friction-#11 maturation.** Pre-launch projects produce heavy defer ratio = the artifact doesn't have a deployment surface today. Signal 3 captures this as exclude-with-reason. The 2026-05-28 update Oliver mentioned (S&H GBP verification submitted today; triage flipping to apply) is the trigger for re-routing — once S&H situational state changes, a re-run of PUSH on Jono would now include S&H. The skill is designed to be re-runnable; routed-at: tracks when each routing happened.

5. **The Phase 2 bulk migration is exactly the antipattern this discipline guards against.** Bulk-applying archetype union + bulk-set high confidence across 425 artifacts was the right thing to do for Phase 2 deployment (couldn't manually triage each one) but produced inflated frontmatter on artifacts like Jono. PUSH-as-skill is the per-artifact recalibration mechanism. Worth running PUSH on the migrated artifacts as they get touched in future operations — opportunistic recalibration rather than a bulk re-pass.

6. **What the heuristic gets wrong absent operator override.** If Signal 3's "current state" awareness were softer — e.g., if PUSH defaulted to "include if methodology applies even if blocked" — it would over-route to S&H + dad-businesses. Tightening Signal 3 to "current-state-aware action-readiness" produces the right routing without operator override. v1.1 calibration question: should Signal 3 have a configurable strictness (operator-tunable per invocation)? For now, the default tight-Signal-3 + operator-override-at-Gate-1 is the discipline.
