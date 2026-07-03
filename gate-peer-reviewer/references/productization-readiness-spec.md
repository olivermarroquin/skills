---
type: reference
skill: gate-peer-reviewer
skill-version: 4.0
created: 2026-07-02
updated: 2026-07-02
purpose: The "automatable by default" standard — tier classifier, Productization-Readiness DoD (B1-B6), deliverable manifest template, gate extension spec for RGH-18/19, task-definition rules, catch→check ratchet. Built by [PR-1].
built-by: pr1-productization-readiness-202607021000
tags: [reference, productization, automation, tier-classifier, dod, deliverable-manifest, capability-gap, task-definition, catch-check-ratchet, pr-1]
---

# Productization-readiness spec ("automatable by default")

> **Built by [PR-1]** (Wave A step 2 of the "Automatable by default" sprint, 2026-07-02).
> This spec DEFINES the standard. Deterministic enforcement code is built by
> [[handoff-2026-06-25-rgh18-deterministic-build-correctness-gate|RGH-18]] (build-correctness checks)
> + [[handoff-2026-06-25-rgh19-deterministic-doc-knowledge-completeness-gate|RGH-19]]
> (doc/knowledge-completeness checks).
>
> **Why this exists:** `client-schema-sync` is a mature skill handoff ONLY because the operator
> pushed the chats to document for repeatability at the end. Without that push, nothing would be
> automatable. This makes productization-readiness a **gated requirement** for qualifying runs — so
> every high-value repeatable run ends already holding the materials for its own skill.

---

## A. Tier classifier (run-start)

The producer proposes the run's tier at spawn; the **reviewer + operator confirm**.
A producer proposing the wrong tier is itself a reviewer catch.

### The three tiers

| Tier | When | What applies | Examples |
|---|---|---|---|
| **Productize** | Repeatable + high-value + generalizable. Done for >1 client, or recurringly, or buildable into a skill/tool. | Full Productization-Readiness DoD (B1–B6) + all existing gates + capability-gap register check. | Client work, audits, content production, schema sync, page builds, SEO workflows. |
| **Capture-only** | One-off but informative. A tricky debug, a real decision, a scoping chat. | Existing Knowledge Capture Protocol (patterns/lessons) only. No B1–B6 requirement. | Architecture decisions, incident debugging, strategic planning. |
| **Throwaway** | Exploratory / scoping / conversation. | Nothing beyond the existing review gate. | Quick questions, experiments, prototyping. |

### Recording the tier

The tier MUST be recorded in:
1. The run's **execution log** (first entry, before work starts): `**Tier:** Productize | Capture-only | Throwaway`
2. The run's **tracker row** (Active table Notes column): `Tier: Productize`
3. The run's **firing-tracker row** (when the reviewer authors it): `Tier` column.
4. The **event-log spawn row**: include the tier.

### Tier confirmation flow

1. **Producer proposes** at spawn (in the execution log + tracker row).
2. **Reviewer verifies** at review time: does the tier match the work? A Productize-tier run that
   actually built a one-off debug should be downgraded; a Capture-only run that built a reusable
   engine should be upgraded. Tier mismatch is a reviewer catch (severity: Process).
3. **Operator confirms** (implicit via the review PASS, or explicit if the reviewer flags a mismatch).

### Default tier when not specified

If a producer does not propose a tier, the reviewer applies the default:
- Any run that writes code, builds pages, creates a skill, or produces a workflow → **Productize**.
- Any run that makes architectural decisions or debugs → **Capture-only**.
- Exploratory conversations → **Throwaway**.

---

## B. Productization-Readiness DoD (Full) — for Productize-tier runs

A Productize-tier run **cannot close** until it has produced ALL six items. Each item has a
machine-checkable signal that RGH-18/19 will enforce as code.

### B1. Repeatable steps

**What:** The exact procedure, captured *during* the run (not reconstructed at close).

**Where it lives:** Execution log (`repos/<venture>/.kos/execution-logs/` or
`second-brain/_meta/handoffs/<project>/execution-logs/`). If generalizable across projects, also
in an SOP at `second-brain/05_shared-intelligence/` or skill SKILL.md.

**Machine-checkable signal (for RGH-19):**
- Execution log exists + has substantive content (OC-1 already checks this).
- Execution log contains a `## Steps` or `## Procedure` or `## What Happened` section with ≥3
  numbered or bulleted items.
