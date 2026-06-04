---
type: reference
skill: gate-peer-reviewer
skill-version: 1.0
created: 2026-06-03
updated: 2026-06-03
tags: [reference, gate-type-registry, substrate-agnostic, future-orchestrator-friendly]
---

# Gate-type registry

The peer-reviewer reads this registry to know what to expect at any gate type — making the skill substrate-agnostic and future-orchestrator-friendly without hard-coding any single orchestrator's gates.

**v1 scope (deliberate).** v1 seeds the registry with vault-orchestrator Mode 6 EXECUTE's 5 gates as the canonical instance + documents the registration shape. Future orchestrators self-register at their build time. Cross-orchestrator generalization is **deferred by design (Build wave 4 per handoff), not by omission** — v1 ships the SHAPE and one full instance; expansion happens when v1 production calibration data surfaces additional gate shapes worth modeling.

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

## How future orchestrators register

When a new orchestrator skill is built (Phase 5 project-surveyor / project-analyst / project-decider; mission-control-dashboard backend operations; Hermes-daemon spawned waves; any future client- or project-specific orchestrator), the orchestrator's build chat appends entries to this registry covering each of its gate types.

Registration entries land at chat close + are validated by the peer-reviewer's next invocation. Invalid entries (missing required fields, contradicting an existing entry without acknowledgment) trigger a Check 4 cross-wave coherence catch on the registration itself.

## Build wave 4 — cross-orchestrator generalization

Per the build handoff, Build wave 4 expands this registry to cover client-seo-onboarding skill's gates + any other orchestrator's gates surfaced by v1 production calibration data. v1 ships only Mode 6's 5 gates because:

1. Mode 6 is the only orchestrator emitting gate decisions in vault production today.
2. Gate shapes for future orchestrators aren't yet stable enough to model — modeling them now would carry forward incorrect assumptions.
3. v1's job is to ship the registration SHAPE + one full canonical instance. The shape is reusable; the canonical instance demonstrates the shape's coverage.

Cross-orchestrator generalization is **deferred by design, not by omission.** Build wave 4 fires once 2-3 production runs of v1 surface enough data to model additional gate shapes accurately.
