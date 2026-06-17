---
type: skill-reference
skill: opportunity-teardown
version: 1.0
created: 2026-06-16
updated: 2026-06-16
tags: [skill-reference, opportunity-teardown, level-up, frameworks, buildability-gate]
---

# Level-Up engine (§7) — design the superior version

**Creative on the idea, disciplined on the plan.** This is where the engine stops admiring the thing and designs
something better — but every "better" must survive a **hard buildability gate** or it's labelled speculative and set
aside. No fantasy.

Runs as part of the deep dive (keepers only). Input: the §6.1 teardown (especially **moat & gaps** — the gaps are the
seams a better version exploits).

## Run the framework checklist EVERY time

Walk all six lenses on every keeper, then add one wildcard. The checklist is mandatory so the engine doesn't only ever
reach for its favorite lever.

| Lens | The question it forces |
|---|---|
| **Jobs-to-be-done** | What job is the buyer really hiring this for? Is there a better way to get *that job* done? |
| **10x, not 10%** | What would make this 10× better/faster/cheaper, not incrementally nicer? |
| **Unbundle / rebundle** | Is one feature the whole value (unbundle it)? Or do scattered tools cry out to be bundled? |
| **Make the boring part disappear** | What tedious step does the user still do that could vanish entirely? |
| **Verticalize** | Take a horizontal tool and make it the killer version for one industry/persona. |
| **AI-native rebuild** | If you rebuilt this assuming today's AI as the substrate (not bolted on), what changes? |
| **Wildcard** | One free-form, outside-the-box slot. Not mechanical. |

## Output: 1–3 ranked "superior version" concepts

Pick the best 1–3 (ranked) of whatever the checklist + wildcard surfaced. Each concept carries all five parts below.
Fewer strong concepts beat three padded ones.

For **each** concept:

### 1. The creative leap
Which lever it pulls and **why it's more valuable** than the original. One tight paragraph.

### 2. What you'd have to build to make it real
The concrete components/pieces. Answer plainly: *"is this even possible, and how?"* List the parts (data, models,
integrations, UI, distribution) — not hand-waving.

### 3. A strategic build plan
A **real sequence**, not a daydream. Phased: what ships first (the thin proof), what comes next, what's the full
version. Tie phases to the crawl→walk→run logic from §6.3 where relevant.

### 4. The hard buildability gate (REQUIRED — no concept passes without it)
Name **what it would take *Oliver* to ship it with the current stack.** Be specific: which skills/tools he already has,
what's missing, rough effort (S/M/L), and the realistic first-shippable slice. If you **cannot** name a credible path
for Oliver to build it with the current or near-current stack, **label the concept `SPECULATIVE`** — it is an idea, not
a real candidate, and it does not get routed to idea-factory as buildable. State the gate verdict explicitly:
`BUILDABLE (effort: S/M/L — <how>)` or `SPECULATIVE (<what's missing>)`.

### 5. Market-crowding check on the better idea too
Are others **already doing this improved version**? Roughly how many? Still early? Run the check on **both** the
original and our version — *crowded-and-late kills more ideas than bad ideas do.* Apply the §4 no-undefended-zeros rule:
a "nobody's doing our version" claim needs ≥2 sources + an adversarial check. If our improved version is itself
crowded, say so — that may flip the recommendation back to "use as-is."

## Concept output template

```markdown
#### Superior concept <N> — <short name>  ·  rank <N of M>
- **Creative leap:** <lever + why more valuable>
- **What to build:** <components: data / models / integrations / UI / distribution>
- **Strategic build plan:** <phased sequence — thin proof → next → full>
- **Buildability gate:** BUILDABLE (effort: S/M/L — <how, with which existing stack pieces>)  |  SPECULATIVE (<missing>)
- **Crowding on this version:** <who's already doing it, how many, still early? — ≥2 sources for any "empty">
- **Evidence tags:** <verifiable / partially-verifiable / unverifiable per claim above>
```

## Discipline reminders
- The level-up does not run in the quick pass — keepers only.
- A great creative leap with no buildable path is `SPECULATIVE`, full stop. Honesty here is what keeps the registry
  full of real candidates instead of a wishlist.
- If every superior concept is either speculative or crowded, the honest output is **"the original wins — use it
  as-is"**, and that feeds straight back into the §6.2 decision.

## Related
- `[[SKILL]]` · `[[deep-dive-contract]]` (provides the moat & gaps this exploits) · `[[quick-pass-contract]]`
- spec `[[spec-opportunity-teardown-engine]]` §7
