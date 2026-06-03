---
name: gate-peer-reviewer
version: 1.0
status: active
created: 2026-06-03
updated: 2026-06-03
description: Automated peer-review layer that sits between any orchestrator skill's gate emission and operator review. Fires 6 structured checks (contract satisfaction / calibration consistency / domain plausibility / cross-gate + cross-wave coherence / carry-forward management / Knowledge Capture Audit verification). Substrate-agnostic. Project-agnostic. Output-agnostic. Composes with vault-orchestrator Mode 6 (peer-reviewer dispatch slot per gate) + output-quality-loop (disjoint scope — process-level vs artifact-level). Returns structured JSON verdict + paste-ready operator-reply + D-row candidates + kickoff-prompt patches.
triggers:
  - any orchestrator emits a gate decision for operator review
  - vault-orchestrator Mode 6 EXECUTE Gates 1-5
  - any closing gate emitting a Knowledge Capture Audit self-report
  - any future orchestrator that registers a gate type in references/gate-type-registry.md
composes-with:
  - vault-orchestrator (Mode 6 EXECUTE dispatch slot per gate; v1.3+ integration block)
  - output-quality-loop (artifact-level downstream; disjoint scope)
  - any future orchestrator registering gate types
tags: [skill, peer-review, gate-review, process-quality, orchestrator-coaching, substrate-agnostic, v1, deliberate-evolution-vs-silent-drift]
---

# `gate-peer-reviewer` skill v1

Automated peer-review layer that fires on every orchestrated output across every project across every skill. Replaces the parallel-Cowork coaching layer Oliver ran by hand through waves A2-A6 of S&H Core 30 research.

## Purpose

When an orchestrator emits a gate output, the peer-reviewer reads the gate output + a defined set of context sources, then runs 6 structured checks before the operator sees the emission. Two outputs land in the operator's view: the gate output + the peer-reviewer's verdict. Operator approves with one action.

The compounding-intelligence value: every catch the peer-reviewer surfaces becomes a D-row candidate for the relevant lesson file + a pattern-extraction candidate if the catch recurs across waves/projects. Over time, the peer-reviewer's review history IS the vault's quality-control corpus.

**Scope. Project-agnostic. Output-agnostic. Step-agnostic.**

- Works on any orchestrator's gate emissions (vault-orchestrator Mode 6 today; future orchestrators registered in `references/gate-type-registry.md`)
- Works on any artifact type (research briefs / page builds / handoffs / lessons / patterns / skill SKILL.md files / state files / event log rows / dispatch prompts / wave-close audits / anything emitted through operator-attended gates)
- Works on any project (S&H Contracting / EV Electric Services / Keelworks / Hermes-harness / mission-control-dashboard / Keelworks-AI-OS-SaaS / every future client and every future project)
- Works at any step within a multi-step workflow (gate emissions + intermediate produce-evaluate-elevate-decide steps + sub-skill compositions + cross-skill handoffs)

## The 6 checks (summary)

Full verbatim spec at `references/check-spec.md`. Summary:

1. **Contract satisfaction** — does the gate output satisfy the kickoff prompt's explicit requirements? For Mode 6 EXECUTE Gate 4 emissions specifically: Gate-4 structural compliance sub-check (5 required template blocks per dispatch prompt).
2. **Calibration consistency** — do the gate's predictions (cost, wall-clock, sub-agent count) match the trend of recent actuals from the state file's `wave_log[]` + recent lesson D-rows?
3. **Domain plausibility** — does the substantive content pass smell-tests for the domain? Optional bounded Sonar probe (1 query max per gate, $0.025-$0.04) for jurisdiction-specific or time-specific claims.
4. **Cross-gate coherence + cross-wave structural coherence** — (4a) within-wave: does this gate fit with the prior gate? (4b) cross-wave: does this wave's structural pattern match the prior wave's revised-final structural pattern? Applies deliberate-evolution vs silent-drift disambiguation.
5. **Carry-forward management** — translate every catch from Checks 1-4 into (a) paste-ready operator-reply text + (b) D-row candidate + (c) kickoff-prompt patch when applicable.
6. **Knowledge Capture Audit verification (closing-gate-only)** — when the closing gate emits a self-reported "Knowledge Capture Audit PASSED N/N," peer-reviewer independently runs 3 layers: Layer A disk-verifies items 1-6 (lesson D-rows + execution log + event log + state file + tool bugs + patterns); Layer B is item 7 completeness probe (6 sub-categories); Layer C is item 8 reusability probe (6 reuse contracts). Self-audits have structural blind spots; external review doesn't.

