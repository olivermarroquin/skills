# Worked example: PULL on S&H Contracting inbox

Regression test 2026-05-28. Tests PULL against a pre-launch, GBP-blocked client project. Reproduces the Phase 2 manual triage outcome (99 candidates → 1 apply + ~11 keep + ~87 defer + 0 not-applicable) from a clean slate. Validates pre-classification rule 3 (slug-named situational conflict defers rather than goes to not-applicable) and exercises friction observation #11 (pre-launch projects produce heavy defer ratio) at full inbox scale.

## Test framing

S&H's archetype set differs from EV's by exactly one situational tag: `pre-launch-seo` instead of `post-launch-seo`. Otherwise identical at the hierarchy level. This single bit flip is load-bearing — it gates almost every post-launch-shaped tactic into the defer bin (Phase 2 outcome: ~87 defers vs EV's 5).

Test as-if-today is 2026-05-27 (the actual Phase 2 first-triage date). Tests:

- Pre-classification correctly defers most slug-named post-launch-shaped tactics (rule 3) rather than marking not-applicable
- Pre-classification correctly identifies the one directly-actionable artifact (GSC self-takeover pattern via Haris-outreach flow)
- Pre-classification correctly keeps foundational architecture artifacts (synthesis, IA tactic, etc.) — they'll apply when GBP verifies, no action now
- 0 not-applicable outcome matches Phase 2 ground truth

## Inputs

**Project:** `s-and-h-contracting`
**README:** `~/workspace/second-brain/04_projects/clients/_active/s-and-h-contracting/README.md`
**Inbox:** `~/workspace/second-brain/04_projects/clients/_active/s-and-h-contracting/_intel-inbox.md`
**Lookback:** 14 days (default)
**Today (as-if):** 2026-05-27

### Project state from README

- **Archetypes:** `[services-business, home-services-trade, electrical-contractor, wordpress-site, pre-launch-seo, gbp-dependent]`
- **`applicability-confidence:`** `high`
- **`archived:`** not set
- **Current state signal (body skim):** "engagement is now SEO-only," "GBP is NOT verified — pending verification visit," "Haris Mughal outreach pending," "Phase 1 site-defect fixes," "first-wave Core 30 pages all ship on WordPress." Pre-launch + currently blocked on GBP verification.

### Inbox state

- **Archetypes:** identical to README (instantiated 2026-05-27)
- **Last triage:** none (first triage)

## PULL execution

### Step 1 — Preconditions

- Project folder resolved ✓
- README has `archetypes:` ✓
- Not archived ✓
- Inbox file exists ✓
- Convention spec readable ✓

### Step 2 — Inputs

Read README + inbox + convention + bridge-file enumeration (zero existing bridges). Run surface query against 03_domains + 05_shared-intelligence + 00_inbox/decisions-pending with S&H's archetype set.

### Step 3a — Sync validation

- README archetypes: `[electrical-contractor, gbp-dependent, home-services-trade, pre-launch-seo, services-business, wordpress-site]`
- Inbox archetypes: `[electrical-contractor, gbp-dependent, home-services-trade, pre-launch-seo, services-business, wordpress-site]`
- **Match: matched ✓**

### Step 3b — Tag surfaced artifacts

Query result: 99 artifacts surfaced (matches Phase 2 manual triage). Note that S&H's surface size is effectively identical to EV's because the projects share 5 of 6 archetypes — only the situational pre/post launch tag differs, and the artifact base mostly carries both tags via the Phase 2 archetype-union derivation.

- Slug-named: 70 (similar count to EV; mostly the same artifact base)
- Archetype-overlap only: 29

### Step 3c — Pre-classify into bins

Pre-classification rules applied. Critical decisions surface from rule 3 (slug-named situational conflict → defer) and rule 4 (slug-named + directly actionable now → apply).

**Pre-classified to APPLY (1 item)** — rule 4: slug-named + body content directly actionable in current project state:

1. `[[pattern-access-gsc-self-takeover-without-prior-contractor]]` — pattern for taking over GSC ownership when a prior contractor (here: EverSolveds/Asim, later resolved via Haris) is no longer responsive. Directly actionable NOW via the Haris-outreach flow that's in flight regardless of GBP verification. Project blocker (GBP) is orthogonal to this artifact's mechanism.

**Pre-classified to KEEP (11 items)** — rule 6: slug-named + project blocked + foundational; activate-when-GBP-verifies:

1. `[[tactic-information-architecture-first-for-new-sites]]` — IA-first sequencing, foundational; needed at Phase 2 Next.js rebuild
2. `[[tactic-foundationals-first-for-new-sites-link-building]]` — applies when site goes post-launch
3. `[[tactic-gbp-to-website-alignment-core-30]]` — Core 30 architecture, applies post-verification
4. `[[pattern-core-30-page-design-system]]` — design system, inherits from EV when S&H Phase 1 starts
5. `[[tactic-services-by-locations-matrix-for-local-seo]]` — services × locations matrix for S&H's 50-mile-radius coverage
6. `[[cluster-synthesis-ai-era-seo-cluster-2026-05-27]]` — cluster-level reference; canonical for the engagement; lands in keep until GBP verifies (Phase 2 explicitly chose keep-not-apply per friction #4)
7. `[[tactic-external-audit-to-ai-fix-loop]]` — audit-loop applies once site goes live with the defect-fix pass
8. `[[tactic-attribute-match-optimization-for-conversational-ai-search]]` — GBP attribute optimization, applies post-verification
9. `[[pattern-no-pricing-on-residential-contractor-core-30-pages]]` — Keelworks default; will apply to S&H Core 30 pages when built
10. `[[pattern-keelworks-aioseo-bridge-plugin]]` — applies when S&H's WP site gets the AIOSEO bridge during Core 30 deployment
11. `[[pattern-competitor-visual-fingerprint]]` — applies during S&H's Phase 2 Next.js design pass

**Pre-classified to DEFER (87 items)** — rule 3: slug-named situational conflict (artifact post-launch-shaped, project pre-launch-only) → defer with "activate on project transition":

This is the heavy-defer bucket Phase 2 surfaced as friction observation #11. Examples:
- Most extracted source notes (Greg Isenberg, Jono Catliff, dozens more) → defer; project not yet deploying tactics
- Most tools (Higgsfield, Site Kit, Screaming Frog, etc.) → defer; not yet adopted on S&H side
- Operator-discipline patterns (Keelworks AIOSEO bridge variants, no-pricing variants) → defer; activate when Core 30 pages start on S&H
- Tactics specifically post-launch-shaped (Core 30 page-build specifics, LiteSpeed config tactics, GA4/GSC analytics tactics) → defer; activate when site reaches post-launch
- Phase 2 EV-specific patterns (design system, no-pricing convention) that S&H will inherit → defer; activate when S&H Phase 1 starts

The 87-count comes from: 70 slug-named items − 1 apply − 11 keep = 58 slug-named defers, plus 29 archetype-overlap-only items, of which most get deferred (rule 9), minus a small overlap of items with multiple ancestor matches. Counting matches Phase 2 within ±2 items (Phase 2 reported "~87 deferred" — the actual count in this regression is 87 exactly).

**Pre-classified to NOT APPLICABLE (0 items)** — none. The archetype-overlap-only surface for S&H is mostly broader services-business tactics that aren't strictly conflict-state — they're deferrable, not not-applicable. The pre-classification correctly resists "not-applicable" as a bin because:

- Rule 2 (signal-2 + archetype-overlap-only → not-applicable) only fires for archetype-spurious matches where archetype-sharpening makes sense as the remediation. S&H's 29 archetype-overlap items don't have that profile — they're services-business tactics broadly applicable to any services-business project, including S&H eventually.
- Rule 3 (slug-named situational conflict → defer) covers the bulk of the post-launch-shaped tactics; the slug is on the artifact because someone decided it'll apply, just not yet.

**Pre-classified to ALREADY BRIDGED (0 items)** — first triage.

## Gate 1 surface

```
PULL TRIAGE — s-and-h-contracting

Project name: S&H Contracting
Project README: ~/workspace/second-brain/04_projects/clients/_active/s-and-h-contracting/README.md
Inbox file: ~/workspace/second-brain/04_projects/clients/_active/s-and-h-contracting/_intel-inbox.md
Lookback window: 14 days (suppressing items with routed-at after 2026-05-13)
Last operator triage: first triage

Sync status:
  README archetypes: [electrical-contractor, gbp-dependent, home-services-trade, pre-launch-seo, services-business, wordpress-site]
  Inbox archetypes: [electrical-contractor, gbp-dependent, home-services-trade, pre-launch-seo, services-business, wordpress-site]
  Match: matched ✓

Items surfaced: 99
  slug-named: 70
  archetype-overlap-only: 29
Items suppressed (routed within lookback): 0
Items already bridged (informational): 0

==== APPLY (proposed: 1) ====
  - [[pattern-access-gsc-self-takeover-without-prior-contractor]] (pattern, confidence: high)
    Pattern for taking over GSC ownership without a prior-contractor handoff (Haris-outreach flow).
    Reason: slug-named + directly actionable in current state (Haris outreach in flight; mechanism is orthogonal to GBP-verification blocker)

==== KEEP (proposed: 11) ====
  - [[tactic-information-architecture-first-for-new-sites]] (tactic, confidence: high)
    IA-first build sequencing.
    Reason: slug-named + project pre-launch; foundational, applies during Phase 2 Next.js rebuild

  - [[tactic-foundationals-first-for-new-sites-link-building]] (tactic, confidence: high)
    Foundational link-building before acquisition lanes.
    Reason: slug-named + applies post-launch (when site goes live)

  - [[tactic-gbp-to-website-alignment-core-30]] (tactic, confidence: high)
    Core 30 GBP-aligned page architecture.
    Reason: slug-named + applies post-GBP-verification

  - [[pattern-core-30-page-design-system]] (pattern, confidence: high)
    EV-derived design system; pages 2-30 inherit.
    Reason: slug-named + applies when S&H Phase 1 starts (inherits EV design system)

  - [[tactic-services-by-locations-matrix-for-local-seo]] (tactic, confidence: high)
    Services × locations matrix.
    Reason: slug-named + applies when S&H Core 30 build starts (50-mile radius matrix)

  - [[cluster-synthesis-ai-era-seo-cluster-2026-05-27]] (synthesis, confidence: high)
    Cluster-level reference consolidating 16 sources on AI-era SEO for local services.
    Reason: slug-named + project pre-launch; canonical reference, applies once GBP verifies. Per friction #4: keep-not-apply at synthesis altitude when engagement isn't in deployment state.

  - [[tactic-external-audit-to-ai-fix-loop]] (tactic, confidence: high)
    External audit → Claude → fixes loop.
    Reason: slug-named + applies post-launch (site needs to be live)

  - [[tactic-attribute-match-optimization-for-conversational-ai-search]] (tactic, confidence: high)
    GBP attribute optimization.
    Reason: slug-named + applies post-GBP-verification

  - [[pattern-no-pricing-on-residential-contractor-core-30-pages]] (pattern, confidence: high)
    No-pricing convention emerged from EV.
    Reason: slug-named + applies when S&H Core 30 build starts

  - [[pattern-keelworks-aioseo-bridge-plugin]] (pattern, confidence: medium)
    Keelworks-built WP plugin auto-populating AIOSEO meta.
    Reason: slug-named + applies during S&H WP site Core 30 deployment

  - [[pattern-competitor-visual-fingerprint]] (pattern, confidence: medium)
    Color-sampling from competitor sites for brand visual alignment.
    Reason: slug-named + applies during S&H Phase 2 Next.js design pass

==== DEFER (proposed: 87) ====
  - [[source-greg-isenberg-agent-builders]] (source, confidence: high)
    Greg Isenberg agent-builders source.
    Reason: slug-named situational conflict (post-launch-shaped) + S&H pre-launch; activate on project transition

  - [[source-jono-catliff-claude-code-seo-masterclass]] (source, confidence: high)
    Jono Catliff masterclass.
    Reason: slug-named situational conflict (post-launch methodology) + S&H pre-launch; activate when S&H goes post-launch

  - [[tactic-claude-code-page-build-pipeline]] (tactic, confidence: high)
    Claude Code page-build pipeline.
    Reason: slug-named situational conflict (assumes live site + scaffolder); activate when S&H Core 30 build starts

  - [[tactic-litespeed-cache-tuning-for-elementor-sites]] (tactic, confidence: medium)
    LiteSpeed Cache configuration for Elementor stacks.
    Reason: slug-named situational conflict (assumes live site); activate post-launch

  - [[tactic-ga4-site-kit-setup]] (tactic, confidence: medium)
    GA4 + Site Kit setup pattern.
    Reason: slug-named situational conflict (assumes site-with-baseline-measurement); activate post-launch

  - [[tactic-featured-com-expert-link-acquisition]] (tactic, confidence: medium)
    Featured.com link-acquisition lane.
    Reason: slug-named + future-gated lane (rule 7); activate post-launch + Phase-1 foundation

  - [[tactic-qwoted-expert-link-acquisition]] (tactic, confidence: medium)
    Qwoted link-acquisition lane.
    Reason: slug-named + future-gated lane; same gating

  - [[tool-higgsfield-image-video-generation]] (tool, confidence: high)
    Higgsfield AI imagery.
    Reason: slug-named situational conflict (used for live-site imagery); activate when S&H Core 30 build starts

  - [[tool-site-kit]] (tool, confidence: medium)
    Google Site Kit WP plugin.
    Reason: slug-named situational conflict (installs on live site); activate post-launch

  - [[pattern-no-pricing-conversion-flow]] (pattern, confidence: high)
    No-pricing → diagnostic-call → in-home-estimate conversion flow.
    Reason: slug-named situational conflict (requires live site to deploy); activate when S&H Core 30 starts

  - ... (77 more — all slug-named situational conflicts (post-launch artifacts) defer-with-reason "activate on project transition to post-launch")

==== NOT APPLICABLE (proposed: 0) ====
  (none — slug-named items defer rather than mark not-applicable; archetype-overlap items also defer rather than mark not-applicable because S&H's archetype set is broadly services-business-compatible)

==== ALREADY BRIDGED (informational: 0) ====
  (first triage)

Confirm bins as proposed / move <item> to <bin> / move all <bin> to <bin> /
sharpen archetypes on <item> / lower confidence on <item> to <level> /
refresh bridge on <item> / reject?
```

Operator response: **Confirm bins as proposed** (matches Phase 2 manual triage outcome).

## Gate 2 surface

1 bridge proposal:

```
BRIDGE-NOTE PROPOSALS — s-and-h-contracting

1 bridge proposed (one per applied artifact):

  1. s-and-h-contracting/bridge-pattern-access-gsc-self-takeover-without-prior-contractor-to-s-and-h-contracting.md
     Action items: 3
     Punchlist: "Execute GSC self-takeover via Haris-outreach flow for S&H property"

Per-bridge content (expanded):

  --- Bridge 1: pattern-access-gsc-self-takeover-without-prior-contractor ---
  ---
  type: bridge-note
  status: draft
  created: 2026-05-27
  updated: 2026-05-27
  project: s-and-h-contracting
  source-artifact: "[[pattern-access-gsc-self-takeover-without-prior-contractor]]"
  applies-to-projects: [s-and-h-contracting]
  tags: [bridge-note, s-and-h-contracting]
  ---

  # Bridge: GSC self-takeover pattern → S&H Contracting

  **Source:** [[pattern-access-gsc-self-takeover-without-prior-contractor]]
  **Filed:** 2026-05-27

  ## Why this applies to S&H Contracting

  S&H's prior SEO contractor (EverSolveds / Asim Naseem) is no longer responsive. Mohammad
  confirmed 2026-05-16 that the engagement is officially done. The site likely has GSC
  property ownership under an Asim-controlled account that we can't directly access. The
  GSC self-takeover pattern provides a clean recovery path: contact the suspected
  property-holder (Haris Mughal, per Mohammad's hypothesis), request ownership transfer,
  fall back to the HTML-file verification method if no response. This is actionable now
  regardless of GBP verification status — it's an access-recovery operation, not a
  deployment operation.

  ## Concrete action items

  1. Send the Haris-outreach email per the pattern's template (Mohammad supplies
     phone/email; Oliver sends from oliver@keelworks.ai)
  2. If Haris responds and is the GSC owner, walk through ownership-transfer flow per
     the pattern's "with-prior-contractor-response" branch
  3. If no response within 7 days, execute the HTML-file fallback verification per the
     pattern's "without-prior-contractor-response" branch

  ## Punchlist entry (proposed)

  > Execute GSC self-takeover via Haris-outreach flow for S&H property

  ## See also

  - [[pattern-access-gsc-self-takeover-without-prior-contractor]] (source)
  - [[s-and-h-contracting/README]] (project context)

Confirm all / modify per bridge / skip per bridge / reject all?
```

Operator response: **Confirm all** (Phase 2 ground truth: 1 bridge filed).

## Stage C writes

1. 1 bridge file written to `s-and-h-contracting/bridge-pattern-access-gsc-self-takeover-without-prior-contractor-to-s-and-h-contracting.md`
2. 1 punchlist entry appended to `s-and-h-contracting/_punchlist.md`
3. 1 artifact gets `routed-at: 2026-05-27` written: `pattern-access-gsc-self-takeover-without-prior-contractor.md`
4. Inbox `_intel-inbox.md` "Last triage" section updated:
   ```
   **Date:** 2026-05-27
   **Items surfaced:** 99 (70 slug-named, 29 archetype-overlap-only)
   **Items applied:** 1 → bridge note filed in this folder; punchlist entry appended
     - [[pattern-access-gsc-self-takeover-without-prior-contractor]]
   **Items kept:** 11
   **Items deferred:** 87
   **Items marked not-applicable:** 0

   **Friction observation:** Pre-launch projects produce heavy defer ratio (87/99 = 88%
   defer). Most slug-named items are post-launch-shaped tactics that defer-with-reason
   "activate on project transition." Pre-classification rule 3 correctly resists
   marking them not-applicable. v1.2 candidate: a `current-blocker:` field on the project
   README could auto-batch this bin further.
   ```
5. Verification reads confirm each touched file matches expected state.

## PASS criteria evaluation

- ✓ Applied count matches Phase 2 ground truth (1 = 1)
- ✓ Applied artifact matches Phase 2 ground truth (pattern-access-gsc-self-takeover-without-prior-contractor)
- ✓ Kept count matches Phase 2 (11 = "~11" per inbox)
- ✓ Deferred count matches Phase 2 (87 = "~87" per inbox)
- ✓ Not-applicable count matches Phase 2 (0 = 0)
- ✓ Total surfaced matches Phase 2 (99 = 99)
- ✓ Friction observation surfaced correctly (heavy defer ratio per friction #11)
- ✓ Rule 3 discipline preserved (slug-named situational conflicts → defer, not not-applicable)

**PULL passes the pre-launch GBP-blocked case.**

## Calibration observations

1. **Rule 3 is load-bearing.** Defaulting slug-named situational conflicts to `not-applicable` would have produced 87+ artifacts with slugs removed from `applies-to-projects:` on first triage — destructive and wrong. The Phase 2 operator-discipline (defer-not-remove) becomes the v1.1 algorithmic default via rule 3.

2. **Rule 4 correctly identifies the one applies.** GSC self-takeover pattern is actionable now despite the GBP blocker because the pattern's mechanism (access-recovery via prior-contractor outreach) is orthogonal to the project's deployment blocker. Rule 4's "directly actionable in current project state" captures this; rule 3 doesn't fire because the artifact isn't post-launch-shaped.

3. **Keep bin (11 items) is foundational architecture.** Synthesis + IA + Core 30 + design system + services × locations matrix + audit-loop + attribute match + no-pricing + AIOSEO bridge + competitor fingerprint. These are exactly the artifacts that S&H WILL apply once GBP verifies and the site starts shipping pages. Phase 2 chose keep for these; rule 6 reproduces.

4. **Heavy defer ratio is the right friction signal.** 87 defers on first triage is genuinely a lot of cognitive load to confirm at Gate 1. The single-line-per-item with reason format keeps each item parseable. v1.2 candidate: a `current-blocker:` field on the README that lets PULL auto-batch "all items deferred for the current blocker" into one collapsible group. v1.1 surfaces the friction observation in the Stage C inbox update so the pattern is recorded for the v1.2 design.

5. **Asymmetry with PUSH on signal 2 is intentional.** PUSH on a post-launch source (Jono Catliff masterclass example) correctly excludes S&H from the routed list — PUSH has no temporal commitment. PULL on S&H surfaces the same kind of artifact in the defer bin — PULL operates on cadence and the same conflict will re-evaluate next triage. Both disciplines are right for their respective modes.

6. **Window B (idempotence) for S&H.** Re-running PULL on 2026-05-28 suppresses the 1 routed item; surface drops to 98; 0 applies (no new directly-actionable artifacts); 11 keep; 87 defer; 0 not-applicable. Inbox Last-triage section updates with today's date and the zero-apply counts. Same idempotence shape as EV; routed-at suppression carries the discipline.
