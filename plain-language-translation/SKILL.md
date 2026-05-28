---
name: plain-language-translation
description: Rewrite dense, jargon-heavy documents into plain language while preserving 100% of the content, structure, evidence, and wikilinks. Use whenever Oliver asks to "translate," "restate," "dumb down," "make plain," "rewrite in plain English," "rewrite so I can understand," "make readable," or "explain in simpler terms" a structured artifact — decisions documents, syntheses, build plans, goal documents, analyses, or any dense vault note. Also trigger when Oliver reads a dense doc and asks what it means, what to do with it, or how to understand it — restate rather than summarize. Default output is a new file saved next to the original with the `-plain` suffix. Always does a FULL restatement (same length, same structure, same content) — does not ask scope questions, does not compress, does not summarize. This is the primary path for making any dense vault artifact actually readable.
---

# Plain-Language Translation

A skill for rewriting dense, jargon-heavy documents into plain language so Oliver can actually read them. Same content, same structure, same evidence — different voice.

**Critical behavior (read this before anything else):**
- **Preserve everything.** This is a *translation*, not a summary. Same length (or slightly shorter). Same section structure. Every pro, every con, every option, every dependency note, every wikilink, every task reference, every pattern citation.
- **Output a new file by default.** Save next to the original with `-plain` appended to the filename. Only output inline if Oliver explicitly asks for inline.
- **Don't ask scope questions.** Always do the full restatement. The whole point is that Oliver wants the entire document made readable, not summarized.

## When to trigger

Direct triggers — these phrases reliably indicate the skill should run:
- "Plain language version of [X]"
- "Translate this into plain English"
- "Rewrite this so I can understand it"
- "Dumb this down"
- "Restate this without the jargon"
- "Make this readable"
- "Explain this in simpler terms"
- "Plain-language [X]"
- "Plain talk version"

Indirect triggers — when Oliver has clearly read a dense document and is struggling with it:
- "I don't really understand this"
- "Can you break this down for me?"
- "What is this actually saying?"
- "This is too jargon-heavy"
- "I need this in language I can read"

When in doubt: trigger the skill. The cost of running the skill on a doc that didn't need it is low; the cost of NOT running it when Oliver needed it is that he can't engage with his own vault.

## Core workflow

### Step 1 — Identify the source document

Oliver will reference a document by name, path, or description. The document might be:
- In project knowledge (most common in web-UI chats)
- At a vault path (`second-brain/_meta/decisions/...`, `second-brain/_meta/synthesis/...`, etc.)
- Pasted inline in the conversation
- Recently created in the current chat

Read the full source document before drafting anything. Don't translate from memory or from a summary.

### Step 2 — Identify the output mode

Default: **new file**, saved next to the original, filename = `<original-name>-plain.md`.

Inline override: if Oliver explicitly says "inline," "in the chat," "don't make a file," "just show me," or similar — output in the chat instead of a file.

If Oliver doesn't specify, default to new file.

### Step 3 — Draft the plain-language version

Follow the rules in `references/translation-rules.md`. Critical preserved elements:
- Every section header (same wording, same hierarchy)
- Every option, every pro, every con
- Every wikilink (`[[...]]`) and every task reference
- Every pattern citation and creator attribution
- Every cross-creator math number (1/3, 2/3, 3/3)
- Every operator-discipline rule reference (with brief gloss added in plain language)
- Every dependency note
- Every "honest framing of where evidence weighs" block

Translate the *voice* — sentence rhythm, jargon density, abstraction level. Don't translate the *content*.

### Step 4 — Write the output

For file output (default):
1. Generate the new file with frontmatter copied from the original, modified as follows:
   - Add `plain-language` to `tags:`
   - Add the original document's wikilink to `related:` (so they cross-reference)
   - Keep all other frontmatter fields unchanged unless they're stale
2. Save to the same directory as the original, with `-plain` appended to the filename stem (before the `.md`).
3. If the skill is running in an environment where Oliver's vault path isn't accessible (e.g., web-UI chat), write the file to `/mnt/user-data/outputs/` and use `present_files` to surface it for Oliver to download and move into his vault.
4. After writing, briefly tell Oliver where the file is and what was preserved vs. changed (a few sentences, not a wall of text).

