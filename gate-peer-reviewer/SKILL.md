---
name: gate-peer-reviewer
version: 3.8
status: active
created: 2026-06-03
updated: 2026-06-16
description: Automated peer-review layer that sits between any orchestrator skill's gate emission and operator review. Fires 6 structured checks + severity tiers + standing regression harness. 21 registered gate types across 13 orchestrators — incl. G-default universal catch-all gate (v3.4) for ad-hoc/non-orchestrated tasks + G-chat-close omission-audit gate (v3.6) for chat-completeness verification at every close. All 9 non-Core-30 skills dispatch the reviewer at their gates (GPR-9). Reviewer performs its own live cache-busted fetch (GPR-11). All sweeps enumerate meta/og/schema surfaces (GPR-12). Verdicts carry blocking/advisory severity (GPR-13). Planted-defect regression suite prevents silent regression (GPR-14). Substrate-agnostic. Project-agnostic. Output-agnostic.
triggers:
  - any orchestrator emits a gate decision for operator review
  - vault-orchestrator Mode 6 EXECUTE Gates 1-5
  - client-seo-onboarding page-build gates G-data / G-scaffold / G-imagery / G-publish / G-wave-close (v2.0)
  - research-brief gates G-service-brief / G-intersection-brief / G-city-brief / G-client-brief / G-competitor-brief (v3.0)
  - knowledge-artifact gates G-extraction / G-routing / G-decompose / G-synthesis (v3.0)
  - any closing gate emitting a Knowledge Capture Audit self-report
  - any future orchestrator that registers a gate type in references/gate-type-registry.md
  - mandatory pre-land review gate Stop hook — when invoked without a registered gate_id, use G-default (v3.4)
  - G-chat-close omission-audit gate — Closing Protocol step 0 (manual) or RGH-5 independent dispatch (auto) (v3.6)
composes-with:
  - vault-orchestrator (Mode 6 EXECUTE dispatch slot per gate; v1.3+ integration block)
  - client-seo-onboarding (page-build gates; v1.4+ integration block; autonomous dispatch via Task sub-agent)
  - service-seo-research, intersection-research, city-base-research, client-fact-research, competitor-deep-research (research-brief gates; v3.0 registered, v3.2 dispatching)
  - vis-extraction, intel-routing, multi-chat-coordination, multi-source-synthesis (knowledge-artifact gates; v3.0 registered, v3.2 dispatching)
  - output-quality-loop (artifact-level downstream; disjoint scope)
  - any future orchestrator registering gate types
tags: [skill, peer-review, gate-review, process-quality, orchestrator-coaching, substrate-agnostic, v2, page-build, autonomous-dispatch, deliberate-evolution-vs-silent-drift]
---

# `gate-peer-reviewer` skill v3.8

Automated peer-review layer that fires on every orchestrated output across every project across every skill. v1 replaced the parallel-Cowork coaching layer Oliver ran by hand through waves A2-A6 of S&H Core 30 research. v2 extends to page-build gates (replacing the manual peer-review transport from the S&H Core 30 page-build run, PR-01..PR-40) and adds autonomous dispatch so the operator stops being the paste-transport layer.

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

## Live-verification discipline (folded in from T2-7, Issue #28; updated GPR-11 v3.2)

Four rules for any peer-reviewer pass that touches live page state (publish gates, backfill gates, any gate where the reviewer assesses whether a page is "done" or "clean"). Source: `[[lesson-core-30-publishing-verification-template-parity-2026-06-04]]` Issues #26/#27/#28; GPR-11 precipitating event (D-12 caught twice by operator, not reviewer).

1. **The REVIEWER performs its own independent live fetch (GPR-11).** The reviewer fetches the live URL itself with a cache-buster (`?v=<timestamp>`), parses the HTML, and runs all checks against the PARSED output. It does NOT rely on the orchestrator's self-reported fetch, the operator's confirmation, or any upstream agent's claim about page state. The reviewer is the primary catch layer; operator confirmation is an optional spot-check. Full procedure: `references/gate-type-registry.md` § `live-rendered-cache-busted-verification` Phase A.

