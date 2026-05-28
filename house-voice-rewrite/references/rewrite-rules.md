# Rewrite rules

Preservation rules and the paragraph-by-paragraph rewrite mechanic for
Mode 2 (`rewrite`) of `house-voice-rewrite`.

Read this before drafting any rewrite. The skill is a voice transformation
— same content, same structure, same factual claims, same links, same
schema. Only the prose changes.

## Critical preservation rules (must hold)

### Links and references

Preserve exactly:

- Every `[[wikilink]]` reference
- Every `/<slug>/` internal link reference
- Every external URL
- Every relative file path
- Every anchor reference (`#section-name`)
- Every cross-page reference in section text

If the draft has `[[panel-upgrade-fairfax-va]]`, the rewrite has
`[[panel-upgrade-fairfax-va]]`. Same string, same target.

### Schema and structured data

JSON-LD blocks, schema.org vocabulary, and structured-data attributes
are character-perfect preserved. The schema is a separate axis from the
prose. If a schema field's value is prose ("description": "..."), that
prose can be rewritten — but the field structure stays.

Same rule for:
- HTML structure in WP-WRAPPED drafts (tag hierarchy, classes, IDs)
- Frontmatter fields (frontmatter is metadata, not voice)
- Image references, alt-text structure (alt-text prose can be rewritten;
  the `alt="..."` syntax stays)

### Factual claims

Never invent, alter, or "fix" factual claims. The rewrite is voice work,
not fact-checking. Preserve exactly:

- Prices and price ranges (numbers and currency)
- Brand names (Federal Pacific, Zinsco, Square D, Eaton, etc.)
- Place names (cities, neighborhoods, addresses, permit offices)
- Code references (NEC article, USBC section, IRC section)
- Credentials (license numbers, certifications, association memberships)
- Phone numbers, email addresses, URLs
- Dates, years in business, review counts, star ratings
- Square footage, amperage, wattage, any technical specifications
- Hours of operation, service-area boundaries

If a fact in the draft is wrong or stale, surface it to the operator
as a flag — don't fix it in the rewrite. Fact-checking belongs to
`perplexity-refinement`, not here.

### Structural elements

- **H2 questions stay H2 questions.** If the draft has "What is a panel
  upgrade?" as H2, the rewrite has a question-form H2 there. The
  question wording can adjust if the personality file's voice requires
  it, but the question SHAPE stays.
- **Bullet counts stay the same.** If a list has 8 items, the rewrite
  has 8 items. Don't condense; don't expand.
- **FAQ count stays the same.** If the draft has 8 FAQs, the rewrite
  has 8 FAQs. Same questions if possible, same order.
- **Section count and order stay the same.** Section 1, 2, 3, ... in
  source = same in rewrite.
- **Word count lands within ±15%.** More than 15% shorter means
  summarization; more than 15% longer means over-explaining. The
  personality file's voice usually keeps word count close to source.

### Capsule-content pluckability

The rewrite must preserve or improve the H2-as-question + answer-in-
first-sentence pluckability pattern from the marketing primer Section G.

