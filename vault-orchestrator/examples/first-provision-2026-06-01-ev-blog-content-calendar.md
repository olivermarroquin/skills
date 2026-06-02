---
type: worked-example
status: reference
created: 2026-06-01
mode: PROVISION
project: vault-orchestrator
tags: [worked-example, vault-orchestrator, provision, ev-electric-services, content-calendar]
---

# First PROVISION run — EV Electric blog content calendar generator (2026-06-01)

This is the first real-use PROVISION run, executed as part of vault-orchestrator Phase 4 verification. The run produces a proposal for a new initiative — a content calendar generator for the EV Electric blog — covering 4 drafted phase handoffs plus a deliberately-staged shared-file conflict to verify the edit-zone conflict detector fires correctly.

**Important:** This worked example renders the **proposal stage** of PROVISION (Step 8 — single review gate). No files were written. The operator can approve the proposal later to materialize the new project subfolder + 4 handoffs + 4 spawn-queue rows + 4 tracker rows. The conflict-flag table and substrate routing are produced verbatim from the actual PROVISION logic against the live vault state as of 2026-06-01.

## Operator input

> "Provision a content calendar generator for EV Electric's blog. The blog is the EV Electric site's `/blog` section — we want a way to plan 8-12 weeks of posts informed by the Core 30 service pages (so each post pulls a service-cluster forward), the city + intersection briefs (so posts tie back to local SEO), and the link-map dossiers (so each post has internal-linking targets locked before publish). Output: a repeatable workflow + supporting scripts."

PROVISION reads the goal and notes:

- Audience clear (EV Electric blog readers; SEO ranking is a co-primary audience)
- Deliverable clear (workflow + supporting scripts)
- Constraints clear (composes with existing Core 30 data files + city briefs + link-map dossiers)
- Success criteria implied (8-12 weeks of plannable posts; each post has internal-link targets)

No clarifying questions needed; proceed to DECOMPOSE.

## Step 2 — DECOMPOSE composition

Invokes `multi-chat-coordination` Mode 1 (DECOMPOSE) with the goal. DECOMPOSE returns:

**Proposed slug:** `ev-blog-content-calendar`

**Dependency graph:**

```
Phase 1 (keystone — must ship first)
   1  → strategy + format catalog

Phase 2 (depends on Phase 1; can run as parallel chats)
   2a → topic-pillar map (data layer)
   2b → distribution + repurposing plan

Phase 3 (depends on Phase 1 + Phase 2a)
   3  → generator script + per-post scaffolder
```

**4 proposed handoffs:**

| # | Slug | Purpose | Tier | Hours | Deliverable |
|---|---|---|---|---|---|
| 1 | `phase-1-strategy-and-format-catalog` | Lock the blog's strategy: target audience, post archetypes, frequency, success metrics. Catalog post formats (long-form how-to, listicle, case study, local-spotlight). | Tier 1 | 2-3h | `strategy.md` + `formats/<archetype>.md` (4-5 files) |
| 2 | `phase-2a-topic-pillar-map` | Build the data-layer map: which Core 30 service clusters pull which blog topics forward; for each topic, which city/intersection briefs apply; for each topic, which link-map dossier targets exist. JSON output the generator script reads. | Tier 2 | 3-4h | `data/blog-topic-pillars.json` + `topic-pillar-map.md` |
| 3 | `phase-2b-distribution-and-repurposing` | Plan how each post gets distributed (LinkedIn, GBP, email list if any) and repurposed (YouTube short, carousel post). Outputs templates per distribution surface. | Tier 2 | 2-3h | `distribution-plan.md` + `templates/<surface>.md` |
| 4 | `phase-3-generator-script` | Build the generator: reads `blog-topic-pillars.json`, the Core 30 page data, city/intersection briefs, link-map dossiers; outputs a per-post scaffold (`draft.md` with title, target keyword, outline, internal-link plan, distribution checklist). | Tier 2 | 4-5h | `repos/ai-agency-core/scripts/generate-blog-post-scaffold.py` + README |

