# VIS Source Extraction — Prompt for Cowork (v3.2)

This document tells Cowork how to extract structured KOS notes from a transcript file. It's read at the start of every extraction job. Treat it as authoritative — if the user's request and this document disagree, ask the user, don't guess.

---

## Inputs

You will be given:

1. **Transcript file path** — a path under `workspace/skills/vis-extraction/cache/` produced by `transcript-pull.sh`. The file has YAML frontmatter (source-type, url, title, etc.) followed by the content body.

2. **Vault root** — `workspace/second-brain/`. All notes you create go inside this root.

3. **Mode** — either `training` (you pause for user review before writing to disk) or `auto` (you write directly, user reviews in Obsidian afterward). Default: `training`.

---

## Phase 1 — Context gathering

Before reading the transcript content, read these files in order:

1. **Templates** — so you know the schemas to populate:
   - `second-brain/_meta/templates/vis/template-source-video.md`
   - `second-brain/_meta/templates/vis/template-tactic.md`
   - `second-brain/_meta/templates/vis/template-opportunity.md`
   - `second-brain/_meta/templates/vis/template-content-idea.md`
   - `second-brain/_meta/templates/kos/template-tool.md`
   - `second-brain/_meta/templates/template-discussion.md` (discussion template — used when starting discussions about sources, not during normal extraction; read for awareness)

2. **Conventions** — naming, linking, frontmatter rules:
   - `second-brain/_meta/conventions.md`

3. **Goals** — `second-brain/_meta/current-goals.md`. **If the file is not found at this exact path, STOP. Surface the missing-file condition to the operator explicitly (state the configured path that was checked) and require explicit acknowledgment before continuing Phase 1 — do not silently treat the file as absent.** If the file exists but has no goals content, treat as "no goals provided" and use generic relevance reasoning. Do not invent goals.

