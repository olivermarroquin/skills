---
type: reference
skill: gate-peer-reviewer
skill-version: 1.0
created: 2026-06-03
updated: 2026-06-03
tags: [reference, check-spec, peer-review, six-checks, load-bearing]
---

# 6-check spec — verbatim

This is the operative spec content. Each check has: **Purpose / Inputs / Procedure / Verdict mapping / Worked examples / Cost**. Checks fire in strict order 1 → 2 → 3 → 4 → 5 → 6. Skip logic at the end.

---

## Check 1 — Contract satisfaction

**Purpose.** Verify the gate output does what its kickoff prompt asked for. The kickoff prompt is the contract; the gate output is the delivery. Drift between the two is the most basic failure mode — and surprisingly common, because orchestrators sometimes summarize / paraphrase / "improve" the contract during emission.

**Inputs read.**

1. The gate output text being reviewed.
2. The wave's kickoff prompt (the contract).
3. (For Gate 4 emissions only) the prior wave's revised-final dispatch prompts for the same orchestrator.
4. (For Gate 4 emissions only) the reusable dispatch prompt skeleton at `vault-orchestrator/references/sub-agent-dispatch-contract.md`, once [3A] ships. Until then, use the prior wave's final dispatch prompts as ground truth.

**Procedure.**

Step 1.1 — Parse the kickoff prompt for explicit requirements: numbered asks, "must include" lists, "verify" instructions, deliverable shape, success criteria. List them.

Step 1.2 — For each requirement, scan the gate output for satisfaction. Mark each ✅ / ❌ / ⚠️ (partial).

Step 1.3 — If the gate being reviewed is a **Mode 6 EXECUTE Gate 4 dispatch prompt emission**, run the Gate-4-specific structural compliance sub-check (below). Load-bearing because carry-forward drift fired at S&H wave A4 → A5 twice in a row.

**Gate-4-specific structural compliance sub-check.** Parse each sub-agent prompt and verify each of the 5 required template blocks is present:

| Block | What to verify present | If missing |
|---|---|---|
| Wrapper | Per-wave plugs (project slug, wave ID, sub-agent slug, artifact path) populated, no `<TODO>` placeholders | REJECT-AND-REDO |
| State-writes | Per-key `quality_log["<step>"]["<slug>"]` + `waves["<wave>"].outputs` append + `failures[]` append + bootstrap clause — OR explicit acknowledgment if architecture deliberately shifted to orchestrator-side | REJECT-AND-REDO if no acknowledgment; APPROVE-WITH-NOTES if shift is acknowledged but not yet folded into contract |
| Four-substep quality loop | Produce → output-quality-loop Mode 1 EVALUATE → Mode 4 AUTO-RESEARCH if not PASS → Mode 5 AUTO-APPROVE-AND-ESCALATE per v1.1 client-seo-onboarding contract — OR explicit acknowledgment if architecture shifted to inline self-eval | REJECT-AND-REDO if no acknowledgment |
| Structured JSON return contract | Required fields: `sub_agent` + `verdict` + `confidence` + `iteration_count` + `artifact_path` + `sonar_queries_run` + `sonar_cost_usd` + `failures[]` + `gate_file_rows_written[]` — OR explicit acknowledgment of field-set changes | REJECT-AND-REDO if fields silently dropped |
| Operator gate routing | 3 allowed + 3 forbidden gate types, per-wave declared | REJECT-AND-REDO if missing |

**Critical disambiguation.** The peer-reviewer must distinguish:

- **Deliberate architectural evolution** = operator-approved + documented as a D-row in the relevant lesson file + folded into a v1.2/v1.3/etc. contract update. Acceptable.
- **Silent drift** = block missing, no acknowledgment, no D-row, no contract update. Unacceptable.

When in doubt, **treat as drift and surface for operator decision**. False-positive cost = one operator clarification. False-negative cost = compounding chaos.

**Verdict mapping.**

| Finding | Verdict |
|---|---|
| All requirements satisfied + all Gate-4 blocks present (if applicable) | PASS — proceed to Check 2 |
| 1-2 minor requirements partially satisfied; nothing load-bearing | APPROVE-WITH-NOTES |
| Any load-bearing requirement unsatisfied OR any Gate-4 block missing without acknowledgment | REJECT-AND-REDO |
| Ambiguous whether requirement was meant literally vs as guidance | ESCALATE-AMBIGUOUS |