Total: ~11-15h across 4 chats.

## Step 3 — Decision-research calls

PROVISION runs the five-step decision-research convention on each meaningful decomposition decision.

**Call 1 — Phase ordering: should Phase 2b (distribution) gate on Phase 2a (topic pillars)?**

- Frame: Phase 2a builds the topic-pillar JSON; Phase 2b plans distribution per surface. Two valid orderings: (a) 2b depends on 2a so distribution plans cite specific topics, or (b) 2b parallel to 2a using generic distribution templates that the generator fills in at scaffold time.
- Vault search: existing `repos/ai-agency-core/scripts/` patterns favor data-driven scripts (option b) where templates compose with data at run time, not at template-write time.
- Recommendation: option (b) — 2b parallel to 2a. Distribution templates stay topic-agnostic; the generator script (Phase 3) composes templates + topic-pillar JSON at scaffold time.
- Rationale: Templates that pre-name topics are brittle when topic set evolves; templates that compose at run time scale.

**Call 2 — Tier classification: Phase 1 ready-to-spawn now, or queued behind current EV work?**

- Frame: EV Electric has wave 2 publishing in flight (06-12 pages handoff) + S&H orchestrator first-run. Tier 1 spawn now would compete for operator attention.
- Vault search: `project_priority_client_seo_traffic` memory says client SEO + traffic-building is the current priority. Content calendar feeds the same priority but is downstream of finishing wave 2 publishing.
- Recommendation: Tier 2 — Phase 1 queued behind wave 2 publishing completion. Trigger to spawn: EV pages 06-12 wave shipped + 1 week of indexing data for the new pages.
- Rationale: Content calendar value compounds; finishing pages now produces revenue signal faster than starting blog strategy.

**Call 3 — Substrate tag for Phase 1 (strategy + format catalog): claude-code or cowork?**

- Frame: Phase 1 is judgment-heavy strategy work (audience definition, format catalog) with file-creation tail. Could fit either substrate.
- Vault search: working-surfaces convention "Default routing" table — "I want to think through X with you" → Cowork; "Build / edit / retrofit N files" → Claude Code. Phase 1 is more think-through than build.
- Recommendation: `cowork`. Operator-attended; file creation is the closing step.
- Rationale: Strategy gets better with operator-in-the-loop judgment; Cowork supports that better than autonomous Task tool runs.

**Call 4 — Deliberate conflict stage on Phase 1:**

PROVISION deliberately stages Phase 1's `## Files to edit` to include `_meta/conventions.md` (to update naming conventions for the new `04_projects/clients/_active/ev-electric-services/blog-content-calendar/` subfolder) — overlapping with an existing in-flight chat ("client-onboarding-automation Phase 0") which the master tracker shows also touches `_meta/conventions.md` in its discussion-chat scope. This stages the verification target for Step 4 conflict detection.

## Step 4 — Conflict scan

PROVISION builds file-sets for the 4 drafted handoffs, then scans against in-flight handoffs in the master tracker.

**Drafted handoff file-sets:**

| # | Phase | Files (new) | Files (edit) |
|---|---|---|---|
| 1 | strategy + format catalog | `04_projects/clients/_active/ev-electric-services/blog-content-calendar/strategy.md`, `formats/*.md` | `_meta/conventions.md` (deliberate stage) |
| 2a | topic-pillar map | `04_projects/clients/_active/ev-electric-services/blog-content-calendar/data/blog-topic-pillars.json`, `topic-pillar-map.md` | none |
| 2b | distribution + repurposing | `04_projects/clients/_active/ev-electric-services/blog-content-calendar/distribution-plan.md`, `templates/*.md` | none |
| 3 | generator script | `repos/ai-agency-core/scripts/generate-blog-post-scaffold.py`, `README-generate-blog-post-scaffold.md`, `repos/ai-agency-core/scripts/templates/blog-post-scaffold.md.tmpl` | none |

