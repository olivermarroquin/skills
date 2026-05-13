# Voice Examples

Paired before/after examples from the canonical worked example (`phase-b-decisions-2026-05-11.md` → `phase-b-decisions-2026-05-11-plain.md`). Read this when you need a voice anchor — when the translation-rules file gives you the rules and you need a concrete sense of how the voice actually lands.

## Section headers + decision framings

### Decision 1 — "What's being decided"

**Original:**
> How the multi-agent system stores, retrieves, updates, and forgets memory across sessions and across agents. Specifically: **what is the substrate for memory (vault-native files / Hermes built-in pillars / external DB / hybrid), and what taxonomy organizes it (Richmond's cognitive-science / Jason's git-metaphor / Hermes file-system / Cole's wiki / something else).** Memory is the spine of the execution + coordination + capability layers; this decision composes into every downstream agent.

**Translation:**
> How does the multi-agent system remember things across sessions and across agents? Specifically: **what's the storage substrate** (vault files / Hermes built-in / external database / mix), and **what's the organizing structure** (Richmond's brain-science categories / Jason's git-style / Hermes' file structure / Cole's wiki / something else)? Memory is the spine of everything else — every agent reads and writes to it — so this matters.

What changed:
- "stores, retrieves, updates, and forgets memory" → "remember things" (one verb, plain)
- "substrate for memory" → "storage substrate" (kept "substrate" because it's load-bearing terminology; dropped "for memory" because it's redundant)
- "cognitive-science" → "brain-science" (plainer)
- "git-metaphor" → "git-style" (plainer)
- "the spine of the execution + coordination + capability layers; this decision composes into every downstream agent" → "the spine of everything else — every agent reads and writes to it — so this matters" (concrete impact, conversational rhythm)

What survived: every architectural framing (substrate / taxonomy / 4 named approaches / "spine" metaphor). No content loss.

## Option framings

### Decision 1 Option A

**Original:**
> **Option A — Vault-native + Hermes file-system taxonomy (substrate-native baseline)**
>
> Use the operator's existing Obsidian vault discipline as the memory substrate. Adopt Hermes' file-system taxonomy as the convention layer: `user.md` / `memory.md` / `agents.md` / `soul.md` / `skills/*.md` / `sessions.db`. Each agent has its own four-file persona pack (`agents.md` / `heartbeat.md` / `soul.md` / `tools.md`) per Paperclip's 4-file-per-agent pattern. Vault is source-of-truth; Hermes pillars are the runtime view onto vault files; `sessions.db` lives in Hermes (SQLite). No ETL pipeline; no embedding store; agents query via Read + grep + Dataview + Obsidian wikilink traversal.

**Translation:**
> **Option A — Use the vault, organized the Hermes way.**
>
> Your existing Obsidian vault becomes the memory store. Use Hermes' file convention (`user.md`, `memory.md`, `agents.md`, `soul.md`, `skills/*.md`, `sessions.db`). Every agent has its own 4-file pack (`agents.md`, `heartbeat.md`, `soul.md`, `tools.md`) like Paperclip does. The vault is the source of truth; Hermes' built-in features look at vault files. No ETL pipeline, no embedding store — agents just read files and grep.

What changed:
- Title: "Vault-native + Hermes file-system taxonomy (substrate-native baseline)" → "Use the vault, organized the Hermes way." (a sentence instead of a noun phrase; reads like a description not a label)
- "Use the operator's existing Obsidian vault discipline as the memory substrate" → "Your existing Obsidian vault becomes the memory store." (you/your; "becomes" instead of "as the memory substrate")
- "the convention layer" → dropped (redundant with "file convention")
- "Each agent has its own four-file persona pack (...) per Paperclip's 4-file-per-agent pattern" → "Every agent has its own 4-file pack (...) like Paperclip does." (fewer prepositional phrases)
- "Vault is source-of-truth; Hermes pillars are the runtime view onto vault files" → "The vault is the source of truth; Hermes' built-in features look at vault files."
- "agents query via Read + grep + Dataview + Obsidian wikilink traversal" → "agents just read files and grep" (plainer; the specific tools matter less than the pattern)

What survived: every file name, the 4-file-per-agent pattern reference to Paperclip, the no-ETL claim, the vault-as-source-of-truth claim, the SQLite detail (in the original but the original sentence about it was implicit; the plain version keeps it equivalent).

## Pros lists

### Decision 1 Option B pro — Cole hooks

**Original:**
> - Cole Medin's self-evolving Claude Code hooks ([[tactic-llm-knowledge-bases-pattern]] 1/3 Cole canonical) automate session-memory accumulation — operator doesn't have to remember to capture decisions.

**Translation:**
> - Cole's auto-capture hooks mean you don't have to remember to capture decisions — sessions self-dump.

What changed:
- "Cole Medin's self-evolving Claude Code hooks" → "Cole's auto-capture hooks" (Cole's last name is recoverable from context; "self-evolving Claude Code hooks" → "auto-capture hooks" describes function not architecture)
- Wikilink + pattern shorthand citation `([[tactic-llm-knowledge-bases-pattern]] 1/3 Cole canonical)` → dropped from this pro because the same wikilink + citation appears in the operator-discipline section a few paragraphs down. Don't repeat citations in tightly-coupled bullets if they appear in adjacent prose.
- "automate session-memory accumulation — operator doesn't have to remember to capture decisions" → "you don't have to remember to capture decisions — sessions self-dump" (you/your; "sessions self-dump" is plainer than "session-memory accumulation")

NOTE: this is a case where a wikilink dropped because of proximity to the same wikilink in a structural section. This is the only acceptable wikilink-drop pattern. If the wikilink doesn't reappear within ~30 lines, preserve it in the bullet.

## Cons lists

### Decision 2 Option A con — daily-scrum fantasy

**Original:**
> - "Imagined value vs real-world complexity gap" risk per [[phase-3-plus-queue]] #5 framing. Paperclip's multi-agent fleet capabilities are the same shape as the "8am daily scrum fantasy" operator explicitly deferred. Adopting Paperclip-heavy = orchestrating an agent fleet, which contradicts the "PM-style single coordinator + sequentially-called sub-agents (NOT 8am scrum)" framing in [[current-goals]].

**Translation:**
> - Paperclip's multi-agent fleet capabilities are the same shape as the "8am daily scrum" failure mode you deferred in phase-3-plus-queue. Going Paperclip-heavy = running an agent fleet, which contradicts the "single PM + sequential sub-agents (NOT 8am scrum)" framing in current-goals.

What changed:
- "'Imagined value vs real-world complexity gap' risk per [[phase-3-plus-queue]] #5 framing" → folded the framing into the next sentence; preserved "phase-3-plus-queue" as a vault reference (still readable as a wikilink-style mention even without the brackets in some renderings — but the actual translation in the file does preserve `[[phase-3-plus-queue]]` as brackets when present in the original)
- "operator explicitly deferred" → "you deferred" (you/your)
- "Adopting Paperclip-heavy = orchestrating an agent fleet" → "Going Paperclip-heavy = running an agent fleet" (plainer verbs)

What survived: the "8am daily scrum fantasy" callout, the phase-3-plus-queue #5 reference, the current-goals reference, the substantive contradiction claim.

## Operator-discipline rule application

### Decision 1 — premature abstraction rule application

**Original:**
> - **Premature-abstraction (precedent #1):** Option C commits to Richmond's full 7+ taxonomy upfront when 2/3 is the cross-creator math; this is the strongest premature-abstraction risk. Option B commits to Cole's LLM-knowledge-bases at 1/3 with Karpathy-weight discipline applied. Option D explicitly avoids both. Option A leans on Hermes substrate-built-in (file-system taxonomy) which is substrate-documentation, not cross-creator pattern math — so the 2/3 promotion threshold question doesn't gate Option A directly, but Hermes-substrate-specific lock-in is the trade.

**Translation:**
> - **Premature abstraction (rule #1):** Option C commits to Richmond's full 7+ type taxonomy when the cross-creator math is only at 2/3 — the strongest premature-abstraction risk. Option B commits to Cole's pattern at 1/3 with the Karpathy-weight problem. Option D explicitly avoids both. Option A leans on Hermes' file convention — which is substrate documentation, not cross-creator pattern math — so the 2/3 promotion threshold doesn't gate it directly, but you're locking in to Hermes specifically.

What changed:
- "(precedent #1)" → "(rule #1)" (plainer; "rule" reads as native English vs. "precedent" reads as legal/institutional)
- "upfront when 2/3 is the cross-creator math" → "when the cross-creator math is only at 2/3" (clearer logical structure)
- "with Karpathy-weight discipline applied" → "with the Karpathy-weight problem" (plainer noun)
- "Hermes substrate-built-in (file-system taxonomy)" → "Hermes' file convention" (drops redundant qualifier)
- "the 2/3 promotion threshold question doesn't gate Option A directly, but Hermes-substrate-specific lock-in is the trade" → "the 2/3 promotion threshold doesn't gate it directly, but you're locking in to Hermes specifically" (you/your; "locking in" instead of "lock-in is the trade")

What survived: every option referenced (A, B, C, D); the 2/3 / 1/3 pattern math numbers; Richmond's 7+ type taxonomy; Cole reference; Karpathy-weight reference; the actual trade-off being articulated.

## Honest framing blocks

### Decision 2 — honest framing opening

**Original:**
> Phase B evidence weighs toward **Option C (PM-coordinator agent owns orchestration), with Paperclip as runtime container** for v1. Reasoning:
>
> - [[current-goals]] Goal A coordination-layer framing explicitly names "single PM-style coordinator agent + sequentially-called sub-agents" — operator-altitude is already committed to this shape. Re-asking "what shape should orchestration take?" risks re-litigating committed operator-altitude.

**Translation:**
> Evidence weighs toward **Option C (PM-coordinator agent, with Paperclip as runtime)** for v1. Reasoning:
>
> - Current-goals Goal A explicitly names "single PM-style coordinator + sequentially-called sub-agents" — you've already committed to this at the operator-altitude. Weighting away from Option C implicitly asks you to reopen that altitude.

What changed:
- "Phase B evidence weighs toward" → "Evidence weighs toward" (slight tightening; the Phase B context is established at document level)
- "Option C (PM-coordinator agent owns orchestration), with Paperclip as runtime container" → "Option C (PM-coordinator agent, with Paperclip as runtime)" (drops "owns orchestration" — the option already named is its own definition; drops "container" — implicit)
- "[[current-goals]] Goal A coordination-layer framing explicitly names" → "Current-goals Goal A explicitly names" (kept the reference; tightened the prose)
- **Rhetorical softening:** "Re-asking 'what shape should orchestration take?' risks re-litigating committed operator-altitude" → "Weighting away from Option C implicitly asks you to reopen that altitude." This is the explicit rhetorical-edge softening from the translation rules. Same substance (deviating from current-goals reopens prior commitment); different posture (descriptive instead of warning).

What survived: the lean (Option C), Paperclip-as-runtime framing, current-goals reference, the substantive observation that current-goals already committed at operator-altitude.

## Surfaced-not-decided items

### Item #9 — PM coordinator persona memory

**Original:**
> 9. **PM coordinator's persona memory is a hidden Decision 5 commit.** Option C (coder + reviewer + PM) and Option B (5-agent roster) both require a PM coordinator persona authored in v1. Decision 1 weighting toward Option D (minimal memory v1, persona stub for PM only) is the same persona-authoring commit. The PM coordinator persona note is the natural integration point between Decisions 1 and 5. Worth explicit operator-design pass on PM coordinator's `soul.md` once Decisions 1 and 5 close.

**Translation:**
> 9. **PM coordinator's persona memory is a hidden Decision 1+5 integration point.** Option C in Decision 5 (coder + reviewer + PM) and Option B in Decision 5 (5-agent roster) both require a PM coordinator persona authored in v1. Decision 1 weighting toward Option D (minimal memory v1, persona stub for PM only) is the same persona-authoring commit. The PM coordinator persona note is the natural integration point between Decisions 1 and 5. Worth an explicit operator-design pass on PM's `soul.md` once Decisions 1 and 5 close.

What changed (this one is very light because the original was already plain-ish):
- "a hidden Decision 5 commit" → "a hidden Decision 1+5 integration point" (slight clarification; both decisions are involved)
- Option references got "in Decision 5" added (slightly clarifying which option in which decision)
- "PM coordinator's `soul.md`" → "PM's `soul.md`" (slight tightening)
- "Worth explicit operator-design pass" → "Worth an explicit operator-design pass" (small grammatical smoothing)

This is what light-touch translation looks like when the original is already reasonably accessible.

## Cross-references

The original document's cross-reference section (upstream / downstream / substrate tools / patterns at threshold) does NOT need plain-language translation — it's a list of wikilinks and labels, not prose. Preserve it verbatim or with minimal copy-edit.

## A note on length

The worked example was 823 lines original → 807 lines plain. ~2% reduction. The reduction came from:
- Slightly tighter sentences (about 60% of the work)
- Dropped redundant qualifiers (about 20%)
- Folded duplicate citations within bullets (about 10%)
- Smaller restructurings where the original had unnecessary nesting (about 10%)

If you find yourself dropping 20% or more, you're summarizing. If you're adding 20% or more, you're over-glossing. The sweet spot is ±5%.
