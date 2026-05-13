# Translation Rules

Detailed rules for the plain-language-translation skill. Read this before drafting a translation.

## The two-axis preservation rule

Think of any document as having two axes:

- **Content axis** — what the document says (facts, claims, evidence, citations, structure, options, pros, cons, dependencies).
- **Voice axis** — how the document says it (sentence rhythm, jargon density, abstraction level, formality).

Translation preserves the content axis 100%. It modifies the voice axis.

If you find yourself dropping a pro, compressing two cons into one, omitting a wikilink, or simplifying a 3-option section to 2 — you're moving on the content axis. Stop.

If you find yourself shortening a sentence, replacing a noun phrase with a verb phrase, or swapping a technical analogy for a plain one — you're moving on the voice axis. Keep going.

## What MUST survive translation (content axis)

### Structural elements
- All section headers (same wording, same hierarchy, same order)
- All option counts (4 options stay 4 options; never collapse, never expand)
- All numbered/bulleted lists (same count of items)
- All frontmatter fields from the original
- The same "where the evidence leans" block per decision (with the same lean, if any)

### Citations + references
- Every `[[wikilink]]` to other vault notes
- Every `[[task-YYYY-MM-DD-...]]` task reference
- Every `[[tactic-...]]` pattern reference
- Every `[[tool-...]]` tool reference
- Every `[[source-YYYY-MM-DD-...]]` source reference
- Every creator-name attribution (Karpathy, Cole Medin, Richmond Alake, KJ Rainey, The Augmented, Brian Casel, Dex Horthy, Nick Saraev, Nate Herk, David Ondrej, Sharbel A., Matt Pocock, Chris Parsons, BridgeMind, etc.)
- Every Phase B source number (source 22, source 31, source 34, etc.)
- Every cross-creator math number (1/3, 2/3, 3/3, past threshold)
- Every dollar/scale reference ($4M/year Leftclick, $2K/mo email client, etc.)

### Discipline rule references
The 10 operator-discipline precedents from `[[phase-b-synthesis-2026-05-10]]` get name-preserved with a plain-language gloss added inline. Never strip the rule name.

The rules:
1. Premature-abstraction discipline
2. One-creator-only-no-spawn discipline
3. Over-fragmentation discipline
4. Cluster-correction precedent
5. Karpathy-weight / mediated-vs-direct discipline
6. Cross-substrate-independent-arrival precedent
7. Diminishing-returns discipline
8. Retroactive precedent application
9. New-cluster-opening discipline
10. First-source-in-folder filing precedent

Plain-language gloss pattern (use this shape):
- Original: "Premature abstraction (precedent #1) applies."
- Translation: "Premature abstraction (rule #1) applies — this is the failure mode where you commit to a pattern's full shape before you've actually used it."

The gloss should be ~10-20 words, in the same sentence or the next sentence. Don't make it its own paragraph.

### Evidence + reasoning
- Every pro must survive as a pro
- Every con must survive as a con
- Every dependency note must survive
- Every "honest framing" reasoning bullet must survive
- Every "evidence gap" or caveat must survive

## What the translation MODIFIES (voice axis)

### Sentence rhythm
- Original: One 40-word sentence with three clauses.
- Translation: Two or three shorter sentences. 12-20 words each.

### Noun-phrase density
- Original: "Memory-architecture commitment as foundational architectural primitive."
- Translation: "Treating memory architecture as a foundational building block."

### Jargon density
- Original: "Operationalizes external-state-as-agent-source-of-truth (3/3 past threshold)."
- Translation: "Task notes ARE the external state both you and agents commit to. And this pattern — external state as the agent's source of truth — is past the 3/3 promotion threshold."

Note: in the second version, the pattern name `external-state-as-agent-source-of-truth` is preserved (it's load-bearing terminology), but the surrounding prose explains what it means.

### Abstraction level
- Original: "Retrieval-at-scale failure modes."
- Translation: "When the vault gets big, grep-based search stops scaling. Agent queries blow up."

### Formality
- Original: "Operator decides whether the weighting reflects the actual constraints."
- Translation: "You decide whether that weighting reflects the actual constraints."

The shift from "operator" to "you" is appropriate ONLY when the original is in operator-altitude voice. If the document is third-person institutional, keep it third-person institutional.

## What the translation DOES NOT add

- No executive summary
- No "TL;DR"
- No new section headers
- No tables of contents (unless the original had one)
- No new recommendations
- No new caveats
- No "I think you should..." framing
- No comparative analysis between options that wasn't in the original

## Edge cases

### When the original uses an unfamiliar acronym
Spell it out the first time, then use the acronym.
- Original: "MCP server"
- Translation (first use): "MCP server (Model Context Protocol — Anthropic's open protocol for agent-tool integration)"
- Translation (subsequent uses): "MCP server"

### When the original uses an operator-personal term
Keep the personal term — it's load-bearing.
- "Cowork" stays "Cowork"
- "second-brain" stays "second-brain"
- "VIS" stays "VIS"
- "Knowledge OS" stays "Knowledge OS"
- "tier-1 task" stays "tier-1 task" (don't expand to "tier-one task")

### When the original uses an in-vault wikilink with display text
Preserve both the link and the display text.
- Original: `[[tactic-supervisor-multi-agent-pattern|supervisor pattern]]`
- Translation: same `[[tactic-supervisor-multi-agent-pattern|supervisor pattern]]`

### When the original cites a Phase B source by number
Preserve the citation.
- Original: "Per Brian Casel source 28..."
- Translation: "Per Brian Casel (source 28)..."

The citation pattern can be lightly modernized for readability but the source number must survive.

### When the original has nested bullet structures
Preserve the nesting. Don't flatten 3-level nested bullets into 1-level prose paragraphs unless the flattening loses no content.

### When the original has rhetorical edges (advocacy-shaped phrasing)
Soften toward descriptive — but only the rhetorical edge, not the substance.
- Original: "Re-asking 'what shape should orchestration take?' risks re-litigating committed operator-altitude."
- Translation: "Weighting away from Option C implicitly asks you to reopen the operator-altitude question. You decide whether to do so."

Same substance (this option contradicts a prior commitment). Different rhetorical posture (no thumb on the scale via "risks re-litigating").

## Length check

After drafting, count lines. A correctly translated document should be within ±10% of the original's line count. Going more than 10% shorter = you summarized. Going more than 15% longer = you over-explained.

The phase-b-decisions worked example: original was 823 lines, plain version was 807 lines. That's a ~2% reduction — exactly the right shape.