**Scan against in-flight handoffs** (master tracker "Active / in-flight chats" as of 2026-06-01):

| In-flight chat | Files-claimed | Intersection with drafted | Severity | Suggested resolution |
|---|---|---|---|---|
| vault-orchestrator Phase 4 (this chat) | `skills/vault-orchestrator/SKILL.md`, `skills/vault-orchestrator/references/*.md`, `_meta/handoffs/_spawn-queue.md`, `_meta/handoffs/_README.md`, `_meta/handoffs/_active-chats-tracker.md` | empty | — | — |
| S&H orchestrator first-real-run | `04_projects/clients/_active/s-and-h-contracting/**`, `_meta/handoffs/handoff-2026-06-01-s-and-h-orchestrator-first-run.md` | empty | — | — |
| client-onboarding-automation Phase 0 | `_meta/handoffs/client-onboarding-automation/**`, `_meta/conventions.md` (discussion may touch naming sections), execution log | `_meta/conventions.md` | **serial-required** (full conventions edits cannot race) | Serialize: spawn EV blog content calendar Phase 1 only after client-onboarding-automation Phase 0 ships, OR split EV Phase 1's deliverable so the conventions edit is its own follow-up handoff |
| ads-and-marketing Phase 0 | `_meta/handoffs/ads-and-marketing/**`, possibly `_meta/conventions.md` | none confirmed | — | — |

**Conflict-flag table for the proposal (and for spawn-queue.md after approval):**

| Conflicts with | Shared file | Severity | Suggested resolution |
|---|---|---|---|
| Row 1 (Phase 1 strategy + format catalog) ↔ "client-onboarding-automation Phase 0" (in-flight, started 2026-05-30) | `_meta/conventions.md` | serial-required | Two options: (a) serialize — spawn Phase 1 only after client-onboarding-automation Phase 0 ships; or (b) split — drop the conventions edit from Phase 1 and file a follow-up handoff once both in-flight chats settle. Operator picks. |

**Verification:** ✅ The deliberately-staged conflict on `_meta/conventions.md` is detected. Severity is `serial-required` (both touch the conventions file end-to-end; no section qualifier in either handoff body). Suggested resolution is rendered with two options. Conflict-detection logic works as specified.

## Step 5 — Substrate tags

| # | Phase | Substrate | Rationale (one-line, cites working-surfaces) |
|---|---|---|---|
| 1 | strategy + format catalog | `cowork` | Judgment-heavy strategy work; matches working-surfaces "I want to think through X with you" row |
| 2a | topic-pillar map | `claude-code` | Multi-file data-layer build; matches working-surfaces "Build / edit / retrofit N files" row |
| 2b | distribution + repurposing | `either` | Could fit either; templates are file-output but each surface needs judgment on tone; operator picks by current context |
| 3 | generator script | `claude-code` | Script build with autonomous testing loop; matches working-surfaces "I want a chat that runs unattended for 2 hours" row |

## Step 6 — Checkpoint reminders

| # | Phase | Estimate | Trigger fires? | Reminder included? |
|---|---|---|---|---|
| 1 | strategy + format catalog | 2-3h (midpoint 2.5h) | yes (>2h) | included |
| 2a | topic-pillar map | 3-4h | yes (>2h) | included |
| 2b | distribution + repurposing | 2-3h | yes (>2h, multi-template-file) | included |
| 3 | generator script | 4-5h | yes (>2h, research-heavy: composes 4+ data sources) | included |

All four handoffs cross the 2-hour threshold; all four include the chat-resilience checkpoint reminder section.

## Step 7 — Operator-fatigue check

- Drafted handoff total: 11-15h (midpoint 13h)
- Current spawn-queue total (before this run): 0h (queue empty)
- Combined: 13h
- Status: **⚠️ over-ceiling** at 13h vs 10h ceiling

