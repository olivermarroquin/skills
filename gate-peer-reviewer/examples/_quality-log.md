---
type: folder-quality-log
status: active
created: 2026-09-24
last-updated: 2026-09-24
artifacts-tracked: 1
shipped: 1
iterating: 0
escalated: 0
tags: [folder-quality-log, quality-loop]
---

# Quality log — gate-peer-reviewer/examples

This file tracks every output-quality-loop evaluation for artifacts in this folder.
One section per artifact; iteration history inside each section.

See [[output-quality-loop|the skill]] for evaluation methodology and the verdict-rollup thresholds.

---

## g-extraction-acceptance-test-2026-09-24

**Latest:** NEEDS REVISION (minor) (2026-09-24) — iteration 1 of 3

### Iteration 1 — 2026-09-24

**Evaluated:** 2026-09-24
**Artifact type:** unrouted (catch-all evaluation) — worked example / acceptance test; no dedicated routing entry
**Spec sources loaded:** [plain-language-conventions.md, conventions.md, CLAUDE.md (catch-all); gate-peer-reviewer SKILL.md § Return contract; gate-type-registry.md P6 check_structured_verdict requirement]
**Note:** This artifact type has no dedicated routing entry. If worked-example / acceptance-test type recurs, add a row to spec-routing-table.md.
**Verdict:** NEEDS REVISION (minor)
**Iteration:** 1 of 3

#### Hard requirements

- [✓] Frontmatter present and well-formed — `type: example`, `status: active`, `gate-id: G-extraction`, `created:`, `updated:`, `session:`, `tags:` all present; YAML parses cleanly (spec source: conventions.md § frontmatter schema)
- [✓] File in correct location — `skills/gate-peer-reviewer/examples/` is the examples folder referenced in gate-peer-reviewer SKILL.md § Worked examples (spec source: gate-peer-reviewer SKILL.md § Worked examples)
- [✓] Two test cases present — Case 1 (BLOCKING fabricated-catch) and Case 2 (PASS clean) cover the two primary verdict paths for G-extraction (spec source: gate-type-registry.md P6 — acceptance test should demonstrate both paths)
- [✓] Case 1 names three specific catches — fabricated tool, fabricated URLs, fabricated workflow step — with enough detail to be actionable (spec source: gate-peer-reviewer SKILL.md § Return contract — `catches[]` must name finding + surface)
- [✓] Case 2 includes `check_2_calibration_metrics` table — 5 claims sampled (≥3 required), includes 2 tool/URL claims (≥1 required), 7/7 sections, BLOCKING not triggered, cost_usd recorded (spec source: gate-type-registry.md P6 check_2_calibration_metrics)
- [✓] `check_3_domain_probe_classes` results present for both sub-classes — `technical-tool-url-validity` and `insight-attribution` — each with specific findings (spec source: gate-type-registry.md P6 check_3_domain_probe_classes)
- [✓] `check_source_fidelity` mandatory-trace table present — 5 claims, trace result for each, zero fabricated claims stated (spec source: gate-type-registry.md P6 check_source_fidelity)
- [✓] `check_conventions_conformance (OC-28)` section present — script output quoted verbatim (`1 vault files checked; 0 FAIL, 0 WARN, 1 PASS`), four sub-checks named with results (spec source: gate-type-registry.md P6 check_conventions_conformance)
- [✓] Mandatory trace event-log row format shown — row follows exact schema from vis-extraction SKILL.md § Mandatory trace (spec source: vis-extraction SKILL.md § Mandatory trace — event-log row format)
- [✓] Independence policy section present in Case 2 — names advisory-only, references escalation log, states first-batch-review constraint (spec source: gate-type-registry.md P6 independence_policy)
- [✓] Verdict file schema block present — JSON shape with all four required_fields (`verdict`, `checks_run`, `catches`, `cost_usd`) plus `gate_id`, `session_id`, `artifact`, `independence_policy`, `model`, `timestamp`, `notes` (spec source: gate-type-registry.md P6 check_structured_verdict.required_fields)
- [✗] Case 1 verdict file path references a real-looking but unverifiable `.review-gate/state/` path — the file `verdict-independent-40a9359a-adversarial-test-1790276926691.json` is cited but no corresponding disk-verification is shown in the document. For an acceptance test this is a gap: the test should either confirm the verdict file exists on disk or note it was produced by the adversarial FRONTIER session and may not persist (spec source: CLAUDE.md § Mandatory Pre-Land Review Gate — verdict file must exist on disk; gate-type-registry.md P6 check_structured_verdict.severity — BLOCKING if verdict file absent)

#### Quality dimensions

- [✓] Gate 3 summary section closes the document cleanly — four bullet points mapping behaviors to expectations; reads as a genuine acceptance-test pass statement (spec source: plain-language-conventions.md — clear conclusions)
- [✓] Case 2 claim trace table is specific — each row names the claim, the trace result, and grounding evidence; "unverified provenance, research task created" honest-limits disclosure is captured (spec source: gate-type-registry.md P6 check_source_fidelity.detail — epistemic honesty)
- [✓] "Speculative sections carry headers" and "Suggested judgments carry disclaimers" noted in insight-attribution — demonstrates the reviewer actually checked extraction discipline, not just fabrication (spec source: vis-extraction SKILL.md § Core workflow — extraction discipline)
- [Partial] Case 1 is thin on check_2_calibration_metrics and check_3_domain_probe_classes results. For the BLOCKING case, the reader cannot tell whether section_count was checked or whether domain probes were run before the fabrication was caught. An acceptance test ideally shows that the reviewer ran all checks, not just the one that triggered BLOCKING. Minor gap — the purpose of Case 1 is to demonstrate the catch path, not full coverage, but a one-line acknowledgment ("checks 2–3 skipped per skip-logic: REJECT-AND-REDO triggered at Check 1") would complete the picture. (spec source: gate-peer-reviewer SKILL.md § The 6 checks — skip logic table)
- [✓] Phase 2 composition note in Gate 3 summary is accurate — "Phase 2 will wire Mode 5 OQL into the G-extraction verdict shape and escalation-log surface" consistent with output-quality-loop SKILL.md § Mode 5 composition note (spec source: output-quality-loop SKILL.md § Mode 5)
- [✓] Plain language throughout — no jargon-only passages; "adversarial test" is self-explanatory; BLOCKING/PASS verdict labels are clear (spec source: plain-language-conventions.md)

#### Discipline rules

- [✓] File does not write vault artifacts — this is a reference/example document; write-authority constraint honored (spec source: gate-peer-reviewer SKILL.md § Return contract write-authority constraint)
- [✓] `updated: 2026-09-24` matches `created: 2026-09-24` — correct for a new file (spec source: CLAUDE.md — bump `updated:` on every content edit)

#### Suggested fixes

1. Add a one-line note under Case 1's verdict block: "Checks 2–5 skipped per skip-logic: REJECT-AND-REDO triggered at Check 1." This is the expected behavior per gate-peer-reviewer SKILL.md § The 6 checks skip-logic table, and naming it explicitly proves the acceptance test understands the skip rules.
2. Add a one-line note about whether the Case 1 verdict file persists on disk, or note that the adversarial FRONTIER session produced it and it is in `.review-gate/state/` — helps a future operator auditing the acceptance test know whether to look for the file or treat it as a simulated output.

**Revision prompt:** generated 2026-09-24; see suggested fixes above (minor; no separate .revision-prompt.md created for minor verdict)

---
