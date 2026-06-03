---
type: example
skill: gate-peer-reviewer
skill-version: 1.0
created: 2026-06-03
updated: 2026-06-03
gate-reviewed: vault-orchestrator Mode 6 EXECUTE Gate 2 PROVISION (S&H wave A4)
verdict: REJECT-AND-REDO
tags: [example, worked-example, peer-review, manassas-electric-department, check-3-domain-plausibility]
---

# Worked example — v1 peer-reviewer applied to S&H wave A4 Gate 2 PROVISION (Manassas Electric Department catch)

This is the v1 unit test. The peer-reviewer running on the actual wave A4 Gate 2 emission must independently reproduce the operator's parallel-Cowork catch (Manassas Electric Department, not Dominion Energy). If it doesn't, the v1 spec goes back for tightening before ship.

## Gate input context

| Field | Value |
|---|---|
| Orchestrator | vault-orchestrator v1.2 |
| Mode | Mode 6 EXECUTE |
| Gate | Gate 2 PROVISION |
| Wave | wave-A4 |
| Project slug | s-and-h-contracting |
| Chat-id (original) | `s-and-h-wave-a4-mode-6-execute-202606031930` |
| Wave coverage | Manassas + Lorton + Springfield (per pass-98 changelog) |

**What Gate 2 PROVISION emitted (excerpted to the Manassas utility block):**

> ## City of Manassas — Public utility coverage
>
> | Utility | Provider | Service area | Notes |
> |---|---|---|---|
> | Water | City of Manassas Utilities | Manassas city limits | Operated by Public Works Dept |
> | Sewer | City of Manassas Utilities | Manassas city limits | Same dept as water |
> | Electric | Dominion Energy Virginia | Northern Virginia | Standard NoVA coverage |
> | Gas | Columbia Gas of Virginia | Manassas + PWC | Standard residential coverage |

**Kickoff prompt requirement (excerpted):** "PROVISION shall correctly identify the operating electric utility for each city brief, including municipal-electric anomalies where they exist."

## Peer-reviewer execution trace

### Check 1 — Contract satisfaction

Parse kickoff requirements:

- "Correctly identify operating electric utility for each city brief" — partial match: utility named, but correctness deferred to Check 3.
- "Including municipal-electric anomalies where they exist" — flag for Check 3. Provisional PASS pending Check 3.
- Other kickoff requirements (water/sewer/gas coverage, service area) — satisfied.

Not a Gate 4 dispatch emission → skip Gate-4 structural compliance sub-check.

Verdict slot: provisional PASS pending Check 3.

### Check 2 — Calibration consistency

Gate 2 PROVISION doesn't emit cost/wall-clock predictions; calibration check N/A for this gate type per `references/gate-type-registry.md`. PASS.

### Check 3 — Domain plausibility

Triage filter:

- "City of Manassas Utilities" for water/sewer — load-bearing + jurisdiction-specific. Skipped: water/sewer aren't the anomaly class the kickoff calls out, and operator memory holds municipal water/sewer as common.
- "Dominion Energy Virginia" for electric — load-bearing + jurisdiction-specific. **Fire Sonar.**
- "Columbia Gas of Virginia" for gas — load-bearing + jurisdiction-specific. Skipped at v1 — gas anomalies are rare in this region. Flag for v1.1 expansion if a wave later surfaces a gas-anomaly miss.

Sonar query with English-anchoring suffix per `lesson-hermes-prework-b-org-transparency-2026-06-03.md` D-row + `lesson-city-base-research-anomaly-check-v1.1-build-2026-06-03.md` D-01:

> "Which Virginia cities operate municipal electric utilities, in 2026 English-language sources?"

Sonar returns (paraphrased from real `sonar-pro` response):

> 16 government-owned electric systems per MEPAV (Municipal Electric Power Association of Virginia) including Manassas, Front Royal, Bedford (post-2013 status pending verification), Danville, Harrisonburg, Martinsville, Salem, Radford, plus 7 towns and Virginia Tech VTES and BVU Authority. Manassas Electric Department serves City of Manassas.

Cost receipt: $0.028, single query, `sonar-pro`.

Cross-reference: `~/workspace/skills/city-base-research/references/jurisdiction-anomaly-known-list.md` confirms Manassas is on the 16-entity MEPAV roster (Class 1 = municipal electric utility; verified at v1.1 ship 2026-06-03).

**Mismatch detected.** Gate 2 emitted "Dominion Energy Virginia" for City of Manassas electric. Truth: Manassas Electric Department (municipal). Load-bearing for service-coverage correctness.

