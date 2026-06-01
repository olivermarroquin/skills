# Plain-language discipline (orchestrator-specific)

Cross-reference to `~/workspace/second-brain/_meta/plain-language-conventions.md` for the canonical rules. This file adds orchestrator-specific examples and the rules-of-thumb the SURVEY and NEXT-MOVES reports follow.

The plain-language conventions doc is canonical for cross-surface enforcement. Read it first. The examples below show what its rules look like when applied to vault-orchestrator output.

## The five orchestrator-specific traps

These are the failure modes orchestrator reports fall into when plain-language discipline lapses. Watch for each.

### 1. Bullet walls instead of synthesis prose

**Failure mode.** SURVEY Section 7 lists 8 unsynthesized sources as 8 bullet points and stops. No synthesis prose. No "what this means" framing.

**Fix.** Lead with a one-paragraph synthesis. Bullets list the underlying rows; prose ties them together.

**Bad:**
```
## Section 7 — Domain signals

- 4 unsynthesized sources in seo/
- 2 draft lessons in automation-systems/
- 1 pattern at 3+ observations in content-systems/
```

**Good:**
```
## Section 7 — Domain signals

Three domains have signal. `seo` has 4 unsynthesized sources from the past 14 days — could feed a Phase 2-style cluster synthesis. `automation-systems` has 2 lessons sitting at draft (the auto-invoke retrofit lesson, the two-file artifact split). `content-systems` has 1 pattern at 3 observations awaiting promotion.
```

### 2. Jargon density without gloss

**Failure mode.** NEXT-MOVES uses "leverage," "spec-routing coverage," "operator-fatigue heuristic," "load-bearing primitive" in dense succession without glossing any of them.

**Fix.** Gloss any rule name, convention name, or technical concept on first use within the report. After first use, the term can stand alone.

**Bad:**
```
Candidate A has high leverage because of spec-routing coverage gaps and a low operator-fatigue ceiling.
```

**Good:**
```
Candidate A is high-leverage — it ships a milestone (panel-upgrade page) and unblocks 3 downstream chats. The spec-routing-coverage gap (how many spec sources Mode 4 successfully loaded for evaluation) is a load-bearing safety net in the quality loop, and this candidate would tighten it.
```

### 3. Executive summaries the operator didn't ask for

**Failure mode.** SURVEY opens with a 4-sentence "Executive summary" wrapping the nine sections that follow. The operator can read the sections themselves.

**Fix.** Skip the executive summary unless explicitly requested. Open with Section 1 directly. The report is scannable by section; no wrapper needed.

**Bad:**
```
## Executive summary

The vault has 3 chats in flight, 4 ready to spawn, 6 queued. There are 6 open decisions and 3 scheduled tasks. Recent wins span 8 chats over the past 7 days. Three domains have signal worth surfacing.

## Section 1 — What's actively in flight
...
```

**Good:**
```
## Section 1 — What's actively in flight

Three chats are in flight. The first is...
```

### 4. Editorializing in neutral sections

**Failure mode.** Session-budget display says "Top 4 candidates total ~12 hours — this is too much for one day." That sentence took a fact and added an opinion the operator didn't ask for.

**Fix.** Display sections stay neutral. Recommendation sections (session plan, decision-research call) get to recommend. Don't blur the line.

**Bad:**
```
## Session-budget totals

Top 2 candidates total ~6 hours.
Top 4 candidates total ~12 hours — recommend scoping back.
```

**Good:**
```
## Session-budget totals

Top 2 candidates total ~6 hours.
Top 4 candidates total ~12 hours.
All 7 spawnable candidates total ~28 hours.

## Recommended session plan (capped at 8 hours)

Take A first (1 hour, Claude Code) — low-context-cost...
```

### 5. Telegraphic vs conversational rhythm

**Failure mode.** SURVEY reads as a series of dense, paragraph-less sentences. "Three in-flight. Four ready. Six queued. Two decisions pending."

**Fix.** Conversational rhythm — sentences vary in length, prose flows, synthesis paragraphs do the work.

**Bad:**
```
Three in-flight. Four ready. Six queued. Two decisions pending. Three scheduled tasks. Eight wins past 7 days. Three domain signals.
```

**Good:**
```
Three chats are in flight, four are ready to spawn, and six are queued behind various triggers. There are two open decisions sitting on you. Three scheduled tasks fire automatically over the next two weeks. The past 7 days closed 8 chats with ~60 artifacts shipped. Three domains have signal worth surfacing.
```

## Sections that should always be prose-heavy

- Section 1 (what's in flight) — each chat gets a sentence of plain description, not a row in a table
- Section 4 (open decisions) — decisions are story-shaped; prose carries the story
- Section 6 (recent wins) — narrative; what shipped and why it mattered
- Section 7 (domain signals) — synthesis paragraph plus underlying detail
- NEXT-MOVES per-candidate reasoning — prose, not bullets

## Sections that can stay terser

- Section 5 (scheduled tasks) — fact-shaped; prose framing + table is fine
- Section 8 (stale signals) — fact-shaped; per-project rows with verdict tags
- Session-budget totals — three sentences, one per total

## Voice-match against the canonical doc

When in doubt, the canonical doc's "What 'plain language' means in this system" section is the calibration point. Specifically:

- "Conversational rhythm. Read like a colleague, not a spec sheet." — every section opening passes this test
- "Concrete over abstract." — never write "retrieval-at-scale failure modes"; write "when the vault gets big, grep stops scaling"
- "Gloss rule names." — first use of any rule name gets a 10-20 word gloss inline
- "Same content, same structure, same length." — translation, not summary; preserve every claim

The output-quality-loop's plain-language compliance check fires on every persisted report. The check uses the same canonical doc as its bar.

## Plain language in the substrate-recommendation rationale

The substrate-recommendation rationale is one of the most frequent failure points for jargon density. Example failure:

**Bad:**
```
Candidate A: Claude Code (multi-file + Task tool parallel sub-agent shape per substrate-routing convention)
```

**Good:**
```
Candidate A: Claude Code — the work is multi-file edits across the vault, and the Task tool's parallel sub-agents fit cleanly. See `_meta/working-surfaces.md` § Default routing.
```

## See also

- `~/workspace/second-brain/_meta/plain-language-conventions.md` — canonical reference
- `~/workspace/skills/plain-language-translation/SKILL.md` — file-level translation skill
- `~/workspace/skills/vault-orchestrator/SKILL.md` § Core operating principles — the rule statement
- `./survey-section-shapes.md` — section-level voice rules
- `./session-budget-display.md` — neutral-display voice rules
