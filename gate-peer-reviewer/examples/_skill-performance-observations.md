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
| Gates observed (skill-fired) | 3 | Gate 001 (wave-1) + Gate 002 (wave-2) + Gate 003 (wave-3), 2026-06-04 |
| Uncovered-gate manual reviews logged | 3 | Phase 0 + PROVISION (Mode 3) + cross-cutting pass-collision — see Coverage-gap observations |
| Skill verdicts that needed meta-correction before operator saw them | 2 of 3 | Gate 001 (full reversal); Gate 002 (caught main issue, missed page 12); Gate 003 (NONE — clean + correct). **Trend: miss → undercount → clean.** |
| Total misses (external caught, skill didn't) | 2 | Gate 001 (Phase 1B command errors); Gate 002 (omitted page 12 from FILL-affected set + underframed 31-field scope) |
| Total false positives (skill flagged, not real) | 0 | — |
| Calibration deltas flagged | 0 | cost / confidence / verdict-severity off vs actual |

**Misses by check** (which check should have caught the miss):

| Check | Misses | Weakest-check rank |
|---|---|---|
| 1 — Contract satisfaction | 2 | Gate 001 (command refs non-existent files); Gate 002 (omitted page 12 from FILL-affected set — needs to enumerate ALL consumers of a shared input). **Weakest check — both misses here.** |
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

## Gate 001 — ev-electric-services wave-1-research-gap-close Mode 6 EXECUTE dispatch (2026-06-04)

**Substrate:** claude-code-task
**Source:** skill JSON emitted inline at the Mode 6 dispatch gate (first-ever production fire of the skill)

### Skill output (autonomous)
- **Verdict:** APPROVE-WITH-NOTES
- **Catches:** 3 notes — (1) no project state file exists, must init at Step 8; (2) cost/wall-clock uncalibrated (first run); (3) Phase 1B `--intersection-briefs` names services without briefs but "scaffold-city-data.py degrades gracefully." + 1 D-row candidate (state-file init schema).
- **Cost / Sonar:** $0 / 0
- **Stated confidence:** n/a (no field)

### Meta-reviewer independent pass
- **Verdict:** REJECT-AND-REDO
- **Catches:** Phase 1B command **will error and break the wave.** `scaffold-city-data.py` (lines 1236-1238) returns exit code 2 when a named `--intersection-briefs` file is missing; it does NOT skip. The command names 5 intersection briefs (`ev-charger,light-fixture,troubleshooting,smoke-alarm,outlet`) that resolve to `intersections/<svc>--mclean-va.md` / `--oakton-va.md` — none exist on disk. Fix: drop `--intersection-briefs` entirely (city-brief-only = the documented graceful empty-slots case; Wave 2 fills inline).

### Delta
- **MISS (load-bearing):** skill approved a Phase 1B command that errors on execution. **Should have been caught by Check 1** (does the command's referenced inputs exist?). **Why it wasn't:** Check 1 has no input/file-existence verification sub-check; the skill accepted the dispatch plan's "degrades gracefully" assertion without grepping for the named intersection-brief files. This is the SAME `disk-verify-integration-target` pattern the skill exists to automate — it missed an instance of its own core pattern.
- **CALIBRATION:** skill's other 2 notes (state-file init, uncalibrated cost) were correct + useful.
- **AGREEMENT:** state-file-init catch was a good, real Check 1 find.

### Improvement signal
- **Recurring?** disk-verify-integration-target — now ALSO at the EXECUTE dispatch gate (4th context). On watchlist; reinforces [T2-5] Phase B.
- **Concrete target:** `references/check-spec.md` Check 1 — add an **input/file-existence verification sub-check**: for every file/command the gate output references, grep disk; flag any that don't exist; for shell commands, verify the referenced inputs resolve. This would have flipped Gate 001 to REJECT-AND-REDO correctly.
- **Verdict-of-verdicts:** YES — the skill's output needed meta-correction before the operator acted (it would have approved a wave-breaking command). Headline metric: on its first production fire, the skill required human override on a load-bearing call.

**Re-emission (post-correction):** the corrected dispatch plan dropped `--intersection-briefs` (city-brief-only graceful path). Independent meta-review: **clean** — no new load-bearing issues; Phase 1A unchanged + sound, Phase 1B fix correct, sequencing + `--client-slug` resolution verified. The skill's re-emitted JSON correctly self-documented the Gate 001 miss (new D-02 high-severity catch + `pattern-disk-verify-integration-target` 4th-occurrence signal). Good transparency. The run (not the skill) did the disk-verify on the corrected command. **Follow-up (not done this turn — avoid mid-run churn):** bump `pattern-disk-verify-integration-target-before-drafting` times-observed 2→4 (my registry close-miss + Gate 001) + add Known Variation "applies to dispatch-plan shell commands, not just integration-spec drafting" — do at [T2-5] B1 ship.

## Gate 002 — ev-electric-services wave-2-page-scaffold-draft Mode 6 EXECUTE dispatch (2026-06-04)

**Substrate:** claude-code-task
**Source:** skill JSON emitted inline at the Wave 2 dispatch gate (skill's 2nd distinct gate fire)

### Skill output (autonomous)
- **Verdict:** APPROVE-WITH-NOTES. **Caught (good, on its own):** the 31-FILL-per-file content gap in the service data files — flagged that the scaffolder renders FILL strings verbatim and sub-agents must author inline. This is a real load-bearing catch the skill made itself — clear improvement over Gate 001 (which missed entirely). Also good: dry-ran the two weakest pages (07, 12).

### Meta-reviewer independent pass
- **Verdict:** APPROVE-WITH-NOTES (with corrections to the skill's enumeration).
- **Disk-verified:** 5/6 service files = 31 FILLs each (ev-charger, light-fixture, smoke-alarm, outlet, panel-upgrade); troubleshooting = 0. Confirms 07/11 are content-complete from the data file; 06/08/09/10/12 need full content authoring.

### Delta
- **PARTIAL MISS (load-bearing):** skill named pages "06, 08, 09, 10" as FILL-affected but **omitted page 12** (uses the same FILL'd `light-fixture.json`). Page 12 falls in a gap: the dispatch's inline-authoring instruction covers 07/11/12 for empty city slots; the FILL note covers 06/08/09/10 for FILLs — page 12's 31 FILLs are covered by neither. Would ship verbatim FILLs. **Should have been caught by Check 1** (trace every data file → every page consuming it).
- **UNDERFRAME:** skill framed 31 prose fields as "find/replace FILL"; actually it's the entire page copy. Wave 2 = the real content-authoring wave; estimate + cost are light.
- **AGREEMENT / improvement:** skill caught the core FILL issue unprompted (vs Gate 001 total miss) + dry-ran weakest pages. The calibration curve is bending the right way: Gate 001 = total miss; Gate 002 = caught main issue, undercounted scope.

### Improvement signal
- **Recurring?** disk-verify-completeness (trace ALL consumers/fields, not the subset you expect) — now at Gate 002 too. Same family as Issue #13. Reinforces [T2-5] B1 (input/consumption-chain verification must enumerate ALL consumers).
- **Concrete target:** `references/check-spec.md` Check 1 input-existence sub-check must also **enumerate every page/consumer of each shared input** (light-fixture.json → pages 06 AND 12), not just the first.
- **Verdict-of-verdicts:** YES, but lighter than Gate 001 — skill's verdict was directionally right; meta-correction added page 12 + scope reframe rather than reversing the verdict.

## Gate 003 — ev-electric-services wave-3-internal-link-publish-prep Mode 6 EXECUTE dispatch (2026-06-04)

**Substrate:** claude-code-task
**Source:** skill JSON inline at the Wave 3 dispatch gate (3rd distinct gate fire)

### Skill output (autonomous)
- **Verdict:** APPROVE (no catches). Light single-agent link-wiring wave; correctly carried forward the Issue #14 `{...}`-token residual check; noted page-10 fix verified.

### Meta-reviewer independent pass
- **Verdict:** APPROVE (agree). Disk-verified: page-10 `{city_name}` fix landed (0 tokens); all 5 cross-link targets (pages 01-05) exist on disk with the exact slugs the plan references. Plan is well-scoped, no FILL authoring, no external writes.

### Delta
- **NO MISS.** First gate where the skill approved clean and was correct. **Enhancement note (not a skill miss):** the dead-link audit verifies 01-05 internal targets match the build-order (disk), not that they resolve on the LIVE evelectric.pro site — a published-URL mismatch would dead-link. Low risk (01-05 published 2026-05-23/25, slugs match), but the audit should HTTP-verify live internal targets, not just build-order match. Surfaced as operator note, not a correction.
- **AGREEMENT:** clean plan, clean verdict.

### Improvement signal
- **Recurring?** none new.
- **Trend:** Gate 001 (full reversal) → Gate 002 (caught main issue, undercounted) → Gate 003 (clean + correct). Maturation curve bending toward trustworthy. Caveat: Gate 003 was a structurally simple wave (link-wiring); the harder test is whether the skill stays clean on a complex wave once [T2-5] B1 ships.
- **Verdict-of-verdicts:** NO meta-correction needed (first time).

---

## Related

- [[_candidates-for-build-wave-2]] — the positive-exemplar collector (spec wins → worked examples)
- [[check-spec]] — the 6-check spec these observations grade against; patch targets point back here
- [[gate-type-registry]] — where new gate types register; a miss may reveal a missing/under-specified gate type
- [[return-contract]] — the JSON shape the skill emits; a miss may reveal a missing field
- `SKILL.md` § "Version history" — Build wave 2 (production calibration) consumes this file