**Worked examples this check must independently reproduce.**

1. Wave A4 Gate 4 original draft — 4 operational sections stripped. Verdict: REJECT-AND-REDO.
2. Wave A5 Gate 4 — four-substep quality loop reverted to inline self-eval. Verdict: REJECT-AND-REDO.
3. Wave A5 Gate 3 close-condition #10 — stale 6-item audit reference vs current 8-item. Verdict: REJECT-AND-REDO.

**Cost.** Free.

---

## Check 2 — Calibration consistency

**Purpose.** Verify the gate's predictions (cost, wall-clock, sub-agent count, iteration count) match the trend of recent actuals.

**Inputs read.**

1. The gate output text (with predictions).
2. The state file's `wave_log[]` for the last 2-3 closed waves.
3. The most-recent 1-2 lesson files for this orchestrator.

**Procedure.**

Step 2.1 — Extract predictions: cost range, wall-clock, sub-agent count, iteration count.

Step 2.2 — Read `wave_log[]`. Pull actuals for the same metrics.

Step 2.3 — Compare. Flag any prediction that is:
- >2× the most recent actual (over-forecasting)
- <0.5× the most recent actual (under-forecasting)
- Trend direction inconsistent (e.g., last 3 waves trended down, this prediction trends up without justification)

Step 2.4 — If flagged, scan kickoff prompt + state file for justification. Justification absorbs the flag; no justification escalates it.

**Verdict mapping.**

| Finding | Verdict |
|---|---|
| Predictions match trend | PASS — proceed to Check 3 |
| Deviation flagged, justification present | APPROVE-WITH-NOTES (log calibration note for next D-row) |
| Deviation flagged, no justification | APPROVE-WITH-NOTES + D-row candidate |
| Systematic deviation (3+ waves in a row off by same direction + magnitude) | APPROVE-WITH-NOTES + kickoff-prompt patch |

Calibration misses are rarely `REJECT-AND-REDO` — they're capture opportunities. Exception: if deviation reveals a fundamental misunderstanding (e.g., gate predicts 100 sub-agents when substrate max is 25), `REJECT-AND-REDO`.

**Worked examples.**

1. Waves A2 + A3 + A4 cost over-forecasting (predicted $0.12-$0.45; actuals $0.075-$0.20). Verdict at A3 (first repeated miss): APPROVE-WITH-NOTES + kickoff-prompt patch at A4 recommending trailing-3-wave median anchoring.
2. Wall-clock over-forecasting same waves (predicted 30-50 min; actual 10-13 min). Same response shape.

**Cost.** Free.

---

## Check 3 — Domain plausibility

**Purpose.** Verify substantive content passes domain smell-tests. Some claims are jurisdiction- or time-specific — too granular to carry encyclopedically but cheap to probe via Sonar.

**Inputs read.**

1. The gate output text.
2. (Conditional) Sonar via `~/workspace/second-brain-tier3/automation/scripts/perplexity_sonar.py` on `sonar-pro`. **Bounded to 1 query max per gate.**

**Procedure.**

Step 3.1 — Identify domain-specific claims amenable to Sonar verification: utility company assignments in a jurisdiction, regulatory-body name currency, brand-name currency for cited entities, recent legislation affecting the brief's content.

Step 3.2 — Triage filter. Only fire Sonar if claim is BOTH (a) load-bearing AND (b) jurisdiction- or time-specific. Skip Sonar for general-knowledge claims.

Step 3.3 — If Sonar fires, use the English-anchoring suffix discipline. Append "in English" or "as of 2026 English-language sources" to anchor the response and prevent language drift. Sources: `05_shared-intelligence/lessons/lesson-hermes-prework-b-org-transparency-2026-06-03.md` (Sonar language drift D-row from Q3 governance query) + `05_shared-intelligence/lessons/lesson-city-base-research-anomaly-check-v1.1-build-2026-06-03.md` D-01 (APPA/VMEA unreachable resolved via Sonar retry with English anchoring). Single query, bounded cost ($0.025-$0.04).

Step 3.4 — Compare Sonar response against gate output. Flag mismatches.

**Verdict mapping.**

