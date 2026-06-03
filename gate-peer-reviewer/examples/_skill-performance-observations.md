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
| Gates observed | 0 | — |
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

_None yet. A gap lands here on its 2nd occurrence with a one-line pointer to both entries._

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

_Awaiting the first production gate (first EV or S&H execution wave). Entries append below as `## Gate 001`, `## Gate 002`, …_

---

## Related

- [[_candidates-for-build-wave-2]] — the positive-exemplar collector (spec wins → worked examples)
- [[check-spec]] — the 6-check spec these observations grade against; patch targets point back here
- [[gate-type-registry]] — where new gate types register; a miss may reveal a missing/under-specified gate type
- [[return-contract]] — the JSON shape the skill emits; a miss may reveal a missing field
- `SKILL.md` § "Version history" — Build wave 2 (production calibration) consumes this file