For each H2:
- Keep it phrased as a question (or convert if the source isn't)
- The first sentence below the H2 directly answers that question
- Subsequent sentences elaborate; don't bury the answer mid-paragraph

If the personality file's voice tightens up loose openings, that's an
improvement — but the structural rule stays.

## The paragraph-by-paragraph mechanic

For each paragraph in the source draft:

### Step A — Identify what the paragraph is doing

Classify the paragraph's job:

- **Scene-setting** (intro to a problem or situation)
- **Definitional** (what is X, how does X work)
- **Operational** (process steps, what we do)
- **Pricing/commercial** (price ranges, what's included)
- **Trust** (credentials, years, reviews, named partners)
- **CTA** (call us, get a quote)
- **FAQ answer** (a single answer in an FAQ block)
- **Closing** (page-end summary, next step, final scene)

The personality file specifies different rhythms and registers for
different paragraph jobs. Scene-setting paragraphs use the
personality's "scene-setting pattern"; operational paragraphs use the
"operational pattern"; etc.

### Step B — Apply the voice patterns

From the personality file's sections 3-7, apply:

- **Sentence rhythm** for this paragraph's job (Section 3)
- **Vocabulary density** for this domain (Section 4)
- **Specificity markers** — surface or add specificity that's latent in
  the source (Section 5)
- **Voice register** — consultative/direct/expert-but-accessible/etc.
  (Section 2)
- **Opinion markers** if the paragraph permits them (Section 6)
- **Anti-patterns** — actively avoid (Section 7)

### Step C — Pull specificity from the source

The source draft usually contains the specifics — named brands, named
places, prices, code references. The rewrite makes those specifics
MORE prominent, not less. Move them earlier in the paragraph; lead with
them when the rhythm permits.

If the source draft mentions Federal Pacific in passing in sentence 4
of a paragraph and the personality file's voice puts brand specificity
in the opening sentence, restructure so "Federal Pacific" leads the
paragraph.

### Step D — Add the client-grounding when the slot exists

The personality file's Section 9 (client-grounding layer) has entity
specifics that the source draft may not have. Where the rewrite
naturally creates a slot for one of those specifics, add it.

Examples:
- The source draft says "we coordinate with the utility." The rewrite
  can say "we coordinate with Dominion Energy" (named utility from the
  client-grounding layer).
- The source draft says "we pull the permit." The rewrite can say "we
  pull the permit at the Fairfax City permit office or the Vienna town
  permit desk depending on jurisdiction" (named permit offices from
  the client-grounding layer).

Don't force grounding. If the slot doesn't naturally exist, don't
shoehorn the grounding in.

### Step E — Check against anti-patterns

Before finalizing the paragraph:

- Generic opening? (rewrite)
- Soft hedging where the claim is real? (sharpen)
- Filler list items? (cut or restructure)
- SEO keyword stuffing? (replace with natural attribute density)
- "Trust us" language without specifics? (replace with specifics)

If any anti-pattern survives, the rewrite isn't done.

## Output discipline

### File output

- **Default path:** alongside source, `-voice-rewrite` suffix
- **Frontmatter** (markdown drafts): copy source's frontmatter, then
  add `voice-rewritten` to tags, add `voice-source: personality-<client>.md`
  field, update `updated:` to today
- **Preamble** (markdown drafts): one-line note `> Voice-rewritten from
  [[<source-name>]] using house-voice-rewrite skill against
  [[personality-<client>]].`
- **HTML drafts (WP-WRAPPED):** no frontmatter; preserve HTML structure
  exactly; rewrite prose inside HTML tags

### Chat output

After writing the rewritten file, surface a SHORT before/after preview
in chat:

- 2-3 paired excerpts (1-2 paragraphs each)
- Plain-language framing
- No long postamble — the file is already on disk

Example chat output:

```
Rewrite landed at [path]. Voice shift visible in two passages:

**Section 2 intro — before:**
"In today's modern home, electrical safety is more important than ever..."

**After:**
"If your house was built between 1965 and 1985 and the panel hasn't been
touched since, the breakers in that box are statistically older than
most Northern Virginia drivers..."

[one more paired excerpt]

Want me to walk through the full diff or move on?
```

## What rewrite is NOT

- **Not summarization.** Source length ±15%; no compression.
- **Not fact-checking.** Preserves all factual claims as-written.
- **Not content generation.** Doesn't add new claims, sections, or
  arguments. Voice transformation only.
- **Not editing for grammar.** If the source has grammar errors,
  preserve them — surface to operator as a flag. (In practice, AI-
  generated drafts rarely have grammar errors; this rule is for human-
  generated drafts where grammar deviations may be intentional voice.)
- **Not Anthropic-style polish.** Don't soften, hedge, or add caveats
  beyond what the source has. The personality file's voice register is
  what governs polish, not generic LLM hedging defaults.

## Failure modes to avoid

- **Drift into summarization.** If output is more than 15% shorter,
  you compressed. Go back and fill in.
- **Drift into improvement.** If you find yourself thinking "this
  section would be clearer if we restructured," stop. Out of scope.
- **Drift into fact-checking.** If you start adjusting prices, brand
  names, or credentials, stop. Flag to operator instead.
- **Loss of wikilinks.** Every `[[...]]` in source must appear in
  rewrite. Verify before output.
- **Loss of schema.** JSON-LD blocks must be character-perfect. Diff
  the schema section between source and output to verify.
- **Personality-file ignored.** If the rewrite reads like the default
  plain-language voice instead of the personality-file voice, the
  rewrite isn't using the personality file. Re-read sections 2-7 and
  re-do.
- **Generic voice (still AI-shaped).** If the rewrite still reads as
  "by an AI doing its best to sound human" rather than "by a person who
  knows this domain," the personality file isn't being applied
  paragraph-by-paragraph. Apply Step A-E for each paragraph rigorously.

## Verification checklist

Before declaring the rewrite complete:

- [ ] Every wikilink in source appears in output
- [ ] Every schema/JSON-LD block character-perfect preserved
- [ ] Every factual claim (prices, brands, places, code refs) preserved
- [ ] Word count within ±15% of source
- [ ] Section count and order match source
- [ ] Bullet counts and FAQ counts match source
- [ ] H2-as-question pluckability preserved/improved
- [ ] Personality file's voice register visible in 3+ paragraphs
- [ ] Specificity markers surfaced (named brands/places/prices visible)
- [ ] Anti-patterns absent (no generic openings, no soft hedging without
      cause, no SEO stuffing, no "trust us" language)
- [ ] Before/after chat preview prepared

If any item fails, fix before output.