- If a SKILL.md was produced, it contains a `## How to run` or `## Steps` section.

### B2. Engine / config split

**What:** Explicitly name what is client/instance-specific (→ config) vs the reusable engine.

**Where it lives:** Execution log under a `## Engine / config split` section, OR in the
SKILL.md's config table / architecture section.

**Machine-checkable signal (for RGH-19):**
- Grep the execution log + SKILL.md for one of: `engine/config`, `Engine / config`, `config split`,
  `client-specific`, `instance-specific`, `reusable engine`.
- At least one config field is named.

### B3. Config schema

**What:** The fields a new instance/client needs to run it. Explicit types and examples.

**Where it lives:** SKILL.md config table (preferred), or execution log `## Config schema` section.

**Machine-checkable signal (for RGH-19):**
- A table or YAML/JSON block with ≥2 named fields exists in the SKILL.md or execution log.
- Each field has at least a name and a description/example.

### B4. 2nd-instance-from-config verdict

**What:** Could instance #2 run this from config alone? If not, what's missing (named).

**Where it lives:** Execution log under `## 2nd-instance verdict` or `## Duplicability`. Or in
the SKILL.md's "Proven on" section.

**Machine-checkable signal (for RGH-19):**
- Grep for `2nd-instance`, `second instance`, `duplicab`, `2nd-client`, `second client`,
  `proven on`, `non-electrician proof`, `2nd-vertical`.
- The section contains an explicit PASS/FAIL verdict or a named gap.

### B5. Safety / quality rules

**What:** The failure modes + guards (e.g., JSON_HEX_TAG, zero-cross-contamination, source-leak,
placeholder sweep). What can go wrong, and what prevents it.

**Where it lives:** Execution log `## Safety rules` section, or SKILL.md `## Safety` /
`## Quality rules` / `## Failure modes` section.

**Machine-checkable signal (for RGH-19):**
- Grep for `safety`, `failure mode`, `quality rule`, `guard`, `cross-contamination`, `leak`.
- At least one failure mode is named with its mitigation.

### B6. Skill-candidacy verdict

**What:** Is this worth productizing into a skill? Explicit yes/no with rationale. If **yes →
auto-spawn a ready skill-build handoff** so the next step is queued, not lost.

**Where it lives:** Execution log under `## Skill-candidacy verdict`.

**Machine-checkable signal (for RGH-19):**
- Grep for `skill-candidacy`, `skill candidacy`, `worth productizing`, `skill verdict`.
- The section contains an explicit `Yes` or `No`.
- If `Yes`, a handoff file is referenced or created (verifiable by `ls`).

---

## C. Deliverable manifest template (for Productize-tier runs)

Every Productize-tier run's handoff (or execution log, if no handoff) MUST include a
`## Deliverable manifest` section. This is the machine-checkable contract that RGH-18 walks
to verify completeness. It extends the existing DoD-manifest spec
([[spec-definition-of-done-manifest]]) with the B1–B6 productization items.

### Template

```markdown
## Deliverable manifest

| # | Deliverable | Path or glob | Assertion | Source | Check |
|---|---|---|---|---|---|
| 1 | Execution log with repeatable steps (B1) | repos/<venture>/.kos/execution-logs/execution-log-YYYY-MM-DD-*.md | exists + non-stub + has-steps-section | — | OC-1 + B1 |
| 2 | Engine/config split documented (B2) | (same exec log or SKILL.md) | contains-engine-config-section | — | B2 |
| 3 | Config schema (B3) | (SKILL.md or exec log) | contains-config-table-or-block | — | B3 |
| 4 | 2nd-instance verdict (B4) | (exec log or SKILL.md) | contains-duplicability-verdict | — | B4 |
| 5 | Safety/quality rules (B5) | (exec log or SKILL.md) | contains-safety-section | — | B5 |
| 6 | Skill-candidacy verdict (B6) | (exec log) | contains-skill-verdict | — | B6 |
| 7+ | [Run-specific deliverables…] | [specific paths] | [assertions per DoD-manifest spec] | [sources] | [check ids] |
```