4. **Active project + system context** — read at appropriate depth:

   **Directory listings only (filenames, not contents):**
   - `second-brain/04_projects/personal/` (active personal projects)
   - `second-brain/04_projects/clients/_active/` (active client work)
   - `second-brain/01_ai-operating-system/` (the user's master architecture — what's built and what's planned)
   - `second-brain/02_core/ideas/` (ideas in flight)
   - `workspace/idea-factory/` if it exists (broader idea pipeline)
   - `workspace/ai-factory/` if it exists (factory infrastructure)

   **Read full content of:**
   - `workspace/CLAUDE.md` if it exists (top-level operating doc — high signal)
   - One or two project READMEs that look directly related to the source content
   - `second-brain/01_ai-operating-system/master-system-map.md` if the source touches system architecture

   **Skim only (open and look at headings):**
   - `second-brain/01_ai-operating-system/roadmap/phase-3-plus-queue.md` — so you know what's deferred and don't surface deferred items as new ideas

   The principle: **read directory listings broadly so you know what exists; read full file contents narrowly only when overlap is detected**. Don't try to read every file in the workspace. Don't go deeper than 2 levels into any directory unless the source explicitly references something there.

5. **Scoring rubric** — read `second-brain/_meta/scoring-rubric.md` (the canonical definitions for tier, relevance score, actionability score, monetization potential). Use those exact definitions in Phase 3 when generating Suggested judgments. Don't invent your own scales.

6. **Existing-note index** — list filenames in:
   - `second-brain/05_shared-intelligence/tools/`
   - `second-brain/05_shared-intelligence/patterns/`
   - `second-brain/03_domains/*/insights/` (across all domains)
   - `second-brain/00_inbox/decisions-pending/` (existing opportunities)

   You don't need to read the contents yet — just the filenames. Reading happens in Phase 4 when overlap is detected.

---

## Phase 2 — Chunking decision

Word count thresholds (count words in the transcript body, excluding frontmatter):

- **< 9,000 words (roughly < 45 minutes of speech):** single-pass extraction. Read the whole transcript at once, run Phases 3-7 normally.

- **9,000 – 25,000 words (roughly 45 min – 2 hours):** single-pass with explicit attention. Read the whole transcript in one go but with this guidance: identify the 5-7 highest-value sections (by content density and apparent insight) and extract primarily from those. Skim the others for connective tissue. Note the timestamps if available so the user can verify. Mark in the source note's frontmatter: `attention-mode: focused`.

- **≥ 25,000 words (roughly ≥ 2 hours):** chunked extraction. Split into 30-minute logical segments using chapter markers if present; otherwise split at natural topic transitions. Run Phase 3 (analysis) on each segment separately, then synthesize in a final pass. Mark `chunked: true` and `segment-count: N` in frontmatter.

For chunked extraction:
- Each segment produces its own internal analysis (don't write segment-level notes to disk)
- The final synthesis combines segment analyses into one source note + supporting notes
- The source note's `Workflow breakdown` section can capture the full sequence across segments
- Warn the user in the report: "synthesis across many segments may have lost some local nuance — re-check segment N if it seemed important"

---

## Phase 3 — Source analysis

Read the transcript (or a segment, in chunked mode). Produce an internal analysis covering:

### Global writing rules (apply throughout the source note)

These rules apply to every section you write. Don't restate them per section — just follow them.

**Acronym handling.** On first use of any acronym in the source note, expand it inline using the format `ACRONYM [expansion]`. Example: "AFK [away-from-keyboard]," "PRD [product requirements document]," "DAG [directed acyclic graph]," "TDD [test-driven development]," "MCP [model context protocol]." Subsequent uses in the same source note can be the acronym alone.

**Plain English coverage.** This source note has both dense technical content and plain-English summaries. The plain-English versions are *additions*, not replacements — the technical content stays, the plain-English summary sits alongside it. Specifically:

- A top-level **`## In plain English`** section sits right after the take-away. 3-5 sentences. The fastest possible comprehension surface — the reader should understand the source's gist in 30 seconds.
- Four jargon-heavy sections each get a `### In plain English` callout at the end of the section: **Take-away**, **Tools mentioned**, **Workflow breakdown**, **Strategy extraction**. Each callout is 1-3 sentences. Translate the jargon, don't repeat the bullets.
- All other sections do NOT get plain-English callouts. They're already plain or operational.

**Style for plain English.** Imagine explaining this to a thoughtful operator who isn't a specialist in this exact subdomain. No jargon (or if you must use a term, expand it). No bullets — flowing sentences. No "this section discusses..." meta-language. State the thing.

### What this source is

- **Take-away:** 1-3 paragraphs, dense and specific. The reader should be able to understand the source's core value from this alone. No generic phrasing ("this video discusses X"). State what the source actually argues, demonstrates, or reveals.

- **Main claim or claims:** if the source makes one central argument, capture it as one sentence. If the source makes multiple distinct claims, list them as bullets — don't artificially compress to a single claim when there are several.

- **Problem being solved (two parts):**

  *Part 1 — The pain in detail:* concretely describe the problem this source addresses. Make it specific. Paint a picture: who experiences this pain, when, what triggers it, what does it cost them, why does the existing approach fail. The reader should feel the pain after reading this.

  *Part 2 — How this pain manifests in the user's work:* given what you know from `current-goals.md` (if populated) and the active projects in `04_projects/`, where does this pain show up in the user's projects, clients, or capabilities? Be concrete: "this maps to the resume-saas onboarding flow problem you flagged in [[lesson-x]]" or "this would affect any client engagement in the [niche] segment." If you can't tie it to anything specific in their vault, say so and add a research question.

- **Audience / use case:** who would benefit from acting on this?

- **Novelty assessment:** new idea / new combination of known ideas / repackaging of known idea / hype with little substance. Pick one and briefly justify.

### Tools mentioned

For each tool, classify as:
- **Explicit** — the source named the tool by name
- **Inferred** — the source showed UI, screen recording, or behavior that strongly implies a specific tool
- **Uncertain** — possible tool but you're guessing

Be honest about which category. Inferring "they probably use Notion based on a brief cutaway" is fine when labeled as inferred. Inferring "they probably use Claude" because every AI creator uses Claude is not — that's noise.

### Workflow / process

If the source explicitly demonstrates a workflow:
- Extract the step-by-step process shown
- Note implementation details
- Note likely architecture (what's probably happening under the hood)

If the source describes a goal/outcome but doesn't show steps:
- Construct a likely workflow from what was said + general knowledge of the tools/domain
- **Place this in a clearly labeled section: `## Workflow (constructed by Claude — not shown in source)`**
- Keep this strictly separate from any actual demonstrated workflow

If the source has neither demonstration nor description:
- Workflow section gets one line: "Source did not demonstrate or describe a workflow."
- Do not invent one.

### Strategy extraction

For each strategy category (business, growth, automation, content, sales/offer):

If the source explicitly addresses it:
- Capture the strategy directly under the category heading

If the source did NOT address it but the content has implications:
- Put inferred strategy under `### <Category> (inferred — source did not state)`
- Reason from what the source did discuss + general principles
- Keep this clearly labeled as *your analysis*, not the source's claim

If the source didn't address it AND no implications can be reasonably drawn:
- One line: "Source did not address X strategy and content offers no clear implications."

### Replication potential

For each takeaway, classify:
- **Directly copyable** — can apply as-is to user's work
- **Needs adaptation** — useful but requires customization
- **Likely fluff or non-reusable** — not worth applying

### Visual signal markers

The transcript captures speech, not visuals. If during the transcript you encounter language that strongly suggests visual content matters (e.g., "as you can see in this folder structure," "look at how I've organized this," "here's the diagram," "watch what happens when I click"):

- Add a research question with the approximate timestamp if available
- Note: "Visual content at ~MM:SS — manually inspect if relevant"
- Do not fabricate what was on screen
- *(Future: a Phase 2.5 automation will auto-screenshot these timestamps. For now, the user does this manually.)*

### Research questions

Things the source hinted at but didn't fully reveal. Examples:
- Specific products/tools mentioned in passing without enough detail
- Strategies whose mechanism isn't fully explained
- Claims worth verifying independently
- Other sources by the same creator worth investigating
- Visual content that seemed important (per the previous section)

Be specific — "What's the actual close rate on this niche?" is useful; "Learn more about AI agents" is not.

### Speculative extensions (optional, clearly labeled)

This is a clearly-separated section in the source note for "what could this become." Use it for:
- "If you took this video's tactic and combined it with [existing project X], you could..."
- "This source's approach + your capability in Y could enable..."
- "An adjacent opportunity not stated by the source: ..."

**This section is explicitly labeled as your analysis, not the source's content.** It sits in its own section in the source note: `## Speculative extensions (Claude's analysis — not from source)`.

Use this when there's real signal worth elevating. Skip it when there's nothing meaningful to add — empty is better than noisy.

### Structured action items (this section drives the task system)

After producing the analytic content above, factor out **discrete, actionable items** into a structured block organized by kind. This is the input to the Phase 6 task-creation approval block and, after approval, becomes task notes in `06_tasks/` at Phase 7.

**Inclusion gate — all four must be true.** An observation rises to a structured action item only if:

1. **Decidable outcome** — closing the item requires a yes / no / done answer. Not "ongoing thought" or "general curiosity."
2. **Specific enough to act on** — names the project, the tool, the artifact, or the deliverable involved. "Investigate AI coding" doesn't qualify; "try `grill-me` on resume-saas auth feature" does.
3. **Generalizes beyond pattern-watching** — pattern observations stay in "Pattern candidates"; tasks live here.
4. **Actionable to the operator** — the operator can plausibly act on it given current capabilities and access. Curiosity questions Claude can't answer and the operator can't act on stay in "Research questions."

**Soft cap: 8-10 items per source.** Surplus observations stay in the legacy sections (Replication potential / Speculative extensions / Research questions). The system shouldn't inherit the diagnostic file's wide-net width — task creation is restrictive on purpose.

**Six kinds. Use the matching kind for each item.**

- **`experiment`** — date-bound test of a specific approach. Closing requires running it and observing the outcome. Often `unblocks:` a specific project task.
- **`decision`** — a choice between enumerated options. Closing means the operator picked one. Capture the options.
- **`comparison`** — side-by-side eval of two existing things to inform a downstream decision. `candidate-against:` the other entity being compared.
- **`research`** — open question whose answer gates a real downstream action. Auto-expires per `review-by:` (set `expires-after-days:`). NOT for curiosity questions — those stay in the source note's "Research questions" section.
- **`adoption`** — install / configure / start using a specific named tool or pattern. Usually small, often immediate.
- **`conditional`** — action gated by a checkable trigger. Stays planned until the trigger fires. Capture the trigger as a checkable string.

**Format in the source note:**

```markdown
## Structured action items

### Experiments
- **<short title>** — kind: experiment, tier: <suggested>, effort: <S|M|L>, unblocks: [<project>]
  <one-paragraph description>

### Decisions
- **<short title>** — kind: decision, tier: <suggested>
  - Options: <enumerated>
  <one-paragraph description>

### Comparisons
- **<short title>** — kind: comparison, tier: <suggested>, candidate-against: [[other-source-or-task]]
  <description>

### Research
- **<short title>** — kind: research, tier: <suggested>, expires-after-days: <14|30|90>
  <description>

### Adoptions
- **<short title>** — kind: adoption, tier: <suggested>, effort: <S|M|L>
  <description>

### Conditional
- **<short title>** — kind: conditional, trigger: "<checkable condition>"
  <description>
```

**Per-task tier is independent of source-note tier.** A tier-3 source can produce tier-1 tasks (and often does — e.g., a "save general" article can still spawn a "skim safety blog before installing X" tier-1 adoption). Calibrate each item on its own merits, not the source's overall tier.

**The Structured action items section sits BEFORE Suggested judgments in the source note.** Reasoning: per-task tier should be calibrated independently of source-tier; placing this section first prevents the source-tier from anchoring task-tier decisions at the gate.

### Suggested judgments (advisory, user fills the actual fields)

Generate suggested values for each judgment field, with one-line reasoning per suggestion. **These suggestions go in a separate section of the source note** (not in the frontmatter — the frontmatter judgment fields stay empty). Format:

```markdown
## Suggested judgments (Claude's analysis — verify before adopting)

These are advisory only. Read each, verify against your goals, then fill in the frontmatter fields above with your actual judgment. Don't anchor on these.

- **Suggested tier:** 2 — adjacent to current goals (resume-saas project), but not directly on the critical path
- **Suggested actionability score:** 3 — has 1-2 specific actions worth taking this month, not all 5
- **Suggested relevance score:** 4 — directly addresses [specific concern]
- **Suggested monetization potential:** medium — connects to client-services lane, but path requires capability development first
- **Suggested execution recommendation:** Save for later — high signal but not next week's priority

If `current-goals.md` is empty, suggestions degrade gracefully — be explicit about that limitation: "Goals doc empty; suggestions based on generic relevance only. Take with extra skepticism." (A missing file is a Phase 1 hard-fail per step 3, not a graceful path.)
```

These suggestions are:
- Explicitly advisory, never authoritative
- Visually separated from the actual fields the user fills
- Honest about their own uncertainty when goals.md is empty

The frontmatter judgment fields (`tier:`, `actionability-score:`, `relevance-score:`, `monetization-potential:`) stay **empty** in the written file. The user fills them after reading the suggestions and applying their own judgment.

---

## Phase 4 — Existing-note check (the dedup-and-enhance pass)

For each potential supporting note (tactic, opportunity, tool, content idea), check the existing-note index from Phase 1.

If there's a name overlap or topical overlap, **read the contents of the existing note**. Then decide one of four outcomes:

### Outcome 1: Pure duplicate

The new source adds nothing this note doesn't already have — same tool, same use case, same level of detail, same insights.

**Action:** No supporting note created. No backlink added (would just be noise). In the source note, mention "Same as [[existing-note]] — no new angle."

### Outcome 2: Enhances the existing note

The new source brings a new angle, use case, integration, edge case, or contradicting datapoint.

**Action:** Append a new section to the *existing* note, NOT a new standalone note. Format:

```markdown
## From [[source-YYYY-MM-DD-channel-topic]] (added YYYY-MM-DD)

<the new contribution — what's the new angle, the new use case, the new evidence>
```

The existing note becomes a living document that grows in richness across sources. The source note links to the existing note (now enhanced), and the source note's "Extracted artifacts" section notes "Enhanced [[existing-note]] with new section."

### Outcome 3: Conflicts with the existing note

The new source contradicts what the existing note claims (different mechanism, different pricing, different conclusion).

**Action:** Don't auto-resolve. Add a new section to the existing note labeled `## Conflicting evidence from [[source-...]] (date)` with both versions visible. Flag in the report so the user can investigate.

### Outcome 4: Genuinely new

No meaningful overlap. The tactic/tool/opportunity is new to the vault.

**Action:** Create a new supporting note as normal.

For opportunity notes, also include a `## Capability gap` section: if pursuing this opportunity requires capabilities the user doesn't have, name them and suggest 1-2 paths to acquire them. This way "I don't have skill X" doesn't silently kill a real opportunity — it becomes "I need to learn X to pursue this."

---

## Phase 5 — Conservative-creation gate

After Phase 4 has decided outcomes for each candidate, apply the conservative-creation rule one more time to the "create new note" decisions:

> **Only create a new supporting note when:**
> 1. The inference is specific enough to act on
> 2. It's distinct from things already in the user's vault (Phase 4 confirmed)
> 3. It would produce real value if linked from a future source

If a slot has nothing genuinely useful to record, leave it empty in the source note and explain *why* in one line. Do not fabricate content to fill quotas.

Type-specific rules:

- **Tactic notes:** create when there's a specific, repeatable approach. Don't create for generic advice ("focus on the customer") or hyper-specific situations that don't generalize.

- **Opportunity notes:** create when there's a real business hypothesis (who pays whom for what, why now). Don't create for vague "you could build X" suggestions or pure speculation.

- **Tool notes:** create when a specific named tool is mentioned (explicit) or strongly inferred and worth tracking. Don't create for tools mentioned only in passing without context.

- **Content idea notes:** create only when there's a specific hook (contrarian take, unique combination, surprising claim). Generic topics don't warrant a separate note — keep them in the source note instead.

When in doubt: don't create the note. Add the half-formed observation to the source note's relevant section as a sentence. The user can promote it later if it grows legs.

---

## Phase 6 — Review gate (training mode only)

If mode is `training`:

Show the user a structured summary:

```
SOURCE NOTE (DRAFT)
- File: source-YYYY-MM-DD-<channel>-<topic>.md
- Title, creator, take-away (1-3 sentences extract)
- Pain points / system fit: <one-line summary of how it ties to user's work>
- Suggested judgments included: yes (in separate section)
- Speculative extensions: <yes/no — if yes, brief>

PROPOSED NEW SUPPORTING NOTES
- tactic-<name> — <one-line reason>
- opportunity-<name> — <one-line reason>
- tool-<name> — <one-line reason>

ENHANCEMENTS TO EXISTING NOTES
- [[tool-claude-code]] ← new section: integration with X workflow
- [[pattern-niche-first-packaging]] ← new evidence section

PURE DUPLICATES (skipped, source note records "same as")
- Tool [[airtable]] mentioned but already documented identically

CONFLICTS DETECTED
- [[opportunity-onboarding-agent-service]] — new source says pricing should be 5x lower; conflict section added

SKIPPED (with reasons)
- Tactic about X — too generic to generalize
- Content idea Z — no specific hook, kept as note in source

LINKS TO EXISTING NOTES
- [[tool-make-com]] — referenced in workflow
- [[pattern-niche-first-packaging]] — this source is candidate evidence

RELEVANCE TAGGING (proposals for relevant-projects / relevant-domains frontmatter)
*(Lookup before proposing: read 04_projects/personal/*/README.md, 04_projects/clients/_active/*/README.md, and 04_projects/clients/_private/*/README.md for active project slugs (frontmatter `project-name:`) and `## Purpose` summaries. Enumerate 03_domains/*/ for valid domain slugs. Do not invent names not on disk. When unsure whether this source applies to a candidate, list it under "Uncertain" with reasoning — do not guess. If no clear matches exist, say "No clear project or domain matches" rather than fabricating.)*

Relevant projects:
- resume-saas — <one-sentence reason this source might inform resume-saas>
- idea-factory — <one-sentence reason>

Relevant domains:
- automation-systems — <one-sentence reason>
- personal-development — <one-sentence reason>

Uncertain:
- <project-or-domain> — <reason; operator decides>

Approved values land in the source's `relevant-projects:` and `relevant-domains:` frontmatter at Phase 7. Operator can modify by saying "remove X" / "add Y" / "swap Z to <other>" — agent revises and re-shows.

VISUAL SIGNAL FLAGS
- ~6:42: folder structure mentioned but not in transcript — manual screenshot recommended

RESEARCH QUESTIONS (3)
- What's the close rate on this productized service in the cited niche?
- Did the creator use Make.com or n8n? Brief shot suggested Make.
- Visual content at ~6:42 (folder structure)

PROPOSED STRUCTURED ACTION ITEMS (would create N task notes at Phase 7)

Experiments (3):
- task-YYYY-MM-DD-<slug> — tier <N>, effort <S|M|L>, unblocks <project>
  <one-line description>
- ...

Decisions (2):
- task-YYYY-MM-DD-<slug> — tier <N>
  Options: <enumerated>
  <one-line description>
- ...

Comparisons (1):
- task-YYYY-MM-DD-<slug> — tier <N>, candidate-against: [[other-source-or-task]]
  <one-line description>

Research (5):
- task-YYYY-MM-DD-<slug> — kind: research, expires-after: <N> days
  <one-line description>
- ...

Adoptions (2):
- task-YYYY-MM-DD-<slug> — tier <N>, effort <S|M|L>
  <one-line description>
- ...

Conditional (1):
- task-YYYY-MM-DD-<slug> — trigger: "<checkable condition>"
  <one-line description>

Approve all / modify item N / skip category X / reject all? (a/m/s/r)

Approve, modify, or reject? (a/m/r)
```

Wait for the user's response before writing anything to disk.

If user approves: proceed to Phase 7.
If user requests modification: revise per their instructions, show the summary again.
If user rejects: stop. Don't write anything. Ask if they want to retry with different framing.

If mode is `auto`: skip this phase, go straight to Phase 7. In auto mode, `relevant-projects:` and `relevant-domains:` frontmatter fields are written as empty arrays — populate later via re-extraction or manual edit.

---

## Phase 7 — Write to disk

For each approved action:

### Source note

1. Filename: `source-YYYY-MM-DD-<channel-or-author-slug>-<topic-slug>.md`
   - Date is the source's *publish* date if known, *ingestion* date if not
   - Channel/author slug: kebab-case, max 25 chars
   - Topic slug: kebab-case, max 35 chars (so the full filename stays under ~80)
   - Examples: `source-2026-05-03-nate-herk-claude-code-skills-six-best.md`, `source-2025-08-25-anthropic-piloting-claude-in-chrome.md`

2. Apply the source-video template, populate all the structured sections produced in Phase 3. **Specifically:** populate the top-level `## In plain English` section (3-5 sentences) AND the four `### In plain English` callouts at the end of Take-away, Tools mentioned, Workflow breakdown, and Strategy extraction. Apply acronym-expansion on first use throughout.

3. **Leave judgment fields empty in frontmatter:**
   - `tier:` — empty, user fills
   - `actionability-score:` — empty
   - `relevance-score:` — empty
   - `monetization-potential:` — empty
   - `Execution recommendation` checkboxes — all unchecked
   - `Reasoning` line under it — empty

4. **Populate the "Suggested judgments" section** of the body with advisory values + reasoning. The user reads these, then fills the actual frontmatter fields with their own judgment.

5. Place in: `second-brain/00_inbox/sources-pending/`

6. **Action log section starts empty.** The template includes an Action log section. When writing a new source note, leave the Action log section as just the heading + the placeholder bullet. The user fills it in over time as they act on the source.

   Do NOT auto-populate the Action log with execution-recommendation items. Those are commitments the user makes, not extractions. The user moves items from Suggested judgments / Speculative extensions / Research questions into the Action log when they decide to act.

7. **Discussions section starts empty.** The template includes a Discussions section with a Dataview block that will auto-populate as discussions get created later. Leave the Dataview block in place — don't remove it, don't pre-create discussions, don't put text in the section beyond what the template provides.

8. Set `status: ingested` (changes to `extracted` after the user reviews)

### New supporting notes

For each new note (post-conservative-creation gate):

- **Tactic notes:** `tactic-<name>.md` in `second-brain/03_domains/<domain>/insights/`. Pick the domain based on the tactic's subject: app-building, automation-systems, video-intelligence, content-systems, client-services. Status: `extracted`.

- **Opportunity notes:** `opportunity-<name>.md` in `second-brain/00_inbox/decisions-pending/`. Status: `surfaced`. Include the capability-gap section if applicable.

- **Tool notes:** `tool-<name>.md` in `second-brain/05_shared-intelligence/tools/`. Status: `evaluating` initially.

- **Content idea notes:** `content-<name>.md` in `second-brain/03_domains/content-systems/insights/`. Status: `ideated`.

### Task notes (from approved Structured action items)

For each item the operator approved at the Phase 6 task-creation block:

- **Filename:** `task-YYYY-MM-DD-<slug>.md`. Date is the creation date (today). Slug is kebab-case, max ~40 chars.
- **Folder:** `second-brain/06_tasks/`.
- **Apply** `_meta/templates/task/template-task.md`.
- **Frontmatter — required fields:**
  - `type: task`
  - `kind:` matches the kind from the proposed item
  - `status: planned`
  - `created:`, `updated:`, `opened:` all = today's date
  - `tags: [task, <kind>]`
  - `source: "[[<source-note-filename-without-extension>]]"`
  - `extracted-via: vis-phase6`
- **Frontmatter — populate when the proposed item provides them:**
  - `relevant-projects:`, `relevant-domains:` — propagate from source note's relevance tagging when the action targets those projects/domains
  - `tier:` — operator-approved tier from the gate
  - `effort:` — operator-approved effort from the gate
  - `due:` — if a date was specified
  - `review-by:` — required if `kind: research`; default = today + `expires-after-days:`
- **Frontmatter — kind-specific (set only when the kind matches):**
  - `kind: conditional` → `trigger:`
  - `kind: experiment` → `unblocks:`
  - `kind: research` → `expires-after-days:`, `review-by:`
  - `kind: comparison` → `candidate-against:`
  - `kind: decision` → `decision-options:`
- **Body sections:**
  - `## Context` — link the source as `[[<source-note>]]`. Summarize the source's rationale for this action in 1-2 paragraphs (this is what the operator wants to read 6 weeks from now to remember why they queued the task). Include "What closing this task looks like."
  - `## Decision archaeology` — first entry: `<today> — created from [[<source-note>]] via vis-phase6 (status: planned)`.
  - `## Notes` — leave empty bullet placeholder.
- **Bidirectional linking:** the source note's "Action log" Dataview block auto-finds the task via `contains(string(source), this.file.name)`. No manual backlink needed beyond the `source:` frontmatter field.

If the operator skipped a category (e.g., "skip research") at the Phase 6 gate, write zero notes for that category. If the operator rejected the whole task block, write zero task notes. The remaining structured items remain in the source note's "Structured action items" section as a record of what was proposed; the section itself is preserved on disk.

### Enhancements to existing notes

For each "enhance existing" decision from Phase 4:

- Open the existing note
- Append the new section at the end (above any "Promotion log" or "Decision log" section if those exist)
- Format: `## From [[source-YYYY-MM-DD-...]] (added YYYY-MM-DD)\n\n<contribution>`
- Update the existing note's frontmatter `updated:` date to today
- Increment `times-observed:` if it's a pattern note

### Bidirectional links

- Source note's "Extracted artifacts" section: list all newly-created supporting notes AND all enhanced-existing notes as `[[wikilinks]]`
- Each newly-created supporting note's "Sources where seen" / "Triggering source" / "Where seen" field: links back to the source note
- Use `[[shortest-path]]` format (Obsidian's setting)

### Do not commit to git

Writing files is your job. Committing is the user's job. Tell the user what to commit at the end.

---

## Phase 8 — Report

After writing, produce a clean summary for the user:

```
EXTRACTION COMPLETE

Source: source-YYYY-MM-DD-<channel>-<topic>.md (in 00_inbox/sources-pending/)
- Mode: single-pass / focused / chunked
- Word count: NNNN

Created (NEW notes):
- 2 tactic notes: [[tactic-x]], [[tactic-y]]
- 1 opportunity note: [[opportunity-z]]
- N task notes in 06_tasks/ (breakdown by kind: experiments=N, decisions=N, research=N, ...)

Enhanced (existing notes that grew):
- [[tool-claude-code]] ← new integration use case section
- [[pattern-niche-first-packaging]] ← new evidence + variant

Linked to existing (no changes to those notes):
- [[tool-make-com]] — referenced in workflow
- [[pattern-three-tier-prompt-architecture]] — same pattern observed

Skipped:
- Pure duplicate: [[tool-airtable]] (no new angle)
- Generic: tactic about "always validate inputs" (not source-specific)

Conflicts flagged for your review:
- [[opportunity-onboarding-agent-service]] — pricing contradiction

Visual signals to investigate manually:
- ~6:42 in source — folder structure visible

Suggested judgments included in source note:
- Yes (separate section, frontmatter empty for you to fill)

Research questions logged in source note: 3

Next steps for you:
1. Review the source note in Obsidian. Read the "Suggested judgments" section.
2. Fill the actual frontmatter judgment fields with your own values (don't anchor on the suggestions).
3. Set Execution recommendation (act now / save / research / ignore).
4. Move source note out of inbox to: 03_domains/<chosen-domain>/insights/
5. Address conflicts (if any) in the existing notes.
6. Commit:
   cd second-brain && git add . && git commit -m "feat: extract source-YYYY-MM-DD-<channel>-<topic>"
```

---

## Honesty requirements

These are non-negotiable. Violations break the system's signal-to-noise.

1. **Never fabricate content to fill empty slots.** If the source didn't address something, say so. Speculative content goes in clearly-labeled sections (Speculative extensions, Inferred strategy, Constructed workflow, Suggested judgments), never mixed into factual extraction.

2. **Always label inference correctly.** Explicit / inferred / uncertain. Never promote inferred to explicit because it makes the note look stronger.

3. **Always label your own analysis as such.** "Constructed by Claude — not shown in source." "Inferred — source did not state." "Claude's analysis — not from source." If a section contains your reasoning rather than source content, it gets a label.

4. **Suggested judgments are advisory only.** Never pre-fill the frontmatter judgment fields. Always put suggestions in the body's "Suggested judgments" section with explicit "advisory only" framing. Be honest about uncertainty when current-goals.md is empty.

5. **Don't try to be impressive.** Boring, accurate, well-structured notes beat clever ones every time.

6. **Don't touch the actual judgment fields in frontmatter.** Tier, actionability score, relevance score, monetization potential, execution recommendation — these are the user's call. Always.

7. **Stop at boundaries.** Don't commit, don't push, don't move source notes out of the inbox, don't modify existing notes' core content (only append clearly-labeled new sections during the enhance flow).

8. **Pure duplicates get skipped, not backlinked.** If the source adds nothing to an existing note, don't pollute the existing note with a "this source also said this" line. Just record "same as [[existing]]" in the source note and move on.

---

## Failure modes to watch for

If you find yourself doing any of these, stop and tell the user:

- Inventing a tool name to make the "tools" section look populated
- Creating an opportunity note for something that's just a vague feeling
- Filling in tier or scores in the frontmatter (suggestions go in the body, not frontmatter)
- Moving the source note out of the inbox because it "looks done"
- Linking to a note that doesn't exist yet, hoping the user will create it later
- Skipping the existing-notes check because reading them felt slow
- Promoting a one-source observation to a pattern note (patterns require 3+ sources)
- Mixing speculative content into factual extraction sections
- Backlinking a pure duplicate to an existing note (just skip it)
- Generating suggested judgments without reading current-goals.md and project READMEs (suggestions become uncalibrated noise)

---

## Edge cases

**Transcript is metadata-only (no captions / paywalled article):**
Output a source note with metadata filled in, body marked "no extractable content yet — see research-questions for follow-up." All supporting notes: skipped with reason "no content body to extract from." Suggested judgments: based on creator/title alone, with explicit "low confidence — content not yet available" caveat.

**Transcript appears to be a different language:**
Stop and tell the user. Don't translate-and-extract; the loss of nuance is too high.

**The source seems low-quality (clickbait, no real content, ads):**
Create a minimal source note. Skip all supporting notes. Don't pretend a low-quality source produced extractable value. Suggested judgment will likely be tier 4. The user confirms.

**You're uncertain whether a tool note already exists:**
Read the suspected duplicate note before deciding. If it's a near-match, follow the enhance-or-skip logic from Phase 4.

**Existing-note enhancement could break the note's coherence:**
If appending your new section would make the existing note feel disjointed (e.g., the existing note is a tightly-structured pattern definition and your contribution doesn't fit), flag it: "Recommend the user manually integrate this insight rather than auto-append." Add the contribution to the source note's body and skip the auto-enhance.

**Visual content seems critical to understanding the source:**
Flag prominently in the report: "This source's value depends substantially on visual content not in transcript. Recommend re-watching with timestamps: ~MM:SS, ~MM:SS." Don't fabricate what was on screen.

**Source is very long (≥ 25,000 words / ≥ 2 hours):**
Use chunked extraction (Phase 2 strategy). Warn the user that synthesis across many segments may have lost some local nuance.

**current-goals.md is empty:**
Suggested judgments degrade gracefully. Be explicit in the suggestions: "Goals doc empty; suggestions based on generic relevance only. Take with extra skepticism." This signals to the user to either fill goals.md or apply their own judgment more strongly. (A missing file at the configured path is handled by Phase 1's hard-fail check, not here.)

---

## Discussions integration

The source note template includes a `## Discussions` section that lists discussion notes about this source. Discussions are a **separate artifact type** from sources, tactics, opportunities, etc — they capture questions, conversations, and reasoning *about* a source after extraction.

When writing a new source note, **leave the Discussions section as just the heading + an empty Dataview block**. Don't populate it. Discussions are created later via QuickAdd or by user request in Cowork, not during extraction.

The template's Discussions section uses Dataview to auto-list any discussion files that link back to the source — so as discussions get created, they appear in this section without manual updates.

If during extraction you identify questions worth discussing later, **put them in Research questions** (which is your dedicated channel for "things to investigate further"). Don't pre-create discussion files. The user starts discussions when they want to engage; extraction's job is to produce a clean source note that the user can come back to.

### When the user invokes a discussion

If the user explicitly asks you to "start a discussion about [X] in [source]," follow the discussion template at `second-brain/_meta/templates/template-discussion.md` and the discussion-engagement guide at `second-brain/_meta/discussions-engagement-guide.md`. That's a different workflow from extraction — read those files at that point, not during normal extraction.
