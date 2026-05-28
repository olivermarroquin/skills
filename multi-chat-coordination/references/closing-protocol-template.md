# Closing Protocol Template

This is the **canonical seven-step closing protocol** that DECOMPOSE mode of the multi-chat-coordination skill appends verbatim to every generated handoff. It sits inside the prompt block of each handoff, between the Status section and the `--- end prompt ---` marker, so the chat consuming the handoff sees it as part of its own instructions.

The protocol exists because prior chats forgot to update the tracker, forgot to flip handoff `status:` to `consumed`, used `git add .` instead of staging files by name, mixed inline comments into command blocks the operator was supposed to copy-paste verbatim, or just declared "done" without doing the tracker and git work. Baking the protocol into every handoff closes those gaps automatically.

## How DECOMPOSE uses this file

When generating handoffs, DECOMPOSE reads this file and inserts the entire "Template body" section below into each generated handoff. Two substitutions:

- `<HANDOFF_FILE_PATH>` → the absolute path of the generated handoff (e.g. `~/workspace/second-brain/_meta/handoffs/youtube-channel-launch/phase-2-brand-setup.md`)
- `<TRACKER_PATH>` → the absolute path of the active-chats tracker (always `~/workspace/second-brain/_meta/handoffs/_active-chats-tracker.md` unless the operator overrides)

No other transformation. The protocol body is the source of truth; DECOMPOSE does not paraphrase, condense, or reorder the steps.

## Template body (insert verbatim into generated handoffs)

```markdown
## Closing protocol (run BEFORE telling the operator the chat is done)

This protocol is **mandatory**. Do not declare the chat complete or hand control back to the operator until every step below has been executed. The operator has had to instruct prior chats to do this manually — that's the friction this section closes.

**Step 1 — Verify scope completion.**

Walk back through the "What you're building" + "Files to create" sections above. For each named deliverable, confirm it exists on disk with non-placeholder content. If anything is incomplete or contains TODO/FILL markers that should have been filled, fix it before closing. Do not declare done with known gaps.

**Step 2 — Update this handoff's frontmatter (+ YAML re-check).**

Edit `<HANDOFF_FILE_PATH>`:

- Flip `status: active` → `status: consumed`
- Add `consumed: YYYY-MM-DD` (today's date) below `created:`
- Add an "Actual deliverable" note inside a **blockquote at the top of the body** (NOT in frontmatter — the body-blockquote pattern avoids the YAML colon-space trap entirely; free-form prose with colons like "Output:", "Result:", "Built at: path", etc all parse safely inside a `> ...` blockquote)

**After editing, verify the handoff's OWN frontmatter still parses cleanly:**

```
python3 -c "import yaml, re; m = re.match(r'^---\n(.*?)\n---\n', open('<HANDOFF_FILE_PATH>').read(), re.DOTALL); yaml.safe_load(m.group(1)); print('OK')"
```

Expected output: `OK`. If it errors, the most common cause is an unquoted colon-space in the `purpose:` line, the `actual-deliverable:` line (if you put it in frontmatter — see above; prefer body blockquote), or an unwrapped apostrophe inside a single-quoted value (apostrophes inside single quotes must be doubled: `it''s`, `Catliff''s`). Re-wrap or move to body blockquote per `~/workspace/skills/multi-chat-coordination/references/handoff-frontmatter-spec.md`. The trap that bit `handoff-2026-05-26-anti-ai-slop-house-voice-skill.md` + `intel-routing-rollout/phase-2-deployment.md` (both broken until the 2026-05-28 sweep): prose values added directly to YAML frontmatter without single-quote wrapping. Body blockquote avoids the trap entirely; use it for `actual-deliverable:`.

**Step 3 — Update the active-chats tracker.**

Edit `<TRACKER_PATH>`:

- **Move** this chat's row from "Active / in-flight" to "Recently closed" with a full outcome paragraph (deliverables, decisions, gotchas, downstream unblocks, pattern candidates). The destination section is the canonical location — **do not** leave a strikethrough'd pointer in "Active / in-flight" per the move-don't-strikethrough rule established at the nineteenth-pass reorganization.
- Add a scannable one-liner to "Recently completed (past 7 days)"
- If this chat cleared a downstream chat's blocker, **move** that downstream chat from Tier-2 or Tier-3 to "Ready to spawn next" — again, move, don't strikethrough
- Update the section's callout-line item count (e.g., "1 chat currently in flight" → "0 chats currently in flight" when you remove the last in-flight row)
- If the chat cleared any other chat's blocker, promote that chat (move from queue → Ready-to-spawn OR strike-through and add a pointer)
- Bump frontmatter `last-change` value — **keep the single-quote wrapper around the value** per the "How to use this file" convention (the YAML colon-space trap has bitten the file repeatedly)

**Step 4 — Verify YAML parses cleanly.**

Run from the second-brain repo root:

\`\`\`
python3 -c "import yaml, re; m = re.match(r'^---\n(.*?)\n---\n', open('_meta/handoffs/_active-chats-tracker.md').read(), re.DOTALL); yaml.safe_load(m.group(1)); print('OK')"
\`\`\`

Expected output: `OK`. If it errors, the two most common causes are:

1. **Unquoted colon-space inside the `last-change` value** — re-wrap in single quotes per Step 3.
2. **Unbalanced apostrophes inside the single-quoted `last-change` value** — every literal apostrophe inside a single-quoted YAML string must be doubled (`it''s` not `it's`). The regex extractor in the command above correctly handles `---` literals inside the value (a naive `.split('---')[1]` would break — that variant has been retired).