Verdict update: REJECT-AND-REDO.

### Check 4 — Cross-gate + cross-wave coherence

**Sub-check 4a (within-wave):** Gate 1 RESUME for wave A4 framed the wave with "carry-forward of utility-co-op service-area framing from wave A3" (Dale City had used NOVEC/Dominion split logic). A4's Manassas defaulted to Dominion without applying the inherited framing. **Within-wave incoherence:** A4 Gate 2 didn't apply the utility-co-op service-area framing it inherited from A3.

**Sub-check 4b (cross-wave structural):** Wave A3 final city briefs (Woodbridge, Lake Ridge, Dale City) all surfaced municipal-utility-vs-investor-owned-utility framing in their water-sewer-electric table. A4's Manassas table uses the same shape — structurally coherent. But A3 didn't have a municipal-electric city in its set, so the Manassas anomaly didn't have a prior-wave precedent to copy. Sub-check 4b returns no cross-wave drift.

Within-wave catch from 4a stands. Verdict remains REJECT-AND-REDO with reinforced rationale: Gate 1 RESUME framing was inherited but not applied.

### Check 5 — Carry-forward management

Translate catches to actionable artifacts.

**Operator-reply text (paste-ready):**

> Gate 2 PROVISION for City of Manassas misidentifies the operating electric utility. Sonar verification (single query, $0.028, English-anchored): "Manassas Electric Department serves City of Manassas; municipal-owned." Gate 2 currently lists "Dominion Energy Virginia." Per Manassas Electric Department + MEPAV roster + city-base-research v1.1 jurisdiction-anomaly reference file, Manassas is one of 16 Virginia government-owned electric systems (Class 1 — municipal electric utility).
>
> Within-wave coherence note: Gate 1 RESUME for wave A4 inherited utility-co-op service-area framing from wave A3 but Gate 2 emitted without applying it. Suggests the carry-forward step lost the framing between gates.
>
> Two corrections needed:
> 1. Update the City of Manassas utility table: electric provider → "Manassas Electric Department (municipal)" with service-area "Manassas city limits" and notes "City-operated municipal electric; one of 16 government-owned VA electric systems per MEPAV. Class 1 anomaly (municipal electric) + Class 2 anomaly (independent city) — full anomaly profile per city-base-research v1.1 jurisdiction-anomaly-known-list.md."
> 2. Forward-looking note for future Mode 6 waves touching Manassas Park (wave A4 covered Manassas + Lorton + Springfield, not Manassas Park): Manassas Park is Class 2 only (independent city; NOT on the 16-entity MEPAV muni-electric roster), so Dominion Energy + NOVEC are the correct electric providers there. Despite adjacency to Manassas, the two cities have different anomaly profiles — Manassas Park did not adopt municipal electric. This counter-intuitive sibling case is documented in jurisdiction-anomaly-known-list.md.

**D-row candidate:**

```yaml
lesson_file_target: 05_shared-intelligence/lessons/lesson-s-and-h-wave-a4-mode-6-third-production-fire-2026-06-03.md
row_id: D-N (next sequential; suggest D-04 if not taken)
what_happened: |
  Wave A4 Gate 2 PROVISION for City of Manassas defaulted electric utility to Dominion Energy Virginia.
  Manassas operates a municipal electric utility (Manassas Electric Department), one of 16 Virginia
  government-owned electric systems per MEPAV (Class 1 anomaly per city-base-research v1.1).
  Peer-reviewer's Check 3 Sonar probe surfaced the mismatch at $0.028 cost.
signal_for_skill: |
  vault-orchestrator Mode 6 Gate 2 PROVISION needs a jurisdiction-anomaly check upstream of dispatch —
  the city-base-research v1.1 reference file at jurisdiction-anomaly-known-list.md already encodes the
  16-entity MEPAV roster, but Mode 6's Gate 2 dispatch doesn't reference it. Same catch will fire on
  every PROVISION for a Virginia municipality until the reference file is wired in.
action: |
  Wave A5 + future Mode 6 EXECUTE waves: kickoff prompts must include "Run jurisdiction-anomaly check
  per city-base-research SKILL.md § Jurisdiction anomaly check before drafting utility tables."
  Alternative: vault-orchestrator Mode 6 directly invokes city-base-research § Jurisdiction anomaly
  check as a pre-Gate-2 sub-skill call.
```

**Kickoff-prompt patch:**