2. **Verify live-rendered + cache-busted, never grep-only.** Compare the RENDERED structure against a named known-good sibling page — H1 form, title visibility, font-family (serif = fail), image fill, map fill, zero placeholder text. A grep of `post_content` HTML for class names ("`evp-corepage` present", "serif title: 0") is NOT acceptance — it cannot detect serif fallback, a duplicate theme title, or old-vs-new content structure. Class presence ≠ rendered styling.

3. **A fetch-vs-operator-screenshot conflict is a cache question first.** When the reviewer's fetch returns different content than an operator's screenshot, treat the discrepancy as a **page-cache staleness issue**, not a "the other agent lied" conclusion. Never override direct operator visual evidence (a screenshot of the logged-in render) with the reviewer's tool fetch. The correct sequence: cache-bust the fetch (`?v=ts`), compare, and if still conflicting, recommend cache purge + incognito re-check. A stale cached snapshot at the canonical URL is itself a real finding — anonymous visitors + search engine crawlers may see the old page.

4. **Don't scope a page as "fine, minor fix" from a prior run note — disk-verify its actual state first.** Before scoping a page as "images render acceptably — only needs the map" (or any similar assessment from a prior note), disk-verify the page's current wired-image + style-wrapper state. The reviewer mis-scoped page 01 as "fine" from an old run note while on disk its hero was never wired and its live content was the old version. Same class as `pattern-disk-verify-integration-target-before-drafting` applied to the reviewer's own scoping.

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

**Verdict-file emission (RGH-1, v3.5).** When the peer-reviewer runs under the mandatory pre-land review gate, it MUST emit its structured return contract to a verdict file that `log-review-pass.py` can consume. The verdict file maps the full return contract to the gate script's expected schema:

```json
{
  "verdict": "PASS|BLOCKING|FAIL",
  "checks_run": [
    {"name": "placeholder-sweep", "result": "PASS", "count": 0},
    {"name": "leak-audit", "result": "PASS", "count": 0},
    {"name": "link-resolution", "result": "PASS", "count": 0},
    {"name": "ground-truth-cross-check", "result": "PASS", "count": 0}
  ],
  "catches": [],
  "cost_usd": 0.0
}
```

**Verdict mapping:** `APPROVE` / `APPROVE-WITH-NOTES` → `PASS`. `REJECT-AND-REDO` / `ESCALATE-AMBIGUOUS` → `BLOCKING`. Any unrecoverable error → `FAIL`.

**checks_run mapping:** each of the 6 checks that was NOT skipped becomes an entry. Use the named procedure name where applicable (`placeholder-sweep`, `leak-audit`, `link-resolution`, `ground-truth-cross-check`, `value-cross-check`, `live-verification`). Full-tier reviews MUST include `ground-truth-cross-check` or `value-cross-check`.

**File location:** write to `.review-gate/state/verdict-<gate_id>-<timestamp>.json`. Then pass the path to `log-review-pass.py --verdict-file <path>`.

**Write-authority.** The peer-reviewer does NOT write pattern files, lesson D-rows, kickoff prompts, or any other vault artifact directly. It SURFACES proposed changes in `catches[]`, `d_row_candidates[]`, `kickoff_prompt_patches[]`, `pattern_promotion_signals[]` + names them in `operator_reply_text`. The originating chat (or operator) does the actual `times-observed` increment + decision-archaeology append + D-row write + kickoff edit. Peer-reviewer is a review layer, not a write layer. The ONE file the reviewer writes directly is the verdict file (above) — this is enforcement infrastructure, not a vault artifact.

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
| Gate 2 PROVISION | Mode 3 PROVISION Step 9 single review gate | **v1.1 (deferred)** — separate mode integration |
| Gates 3 + 4 (combined: dispatch plan + dispatch prompts) | Mode 6 EXECUTE Step 6/7 single review gate | **v1.0 (SHIPS HERE)** — single Mode 6 hook |
| Gate 5 wave-close | Mode 6 EXECUTE Step 10 wave-close | **v1.1 (deferred)** — auto-closes in v1.2; integration when operator-attended wave-close lands |
| Step 9 conditional sub-agent gates | Routed via `operator-gate-routing` | **v1.1 (deferred)** — separate routing channel |