**Step 5 — Identify which repos this chat touched.**

`~/workspace` is **NOT** a single git repo. It contains nested repos. The roots that matter:

- `~/workspace/second-brain/` — vault edits (handoffs, execution logs, conventions, primers, source notes, tactics, tools, patterns, READMEs, etc.)
- `~/workspace/skills/` — skill files (SKILL.md and references/ for any skill at the top level)
- `~/workspace/repos/ai-agency-core/` — shared scripts, data files, READMEs for the ai-agency-core repo
- `~/workspace/repos/<client-slug>/` — per-client repos (resume-saas, app-factory, etc.)

Identify every repo your edits landed in. You will produce one command block per repo touched.

**Step 6 — Produce copy-paste git commands.**

For each repo touched, output **exactly** this format (no inline comments, no surrounding prose — operator copies the entire block verbatim):

\`\`\`
cd ~/workspace/<repo-root>
rm -f .git/index.lock
git add <file1> <file2> <file3>
git commit -m "<descriptive multi-line message>"
\`\`\`

Rules:

- **`rm -f .git/index.lock` runs first defensively.** When Cowork sessions or background tools touch the repo, git often leaves a stale `index.lock` that blocks subsequent `git add` / `git commit` with the message `fatal: Unable to create '/path/.git/index.lock': File exists`. Including `rm -f .git/index.lock` (the `-f` flag means "no error if the file doesn't exist") at the top of every block clears this proactively, so the operator never hits the error mid-paste. The flag is safe — if no lock exists, the rm is a no-op.
- **Stage files by name explicitly.** Never `git add .` — per Oliver's standing convention (memory: `feedback_git_add_specific_files.md`), the workspace has WIP across many files; `git add .` risks staging unrelated work.
- **No inline comments** inside the command block — the operator copies the whole block as one unit. Explanatory prose goes ABOVE or BELOW the block, never inside.
- **One block per repo.** If this chat edited both `~/workspace/second-brain/` and `~/workspace/skills/`, give TWO blocks. Each block opens with its own `cd` + `rm -f .git/index.lock`.
- **Multi-line commit messages OK** via `-m "..."` syntax — describe what landed concretely (skill name, references shipped, downstream unblocks, pattern candidates). Avoid filler.
- **Never push.** Per CLAUDE.md "What NOT to Do Without Explicit Approval" — commits only; Oliver pushes.

**Step 7 — Declare the chat done.**

Tell the operator the chat is complete. Surface in a short closing message:

- One sentence on what landed
- Any open follow-ups (operator-side manual tasks, scheduled crons to register, recommended next chats)
- The git commands (from Step 6)

Only after all seven steps complete may you say the chat is done.
```

## Notes for the skill (not part of the inserted template)

- The triple-backtick-wrapped Step 4 and Step 6 blocks above are escaped with `\`\`\`` inside this template file so the outer code fence works. When inserting into a generated handoff, restore them to plain triple backticks.
- The `<HANDOFF_FILE_PATH>` substitution always uses the **absolute path** so the consuming chat doesn't need to compute it from context.
- If a chat is consumed but no git-trackable files were touched (rare, but possible for tracker-only updates that fail the YAML check and revert), Step 6 still runs — produce the block for the tracker file alone.
- If the operator opts into auto-spawn (out of scope for v1), this protocol would need a Step 8 — register the next chat as in-flight in the tracker. Not included in v1.

## Related

- `~/workspace/second-brain/_meta/handoffs/_active-chats-tracker.md` — the canonical tracker the protocol updates
- `~/workspace/second-brain/_meta/handoffs/_README.md` — handoffs folder conventions
- Memory `feedback_git_add_specific_files.md` — the standing rule behind Step 6
- Memory `feedback_running_execution_log_default.md` — companion discipline (running execution log is the substantive record; closing protocol is the bookkeeping)
