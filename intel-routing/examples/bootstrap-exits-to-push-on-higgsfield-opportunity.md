# Worked example: BOOTSTRAP exits to PUSH on the Higgsfield opportunity

Test run 2026-05-28. Tests BOOTSTRAP against an opportunity that has strong overlap with an existing project (Keelworks). Validates the Stage A1 apply-to-existing detection and the clean exit path: BOOTSTRAP recommends apply-to-existing, operator confirms, no scaffolding occurs, and a paste-ready PUSH invocation is emitted instead.

## Test framing

The source artifact is `00_inbox/decisions-pending/opportunity-higgsfield-predict-virality-as-cro-deliverable-tier.md` — a medium-confidence (tier 2) pricing-tier-differentiation mechanism for Keelworks. Hypothesis: "If Keelworks adopts Higgsfield as agency-substrate-pipeline tool for client AI before/after video deliverables, the Higgsfield Predict Virality scoring feature becomes a pricing-tier-differentiation mechanism enabling Keelworks to offer a premium-tier service ladder."

The body explicitly names Keelworks throughout. The opportunity is structurally a Keelworks-internal CRO-pricing-tier mechanism, not a new productization that warrants its own project. This is exactly the case BOOTSTRAP's apply-to-existing exit path is designed for.

## Inputs

**Source artifact:** `~/workspace/second-brain/00_inbox/decisions-pending/opportunity-higgsfield-predict-virality-as-cro-deliverable-tier.md`
**Today (as-if):** 2026-05-28

### Source frontmatter (read at Step 2)

- `type: opportunity`
- `status: surfaced`
- `opportunity-type: pricing-tier-differentiation-mechanism`
- `confidence: medium-low`
- `tier: 2`
- `applies-to-projects:` — not set
- `applies-to-archetypes:` — not set (pre-Phase-2 shape)

### Source body summary (executor read)

Opportunity to make Higgsfield Predict Virality scoring the differentiating mechanism for a premium Keelworks CRO video deliverable tier (above baseline AI before/after video delivery). Body explicitly names Keelworks, names dad-businesses as first test cases, references Jono Catliff service-business pattern. Structurally a Keelworks-internal R&D / productization mechanism, not a new project.

### Existing project READMEs enumerated

Same 11 projects as the onboarding-agent test. Most relevant for this opportunity:

- **keelworks (services-business + professional-services):** body explicitly names "Keelworks" 6+ times; describes a CRO-pricing-tier mechanism for Keelworks engagements; cites three Keelworks-internal strategic-decisions documents. **Strong body alignment.**
- **dad-businesses (services-business + professional-services):** body names dad-businesses as test cases for the basic-tier delivery, but the productization shape is Keelworks-internal. **Partial body alignment** (dad-businesses is consumer of basic-tier, not owner of productization).

### Vault reconnaissance for pre-population

Skip pre-population estimate at this stage — apply-to-existing detection runs first; if it surfaces strong overlap, BOOTSTRAP exits before computing pre-population.

## Stage A — Apply-to-existing detection (Step 3a)

Computing overlap against each project:

- **keelworks:** archetype overlap with inferred source archetypes = 2 (services-business, professional-services) — but archetype-count alone underrates this case. Body alignment is dominant: source body names Keelworks explicitly 6+ times, describes pricing-tier mechanism for Keelworks engagements, cites Keelworks-internal `_strategic-decisions/` documents (visual-social-proof-capture, three-track-migration-playbooks). The signal-strength is "this opportunity IS a Keelworks-internal R&D item, not a separate project." **Strong overlap.**
- **dad-businesses:** archetype overlap = 2 (services-business, professional-services). Body alignment partial — dad-businesses gets named as basic-tier test consumer, but the opportunity is structurally Keelworks-owned. **Partial overlap.**
- **All other projects:** 0 or weak archetype overlap.

**Strong overlap:** keelworks.
**Partial overlap:** dad-businesses.
**No overlap:** 9 others.

**Recommendation:** APPLY-TO-EXISTING for keelworks. Default per spec open question #6: when any project has strong overlap, recommend apply-to-existing. Operator can override with "promote anyway" if they have a reason.

## Stage A — Scaffold parameters proposal (Step 3b)

Even though recommendation is apply-to-existing, executor prepares the promote-path proposal in case operator overrides. (Most operators reading this would skip-read this section in the actual Gate 1 surface and go straight to confirming apply-to-existing.)

