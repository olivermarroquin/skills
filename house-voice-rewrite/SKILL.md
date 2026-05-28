---
name: house-voice-rewrite
description: Two-mode skill for producing human-sounding SEO content from AI-generated drafts. **Mode 1 (init-personality):** at client onboarding, researches proven-SEO editorial sources in the client's domain (residential electrical, plumbing, HVAC, roofing, etc.), extracts voice patterns from real-newspaper home-improvement editorials and top-ranking organic content, and writes a per-client personality file that captures the established house voice for that domain. **Mode 2 (rewrite):** at every page production, takes a draft (Core 30 page, blog post, AI-generated content) plus the per-client personality file, and rewrites the draft so it reads as authentically human-written editorial content indistinguishable from real-editor content in the same niche. Trigger phrases include "rewrite this in house voice," "apply house voice," "voice-rewrite this draft," "de-AI this page," "run the anti-slop pass," "initialize personality for [client]," "build the voice for [client]," "research the voice for [domain]," "make this not read like AI." This is the cross-client anti-AI-slop primitive — voice comes from researched editorial sources, NOT from client-specific writing samples (which often have broken English, no samples, or unhelpful style). Built 2026-05-27 to supersede Jono Catliff's voice-injection-via-reference-files approach for clients without polished writing samples.
---

# House Voice Rewrite

The anti-AI-slop and house-voice skill for Keelworks SEO content production.

This skill has two modes that work together:

1. **`init-personality`** — researched-once-per-client. Surveys proven-SEO
   editorial content in the client's domain, extracts the voice patterns
   that real human editors use, and writes a per-client personality file
   that captures the established house voice. Adds a small entity-grounding
   layer for the specific client (service-area cities, owner credentials,
   named-brand stack).
2. **`rewrite`** — every page production. Takes a draft plus the
   personality file and rewrites the draft in the established house voice.
   Output reads as authentically human-written SEO content.

The skill exists because most local-service clients can't supply the
writing samples Jono Catliff's voice-injection approach assumes — broken
English, no writing samples, or unhelpful style. So we **paint the voice
ourselves from proven editorial sources** and only add a small client-
specific entity-grounding layer on top.

## When to trigger

### Mode-1 trigger phrases (`init-personality`)

Direct triggers for building the personality file at client onboarding:

- "Initialize personality for [client]"
- "Build the house voice for [client]"
- "Research the voice for [domain]" (e.g., "for residential electrical")
- "Set up the personality file for [client]"
- "Onboard [client] for the house-voice skill"
- "Run the voice research for [client/domain]"

Indirect triggers — when Oliver mentions onboarding a new client and the
personality file doesn't yet exist:

- "We're starting work on [new client]. Get them set up."
- "Add [client] to the Keelworks client list."
- The skill is loaded and the operator asks to rewrite a draft for a
  client that has no personality file yet — surface init-personality as
  a precondition.

### Mode-2 trigger phrases (`rewrite`)

Direct triggers for rewriting a draft using the personality file:

- "Rewrite this in house voice"
- "Apply house voice to this draft"
- "Voice-rewrite this Core 30 page"
- "Rewrite [file] in [client]'s house voice"
- "De-AI this draft"
- "Run the anti-slop pass on [file]"
- "Make this not read like AI"
- "Run house-voice on [file]"

