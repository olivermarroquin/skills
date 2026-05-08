---
type: workflow
status: canonical
created: <% tp.date.now("YYYY-MM-DD") %>
domains: [knowledge-os]
tags: [workflow, promotion, enforcement]
---

# Workflow: knowledge promotion

The non-negotiable ritual that makes intelligence compound. A project is not complete until promotion has happened.

## When to run
- Project milestone complete
- Significant lesson learned (don't wait for milestone)
- 3+ sources converging on the same pattern
- Weekly review (catch anything missed)

## Inputs
- Project `.kos/lessons/` (recent additions)
- Project `.kos/execution-logs/` (last week)
- Source notes ingested this week
- Tactic notes extracted this week

## Steps

### 1. Identify candidates
Run this Dataview query in the project vault:

```dataview
LIST
FROM "lessons" OR "execution-logs"
WHERE updated >= date(today) - dur(7 days)
AND !contains(file.outlinks, "shared-intelligence")
```

Anything that hasn't been linked into shared-intelligence is a candidate.

### 2. For each candidate, ask
- Does this generalize beyond this project?
- Would I want a future project to find this?
- Is the rule clear enough to apply elsewhere?

If yes to all three: promote.
If no to any: leave in project, possibly archive.

### 3. Choose the destination

| Candidate | Promote to |
|---|---|
| "We learned X works because Y" | `05_shared-intelligence/lessons/` |
| "We discovered a reusable approach" | `05_shared-intelligence/patterns/` |
| "We built something reusable" | `05_shared-intelligence/blueprints/` |
| "We validated a workflow" | `05_shared-intelligence/workflows/` |
| "We tested a tool" | `05_shared-intelligence/tools/` |

### 4. Sanitize
Strip from the promoted version:
- Client names
- Project-specific identifiers
- Confidential business details
- Anything in `_private/`

The promoted note describes the pattern, not the case.

### 5. Link bidirectionally
The original project note must link to the promoted note. The promoted note's `Evidence` section must link back to the source case.

### 6. Update the home dashboard
The promotion log on `_HOME.md` auto-updates via Dataview. Verify your new note appears there within 24 hours.

## Outputs
- New note in appropriate `05_shared-intelligence/` folder
- Bidirectional link to source
- Frontmatter `status: promoted`
- Optional: weekly synthesis mentions the promotion

## Validation
- [ ] Note exists in shared-intelligence
- [ ] Backlinks visible in graph view
- [ ] Sanitization complete (no client/project specifics leaked)
- [ ] Original note marked `status: promoted`

## Failure modes
- "I'll promote later" — never happens
- Over-promotion — every minor observation becomes a pattern, signal-to-noise drops
- Lazy promotion — copy-paste without sanitizing or generalizing
- Orphan promotion — promoted note never gets linked from anywhere else

## Cadence target
- 2–4 promotions per week
- 0 promotions for 2+ weeks = drift indicator (raise on home dashboard)
- 10+ promotions in a week = probably noise, audit