**Slug:** `higgsfield-predict-virality-cro-tier` (derived from source filename, `opportunity-` prefix stripped, `as-cro-deliverable-tier` shortened to `cro-tier` for filename brevity).

**Slug uniqueness:** unique.

**Area:** `personal/`. (Productization mechanism Oliver builds; not a client engagement.)

**Archetypes:** `[services-business, professional-services, productized-service, ai-tooling]`. Same shape as the onboarding-agent opportunity — both are productized service offerings.

**Conventions check:** `services-business` + `professional-services` + `ai-tooling` live; `productized-service` is `(future)` (or already promoted if the onboarding-agent example ran first this session).

**Confidence:** `medium`.

**Founding-artifact:** `[[opportunity-higgsfield-predict-virality-as-cro-deliverable-tier]]`.

**Repo scaffold:** `yes-repo` per default rules.

**Purpose statement (drafted):** "Productize a CRO-pricing-tier mechanism for Keelworks client AI video deliverables, using Higgsfield Predict Virality scoring as the differentiating feature. Basic tier: AI before/after video delivery; premium tier: scoring + iteration cycles + scoring-history-as-deliverable."

## Gate 1 surface

```
BOOTSTRAP SCAFFOLD PROPOSAL — opportunity-higgsfield-predict-virality-as-cro-deliverable-tier

Source artifact: ~/workspace/second-brain/00_inbox/decisions-pending/opportunity-higgsfield-predict-virality-as-cro-deliverable-tier.md
Type: opportunity
Tier: 2
Body summary (1-2 sentences):
  Higgsfield Predict Virality scoring as differentiating mechanism for a premium Keelworks
  CRO video deliverable tier (above baseline AI before/after video delivery). Body explicitly
  names Keelworks 6+ times; cites Keelworks-internal _strategic-decisions/ documents.

Existing source frontmatter:
  applies-to-projects: not set
  applies-to-archetypes: not set
  applicability-confidence: not set
  routed-at: not set

Apply-to-existing detection:
  Strong overlap with: keelworks
    keelworks: 2 archetype overlap (services-business, professional-services) +
      DOMINANT body alignment — source body names Keelworks 6+ times, describes pricing-tier
      mechanism for Keelworks engagements, cites three Keelworks-internal strategic-decisions
      documents (visual-social-proof-capture, three-track-migration-playbooks,
      visual-social-proof-capture-as-service-delivery-model). The signal-strength reads as
      "this is a Keelworks-internal R&D item," not "this is a separate productization."
  Partial overlap with: dad-businesses
    dad-businesses: 2 archetype overlap (services-business, professional-services); body
      names dad-businesses as basic-tier test consumer but opportunity is structurally
      Keelworks-owned
  No overlap with: 9 other projects

Recommendation: APPLY-TO-EXISTING for keelworks
Reason: Source body explicitly names Keelworks as the owning project for the productization
  mechanism. Promoting a separate project would orphan the opportunity from its operational
  context (Keelworks's CRO-deliverable pricing) and require manual coordination between the
  new project and Keelworks anyway. The cleaner path is PUSH-route to keelworks, which
  writes a bridge note in the keelworks/ folder + updates source frontmatter — preserving
  Keelworks as the operational owner.

==== PROMOTE-TO-PROJECT proposal (shown for override only) ====

Slug:       higgsfield-predict-virality-cro-tier
  Uniqueness: unique
Area:       personal/
Archetypes: [services-business, professional-services, productized-service, ai-tooling]
  Conventions check: productized-service is (future) or recently-promoted
Confidence: medium
Founding-artifact: [[opportunity-higgsfield-predict-virality-as-cro-deliverable-tier]]
Repo scaffold: yes-repo

Purpose (proposed):
  Productize a CRO-pricing-tier mechanism for Keelworks client AI video deliverables,
  using Higgsfield Predict Virality scoring as the differentiating feature.

Friction observations:
  - Productizing a Keelworks-internal pricing tier as a separate project would split
    operational ownership between two folders. Strongly suggest apply-to-existing instead.
  - productized-service archetype is currently (future) in conventions.md; would need inline
    promotion if promote-anyway path chosen.

==== APPLY-TO-EXISTING (recommended) ====

Target project: keelworks
Overlap rationale: Strong — source body names Keelworks explicitly as owner of the
  productization; cites three Keelworks-internal strategic-decisions documents; opportunity
  is structurally Keelworks-internal R&D.
Suggested invocation (paste into a fresh chat or this one):
  "PUSH-route 00_inbox/decisions-pending/opportunity-higgsfield-predict-virality-as-cro-deliverable-tier.md to keelworks"

PUSH will:
  - Write a bridge note at 04_projects/personal/keelworks/bridge-opportunity-higgsfield-predict-virality-as-cro-deliverable-tier-to-keelworks.md
  - Append to keelworks/_punchlist.md
  - Update source frontmatter: applies-to-projects: [keelworks], routed-at: 2026-05-28,
    applies-to-archetypes: <derived from keelworks archetypes>, applicability-confidence: high
  - Source artifact stays in 00_inbox/decisions-pending/ (no physical relocation)

No BOOTSTRAP writes will occur if you confirm apply-to-existing.

Confirm promote / confirm apply-to-existing for keelworks / modify <field> / promote anyway / reject?
```

