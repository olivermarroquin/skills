---
type: reference
status: active
created: 2026-06-19
updated: 2026-06-19
skill: vault-orchestrator
skill-version: 1.6
tags: [reference, vault-orchestrator, provision, existing-project, classification]
---

# Existing-project phase classification rules

When PROVISION operates on an existing (in-progress) project via `--existing-project <slug>`, it must classify every planned phase/deliverable before decomposing. This reference defines the classification rules, signal sources, and edge-case handling.

## Three-state classifier

Every phase/deliverable in the project's decomposition is classified into exactly one of:

| State | Definition | PROVISION action |
|---|---|---|
| **done** | Phase fully shipped — consumed handoff + artifacts on disk + no open items | Skip entirely. Never re-propose. |
| **partial** | Phase started but incomplete — some artifacts exist, or handoff is active/staging-complete, or execution log documents rejected run / blocker | Decompose only the remaining sub-work. State honestly: "X of Y done; remaining: Z." |
| **not-started** | Phase has no execution evidence — handoff is queued/planned, no execution logs, no artifacts | Decompose fully (same as greenfield for this phase). |

## Signal sources (read order)

Classification consumes the same six sources as Mode 5 RESUME (see [[resume-input-sources]]), plus two additional checks:

1. **Handoff frontmatter `status:`** — the primary signal.
   - `consumed` / `completed` / `closed` → **done** (unless execution log documents rejection — then **partial**)
   - `active` / `active-with-*` / `staging-complete` → **partial**
   - `queued` / `ready-to-spawn` / `ready` / `planned` → **not-started** (unless execution logs exist for this phase)
   - `superseded` → **done** (the work was replaced, not remaining)

2. **`consumed:` date in frontmatter** — presence confirms done; absence with `status: consumed` is a data-quality warning (surface it, still classify as done).

3. **`_recently-closed` tracker rows** — if a chat for this phase appears in recently-closed with a shipped outcome, classify as **done** even if the handoff frontmatter hasn't been flipped yet (stale-state reconciliation, same as RESUME Rule 2).

4. **Execution logs** — `execution-log-*` files referencing this phase's slug or handoff filename.
   - Execution log exists + documents completion → **done**
   - Execution log exists + documents rejection/partial/blocker → **partial** (read the log to scope what remains)
   - No execution log → supports **not-started** (but not dispositive alone — check other signals)

5. **On-disk artifacts** — `ls`/grep for the deliverables the phase was supposed to produce.
   - All deliverables exist → supports **done**
   - Some deliverables exist → supports **partial** (name which are present and which are missing)
   - No deliverables exist → supports **not-started**

6. **Master tracker rows** — in-flight / ready / queued rows naming this phase.
   - In-flight row → **partial** (work is actively happening)
   - Ready row → **not-started** (queued but not started)
   - No row (and no recently-closed row) → ambiguous; fall through to other signals

7. **State file** (if project uses one) — `waves[]`, `wave_log[]`, `planned_remaining_waves[]`.
   - Wave closed with PASS verdicts → **done**
   - Wave in-progress → **partial**
   - Wave in planned_remaining → **not-started**

8. **`depends-on:` array in handoff frontmatter** — if all dependencies are consumed/done, the phase is unblocked. If some dependencies are not-done, the phase is blocked (still not-started, but flag the blocker).

## Conflict resolution between signals

Signals may disagree. Resolution priority (highest wins):

1. **`_recently-closed` + execution log with shipped outcome** → done (overrides stale handoff frontmatter)
2. **Execution log documenting rejection** → partial (overrides `consumed` status if the rejection led to a redo — check for a `-R2` or successor handoff)
3. **Handoff frontmatter `status: consumed`** → done
4. **On-disk artifacts fully present** → done (even if handoff frontmatter is stale)
5. **Handoff frontmatter `status: queued` + no execution logs + no artifacts** → not-started

When signals genuinely conflict (e.g., handoff says consumed but no artifacts on disk), surface the conflict in the classification table with a `⚠️` marker and let the operator resolve at the approval gate. Do not silently pick a side.

If a README or body text states "superseded by X" but the handoff's frontmatter `status:` is not `superseded` (e.g., still `staging-complete` or `active`), surface a `⚠️` conflict marker and recommend the operator update the frontmatter to match the body-text intent. Classify based on the body-text signal (superseded → done) but flag the stale frontmatter.

## Classification output shape

The classifier produces a table included in the PROVISION proposal:

```
Phase classification (existing-project decomposition):

| Phase | Handoff | Status signal | Artifacts on disk | Classification | Remaining work |
|---|---|---|---|---|---|
| [WF-1] Planning | consumed 06-12 | execution-log exists, shipped | decisions locked | ✅ done | — |
| [WF-4] EV build | staging-complete | run 1 rejected, R2 ready | baseline pages on disk | 🟡 partial | Full redo via WF-4-R2 (content parity + architecture) |
| [WF-8] Render-layer | queued | no execution log | no artifacts | ⬜ not-started | Full phase |
| ... | ... | ... | ... | ... | ... |
```

The "Remaining work" column becomes the input to DECOMPOSE for partial and not-started phases. Done phases are excluded from DECOMPOSE entirely.

## Partial-phase decomposition

For **partial** phases, PROVISION must scope the remaining work honestly:

1. Read the execution log to understand what was completed and what failed/was deferred.
2. Read any rejection notes, blocker descriptions, or "next session should start with" sections.
3. If a successor handoff exists (e.g., `-R2` redo), treat the successor as the remaining-work specification — do not re-derive from scratch.
4. If no successor exists, derive the remaining scope from: (original handoff deliverables) minus (artifacts verified on disk).
5. State the partial honestly in the proposal: "Phase X is 60% complete. Completed: A, B. Remaining: C, D. Blocker: E."

## Collision awareness

Before drafting any handoff for remaining work, check:

1. **Existing handoffs** — grep `_meta/handoffs/` for handoffs already covering this phase (including `-R2` redos, follow-up handoffs, etc.). If one exists and isn't consumed, do NOT draft a duplicate — reference the existing handoff instead.
2. **In-flight chats** — check the master tracker's Active section. If a chat is actively working on this phase, do NOT draft a competing handoff.
3. **Spawn queue** — check `_spawn-queue.md` for rows already queued for this phase.

For each collision detected, flag it in the proposal's conflict table with the action: "existing handoff covers this — no new draft needed" or "in-flight chat active — defer until chat closes."

## Edge cases

- **Project with no handoff files (tracker-only).** Classification falls back to tracker rows + execution logs + on-disk artifacts. Surface: "no separate handoff files for this project — classifying from tracker + artifacts only."
- **Project with no state file.** Classification skips signal source 7. Surface advisory per RESUME's convention.
- **Phase with multiple handoff files (original + redo).** Classify from the most recent/active handoff. The original's `consumed` status + rejection log = partial; the redo's status determines what remains.
- **Phase not in any handoff (planned in README/roadmap only).** Classify as not-started. Draft a new handoff for it.
- **Superseded phases.** Classify as done (superseded = work replaced, not remaining). Do not decompose.

## Related

- [[resume-input-sources]] — the six-source read that feeds classification
- [[SKILL]] § "Mode 3 — PROVISION" — the parent mode
- [[edit-zone-conflict-detection]] — reused for collision awareness
- [[spawn-queue-shape]] — where remaining-work rows land after approval
