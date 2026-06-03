---
type: build-wave-2-candidates
status: queued
created: 2026-06-03
updated: 2026-06-03
skill: gate-peer-reviewer
tags: [build-wave-2, calibration, worked-example-candidates]
---

# Build wave 2 — worked-example candidates

Production-use runs of the Check 6 KCA verification spec (Layer A / B / C) that surfaced silent-drift failures the originating chat would have shipped otherwise. Each candidate is a 1st-instance external-skill-use exemplar suitable for promotion into `examples/` at Build wave 2 calibration.

## Candidate 1 — competitor-deep-research v1.1 enhancement chat (2026-06-03)

**Originating chat:** `competitor-deep-research-enhancements-202606032030`
**Date:** 2026-06-03
**Substrate:** Cowork sequential

**What the chat shipped before the gap-close:**
SKILL.md v1.0 → v1.1 + 2 reference template edits + 1 enhanced EV synthesis (non-destructive) + 1 sibling skill update (service-seo-research SKILL.md) + tracker close + 4 event log rows + handoff status flip.

**What the operator-applied KCA caught at gap-close (mirrors the Check 6 spec):**

- **Gap 1 (Layer A, item 1 — Lesson D-rows):** No lesson file existed at `05_shared-intelligence/lessons/lesson-*competitor-deep-research*2026-06-03*.md`. Disk-verified via Glob. Operator required at least 7 D-rows + 1 pattern candidate before commit.
- **Gap 2 (Layer A, item adjacent — v1.0 → v1.1 paperwork):** SKILL.md frontmatter had no `version:` field; no changelog blockquote. Operator required both, mirroring vault-orchestrator v1.3 pattern (line 8 template). Cited the D-row as deliberate-evolution archaeology.
- **Gap 3 (procedural):** Operator required the full 8-item KCA (Layers A/B/C) self-report before commit, per `feedback_knowledge_capture_audit_before_closing` + the Check 6 spec shipped at [2A] earlier the same day.

**Outcome after gap-close:**
- Lesson file shipped: 7 D-rows (D-01 Tier-2 sequencing, D-02 15-field selection with cuts named, D-03 ≥80% threshold with rejected alternatives, D-04 dual-path design, D-05 $0.00 baseline, D-06 Root Electric archaeology, D-07 non-destructive `-enhanced` filename) + `pattern-reproduce-cross-competitor-structural-blueprint` 1st-instance candidate flagged for WAIT-for-2nd-instance promotion.
- SKILL.md frontmatter `version: 1.1` + changelog blockquote at line 8 added (mirrors vault-orchestrator v1.3 line 8 pattern; cites `feedback_check_folder_structure_before_writing` as deliberate-evolution discipline; cross-links D-07 archaeology).
- 8-item KCA Layer A + B + C all PASS — self-reported with disk-verify probe outputs captured in execution log.

**Why this is the 1st-instance exemplar.**
This is the first production use of the Check 6 spec **outside** the gate-peer-reviewer build chat itself. It validates the spec catches REAL silent-drift failure modes (not just synthetic test cases from the build chat). Self-applying-spec demonstration: the chat tried to ship without applying the discipline; the operator (acting as external peer-reviewer proxy) caught it via the Check 6 Layer A spec; gap-close cycle produced the missing artifacts.

**Why this stays a 1st-instance for `pattern-skill-build-self-applying-spec-demonstration`.**
Caught-by-external-review (operator-as-peer-reviewer-proxy), NOT caught-by-own-spec (the originating chat's own skill spec). Per the discipline applied: 2nd-instance promotion fires when a skill build catches its own failure mode VIA ITS OWN SPEC. Count stays at 1.

**Files to reference when promoting to a worked-example:**
- `~/workspace/second-brain/05_shared-intelligence/lessons/lesson-competitor-deep-research-v1.1-enhancements-2026-06-03.md` — 7 D-rows + pattern candidate row + self-applying-spec observations subsection
- `~/workspace/second-brain/_meta/execution-logs/exec-log-2026-06-03-competitor-deep-research-enhancements.md` — KCA self-report subsection with full Layer A / B / C disk-verify probe output
- `~/workspace/second-brain/_meta/handoffs/handoff-2026-05-26-competitor-deep-research-enhancements.md` — Actual deliverable blockquote at top names all 6 deliverables shipped
- Git commits: second-brain `b528e41`, skills `7d14eb0`

**When to promote into `examples/<filename>.md`:**
At Build wave 2 (production calibration) — operator already named this slot at gap-close 2026-06-03. Suggested filename: `external-use-2026-06-03-competitor-deep-research-v1.1-gap-close.md`.

## How to add a candidate

When the gate-peer-reviewer spec catches a real silent-drift failure during a non-build chat (production-use), append a new ## Candidate N section here. Naming convention: `Candidate N — <originating-chat-topic> (YYYY-MM-DD)`. Keep each candidate self-contained so Build wave 2 can promote without re-deriving context.
