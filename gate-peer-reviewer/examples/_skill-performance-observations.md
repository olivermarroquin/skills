---
type: skill-performance-log
status: active
skill: gate-peer-reviewer
skill-version: 1.0
created: 2026-06-03
updated: 2026-06-03
tags: [build-wave-2, calibration, meta-review, skill-performance, gap-log, peer-review-of-peer-reviewer]
---

# gate-peer-reviewer — skill performance observations (meta-review log)

The running record of how the `gate-peer-reviewer` skill performs when it runs **autonomously** on production gates, judged by an **external meta-reviewer** (a human-grade reviewer doing an independent 6-check pass on the same gate). It captures the **delta**: what the skill missed, what it over-flagged, and where its calibration drifted — so v1.1 / Build wave 2 has concrete, disk-grounded enhancement targets instead of guesswork.

**This file is the inverse of [[_candidates-for-build-wave-2]].** That file collects cases where the skill's spec *caught* real drift (positive exemplars → promote to `examples/`). This file collects where the skill *fell short* of an external reviewer (gaps → spec patches). Both feed Build wave 2; together they are the skill's full calibration corpus.

**Write-discipline.** Append-only. One `## Gate NNN` entry per reviewed gate. Never edit a prior entry except to flip its watchlist/patch status. Update the scoreboard at the top after each entry.

---

## Scoreboard (update after every entry)

The actionable rollup. Over N gates this surfaces which checks are weakest → that ranking *is* the v1.1 enhancement agenda.