| Finding | Verdict |
|---|---|
| No domain-specific claims OR Sonar confirms claim | PASS — proceed to Check 4 |
| Sonar contradicts a load-bearing claim | REJECT-AND-REDO with Sonar finding cited verbatim |
| Sonar contradicts a non-load-bearing claim | APPROVE-WITH-NOTES + D-row candidate |
| Sonar response ambiguous | APPROVE-WITH-NOTES + flag for operator |

**Worked examples.**

1. Wave A4 Gate 2 PROVISION — Manassas Electric Utility gap. Orchestrator defaulted electric to Dominion; Sonar probe ("Which Virginia cities operate municipal electric utilities, in 2026 English-language sources?") returned MEPAV 16-entity roster including Manassas. Verdict: REJECT-AND-REDO. Full worked example at `examples/first-review-2026-06-03-s-and-h-wave-a4-gate-2-provision.md`.
2. Wave A5 Gate 2 PROVISION — NOVEC/Dominion split in Stafford + AlexRenew rebrand from Alexandria Renew Enterprises. Verdict: REJECT-AND-REDO for AlexRenew + APPROVE-WITH-NOTES for NOVEC/Dominion split (both load-bearing for service-area coverage).

**Cost.** $0.025-$0.04 per gate when Sonar fires. Typically 1-2 of 5 gates need it. Per-wave incremental: $0.025-$0.08. Upper-bound edge case (all 5 gates fire Sonar): $0.125-$0.20, bounded by triage filter.

---

## Check 4 — Cross-gate coherence + cross-wave structural coherence

**Purpose.** Two sub-checks. (4a) Within-wave: does this gate fit with the prior gate? (4b) Cross-wave: does this wave's structural pattern match the prior wave's revised-final pattern? Surfaces drift Check 1 alone misses — Check 1 verifies kickoff satisfaction; Check 4 verifies consistency with what already shipped.

**Inputs read.**

1. The gate output text.
2. Prior gate's output text within the same wave (state file `quality_log` rows + emitted text if cached).
3. Prior wave's revised-final artifacts of the same type. For Gate 4 emissions: prior wave's revised-final dispatch prompts (after any operator catch + restoration).

**Procedure.**

**Sub-check 4a — Within-wave cross-gate coherence.**

Step 4a.1 — Identify framing decisions made in the prior gate (e.g., "parallel dispatch", "sequential carry-forward", "4 sub-agents", "shared Sonar budget").

Step 4a.2 — Check this gate's content for consistency with each framing decision.

Step 4a.3 — Flag contradictions.

**Sub-check 4b — Cross-wave structural coherence.**

Step 4b.1 — Identify the artifact type (Gate 4 dispatch prompts, JSON return contracts, quality loop contracts, state-write contracts).

Step 4b.2 — Locate the prior wave's revised-final artifact. If none exists (first wave), skip 4b.

Step 4b.3 — Diff structurally:
- Gate 4 dispatch prompts vs prior wave's revised-final dispatch prompts. Any operational section stripped, simplified, or restructured = flag.
- JSON return contracts vs prior wave. Any field added/dropped = flag.
- Quality loop contracts vs prior wave. Any switch sub-skill ↔ inline = flag.
- State-write contracts vs prior wave. Any architectural shift = flag.

Step 4b.4 — Apply deliberate-evolution vs silent-drift disambiguation. Look for D-row + contract-update handoff + operator acknowledgment in the kickoff or state file.

**Verdict mapping.**

| Finding | Verdict |
|---|---|
| Within-wave + cross-wave both coherent | PASS — proceed to Check 5 |
| Minor cross-wave drift, operator-decidable on the fly | APPROVE-WITH-NOTES + paste-ready operator-reply |
| Load-bearing drift without acknowledgment | REJECT-AND-REDO + paste-ready operator-reply citing prior wave + proposing restore-OR-formalize |
| Within-wave contradiction | REJECT-AND-REDO + paste-ready operator-reply naming the contradiction |

**Worked examples.**

1. Wave A5 Gate 4 dispatch prompts vs A4 revised-final — three structural drifts: (i) four-substep quality loop → inline self-eval; (ii) state-writes sub-agent → orchestrator-only; (iii) JSON dropped `failures[]` + `gate_file_rows_written`. Verdict: REJECT-AND-REDO per drift with restore-OR-formalize framing.
2. Wave A4 Gate 3 within-wave contradiction — PWC dispatch plan said "parallel dispatch" but time estimates assumed sequential carry-forward. Verdict: REJECT-AND-REDO.