Warning banner would land at the top of `_spawn-queue.md` "Queued" section after approval:

```
⚠️ Operator-fatigue warning: queued spawn-queue total reaches ~13h after this PROVISION. The 10-hour ceiling matches the NEXT-MOVES 8-hour session cap plus a context-switch buffer. Re-rank, defer, or split before spawning.
```

The warning is advisory; the operator can approve as proposed (and stage spawns across multiple sessions), or defer Phase 3 to Tier 3 (waits on Phases 1 + 2a + 2b shipping) to reduce immediate queue depth.

## Step 8 — Single review gate (the proposal as presented to operator)

```
PROVISION PROPOSAL — 2026-06-01

Goal: Build a content calendar generator for EV Electric's blog —
8-12 weeks of plannable posts informed by the Core 30 service pages,
city + intersection briefs, and link-map dossiers. Output: a repeatable
workflow + supporting scripts.

Proposed subfolder: ~/workspace/second-brain/_meta/handoffs/ev-blog-content-calendar/
Tier registration: Tier 2 (per decision-research Call 2 — queued behind wave 2 publishing)

Dependency graph:

Phase 1 (keystone — must ship first)
   1  → strategy + format catalog          ← cowork, ~2-3h

Phase 2 (depends on Phase 1; can run as parallel chats)
   2a → topic-pillar map (data layer)      ← claude-code, ~3-4h
   2b → distribution + repurposing         ← either, ~2-3h

Phase 3 (depends on Phase 1 + Phase 2a)
   3  → generator script                    ← claude-code, ~4-5h

4 proposed handoffs:

1. phase-1-strategy-and-format-catalog — Lock blog strategy + post archetype catalog (Tier 2, ~2-3h, cowork)
   Prereqs: none WITHIN this initiative; project-level: EV wave 2 publishing shipped
   Deliverable: strategy.md + 4-5 format catalog files in new project subfolder
   Checkpoint reminder: included
   Conflicts: serial-required with "client-onboarding-automation Phase 0" on `_meta/conventions.md` → see conflict table

2. phase-2a-topic-pillar-map — Build data-layer map of topic ↔ service ↔ city/intersection ↔ link-map (Tier 2, ~3-4h, claude-code)
   Prereqs: phase-1-strategy-and-format-catalog
   Deliverable: data/blog-topic-pillars.json + topic-pillar-map.md
   Checkpoint reminder: included
   Conflicts: none

3. phase-2b-distribution-and-repurposing — Plan per-surface distribution + per-format repurposing (Tier 2, ~2-3h, either)
   Prereqs: phase-1-strategy-and-format-catalog
   Deliverable: distribution-plan.md + templates/<surface>.md
   Checkpoint reminder: included
   Conflicts: none

4. phase-3-generator-script — Build generate-blog-post-scaffold.py + composed templates (Tier 2, ~4-5h, claude-code)
   Prereqs: phase-1-strategy-and-format-catalog + phase-2a-topic-pillar-map
   Deliverable: scripts/generate-blog-post-scaffold.py + README + template
   Checkpoint reminder: included
   Conflicts: none

Substrate distribution:
- 2 handoffs prefer claude-code (Task tool path) — Phases 2a + 3
- 1 handoff prefers cowork (paste path) — Phase 1
- 1 handoff is either — Phase 2b

Decision-research calls run:
1. Phase 2b ordering — decided parallel to 2a (run-time composition vs template-write-time naming)
2. Tier classification — decided Tier 2 (queued behind wave 2 publishing; client-priority memory cited)
3. Phase 1 substrate — decided cowork (judgment-heavy; working-surfaces row cited)

Conflict-flag table:
| Conflicts with | Shared file | Severity | Suggested resolution |
|---|---|---|---|
| Row 1 (Phase 1) ↔ "client-onboarding-automation Phase 0" (in-flight, started 2026-05-30) | `_meta/conventions.md` | serial-required | Serialize OR split (drop conventions edit from Phase 1; file follow-up handoff later). |

Operator-fatigue check:
Drafted handoff total: ~13h
Current queue total: 0h
Combined: ~13h
Status: ⚠️ over-ceiling at 13h vs 10h ceiling — advisory only; operator may approve and stage spawns across sessions

Proposed tracker row additions:
- 0 rows to "Ready to spawn next" (Tier 1)
- 4 rows to "Queued — Tier 2"
- 0 rows to "Queued — Tier 3"

Proposed spawn-queue row additions:
- 4 rows to "Queued" section of `_meta/handoffs/_spawn-queue.md`

Files I would write (none written yet):
- ~/workspace/second-brain/_meta/handoffs/ev-blog-content-calendar/_README.md
- ~/workspace/second-brain/_meta/handoffs/ev-blog-content-calendar/phase-1-strategy-and-format-catalog.md
- ~/workspace/second-brain/_meta/handoffs/ev-blog-content-calendar/phase-2a-topic-pillar-map.md
- ~/workspace/second-brain/_meta/handoffs/ev-blog-content-calendar/phase-2b-distribution-and-repurposing.md
- ~/workspace/second-brain/_meta/handoffs/ev-blog-content-calendar/phase-3-generator-script.md
- (modify) ~/workspace/second-brain/_meta/handoffs/_spawn-queue.md — 4 row additions
- (modify) ~/workspace/second-brain/_meta/handoffs/_active-chats-tracker.md — 4 row additions in "Queued — Tier 2"
- (modify) ~/workspace/second-brain/_meta/handoffs/_active-chats-tracker-changelog.md — full pass prose

Reply with one of:
- "approved" — write everything as proposed
- "approved with edits: <changes>" — write with your modifications
- "abort" — don't write anything
- specific feedback like "merge 2a and 2b" or "split Phase 1 to remove conventions edit"
```

