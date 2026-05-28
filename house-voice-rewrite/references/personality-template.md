# Personality file template

Use this template structure when `init-personality` produces a per-client
personality file. Every section is required; the content is filled in
from research findings.

The output path is
`~/workspace/second-brain/04_projects/clients/_active/<client>/personality-<client>.md`.

---

```markdown
---
type: personality
status: active
created: YYYY-MM-DD
updated: YYYY-MM-DD
client: <client-slug>
domain: <domain-string>
built-from: house-voice-rewrite init-personality
source-corpus-snapshot: YYYY-MM-DD
tags: [personality, house-voice, anti-ai-slop, <client>, <domain>]
---

# Personality — <Client Name> (<Domain>)

> Voice specification for every page Keelworks ships for <Client>. Built
> from researched proven-SEO editorial sources in the <domain> domain.
> Source corpus is not the client's own writing — it's the editorial
> conventions of the real-editor content that's already ranking and
> reading as human. The client-grounding layer at the bottom attaches
> entity specifics so the voice produces content about <Client>
> specifically, not a generic <domain> business.

## 1. Source corpus (one-time research snapshot, dated YYYY-MM-DD)

The 8-15 editorial sources this voice was extracted from. Each entry
is a single line: URL, what kind of source, what voice signal it
contributed.

- [URL] — This Old House cost guide — sentence rhythm, consultative voice
- [URL] — Family Handyman DIY editorial — specificity markers, named brands
- [URL] — Top organic SERP result for "[query]" — H2-as-question
  pluckable structure
- ... (8-15 entries)

The snapshot date in frontmatter (`source-corpus-snapshot:`) marks when
this research ran. When the personality refreshes, the new snapshot date
goes here.

## 2. Voice register

Two or three sentences describing the overall feel. Examples:

- "Expert-but-accessible. The writer is the master electrician who's seen
  this exact panel a hundred times and isn't going to lecture, but
  isn't going to dumb it down either. Direct, not consultative-soft.
  Takes positions on which approach beats which."
- "Editorial home-improvement column tone — like the New York Times's
  Tip column. The writer assumes the reader is a homeowner trying to
  make an informed call, not a tradesperson. Names things, prices
  things, walks through trade-offs."

What pronouns dominate? Usually "you" (addressing the homeowner) plus
"we" (the business). "The homeowner" appears occasionally in third-person
explanations.

## 3. Sentence rhythm

Sample patterns from the corpus, with examples.

**Short sentences** (8-15 words):
- "Federal Pacific panels don't always trip when they should."
- "The price moved from $2,400 in 2018 to $3,200 today."
- "You won't always see scorching, but the breakers don't latch right."

**Medium sentences** (15-25 words):
- "If the panel was installed before 1980 and the house has Federal Pacific
  or Zinsco branding on the breaker handles, it should be replaced."
- "Most Northern Virginia panel upgrades from 100A to 200A run $2,800-$3,800
  with permit, Dominion coordination, and county inspection included."

**Long sentences** (25-40 words):
- "When a homeowner in McLean calls about flickering kitchen lights and
  the panel is a 1972 Federal Pacific Stab-Lok, the conversation isn't
  about whether to upgrade — it's about which afternoon next week we can
  pull a permit and stage the parts."

**Pattern observed across corpus:** medium-short-medium for problem
paragraphs; long-short-medium for scene-setting; bullet-then-paragraph
for service-list sections.

## 4. Vocabulary density

How many technical terms appear per paragraph? How are they glossed?

- **Domain-jargon ratio:** 2-3 specific terms per paragraph (panel
  amperage, breaker brand, code reference, neighborhood name)
- **Glossing rule:** if the term is one a homeowner wouldn't know
  cold ("AFCI," "load calculation," "service mast"), gloss inline on
  first appearance in plain language. Subsequent uses don't need
  re-glossing.
- **Code references:** name the relevant section ("NEC 2020 Article
  408," "Virginia USBC R3603.7") when it's load-bearing for the claim.
  Don't cite code-as-decoration.
- **Brand names:** name the specific brand whenever the brand matters
  to the claim. Square D, Eaton, Siemens, Federal Pacific, Zinsco,
  Murray. Don't say "the panel manufacturer" when "Federal Pacific" is
  what's meant.

## 5. Specificity markers

The voice's signature trait. What gets named, when, why.

- **Places.** Cities, neighborhoods, landmarks. Not "the area" — "Old
  Town Fairfax" or "Vienna's Hillside neighborhood." Cite at least one
  named place per page section.
- **Prices.** Real ranges with the basis explicit. Not "affordable" —
  "$2,800-$3,800 for a 100A-to-200A residential panel upgrade in
  Northern Virginia, permit included." If exact prices aren't ethical
  to publish, say what the variables are.
- **Brands.** Named, not "the manufacturer." Federal Pacific Stab-Lok,
  Zinsco-Sylvania, Square D QO/Homeline, Eaton CH/BR. The brand stack
  is part of the credibility.
- **Code references.** Named when relevant — NEC article, IRC section,
  state code. Not "current code" — "Virginia USBC adoption of NEC 2020,
  Article 408.3."
- **Permit offices.** Named — Fairfax City permit office, Vienna town
  permit desk, Fairfax County Land Development Services. Not "the
  county."
- **Scenarios.** Told as scenes, not abstractions. Not "homeowners often
  face this issue" — "A homeowner in Vienna's Hillside neighborhood
  called us last March with flickering kitchen lights..."

## 6. Opinion markers

Does the voice take positions? Where on the spectrum from
neutral-explainer to opinionated-advocate?

The default for residential-service editorial voice is **mildly opinionated
expert** — willing to say "if your panel is Federal Pacific, replace it"
rather than "you may want to consider replacement options," but not
ranting against contractors or making categorical claims that would harm
trust.

Examples of valid opinion markers in this voice:

- "Federal Pacific panels are a fire risk and should be replaced — full
  stop. The CPSC declined to recall them in the 1980s, but that's not
  the same as saying they're safe."
- "100A service is fine for a 1950s house with gas heat, gas range, and
  no EV. It's not fine if you're adding a Level 2 charger, a heat pump,
  and an induction range. Math first, decision second."
- "Skip the cheapest quote. The work is permit-bound, code-bound, and
  inspection-bound — if the cheapest quote is a third less than the
  median, the corner being cut is one of those three."

Opinion does NOT mean:

- Trashing competitors by name
- Categorical claims that don't survive edge cases
- Anything that would harm professional trust

## 7. Anti-patterns (what NOT to do)

The voice's negative space. What the editorial corpus does NOT do, and
neither should this voice.

- **No generic openings.** "In today's fast-paced world..." "When it
  comes to electrical work..." These read as AI immediately.
- **No soft hedging where the claim is real.** "You might want to
  consider..." when the actual answer is "you should." If the claim is
  hedged, hedge it; if the claim is firm, write it firm.
- **No listicle-without-depth.** "5 reasons to upgrade your panel" with
  three sentences per reason isn't editorial — it's filler. Each list
  item should carry its weight.
- **No SEO-keyword stuffing.** Mentioning "panel upgrade Vienna VA" six
  times in a paragraph reads as generated. Attribute density (the
  specific words that conversational queries contain) is different from
  keyword stuffing — see Section G of the marketing primer.
- **No closing summary that restates the page.** Real editors don't do
  this. They end with the next concrete step or a final scene-setting
  observation.
- **No FAQ-bolted-on-at-the-end** with generic answers. If the FAQs are
  real (someone actually asked them, or they emerged from GSC regex
  query mining), keep them in voice. If they're filler, cut them.
- **No "trust us" language.** Trust is earned by specifics. Naming the
  permit office is trust. Citing the code section is trust. "Trust the
  experts" is the opposite of trust.

## 8. Voice signals (concrete examples from corpus)

3-5 paired before/after sentences showing what the voice replaces vs.
produces. The "before" examples are typical AI-slop the rewrite is
correcting; the "after" examples are the voice this personality file
encodes.

**Before:** "In today's modern home, electrical safety is more important
than ever. Many homeowners are unaware of the risks associated with
outdated electrical panels."

**After:** "If your house was built between 1965 and 1985 and the panel
hasn't been touched since, the breakers in that box are statistically
older than most Northern Virginia drivers. They were rated for a 1970s
load. Your house isn't running a 1970s load anymore."

(Concrete claim, named timeframe, named place, named load context.
Replaces generic anxiety with specific scene.)

**Before:** "We offer a wide range of electrical services for your home
or business, including panel upgrades, troubleshooting, and more."

**After:** "Panel upgrades, EV charger installs, troubleshooting,
fixture work, smoke alarms, outlets. That's the menu. Each one is
permit-bound where Fairfax City and Vienna require it, and we pull the
permit — you don't."

(Specific list, named services, named jurisdictions, ownership claim.
Replaces vague competence with specific operational claim.)

(Add 1-3 more pairs from actual corpus extraction)

## 9. Client-grounding layer (entity specifics for <Client>)

This is the short section that attaches the researched house voice to
the specific client's entity profile. Fill from
`<client>/_status.md`, `<client>/business-context/`,
`<client>/credentials.reference.md`.

- **Business name:** <full legal name>
- **Owner name + credentials:** <e.g., Ahmad Hussein, Master
  Electrician, Virginia license #XXXX>
- **Geographic frame:** <e.g., "Northern Virginia," "Fairfax County
  primarily">
- **Service-area cities (Core 30 footprint):** <comma-separated list>
- **Years in business / years of experience:** <e.g., "20+ years
  residential electrical">
- **Standing phone number:** <e.g., 571-500-6637>
- **Domain URL:** <e.g., evelectric.pro>
- **Permit offices typically used:** <e.g., Fairfax City permit office,
  Vienna town permit desk, Fairfax County LDS>
- **Utility coordinator:** <e.g., Dominion Energy>
- **Named-brand stack the client uses:** <e.g., Square D QO, Eaton CH,
  Siemens; replacements for Federal Pacific Stab-Lok, Zinsco-Sylvania>
- **Non-negotiable phrasings** (from decision docs): <e.g., "no pricing
  on Core 30 pages per 2026-05-26 decision">
- **Voice quirks the operator has flagged:** <fill if any; otherwise
  "none flagged">

## 10. Refresh log

Append-only log of personality refreshes. Date, what changed, why.

- **YYYY-MM-DD — Initial build.** Built from <N>-source corpus dated
  YYYY-MM-DD. See execution log
  `[[execution-log-YYYY-MM-DD-house-voice-rewrite-skill-build]]`.

(Future entries append below)

## See also

- `[[house-voice-rewrite]]` — the skill that produced this file
- `[[plain-language-translation]]` — the prose-level voice subcomponent
- `[[primer-seo]]` — the operational SEO primer (Section D references
  this skill)
- `[[primer-marketing-vocabulary-and-concepts]]` — Section G on content
  discipline for AI citation
- `[[_status]]` — the client's current state doc
- `[[credentials.reference]]` — client credentials source-of-truth
```

---

## Notes on using this template

- The template is a starting structure, not a strict schema. If the
  research surfaces a voice trait that doesn't fit any of sections 2-7,
  add a section rather than forcing it into an existing one.
- Sections 1, 8, and 10 must always exist (corpus snapshot, paired
  examples, refresh log) — they're load-bearing for downstream rewrite
  work and for the refresh path.
- Section 9 (client-grounding layer) must be filled in COMPLETELY from
  the client folder. If a field is missing in the client folder, flag
  it for the operator rather than guessing.
- Avoid filling section 8 (paired examples) with hypothetical examples —
  use real before/after from the corpus extraction. If you can't produce
  3-5 real pairs, the corpus was probably too thin and you should expand
  research.
