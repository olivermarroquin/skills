---
type: execution-log
status: complete
created: 2026-11-21
updated: 2026-11-21
session: vis-p2-gate3-batch-202611200d9e
venture: vis-extraction
tier: Productize
tags: [execution-log, vis-extraction, gate3, productize]
---

# Execution Log — VIS Gate 3 (Phase 2 live batch)

**Session ID:** `0d9edbd7-72de-49d1-a684-1056d35d3440`
**Dates:** 2026-11-20 (batch started) — 2026-11-21 (complete) — 2026-11-23 (Gate 4 close)
**Tier:** Productize
**Mode:** Handoff-spawned, full auto, concurrency ≤2

---

## What was built

Five-URL live mini-batch run of the VIS extraction pipeline in full auto mode. Exercised Phase 0–8 per URL, the four-signal auto-proceed gate, and the escalation-log. Result: 1 auto-shipped (URL 5 — the 51-second Short), 4 parked (Signals 3 and/or 4 fail).

---

## Decisions made

1. **Coverage-diff exit 1 = Signal 4 FAIL regardless of flag quality.** Three notes had exit 1 with 0 real misses. Policy held: flag quality is a post-park human judgment; the exit code is the routing signal. This is correct — the alternative (auto-pass on "flags look like artifacts") would require the pipeline to trust its own self-assessment, which undermines the gate.

2. **G-extraction BLOCKING catch = fix and park, not halt.** For URLs 1 and 3, G-extraction returned APPROVE-WITH-NOTES with one BLOCKING-severity catch each. Advisory-only independence policy means: fix the finding, park the note, log the escalation-log row. The pipeline does not halt and wait for the operator — it proceeds. This matches the DECIDED 2026-09-21 independence policy.

3. **Escalation-log rows only for BLOCKING-severity catches.** URLs 4 and 5 had advisory-only G-extraction findings. No escalation-log rows written. Policy correctly applied.

4. **Short-form extraction uses standard pipeline.** URL 5 (51-second Short) went through the same Phase 0–8 pipeline as long-form URLs. No short-form lane deviation was needed. The only difference was attention-mode: standard (not dense-chunked) and expected exit 0 on coverage-diff (confirmed).

5. **Dense-chunked on URL 2 (26,255 words, 29 segments).** Required 3 sequential transcript reads covering ~1,200 lines each. Squeeze pass found 4 real misses. The dense-chunked mode works as designed for long transcripts.

---

## B1–B6 Productization-Readiness DoD

**B1 — Repeatable steps**

The pipeline Phase 0–8 is fully documented in `skills/vis-extraction/SKILL.md`. Another operator can follow the same steps on a new batch of URLs and expect the same behavior: transcript fetch → attention-mode decision → extraction → squeeze → coverage-diff → G-extraction → four-signal gate → ship or park. The batch digest format (file at `skills/vis-extraction/execution-logs/batch-digest-*.md`) is now demonstrated by this run.

**B2 — Engine/config split**

Engine: Phase 0–8 pipeline logic + four-signal gate + escalation-log policy (all in SKILL.md). Config: the URL list, batch size (≤2 concurrent), word-count threshold for dense-chunked (3,000 words + DENSE flag). The config is provided per-batch by the operator; the engine runs unchanged.

**B3 — Config schema**

Required config per batch:
- `urls`: list of YouTube URLs (video or Short)
- `concurrency`: integer ≤2
- `mode`: auto (four-signal gate applies) or interactive (operator approves each step)
- `attention-mode-threshold`: 3,000 words (default) + DENSE:yes judgment

Implicit config (from SKILL.md): escalation-log path, transcript cache directory, source-note output directory.

**B4 — 2nd-instance verdict**

Another operator could run this pipeline on a new batch of 5 URLs by following SKILL.md Phase 0–8 with the config above. The pipeline is not session-specific or model-specific. The reviewer (WORKHORSE tier) confirmed the five live-run checks pass, which is the independent verification that the documented procedure matches actual behavior.

**B5 — Safety/quality rules**

