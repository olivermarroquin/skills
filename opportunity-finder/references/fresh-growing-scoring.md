---
type: skill-reference
skill: opportunity-finder
version: 1.0
created: 2026-06-17
updated: 2026-06-17
tags: [skill-reference, opportunity-finder, fresh-growing, saturation, scoring, noise-filter, no-undefended-zeros]
---

# Fresh / growing / saturation scoring (§4) — the noise filter (NEW)

This is the **genuinely-new** part of the finder. It is a **lightweight 3-factor read, not a scraping project.** Its
job is to rank a firehose of discovered candidates down to a **cap-5 shortlist** worth the operator's triage time —
biasing toward *fresh + growing + not-yet-crowded*, which is exactly where a clone-and-improve play has room.

It is deliberately cheaper than the engine's deep-dive crowding analysis (§6/§7). It uses only the cheap `raw_signal`
each lane already surfaced, plus at most one quick confirming fetch/Sonar cross-check per candidate.

## The three factors

| Factor | Question | Cheap evidence to read | Score 1–5 (5 = best for us) |
|---|---|---|---|
| **Recency** | How new is it? | launch/ship date, "new" badge, version cadence | 5 = launched/relaunched <12mo & still shipping; 1 = old + static |
| **Velocity** | Is it climbing? | upvote/review-count slope, rank climb, funding/press cadence, stars/forks slope | 5 = clearly accelerating; 1 = flat/declining |
| **Saturation penalty** | How crowded already? | # of visible direct competitors, "everyone's pushing it" signal | 5 = early, few direct competitors; 1 = crowded-and-late |

**Composite (default weights — overridable per profile in `finder-config-profiles.md`):**

```
fresh_growing_score = 0.35·recency + 0.40·velocity + 0.25·saturation_headroom
```

Velocity is weighted highest (a growing thing is the strongest "worth tearing down" signal) and means **early traction
climbing** (adoption/reviews/stars rising), not mass scale. Saturation is a **headroom** factor (high score = lots of
headroom = few competitors) and is the **contrast axis for the trending-vs-indie comparison**: trending tools cluster at
low headroom (crowded), indie/under-the-radar tools at high headroom — surfacing both side-by-side is how the finder
shows where the clone-and-improve openings are. The composite is a 1–5 number used **only to
rank** — it is not a verdict. The operator sets the bar at Gate 3.

A numeric per-factor score is optional but the **evidence behind each factor is mandatory** — a score with no cited
evidence is rejected by the quality gate.

## Hard rule — no undefended zeros (§4)

Any **"0 / nobody's doing this / fully saturated / empty / nothing found"** reading requires **≥2 independent sources +
an adversarial check** that actively tries to disprove it (`feedback_no_undefended_zeros_enumerate_sources`):

- A saturation score of 5 ("almost no competitors — wide open") from a single Sonar answer is **not allowed**. Confirm
  with a second source (a marketplace search, a WebSearch) before claiming headroom.
- A velocity of 1 ("not growing") from one stale data point is **not allowed** — soften to "no growth signal found in
  [sources checked]; not confirmed flat" and flag for the deep dive.
- The adversarial check: before finalizing any extreme score (1 or 5 on any factor), spend one query actively trying to
  **disprove** it ("are there in fact many {category} competitors?", "did {tool} actually grow this year?"). Record what
  the disproof attempt found.

A thin-sample or single-source extreme is downgraded to a mid score with a "needs deep-dive confirmation" flag, never
presented as fact.

## Evidence tagging (lightweight here)

Do not launder hype. If a growth/recency claim comes from the maker's own marketing, tag it `maker-claimed; unverified`.
Reserve the full `verifiable / partially-verifiable / unverifiable / likely-fake` tagging for the engine's deep dive,
but never present a marketing claim as a fact in a shortlist.

## Final ranking (§8) — hand off to `prioritization`

The `fresh_growing_score` is the finder's **pre-filter / triage** score. The **final cap-5 ranking** runs through the
`prioritization` skill + `_meta/scoring-rubric.md`, which folds in the broader §8 factors:

- fresh/growing score (this file),
- **build-for-myself-first fit** (first-class tag — does Oliver actually want this for his own use?),
- effort-to-clone (inverse — cheaper is better),
- money potential (short + long),
- market headroom (inverse of saturation),
- strategic fit with current focus (client-routable ideas score higher per `project_priority_client_seo_traffic`).

The finder fills the fresh/growing/headroom inputs from cheap signal; the deeper factors (effort-to-clone, money
potential) get a **first-look estimate** here and the **real** read in the engine's deep dive. The shortlist is capped
at **5 per run** (spec §4) — breadth held in check on purpose.

## Output: the shortlist row

Each shortlisted candidate is rendered for operator triage as:

```markdown
**N. <name>** — score <composite>/5  ·  [pursue / park / skip] rec
- **What it is:** <one plain sentence>
- **Fresh/growing read:** recency <r>/5 (<evidence>) · velocity <v>/5 (<evidence>) · headroom <h>/5 (<evidence>)
- **How crowded (first look):** <who else, roughly how many, still early?>  — sources: <≥2 if any zero/extreme>
- **Provenance:** <lane> · <source> · <date>
- **Why this rec:** <one line>  (Operator decides.)
```

The shortlist feeds straight into `opportunity-teardown`'s quick-pass contract — the `fresh/growing read` and
`how crowded` fields are shaped to match, so a picked keeper carries its evidence into the engine with no rework.

## Related
- `[[SKILL]]` · `[[discovery-lanes]]` (where raw_signal comes from) · `[[finder-config-profiles]]` (weight overrides) ·
  `[[dedup-rejection-sourceyield]]`
- spec `[[spec-opportunity-teardown-engine]]` §4 (this filter) + §8 (final scoring) ·
  `[[quick-pass-contract]]` (the engine field this feeds)
