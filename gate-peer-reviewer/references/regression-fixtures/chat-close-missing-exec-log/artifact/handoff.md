---
type: handoff
status: active
created: 2026-01-01
updated: 2026-01-01
tags: [handoff, build, fixture]
---

# Fixture handoff — synthetic build chat (multi-step, no exec log)

> This is a synthetic fixture for regression testing G-chat-close OC-1.
> It represents a multi-step build chat that reaches close without an execution log.

## What must be built

1. Scaffold the widget component
2. Wire the API integration
3. Add unit tests
4. Update the SKILL.md references
5. Run the quality loop

## Definition of Done

- Widget component exists at `src/widget.tsx`
- API integration tested
- SKILL.md updated
- Execution log written

## Notes

This handoff describes 5 steps of work — well above the OC-1 threshold of 3+ steps.
The fixture deliberately omits any `execution-log-*.md` file so OC-1's `ls` finds nothing.