**Operator response:** *Confirm apply-to-existing for keelworks*.

## BOOTSTRAP exit

```
BOOTSTRAP EXITED — apply-to-existing path chosen.

Source: 00_inbox/decisions-pending/opportunity-higgsfield-predict-virality-as-cro-deliverable-tier.md
Target project: keelworks

To proceed, invoke PUSH:
  "PUSH-route 00_inbox/decisions-pending/opportunity-higgsfield-predict-virality-as-cro-deliverable-tier.md to keelworks"

The source artifact stays in 00_inbox/decisions-pending/ and gets routed via PUSH.
PUSH will write a bridge note to 04_projects/personal/keelworks/, append to keelworks
punchlist, and update source frontmatter (applies-to-projects, applies-to-archetypes,
applicability-confidence, routed-at).

No BOOTSTRAP writes occurred. Source frontmatter is unchanged.
```

**No further BOOTSTRAP execution.** Operator runs PUSH separately when ready.

## PASS criteria evaluation

- ✓ Apply-to-existing detection correctly identified keelworks as strong-overlap target
- ✓ Body alignment correctly weighted over archetype-count alone (archetypes match keelworks AND dad-businesses with the same count; body alignment is what distinguishes the two)
- ✓ Default recommendation was APPLY-TO-EXISTING per spec open question #6
- ✓ Promote-path proposal was prepared and surfaced for operator-readability, with friction observation flagging that promote-anyway would split operational ownership
- ✓ PUSH invocation hint emitted in paste-ready form
- ✓ No scaffolding writes occurred (cleanly exited)
- ✓ Source artifact frontmatter untouched (PUSH owns the routing-time updates)
- ✓ No half-states: zero files created, zero edits made

**BOOTSTRAP passes the apply-to-existing exit path.**

## Calibration observations

1. **Body alignment is the load-bearing signal for strong-overlap detection.** Archetype overlap alone (which would have flagged dad-businesses equally) doesn't capture the "this opportunity IS owned by project X" signal. The body-naming heuristic (project named in source body 5+ times + cites project-internal documents) is the right tiebreaker. Worth noting: friction observation candidate if the body-naming heuristic produces false positives in future cases.

2. **Apply-to-existing exit is operationally clean.** No BOOTSTRAP writes. Operator runs one separate skill invocation (PUSH) which handles routing-time updates. This composability is the design intent — BOOTSTRAP and PUSH cover adjacent decision spaces (new vs existing) and hand off cleanly between them.

3. **Promote-path proposal shown for transparency even when not recommended.** Operator can override; suppressing the promote-path proposal would burden the operator with re-asking for it if they want to consider it. The "shown for override only" header makes the recommendation hierarchy clear.

4. **Friction observation flagged the trade-off of overriding.** "Promoting a Keelworks-internal pricing tier as a separate project would split operational ownership" — this is the kind of skill-surfaced observation that helps the operator make the call. Without it, operator might override to promote-path without thinking through the consequence.

5. **No source-artifact update is intentional.** BOOTSTRAP exits → source frontmatter untouched. PUSH (when operator invokes it) does the frontmatter updates. This preserves separation of concerns and keeps BOOTSTRAP from accidentally side-effecting on what's essentially a no-op invocation.

6. **dad-businesses partial-overlap was correctly NOT recommended as the apply-to-existing target.** dad-businesses appears in the source body but as a consumer of the basic-tier offering, not as owner. BOOTSTRAP's apply-to-existing detection correctly distinguished consumer from owner. Worth capturing this distinction in the prompt's apply-to-existing heuristic for future maintenance: "named project should be the owner/operator of the opportunity, not the beneficiary."