**Rules:**
- Rows 1–6 are ALWAYS present for Productize-tier runs (they are the B1–B6 items).
- Row 7+ are the run-specific deliverables (code files, config files, skill SKILL.md, etc.),
  using the existing assertion vocabulary from [[spec-definition-of-done-manifest]].
- The reviewer + RGH-18 walk this manifest row by row. Any missing row = BLOCKING.
- The producer authors the manifest at spawn (rows 7+ may be refined during the run).

---

## D. Task-definition rules (stop the silent-substitution class)

These rules are reviewer-checkable and wired into the omission-check registry (see OC-17, OC-18 below).

### D1. Define tasks by the operator's decision-need, not the literal artifact

The deliverable must answer the operator's **decision** ("should I invest in more pages?" "why
aren't my pages indexed?"), not just produce the **artifact** (a count, a spreadsheet). The
reviewer checks: does the deliverable answer the decision, or just produce the artifact?

**Seed incident:** [A2] indexation — the operator needed "tell me if my pages are healthy and
what's blocking them"; the run delivered a count + `site:` check, not per-page reasons.

### D2. A capability gap that forces a weaker method is a headline blocker

When a run uses a weaker/less-accurate method because the strong one is blocked (missing API
scope, missing credential, tool limitation), this MUST be:
1. **Registered** in `[[_capability-gap-register]]` as a CG-### entry.
2. **Surfaced in the headline / close summary** — never only a buried "limitations" note.
3. The reviewer checks: was the substitution surfaced? Is there a CG entry?

**Seed incident:** [A2] — URL-Inspection API blocked by auth scope → fell back to
impressions + `site:` → filed as a buried "Method/limitation" note → operator never learned
the answer was unreliable until post-hoc review.

---

## E. Gate extension (hard-block) — what RGH-18/19 must enforce

> **PR-1 defines the WHAT. RGH-18/19 build the CODE.**

### E1. RGH-18 build-correctness checks (for Productize-tier runs)

The existing RGH-18 checks (completeness diff, all-dirty-file sweep, staging-reality audit)
are extended with:
- **Deliverable-manifest walk:** for each row in `## Deliverable manifest`, verify the path
  exists and the assertion passes. Any failure = BLOCKING.
- **CG-register check:** if the run's execution log mentions a weaker method / substitution /
  limitation / workaround, verify a matching CG-### entry exists in
  `_meta/handoffs/_capability-gap-register.md`. Missing entry = BLOCKING.

### E2. RGH-19 doc/knowledge-completeness checks (for Productize-tier runs)

The existing RGH-19 checks are extended with:
- **B1–B6 presence checks:** grep for each DoD item's machine-checkable signal (listed in §B
  above) in the execution log + SKILL.md. Any missing = BLOCKING for Productize-tier.
- **Task-definition check (D1):** the execution log's opening section names the operator's
  decision-need (not just the artifact). Grep for `decision-need`, `operator needs`,
  `why this matters`, or a `## Purpose` / `## Decision this answers` section. Missing = WARN
  (not BLOCKING — judgment-dependent).
- **CG-headline check (D2):** if a CG entry was registered this run, the close summary /
  execution log headline mentions it. Grep the first 20 lines of the execution log + the
  event-log close row for the CG-### id. Missing = BLOCKING.

### E3. Tier-gated enforcement

| Tier | B1–B6 | Deliverable manifest | CG checks | Existing gates |
|---|---|---|---|---|
| Productize | BLOCKING | BLOCKING | BLOCKING | All |
| Capture-only | Exempt | Exempt | BLOCKING (if substitution occurred) | All |
| Throwaway | Exempt | Exempt | Exempt | All |

---

## F. Catch→check ratchet (standing rule)