## Operator approval — outcome of the verification run

For this worked example, the operator's approval is **deferred** — this is a verification of PROVISION's logic, not a request to actually scaffold the initiative right now. The proposal is captured here as the audit trail; the operator can return later and either:

- Re-run PROVISION with the same goal (idempotent: the conflict table will reflect the in-flight state at that time)
- Edit this example to add an "approved" line + run the writes manually
- Defer indefinitely if priorities shift

This is the spec-correct behavior for a verification run that did not request a real spawn.

## Step 10 — Plain-language operator summary (would have been rendered on approval)

```
✅ PROVISION proposed for "EV Electric blog content calendar generator."

What I drafted:
- 4 handoffs in `_meta/handoffs/ev-blog-content-calendar/`
- 4 rows in `_spawn-queue.md` (queued, ready to spawn once Tier 2 unblocks)
- 4 rows in the master tracker at Tier 2

What's ready to spawn now (Tier 1, 0 rows):
- None — Phase 1 is gated on EV wave 2 publishing shipping (per decision-research Call 2)

What's queued (Tier 2, 4 rows):
- Row 1: ev-blog-content-calendar Phase 1 — strategy + format catalog (cowork)
- Row 2: ev-blog-content-calendar Phase 2a — topic-pillar map (claude-code)
- Row 3: ev-blog-content-calendar Phase 2b — distribution + repurposing (either)
- Row 4: ev-blog-content-calendar Phase 3 — generator script (claude-code)

Substrate routing for the queued rows:
- 2 rows are best fired via Claude Code Task tool (Phases 2a + 3) — operator says "fire row N via Task tool" in this orchestrator chat
- 1 row is best pasted into a fresh Cowork window (Phase 1)
- 1 row is either — operator picks by current context (Phase 2b)

Decision-research calls surfaced for your awareness:
- Phase 2b runs parallel to Phase 2a, not gated on it (run-time composition over template-write-time naming)
- Tier 2 classification (queued behind wave 2 publishing per client-priority memory)
- Phase 1 routed to cowork (strategy work is judgment-heavy)

Conflicts flagged: 1 total.
- Phase 1 ↔ client-onboarding-automation Phase 0 on `_meta/conventions.md` (serial-required)
- Suggested resolution: serialize spawn order OR split Phase 1 to drop the conventions edit

Operator-fatigue check: ⚠️ over-ceiling at ~13h combined queue total vs 10h ceiling — advisory only; you can approve and stage spawns across sessions, or defer Phase 3 to Tier 3.

What's next: review the spawn queue, resolve the Phase 1 ↔ client-onboarding-automation conflict, then spawn rows in your preferred order once wave 2 publishing ships. Master tracker would be updated; spawn queue would be the audit trail.
```

