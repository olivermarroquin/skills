---
name: vis-extraction
description: Extract structured intelligence from videos, articles, transcripts, and other long-form content into Oliver's Knowledge OS vault. Triggers on phrases like "ingest this video," "extract this URL," "process this transcript," "pull and extract from a URL," "analyze this article," "ingest this source," "run VIS on this," or any time the user provides a YouTube URL, web article URL, or local transcript file and wants a structured source note plus extracted artifacts (tools, tactics, opportunities, content ideas) written into the second-brain vault. Also use when the user mentions adding a video/article/talk to their vault, or when they paste a URL with no other instruction in a Knowledge OS context. This is the primary path for converting external content into vault artifacts.
---

# VIS Extraction Skill (v1.1)

The Video Intelligence System (VIS) extraction skill. Wraps the `transcript-pull.sh` script and the v3.2 extraction prompt into a single workflow. Pull a transcript, run extraction, write structured notes to the vault.

**Critical behavior (read this before anything else):**
- **Cache and dedup are first-class.** Before pulling a transcript, check the cache. Before running an extraction, check whether the source already exists in the vault. Don't silently re-extract or overwrite the user's calibrated work.
- **Sandbox network may be limited.** If the sandbox can't reach a URL, route the pull to the user's host machine — don't fake the work.
- **Stop at the review gate by default.** Training mode is the default. Only skip review when the user explicitly says "auto."

## Core workflow

When invoked, follow these steps in order. Stop and ask the user only when explicitly required.

### Step 1 — Identify the input

The user gave you one of:
- A YouTube URL (most common): `https://www.youtube.com/watch?v=...` or `https://youtu.be/...`
- An article URL: any other `https://` URL
- A local file path: `/path/to/transcript.md` or similar — usually a previously-pulled transcript or an uploaded text file

If the input is ambiguous (e.g., user said "ingest the latest one"), ask which URL or file they want.

### Step 2 — Identify the mode

Default mode: `training` (stops at the Phase 6 review gate; user approves before write).

Override: if the user explicitly says "auto," "auto mode," "no review," or "skip the review," use `auto` mode (writes immediately after extraction, no review gate).

If the user doesn't specify, default to `training`.

### Step 3 — Capture optional "why ingested" note

If the user provided a one-liner explaining why they're ingesting this source (e.g., "want to compare this against my migration pipeline"), capture it. It goes in the source note's "Why ingested" field.

If they didn't provide one, leave the field empty — don't ask for it. The user can fill it later, or it can stay empty.

### Step 4 — Pull the transcript

The transcript-pull script may run in different contexts with different network capabilities. Handle three scenarios:

**Scenario A — Cache hit (fastest path):**

Before running the pull, check if a transcript for this URL already exists in the cache:

```bash
ls -t /Users/olivermarroquin/workspace/skills/vis-extraction/cache/*.md 2>/dev/null | head -5
```

If a recent transcript file exists matching the source's video ID or article slug, use it directly. Skip to Step 5 with the cached filename. Tell the user: "Found a pre-existing cached transcript for this exact source from [date]. Using it rather than re-pulling."

**Scenario B — Sandbox can fetch (one-step path):**

Try running the script:

```bash
cd /Users/olivermarroquin/workspace/skills/vis-extraction/scripts
./transcript-pull.sh "<URL-or-path>" ../cache
```

If this succeeds, capture the output filename and proceed to Step 5.

**Scenario C — Sandbox network blocked (two-step path):**

If you see errors like:
- `connection not allowed by ruleset`
- `403 Forbidden ... blocked-by-allowlist`
- `x-deny-reason: blocked-by-allowlist`
- `ERROR: [youtube] ...: connection not allowed`

The sandbox cannot fetch the source. **Do not retry.** Instead, surface this to the user and instruct them to run the pull on their host machine. Provide the exact command:

```
The sandbox can't reach <domain>. Please run this in your Mac terminal:

  cd /Users/olivermarroquin/workspace/skills/vis-extraction/scripts
  ./transcript-pull.sh "<URL>" ../cache

Then paste the resulting filename back to me. I'll continue from Step 5.

(The output will be at /Users/olivermarroquin/workspace/skills/vis-extraction/cache/transcript-YYYY-MM-DD-HHMMSS-<slug>.md)
```

Wait for the user to provide the filename, then proceed to Step 5 using that filename.

**For local file inputs (user provided a path, not a URL):**

Local files don't need network. Run the script normally — it produces a copy in cache with proper frontmatter. If for some reason the script fails on a local file, just use the original file path; the extraction can read from anywhere on disk.

### Step 5 — Read the extraction prompt and scoring rubric

These are mandatory pre-extraction reads:

```bash
cat /Users/olivermarroquin/workspace/skills/vis-extraction/prompts/extraction-prompt.md
cat /Users/olivermarroquin/workspace/second-brain/_meta/scoring-rubric.md
```

The extraction prompt is v3.2. It defines all 8 phases of the extraction. The scoring rubric is canonical for tier/relevance/actionability/monetization values.

### Step 6 — Run the extraction

Following the v3.2 extraction prompt, execute the 8 phases:

1. **Phase 1 — Context gathering.** Read templates, conventions, broad workspace context (CLAUDE.md, current-goals.md per Phase 1 step 3 of the extraction prompt, project READMEs, existing-note index from the vault).
2. **Phase 2 — Chunking decision.** Determine attention mode:
   - <9,000 words → single-pass
   - 9,000-25,000 words → focused-attention
   - ≥25,000 words → chunked
