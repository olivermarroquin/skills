# Worked example: PUSH on the SEO cluster synthesis

Test run 2026-05-28. Tests PUSH against an operator-produced multi-project synthesis. Validates project-first routing + archetype-union derivation + multi-project bridge discipline.

## Inputs

**Artifact:** `~/workspace/second-brain/03_domains/seo/cluster-synthesis-ai-era-seo-cluster-2026-05-27.md`
**Type:** `synthesis` (synthesis-shape: cluster)
**Body summary:** Cluster-level reference consolidating 16 source notes on AI-era SEO for local services across 10 months. Covers GBP-to-website alignment (Core 30), services × locations matrices, external audit-to-AI-fix loops, HTML-first static sites, content freshness for AI citation, Capsule Content for AEO/GEO, attribute match for conversational AI. Operator-deployed at scale on EV; partially deployed pending on S&H; informs Keelworks's own SEO + dual-toolkit-evaluation; informs dad-businesses platform decisions.

## Ground truth (synthesis was operator-routed at creation 2026-05-27)

```yaml
applies-to-projects: [ev-electric-services, s-and-h-contracting, keelworks, dad-businesses]
applies-to-archetypes: [services-business, professional-services, home-services-trade, electrical-contractor, wordpress-site, pre-launch-seo, post-launch-seo, gbp-dependent]
applicability-confidence: high
routed-at: 2026-05-27
based-on-clients: not set
```

This is the canonical ground truth because the synthesis was produced WITH the intel-routing convention (not migrated). Decision archaeology in the synthesis at line 286-288 confirms operator-explicit selection of projects at the multi-source-synthesis shape-and-destination gate.

## PUSH execution

### Step 1 — Precondition checks

- Artifact resolved ✓
- Frontmatter valid (type, status, created, updated, tags all present) ✓
- 11 projects with archetypes declared (2 clients + 9 personal) ✓
- Convention spec readable ✓

### Step 2 — Inputs gathered

- Artifact full content read
- 11 project READMEs read, archetypes extracted
- Convention spec re-read
- Existing frontmatter held for diff

### Step 3a — Propose applicable projects (project-first)

Project-by-project signal evaluation:

**ev-electric-services** [services-business, home-services-trade, electrical-contractor, wordpress-site, post-launch-seo, gbp-dependent]
- Signal 1: 5 hierarchy + situational archetypes overlap ✓
- Signal 2: synthesis is methodologically agnostic (covers both pre and post launch via different tactics within); no situational gating ✓
- Signal 3: body explicitly names EV ("services × locations matrix (EV Core 30 + S&H pending)," "audit-to-AI-fix loop (EV PageSpeed work shipped 2026-05-22)," etc.); active engagement deploying multiple covered tactics ✓
- INCLUDE. Reason: live EV engagement deploying Core 30 + Attribute Match + audit-loop tactics from this cluster; synthesis is canonical reference for ongoing work.

**s-and-h-contracting** [services-business, home-services-trade, electrical-contractor, wordpress-site, pre-launch-seo, gbp-dependent]
- Signal 1: 4 archetype overlaps ✓
- Signal 2: synthesis agnostic on launch state ✓
- Signal 3: body explicitly names S&H ("S&H GBP verification visit pending," "synthesis lands in S&H's keep state until GBP verifies") — explicit naming gives Signal 3 ✓ pass even with current-blocked state ✓
- INCLUDE. Reason: active S&H engagement (pre-launch, GBP-blocked); synthesis is keep-state reference for when GBP verifies.

**keelworks** [services-business, professional-services]
- Signal 1: services-business overlap ✓
- Signal 2: keelworks has no situational tag (agnostic) — no gating ✓
- Signal 3: body explicitly names keelworks ("Keelworks Phase 2 Next.js pivot... candidate timing," "Keelworks's own SEO; synthesis is operationally referenced for client-acquisition and for the dual-toolkit-evaluation track") ✓
- INCLUDE. Reason: keelworks's own SEO surface; informs client-acquisition + dual-toolkit-evaluation track + Phase 2 Next.js pivot timing.

**dad-businesses** [services-business, pre-launch-seo, gbp-dependent]
- Signal 1: 3 archetype overlaps ✓
- Signal 2: synthesis covers pre-launch tactics (HTML-first build, platform decisions) ✓
- Signal 3: body explicitly names dad-businesses ("dad-businesses — pre-build site; synthesis informs platform-decision and build-stack choices") ✓
- INCLUDE. Reason: pre-build site; synthesis informs platform-decision and HTML-first build-stack choice.

**Other projects** (resume-saas, hire-relay, legal-toolkit, ai-agency-core, app-factory, idea-factory, resume-factory): Signal 1 fails (no hierarchy overlap with services-business / home-services-trade / professional-services). Not listed; no further evaluation.

### Step 3b — Derive archetype union

