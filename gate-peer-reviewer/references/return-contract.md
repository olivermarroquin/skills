---
type: reference
skill: gate-peer-reviewer
skill-version: 3.3
created: 2026-06-03
updated: 2026-06-07
tags: [reference, return-contract, json-schema, write-authority, severity-tiers]
---

# Return contract — full field-by-field spec

The peer-reviewer returns exactly this structured JSON shape per gate review. v1.1 schema (GPR-13 severity tiers added v3.2).

## Full shape

```json
{
  "schema_version": "1.1",
  "gate_reviewed": {
    "orchestrator": "<vault-orchestrator | client-seo-onboarding | ...>",
    "mode": "<Mode 6 EXECUTE | Mode 5 RESUME | ...>",
    "gate_id": "<Gate 2 PROVISION | Gate 4 dispatch | Gate 5 wave-close | ...>",
    "wave_id": "<wave-A4 | wave-A5 | null>",
    "chat_id": "<chat-id of the parent orchestrator>",
    "project_slug": "<s-and-h-contracting | ev-electric-services | ...>"
  },
  "verdict": "<APPROVE | APPROVE-WITH-NOTES | REJECT-AND-REDO | ESCALATE-AMBIGUOUS>",
  "verdict_severity": "<blocking | advisory>",
  "verdict_rationale": "<one-paragraph summary; load-bearing for operator scan>",
  "checks_skipped": [
    {"check": "check_3", "reason": "no domain-specific claims to probe"},
    {"check": "check_6", "reason": "not a closing gate"}
  ],
  "catches": [
    {
      "catch_id": "C-1",
      "severity": "<blocking | nit | calibration | follow-up>",
      "check_source": "<check_1 | check_2 | check_3 | check_4 | check_5 | check_6.layer_a | check_6.layer_b | check_6.layer_c>",
      "summary": "<one-line>",
      "rationale": "<2-3 sentences naming the specific finding + cited source>",
      "cited_source": "<file path + line OR Sonar query receipt OR memory file name>",
      "deliberate_evolution_check": "<acknowledged | unacknowledged | n/a>"
    }
  ],
  "operator_reply_text": "<paste-ready, self-contained, calibrated for direct paste back to the orchestrator substrate. Multi-paragraph if needed. Names each catch + proposes each fix. No 'see above' references.>",
  "d_row_candidates": [
    {
      "lesson_file_target": "<full path>",
      "row_id": "<D-N, next sequential>",
      "what_happened": "<one paragraph>",
      "signal_for_skill": "<one paragraph>",
      "action": "<one paragraph>"
    }
  ],
  "kickoff_prompt_patches": [
    {
      "next_wave_target": "<wave-A6 | next-project-onboarding | EV-pages-13-30>",
      "patch_location": "<which section of the kickoff prompt>",
      "patch_text": "<verbatim text to insert>",
      "rationale": "<why this patch prevents recurrence>"
    }
  ],
  "pattern_promotion_signals": [
    {
      "pattern_candidate_name": "<kebab-case>",
      "instance_count_after_this_run": "<1 | 2 | 3+>",
      "promote_now": "<true if instance_count >= 2, false if 1>",
      "pattern_file_target": "<full path if promote_now=true, else null>",
      "promotion_trigger": "<when next instance would fire, optional context>"
    }
  ],
  "cost_usd": 0.0,
  "sonar_queries_run": 0,
  "sonar_query_receipts": [
    {
      "query": "<verbatim query text>",
      "model": "sonar-pro",
      "cost_usd": 0.0,
      "anchoring_suffix_used": true
    }
  ],
  "wall_clock_seconds": 0
}
```

`checks_run` is implicit: `{check_1, check_2, check_3, check_4, check_5, check_6} \ {checks_skipped[].check}`.

## Field-level notes

| Field | Notes |
|---|---|
| `schema_version` | Locks the contract. Bumped to 1.1 at GPR-13. |
| `gate_reviewed.wave_id` | JSON `null` when orchestrator has no wave concept. Optional-presence — do not use sentinel strings (they break grep/regex at the parsing layer). |
| `gate_reviewed.chat_id` | Chat-id of the PARENT orchestrator emitting the gate, not the peer-reviewer's own chat-id. |
| `gate_reviewed.project_slug` | Used to locate the state file at `04_projects/<area>/<project_slug>/_state/onboarding.json`. |
| `verdict_severity` | Top-level severity: `blocking` if ANY catch is blocking; `advisory` otherwise. Determines whether operator must review or can auto-approve. See § Severity tiers. |
| `verdict_rationale` | Operator skims THIS first, not the catches array. Must stand alone. One paragraph max. |
| `checks_skipped[]` | Explicit list with reasons. Prevents silent skip-bugs. Default empty array `[]` if all 6 checks ran. |
| `catches[].deliberate_evolution_check` | Only populated when the catch is a cross-wave drift (Check 4). Forces explicit disambiguation. Values: `acknowledged` (deliberate evolution with D-row + contract update) / `unacknowledged` (silent drift) / `n/a` (not a cross-wave drift catch). |
| `operator_reply_text` | The single piece the operator copies to act on the review. Must be paste-ready, self-contained, no "see above" references. |
| `pattern_promotion_signals[]` | Automated promotion trigger per `workflow-knowledge-promotion`. First instance = candidate flagged (`promote_now: false`); second = promotion fires (`promote_now: true`). `promotion_trigger` field optionally documents when next instance would fire. |
| `cost_usd` | Total spend for THIS review invocation (Opus + Sonar). Honest accounting per `lesson-hermes-prework-c-perplexity-validation-2026-06-03.md` cost-correction precedent. |
| `sonar_queries_run` | Count of Sonar queries fired. Bounded by Check 3's 1-query-per-gate ceiling. |
| `sonar_query_receipts[]` | Per-query receipts. `anchoring_suffix_used: true` if English-anchoring suffix appended (recommended for all queries; non-English drift is a known failure mode). |
| `wall_clock_seconds` | Time from invocation to JSON return. Used for calibration data accumulation. |