```yaml
next_wave_target: wave-A5 (already shipped; apply retrospectively as D-row in A5 lesson) + all future Mode 6 EXECUTE waves
patch_location: Kickoff prompt for any future Mode 6 EXECUTE wave touching Virginia municipalities
patch_text: |
  Pre-Gate-2 PROVISION discipline: before drafting any city utility table, invoke city-base-research
  SKILL.md § Jurisdiction anomaly check (5-15 min Sonar probe with English-anchoring suffix per the
  90-day skip-clause; cross-reference jurisdiction-anomaly-known-list.md). Encode any Class-1 or
  Class-2 anomaly in a > [!warning] callout in §1 of the brief and a sub-paragraph in §6. Free
  verification step prevents Dominion-by-default failure mode.
rationale: |
  The same catch will fire on every Mode 6 PROVISION for VA municipalities (Vienna, Falls Church,
  Fredericksburg, etc.) until the jurisdiction-anomaly check is wired into the kickoff template.
```

**Pattern promotion signals:**

```yaml
pattern_candidate_name: vault-orchestrator-pre-gate-2-anomaly-check
instance_count_after_this_run: 1
promote_now: false
pattern_file_target: null
promotion_trigger: 2nd-instance trigger checked at every future Mode 6 PROVISION emission touching a VA muni-electric city — promotion fires automatically when next instance lands.
```

### Check 6 — KCA verification

Skip. Gate 2 PROVISION is not a closing gate.

## Full structured JSON return (verbatim)

```json
{
  "schema_version": "1.0",
  "gate_reviewed": {
    "orchestrator": "vault-orchestrator",
    "mode": "Mode 6 EXECUTE",
    "gate_id": "Gate 2 PROVISION",
    "wave_id": "wave-A4",
    "chat_id": "s-and-h-wave-a4-mode-6-execute-202606031930",
    "project_slug": "s-and-h-contracting"
  },
  "verdict": "REJECT-AND-REDO",
  "verdict_rationale": "City of Manassas electric utility misidentified as Dominion Energy Virginia. Truth: Manassas Electric Department (municipal). Manassas is one of 16 VA government-owned electric systems per MEPAV (Class 1 anomaly). Sonar-verified at $0.028. Within-wave coherence note: Gate 1 RESUME inherited utility-co-op framing from wave A3 that Gate 2 didn't apply.",
  "checks_skipped": [
    {"check": "check_6", "reason": "not a closing gate"}
  ],
  "catches": [
    {
      "catch_id": "C-1",
      "severity": "blocking",
      "check_source": "check_3",
      "summary": "Manassas electric utility misidentified as Dominion; actual is Manassas Electric Department (municipal)",
      "rationale": "Sonar probe with English-anchoring suffix returned MEPAV 16-entity roster including Manassas as government-owned electric. Cross-referenced jurisdiction-anomaly-known-list.md (city-base-research v1.1, 2026-06-03). Load-bearing for service-area correctness.",
      "cited_source": "Sonar receipt $0.028 single query + skills/city-base-research/references/jurisdiction-anomaly-known-list.md",
      "deliberate_evolution_check": "n/a"
    },
    {
      "catch_id": "C-2",
      "severity": "follow-up",
      "check_source": "check_4",
      "summary": "Within-wave incoherence: Gate 1 RESUME framing not applied at Gate 2",
      "rationale": "Wave A4 Gate 1 RESUME inherited utility-co-op service-area framing from wave A3 close-out (NOVEC-vs-Dominion in Dale City). Gate 2 emitted City of Manassas without applying the inherited framing. Suggests carry-forward step is dropping framing between gates.",
      "cited_source": "wave-A4 Gate 1 RESUME output + wave-A3 close-out lesson D-rows",
      "deliberate_evolution_check": "unacknowledged"
    }
  ],
  "operator_reply_text": "<the full paste-ready text from Check 5 above>",
  "d_row_candidates": [
    "<the D-row from Check 5 above with the corrected lesson_file_target>"
  ],
  "kickoff_prompt_patches": [
    "<the kickoff patch from Check 5 above>"
  ],
  "pattern_promotion_signals": [
    {
      "pattern_candidate_name": "vault-orchestrator-pre-gate-2-anomaly-check",
      "instance_count_after_this_run": 1,
      "promote_now": false,
      "pattern_file_target": null,
      "promotion_trigger": "2nd-instance trigger checked at every future Mode 6 PROVISION emission touching a VA muni-electric city — promotion fires automatically when next instance lands."
    }
  ],
  "cost_usd": 0.028,
  "sonar_queries_run": 1,
  "sonar_query_receipts": [
    {
      "query": "Which Virginia cities operate municipal electric utilities, in 2026 English-language sources?",
      "model": "sonar-pro",
      "cost_usd": 0.028,
      "anchoring_suffix_used": true
    }
  ],
  "wall_clock_seconds": 47
}
```