**No `CR-###` of class "reviewer/gate missed X" may be marked closed** until one of:
1. It is **converted into a deterministic check** added to RGH-18 or RGH-19 (or the
   omission-check registry as a new OC-### row), OR
2. An **explicit operator-approved "can't-be-deterministic" exception** is recorded in the
   CR row's "What would close it" column with the reason.

### Where this is wired

- **Gate close protocol** (`_handoff-run-standard.md` closing protocol): before marking a
  CR as "Applied" or "Resolved," verify it meets one of the two conditions above.
- **Independent reviewer mandate** (`independent-reviewer-mandate.md`): the reviewer checks
  that any CR being closed this run has a matching deterministic check or an operator exception.
- **Catch register** (`_review-gate-catch-register.md`): the "What would close it" column
  must name the specific check (OC-###, RGH-18 check name, or RGH-19 check name) or
  "operator exception: <reason>."

### Why this exists

Without the ratchet, the same miss recurs: CR-108 (dropped page), CR-109 (cross-client leak
in source data), CR-110 (staging mismatch) — all found by operator QC, not the gate. The
ratchet converts each miss into a permanent check, so coverage grows every run instead of
the same defect class recurring.

---

## G. Integration points (where this spec is consumed)

| Consumer | What it reads | How |
|---|---|---|
| RGH-18 (build-correctness gate) | Deliverable manifest rows + CG-register | Code walks manifest, diffs against disk |
| RGH-19 (doc-completeness gate) | B1–B6 signals + D1/D2 signals | Code greps execution log + SKILL.md |
| Independent reviewer mandate | Tier confirmation + D1/D2 + catch→check ratchet | Reviewer reads spec, checks manually |
| Omission-check registry | OC-18 (D1) + OC-19 (D2) + OC-20 (B1–B6 completeness) | Deterministic checks (RGH-19 code) |
| `_handoff-run-standard.md` | Tier recording + catch→check rule | Instruction-level (producer reads at spawn) |
| CLAUDE.md | Tier classifier + Productize-DoD reference | Instruction-level (all sessions read) |

---

## H. New omission-check rows (to be added to the registry)

### OC-18: Task-definition — decision-need alignment (D1)

**Check:** The execution log's opening names the operator's decision-need, and the
deliverable answers it (not just produces an artifact).

**Procedure:**
1. Read the execution log's first section / purpose statement.
2. Read the originating handoff's purpose / "why" section.
3. Verify the deliverable addresses the decision-need, not just the literal artifact.
4. Missing purpose statement → WARN. Deliverable that answers only the artifact → WARN.

**Severity:** WARN (judgment-dependent; upgraded to BLOCKING when a capability gap forced a
weaker method — see OC-19).

**Seed incident:** [A2] indexation — operator's decision-need was "why aren't pages indexed";
deliverable was a count + `site:` check that couldn't answer the question.

### OC-19: Capability-gap surfacing (D2)

**Check:** Any weaker-method substitution is registered as a CG-### entry AND surfaced in
the headline / close summary.

**Procedure:**
1. Grep execution log for substitution language: `"weaker"`, `"fallback"`, `"workaround"`,
   `"limitation"`, `"blocked"`, `"couldn't use"`, `"not available"`, `"insufficient scope"`,
   `"missing credential"`, `"API not accessible"`.
2. For each hit, verify a matching CG-### entry exists in `_capability-gap-register.md`.
3. Verify the CG-### id appears in the first 20 lines of the execution log OR in the
   event-log close row.
4. Missing CG entry → BLOCKING. Missing headline surfacing → BLOCKING.

**Seed incident:** [A2] — URL-Inspection API auth-scope gap buried as a limitation note.

### OC-20: Productization-DoD completeness (B1–B6) — Productize-tier only

**Check:** A Productize-tier run has all six DoD items present and substantive.

**Procedure:**
1. Confirm run tier = Productize (from execution log or tracker row).
2. For each B1–B6 item, run the machine-checkable signal grep (listed in §B above).
3. Any missing item → BLOCKING.
4. Non-Productize tiers → skip (report `skipped (tier: Capture-only/Throwaway)`).

**Seed incident:** [PR-1] founding — every prior Productize-class run lacked one or more of
B2–B6 until the operator manually pushed for them.

---

## See also

- [[spec-definition-of-done-manifest]] — the existing DoD-manifest spec this extends
- [[omission-check-registry]] — where OC-18/19/20 are registered
- [[independent-reviewer-mandate]] — where tier confirmation + D1/D2 + ratchet are wired
- [[_capability-gap-register]] — the CG-### register (sibling to catch register)
- [[sprint-2026-06-24-automatable-by-default-foundation]] — the sprint this anchors
- [[handoff-2026-06-25-rgh18-deterministic-build-correctness-gate]] — builds E1 as code
- [[handoff-2026-06-25-rgh19-deterministic-doc-knowledge-completeness-gate]] — builds E2 as code