## Severity tiers (GPR-13, v3.2)

Each catch carries a `severity` field. The top-level `verdict_severity` is the MAX severity across all catches (blocking > advisory). This tells the operator what truly needs eyes vs what's auto-approvable.

### Tier definitions

| Tier | Meaning | Operator action | Examples |
|---|---|---|---|
| `blocking` | Defect visible to end-users, search engines, or downstream consumers. Cannot ship. | Must review + fix before proceeding. | Source-client leak in any surface; wrong factual value (D-10/D-11/D-12/D-13); placeholder token at G-publish; live page rendering wrong content; JSON-LD claiming wrong entity |
| `nit` | Cosmetic imperfection. Not wrong, not harmful, but sub-optimal. | Auto-approvable. Operator may choose to fix or defer. | Slightly inconsistent capitalization in meta-description; non-ideal word choice in og:description; minor whitespace formatting |
| `calibration` | Prediction drift without downstream harm. Informational for future tuning. | Auto-approvable. Logged as D-row candidate. | Cost over-forecast (predicted $0.12, actual $0.07); wall-clock under-forecast |
| `follow-up` | Not a defect now, but will become one if not addressed in a named future step. | Auto-approvable now. Must be tracked for the named step. | Image FILL token at G-data (expected; must resolve at G-publish); pattern candidate needing second instance |

### Aggregation rules

```
verdict_severity = "blocking" if ANY catch has severity "blocking"
verdict_severity = "advisory" otherwise (all catches are nit/calibration/follow-up, or no catches)
```

### Operator decision matrix

| `verdict` | `verdict_severity` | Operator action |
|---|---|---|
| APPROVE | advisory | Proceed. No operator review needed. |
| APPROVE-WITH-NOTES | advisory | Auto-approvable. Notes logged for awareness. |
| APPROVE-WITH-NOTES | blocking | **Operator must review.** At least one catch is blocking but the gate is still approvable if the operator accepts the risk. |
| REJECT-AND-REDO | blocking | **Operator must review.** Orchestrator should auto-fix if possible (cap 2 iterations), else escalate. |
| ESCALATE-AMBIGUOUS | — | **Operator must review.** Reviewer cannot determine severity. |

### Engine-level applicability

Severity tiers are content-type-agnostic. "Blocking" means "cannot ship this artifact in this state" regardless of whether the artifact is a published page, a research brief, a routing decision, or a synthesis document. The definition is: "Would an end-user, search engine, or downstream consumer see incorrect/harmful content if this ships?" If yes → blocking. If no → advisory.

---

## Write-authority constraint

The peer-reviewer does NOT write pattern files, lesson D-rows, kickoff prompts, or any other vault artifact directly. It SURFACES proposed changes in `catches[]`, `d_row_candidates[]`, `kickoff_prompt_patches[]`, `pattern_promotion_signals[]` + names them in `operator_reply_text`. The originating chat (or operator) does the actual `times-observed` increment + decision-archaeology append + D-row write + kickoff edit.

**Peer-reviewer is a review layer, not a write layer.** This constraint exists because:

1. The peer-reviewer's primary contract is "say what's wrong + propose what's right." Writing the fix would conflate review with execution.
2. The originating chat has the full context (decision archaeology, prior framings, in-flight state) that the peer-reviewer's snapshot doesn't.
3. Write-authority separation prevents the peer-reviewer from compounding errors silently (a bad review followed by a bad write is worse than a bad review followed by operator catching it at write-time).

When a future orchestrator wants to "auto-apply" a peer-reviewer recommendation, the orchestrator does the write itself — not the peer-reviewer.

## Substrate-specific delivery

The JSON return is the substrate-neutral payload. How it lands in the operator's view depends on substrate:

| Substrate | Delivery shape |
|---|---|
| Claude Code Task tool | JSON returned to parent orchestrator, which renders it as markdown alongside the original gate output |
| Cowork sequential | JSON rendered inline in the chat as a markdown table + `operator_reply_text` in a copy-paste fenced block |
| Hermes-harness daemon (Level 3) | JSON posted back to parent substrate's stdin; parent substrate handles rendering per its conventions |

In all three cases, the operator sees: gate output + verdict + verdict_rationale + catches table + operator_reply_text in a paste-ready block.