- Four-signal gate (Signals 1–4): all four must pass to auto-ship; any fail → park
- G-extraction independence policy: advisory-only; BLOCKING catches trigger an escalation-log row but do not halt the pipeline; first-batch-review remains open until operator reviews
- Park semantics: routing decision only; parked notes are fully extracted and await operator review
- Escalation-log policy: append rows only for BLOCKING-severity G-extraction catches
- Coverage-diff policy: exit code is the routing signal, not flag quality; exit 1 = Signal 4 FAIL regardless

**B6 — Skill-candidacy verdict**

The VIS extraction pipeline is a confirmed skill candidate (already registered as `vis-extraction` in `skills/`). Gate 3 validates Phase 2 specifically: the four-signal auto-proceed gate is now live-verified. The remaining unvalidated piece is Signal 2 (OQL Mode 5 wiring — currently advisory-pass-pending). See CG-006 in the capability-gap register.

---

## Capability gap — Signal 2 (OQL Mode 5 wiring)

Signal 2 runs as `advisory-pass-pending` in this batch. The OQL Mode 5 wiring (output-quality-loop evaluation as an auto-proceed gate signal) is not yet implemented. Every note in this batch passed Signal 2 with no evaluation. This is the designed state — Mode 5 wiring is a Phase 3 deliverable. Registered as CG-006 in `_capability-gap-register.md`.

---

## Coverage-diff auto-caption over-flagging

Signal 4 functioned as a mandatory-human-review gate for auto-captioned sources in this batch: 3 of 4 exit-1s had 0 real misses. Only URL 2 had real misses (OpenClaw, Granola/Fathom URLs — fixed before park). This is correct per policy but inefficient: the gate is spending operator-review cycles on notes with clean content. Registered as CR-281 in `_review-gate-catch-register.md`. Recommended fix: `--auto-caption` mode in coverage-diff.py that filters known phoneme-substitution patterns before scoring.

---

## OQL evaluation

**Mode:** catch-all (no routed spec for VIS batch runs in `spec-routing-table.md`)

**Artifact evaluated:** the five extraction notes + batch digest

**Checks:**
1. YAML frontmatter valid, all required fields present in all notes ✓
2. Plain-language sections present (In plain English) in all notes ✓
3. No TODO/FIXME/PLACEHOLDER tokens in shipped note (URL 5) ✓
4. Suggested judgments populated in all notes ✓
5. Tool URLs marked not-stated where transcript gives no URL (Pstack, Open Code, OpenClaw) ✓
6. Squeeze-delta transparency: delta fields populated and honest in all notes ✓
7. G-extraction catch-and-fix loop documented (escalation-log rows, fixes applied before park) ✓
8. Coverage-diff command and exit code documented in frontmatter for all notes ✓

**Mode 4 auto-research (analyst judgment — Perplexity Sonar not available; CG-006):** Strongest published version of a VIS batch extraction run would include: quantitative squeeze-pass tracking (this batch does: delta:4/4/2/0/0), coverage-diff exit code as frontmatter field (this batch does), escalation-log with BLOCKING-severity policy (this batch does), independent reviewer verification of the auto-proceed gate (this batch does via WORKHORSE reviewer). Gap: no routing row in OQL spec-routing-table.md for VIS source notes — a recurring gap noted in prior runs.

**OQL verdict:** PASS (catch-all)

---

## Weaker-method substitutions

- **Signal 2:** advisory-pass-pending instead of OQL Mode 5 → see CG-006
- **OQL Mode 4:** analyst judgment instead of Perplexity Sonar → see CG-003 (pre-existing)

---

## What to do next

1. Operator reviews 4 parked notes (the first-batch review queue)
2. Operator reviews 3 escalation-log rows, marks operator-action `approved` on each
3. After first-batch review, update `gate-type-registry.md` §P6 `independence_policy.first_batch_review` with date
4. Phase 3: wire OQL Mode 5 as Signal 2 (CG-006)
5. Phase 3: implement coverage-diff `--auto-caption` mode (CR-281)