**Why v1.0 ships with just the Mode 6 Step 6/7 hook.** That's the single existing operator-attended gate where the catches from waves A2-A6 (Manassas MED utility, PWC carry-forward contradiction, A4/A5 dispatch prompt drift, A5 Gate 3 stale audit-count reference) all fired. Production calibration data from v1.0 production runs drives when to wire in the additional hooks at v1.1.

**Self-applying-spec demonstration.** The build chat for v1 caught this scope mismatch at Gate 5 disk-verify: the build handoff specified "5 additive blocks per gate" but vault-orchestrator v1.2 disk-verified to ONE explicit Mode 6 operator-attended gate (Step 6/7), not 5. The "5 gates" framing was forward-looking. Caught by the exact Check 4 cross-document coherence discipline the peer-reviewer is spec'd to automate. Documented as D-row in `lesson-gate-peer-reviewer-v1-build-2026-06-03.md`.

See `vault-orchestrator/SKILL.md` § Step 7 "Peer-reviewer dispatch (v1.3)" for the integration block.

## Integration with client-seo-onboarding (v1.4) — autonomous dispatch

Client-seo-onboarding v1.4 adds a peer-reviewer dispatch block after each artifact-producing step's quality-loop exit. **Autonomous dispatch** — the orchestrator spawns the peer-reviewer as a Claude Code Task sub-agent after each gate, inlines the verdict, and surfaces the combined result (gate output + peer-review verdict) to the operator as a single approve/notes surface. The operator no longer pastes gate outputs between two chats. This is the legitimate home of the convenience mode: per-page Core-30 builds are the high-volume, low-stakes tail described in the Independence precedence section — the sub-agent's weaker independence is an accepted trade for not hand-pasting dozens of page gates. For the wave-close gate (G-wave-close), which can register or change shared state, prefer a separate-session running review per the precedence rule.

**5 page-build gates registered in `references/gate-type-registry.md`:**

| Gate | Fires after | Named procedures run at Check 1 |
|---|---|---|
| G-data | Step 3 quality-loop exit | source-client-leak-audit + full-placeholder-family-sweep |
| G-scaffold | Step 5 quality-loop exit | source-client-leak-audit + full-placeholder-family-sweep |
| G-imagery | Step 6 quality-loop exit | source-client-leak-audit + full-placeholder-family-sweep |
| G-publish | Step 8 substep 3 (wire) | live-rendered-cache-busted-verification + full-placeholder-family-sweep + source-client-leak-audit |
| G-wave-close | Closing Protocol | KCA Check 6 (same as vault-orchestrator) |