3. **Phase 3 — Source analysis.** Apply global writing rules (acronym expansion on first use; plain-English coverage at top + 4 jargon-section callouts). Produce all structured analysis. **Also produce a "Structured action items" block organized by kind (experiment / decision / comparison / research / adoption / conditional)** — apply the four-rule inclusion gate (decidable outcome, specific enough to act on, generalizes beyond pattern-watching, actionable to the operator). Soft cap at 8-10 items per source; surplus stays in legacy sections.
4. **Phase 4 — Existing-note check.** Dedup-and-enhance pass against vault content.
5. **Phase 5 — Conservative-creation gate.** Apply the "would this note be useful 3 months from now" filter.
6. **Phase 6 — Review gate.** In `training` mode: STOP and present structured summary including the new "Proposed structured action items" approval block. Wait for user approval. In `auto` mode: skip directly to Phase 7.
7. **Phase 7 — Write to disk.** Write source note to `00_inbox/sources-pending/`, supporting notes to their canonical locations. **Materialize approved structured action items as task notes in `06_tasks/`** with `extracted-via: vis-phase6` and `source: [[<source-note>]]`. Set `attention-mode` in frontmatter. Leave the source note's "Action log" Dataview block in place (it auto-populates from the new task notes). Leave Discussions section's Dataview block in place.
8. **Phase 8 — Report.** Generate the structured report (see "Final report format" below).

**Do NOT touch git.** The user commits manually after inspecting on disk.

### Step 7 — Generate the final report

The final report goes in the conversation, not in the vault. Format below.

## Final report format

After all writes complete, produce a report with this structure:

```
EXTRACTION COMPLETE

Source: <filename>.md
        → <full-path-relative-to-vault>
- Source-type: <video|article|transcript>
- Mode: <training|auto>
- Word count: ~<N> (file total)
- attention-mode: <single-pass|focused|chunked>
- Frontmatter judgment fields: empty (your call)
- Action log: placeholder only

Created (NEW notes):
- <list of new notes with brief 1-line descriptions and links>
- Task notes in 06_tasks/ (if any approved at Phase 6): N total — experiments=N, decisions=N, comparisons=N, research=N, adoptions=N, conditional=N

Enhanced (existing notes that grew):
- <list of enhanced notes with brief description of what was added>

Linked to existing (no changes to those notes):
- <list of linked notes>

Skipped (with reasons):
- <list of skipped extractions with brief reasons>

Conflicts flagged for your review:
- <list of any architectural conflicts surfaced for user decision>

Visual signals to investigate manually:
- <list of timestamps where visual content seemed important, or "none" for articles>

Suggested judgments included in source note:
- Yes (separate body section; frontmatter empty for you to fill)
- TL;DR: tier <N>, actionability <N>, relevance <N>, monetization <high|medium|low|none>
- Execution recommendation: <Act now|Save for later|Research deeper|Ignore|mixed>

Research questions logged in source note: <count>

Pattern candidates surfaced:
- <list of pattern candidates with their N/3 progress>

Files written / modified:
A  <path>
A  <path>
M  <path>
...

Next steps for you:
1. Review the source note in Obsidian — read the Suggested judgments section.
2. Fill the actual frontmatter judgment fields (tier, relevance-score, actionability-score, monetization-potential) with your own values.
3. Set the Execution recommendation checkboxes.
4. Move the source note out of inbox to <recommended-destination> once judgments are filled.
5. Commit (when ready, run yourself):

   cd /Users/olivermarroquin/workspace/second-brain && git add . && git commit -m "feat: extract <source-filename>"
```

## What this skill does NOT do

- Does NOT commit to git. User runs the commit command after inspecting.
- Does NOT push to GitHub. User pushes when ready.
- Does NOT move source notes out of `00_inbox/sources-pending/`. User does that after filling judgment fields.
- Does NOT auto-update existing source notes (e.g., bumping `updated:` field) just because a related extraction happened.
- Does NOT chase pattern promotions. If a pattern reaches 3/3, surface it as a candidate; don't auto-create the pattern note.
- Does NOT read or modify discussion files. Discussions are a separate workflow (see `_meta/discussions-engagement-guide.md`).

## Edge cases

**Local file with no metadata:** If the user gave a local file (not a URL), the transcript-pull script will produce a transcript with minimal frontmatter. The extraction proceeds normally; the source note's frontmatter will have empty `url`, `creator`, `published` fields — that's fine, the body content carries the value.

**Re-extracting an already-extracted source:** If the user is re-running on a source you've already extracted (filename collision), report this as a problem and ask whether to overwrite, append-as-update, or skip. Don't silently overwrite.

**Empty or near-empty transcript:** If the transcript file is <500 words, the source likely failed to extract usefully. Report this and ask whether to proceed with a minimal source note or abort.

**User says "auto" mode but you have low confidence:** If you're in auto mode but the source has unusual characteristics (very long, very short, low quality, conflicting evidence with vault content), surface a brief flag in the report rather than silently writing low-quality artifacts. Auto mode skips the review gate but doesn't suspend judgment.

**Skill invoked without a URL or path:** If the user invokes the skill without specifying a source, ask which URL or file they want extracted.

## Reference files

The actual content this skill operates on lives outside the skill folder:

- **Transcript pull script:** `/Users/olivermarroquin/workspace/skills/vis-extraction/scripts/transcript-pull.sh`
- **v3.2 extraction prompt:** `/Users/olivermarroquin/workspace/skills/vis-extraction/prompts/extraction-prompt.md`
- **Scoring rubric (canonical):** `/Users/olivermarroquin/workspace/second-brain/_meta/scoring-rubric.md`
- **Source-video template:** `/Users/olivermarroquin/workspace/second-brain/_meta/templates/vis/template-source-video.md`
- **Vault root:** `/Users/olivermarroquin/workspace/second-brain/`

Read these as needed. The extraction prompt is the authoritative spec; this SKILL.md is the orchestration layer.
