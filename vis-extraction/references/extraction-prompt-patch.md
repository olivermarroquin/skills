# Extraction Prompt Patch — v3.1

This document describes two small updates to apply to `workspace/skills/vis-extraction/prompts/extraction-prompt.md`. Both are small enough to apply by hand; both make Phase 2 better.

---

## Patch 1 — Formalize workspace context reading

### Current text (Phase 1, item 4)

Replace this:

```markdown
4. **Active project context** — list filenames in `second-brain/04_projects/personal/` and `second-brain/04_projects/clients/_active/` so you know what the user is currently shipping. When relevant, read the README of one or two projects that look related to the source.
```

### New text

```markdown
4. **Active project + system context** — read the following at appropriate depth:

   **Directory listings only (filenames, not contents):**
   - `second-brain/04_projects/personal/` (active personal projects)
   - `second-brain/04_projects/clients/_active/` (active client work)
   - `second-brain/01_ai-operating-system/` (the user's master architecture — what's built and what's planned)
   - `second-brain/02_core/ideas/` (ideas in flight)
   - `workspace/idea-factory/` (if it exists — broader idea pipeline)

   **Read full content of:**
   - `workspace/CLAUDE.md` if it exists (top-level operating doc — high signal)
   - One or two project READMEs that look directly related to the source content
   - `second-brain/01_ai-operating-system/master-system-map.md` if the source touches system architecture

   **Skim only (open and look at headings):**
   - `workspace/ai-factory/` directory listing
   - `second-brain/01_ai-operating-system/roadmap/phase-3-plus-queue.md` (so you know what's deferred and don't surface deferred items as new ideas)

   The principle: **read directory listings broadly so you know what exists; read full file contents narrowly only when overlap is detected**. Don't try to read every file in the workspace.
```

---

## Patch 2 — Reference the canonical scoring rubric

### Current text (Phase 3, "Suggested judgments" section)

Find this section and add to it.

### Add this paragraph at the start of the "Suggested judgments" section

```markdown
**Use the canonical scoring rubric.** Read `second-brain/_meta/scoring-rubric.md` once at the start of the analysis (in Phase 1). Use those exact definitions for tier, relevance score, actionability score, and monetization potential. Don't invent your own scales. The rubric is the source of truth.

In the source note's body, include a compressed quick-reference at the top of the Suggested judgments section (the template handles this — just confirm it's present after writing).
```

### Why

Without referencing the canonical rubric, every extraction would use slightly different scales, defeating the purpose of standardization.

---

## Patch 3 — Add Action log handling

### Add this short section near Phase 7 (Write to disk), under "Source note"

```markdown
6. **Action log section starts empty.** The template includes an Action log section. When writing a new source note, leave the Action log section as just the heading + the placeholder bullet. The user fills it in over time as they act on the source.

   Do NOT auto-populate the Action log with execution-recommendation items. Those are commitments the user makes, not extractions. The user moves items from Suggested judgments / Speculative extensions / Research questions into the Action log when they decide to act.
```

---

## How to apply these patches

You have two options:

**Option A (recommended) — manual edits in your editor.** Open `workspace/skills/vis-extraction/prompts/extraction-prompt.md` in any text editor. Find the sections referenced above. Apply the changes by hand. Takes ~5 minutes.

**Option B — replace the whole file** with the v3.1 version. Skip the patch dance entirely if you'd rather just have the new file. (If you want this option, tell Claude to deliver the full v3.1 prompt instead of patches.)

After applying, verify the file is intact:

```bash
wc -l workspace/skills/vis-extraction/prompts/extraction-prompt.md
```

Should be roughly 50-80 lines longer than before depending on edit precision.

---

## Files that change in this patch round

1. `second-brain/_meta/scoring-rubric.md` — NEW canonical rubric
2. `second-brain/_meta/templates/vis/template-source-video.md` — UPDATED with Action log + rubric quick-reference
3. `workspace/skills/vis-extraction/prompts/extraction-prompt.md` — UPDATED per patches above
4. `second-brain/01_ai-operating-system/roadmap/phase-3-plus-queue.md` — UPDATED to add task-system queue item

The just-written source note (the Nate Herk one) does not have the Action log section yet. After applying these patches, manually add an Action log section to it before committing — copy the section heading and placeholder text from the template.
