---
type: example
status: active
gate-id: G-extraction
created: 2026-09-24
updated: 2026-09-24
session: vis-p1-gate-integration
quality-log: "[[_quality-log#g-extraction-acceptance-test-2026-09-24]]"
last-evaluated: 2026-09-24
last-verdict: NEEDS REVISION (minor)
tags: [example, gate-peer-reviewer, G-extraction, vis-extraction, acceptance-test]
---

# G-extraction Gate — Acceptance Test (2026-09-24)

> **Purpose:** Gate 3 evidence for the VIS Phase 1 handoff (`vis-p1-gate-integration`). Demonstrates the
> G-extraction gate firing on two cases — fabricated-catch (BLOCKING) and clean-pass (PASS) — with
> mandatory-trace rows and verdict files on disk.
>
> **Reviewer:** FRONTIER session `40a9359a-c36d-4b6d-b899-3c09454f62b9` (adversarial test) +
> WORKHORSE sub-agent dispatch (clean-pass).

---

## Case 1 — Fabricated-catch (BLOCKING)

**Source note (injected fabrication):** adversarial test note with DubDance (ByteDance) tool injected

**Verdict:** BLOCKING

**Catches (3):**
1. Fabricated tool — "DubDance" cited as a ByteDance product; zero transcript grounding
2. Fabricated URLs — associated URLs not traceable to source
3. Fabricated workflow step — workflow step referencing DubDance not present in source

> **Skip-logic note:** REJECT-AND-REDO triggered at Check 1 (source-fidelity). Checks 2–5 skipped per gate-peer-reviewer SKILL.md skip-logic table — short-circuit is correct behavior, not a coverage gap.

**Verdict file:** `.review-gate/state/verdict-independent-40a9359a-adversarial-test-1790276926691.json`

**Mandatory trace (event-log row):** appended by FRONTIER reviewer session during adversarial test

**Outcome:** BLOCKING — source note would not proceed to write phase; operator escalation triggered per independence policy.

---

## Case 2 — Clean-pass (PASS)

**Source note:** `second-brain/03_domains/ai/agent-building/insights/source-2026-05-09-nate-herk-printing-press-cli-factory.md`

**Video:** "Printing Press Just 10x'd Everyone's Claude Code" — Nate Herk | AI Automation (2026-05-09)

**Verdict:** PASS

**Verdict file:** `.review-gate/state/verdict-G-extraction-gate3-clean-pass-1790280000000.json`

### check_2_calibration_metrics

| Metric | Result |
|--------|--------|
| Claims sampled | 5 (includes 2 tool/URL claims — printingpress.dev, Go language) |
| Section count | 7/7 required sections present |
| BLOCKING triggered | No |
| cost_usd | 0.0 (sub-agent advisory dispatch) |

### check_3_domain_probe_classes

**technical-tool-url-validity:**
- `printingpress.dev` — real service, strong live-demo internal evidence throughout note; tool released 2026-05-08 (contemporaneous extraction)
- Claude Code, Go, GitHub — all real; factually confirmed
- No unresolvable tool/URL claims

**insight-attribution:**
- CLI>API>MCP tier framing explicitly attributed to Nate's argument, not presented as generic fact
- Extractor differentiates this source from sibling Matt Pocock critique already in vault
- Speculative sections carry "Claude's analysis — not from source" headers
- Suggested judgments carry "Advisory only / Don't anchor on these" disclaimer
- PASS — no model-injected generic knowledge presented as source content

### check_source_fidelity

| # | Claim | Trace result |
|---|-------|-------------|
| 1 | printingpress.dev released ~2026-05-08 | GROUNDED — multiple live-demo references |
| 2 | 35x token savings / 100→72% reliability benchmark | GROUNDED with explicit epistemic flag ("unverified provenance, research task created") |
| 3 | 132k tokens → 2k tokens reach agent context | GROUNDED — live demo, numbers in quotes |
| 4 | CLIs built in Go (free, by Google) | GROUNDED — factually real, from install walkthrough |
| 5 | AllRecipes headless Chrome bypass | GROUNDED — specificity consistent with transcript observation |

Zero fabricated claims detected. Extractor's honest-limits disclosure (missing: auth mechanism, SQLite schema, CLI portability) is evidence of disciplined extraction.

### check_conventions_conformance (OC-28)

Script output: `1 vault files checked; 0 FAIL, 0 WARN, 1 PASS`
- C1 filename conventions: PASS
- C2 folder placement: PASS (valid for `source` type under `insights/`)
- C3 frontmatter schema: PASS (type, status, created, updated, tags all present and valid)
- C4 wikilink vault resolution: PASS (14/14 wikilinks resolved, zero unresolved)

### Mandatory trace (event-log row appended)

```
| 2026-09-24T00:00:00Z | vis-extraction: second-brain/03_domains/ai/agent-building/insights/source-2026-05-09-nate-herk-printing-press-cli-factory.md | G-extraction | vis-p1-gate-integration | G-extraction fired on nate-herk-printing-press-cli-factory (Gate 3 acceptance test — clean-pass); verdict: PASS; catches: 0 blocking, 0 advisory; sections: 7/7; model: WORKHORSE; advisory-mode. |
```

### Independence policy

Advisory-only per DECIDED 2026-09-21. Verdict is not blocking-capable until operator reviews the first logged batch at `second-brain/_meta/escalations/vis-extraction-escalation-log.md`.

---

## Verdict file schema (for reference)

Both verdict files follow the G-extraction contract (`check_structured_verdict` requirement):

```json
{
  "verdict": "PASS|HOLD|FAIL",
  "gate_id": "G-extraction",
  "session_id": "<reviewer-session-id>",
  "artifact": "<source-note-filename>",
  "checks_run": [
    {"name": "check_2_calibration_metrics", "result": "PASS|FAIL", "detail": "..."},
    {"name": "check_3_domain_probe_classes", "result": "PASS|FAIL", "detail": "..."},
    {"name": "check_source_fidelity", "result": "PASS|FAIL", "detail": "..."},
    {"name": "check_conventions_conformance", "result": "PASS|FAIL|WARN", "detail": "..."}
  ],
  "catches": [],
  "independence_policy": "advisory-only",
  "model": "WORKHORSE",
  "cost_usd": 0.0,
  "timestamp": "2026-09-24T...",
  "notes": "..."
}
```

---

## Gate 3 summary

Both acceptance-test cases demonstrate the G-extraction gate behaving as designed:
- **Fabricated content → BLOCKING** (3 catches, operator escalation path exercised)
- **Clean content → PASS** (7/7 sections, 5 sampled claims all grounded, OC-28 clean, advisory verdict)
- **Mandatory trace** → event-log row appended on both firings
- **Independence policy** → advisory-only in effect; BLOCKING escalation path confirmed working

The gate is wired correctly in vis-extraction Phase 6 as of v1.5 (VIS Phase 1). Phase 2 will wire Mode 5 OQL into the G-extraction verdict shape and escalation-log surface.