For inline output:
1. Write the plain-language version directly in the chat.
2. Don't preface with a long meta-comment — just give Oliver the translation.

### Step 5 — DON'T add things that weren't there

The skill is a translation, not an improvement. Do NOT:
- Add executive summaries
- Add a "TL;DR" at the top
- Add new sections, tables of contents, or summaries
- Reorder options or sections
- Drop or compress pros/cons even if they seem redundant
- Soften pro/con framing — if the original says one option is risky, the plain version says the same option is risky in plainer words
- Decide for the operator — if the original surfaces options without recommending, the plain version surfaces the same options without recommending
- Change the substance of any "honest framing" or "where the evidence weighs" section

## The voice — what plain language looks like in this skill

Oliver liked a specific voice in the conversation that produced this skill. Match it:

- **Short sentences.** Break dense sentences into 2-3 shorter ones.
- **Conversational rhythm.** Read like a colleague explaining over coffee, not a whitepaper.
- **"You" and "your."** Address Oliver directly, not "the operator" (when context is operator-altitude). Match the original's perspective if it's third-person.
- **Concrete over abstract.** "Vault grows to thousands of notes; agent queries blow up on grep" not "retrieval-at-scale failure modes."
- **Gloss rule names.** When the original cites an operator-discipline rule by name ("premature-abstraction discipline applies"), keep the name and add a brief gloss in the same sentence: "this is the failure mode where you commit to a pattern's full shape before you've actually used it."
- **Soften rhetorical edges.** If the original uses operator-discipline as a thumb-on-the-scale phrase ("risks re-litigating committed operator-altitude"), rewrite to descriptive ("weighting away from this option implicitly asks you to reopen that altitude").
- **Keep technical terms when they're the actual subject.** Don't replace "MCP server" with "thing that exposes tools." Plain language ≠ dumbed down terminology; it means dumbed-down *prose around* the terminology.

For more guidance on the voice, see `references/voice-examples.md`.

## Filename + frontmatter rules

**Filename:** Insert `-plain` before the `.md` extension.
- `phase-b-decisions-2026-05-11.md` → `phase-b-decisions-2026-05-11-plain.md`
- `current-goals.md` → `current-goals-plain.md`
- `master-system-map.md` → `master-system-map-plain.md`