Selected projects: [ev-electric-services, s-and-h-contracting, keelworks, dad-businesses]

Union of their archetypes:
- services-business (from all 4)
- professional-services (from keelworks)
- home-services-trade (from ev + sh)
- electrical-contractor (from ev + sh)
- wordpress-site (from ev + sh)
- pre-launch-seo (from sh + dad-businesses)
- post-launch-seo (from ev)
- gbp-dependent (from ev + sh + dad-businesses)

Union (alphabetized): `[electrical-contractor, gbp-dependent, home-services-trade, post-launch-seo, pre-launch-seo, professional-services, services-business, wordpress-site]` — 8 archetypes.

### Step 3c — Confidence

Multi-project routing where every project has explicit body naming + operator-produced synthesis with explicit project list at creation → **high**.

### Step 3d — Set routed-at and provenance

- `routed-at:` = 2026-05-28 (today)
- `based-on-clients:` = unchanged (was not set; remains not set)

## Gate 1 surface

```
ROUTING-DECISION PROPOSAL — cluster-synthesis-ai-era-seo-cluster-2026-05-27

Artifact: ~/workspace/second-brain/03_domains/seo/cluster-synthesis-ai-era-seo-cluster-2026-05-27.md
Type: synthesis (synthesis-shape: cluster)
Body summary: Cluster-level reference consolidating 16 sources on AI-era SEO for local
services. Covers Core 30 / GBP, services × locations, audit-to-AI-fix loops, HTML-first
static, content freshness, Capsule Content for AEO/GEO. Operator-produced 2026-05-27.

Existing frontmatter:
  applies-to-projects: [ev-electric-services, s-and-h-contracting, keelworks, dad-businesses]
  applies-to-archetypes: [services-business, professional-services, home-services-trade, electrical-contractor, wordpress-site, pre-launch-seo, post-launch-seo, gbp-dependent]
  applicability-confidence: high
  routed-at: 2026-05-27
  based-on-clients: not set

Re-derived values:
  applies-to-projects: [dad-businesses, ev-electric-services, keelworks, s-and-h-contracting]
  applies-to-archetypes: [electrical-contractor, gbp-dependent, home-services-trade, post-launch-seo, pre-launch-seo, professional-services, services-business, wordpress-site]
  applicability-confidence: high
  routed-at: 2026-05-28
  based-on-clients: not set

Diff vs existing: minor (only routed-at changes by 1 day from re-run; alphabetization
differences in lists are display-only, not semantic).

Per-project reasoning:
  ev-electric-services: live engagement deploying Core 30 + Attribute Match + audit-loop tactics covered in synthesis; explicit body naming
  s-and-h-contracting: active engagement, currently GBP-blocked; synthesis is keep-state reference until verification; explicit body naming
  keelworks: own SEO surface + client-acquisition + dual-toolkit-evaluation track + Phase 2 Next.js pivot timing; explicit body naming
  dad-businesses: pre-build site; synthesis informs platform-decision + HTML-first build-stack; explicit body naming

Excluded by situational gating: none (synthesis is launch-state-agnostic)
Excluded by signal 3: none

Confirm / modify per project / reject?
```

Operator response: **Confirm** (re-derivation matches existing intent; routed-at updates by 1 day is expected).

## Gate 2 surface

Bridge-note proposals — 4 bridges, one per project:

```
BRIDGE-NOTE PROPOSALS — cluster-synthesis-ai-era-seo-cluster-2026-05-27

4 bridges proposed (one per applicable project):

  1. ev-electric-services/bridge-cluster-synthesis-ai-era-seo-cluster-2026-05-27-to-ev-electric-services.md
     Action items: 3
     Punchlist: "Reference SEO cluster synthesis as canonical for Core 30 + audit-loop + AEO work"

  2. s-and-h-contracting/bridge-cluster-synthesis-ai-era-seo-cluster-2026-05-27-to-s-and-h-contracting.md
     Action items: 2
     Punchlist: "Reference SEO cluster synthesis as canonical reference; activate on GBP verification"

  3. keelworks/bridge-cluster-synthesis-ai-era-seo-cluster-2026-05-27-to-keelworks.md
     Action items: 3
     Punchlist: "Reference SEO cluster synthesis for Keelworks own SEO + dual-toolkit evaluation + Phase 2 Next.js timing"

  4. dad-businesses/bridge-cluster-synthesis-ai-era-seo-cluster-2026-05-27-to-dad-businesses.md
     Action items: 2
     Punchlist: "Reference SEO cluster synthesis for platform-decision + HTML-first build-stack"

Per-tactic bridges (opt-in — default off):
  Synthesis covers 6 promoted patterns + 5 held + 4 anti-tactics. Default discipline is
  one cluster-level bridge per project. Per-tactic bridges (would produce 24+ bridges
  across projects) are operator-explicit opt-in.

Confirm all / modify per bridge / skip per bridge / reject all?
```

