# Fixture: chat-close-missing-version-paperwork

**Tests:** G-chat-close OC-10 — a skill-build chat that edits a SKILL.md but ships without
version bump, changelog entry, or event-log row.

**Profile tested:** skill-build (non-WF chat type — proves profiles work beyond the WF seed
corpus, satisfying acceptance criterion A2).

**Setup:** A synthetic skill-build chat (chat ID `fixture-skill-build-no-paperwork`) with:
- Originating handoff at `artifact/handoff.md` (type: handoff, tags: [handoff, skill-build, fixture])
- A SKILL.md at `artifact/SKILL.md` that was edited (new reference `new-reference-added-by-chat.md`
  added to the index on line 17)
- Version field unchanged (still reads `version: 1.0` — should be 1.1)
- No new changelog entry in the version history section (only the original v1.0 entry)
- No event-log row with a version bump

**Planted defect:** All three version-paperwork elements missing. OC-10's procedure checks:
1. `version:` in frontmatter bumped vs prior → NOT bumped (still 1.0) → BLOCKING
2. Changelog entry in version history → MISSING (no v1.1 entry) → BLOCKING
3. Event-log row → MISSING → BLOCKING

**Expected outcome:** OC-10 fires → BLOCKING. The gate prevents close until all three
paperwork elements are present.

**Regression for:** competitor-deep-research v1.1 close (missing version paperwork caught
only by operator-applied review, 06-03). Also proves the skill-build profile works
independently of the planning/decision and build profiles tested by the WF-1 and COA-4b
seed corpora.
