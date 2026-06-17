---
type: skill-reference
skill: opportunity-teardown
version: 1.0
created: 2026-06-16
updated: 2026-06-16
tags: [skill-reference, opportunity-teardown, quick-pass-contract, teardown]
---

# Quick Pass contract (§5) — beefy preview, every candidate

The quick pass is the cheap, high-breadth tier. It runs over **everything** that arrives (Lane A manual-add in v1.0).
Its job is to let Oliver decide **"dig deeper?"** with confidence — so it is a **beefy preview, not a stub.** It is the
defense against a firehose: depth comes later, only on what survives this gate.

Produced in `quick-pass` mode and at the start of `full` mode. Output is a short markdown block (see template). Hold
**one** thing back religiously: cost. The expensive work (paid trial, visuals, full money plan, full level-up) waits for
the operator's go.

## Required fields (verbatim from spec §5)

| Field | What it must contain | Discipline |
|---|---|---|
| **What it is** | One plain sentence: what's sold/offered, and to whom. | Plain language. No jargon without a gloss. |
| **The value & the interest** | Why it's worth a look; what's genuinely innovative or clever about it. | Name the *specific* clever thing, not "it uses AI." |
| **Why it's a good idea** | The core appeal, in plain language. | The reason a real buyer cares. |
| **How it makes money** | The basic revenue mechanism. | Subscription / usage / one-time / marketplace take / ads — name it. |
| **Fresh / growing read** | The §4 three-factor score (recency · velocity · saturation penalty) + the evidence behind it. | Lightweight, not heavy scraping. Cite what you looked at. |
| **How crowded** | First-look saturation: is anyone else doing this, roughly how many, is it still early? | A first look, not the full crowding analysis (that's deep-dive/level-up). |
| **Provenance** | Lane + source + date. | Always present. Lane A = "operator manual-add." |

## The "fresh + growing" score (§4) — how to fill the fresh/growing field

A lightweight 3-factor read, **not** a scraping project:

1. **Recency** — how new is it? (launch/ship date, "new" badges, version cadence.)
2. **Velocity** — is it climbing? (rank climb, review-count slope, upvotes, funding/press cadence; stars/forks slope
   for repos.)
3. **Saturation penalty** — how many people already push it? Crowded-and-late is penalized.

Express as a short qualitative read (e.g. "fresh: launched <2y, still shipping weekly; growing: review count climbing;
moderately crowded: 4–6 visible direct competitors") plus the evidence you used. A numeric 1–5 per factor is optional;
the **evidence is mandatory.**

## Hard rule — no undefended zeros (§4)

Any "0 / empty / nobody's doing this / fully saturated" reading requires **≥2 independent sources + an adversarial
check** that actively tries to disprove it (`feedback_no_undefended_zeros_enumerate_sources`). A single-source or
thin-sample zero is not allowed in a quick pass — soften to "not found in [sources checked]; not confirmed absent" and
flag it for the deep dive.

## What the quick pass deliberately holds back (cost control)

Do **not** produce any of these in a quick pass — they belong to the deep dive only, after the operator flags a keeper:

- the paid hands-on trial recommendation,
- diagrams / visuals,
- the deep business / money / go-to-market plan,
- the full level-up (frameworks + superior-version concepts).

## Evidence tagging (lightweight here, strict in the deep dive)

Even in the quick pass, do not launder hype. If a growth or revenue claim comes from the maker's own marketing, say so
("maker-claimed; unverified"). Reserve the full `verifiable / partially-verifiable / unverifiable / likely-fake`
tagging for the deep dive, but never present a marketing claim as a fact here.

## Output template

```markdown
### Quick Pass — <candidate name>
**Profile:** product/offer · **Mode:** quick-pass · **Date:** YYYY-MM-DD

- **What it is:** <one plain sentence>
- **The value & the interest:** <the specific clever/innovative thing>
- **Why it's a good idea:** <core appeal in plain language>
- **How it makes money:** <revenue mechanism>
- **Fresh / growing read:** <recency · velocity · saturation, with the evidence used>
- **How crowded:** <first-look saturation: who else, roughly how many, still early?>
- **Provenance:** <lane + source + date>

**Gate recommendation:** pursue / park / skip — <one-line why>. (Operator decides.)
```

End every quick pass with a **gate recommendation** (pursue / park / skip) and a one-line reason — but the operator
makes the call. The engine proposes; the operator disposes.

## Related
- `[[SKILL]]` (the engine) · `[[deep-dive-contract]]` (the next tier) · `[[profiles]]` (what config drove this)
- spec `[[spec-opportunity-teardown-engine]]` §4 (noise filter) + §5 (this contract)