**Composition with output-quality-loop.** Disjoint scope maintained: output-quality-loop (Modes 1-5) evaluates artifact quality (does this page meet the content spec?); peer-reviewer evaluates process integrity (does this gate output carry source-client leaks, residual placeholders, or structural drift?). Quality loop fires FIRST (per the orchestrator's four-substep contract); peer-reviewer fires AFTER quality-loop exit, BEFORE operator gate.

**Calibration corpus.** The S&H Core 30 page-build peer-review run (2026-06-04/05) produced the calibration data for all 5 gate types. Catches PR-01/07/15/16/17/19a/19b are the acceptance test — the peer-reviewer must independently reproduce all 7 from Check 1 satisfaction targets without operator prompting.

See `client-seo-onboarding/SKILL.md` § "Peer-reviewer dispatch (v1.4)" for the integration block.

## Independence precedence (v3.8) — separate-session running review is canonical

There are two dispatch shapes for the reviewer, and they are **not** equally independent. This section establishes which to use when. It governs every dispatch block in this skill and in every downstream skill that references it.

**1. Separate-session, step-by-step running review (canonical — strongest independence).** The reviewer runs in its own session (a fresh Cowork window or a separate Claude Code session) with its own context and its own disk reads. The operator relays each producer output as it is produced; the reviewer disk-verifies it and hands back paste-ready text before the producer proceeds. This is the canonical form, defined in `~/workspace/second-brain/05_shared-intelligence/patterns/pattern-independent-peer-review-chat.md` and automated by the `references/independent-reviewer-mandate.md` (Phase R). **It is MANDATORY for skill registrations, vault state changes, client deliverables, and any live/external-state change.**

**2. In-session Task sub-agent autonomous dispatch (weaker independence — convenience mode).** The orchestrator spawns the reviewer as a Task sub-agent inside the producer's own session (the v2.0 path below). This removes the operator-as-transport, but the sub-agent shares the producer's process and context — so its independence is structurally weaker (the mandate's own "Honest limits" §6 says as much: the strongest form of independence is a separate process). It is acceptable ONLY for **high-volume, low-stakes gates** — e.g. per-page Core-30 page builds (G-data / G-scaffold / G-imagery / G-publish) where the operator has opted into autonomy to avoid pasting dozens of gate outputs by hand. It is **never** a substitute for a separate-session running review on state-changing, skill-registration, or high-stakes work, and a sub-agent verdict must never be labelled as full independent review.

**Precedence rule.** When a gate qualifies as state-changing / skill-registration / high-stakes, the separate-session running review wins even if an autonomous-dispatch path exists for that gate. Autonomous dispatch is an optimization for the low-stakes high-volume tail, not the default for everything.

## Autonomous dispatch (v2.0) — convenience mode, see Independence precedence above

v1 required the operator to manually paste each gate output into a peer-review chat and paste the reply back. v2 removes the operator-as-transport **for the low-stakes high-volume tail** (per the Independence precedence section above — this is the weaker-independence convenience mode, not the default for state-changing or skill-registration work):

**Under Claude Code (current substrate):** the orchestrator spawns the peer-reviewer as a Task sub-agent after each gate emission. The Task receives: (1) the gate output text, (2) the gate type from the registry, (3) paths to the context sources (state file, lesson files, kickoff prompt). The Task returns the structured JSON verdict. The orchestrator inlines the verdict alongside the gate output in the operator's view.

**Under Cowork sequential:** the orchestrator invokes the peer-reviewer as a sub-skill (single-process). Output renders in the same chat.

**Under Hermes-harness daemon (Build wave 3 / Level 3 target):** daemon watches event log; on every gate event, fires the peer-reviewer; posts response back to the parent substrate's stdin. Requires Hermes Prework A + B + C.

The 3-probe substrate detection sequence (unchanged from v1) determines which dispatch path to use. Default: if all 3 probes fail, assume `cowork-sequential` and log warning.

**Write-authority constraint (unchanged).** The peer-reviewer surfaces proposed changes; the orchestrator (or operator) does the actual writes. Autonomous dispatch does not change who writes — it changes who transports.

**Pre-gate dispatch checklist (v2.1).** Before surfacing ANY gate output to the operator, the orchestrator must confirm:

1. Look up the current gate_id in `references/gate-type-registry.md`.
2. If the gate_id is registered → the peer-reviewer MUST have been dispatched. A miss is a skip, not a judgment call.
3. If peer-reviewer dispatch was not attempted → dispatch NOW, before surfacing the gate to the operator.
4. If dispatch was attempted and failed (skill unavailable on substrate) → log the `peer-reviewer-skipped` event per the graceful-degradation format below, then surface the gate to the operator with the skip noted.

This checklist exists because the orchestrator skipped peer-reviewer dispatch at G-imagery during the Alexandria run (D-03) — it handed the operator a manual checklist instead of spawning the peer-reviewer Task sub-agent. The v1.4 dispatch table (above) lists G-imagery as a registered gate; skipping it silently is a defect, not a design decision. Every registered gate gets peer-reviewed. No exceptions.

## Gate-type registry (substrate-agnostic + future-orchestrator-friendly)

The peer-reviewer reads `references/gate-type-registry.md` to know what to expect at any gate type. v1 seeds the registry with vault-orchestrator Mode 6's 5 gates as the canonical instance. Future orchestrators (Phase 5 project-surveyor / project-analyst / project-decider sub-skills, mission-control-dashboard backend operations, Hermes-daemon spawned waves) self-register at their build time by appending entries to the registry.

**Cross-orchestrator generalization shipped at Build wave 4 (v2.0, 2026-06-05).** The registry now covers vault-orchestrator Mode 6's 5 research-brief gates (v1 seed) + client-seo-onboarding's 5 page-build gates (v2 expansion) + 3 reusable named verification procedures. Future orchestrators self-register at their build time using the same shape.

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
- `references/gate-type-registry.md` — Substrate-agnostic registry of gate types + registration shape + 4 named verification procedures (full-placeholder-family-sweep, source-client-leak-audit, live-rendered-cache-busted-verification, ground-truth-value-cross-check). 21 gate types across 13 orchestrators.
- `references/omission-check-registry.md` — G-chat-close omission-audit gate: 16 checks (OC-1..OC-16), 6 per-chat-type profiles, severity mapping, per-check verification procedures, honest limits. The omission half of the review stack (v3.6).
- `references/regression-harness.md` — Standing planted-defect regression suite. 25 fixtures (7 v3.2 seed + 2 v3.6 G-chat-close + 16 v3.7 COA-4b corpus), run at every version bump. Prevents silent regression of known-caught defect classes.
- `references/regression-fixtures/` — Synthetic test fixtures with planted defects + expected outcomes. 25 fixtures: 7 v3.2 seed + 2 v3.6 G-chat-close + 16 v3.7 COA-4b corpus.
- `references/return-contract.md` — Full field-by-field JSON return contract + write-authority detail.
- `references/facts-registry-spec.md` — Ground-truth value-correctness layer: generic facts profile shape, cross-check algorithm, boundary (output-matches-source, not source-matches-reality), non-SEO proof architecture.
- `references/facts-profiles/` — Registered facts profiles (declarative YAML). `core-30-page-build.yaml` + `research-brief.yaml`.

## Worked examples

- `examples/first-review-2026-06-03-s-and-h-wave-a4-gate-2-provision.md` — v1 peer-reviewer applied to the Manassas Electric Department catch. Reproduces operator's parallel-Cowork catch + adds within-wave coherence finding + kickoff-prompt patch + pattern candidate. Includes self-applying-spec demonstration (Check-3-class errors caught at Gate 4 spot-check during build).

## Version history

- **v3.8 (2026-06-16)** — Independence precedence (operator-directed). New "Independence precedence" section establishes the separate-session, step-by-step running review as the canonical and MANDATORY form for skill registrations / vault state changes / client deliverables / live-state changes, and demotes in-session Task sub-agent autonomous dispatch to a weaker-independence convenience mode for the high-volume low-stakes tail only (e.g. per-page Core-30 builds). The v2.0 "Autonomous dispatch" section and the client-seo-onboarding v1.4 integration note are re-scoped accordingly (no machinery removed — subordinated). Pairs with `independent-reviewer-mandate.md` v1.1 (Phase R: per-paste-back running verification as default) and the updated `pattern-independent-peer-review-chat.md` (running review = default, close-out-only = narrow exception). No engine/check changes; gate + orchestrator counts unchanged.
- **v3.7 (2026-06-16)** — COA-4b regression-fixture corpus + OC-12↔dod-check reconnect (RGH-FIN). 16 committed regression fixtures (12 runnable + 4 design-verified) under `regression-fixtures/coa4b-*/` — synthetic defect/clean state pairs for the 15 deterministic COA-4b catches (C-02..C-24). Suite: 32/32 expectations met, 0 false positives. `.wf-tmp` good-states snapshotted as committed evidence (5.1 MB manifests + structural JSONs). OC-12 reconnected to `dod-check.py` (stale "fall back to OC-9" note removed — RGH-7 shipped). `source_type` parser gap closed: markdown DoD tables auto-dispatch mechanizable assertions; non-mechanizable deferred to independent reviewer (documented in `spec-definition-of-done-manifest.md`). OC-16 git-integration conformance test handed to [RGH-2] (deliverable #6). Fixture count 9→25. Harness version synced. Composes with [RGH-5] (consumes the committed corpus for its replay acceptance test).
- **v3.6 (2026-06-15)** — G-chat-close omission-audit gate (RGH-6). New gate type `G-chat-close` registered in `references/gate-type-registry.md` — the omission half of the review stack. Every existing gate inspects artifacts that exist (commission); G-chat-close diffs expected-artifact-and-follow-through set against disk reality (omission). 16 checks (OC-1..OC-16) in an append-only registry, 6 per-chat-type profiles (planning/decision, build, research/extraction, production-fire, skill-build, micro), severity mapping, per-check ls/grep verification procedures — all $0/no-LLM, <5 min wall-clock. Wired as Closing Protocol step 0 in `_active-chats-tracker.md` (manual dispatch until RGH-5 auto-dispatches). OC-12..16 cite [RGH-7]'s deterministic Layer-A procedures (per-deliverable existence, count-reconciliation, rename-propagation, frontmatter-freshness, commit-staging-audit). Mapping-validated on WF-1 corpus (OC-1/2/3/4 map to the 4 known gaps) + COA-4b corpus (OC-12..16 map to 22/25 deterministic catches); true regression replay requires preserved pre-fix fixtures (RGH-5/RGH-7 scope). Gate count 20→21 (orchestrator count stays 13 — G-chat-close shares the gate-peer-reviewer orchestrator namespace). New reference file: `references/omission-check-registry.md`. Composes with RGH-5 (independent dispatch) + RGH-7 (DoD manifest + Layer-A scripts). Honest limits: known-gap-classes only (compounding rule), OC-4 Cowork-only, self-dispatch until RGH-5.
- **v3.5 (2026-06-11)** — Verdict-file emission (RGH-1). When running under the mandatory pre-land review gate, the peer-reviewer now emits its structured return contract to a verdict file (`.review-gate/state/verdict-<gate_id>-<timestamp>.json`) that `log-review-pass.py` consumes. Verdict mapping: APPROVE/APPROVE-WITH-NOTES→PASS, REJECT-AND-REDO/ESCALATE-AMBIGUOUS→BLOCKING. checks_run mapped to named procedures (placeholder-sweep, leak-audit, ground-truth-cross-check, etc.). Full-tier requires ground-truth-cross-check or value-cross-check. Write-authority updated: verdict file is the ONE file the reviewer writes directly (enforcement infrastructure, not a vault artifact). Composes with the hardened mandatory-review-gate scripts (verdict-file-backed markers, tier enforcement, scoped aggregation).
- **v3.4 (2026-06-08)** — G-default universal catch-all gate. New gate type `G-default` registered in `references/gate-type-registry.md` for ad-hoc/non-orchestrated tasks. When the mandatory pre-land review gate (Stop hook) fires and no registered orchestrator gate applies, G-default provides the gate contract: full-placeholder-family-sweep + source-client-leak-audit + body-level link-resolution + ground-truth-value-cross-check + live-rendered-cache-busted-verification Phase C (when live state touched). Tiered: fast-path (grep-based, single trivial edit) vs full (multi-file/new-artifact/state-change). Gate count 19→20, orchestrator count 12→13. Composes with the mandatory-review-gate Stop/SubagentStop hook in `.claude/settings.json`. Addresses GAP-01/02/06 from `lesson-review-layer-misses-indexing-cache-run-2026-06-08`.
- **v3.3 (2026-06-07)** — Cross-project reusability + robustness (RQ-sprint step 3). **GPR-9:** Peer-reviewer dispatch blocks wired into all 9 non-Core-30 skills (service-seo-research, intersection-research, city-base-research, client-fact-research, competitor-deep-research, vis-extraction, intel-routing, multi-chat-coordination, multi-source-synthesis) — reviewer now fires across the whole toolkit, not just Core-30. **GPR-13:** Verdict severity tiers (`blocking` vs `advisory`) added to return contract (schema 1.1); operator decision matrix distinguishes must-review from auto-approvable; Check 5 Step 5.0 classifies severity before carry-forward. **GPR-14:** Standing planted-defect regression harness with 7 declared fixtures + 3 seed fixture implementations (meta-only-placeholder, og-title-source-client-leak, jsonld-wrong-value). Run at every version bump to prevent silent regression. Closes GPR-9/GPR-13/GPR-14 from the enhancement log.
- **v3.2 (2026-06-07)** — Reviewer live-gate self-sufficiency (RQ-sprint step 2). **GPR-11:** `live-rendered-cache-busted-verification` restructured into 3 phases (A: reviewer-owned fetch+parse, B: structural verification, C: cache-coherence second fetch) — reviewer performs its own independent live fetch, operator becomes optional spot-check. **GPR-12:** `full-placeholder-family-sweep` and `source-client-leak-audit` now enumerate 7 mandatory surfaces (body, title, meta-description, og:title, og:description, JSON-LD/schema, frontmatter) — "body only" sweeps impossible. Both procedures engine-level (any artifact with text content + optional metadata). Live-verification discipline expanded from 3 rules to 4. Closes GPR-11/GPR-12 from the enhancement log.
- **v3.1 (2026-06-07)** — Value-correctness layer (RQ-sprint step 1). New named procedure `ground-truth-value-cross-check`: engine-level facts registry that cross-checks every claimed value in an artifact (body + meta + og + JSON-LD) against declarative ground-truth profiles. Two profiles registered: `core-30-page-build` (6 checkable facts across 3 data sources) and `research-brief` (4 checkable facts — non-SEO proof). Procedure wired into G-data, G-scaffold, G-publish, G-city-brief, G-client-brief. Companion scripts: `hardcode-scanner.py` (SC-1 — post-scaffold default detection) and `facts-completeness-gate.py` (SC-2 — pre-scaffold data completeness). Both engine-level with declarative profiles. Boundary documented: this layer verifies output-matches-source, not source-matches-reality. All three always-required-explicit: even when the default value IS correct, the data file must state it consciously. Closes GPR-10/SC-1/SC-2 from the enhancement log.
- **v2.1 (2026-06-06)** — Build wave 2 calibration. Applied D-01–D-06 from the Alexandria production run calibration corpus (`lesson-gate-peer-reviewer-build-wave-2-calibration-2026-06-06`). Fixes: (D-01) source-client-leak-audit reads ALL foreign-client identity strings from `data/client-*.json` at runtime, never from memory; (D-02) full-placeholder-family-sweep reports real counts per token type, stage-classifies expected-vs-unexpected, clean-gate reserved for G-publish only; (D-03) pre-gate dispatch checklist — orchestrator must confirm peer-reviewer dispatched at every registered gate incl. G-imagery; Check 1 Step 1.2a requires execution evidence for named procedures. choose-image-variant.py updated: (D-04) variant filename bound in system prompt + post-score cross-variant contamination check; (D-05) 3-tier parse retry (same prompt → simplified prompt → JSON-only instruction), escalates with context instead of silent punt; (D-06) `--display-context hero|thumbnail|full-page` flag down-weights text_legibility for hero-size display. Engine remains project-agnostic (registered-instance pattern, no fork). D-07/D-08 (quality-loop/house-voice) + D-09 (meta-vs-body consistency) deferred to F5 skill-quality-integration-audit — cross-linked.
- **v2.0 (2026-06-05)** — Build wave 4. Cross-orchestrator generalization: registered client-seo-onboarding's 5 page-build gates (G-data / G-scaffold / G-imagery / G-publish / G-wave-close) as the second instance in the gate-type registry alongside vault-orchestrator Mode 6's 5 research-brief gates. 3 reusable named verification procedures added to the registry (full-placeholder-family-sweep, source-client-leak-audit, live-rendered-cache-busted-verification) — project-agnostic, referenced by gate type entries. Autonomous dispatch: orchestrator spawns peer-reviewer as a Task sub-agent after each gate — operator stops being the manual paste-transport. 6-check engine unchanged — page-build gates are a registered instance, not a fork. Calibrated against S&H Core 30 page-build peer-review corpus (PR-01..PR-40). Acceptance test: independently reproduces catches PR-01/07/15/16/17/19a/19b from Check 1 satisfaction targets without operator prompting.
- **v1.0 (2026-06-03)** — Initial ship. 6-check spec + 3-probe substrate detection + structured JSON return contract + write-authority constraint + vault-orchestrator Mode 6 integration (v1.3 bump in vault-orchestrator) + Mode 6 as seed gate-type registry instance + graceful degradation event log format. Build wave 1 — Cowork sequential substrate, operator-attended through 5 gates. Build wave 2 (production calibration) and Build wave 4 (cross-orchestrator generalization) deferred by design. See `lesson-gate-peer-reviewer-v1-build-2026-06-03.md` for build-time D-rows.
