# Fixture: chat-close-missing-exec-log

**Tests:** G-chat-close OC-1 — a multi-step build chat that reaches close with no execution log.

**Setup:** A synthetic build chat (chat ID `fixture-build-no-exec-log`) with:
- Originating handoff at `artifact/handoff.md` (type: handoff, tags: [handoff, build, fixture])
- 5 steps of work described in the handoff (multi-step → OC-1 applies)
- No `execution-log-*.md` file anywhere in this fixture directory

**Planted defect:** The execution log simply does not exist. OC-1's procedure `ls`es the
expected path and finds nothing. The `artifact/` directory contains only the handoff — no
exec log.

**Expected outcome:** OC-1 fires → BLOCKING. The gate prevents close until the exec log
is written.

**Regression for:** WF-1 gap #1 (exec log rationalized away at close — "decision-record +
changelog as sufficient"); S&H wave A2 (same class, 06-03).
