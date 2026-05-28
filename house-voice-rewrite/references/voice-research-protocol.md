# Voice research protocol

The step-by-step workflow for `init-personality` Mode 1 — researching the
proven-editorial corpus and extracting voice patterns for a domain.

This protocol is what makes the house voice "proven-to-rank" rather than
"authentically client." The corpus consists of pages that are ALREADY
ranking and reading as human in the client's domain. We extract the
voice patterns from those pages and synthesize them into a single house
voice.

## When to run

- One-time per client at onboarding (after the client folder is scaffolded)
- Quarterly refresh per client (compare new corpus to existing personality
  file; surface drift)
- On-demand when the operator says "refresh the personality for [client]"
  or "re-research the voice for [domain]"

## Inputs

- **Client name** (e.g., "EV Electric Services")
- **Domain string** (e.g., "residential electrical")
- **Geographic frame** (e.g., "Northern Virginia," "Fairfax County")
  — pulled from client folder if not passed explicitly
- **Target client folder path** for output

## Phase 1 — Build the seed query list

Generate 6-10 high-value SEO queries in the client's domain. Mix of:

- **High-intent commercial:** "[service] cost," "[service] near me,"
  "[service] [geography]"
- **Symptom-led:** "[problem symptom]," "why does my [thing] [problem]"
- **Educational:** "how to know when to [action]," "what is [domain term]"
- **Brand-named:** "[notable problematic brand] [issue]" (e.g.,
  "Federal Pacific panel replacement")

Example seed query list for residential electrical:

1. "electrical panel upgrade cost"
2. "how to know when to upgrade electrical panel"
3. "Federal Pacific panel replacement"
4. "200 amp panel upgrade"
5. "Zinsco panel dangers"
6. "EV charger installation cost"
7. "why does my circuit breaker keep tripping"
8. "electrician [geography]" (substitute geography)

For other domains, swap the service-specific queries but keep the
intent mix (commercial + symptom + educational + brand-named).

## Phase 2 — Run the queries and collect candidate sources

For each seed query, run WebSearch and collect the top 5 organic results.
Note: AI Overviews and ads don't count — we want the organic SERP.

Per query, evaluate each result against the exclusion rules below. Keep
the ones that pass; drop the ones that fail.

### Exclusion rules

Drop the result if any of these are true:

