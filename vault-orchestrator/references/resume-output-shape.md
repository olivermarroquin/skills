# RESUME — output shape

Mode 5 produces a four-part plain-language report that reads top-to-bottom like a colleague catching the operator up on a specific project. This reference defines the shape, the voice, the minimum content per section, and the operator-confirmation surfaces.

## What Mode 5 produces

```
RESUME REPORT — <project name> (<YYYY-MM-DD>)

# Project state summary

# Available next-wave handoffs

# Cross-project unblockers

# Decomposition diagram

# Stale-state reconciliations (operator confirmation requested)

# What I read to produce this
```

Six sections. Sections 1-4 are the canonical 4-part output the v1.2 handoff names. Section 5 is the stale-state surface added at Gate 1 operator refinement (transparency over magic). Section 6 is a brief audit trail of what sources Mode 5 read.

## Cross-section voice rules

Same plain-language voice as SURVEY / NEXT-MOVES / PROVISION reports. Per [[plain-language-discipline]]:

- H1 / H2 headings stay as named below; don't paraphrase for cuteness
- Each section opens with a one-sentence framing of what's in it
- Plain prose paragraphs as the synthesis; bullets fine for naming rows
- Jargon glossed inline on first use (`wave_log` → "the state file's append-only per-wave summary")
- Wikilinks preserved per knowledge-os conventions
- Zero invented data — every claim cites the source

## Section 1 — Project state summary

**What lives here.** A plain-language paragraph naming where the project is right now: what wave is in flight (or whether no wave is active), what the last closed wave shipped, what the next planned wave is, and any blockers the project itself has flagged.

**Minimum content.**

- Project slug + canonical project name (e.g., "s-and-h-contracting (S&H Contracting Unlimited)")
- The state-file `updated_at` timestamp + a brief comment on freshness (e.g., "state file last wrote 2026-06-01 16:30 UTC; ~1 day old")
- Current wave: `wave_id` + scope summary + status (in-progress / pending / null)
- Last closed wave: `wave_id` + one-paragraph summary from `wave_log` + closed date
- Blockers from `state_file.blocked_on[]` — name each, with reconciliation pointer if applicable (e.g., "blocker X — see Section 5 reconciliation 1")
- Active operator-decisions-pending entries (`state_file.operator_decisions_pending[]` if present)

**Example shape:**

```
S&H Contracting (`s-and-h-contracting`) is mid-Step-2 research. The state file
last wrote 2026-06-01 16:30 UTC (~1 day old). Wave A1 (1 service brief +
spot-check) closed 2026-06-01 with both blockers spawned outward (v1.1 SKILL
rewrite + API keys wiring). No wave is currently in flight — wave A2 is the
next planned wave but is recorded as blocked in the state file. See Section 5
for the reconciliation that fires here.
```

## Section 2 — Available next-wave handoffs

**What lives here.** The list of `planned_remaining_waves[]` entries whose dependencies are all cleared, plus any matching handoff files Mode 5 found via `client:` frontmatter grep.

**Minimum content.**

- For each planned wave whose `blocks_on[]` is empty OR whose blockers are all cleared: name `wave_id`, scope, estimated hours, the matching handoff file (if any), and whether the handoff is currently in the master tracker's Ready-to-spawn / Tier-2-queued / Tier-3-queued sections
- Distinguish "next wave Mode 5 thinks is ready" from "operator-named handoff already in Ready-to-spawn" — they may not match if the state file's `planned_remaining_waves[]` was last edited before the handoff was promoted
- Order: tracker-Ready waves first (those have a written handoff), then state-file-ready waves (those need a handoff drafted via PROVISION)

**Example shape:**

```
Wave A2 — 2 service briefs (ev-charger-installation + light-fixture-installation),
~1.5h. Handoff file: [[handoff-2026-06-01-s-and-h-wave-a2-service-briefs]] —
currently in master tracker Ready-to-spawn. Both blockers cleared 2026-06-02
(see Section 5).

After A2, waves A3-A6 are queued in the state file but no handoff files exist yet.
Operator may want to trigger PROVISION on those to draft handoffs once A2 ships.
```

**The Mode 5 → Mode 3 PROVISION chain.** When a wave is state-file-ready but has no handoff file, the operator's natural next move is "provision wave-X" — which invokes Mode 3 PROVISION to draft the handoff. Mode 5 names this chain explicitly:

```
Chain note: wave A3 is state-file-ready but no handoff exists. To draft one,
say "provision wave-A3 for s-and-h-contracting" and Mode 3 will decompose +
draft + queue the handoff.
```

## Section 3 — Cross-project unblockers

**What lives here.** Sibling-project handoffs that, if landed, would unblock this project's queued waves. Per the Gate 1 refinement, this is a FILTERED SUBSET of the vault-wide cross-project heuristics — Mode 5 only surfaces signals whose connection to the named project is direct.

**Filter rule (mandatory).** A cross-project signal qualifies for Section 3 only if one of these holds:

- The signal's source handoff has `client:` frontmatter matching the named project's slug, OR
- The signal explicitly names the project's slug (e.g., "EV Electric pages 06-12" naming `ev-electric-services`), OR
- A wave in `state_file.planned_remaining_waves[]` has `blocks_on:` pointing to the source handoff filename

Don't surface vault-wide signals that don't pass this filter. SURVEY's Section 9 is the place for those.

**Minimum content.**

- For each qualifying signal: name the source handoff filename, what it ships, current status (queued / in-flight / ready-to-spawn), and which of this project's waves it would unblock
- If zero signals qualify, say so explicitly ("no cross-project unblockers — this project's queued waves don't depend on sibling handoffs") rather than skipping the section

**Example shape:**

```
No cross-project unblockers fire for S&H today. The 5 spawned-from-wave-A1
handoffs are either consumed (v1.1 SKILL rewrite + API keys + event log
Phase 1) or in-flight (vault-orchestrator v1.2 Mode 5 — this chat). Wave A2
is unblocked already; the remaining vault-orchestrator work doesn't block S&H
A2-A6.
```

## Section 4 — Decomposition diagram

**What lives here.** A text rendering of the project's wave dependency graph, showing closed / in-progress / ready / blocked status for each wave. Detailed rendering rules live in [[resume-decomposition-diagram-text]].

**Minimum content.**

- One ASCII diagram for the project's waves
- Status markers: `[✓]` closed, `[~]` in-progress, `[•]` ready, `[✗]` blocked (with blocker name parenthesized)
- Cycle detection — if a circular dependency is detected, render a `⚠️ CIRCULAR DEPENDENCY DETECTED` banner above the diagram + flag the offending wave pair

**Example shape:**

```
S&H Contracting wave decomposition:

[✓] wave-A1 — emergency-electrician service brief + spot-check
     ↓
[•] wave-A2 — ev-charger + light-fixture service briefs
     ↓
[•] wave-A3 — Woodbridge + Lake Ridge + Dale City city briefs
     ↓
[•] wave-A4 — Manassas + Lorton + Springfield city briefs
     ↓
[•] wave-A5 — Burke + Alexandria + Stafford city briefs
     ↓
[•] wave-A6 — 4 Woodbridge intersection briefs
```

## Section 5 — Stale-state reconciliations (operator confirmation requested)

**What lives here.** Every reconciliation Mode 5 applied while reading inputs. Per Gate 1 refinement, this surface is operator-facing — the operator sees Mode 5's reasoning, not just its output.

**Minimum content.**

- One subsection per reconciliation, numbered
- For each: name the source contradiction (state-file-says-X vs event-log-says-Y), Mode 5's inferred resolution, and the operator confirmation prompt
- If zero reconciliations fire, the section reads "no stale-state contradictions detected — state file is consistent with the event log and master tracker"

**Detection rules.** Per [[resume-input-sources]] § "Stale-state reconciliation rules" (numbered 1-5). Each detection rule that fires gets its own subsection here.

**Example shape (S&H wave A1 — both blockers fire detection rule 1):**

```
Reconciliation 1 — blocker apparently un-cleared, handoff consumed

State file `blocked_on[0]` says: "client-seo-onboarding v1.1 SKILL.md rewrite —
wave A2+ should run through the corrected orchestrator"

Event log row 2026-06-02 14:56:15 says: `client-seo-onboarding v1.0 → v1.1`
shipped (chat client-seo-onboarding-v1.1-rewrite-202606021400 consumed the
handoff at 2026-06-02 15:03:28).

Mode 5 inferred: this blocker is effectively cleared. The state file just
hasn't been updated yet. Mode 5 treats wave A2 as unblocked on the v1.1 side.

Operator confirm: is this right? (yes / no / edit)

Reconciliation 2 — blocker apparently un-cleared, handoff consumed

State file `blocked_on[1]` says: "OpenAI/Gemini/Claude API keys wiring — §4
closure on subsequent service briefs"

Event log rows 2026-06-02 09:15 / 09:18 / 09:22 say: OpenAI + Gemini + Claude
API keys all wired into the tier-3 carve-out by chat
api-keys-wiring-202606020900.

Mode 5 inferred: this blocker is effectively cleared. Wave A2 is unblocked on
the API-keys side as well.

Operator confirm: is this right? (yes / no / edit)
```