**Cost.** Free.

---

## Check 5 — Carry-forward management

**Purpose.** Translate every catch from Checks 1-4 into actionable artifacts the operator + future waves can use. Peer-reviewer is the single point where a catch becomes (a) an immediate fix prompt, (b) a D-row candidate for compounding intelligence, (c) a kickoff-prompt patch that prevents the same catch from firing twice.

**Inputs read.**

1. All catches surfaced by Checks 1-4 (held in working memory).
2. The relevant lesson file path (per orchestrator + wave naming convention).
3. The next wave's kickoff prompt template, if it exists in the spawn queue or as a draft.

**Procedure.**

Step 5.1 — For each catch, produce three outputs:

**(a) Paste-ready operator-reply text.** Self-contained (no "see above" references); names the specific issue; proposes the specific fix; calibrated for direct orchestrator paste.

**(b) D-row candidate.** Structured for direct lesson-file append. Fields:
- `lesson_file_target`: full path
- `row_id`: next sequential D-N
- `what_happened`: one paragraph
- `signal_for_skill`: one paragraph (skill-level, not wave-level)
- `action`: one paragraph naming concrete change

**(c) Kickoff-prompt patch (when applicable).** When the catch reveals a pattern likely to recur (drift fired twice across two waves, calibration tracks a trend), propose specific text for the next kickoff prompt.

Step 5.2 — Bundle all three classes into the structured JSON return.

**Verdict mapping.** Check 5 doesn't change the verdict — it ENRICHES it.

| Upstream check finding | Check 5 must produce |
|---|---|
| Any catch flagged | At minimum (a) operator-reply text + (b) D-row candidate |
| Catch is SECOND instance of same pattern across waves | All three (a) + (b) + (c) kickoff-prompt patch |
| Pattern surfaced for FIRST time | (a) + (b) + flag for second-instance promotion per `workflow-knowledge-promotion` |

**Worked example.**

Same dispatch prompt drift fired at A4 Gate 4 AND A5 Gate 4. After A4 correction, no A5 kickoff patch made. Peer-reviewer at A5 Gate 4 must produce all three outputs + flag the absence of an A5 kickoff patch as a meta-finding. Specifically: "Wave A6 kickoff prompt must include: 'Verify all 4 operational sections (state-writes + four-substep quality loop + structured JSON return contract + operator gate routing) present in each sub-agent dispatch prompt before emitting Gate 4. If any block is missing OR drifted from prior wave's final, restore from prior wave OR explicitly acknowledge as deliberate architectural evolution + queue a contract-update handoff.'"

**Cost.** Free.

---

## Check 6 — Knowledge Capture Audit verification (closing-gate-only)

**Purpose.** When the closing gate emits a self-reported "Knowledge Capture Audit PASSED N/N," peer-reviewer does NOT trust the self-report. Runs the 8-item audit per `feedback_knowledge_capture_audit_before_closing` memory across three layers. Self-audits have structural blind spots; external review doesn't.

**Inputs read.**

1. The closing gate emission (audit self-report).
2. Every file path the audit names as PASS — Read each from disk.
3. The lesson file for this wave.
4. The state file for the project.
5. The event log (`_meta/_event-log.md`) for rows tagged with this chat's chat-id.
6. Pattern files referenced in the audit or in this wave's work.
7. The handoff file for the next chat (if drafted in this wave).

**Procedure.**

### Layer A — Disk-verify each of the 6 original checklist items

| Audit item | What to disk-verify |
|---|---|
| 1. Lesson D-rows | Lesson file exists at expected path; D-row count matches self-report; each D-row has non-placeholder content |
| 2. Execution log | Execution log file exists at expected path; timeline + decisions captured |
| 3. Event log | Event-log rows present for this chat-id; rows name meaningful semantic events |
| 4. State file accurate | State file fields reflect closed-wave state |
| 5. Tool bugs as D-rows | If chat surfaced tool/script bugs, they're in lesson D-rows tagged as such |
| 6. Patterns validated/refuted | Pattern files referenced have current `times-observed` counts + `decision-archaeology` entries naming THIS run |

If any item fails Layer A → REJECT-AND-REDO with specific gap named.

### Layer B — Item 7 completeness probe (what's missing)