- **Reads as AI-generated.** Hallmarks: generic phrasings ("In today's
  modern world..."), soft hedging without specifics, no named entities,
  no real prices, no real case studies, every paragraph the same shape.
- **Directory page.** Yelp, BBB, Angi, HomeAdvisor listings without
  editorial content.
- **Pure lead-gen.** A page that's just hero + CTA + form, no editorial
  body.
- **Forum thread.** Reddit, Quora, contractor forums — different voice
  register that doesn't generalize.
- **Wrong domain.** The result is about a different service or in a
  different industry vertical.
- **Paywall.** Can't read the content, can't extract the voice.

### Keep rules

Prefer results that have:

- Named entities (brands, places, code references, prices)
- Paired before/after scenarios (problem described, solution explained)
- Real prices stated as ranges with the basis explicit
- Editorial column structure (introduction → exposition → conclusion or
  next-step)
- Clear authorship or editorial-team attribution
- A "last updated" date within the last 18 months

## Phase 3 — Add national-editorial anchors

In addition to the SERP-pulled corpus, deliberately add 2-4 articles
from established home-improvement editorial publications:

- **This Old House** (thisoldhouse.com) — long-form editorial standard
  for residential trade content
- **Family Handyman** (familyhandyman.com) — DIY-leaning but with strong
  specificity markers
- **Bob Vila** (bobvila.com) — older brand, varies in quality, can be
  useful as anchor
- **The Spruce** (thespruce.com) — general home content; pull only the
  editorial pieces, skip the listicles
- **Consumer Reports** — when relevant for safety/recall content

These anchors aren't always in the SERP for local-service queries
(geography filters them out), but they establish the editorial-norm
voice for the domain. Add 2-4 for triangulation.

Search query pattern: `site:thisoldhouse.com [topic]` — restrict to the
publication, then pick the best 1-2 results.

## Phase 4 — Add local-newspaper anchors (if findable)

If the client's geography has a local newspaper with a home-improvement
column, search for 1-2 columns relevant to the domain. For Northern
Virginia, candidates: Washington Post home section, Northern Virginia
Magazine, Reston Now home columns.

These are often hard to find — skip the phase if 30 minutes of search
yields nothing. The national-editorial anchors carry most of the
weight; local-newspaper anchors are nice-to-have, not critical.

## Phase 5 — Add industry-association anchors

1-2 editorial pieces from industry associations relevant to the domain.

For residential electrical:
- **NECA** (National Electrical Contractors Association) — necanet.org
- **IAEI** (International Association of Electrical Inspectors) —
  iaei.org

For plumbing:
- **PHCC** (Plumbing-Heating-Cooling Contractors Association)

For HVAC:
- **ACCA** (Air Conditioning Contractors of America)

Find their editorial/blog sections and pull 1-2 articles per association
that have substantive editorial content (not pure regulatory bulletins).

## Phase 6 — Extract voice patterns

The final corpus should be 8-15 sources. For each source, read the full
article (don't summarize from snippets) and extract:

### 6.1 — Sentence rhythm

Sample 3 short sentences (8-15 words), 3 medium (15-25), 3 long (25-40)
from each source. Note the pattern — short-medium-medium, long-short-
medium, etc.

### 6.2 — Vocabulary density

Count technical terms per paragraph in 3-5 sample paragraphs per source.
Note glossing patterns — do they gloss on first use? Do they assume the
reader knows the term?

### 6.3 — Specificity markers

For each source, note:
- Are brands named?
- Are places named?
- Are prices stated as real ranges with basis?
- Are code references cited?
- Are scenarios told as scenes or as abstractions?

### 6.4 — Voice register

Single-sentence characterization per source. Examples:
- "Consultative expert with mild authority"
- "Direct trade-press voice, opinion-bearing"
- "Editorial column tone, scene-setting heavy"

### 6.5 — Opinion markers

Note 2-3 examples per source of the writer taking positions, hedging,
acknowledging trade-offs, or refusing to recommend.

### 6.6 — Anti-patterns

Note what the source does NOT do — generic openings absent, soft hedging
absent, etc. These are the negative-space patterns the personality file
should also avoid.

## Phase 7 — Synthesize into a single house voice

Don't average — synthesize. The personality file should encode ONE
coherent voice that matches the editorial norms of the domain, not the
lowest common denominator across the corpus.

Rules of synthesis:

1. **Pick the dominant register.** If 70% of the corpus is consultative-
   expert and 30% is folksy-DIY, the personality is consultative-expert.
   The minority style gets noted as "occasional" or dropped.
2. **Specificity markers always rise to the top.** Any specificity
   pattern that appears in 50%+ of the corpus becomes a personality
   requirement.
3. **Pick the strictest anti-pattern set.** If one source bans generic
   openings and another tolerates them, the personality bans them.
   Anti-patterns are union, not intersection.
4. **Sentence rhythm: pick the modal pattern.** If most sources use
   medium-short-medium for problem paragraphs, that's the personality's
   problem-paragraph pattern.
5. **Opinion markers: pick the medium-strong default.** Don't go to the
   most opinionated source's level (that's risky for trust); don't go to
   the most neutral source's level (that reads as filler). Medium-strong
   opinion is the right calibration for residential-service editorial.

## Phase 8 — Add the client-grounding layer

Read the client folder for entity facts:

- `<client>/_status.md`
- `<client>/business-context/`
- `<client>/credentials.reference.md`
- Bridge-tactic files for service offerings
- Any decision docs that constrain voice (e.g., the "no pricing" decision
  for EV Electric)

Fill the client-grounding section of the personality template. This is
SHORT — service-area cities, owner name + credentials, named-brand stack,
phone number, permit offices, utility coordinator, non-negotiable
phrasings.

If a field is missing from the client folder, flag it for the operator
rather than guessing.

## Phase 9 — Write the personality file

Use the template at `references/personality-template.md`. Output to
`~/workspace/second-brain/04_projects/clients/_active/<client>/personality-<client>.md`.

Frontmatter:
- `source-corpus-snapshot:` = today's date
- All other fields per the template

## Phase 10 — Surface for operator review

Present the file via `mcp__cowork__present_files`. Briefly tell the
operator:
- How many sources the corpus contained
- The 2-3 voice traits that came through strongest in the synthesis
- Any client-folder gaps that were flagged
- Recommended next step (review the file, then run `rewrite` on a test
  draft)

## Cost estimate

Per init-personality run:
- 8-12 WebSearch queries (seed queries + per-source full reads)
- 8-15 page reads (sometimes via WebFetch if SERP snippet wasn't enough)
- Total chat-time: 15-25 minutes
- No per-query API cost — uses WebSearch and WebFetch, which are
  available tools

This is a one-time cost per client (with quarterly refresh as the
recurring cost).

## Failure modes

- **Thin corpus.** If the domain is niche and the SERP isn't producing
  8+ editorial sources, expand to adjacent queries OR drop the geography
  constraint and pull national-only content. Don't ship a personality
  file built from <6 sources.
- **All sources read as AI-generated.** This is the "AI slop saturation"
  failure mode — the domain's SERP is dominated by AI content. In that
  case, lean harder on the national-editorial anchors and the industry-
  association anchors; the SERP corpus may need to drop entirely. Flag
  to the operator: "Domain SERP is AI-saturated; personality built
  primarily from editorial-publication anchors."
- **Voice patterns don't converge.** If the corpus's voice patterns
  contradict each other (consultative-soft vs. blunt-trade), pick the
  pattern that matches the client's actual customer profile (homeowner-
  decision-maker → consultative-expert; commercial-contractor → blunt-
  trade) and note the divergence in the personality file's source
  corpus section.