**Skip logic.**

| Condition | Skip |
|---|---|
| Check 1 returns `REJECT-AND-REDO` | Skip Check 3 (Sonar cost); STILL run Check 4 (free, surfaces additional structural drift); jump to Check 5 + Check 6 if closing gate |
| Gate is not a closing gate (Gates 1-4 in Mode 6) | Skip Check 6 entirely |
| Gate is not a Mode 6 EXECUTE Gate 4 emission | Skip Gate-4-specific structural compliance sub-check inside Check 1 |
| No domain-specific claims surface in Check 3 triage | Skip Sonar fire; Check 3 returns PASS without cost |
| First wave of an orchestrator run (no prior wave to compare) | Skip Sub-check 4b |

## Substrate detection (3-probe sequence)

The peer-reviewer runs under three substrates without spec changes:

| Substrate | How peer-reviewer fires | Status |
|-----------|------------------------|--------|
| Claude Code Task tool | Parent orchestrator spawns peer-reviewer as a Task tool sub-agent after each gate emission | Feasible today |
| Cowork sequential | Parent orchestrator invokes peer-reviewer as a sub-skill (single-process), output to chat | Feasible today |
| Hermes-harness daemon (Build wave 3 / Level 3 target) | Daemon watches event log; on every gate event, fires peer-reviewer; posts response back to parent substrate's stdin | Requires Hermes Prework A + B + C |

**Why 3-probe over 2-probe.** A 2-probe sequence (parent-orchestrator-provided substrate tag → fallback) is simpler. The peer-reviewer uses 3-probe because under Hermes daemon dispatch (Build wave 3), the parent-orchestrator-provided substrate tag is NOT reliably available — the daemon fires from outside the orchestrator's process, so the tag-passing channel may not exist. Daemon robustness is the load-bearing reason; sibling-consistency with vault-orchestrator Mode 6's 3-probe sequence is the bonus.

**The 3-probe sequence:**

```
Probe 1 — Read env var GATE_PEER_REVIEWER_SUBSTRATE (set by parent dispatcher when known)
Probe 2 — Read parent-context introspection (Task tool exposes hasTaskParent; Cowork sub-skill invocation exposes parentSkill)
Probe 3 — Fallback to interactive prompt OR daemon-mode signal file at /tmp/hermes-substrate-tag
```

Default: if all 3 probes fail, assume `cowork-sequential` and log warning to event log.

## Inputs read at every invocation

Per gate review:

1. **Current gate output text** — the thing being reviewed
2. **Current wave's kickoff prompt** — the contract
3. **`feedback_*` memory files** under `~/Library/Application Support/Claude/local-agent-mode-sessions/.../memory/` — what the operator has validated as good or corrected as wrong
4. **State file** — `04_projects/<area>/<name>/_state/onboarding.json` (or equivalent for non-S&H/EV orchestrators)
5. **Recent lesson D-rows** — most recent 1-2 lesson files for this orchestrator + project
6. **Active chats tracker** — `_meta/handoffs/_active-chats-tracker.md`, what other orchestrators are in flight that might collide
7. **Gate-type registry** — `references/gate-type-registry.md`, what to expect at this gate type
8. **Orchestrator skill's SKILL.md + references/** — to verify the gate output follows the skill's own contract
9. **(Optional, conditional) Perplexity Sonar** — bounded to 1 query max per gate (Check 3)
10. **(For Gate 4 specifically) Prior wave's revised-final dispatch prompts + the reusable skeleton at `vault-orchestrator/references/sub-agent-dispatch-contract.md` once [3A] ships**

## Return contract — structured JSON

Full field-by-field spec at `references/return-contract.md`. Top-level shape:

```json
{
  "schema_version": "1.0",
  "gate_reviewed": {
    "orchestrator": "<vault-orchestrator | client-seo-onboarding | ...>",
    "mode": "<Mode 6 EXECUTE | Mode 5 RESUME | ...>",
    "gate_id": "<Gate 2 PROVISION | Gate 4 dispatch | Gate 5 wave-close | ...>",
    "wave_id": "<wave-A4 | wave-A5 | null>",
    "chat_id": "<chat-id of the parent orchestrator>",
    "project_slug": "<s-and-h-contracting | ev-electric-services | ...>"
  },
  "verdict": "<APPROVE | APPROVE-WITH-NOTES | REJECT-AND-REDO | ESCALATE-AMBIGUOUS>",
  "verdict_rationale": "<one-paragraph summary; load-bearing for operator scan>",
  "checks_skipped": [
    {"check": "check_3", "reason": "no domain-specific claims to probe"},
    {"check": "check_6", "reason": "not a closing gate"}
  ],
  "catches": [...],
  "operator_reply_text": "<paste-ready, self-contained>",
  "d_row_candidates": [...],
  "kickoff_prompt_patches": [...],
  "pattern_promotion_signals": [...],
  "cost_usd": 0.0,
  "sonar_queries_run": 0,
  "sonar_query_receipts": [...],
  "wall_clock_seconds": 0
}
```

(`checks_run` is implicit: `{check_1, check_2, ..., check_6} \ {checks_skipped[].check}`.)

**Write-authority.** The peer-reviewer does NOT write pattern files, lesson D-rows, kickoff prompts, or any other vault artifact directly. It SURFACES proposed changes in `catches[]`, `d_row_candidates[]`, `kickoff_prompt_patches[]`, `pattern_promotion_signals[]` + names them in `operator_reply_text`. The originating chat (or operator) does the actual `times-observed` increment + decision-archaeology append + D-row write + kickoff edit. Peer-reviewer is a review layer, not a write layer.

## Composition with `output-quality-loop`

| Skill | Reviews | When fires | Scope |
|-------|---------|-----------|-------|
| `output-quality-loop` Modes 1-5 | Produced artifacts | After artifact production | Artifact-level: does this brief / page / data file meet spec? |
| `gate-peer-reviewer` (this skill) | Orchestrator gate decisions | After gate emission, before operator review | Process-level: does this dispatch plan / kickoff prompt / wave-close protocol make sense before any artifacts get produced? |

Disjoint scopes. Peer-reviewer catches process drift upstream; output-quality-loop catches artifact drift downstream. Together they remove most of the operator's spot-check burden while keeping the operator authoritative on genuinely ambiguous catches.

## Integration with vault-orchestrator (v1.3)

Vault-orchestrator v1.3 adds a peer-reviewer dispatch slot at Mode 6 EXECUTE Step 6/7 single review gate. Concrete shape: ONE additive block (~30 lines) inserted after the existing operator-confirmation discussion at Mode 6 Step 7. No Mode 6 rewrites.

**Cross-mode integration map (v1 honest read of vault-orchestrator v1.2 architecture).** The 6 conceptual gates the peer-reviewer's `references/gate-type-registry.md` names map across vault-orchestrator modes as follows:

| Conceptual gate | Actual orchestrator gate | Integration status |
|---|---|---|
| Gate 1 RESUME | Mode 5 RESUME Step 11 confirmation | **v1.1 (deferred)** — separate mode integration |
| Gate 2 PROVISION | Mode 3 PROVISION Step 8 single review gate | **v1.1 (deferred)** — separate mode integration |
| Gates 3 + 4 (combined: dispatch plan + dispatch prompts) | Mode 6 EXECUTE Step 6/7 single review gate | **v1.0 (SHIPS HERE)** — single Mode 6 hook |
| Gate 5 wave-close | Mode 6 EXECUTE Step 10 wave-close | **v1.1 (deferred)** — auto-closes in v1.2; integration when operator-attended wave-close lands |
| Step 9 conditional sub-agent gates | Routed via `operator-gate-routing` | **v1.1 (deferred)** — separate routing channel |

**Why v1.0 ships with just the Mode 6 Step 6/7 hook.** That's the single existing operator-attended gate where the catches from waves A2-A6 (Manassas MED utility, PWC carry-forward contradiction, A4/A5 dispatch prompt drift, A5 Gate 3 stale audit-count reference) all fired. Production calibration data from v1.0 production runs drives when to wire in the additional hooks at v1.1.

**Self-applying-spec demonstration.** The build chat for v1 caught this scope mismatch at Gate 5 disk-verify: the build handoff specified "5 additive blocks per gate" but vault-orchestrator v1.2 disk-verified to ONE explicit Mode 6 operator-attended gate (Step 6/7), not 5. The "5 gates" framing was forward-looking. Caught by the exact Check 4 cross-document coherence discipline the peer-reviewer is spec'd to automate. Documented as D-row in `lesson-gate-peer-reviewer-v1-build-2026-06-03.md`.

