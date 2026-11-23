---
type: reference
status: active
created: 2026-11-23
updated: 2026-11-23
purpose: Required-sections manifest for sections-check.py (T1 + T2, VIS Phase 8)
source-spec: skills/vis-extraction/prompts/extraction-prompt.md v3.7
drift-test: grep exact header strings against extraction-prompt.md; any string not found = manifest drift
tags: [vis-extraction, sections-check, manifest, phase-8]
---

# VIS Required-sections Manifest

**Source spec:** `extraction-prompt.md` v3.7 — this manifest enforces mandates that already exist in
the spec. Do not modify the manifest without first verifying the mandate still exists in the spec
(and vice versa: if the spec mandate changes, update this file and `sections-check.py`'s MANIFEST dict).

---

## Short-form notes

Type slug: `short`
Description: Short-form video note (social reels, Shorts, TikToks ≤ ~5 min)

| Section header | Mandate | Source in extraction-prompt.md |
|---|---|---|
| `## Operator follow-ups` | ALWAYS present | §short-form Step 4: "This section is **ALWAYS present** for social reels." |

**Drift test:** `grep -n "ALWAYS present" prompts/extraction-prompt.md` must return Step 4.

---

## Standard notes

Type slug: `standard`
Description: Standard source note (long-form video, article, course, podcast)

| Section header | Mandate | Source in extraction-prompt.md |
|---|---|---|
| `## Suggested judgments` | Always generated (Phase 3) | §Suggested judgments (Phase 3): advisory block generated for every note |
| `## Related notes` | Required for every source note | Phase 7 §8: "Every source note must link to: (a) a parent context … (b) at least one peer artifact" |
| `## Second-squeeze delta` | MANDATORY Phase 4b | Phase 4b: "Record every pass in the note's `## Second-squeeze delta` table … Row 1 is the inventory extraction." |

**NOT in manifest (conditional):**
- `## Structured action items` — inclusion gate: "An observation rises to a structured action item only if [all 4 criteria met]." Present only when qualifying items exist; absent by design when no items qualify.
- `## Verbatim prompt library` / `## Prompt library (from source)` — use note type `prompt-library` instead.

**Drift test:**
- `grep -n "Every source note must" prompts/extraction-prompt.md` must return Phase 7 §8.
- `grep -n "MANDATORY" prompts/extraction-prompt.md` must include Phase 4b "Second squeeze".

---

## Prompt-library notes

Type slug: `prompt-library`
Description: Note where transcript contains demonstrated AI prompts (shown, spoken, or screen-shared verbatim)

| Section header | Mandate | Source in extraction-prompt.md |
|---|---|---|
| `## Prompt library (from source)` | Mandatory when present | Phase 3: "mandatory when present: when the source speaks, shows, or demonstrates actual AI prompts … extract them **verbatim** … in a `## Prompt library (from source)` section" |

**Detection:** Transcript grep for prompt-quoting cues (screen-share of a prompt, "here's the prompt I use", speaker reads aloud a full instruction block). Ambiguous cases → WARN-tier (ask operator before requiring the section).

**Drift test:** `grep -n "mandatory when present" prompts/extraction-prompt.md` must return Phase 3 verbatim prompt library instruction.

---

## Enforcement

`sections-check.py` (sibling script in `scripts/`) implements these rules as a deterministic check.
Missing mandatory section → exit 1 (structure failure), naming the section.
Stub action entries → exit 2 (content failure), naming the entry.

Auto-proceed gate integration (SKILL.md §Auto-proceed policy, Phase 2):
- Signal 2a: `python3 scripts/sections-check.py <note> --type <type>` → missing section = PARK
- Signal 2b: `python3 scripts/sections-check.py <note> --type <type> --content` → stub entry = PARK
- Signal 2c: `python3 scripts/oql_signal2.py <verdict-json>` → score < 80 = PARK

All three must pass before auto-proceed. Failure at any step = PARK naming the failing check.

---

## Calibration

As of 2026-11-23 (VIS Phase 8):
- Pre-patch short fixture: missing `## Operator follow-ups` → exit 1 ✓ (T4a regression)
- Patched short + 4 released standard notes: `--stubs-only` all 5 PASS ✓ (T4b calibration)
- Released standard notes (URLs 1–4): missing `## Related notes` and `## Second-squeeze delta` → these are REAL gaps from pre-Phase-8 extractions, not false parks. Notes need amendment to pass the full structure check going forward.
