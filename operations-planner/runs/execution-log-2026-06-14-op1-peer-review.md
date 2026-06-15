---
type: execution-log
status: draft
created: 2026-06-14
updated: 2026-06-14
venture: operations-planner
tags: [execution-log, operations-planner, peer-review, adversarial-review]
---

## 2026-06-14 — [OP-1] adversarial peer review

**What was built:** Independent adversarial peer review of the [OP-1] operations-planner reverse-dependency leverage scorer build, across all 4 operator gates.

**Reviewer findings (7 items across 4 gates):**

### Gate 1 (Plan) — 2 catches

1. **`ready_now` filter too loose** — accepted `in_flight` deps as "done." Fixed before build.
2. **"Compose" claims needed honest scoping** — demanded the build specify whether it was actually calling skills or reimplementing inline. Result: honest documentation that it reimplements simple arithmetic inline (correct trade-off for v1).

### Gate 2 (Leverage spot-check) — 3 catches

3. **RGH-1 `active` → `queued` bug** — Build claimed "frontmatter says status: queued" but disk showed `status: active`. Root cause: `active` was not in the STATUS_TO_COLUMN map, defaulting to `queued`. Real bug in analyze.py, fixed by adding `active` → `in_flight`. Took 3 iterations to diagnose: first the build blamed _recently-closed matching, then I redirected to the simpler question ("why is a node with `status: active` in `ready_now` at all?").
4. **DI-1 blocker status mislabeled** — Build said "blocked by PHASE-4B (in_flight)" but COA-4b frontmatter says `status: draft`. Turned out the tracker override (pass 188, from a parallel chat) was correct — tracker is canonical runtime state.
5. **Pass 188 reference challenged** — Flagged as potentially fabricated. Verified real (parallel COA-4b chat created it).

### Gate 3 (Proof run) — 4 non-blocking notes

6. **CORE-30 duplicate IDs** — 4 entries with identical `CORE-30` tag, no disambiguation.
7. **LEVEL-4 "None (next)" display** — Blocker nodes without tags render as `None`.
8. **COA phases inflating ready_now** — Tracker references them collectively via README wikilink, not individual files; analyzer can't match.
9. **`waiting_on` shape vs contract** — Tag-keyed, not gate-keyed as the draft contract suggests.

### Gate 4 (Closing) — 1 catch (post-ship)

10. **Pre-staged git collateral** — Skills commit included 17 extra files from 8 other skill dirs that were pre-staged from prior sessions. Scope discipline violation. See [[lesson-git-add-by-name-pre-staged-collateral-2026-06-14]].

**Decisions made:**
- Approved all 4 gates (Plan → Leverage → Proof run → Closing)
- Catches #1-5 were fixed before ship; #6-9 recorded as known limitations; #10 discovered post-ship

**Reusable for future apps?:** Yes — the peer review protocol (demand disk-verified evidence, don't trust build chat prose claims, check `git status` before commits) applies to every build chat. Reinforces [[pattern-independent-peer-review-chat]].