**Phase 2 ground truth on bridges:** Workstream F shipped 5 bridges for EV (4 tactic-level + 1 synthesis-level) and 1 bridge for S&H (synthesis-level keep state). The 5 EV bridges were ALREADY filed before this synthesis routing pass — those were per-tactic bridges from the migrated tactics, not from the synthesis. The synthesis-level bridge on EV (file `bridge-cluster-synthesis-ai-era-seo-cluster-2026-05-27-to-ev-electric-services.md`) is already shipped per the Workstream E closeout note in the running execution log.

Operator response: **Skip bridges 1, 2** (already filed in Phase 2 — duplicate writes would conflict); confirm 3, 4 if not already present.

Bridge 1 (EV) already exists at `04_projects/clients/_active/ev-electric-services/bridge-cluster-synthesis-ai-era-seo-cluster-2026-05-27-to-ev-electric-services.md` per the Phase 2 execution log. PUSH detects this and surfaces at Gate 2; operator skip is correct.

Bridge 2 (S&H) — same. Phase 2 filed 1 S&H bridge for the synthesis; PUSH detects + operator skips.

Bridge 3 (Keelworks) — Phase 2 did NOT file a Keelworks bridge for this synthesis. PUSH would file it. Whether to file it depends on whether Keelworks's `_intel-inbox.md` triage produced the keep-not-bridge or apply-with-bridge outcome. The Phase 2 log doesn't show a triage pass on Keelworks's inbox (Workstream F was clients only). Operator decision.

Bridge 4 (dad-businesses) — same as Keelworks; no Phase 2 triage pass on personal-project inboxes.

This is itself a PUSH-discovered gap: the Phase 2 triage covered the 2 active client projects but didn't extend to the 9 personal projects' inboxes. PUSH surfaces this as a side effect of routing — when an artifact applies to a project whose inbox hasn't been triaged in the lookback window, PUSH proposes a bridge but the operator may say "let me just triage the inbox first" and reject the PUSH-proposed bridge.

For this worked example, assume operator confirms 3 + 4, skips 1 + 2 (already shipped).

## Stage C writes

If operator confirmed 3 + 4 only:

1. Update artifact frontmatter — only `routed-at:` changes (2026-05-27 → 2026-05-28); other fields already match re-derivation
2. Write bridge 3 to `keelworks/bridge-cluster-synthesis-ai-era-seo-cluster-2026-05-27-to-keelworks.md`
3. Write bridge 4 to `dad-businesses/bridge-cluster-synthesis-ai-era-seo-cluster-2026-05-27-to-dad-businesses.md`
4. Append punchlist entry to `keelworks/_punchlist.md` (or create if missing)
5. Append punchlist entry to `dad-businesses/_punchlist.md` (or create if missing)
6. Verify each write by reading touched files

## PASS criteria evaluation

Per Oliver's stated criteria (PUSH passes if):

- ✓ All five frontmatter fields produced
- ✓ `applies-to-projects` exact match against ground truth (4 projects, all 4 correct, no spurious additions, no missing)
- ✓ `applies-to-archetypes` ≥80% overlap (8/8 = 100% match)
- ✓ `applicability-confidence` matches within one tier (high = high, exact match)
- ✓ Skill surfaces routing reasoning per decision so operator can override at Gate 1

**PUSH passes the complex case.**

## Calibration observations

1. **Re-derivation matches operator intent.** This validates the project-first algorithm — when an artifact is operator-produced with explicit project naming in the body, PUSH re-derivation produces the same routing the operator made manually at creation. The synthesis decision archaeology (Audit-pass item #6) explicitly documented the archetype-union derivation; PUSH automates what was done manually.

2. **Existing-vs-rederived diff is the safety net.** Even when re-derivation matches existing exactly, surfacing the diff at Gate 1 lets the operator verify nothing drifted. For artifacts where re-derivation differs (e.g., migrated artifacts with bulk-applied frontmatter — see Jono worked example), the diff is load-bearing.

3. **Phase 2 already-shipped bridges are detected at Gate 2.** PUSH proposing duplicate writes is not a bug — it's the right default. Operator skip-per-bridge at Gate 2 handles the existing-bridge case cleanly without forcing PUSH to track its own state.

4. **The gap PUSH surfaced (personal-project inboxes not triaged).** Not a PUSH-on-this-artifact issue; it's a vault-hygiene observation that PUSH surfaces as a side effect. Worth carrying into the running execution log as a Phase 2 follow-up.

5. **Routed-at updates by 1 day on re-run.** This is correct behavior — PUSH timestamps the new routing operation. If operator wants to preserve the original 2026-05-27 routed-at (e.g., because the synthesis was first routed then), they can modify at Gate 1 with "keep routed-at: 2026-05-27." The default is fresh timestamp.
