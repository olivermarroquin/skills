---
type: tactic
status: extracted
created: 2026-04-28
source: "[[source-example-onboarding-agent]]"
domain: app-building
confidence: high
explicitness: explicit
actionability: 5
sources: ["[[source-example-onboarding-agent]]"]
tags: [tactic]
---

# Tactic: schema-first agent design

## What it is
Design the data schema before writing the agent's prompt. Qualification logic, scoring, and state live in the schema (Airtable, Postgres, Notion DB) — the prompt only handles conversation.

## How it works
Separating state from prompt means: prompts stay short and stable, qualification logic is editable without re-prompting, and the buyer (who often can't write prompts) can still tweak fields, scoring rules, and views.

## Where seen
- [[source-example-onboarding-agent]] — primary source, explicit

## Conditions for it to work
- Buyer or operator needs editability post-handoff
- Qualification logic is non-trivial (>3 conditional branches)
- Output needs to be queryable later (reporting, follow-up automation)

## Conditions where it fails
- Pure conversational agent with no state
- Prototype where speed > maintainability
- Schema is so simple it adds overhead

## Reusability
- [x] Can apply to my own projects
- [x] Can apply to client work
- [ ] Can apply to content (yes, as a content angle though)
- [ ] Theoretical only

## Action item
Refactor the AI Factory's own intake bot to put qualification logic in Airtable instead of in the system prompt. Estimated: 2 hours.

## Promotion path
- [ ] Confirmed across 3+ sources → promote to pattern
- Linked from: [[source-example-onboarding-agent]]