See `vault-orchestrator/SKILL.md` § Step 7 "Peer-reviewer dispatch (v1.3)" for the integration block.

## Gate-type registry (substrate-agnostic + future-orchestrator-friendly)

The peer-reviewer reads `references/gate-type-registry.md` to know what to expect at any gate type. v1 seeds the registry with vault-orchestrator Mode 6's 5 gates as the canonical instance. Future orchestrators (Phase 5 project-surveyor / project-analyst / project-decider sub-skills, mission-control-dashboard backend operations, Hermes-daemon spawned waves) self-register at their build time by appending entries to the registry.

**Cross-orchestrator generalization is deferred by design, not by omission.** Build wave 4 (per handoff) expands the registry to cover client-seo-onboarding skill's gates + any other orchestrator's gates surfaced by v1 production calibration data. v1 ships the registration SHAPE + Mode 6 as the seed instance.

## Graceful degradation

Substrates may not have peer-reviewer wired in at first deploy (e.g., Hermes Level 3 daemon dispatch before Prework A+B+C close). When the orchestrator's dispatch attempt fails because the peer-reviewer skill is unavailable, the orchestrator MUST log a row to `_meta/_event-log.md` in this format:

```
event-type: peer-reviewer-skipped
reason: skill not available on <substrate>
chat-id: <id>
gate-id: <id>
orchestrator: <name>
```

Five parseable fields. Grep-friendly: future operators run `grep "event-type: peer-reviewer-skipped" _meta/_event-log.md` to find every skip occurrence. Skipping is acceptable as long as it's tracked; silently dropping the review step is not.

## Cost surface

Per-gate incremental cost when peer-reviewer fires:

| Layer | Per-gate cost | Per-wave cost (5 gates) | Notes |
|-------|---------------|------------------------|-------|
| Opus invocation (peer-reviewer reasoning) | $0.05-$0.12 | $0.25-$0.60 | Default; reads ~5-10K tokens of context, produces structured JSON |
| Sonar query (optional Check 3 domain probe) | $0.025-$0.04 | $0.025-$0.08 | Bounded to 1 query per gate max; typically 1-2 of 5 gates need it |
| Total per-wave incremental | — | $0.28-$0.68 | Edge case all-5-gates-Sonar: $0.125-$0.20 additional, bounded by triage filter |

Justified: the catches Oliver was making in parallel Cowork would otherwise cost (a) Mode 4 iterations on failed briefs ($0.05-$0.15 per re-iteration) or (b) operator time at Gate 2 spot-check. Peer-reviewer absorbs both.

## Operator invocation modes

The peer-reviewer is normally dispatched by a parent orchestrator. Operator-driven invocation:

**Mode A — Manual review of an existing gate emission.** Operator pastes gate output + kickoff prompt + context paths; peer-reviewer returns JSON.

**Mode B — Retroactive review of a past wave.** Operator names wave ID + project; peer-reviewer reads state file + gate emissions from chat-history references + returns per-gate JSONs.

**Mode C — Dispatched via parent orchestrator (canonical).** Parent orchestrator follows the integration block in its own SKILL.md.

## Reference files (index)

- `references/check-spec.md` — Full verbatim 6-check spec with worked-example anchors. **Load-bearing.**
- `references/gate-type-registry.md` — Substrate-agnostic registry of gate types + registration shape. Mode 6 as the seed instance.
- `references/return-contract.md` — Full field-by-field JSON return contract + write-authority detail.

## Worked examples

- `examples/first-review-2026-06-03-s-and-h-wave-a4-gate-2-provision.md` — v1 peer-reviewer applied to the Manassas Electric Department catch. Reproduces operator's parallel-Cowork catch + adds within-wave coherence finding + kickoff-prompt patch + pattern candidate. Includes self-applying-spec demonstration (Check-3-class errors caught at Gate 4 spot-check during build).

## Version history

- **v1.0 (2026-06-03)** — Initial ship. 6-check spec + 3-probe substrate detection + structured JSON return contract + write-authority constraint + vault-orchestrator Mode 6 integration (v1.3 bump in vault-orchestrator) + Mode 6 as seed gate-type registry instance + graceful degradation event log format. Build wave 1 — Cowork sequential substrate, operator-attended through 5 gates. Build wave 2 (production calibration) and Build wave 4 (cross-orchestrator generalization) deferred by design. See `lesson-gate-peer-reviewer-v1-build-2026-06-03.md` for build-time D-rows.