Indirect triggers — when a draft has just been produced by the Core 30
scaffolder or any AI-generation step, surface the rewrite as the next
step (don't auto-invoke; mention it).

## Why this beats voice-injection-from-client-samples

Jono Catliff's framing (source-2026-04-26) builds five reference files —
`voice.md`, `humor.md`, `stats.md`, `stories.md`, `opinions.md` — from
the client's own LinkedIn posts, emails, transcripts, and phone calls.
That works for clients with a polished writing voice. It fails for the
clients Keelworks actually serves.

Three failure modes the researched-editorial approach solves:

1. **Clients with broken English or non-native writers don't pollute the
   voice.** Both EV Electric and S&H Contracting fit this — see standing
   memory `project_clients_both_electrical`. Their actual writing is
   unhelpful for SEO. We build from proven-editor sources instead.
2. **Clients with no writing samples can still get a polished voice.**
   New businesses, small operators, and clients who don't write much have
   no corpus to extract from. The researched approach doesn't need one.
3. **The voice becomes "proven-to-rank" rather than "authentically
   client."** This is better for SEO outcomes specifically — we're not
   trying to capture the client's "true self"; we're trying to produce
   content that ranks and reads as human. Real editorial sources have
   already proven both.

The trade-off: a personality file built this way is house voice, not
client voice. We add a small client-grounding layer for entity specifics
(service-area cities, owner name, credentials, named-brand stack) so
generic editorial voice gets attached to the specific client's identity.

## Core workflow — Mode 1 (`init-personality`)

This is the one-shot setup that runs once per client.

### Step 1 — Identify the client and the domain

The skill needs two inputs:

1. **Client name** — e.g., "EV Electric Services" or "S&H Contracting."
   The client folder at
   `~/workspace/second-brain/04_projects/clients/_active/<client>/` should
   already exist. If it doesn't, surface a precondition error and stop —
   `init-personality` runs after client folder scaffolding, not before.
2. **Domain** — the SEO domain we're researching for. For residential
   electrical, "residential electrical" is the domain string. For
   plumbing, "residential plumbing." This becomes the seed for web search.

If Oliver provides only the client name, derive the domain from
`<client>/business-context/` or `<client>/_status.md`. If still unclear,
ask once for the domain string in plain language.

### Step 2 — Research the proven-editorial corpus

Use the protocol in `references/voice-research-protocol.md` to assemble
the editorial corpus. The general shape:

- Top 5-10 organic SERP results for high-value queries in the domain
  (e.g., "electrical panel upgrade cost," "how to know when to upgrade
  electrical panel," "Federal Pacific panel replacement")
- 2-4 articles from established home-improvement editorial publications
  (This Old House, Family Handyman, Bob Vila, The Spruce, HomeAdvisor's
  editorial content — NOT their lead-gen pages)
- 1-2 local-newspaper home-improvement columns if findable for the
  client's geography
- 1-2 industry-association editorial pieces (NECA, IAEI, local chambers)

**Exclusion rules:**

- Skip pages that read as AI-generated (generic phrasings, missing
  specifics, soft hedging, no named entities, no real prices, no real
  case studies).
- Skip directory pages (Yelp, BBB, Angi listings).
- Skip pure lead-gen pages (no editorial content, just CTA + form).
- Skip Reddit/forum threads (different voice register).

### Step 3 — Extract the voice patterns

For each editorial source, extract:

- **Sentence rhythm.** Sample 3 short sentences, 3 medium sentences, 3
  long sentences. Record the typical rhythm — short-medium-medium, or
  long-short-medium, or whatever pattern the source uses.
- **Vocabulary density.** How many technical terms per paragraph?
  Glossed inline or assumed? Domain-jargon ratio?
- **Specificity markers.** Are brands named? Places named? Code
  references cited? Prices stated as ranges or as exact numbers? Are
  scenarios told as scenes ("a homeowner in Royal Oak last March...") or
  abstractions?
- **Voice register.** Consultative? Direct? Expert-but-accessible?
  Folksy? Authoritative? What pronouns dominate ("you," "we," "the
  homeowner")?
- **Opinion markers.** Does the writer take positions? Hedge?
  Acknowledge trade-offs? Refuse to recommend? Where does opinion live
  on the spectrum from neutral-explainer to opinionated-advocate?
- **Anti-patterns.** What does the source NOT do? No generic openings?
  No soft hedging? No listicle-without-depth?

Synthesize across the 8-15 sources into ONE coherent house voice. Don't
average — the result should be a single voice that matches the editorial
norms of the domain, not the lowest common denominator.

### Step 4 — Add the client-grounding layer

Read the client's existing folder to extract entity facts:

- `<client>/_status.md` — current state, service area, owner
- `<client>/business-context/` — business background
- `<client>/credentials.reference.md` — credentials, license numbers,
  certifications
- Any existing `bridge-tactic-*` files — service offerings, target
  cities

Capture:

- Service-area cities (and the geographic frame — "Northern Virginia,"
  "Fairfax County," etc.)
- Owner name and titled credentials (Master Electrician, IBEW Local,
  etc.)
- Named-brand stack the client uses (Square D, Eaton, Federal Pacific
  replacements, etc.)
- Standing phone number / contact info (for in-page CTAs)
- Any non-negotiable phrasings the operator has flagged (e.g., from
  decision docs)

This grounding layer is SHORT. It's not capturing client voice — it's
attaching entity specifics so the house voice produces content that's
about the specific client, not generic.

### Step 5 — Write the personality file

Output path: `~/workspace/second-brain/04_projects/clients/_active/<client>/personality-<client>.md`

Use the template at `references/personality-template.md`. Frontmatter
includes:

- `type: personality`
- `status: active`
- `created: YYYY-MM-DD`
- `updated: YYYY-MM-DD`
- `client: <client-slug>`
- `domain: <domain-string>`
- `built-from: house-voice-rewrite skill init-personality mode`
- `tags: [personality, house-voice, anti-ai-slop, <client>]`

### Step 6 — Surface for operator review

After writing, present the file to Oliver via
`mcp__cowork__present_files` and offer:

- Quick read-and-approve
- Targeted edits (e.g., "the voice register should be more direct, less
  consultative")
- Re-research with adjusted source-corpus parameters

The personality file is the load-bearing artifact for every future page
on this client — it's worth a careful review pass before treating it as
canonical.

## Core workflow — Mode 2 (`rewrite`)

This runs per-page, every time a draft needs voice work.

### Step 1 — Identify the draft and the personality file

The skill needs two inputs:

1. **Draft path** — the file to rewrite. Usually a Core 30 page draft
   (`...draft-v1-WP-WRAPPED.html` or similar) or a markdown blog draft.
2. **Personality file path** — either passed explicitly or auto-discovered.
   For auto-discovery: read the draft's frontmatter for the `client:`
   field, then locate
   `04_projects/clients/_active/<client>/personality-<client>.md`. If
   the personality file doesn't exist, surface a precondition error and
   suggest running `init-personality` first.

### Step 2 — Read everything

Read in this order:

1. The full draft (don't paraphrase from memory)
2. The personality file (the voice spec we're rewriting toward)
3. `references/rewrite-rules.md` (preservation rules + rewrite mechanic)
4. The `plain-language-translation` skill's
   `references/translation-rules.md` (subcomponent voice rules — what to
   preserve vs. what to translate)

### Step 3 — Rewrite paragraph-by-paragraph

Apply the personality file's voice patterns paragraph-by-paragraph.
Critical preservation rules (full list in `references/rewrite-rules.md`):

- **All wikilinks and internal links** — preserve every `[[...]]` and
  every `/<slug>/` reference exactly.
- **All schema markup** — JSON-LD blocks, structured data, schema.org
  vocabulary stay character-perfect.
- **All HTML structure for paste-ready files** — if the input is a WP-
  wrapped HTML draft, the HTML tags, classes, and structure are preserved
  while the prose inside them gets rewritten.
- **All factual claims** — prices, credentials, license numbers, named
  brands, named places, named code references, phone numbers, addresses,
  permit-office names. Never invent or alter these. If the draft says
  "Federal Pacific panels," the rewrite says "Federal Pacific panels."
- **All structural elements** — H2 questions, FAQ structure, bullet
  counts, section order. Voice is the only axis that changes.
- **Capsule-content pluckability** — preserve or improve. Each H2 stays
  a question with the answer in the first sentence below. Don't bury
  the answer mid-paragraph.

What changes:

- Sentence rhythm shifts to match the personality file's pattern
- Generic openings get replaced with attribute-dense, specific openings
- Soft hedging gets sharpened to direct claims (when the draft permits
  it factually)
- Listicle-without-depth gets restructured with editorial scene-setting
- Vocabulary density adjusts to match the personality file's register
- Specificity markers (brands, places, code references, prices) get
  surfaced from the draft into more prominent positions

### Step 4 — Write the output

Default output path: alongside the input draft with `-voice-rewrite`
appended to the filename stem.

- `draft-v14-WP-WRAPPED.html` → `draft-v14-WP-WRAPPED-voice-rewrite.html`
- `draft-v1.md` → `draft-v1-voice-rewrite.md`

For new drafts being produced fresh by the Core 30 scaffolder, the
output can be written as the next version number (`draft-v15-...html`)
if the operator wants the voice-rewrite to become the canonical version
— but ask before bumping the version number, since version-log
discipline matters.

### Step 5 — Surface the before/after

Present a 2-3 paragraph before/after comparison in the chat so Oliver
can verify the voice shift before committing. The full rewrite file is
already on disk; the chat just shows the diff.

Don't make this a long postamble — short, paired excerpts, plain
language framing.

### Step 6 — Pair with related skills

If the rewritten draft is then heading to publish:

- Mention that `step-by-step-walkthrough` can guide the paste-to-WordPress
  flow if the draft is a Core 30 page
- Mention that `perplexity-refinement` can fact-check the rewritten draft
  if Oliver wants an extra citation pass before publishing

Don't auto-invoke. Surface as follow-up options.

## What this skill is NOT

- **Not a summarizer.** Rewrite preserves the full draft — same length
  (±10%), same structure, same content.
- **Not a fact-checker.** Rewrite preserves factual claims as written;
  if the draft says "$2,800," the rewrite says "$2,800." For fact-checking,
  pair with `perplexity-refinement` afterward.
- **Not a content generator.** The skill takes existing drafts and shifts
  their voice. The Core 30 scaffolder (or any other content-generation
  step) produces drafts; this skill rewrites them.
- **Not voice-injection-from-client-samples.** That's Jono Catliff's
  approach (source-2026-04-26). This skill builds voice from researched
  editorial sources instead. See the rationale section above.

## Filename and frontmatter rules

### Personality file (output of `init-personality`)

- **Path:** `~/workspace/second-brain/04_projects/clients/_active/<client>/personality-<client>.md`
- **Frontmatter:**
  ```
  type: personality
  status: active
  created: YYYY-MM-DD
  updated: YYYY-MM-DD
  client: <client-slug>
  domain: <domain-string>
  built-from: house-voice-rewrite init-personality
  source-corpus-snapshot: YYYY-MM-DD
  tags: [personality, house-voice, anti-ai-slop, <client>, <domain>]
  ```

### Rewritten draft (output of `rewrite`)

- **Path:** alongside input, `-voice-rewrite` suffix on the filename
  stem (or next version number if operator approves)
- **Frontmatter** (markdown drafts only — HTML drafts have no
  frontmatter): copy the source draft's frontmatter, then:
  - Update `updated:` to today's date
  - Add `voice-rewritten` to `tags:`
  - Add `voice-source: personality-<client>.md` field
  - Add 1-line preamble: `> Voice-rewritten from [[<source-draft-name>]] using house-voice-rewrite skill against [[personality-<client>]].`

## Refresh path for the personality file

The personality file isn't static. As the client publishes more pages
and Keelworks observes what ranks vs. what doesn't, the personality
should refine:

- **Quarterly refresh.** Every 3 months, re-run the research phase with
  the same domain string. Compare to the existing personality file.
  Surface drift (new editorial conventions emerging, vocabulary
  shifting). Operator decides whether to update.
- **Trigger refresh.** When a published page underperforms vs. peers,
  surface a refresh prompt — maybe the voice has drifted from what the
  current SERP rewards.
- **Bump refresh.** When the operator explicitly says "refresh the
  personality for [client]," re-run init-personality with `--mode refresh`
  (proposed flag) that compares old vs. new and proposes specific edits
  rather than rewriting wholesale.

The skill is non-destructive on refresh by default — proposes edits,
doesn't overwrite without operator approval.

## Hand-offs

### Inward

- **From client-fact-research** (Phase 2d skill): after a client-fact
  brief is written, surface init-personality as the next step in
  client onboarding.
- **From the Core 30 scaffolder** (in `repos/ai-agency-core/scripts/`):
  after a draft is generated, surface rewrite as the next step.
- **From `vis-extraction`**: when ingesting a source that proposes a new
  voice-injection tactic (like Jono Catliff's source-2026-04-26), the
  source note should reference this skill rather than spawning a parallel
  tactic.

### Outward

- **To `plain-language-translation`**: rewrite uses plain-language's
  translation-rules.md as a sub-component for what to preserve vs.
  translate at the prose level. The personality file is the additional
  voice spec layered on top.
- **To `perplexity-refinement`**: rewritten drafts can be passed to
  perplexity-refinement for fact-checking before publish.
- **To `step-by-step-walkthrough`**: if the rewritten draft is a Core 30
  page heading to WordPress, the walkthrough can guide the paste flow.

## Reference files

- `references/personality-template.md` — the template structure for
  per-client personality files (the output of init-personality)
- `references/voice-research-protocol.md` — the step-by-step research
  workflow for init-personality (which queries to run, which sources to
  prefer, which to skip, how to extract voice patterns)
- `references/rewrite-rules.md` — preservation rules + paragraph-by-
  paragraph rewrite mechanic for the rewrite mode

## Worked example

The canonical worked example for this skill:

- **Client:** EV Electric Services
- **Domain:** residential electrical
- **Personality file:** `~/workspace/second-brain/04_projects/clients/_active/ev-electric-services/personality-ev-electric.md`
- **Worked rewrite:** demonstrated against a representative AI-slop intro
  paragraph for the panel-upgrade-vienna-va Core 30 page (illustrative;
  doesn't replace the published v14 copy)
- **Execution log:** `~/workspace/second-brain/04_projects/clients/_active/ev-electric-services/execution-logs/execution-log-2026-05-27-house-voice-rewrite-skill-build.md`

If you're uncertain about voice, output shape, or what "house voice"
means in Keelworks's vault context, read the personality file and the
execution log side by side.

## See also

- `[[plain-language-translation]]` — the prose-level voice subcomponent
  this skill uses internally
- `[[perplexity-refinement]]` — pair after rewrite to fact-check
- `[[step-by-step-walkthrough]]` — pair after rewrite for paste-to-WP flow
- `[[vis-extraction]]` — pair when ingesting new voice-injection sources
- `[[client-fact-research]]` (Phase 2d) — pair at client onboarding,
  this skill runs after client-fact-research
- Source: `source-2026-04-26-jono-catliff-claude-code-seo-50000-clicks-per-month-masterclass`
  — the voice-injection approach this skill supersedes for clients
  without writing samples
- Standing memory: `feedback_plain_language_default` — the broader
  plain-language voice default this skill operates within
