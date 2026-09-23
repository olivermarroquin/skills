---
type: reference
skill: gate-peer-reviewer
skill-version: 4.1
created: 2026-09-23
updated: 2026-09-23
purpose: standing mandate for the meta-reviewer — the operator-side check on the independent reviewer itself
immutable: true
tags: [reference, meta-reviewer, mandate, review-gate, rgh-22, anti-regress]
---

# Meta-Reviewer Mandate

> **This file is the standing instruction set for the meta-reviewer role.**
> The meta-reviewer is a SECOND independent reviewer that verifies the first independent reviewer
> did not fabricate verdicts, downgrade findings under convergence pressure, or miss defects that
> the reviewer mandate requires catching. It is the anti-regress stopper for the reviewer layer
> itself. It is dispatched by the OPERATOR (or a strategic chat), not by the producer.
>
> Root cause: VIS-5 / CR-211 / CR-212 — a reviewer called convention violations
> "test-artifact conformance issues" and waved them off. Three rounds passed. This file
> ensures that pattern cannot compound silently into a future session.

---

## 0. When to dispatch

### Mandatory (every Productize-tier run)

Dispatch the meta-reviewer on EVERY Productize-tier run before the close commit is handed to
the operator. Productize-tier is the tier where B1–B6 DoD items are required (see
`productization-readiness-spec.md`). A Productize run that ships without meta-reviewer
clearance is an open D-09 class defect.

### Sampled (Capture-only and Throwaway tiers)

Dispatch on a random sample (~1 in 4) of Capture-only runs where the independent reviewer
returned a PASS. Throwaway runs are exempt. Sampling is manual for now — the operator
decides; no automated sampling until Hermes Phase 2.

### Always dispatch when

- The independent reviewer returned PASS on a run that the operator has reason to doubt.
- The independent reviewer's verdict was delivered unusually fast (< 90 seconds wall-clock for
  a full-tier review of 3+ files is a fabrication signal).
- A relay file shows the reviewer agreed with the producer on a contested finding without
  running independent verification commands.
- Any run where CR-212 class pressure was visible: reviewer language like "convergence is
  close," "minor conformance issue," "test-artifact only," or "not blocking in context."

---

## 1. What to verify

### Phase M1 — Verdict file integrity

1. Read the verdict file from `.review-gate/state/` — the path is in the reviewer's relay file
   or in the gate-block `->` pointer line.
2. Verify `reviewer_type: "independent"` is present.
3. Verify `checks_run` is non-empty and contains at least the checks mandated for the tier:
   - full-tier MUST include: `filename-kebab-case` (or equivalent C1), `frontmatter-freshness-OC-15`,
     `ground-truth-cross-check` (DEFERRED is acceptable if deterministic layer passed and LLM
     layer ran independently), `conventions-conformance-OC-28` (if any vault files touched).
4. Verify `mandate_version` ≥ `"1.4"` (the version that added OC-28 + no-downgrade rule).
5. Verify `cost_usd` is present. A $0.0 verdict on a full-tier multi-file review is suspicious —
   flag if `generator` is not `independent-reviewer-dispatch/deterministic`.

### Phase M2 — Execution evidence

1. Read the reviewer's relay file (`_relay-reviewer-<task-slug>.md`).
2. Verify the relay file contains ACTUAL COMMAND OUTPUT — not narrative summaries. A relay file
   that says "I ran the tests and they passed" without pasting the actual output is a fabrication
   signal (CR-214 class).
3. For OC-28 specifically: verify the relay shows the adversarial spot-check output (the 4-row
   table format from the mandate: `filename → C1: PASS/FAIL`). A reviewer that skipped the
   adversarial spot-check did not follow the mandate.
4. For test runs: verify the relay shows the exact pytest output (`N passed in Xs` line). A
   summary of "all tests passed" without the output is not acceptable.

### Phase M3 — No-downgrade check (CR-212 anti-regress)

1. Scan the reviewer's relay file for any of these phrases:
   - "test-artifact conformance issue"
   - "not blocking in context"
   - "convergence pressure"
   - "minor issue that doesn't affect"
   - "acceptable for this run"
   - "waving"
   - any language that reclassifies a FAIL as advisory/nit without citing a grandfathering rule
2. If any such phrase appears: flag it as a CR-212 class finding. The finding is BLOCKING —
   it means the reviewer's PASS verdict is tainted and must be re-verified from scratch by the
   meta-reviewer independently.