**Frontmatter:** Copy the original's frontmatter, then:
- Add `plain-language` to `tags:`
- Add the original's wikilink to `related:` array
- Update `updated:` to today's date
- If the original has `status:`, copy it unchanged (a plain-language draft of a committed document is still a draft of a committed document — the status reflects the original's status)
- Add a 1-line note in the document's preamble identifying it as the plain-language version of the original

Example preamble note (one-liner under the H1, before the rest of the content):
```
> Same content as [[original-doc-name]]. Rewritten in plain language so you can read it without translating jargon in your head.
```

## Closing step — Auto-invoke output-quality-loop

After the plain-language companion is written and the preamble note added under the H1, emit the standard auto-invoke block per `~/workspace/skills/output-quality-loop/references/auto-invoke-convention.md` and `~/workspace/second-brain/_meta/conventions.md` § "Output quality". This is the closing step every artifact-producing skill emits before declaring the chat done. Convention shipped Phase 5 of the output-quality-loop project (2026-05-28).

**Artifact list for this skill.** The plain-language companion file (e.g., `<original-slug>-plain.md` in the same folder as the original). Do NOT include the original — it is not modified by this skill.

**The block to emit (verbatim):**

````markdown
## Auto-invoke output-quality-loop

This skill produced the following artifact(s):
- `<plain-language-companion-path>`

[output-quality-loop:eval] — for each artifact, run output-quality-loop in EVALUATE mode. If PASS, declare the chat done. If NEEDS REVISION or FAIL, ingest the revision prompt as if it were operator input and regenerate the artifact, then re-invoke output-quality-loop. Cap at 3 iterations; on the 3rd FAIL, escalate to the operator with the evaluation report.
````

Required-element discipline per the convention spec: heading text matches verbatim (`## Auto-invoke output-quality-loop`); one bullet per artifact with full path in backticks; directive opens with `[output-quality-loop:eval]` and includes the iteration-cap discipline language.

**Iterate or declare done.** All PASS → declare done. Any NEEDS REVISION (minor / substantive) → Mode 2 auto-fires a revision prompt; ingest as operator input, apply fixes (re-translate paragraphs that drifted into summarization, restore lost wikilinks, restore lost pattern citations, tighten an over-glossed section, fix soft-rhetorical-edge drift), re-emit the block, loop. Any FAIL → revision prompt includes root-cause analysis; address the root cause (often: drift into advocacy / improvement / summarization, missing preamble, structural reordering), regenerate, re-emit, loop.

**Iteration cap (3 max).** Track count via the folder-quality-log's per-artifact section before each regeneration. If three iteration entries exist and the verdict is still not PASS, **escalate** to the operator with the evaluation report and stop. Don't run a fourth iteration — that's the load-bearing cost-control discipline.

**Operator bypass.** Include `--bypass-quality-loop` (or "skip the quality loop") in the original translation request to skip the block for that invocation. The bypass records to the closest folder's `_quality-log.md` under `### Bypassed (manual override)`.

## Failure modes to avoid

- **Drift into summarization.** If your output is shorter than the original by more than ~10%, you summarized instead of translating. Go back and fill in.
- **Drift into improvement.** If you find yourself adding a "this could be clearer if we restructured as..." section, stop. You're outside scope.
- **Drift into advocacy.** If the original is option-neutral and your translation makes one option sound better, that's a voice failure. Match the original's neutrality.
- **Loss of wikilinks.** Every `[[...]]` reference in the original must appear in the translation. They're operationally load-bearing for vault navigation.
- **Loss of pattern citations.** Every "3/3" or "1/3 promoted via X" reference must survive. They're operationally load-bearing for the operator-discipline rules.
- **Over-glossing.** Don't gloss every term — only the ones where the jargon is the obstacle. "MCP server" can stay; "Operationalizes external-state-as-agent-source-of-truth (3/3 past threshold)" needs to become "Task notes ARE the external state both you and agents commit to — and this pattern (external state as the agent's source of truth) is past the 3/3 promotion threshold."

## Reference files

- `references/translation-rules.md` — the detailed rules for what to preserve and how to translate voice. Read this before drafting.
- `references/voice-examples.md` — paired before/after examples from the worked example (phase-b-decisions). Read this when you need a voice anchor.

## Worked example

The canonical worked example for this skill is the pair:
- Original: `second-brain/_meta/decisions/phase-b-decisions-2026-05-11.md`
- Plain version: `second-brain/_meta/decisions/phase-b-decisions-2026-05-11-plain.md`

If you're uncertain about voice, output shape, or what "plain language" means in Oliver's vault context, read those two files side by side. The plain version is the anchor — match its voice and structural fidelity in any future translation.

## See also: pairing with step-by-step-walkthrough

If the doc you just translated is a process, SOP, setup flow, or anything else Oliver is about to execute (not just read), mention that [[step-by-step-walkthrough]] can guide him through the plain version one step at a time.

The pattern:
1. Translate the dense doc → readable version (this skill)
2. Walk through the readable version one action at a time (step-by-step-walkthrough)

Don't auto-invoke the walkthrough. Just surface it as a follow-up option after delivering the translation: "Want me to walk you through this step by step now?" Oliver decides.

Trigger this suggestion when:
- The translated doc reads as procedural — has numbered steps, sequential actions, setup instructions, or "do X then Y" structure
- Oliver mentions he's about to execute it ("I need to do this," "let me run through this")
- The original is an SOP, runbook, onboarding flow, or similar action-oriented artifact

If the doc is purely analytical (a decision document, a synthesis, a strategy note) and there's nothing to execute, skip the suggestion.