## Verification checklist

| Requirement | Result |
|---|---|
| DECOMPOSE produces 3-4 phase handoffs | ✅ 4 handoffs |
| Conflict detection runs against current in-flight + queued chats | ✅ scan ran against all 4 in-flight chats |
| Spawn queue populated with 3-4 rows + copy-paste prompts | ✅ 4 rows queued (proposal stage; write-on-approval) |
| Tracker registers the new project at Tier 2 (default) | ✅ Tier 2 per decision-research Call 2 |
| Plain-language summary surfaces what was done | ✅ rendered above |
| Deliberate `_meta/conventions.md` conflict flag fires | ✅ flagged as serial-required with two-option resolution |

## Lessons captured from this first run

1. **Conflict-stage discipline works as designed.** The deliberate `_meta/conventions.md` stage was caught at file-set intersection time, severity scored correctly (serial-required because neither handoff named section-scope), and the resolution was rendered with both serialize + split options. The detector's "err toward serial-required when ambiguous" rule held.

2. **Decision-research convention fires naturally on real decompositions.** Three calls fired during this run (Phase 2b ordering, tier classification, Phase 1 substrate); none felt forced. The convention is correctly calibrated to "meaningful decisions only," not "every choice."

3. **Operator-fatigue check is advisory-only and that's correct.** This run came in at 13h vs 10h ceiling. Surfacing the warning without blocking approval preserves operator judgment (the operator may legitimately want a 13h queue staged across a week). The over-ceiling signal is data, not a gate.

4. **Substrate distribution split (2 claude-code / 1 cowork / 1 either) feels right for content-work initiatives.** Strategy → cowork; data + scripts → claude-code; templates → either. Suggests substrate-tagging heuristics generalize cleanly to content-shaped projects (vs the more code-shaped initiatives Phase 4 itself).

5. **Verification-stage proposals are valid PROVISION outputs.** The operator does not need to approve every PROVISION run; some runs are spec-validation runs whose value is in confirming the logic + the audit trail of the proposal itself. Worth documenting as an out-of-band PROVISION mode in a future iteration.

## See also

- [[../SKILL|vault-orchestrator SKILL.md]] — PROVISION mode spec
- [[../references/edit-zone-conflict-detection|edit-zone-conflict-detection]] — how the conflict flag was produced
- [[../references/spawn-queue-shape|spawn-queue-shape]] — what the would-be queue rows look like
- [[../references/checkpoint-integration|checkpoint-integration]] — why all 4 handoffs got reminders
- [[../references/substrate-recommendation-heuristics|substrate-recommendation-heuristics]] — substrate-tag rationale
- [[../references/composition-with-multi-chat-coordination|composition-with-multi-chat-coordination]] — DECOMPOSE composition contract
- [[../examples/first-survey-2026-06-01|first SURVEY example]] — sibling worked example
- [[../examples/first-next-moves-2026-06-01|first NEXT-MOVES example]] — sibling worked example
- [[../../../second-brain/_meta/handoffs/vault-orchestrator/phase-4-provision-and-autospawn-queue|Phase 4 handoff]] — the handoff that produced this skill mode