| Metric | Count | Notes |
|---|---|---|
| Gates observed (skill-fired) | 0 | skill not yet fired in production — first fire is EV Wave 1 EXECUTE (Phase 1c) |
| Uncovered-gate manual reviews logged | 3 | Phase 0 + PROVISION (Mode 3) + cross-cutting pass-collision — see Coverage-gap observations |
| Skill verdicts that needed meta-correction before operator saw them | 0 | the headline efficiency metric: how often the meta-layer still has to intervene |
| Total misses (external caught, skill didn't) | 0 | — |
| Total false positives (skill flagged, not real) | 0 | — |
| Calibration deltas flagged | 0 | cost / confidence / verdict-severity off vs actual |

**Misses by check** (which check should have caught the miss):

| Check | Misses | Weakest-check rank |
|---|---|---|
| 1 — Contract satisfaction | 0 | — |
| 2 — Calibration consistency | 0 | — |
| 3 — Domain plausibility | 0 | — |
| 4 — Cross-gate / cross-wave coherence | 0 | — |
| 5 — Carry-forward management | 0 | — |
| 6 — Knowledge Capture Audit | 0 | — |

**Recurring-gap watchlist** (a gap that appears 2+ times → promote to a v1.1 spec-patch handoff):

- **`disk-verify-integration-target` (3 occurrences) → PROMOTE.** Asserting an input/integration target exists without grepping disk. Seen: gate-peer-reviewer build "5 gates" vs 1; [T2-4] schema registry doc-derived vs disk (lesson D-06); EV pages 06-12 PROVISION gap analysis (run Issue #7). **Fix:** input-existence / consumption-chain verification sub-check on Check 1, fired at the PROVISION gate. Tracked: handoff [T2-5] Phase B. Underlying pattern already promoted: `pattern-disk-verify-integration-target-before-drafting`.

---

## How an entry gets filled (frictionless protocol)

Designed to add **zero real-time coupling** to the Claude Code multi-agent run.

1. **The run produces the skill's output to disk.** A vault-orchestrator Mode 6 EXECUTE run (Claude Code, Task-tool parallel) dispatches the `gate-peer-reviewer` skill per gate via the Mode 6 Step-7 hook. The peer-reviewer's JSON verdict lands where Mode 6 already persists it — the project state file's `quality_log` and/or the per-wave gate file. No new plumbing.
2. **The meta-reviewer reads from disk — not in real time.** The external reviewer (a separate process/chat with disk access) reads (a) the original gate output and (b) the skill's JSON verdict from the state file / gate file, then runs an **independent** 6-check pass on the gate. The Claude Code run never waits on the meta-reviewer.
3. **Append one entry here** using the schema below.
4. **Update the scoreboard.** If a gap hits its 2nd occurrence, move it to the watchlist and (if warranted) draft a v1.1 spec-patch handoff.

Lower-friction fallback when no run is persisting to disk: the operator pastes the gate output + the skill's JSON verdict into the meta-reviewer chat, same relay used for manual gate review.

---

## Per-gate entry schema (copy for each new gate)

```markdown
## Gate NNN — <project> <wave-id> <gate-id> (YYYY-MM-DD)

**Substrate:** <claude-code-task | cowork-sequential | hermes-daemon>
**Source:** skill JSON read from <state-file quality_log | per-wave gate file | operator paste>

### Skill output (autonomous)
- **Verdict:** <APPROVE | APPROVE-WITH-NOTES | REJECT-AND-REDO | ESCALATE-AMBIGUOUS>
- **Catches:** <bullets the skill surfaced>
- **Cost / Sonar queries:** <$ / n>
- **Stated confidence:** <if present>

### Meta-reviewer independent pass
- **Verdict:** <my verdict>
- **Catches:** <bullets I surfaced independently>

### Delta
- **MISS** (I caught, skill didn't): <what> → **should have been caught by Check <N>** → **why it wasn't** (spec gap / triage filter too narrow / input not in skill's read-set / reasoning miss) → **proposed spec patch** (file + section/line)
- **FALSE POSITIVE** (skill flagged, not real): <what> → **why over-flagged** → **proposed tightening**
- **CALIBRATION**: <cost / confidence / verdict-severity vs actual>
- **AGREEMENT**: <where skill and I matched — confirms the check works; keep brief>

### Improvement signal
- **Recurring?** <1st instance | 2nd → watchlist | Nth>
- **Concrete target:** <e.g. references/check-spec.md Check 3 triage filter; gate-type-registry.md entry; return-contract.md field>
- **Verdict-of-verdicts:** did the skill's output need correction before the operator acted on it? <yes/no — this is the headline metric>
```

---

## Observations

### Coverage-gap observations (EV pages 06-12 run, 2026-06-03/04)

The skill has **not yet fired in production** — the EV pages 06-12 run reached Phase 1b (PROVISION) but the skill's only hook is the Mode 6 EXECUTE dispatch gate (Phase 1c). So every catch below came from the **manual meta-layer at gates the skill does not cover.** These are the calibration evidence base for extending coverage (handoff [T2-5] Phase B is gated on this).

**Uncovered gate: Phase 0 (measurement).** Manual review caught: (a) DataForSEO pulled at US-national + organic-only for a local-SEO client (wrong ranking surface; would have shipped "EV has zero visibility" — false); (b) the run's analysis noticed the Map-Pack-vs-organic distinction in prose but didn't act on it ("noticed-but-didn't-act"). → A future Check 3 (domain plausibility) extension should verify geo-targeting matches client locality + flag prose-vs-measurement mismatches. Source: run Issues #2.

**Uncovered gate: Phase 1b (PROVISION / Mode 3).** Manual review caught: gap analysis built from the pipeline model, not disk — claimed a non-existent troubleshooting brief existed + missed McLean/Oakton city data files; both would have broken Wave 2. → This is the literal job of a PROVISION-gate Check 1 with an **input-existence verification sub-check** (grep every claimed input; trace the full consumption chain). Source: run Issue #7. **This is exactly `pattern-disk-verify-integration-target-before-drafting` recurring at an uncovered gate.**

**Cross-cutting: pass-number collision.** Two chats nearly wrote the same changelog pass (116) because snapshots go stale. → A coherence check at any tracker-writing gate should re-read the pass counter from disk before allocating. Source: run Issue #9.

**Recurring-gap signal for the watchlist:** `disk-verify-integration-target` has now appeared as a catch at **3 uncovered gates/contexts** (gate-peer-reviewer build "5 gates" + [T2-4] schema registry doc-vs-disk + this PROVISION gap analysis). It is the single highest-value thing for the skill to automate via an input-existence / consumption-chain verification sub-check once coverage extends. → **Promote to the v1.1 spec-patch agenda** (see [T2-5] Phase B).

### Per-gate entries (skill-fired)

_The first skill-fired entry lands when Wave 1 EXECUTE (Phase 1c) dispatches — the first gate the skill actually covers. It will use the `## Gate 001` schema above._

---

## Related

- [[_candidates-for-build-wave-2]] — the positive-exemplar collector (spec wins → worked examples)
- [[check-spec]] — the 6-check spec these observations grade against; patch targets point back here
- [[gate-type-registry]] — where new gate types register; a miss may reveal a missing/under-specified gate type
- [[return-contract]] — the JSON shape the skill emits; a miss may reveal a missing field
- `SKILL.md` § "Version history" — Build wave 2 (production calibration) consumes this file