Probe 6 sub-categories self-audits routinely miss:

- **Stale pattern files** — referenced but `times-observed` not incremented + no `decision-archaeology` entry for this run.
- **Pattern extraction candidates** — reusable shapes surfaced without a pattern file written (per workflow-knowledge-promotion: 1st instance = candidate flagged; 2nd = pattern promoted).
- **Dangling references** — file paths cited in newly-written content (lesson, execution log, SKILL.md) that don't exist on disk.
- **Confidence-calibration data scattered** — Sonar cost actuals, wall-clock actuals, iteration counts in scattered places without consolidation.
- **Decision-archaeology gaps** — non-obvious choices made without WHY captured (e.g., "chose Option A over B" without rationale).
- **Cross-skill composition signals** — cases where this skill's output triggered or could trigger another skill, not documented.

If Layer B surfaces gaps → APPROVE-WITH-NOTES + specific fill-in proposals.

### Layer C — Item 8 reusability probe (is what's there useful?)

Files existing on disk is a FLOOR, not a ceiling. Verify each captured artifact contains content depth a future agent needs to rerun the work without re-deriving from scratch. Test against reuse contracts:

| Artifact | Reusability contract |
|---|---|
| Execution log | (a) Full timeline with decisions + WHY each decision (rationale, not just outcome); (b) cost actuals broken out by sub-agent + per-query cost; (c) what worked / what was harder / what was easier; (d) concrete artifact references with paths + commit hashes + cost lines. Timestamps without decisions = not reproducible. |
| Lesson D-rows | Every D-row has 3-part structure: What happened / Signal for the skill / Action. D-rows that only say "X happened" without skill-level signal or next-action are narrative, not knowledge. |
| Pattern files | When `times-observed` incremented, matching `decision-archaeology` entry names (a) validating/refuting run, (b) specific behavior that validated/refuted, (c) WHY this run was novel evidence. Bare count increments are folklore. |
| Handoffs (newly-drafted) | Include `spawn-trigger` + `scope` + `close-protocol` + `estimated effort` + `related` links sufficient for a fresh chat with no prior context to spawn cleanly. Handoffs that say "do X" without WHY now, WHAT to do, HOW to close, or WHO it composes with are unspawnable. |
| State file quality_log entries | Name not just verdict + confidence but reason + iteration count + gaps. Bare `{"verdict": "PASS"}` entries insufficient. |
| Event log rows | Name meaningful semantic event (not just "edit") + chat-id + file changed, so parallel chats see WHY each event matters. |

If Layer C surfaces gaps → APPROVE-WITH-NOTES + reusability fill-in proposals. Peer-reviewer CAN fill structural gaps (e.g., missing execution log skeleton) but FLAGS rather than fills content gaps requiring the originating chat's context.

**Verdict mapping.**

| Finding | Verdict |
|---|---|
| All 3 layers pass | PASS — closing gate confirmed |
| Layer A fails | REJECT-AND-REDO; specific gap named |
| Layer B surfaces gap | APPROVE-WITH-NOTES; fill-in proposals |
| Layer C surfaces gap | APPROVE-WITH-NOTES; reusability fill-in proposals + flag for operator |

**Worked example.**

Wave A4 Gate 5 close — self-reported 6/6 PASS, disk verification surfaced 6 gaps: execution log missing; pattern file `times-observed: 1` when truth was 6; 4 missing supplemental D-rows; pattern extraction candidate not extracted; dangling `confidence-calibration.md` reference. Verdict: APPROVE-WITH-NOTES (or REJECT-AND-REDO if execution log entirely missing).

**Cost.** Free for all 3 layers.

---

## Skip logic (reference)

| Condition | Skip |
|---|---|
| Check 1 returns `REJECT-AND-REDO` | Skip Check 3 (Sonar cost); STILL run Check 4 (free, surfaces additional structural drift); jump to Check 5 + Check 6 if closing gate |
| Gate is not a closing gate (Gates 1-4 in Mode 6) | Skip Check 6 entirely |
| Gate is not a Mode 6 EXECUTE Gate 4 emission | Skip Gate-4-specific structural compliance sub-check inside Check 1 |
| No domain-specific claims surface in Check 3 triage | Skip Sonar fire; Check 3 returns PASS without cost |
| First wave of an orchestrator run (no prior wave to compare) | Skip Sub-check 4b |