3. The only valid grounds for reclassifying a FAIL are:
   - The file appears in `GRANDFATHERED_SLUGS` or `GRANDFATHERED_SLUG_PREFIXES` in
     `oc28-conventions-conformance.py` (for OC-28 findings).
   - The operator explicitly granted a named exception (recorded in the catch register or
     handoff DoD exceptions list).
   - A `gate-skip.py` was run by the OPERATOR with `--force-deliverables` (D-09 class; flag
     it anyway so the operator knows it happened).

### Phase M4 — Re-run independent verification (if M2 or M3 flagged)

If Phase M2 or M3 surfaces a finding:

1. Run the deterministic checks yourself (independent meta-reviewer session):
   - `python3 ~/workspace/repos/ai-agency-core/scripts/mandatory-review-gate/oc28-conventions-conformance.py <vault-files>`
   - `pytest ~/workspace/repos/ai-agency-core/scripts/mandatory-review-gate/test_oc28.py -v`
2. Compare your output to the reviewer's claimed output. Any discrepancy is a CR-214 class
   fabrication finding — BLOCKING.
3. Write a meta-reviewer verdict (see §3 below) with your actual output pasted verbatim.

---

## 2. Dispatch rule (how to invoke)

The meta-reviewer is dispatched as a SEPARATE independent Claude Code session by the operator.
The operator hands the meta-reviewer:

1. The path to the reviewer's relay file: `~/workspace/_scratch/relay/_relay-reviewer-<task-slug>.md`
2. The path to the verdict file (from the gate-block output or the relay file).
3. The paths to the files that were reviewed.
4. This mandate file path: `skills/gate-peer-reviewer/references/meta-reviewer-mandate.md`

Spawn prompt template:

```
Read and execute the meta-reviewer mandate at:
~/workspace/skills/gate-peer-reviewer/references/meta-reviewer-mandate.md

Reviewer relay file: ~/workspace/_scratch/relay/_relay-reviewer-<task-slug>.md
Verdict file: <path-from-relay-or-gate-block>
Files reviewed: <file1> <file2> ...
Task slug: <task-slug>

Run Phases M1–M4. Write your meta-reviewer verdict and log it.
```

---

## 3. Meta-reviewer verdict format

After completing Phases M1–M4, write a verdict to:
`~/workspace/_scratch/relay/_relay-meta-reviewer-<task-slug>.md`

Format:

```
## META-REVIEWER VERDICT — <task-slug> — <date>

**Meta-reviewer session:** <session-id>
**Reviewing reviewer session:** <reviewer-session-id>
**Verdict: PASS | BLOCKING**

### Phase M1 — Verdict file integrity
[findings or PASS]

### Phase M2 — Execution evidence
[findings or PASS — paste any discrepant output verbatim]

### Phase M3 — No-downgrade check
[findings or PASS — quote exact phrases if flagged]

### Phase M4 — Independent re-run (if triggered)
[output pasted verbatim, or SKIP if M2+M3 clean]

### Overall assessment
[one paragraph]
```

If BLOCKING: the producer's session remains gated. Relay findings to the operator. The operator
decides whether to re-dispatch the reviewer or accept a named exception.

If PASS: the meta-reviewer clears the reviewer's verdict. The producer may proceed to commit.

---

## 4. Anti-regress commitment

This mandate exists because VIS-5 showed that a reviewer can rationalize away convention
violations across 3 rounds when under convergence pressure. The meta-reviewer is the circuit
breaker. Its job is not to be adversarial for its own sake — it is to catch the specific failure
mode of a reviewer that agrees with the producer instead of independently verifying.

**The meta-reviewer's single most important output is M3.** M1 and M2 are checks that a
diligent reviewer would always pass. M3 catches the subtle drift where a technically-present
verdict file masks a soft abdication. CR-212 is the reference incident. Know it.

---

## 5. Version

- **Mandate version:** 1.0
- **Created by:** [RGH-22] conventions-conformance ratchet (2026-09-23)
- **v1.0 (2026-09-23):** Initial — meta-reviewer role scoped to Productize-tier mandatory /
  Capture-only sampled. M1–M4 phases. CR-212 no-downgrade anti-regress as the primary
  purpose. OC-28 execution-evidence requirement (adversarial spot-check output required in
  relay). Mandate version gate: mandate_version ≥ 1.4.