## Section 6 — What I read to produce this

**What lives here.** A brief audit trail of what sources Mode 5 read, in read order. Keeps the report self-describing — the operator can scan and see if anything that should have been read was missed.

**Minimum content.**

- Numbered list, one entry per source read
- For each: source path, what was extracted, freshness signal
- If a source was missing, name it explicitly (per the honest-gap-surfacing principle)

**Example shape:**

```
1. Master tracker — read pass-86 (current). 3 in-flight rows, 5 Ready, 4 Tier-2,
   6 Tier-3. S&H matches: 1 Ready row (wave A2 handoff).
2. Event log delta — read 13 rows since state file's 2026-06-01 16:30 UTC
   `updated_at`. 2 blocker-clearing events captured.
3. State file — read `_state/onboarding.json` (schema v1.0; current_wave =
   wave-A1, status closed-with-spawned-blockers).
4. Execution logs — read newest (2026-06-01 orchestrator-first-real-run).
5. Per-project chat tracker — no S&H per-project tracker exists yet (Phase 1
   convention; project predates it).
6. Handoffs naming s-and-h-contracting — 7 handoff files match the
   `client: s-and-h-contracting` grep. All accounted for in Sections 2-3.
```

## When Mode 5 emits the report

**Default:** emit as chat output. The operator reads inline.

**On `--persist`:** write to `~/workspace/second-brain/_meta/handoffs/vault-orchestrator/runs/<YYYY-MM-DD-resume-<slug>>.md`. Use minimal frontmatter:

```yaml
---
type: report
status: draft
created: <today>
updated: <today>
project: <slug>
mode: resume
tags: [report, vault-orchestrator, resume, <slug>]
---
```

Free-form fields stay single-quote-wrapped. The regex-extractor YAML check runs after the write.

**On persist, auto-invoke output-quality-loop.** Per the standing convention, emit the standard block naming the persisted report as the artifact. Spec sources are routed via `spec-routing-table.md` § "Vault-orchestrator RESUME report" — see the v1.2 additive routing entry.

## Operator confirmation flow

When Section 5 fires (one or more reconciliations), the report includes per-reconciliation `Operator confirm: ...` prompts. The operator responds inline ("yes / no / edit") and Mode 5:

- On "yes" → treats the reconciled state as truth for downstream sections (e.g., wave A2 is unblocked if both reconciliations confirm)
- On "no" → reverts to the state-file truth + re-renders the relevant sections (e.g., wave A2 stays blocked)
- On "edit" → asks one clarifying question + re-renders

Mode 5 NEVER writes a fix to the state file as part of confirmation. State file edits remain the owning skill's responsibility (e.g., `client-seo-onboarding` writes its own state file). Mode 5 just produces an accurate read.

If the operator wants Mode 5 to also propose state-file edits, that's a Mode 6 EXECUTE concern — out of scope for v1.2 Mode 5.

## Plain-language compliance — what the quality loop checks

When the persisted report is evaluated by output-quality-loop:

- Headings stay verbatim per this reference's spec
- Per-section minimum content present
- Stale-state reconciliations include operator confirmation prompts (or the section explicitly says "no reconciliations fired")
- Decomposition diagram includes status markers + cycle-detection check
- "What I read" audit names every source from [[resume-input-sources]]
- Wikilinks render correctly (no broken targets)
- Jargon glossed inline on first use
- No invented data — every claim points to a vault source

## Related

- [[SKILL]] § "Mode 5 — RESUME"
- [[resume-input-sources]] — what Mode 5 reads to produce this report
- [[resume-decomposition-diagram-text]] — diagram rendering rules
- [[plain-language-discipline]] — voice rules every orchestrator report follows
- [[survey-section-shapes]] — the section-shape pattern Mode 5 mirrors
- [[cross-project-signal-detection]] — vault-wide heuristics Mode 5's Section 3 filters
- [[../../output-quality-loop/references/spec-routing-table|output-quality-loop spec-routing]] — v1.2 additive entry for RESUME reports