## Reproduction validation

The operator's real wave A4 parallel-Cowork catch surfaced:
- "Manassas is one of ~16 Virginia municipal-electric cities and Dominion is wrong"
- Recommendation: update utility table to name Manassas Electric Department + flag the anomaly class

The v1 peer-reviewer running on this gate independently surfaces:

- ✅ Same load-bearing catch (Manassas Electric Department, not Dominion)
- ✅ Same anomaly class framing (16-entity MEPAV roster + Class 1)
- ✅ Plus: within-wave coherence catch the operator's parallel chat noted but didn't formally surface (Gate 1 RESUME framing not applied)
- ✅ Plus: forward-looking kickoff patch + pattern candidate

**v1 spec passes this unit test.** The peer-reviewer reproduces the real operator catch and adds two artifacts the operator didn't formally produce (kickoff patch + pattern candidate).

## Self-applying-spec demonstrations (caught during build)

Two Check-3-class errors were caught at Gate 4 spot-check during this build chat — by the exact review pass the peer-reviewer is spec'd to automate. Both fixed before ship; documented here as demonstration that the spec is self-applying.

**Demonstration 1 — Class 1/Class 2 label inversion.** The original draft of this worked example inverted the Class 1 and Class 2 anomaly labels: called Manassas Park "Class 1 only on the 7-town list" — wrong on two counts (Manassas Park is Class 2 only, not Class 1; the 7-town list is part of Class 1 muni-electric coverage, separate from the 38 independent cities). Operator caught the inversion via Check 3 domain plausibility + cross-reference to `jurisdiction-anomaly-known-list.md`. v1 peer-reviewer running on this worked example would have surfaced the same catch: Check 3 fires Sonar/disk-verify on the Class 1/2 label assignment + flags REJECT-AND-REDO.

**Demonstration 2 — Dangling lesson file path.** Original D-row candidate cited `lesson-s-and-h-wave-a4-mode-6-execute-2026-06-03.md`. Glob-verified: actual file is `lesson-s-and-h-wave-a4-mode-6-third-production-fire-2026-06-03.md`. Operator caught at Gate 4 spot-check. v1 peer-reviewer running its own Check 6 Layer B (completeness probe → dangling references sub-category) would surface the same catch: dangling reference path in newly-written content.

Shipping a dangling lesson path + label inversion INTO the example for the skill spec'd to catch dangling references + Class-3-domain errors would have been a double self-application failure. Caught at Gate 4 spot-check during this build.

## Additional unit-test claims (compact appendix)

Full JSON returns deferred to Build wave 2 production calibration. One-line expected verdicts:

| # | Gate | Expected v1 verdict | Expected catch | Check pathway exercised |
|---|---|---|---|---|
| 2 | Wave A4 Gate 4 dispatch prompts (original draft, pre-restoration) | REJECT-AND-REDO | 4 operational sections stripped (state-writes + four-substep quality loop + structured JSON return contract + operator gate routing); no D-row acknowledging deliberate evolution | Check 1 Gate-4-specific structural compliance sub-check |
| 3 | Wave A5 Gate 4 dispatch prompts | REJECT-AND-REDO | four-substep quality loop reverted to inline self-eval despite kickoff explicitly requiring four-substep; same drift pattern as A4 → kickoff-prompt patch must propose recurrence guard | Check 1 + Check 4 sub-check 4b + Check 5 carry-forward patch |
| 4 | Wave A5 Gate 3 close-condition #10 | REJECT-AND-REDO | Orchestrator referenced stale 6-item audit instead of current 8-item audit per `feedback_knowledge_capture_audit_before_closing` memory | Check 1 contract satisfaction (memory item count) |
| 5 | Wave A5 Gate 2 PROVISION (Stafford + Alexandria) | REJECT-AND-REDO | NOVEC/Dominion split in Stafford missed; AlexRenew rebrand from Alexandria Renew Enterprises not picked up | Check 3 Sonar probe (jurisdiction-specific + brand-currency) |
| 6 | Wave A4 Gate 5 wave-close + KCA | APPROVE-WITH-NOTES (or REJECT-AND-REDO if execution log entirely missing) | Self-reported 6/6 PASS; disk verification surfaces: execution log missing, pattern file `times-observed: 1` when truth was 6, 4 missing supplemental D-rows, pattern extraction candidate not extracted, dangling `confidence-calibration.md` reference | Check 6 Layer A + Layer B + Layer C |

Build wave 2 (v1 production calibration) consumes these as full unit tests against the actual emissions.
