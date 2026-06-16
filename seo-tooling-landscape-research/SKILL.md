---
name: seo-tooling-landscape-research
description: Survey the SEO tool landscape comprehensively for a given agency context — free tools, paid tools, AEO/GEO bleeding-edge category, per-task tool recommendations, and tiered stack proposals. Three modes: (1) SURVEY mode — full landscape research producing a 5-file output set (free/paid/AEO-GEO/per-task/stack), (2) DISCOVERY mode — recurring scan for new/emerging/obscure high-leverage tools + free public data sources per arena, and (3) INTAKE mode — operator drops a tool link/name/video → eval rubric → tool-*.md + adopt/skip recommendation. Triggers on phrases like "survey SEO tools," "research SEO tooling landscape," "what SEO tools should we use for [vertical]," "build an SEO tool stack for [agency size]," "compare SEO tools," "evaluate AEO/GEO tools," "do an SEO tool inventory," "discover new SEO tools," "scan for emerging tools," "digest this tool," "evaluate this tool," or any time the user wants a comprehensive landscape report, emerging-tool scan, or single-tool evaluation. Also use when an existing tool stack needs refreshing, when entering a new vertical that needs its own tool calibration, or when assessing a new SEO tool category (AI-search tools, schema tools, citation tools, etc.).
---

# SEO Tooling Landscape Research Skill (v2.0)

This skill packages the systematic SEO tool survey methodology Oliver used on 2026-05-23 to evaluate ~47 tools for Keelworks's residential-services SEO work, **plus two self-expanding modes added in v2.0** (2026-06-15) that keep the tool landscape living and growing:

- **Survey mode** (v1.0, Phases 1–6) — full landscape research producing a 5-file output set
- **Discovery mode** (v2.0) — recurring scan for new/emerging/obscure tools + free public data sources per arena
- **Intake mode** (v2.0) — operator-initiated single-tool evaluation pipeline

The canonical exemplar lives at `~/workspace/second-brain/03_domains/seo/tools/`. The five files there are the reference output for survey mode — read them before writing anything new.

## Mode selection

When the skill is invoked, determine the mode from the trigger phrase:

| Trigger | Mode | Jump to |
|---|---|---|
| "survey SEO tools," "research SEO tooling landscape," "build an SEO tool stack," "do an SEO tool inventory," "refresh the tools landscape" | **Survey** | Phase 1 (existing) |
| "discover new SEO tools," "scan for emerging tools," "what new tools are out there," "run a discovery scan," "monthly tool scan" | **Discovery** | Discovery mode section |
| "digest this tool," "evaluate this tool [name/URL]," "I saw a tool called [X]," or a URL/name dropped with intake intent | **Intake** | Intake mode section |

If ambiguous, ask the operator which mode. If the operator says "run the full thing," that means Survey mode.

## What this skill produces

### Survey mode (Phases 1–6)

Five Markdown files in the operator-specified output folder:

1. **free-seo-tools-inventory.md** — exhaustive inventory of free SEO tools across keyword research, competitor analysis, site audit, rank tracking, backlinks, schema, content optimization
2. **paid-seo-tools-inventory.md** — major paid tools with current pricing tiers, strengths, weaknesses, who-it's-for, fit-for-context rating
3. **aeo-geo-tools-survey.md** — bleeding-edge category for ranking in AI-generated answers; dedicated tools + emerging players + legacy SEO platform AEO modules
4. **keelworks-standard-seo-stack.md** (or `<agency>-standard-seo-stack.md`) — three-tier stack proposal (Solo / Growing / Scaled) with monthly cost totals and migration triggers
5. **per-task-tool-recommendations.md** — best tool by common SEO use case (keyword research, competitor content analysis, site audit, rank tracking, schema, backlinks, content briefs, citations, AI visibility, GBP audit)

Plus an update to the destination folder's `_README.md` adding a navigation section to the new files.

### Discovery mode (v2.0)

- `tool-*.md` notes in `03_domains/seo/tools/` for candidates scoring Trial or above
- Updated TG-rows in `_data-gap-register.md` (for Adopt/Trial candidates)
- Updated `mi-arena-source-checklist.md` (for new public data sources/registries)
- Discovery log summary in chat output

### Intake mode (v2.0)

- One `tool-*.md` note in `03_domains/seo/tools/` per evaluated tool (with filled eval rubric)
- TG-row in `_data-gap-register.md` (if Adopt or Trial)
- Updated `keelworks-standard-seo-stack.md` (if Adopt)
- Processed source files moved to `00_inbox/tools-pending/_processed/`

## Inputs the skill needs

Before doing any research, confirm these with the operator. Present as plain text — do not use AskUserQuestion (it's glitching in Cowork per Oliver's standing feedback memory).

1. **Target agency context:**
   - Agency name (e.g., "Keelworks") — used in stack proposal filename and exec summary
   - Agency size today (solo / 1-2 clients / 3-5 / 6+) — determines which tier is the "you are here" anchor
   - Existing tool stack if any (Claude/ChatGPT subscriptions, existing Ahrefs seat, existing BrightLocal, etc.)

2. **Target vertical:**
   - Primary client vertical (residential services? e-commerce? B2B SaaS? local pros? franchises?)
   - Specific sub-vertical if narrow (e.g., "electricians and contractors in Northern Virginia")
   - Local SEO weight: is this a single-location, multi-location, or non-local play?

3. **Output folder path:**
   - Default: `~/workspace/second-brain/03_domains/seo/tools/` (the canonical Keelworks folder)
   - Alternative: any other folder where the operator wants the output written (e.g., a client-specific subfolder, a different vault, a non-KOS folder)
   - If the folder doesn't exist, ask whether to create it.

4. **Depth and scope:**
   - Should we re-survey free tools, or trust the existing canonical file?
   - Should we re-survey paid tools, or refresh only specific tools? (Pricing can change in weeks — full re-survey is the default unless operator says otherwise.)
   - Special interests? (e.g., "spend extra time on AEO/GEO," "include enterprise tools," "skip enterprise tools entirely")

5. **Tone calibration:**
   - Honest hype-call language? (Default: yes, per Oliver's standing preference. Soften only if the operator is using this skill for a client-deliverable that needs more diplomatic framing.)
   - Plain language? (Default: yes, per Oliver's plain-language convention. Always.)

Don't proceed until these are pinned. Underspecified inputs are the most common failure mode for this skill — vague answers produce generic outputs.

## Pre-flight: read the canonical exemplar

Before writing anything new, read the canonical exemplar files to anchor structure, frontmatter, and tone:

- `~/workspace/second-brain/03_domains/seo/tools/free-seo-tools-inventory.md`
- `~/workspace/second-brain/03_domains/seo/tools/paid-seo-tools-inventory.md`
- `~/workspace/second-brain/03_domains/seo/tools/aeo-geo-tools-survey.md`
- `~/workspace/second-brain/03_domains/seo/tools/keelworks-standard-seo-stack.md`
- `~/workspace/second-brain/03_domains/seo/tools/per-task-tool-recommendations.md`

The Methodology section appended to each canonical file is the authoritative methodology for this skill. Reference it directly in the new files' Methodology sections rather than re-deriving it from scratch.

Also read:
- The KOS conventions: `~/workspace/second-brain/_meta/conventions.md` for frontmatter and naming rules
- The destination folder's existing `_README.md` to understand what's already there

### Recovery: what to do if the canonical exemplar isn't where this skill expects it

This skill was authored on 2026-05-23 against a canonical exemplar at the path above. If those files don't exist at that path when you read this:

1. **First, search the vault for the files by filename.** Use Glob or Grep against `~/workspace/second-brain/` for `free-seo-tools-inventory.md`, `paid-seo-tools-inventory.md`, etc. The files may have been moved (vault reorganization is normal in this project) but typically not renamed.
2. **If found, update this skill's paths** to point to the new location, then proceed. This is a one-line edit per file.
3. **If not found** (e.g., the exemplar was deleted, or this skill is being used in a fresh vault), fall back to the skill body — every required section structure, frontmatter pattern, Methodology template, and decision criterion is described inline below. The exemplar is helpful but not load-bearing.
4. **Tell the operator** which recovery path you took and recommend they refresh the canonical exemplar so future invocations are anchored against the operator's current vault state.

The same recovery logic applies if `~/workspace/second-brain/_meta/conventions.md` has moved — search by filename, then proceed with the conventions described in this skill body if the file is unreachable.

## Phase 1 — Confirm inputs

Present the input list as plain text. Wait for the operator's answers before proceeding. Underspecified inputs ruin the output.

## Phase 2 — Parallel research

Dispatch three sub-agents in parallel via the Agent tool (`general-purpose` subagent_type). Each returns a concise synthesis under 2,000 words with cited sources. Running them in parallel is important — sequential runs blow out the time budget.

### Sub-agent 1: Paid SEO tools

Brief the agent with the agency context and target vertical, then ask for current-pricing-current-positioning data on the major paid tools. Default list (override if operator specified differently):

Ahrefs, SEMrush, Moz Pro, Ubersuggest, SE Ranking, BrightLocal, Mangools, SpyFu, Surfer SEO, Frase, NeuronWriter, Clearscope, MarketMuse, WriterZen, AIOSEO Pro.

For each tool, request: pricing tiers (current as-of-today), free trial availability, strengths (2-3 bullets), weaknesses (2-3 bullets, including hype/lock-in/feature gaps), best-for one-liner, vertical-specific fit one-liner.

**Pricing currency is the single most important constraint.** Many aggregators carry stale 2022–2024 pricing. The agent must verify pricing on each vendor's actual pricing page where possible. Annual-vs-monthly billing must be distinguished.

### Sub-agent 2: AEO/GEO tools

Brief with the agency context (especially local SEO weight — the local vs. enterprise split is the most consequential calibration in this category).

Default tools to research:
- Profound, Otterly.ai, AthenaHQ, BrightEdge AI Generative Search Optimization, Goodie AI, Daydream, Peec AI
- Emerging tools: Scrunch AI, Local Falcon (with Falcon AI), BrightLocal AI features, SE Ranking AI Overview tracker, plus 2-3 more if the agent finds them
- Legacy incumbent AEO modules: Ahrefs Brand Radar, SEMrush One AI Visibility

For each: what it does (track? optimize? both?), who's behind it (founders, year founded, funding if known), pricing (current; "demo only" if enterprise-gated), maturity (real product with traction vs. landing page), and vertical fit.

This category moves fast — funding rounds, pricing changes, and pivots happen quarterly. The agent must verify against current vendor pages, not 6-month-old reviews.

### Sub-agent 3: Free SEO tools verification

Brief with the agency context. For ~20 free tools across keyword research, competitor analysis, site audit, rank tracking, backlinks, schema, and content optimization, verify current free-tier limits as of today.

Default tools to verify:
- Keyword research: Google Keyword Planner, Ubersuggest free, AnswerThePublic, AlsoAsked, Keyword Surfer extension, Keywords Everywhere free portion
- Competitor: Wappalyzer, BuiltWith, SimilarWeb free, SpyFu free
- Audit: PageSpeed Insights, Lighthouse, Ahrefs Webmaster Tools, Bing Webmaster Tools
- Rank tracking: SerpRobot free tier, Google Search Console
- Backlinks: Ahrefs Free Backlink Checker, SEMrush Free Backlink Checker
- Schema: Google Rich Results Test, Schema.org Validator, AIOSEO free
- Content: Whatever has a genuinely useful free tier today

For each: what it does (one sentence), what's free (specific limits), what's paid (one-line entry tier), vertical-relevance rating (high / medium / low).

**Free-tier limits tighten regularly** as vendors compress free offerings to push paid conversions. The agent must verify limits against current vendor docs.

## Phase 3 — Synthesize into five files

After all three sub-agents return, synthesize their outputs into the five files. Apply these rules:

### File structure and frontmatter

Every file gets KOS-conformant YAML frontmatter:

```yaml
---
type: tool
status: draft
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
domains: [seo]
sensitivity: standard
tags: [tool, seo, <inventory|survey|stack|recommendations>, <agency-name>, <vertical>]
---
```

Filenames are descriptive and consistent across the canonical exemplar:
- `free-seo-tools-inventory.md`
- `paid-seo-tools-inventory.md`
- `aeo-geo-tools-survey.md`
- `<agency>-standard-seo-stack.md` (e.g., `keelworks-standard-seo-stack.md`)
- `per-task-tool-recommendations.md`

These are descriptive filenames without the `tool-` prefix because they're cross-tool reference docs that span the category — they don't fit the per-tool `tool-*.md` convention. The destination folder's `_README.md` should already document this naming exception (the canonical Keelworks folder does).

### Required sections per file

Each file follows this structure:

1. **YAML frontmatter** (above)
2. **# Title** with date in parentheses, e.g., `# Free SEO Tools — Comprehensive Inventory (2026-05-23)`
3. **## Executive summary** — 4-6 paragraphs maximum. Lead with the operator-actionable takeaway. Name the recommendation, not just the field.
4. **## [Body sections]** — the actual inventory or synthesis content
5. **## Methodology** — the canonical methodology section (see template below). Tailor 2-3 bullets per section to the specific file's research scope.
6. **## See also** — wikilinks to peer files, the folder README, parent domain, and the anchor client/project for context

### The Methodology template (canonical)

Every file gets this Methodology section, with file-specific tailoring of the bullets. The exemplar files in `~/workspace/second-brain/03_domains/seo/tools/` show what good tailoring looks like.

```markdown
## Methodology

### Sources consulted

- Vendor pricing pages and help-center articles current as of <date>
- Comparison articles from <relevant aggregators for this file>
- <File-specific source category: funding reports for AEO, free-tier vendor docs for free inventory, KOS vault context for synthesis files>
- Existing vault context: <named files that informed this output>

### Tools used

- WebSearch as the primary current-state lookup, delegated to a general-purpose sub-agent
- The sub-agent ran ~<N> search-and-fetch operations and returned a synthesis with cited sources
- <File-specific tool: cross-source pricing verification, founding-team searches, free-tier limit confirmations, etc.>
- No live testing of any tool against a shared dataset — claims based on vendor docs + recent reviews, not first-hand May 2026 verification

### Decision criteria

- <Lead criterion specific to this file: "Local-SEO relevance for residential services" / "Pricing currency" / "Maturity over hype" / "Client-count tier axis" / "Use-case framing first, tool framing second">
- <Second criterion>
- <Third criterion>
- Honest skip calls — tools that don't fit the use case named explicitly with reasons

### Gaps and limitations

- <File-specific limit 1>
- <File-specific limit 2>
- <File-specific limit 3>
- No first-hand tool tests — recommendations based on synthesized review data, not direct trial use

### What I'd do differently next time

- <File-specific improvement 1: snapshot pricing pages, run side-by-side tests, validate against practitioner community, etc.>
- <Improvement 2>
- <Improvement 3>
```

### Plain-language requirement

Per Oliver's standing memory (`feedback_plain_language_default.md`): write everything in plain language. Gloss jargon inline the first time it appears. AEO = answer engine optimization (showing up in AI answers). NAP = Name, Address, Phone consistency across directories. LCP = Largest Contentful Paint (a Core Web Vitals metric).

Apply this to both files and chat responses. No exceptions.

### Honest assessment requirement

Per Oliver's standing preferences captured across multiple memories: call out hype, lock-in, and feature gaps explicitly. Don't write a tool review that reads like a vendor brochure.

Specific patterns that should appear in the output:
- "Skip categorically for [context]" lists at the bottom of inventory files
- "What hype to ignore" sections in the AEO/GEO survey (the category is hype-dense)
- "What's deliberately left out" sections in the tiered stack proposal
- "Skip" lines per task in the per-task recommendations

### Wikilink rules

Slug-only wikilinks for files with unique filenames: `[[free-seo-tools-inventory]]`. Path-based wikilinks for ambiguous filenames like project READMEs: `[[ev-electric-services/README]]`.

Every file must link to:
- All peer files in the same survey set (free, paid, AEO/GEO, stack, per-task)
- The folder `_README` (`[[_README]]`)
- The anchor project/client if applicable (e.g., `[[ev-electric-services/README]]` for the Keelworks-residential-services calibration)
- The parent domain or domain primer where relevant

### Vertical and context calibration

Every file should reference the specific agency context in the Executive Summary. Replace generic "for residential-services agencies" with the operator's specific vertical (e.g., "for e-commerce agencies serving DTC brands" or "for B2B SaaS marketing teams").

The tiered stack proposal especially needs vertical-specific calibration. Tier transitions that work for a residential-services agency don't work the same way for an enterprise-content agency.

## Phase 4 — Update the folder `_README.md`

Add a "Surveys and meta-references" section (or update the existing one) to the destination folder's `_README.md` linking to the five new files. Be non-destructive — don't overwrite existing content; add a new section if one doesn't already exist.

If the destination folder's `_README.md` doesn't exist, create one with `type: folder-readme` frontmatter and a brief explanation of what lives in the folder.

If the folder is outside the second-brain vault (e.g., a client folder, a different repo), skip the `_README.md` update unless the operator asks for one.

## Phase 5 — Verification

Before declaring done, run a verification pass:

1. **Frontmatter check** — every file has valid YAML frontmatter with required fields (type, status, created, updated, domains, tags). Use `head -10 <file>` per file via Bash.
2. **Wikilink check** — extract wikilinks via `grep -oE "\[\[[^]]+\]\]" <file>` and confirm peer links resolve.
3. **Pricing consistency check** — spot-check that the same tool's pricing matches across files (e.g., Ahrefs Lite price in the paid inventory matches the Ahrefs Lite price in the per-task recommendations).
4. **Currency check** — confirm no obviously stale dates or pricing slipped in (e.g., "$15/mo Frase Starter" would be wrong because Frase repriced to $45/mo in 2024–2025).
5. **Plain-language check** — scan for unglossed jargon. AEO, GEO, NAP, LCP, CTR, CWV, GBP, SERP, etc. should be defined inline on first use.

## Phase 6 — Closing step

### 6a — House-voice rewrite (client-scoped outputs only)

When the output folder is client-scoped (path contains `clients/_active/`), invoke house-voice-rewrite Mode 2 on the stack proposal file before the auto-invoke output-quality-loop block.

- **Target file:** the `<agency>-standard-seo-stack.md` file in the output folder.
- **Personality file:** `~/workspace/second-brain/04_projects/clients/_active/<client-slug>/_state/personality-<client-slug>.md` — derive `<client-slug>` from the output path.
- **Graceful degradation:** If the personality file does not exist at the expected path, skip the house-voice rewrite silently and proceed to 6b. Do not error, do not prompt the operator.

### 6b — Auto-invoke output-quality-loop

After Phase 5 verification passes (and 6a if applicable), emit the standard auto-invoke block per `~/workspace/skills/output-quality-loop/references/auto-invoke-convention.md` and `~/workspace/second-brain/_meta/conventions.md` § "Output quality". This is the closing step every artifact-producing skill emits before declaring the chat done. Convention shipped Phase 5 of the output-quality-loop project (2026-05-28).

**Artifact list for this skill.** The full five-file output set: free-tools inventory, paid-tools inventory, AEO/GEO survey, per-task recommendations, tiered stack proposal. Plus the destination folder's `_README.md` if newly created (otherwise it's a hygiene update, not a content artifact).

**The block to emit (verbatim):**

````markdown
## Auto-invoke output-quality-loop

This skill produced the following artifact(s):
- `<free-tools-inventory-path>`
- `<paid-tools-inventory-path>`
- `<aeo-geo-survey-path>`
- `<per-task-recommendations-path>`
- `<tiered-stack-proposal-path>`

[output-quality-loop:eval] — for each artifact, run output-quality-loop in EVALUATE mode. If PASS, declare the chat done. If NEEDS REVISION or FAIL, ingest the revision prompt as if it were operator input and regenerate the artifact, then re-invoke output-quality-loop. Cap at 3 iterations; on the 3rd FAIL, escalate to the operator with the evaluation report.
````

Required-element discipline per the convention spec: heading text matches verbatim (`## Auto-invoke output-quality-loop`); one bullet per artifact with full path in backticks; directive opens with `[output-quality-loop:eval]` and includes the iteration-cap discipline language.

**Iterate or declare done.** All PASS → declare done. Any NEEDS REVISION (minor / substantive) → Mode 2 auto-fires a revision prompt; ingest as operator input, apply fixes to the affected file (tighten an inventory entry, gloss missed jargon, fix pricing inconsistency, restore wikilinks), re-emit the block, loop. Any FAIL → revision prompt includes root-cause analysis; address the root cause (often: hype-vs-substance softening crept in, vertical calibration didn't fit the operator's context, paid-tool defaults assumed without surfacing), regenerate, re-emit, loop.

**Iteration cap (3 max).** Track count via the folder-quality-log's per-artifact section before each regeneration. If three iteration entries exist and the verdict is still not PASS, **escalate** to the operator with the evaluation report and stop. Don't run a fourth iteration — that's the load-bearing cost-control discipline.

**Operator bypass.** Include `--bypass-quality-loop` (or "skip the quality loop") in the original research request to skip the block for that invocation. The bypass records to the closest folder's `_quality-log.md` under `### Bypassed (manual override)`.

---

# Discovery Mode (v2.0)

**Purpose:** Recurring scan for new, emerging, or obscure high-leverage SEO tools that aren't in the
current stack or inventories — plus free public data sources and registries per MI arena. This is the
self-expanding mechanism from `spec-market-intelligence-engine.md` §6.3.

**Cadence:** Monthly scan (operator-triggered or scheduled via [MI-8]). Can also run ad hoc ("what new
tools are out there?").

**Trigger phrases:** "discover new SEO tools," "scan for emerging tools," "what new tools are out there,"
"run a discovery scan," "monthly tool scan."

## Discovery — inputs

Lighter than survey mode. Confirm with the operator:

1. **Scope:** Full scan (all categories) or focused (e.g., "just AEO/GEO," "just local SEO tools,"
   "just free data sources")?
2. **Recency window:** Default is "last 90 days" (tools launched, repriced, or significantly updated).
   Operator can narrow ("last 30 days") or widen ("last 6 months").
3. **Known stack:** Read `~/workspace/second-brain/03_domains/seo/tools/keelworks-standard-seo-stack.md`
   and existing `tool-*.md` files to know what's already tracked. Don't re-discover known tools.

## Discovery — research phase

Dispatch a `general-purpose` sub-agent with the following brief:

> Scan for SEO tools that are new, recently launched, recently repriced, or recently gained significant
> traction in the last [recency window]. Focus on tools that a small local-services SEO agency might
> not know about yet. Sources to check:
>
> 1. **Product Hunt** — search "SEO," "local SEO," "AEO," "AI search optimization," "rank tracking,"
>    "citation management" in the last [recency window]. Look for launches with 200+ upvotes or
>    featured status.
> 2. **SEO blogs and publications** — Search Engine Journal, Search Engine Land, Moz blog, Ahrefs blog,
>    BrightLocal blog, Near Media, Sterling Sky, Local SEO Guide. Look for "new tool," "tool review,"
>    "just launched," "beta" posts.
> 3. **Practitioner YouTube channels** — @nicksaraev, @nateherk, @MattDiggity, @chasereiner,
>    @JulianGoldie, @KyleRoof, plus any SEO tool review channels. Look for "I found this tool,"
>    "new SEO tool," "tool nobody talks about" videos.
> 4. **AEO/GEO-specific sources** — Lily Ray's content, Wil Reynolds, Rand Fishkin (SparkToro blog),
>    Marie Haynes, plus AEO-focused newsletters. This category churns fastest.
> 5. **Reddit r/SEO, r/bigseo, r/localseo** — practitioner discussions about tools they actually use
>    (vs. what vendors market). Look for "what tool do you use for [X]" threads.
> 6. **Free public data sources and registries** — government data portals, Google-operated tools
>    (Ads Transparency Center, Knowledge Panel, PageSpeed Insights, Search Console, Merchant Center),
>    Meta Ad Library, Yelp/BBB public profiles, Wikidata, industry directories. These are often
>    missed because they're not "SEO tools" but they provide data that closes MI arena gaps.
> 7. **Business viability signals** — for paid tools, check TrustMRR (`trustmrr.com`) for
>    Stripe-verified revenue data (MRR, churn rate, growth trend, for-sale status). Also check
>    Crunchbase for funding status and LinkedIn for team size/recent departures. A tool with
>    impressive features but declining revenue is a risk signal worth surfacing.
>
> For each candidate found, return:
> - Name and URL
> - What it does (one sentence)
> - Category (keyword research / rank tracking / local SEO / AEO-GEO / backlinks / content /
>   schema / audit / citation / social / data-source)
> - Pricing (free / freemium with limits / paid with entry tier price)
> - Why it's interesting (what's new or different about it)
> - Source where you found it (URL or channel name + video title)
> - Whether it's a TOOL (software you use) or a DATA SOURCE (public registry you query)

## Discovery — evaluation phase

For each candidate the sub-agent returns:

1. **Deduplicate** against existing `tool-*.md` notes and the five survey files. If the tool is already
   tracked, skip unless there's a significant update (new pricing, new features, pivot).

2. **Score against the tool-eval rubric** (`references/tool-eval-rubric.md`). Fill all five dimensions.

3. **Write a `tool-*.md` note** for every candidate scoring Trial or above. Write a brief note for
   Watch candidates. Skip-scored candidates get a one-line entry in the discovery log only.

4. **Register tool-gap rows** in `~/workspace/second-brain/_meta/handoffs/market-intelligence/_data-gap-register.md`
   for any candidate scoring Adopt or Trial (TG-row with status matching the recommendation).

5. **For data sources / registries:** append new entries to `mi-arena-source-checklist.md` under the
   relevant arena's "Public registries" column. This keeps the source checklist living — the same
   way the data-gap register grows. Mark which arena each source serves.

## Discovery — output

- `tool-*.md` notes in `~/workspace/second-brain/03_domains/seo/tools/` (one per evaluated candidate)
- Updated TG-rows in `_data-gap-register.md` (if any Adopt/Trial candidates)
- Updated `mi-arena-source-checklist.md` (if any new data sources found)
- A **discovery log entry** appended to the bottom of this invocation's chat summary:

```markdown
### Discovery scan — [YYYY-MM-DD]
- **Recency window:** [X days]
- **Candidates found:** [N]
- **Evaluated:** [N] (after dedup)
- **Adopt:** [list or "none"]
- **Trial:** [list or "none"]
- **Watch:** [list or "none"]
- **Skip:** [list or "none"]
- **Data sources added to checklist:** [list or "none"]
- **Sources consulted:** [list]
```

## Discovery — closing

Run `gate-peer-reviewer` on the `tool-*.md` notes produced. Then emit the auto-invoke
output-quality-loop block (same convention as survey mode Phase 6b) listing the produced artifacts.

Report back with a terse summary: number of candidates found, number evaluated, top surprises,
any adopt/trial recommendations, data sources added.

---

# Intake Mode (v2.0)

**Purpose:** The "I saw a tool" path. The operator finds a tool (browsing, a YouTube video, a blog
post, a conference talk, a competitor's site) and wants it evaluated quickly against the current stack.
This is the self-expanding mechanism from `spec-market-intelligence-engine.md` §6.4.

**Trigger phrases:** "digest this tool," "evaluate this tool [name/URL]," "I saw a tool called [X],"
or a URL/name dropped with evaluation intent. Also triggered by processing files in
`~/workspace/second-brain/00_inbox/tools-pending/`.

## Intake — two entry points

### Entry point 1: In-chat trigger

The operator says something like "digest this tool: [URL or name]" or "evaluate Otterly" or
"I saw this tool in a video: [YouTube URL]."

1. **If the input is a YouTube URL or article URL:** invoke `vis-extraction` (VIS — the structured
   intelligence extraction skill for video/article sources) first to extract structured intelligence
   from the source. The VIS output becomes the research input for the eval rubric — don't
   re-research what VIS already extracted.

2. **If the input is a tool name only:** dispatch a `general-purpose` sub-agent to research the tool:
   vendor page, current pricing, features, reviews, founding team, funding status. Same depth as
   Survey mode's per-tool research but for a single tool.

3. **If the input is a tool name + context** ("I saw PRO Electric using this tool called X on their
   site"): research the tool AND note the competitive-intelligence context in the `tool-*.md` note.

### Entry point 2: Inbox queue

The operator drops files (links, notes, screenshots) into `~/workspace/second-brain/00_inbox/tools-pending/`.
When the skill is invoked with "process the tools inbox" or "digest pending tools":

1. Read all files in `00_inbox/tools-pending/`.
2. For each file, extract the tool name/URL and any context the operator included.
3. Process each tool through the same pipeline as Entry point 1.
4. After processing, move the source file to `00_inbox/tools-pending/_processed/` (create if needed)
   with a date prefix: `YYYY-MM-DD-<original-filename>`.

## Intake — evaluation

Regardless of entry point:

1. **Deduplicate** against existing `tool-*.md` notes. If the tool already has a note, update it
   rather than creating a duplicate. Flag the update to the operator: "This tool already has a note
   at [path]. Updating with new information."

2. **Score against the tool-eval rubric** (`references/tool-eval-rubric.md`). Fill all five dimensions
   with rationale.

3. **Present the rubric + recommendation to the operator** before writing. Unlike discovery mode
   (which batch-writes), intake mode is interactive — the operator confirms or overrides the
   recommendation before it's committed.

4. **Write the `tool-*.md` note** in `~/workspace/second-brain/03_domains/seo/tools/` with:
   - Full KOS frontmatter (`type: tool`, `status: <adopted|evaluating|killed>`, `domains: [seo]`)
   - Source attribution (where the operator found it, VIS extraction link if applicable)
   - The filled eval rubric block
   - The recommendation + operator's decision (if they overrode)

5. **Register a TG-row** in `_data-gap-register.md` if the recommendation is Adopt or Trial.

6. **Update `keelworks-standard-seo-stack.md`** if the recommendation is Adopt — add the tool to
   the appropriate tier with a note on what it replaces or supplements.

## Intake — tool-*.md template

```markdown
---
type: tool
status: <adopted|evaluating|killed>
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
domains: [seo]
source: <where the operator found it — URL, video title, "discovery scan YYYY-MM-DD", etc.>
tags: [tool, seo, <category>]
---

# tool-<vendor-or-product>

**What it does:** <one sentence>
**Category:** <keyword-research | rank-tracking | local-seo | aeo-geo | backlinks | content |
schema | audit | citation | social | data-source>
**Vendor:** <company name> · <year founded if known> · <funding status if known>
**URL:** <vendor URL>
**Pricing:** <current pricing tiers — entry tier highlighted>

## Eval rubric

| Dimension | Score | Rationale |
|---|---|---|
| Value | /3 | |
| Time saved | /3 | |
| Cost | /3 | |
| Fit | /3 | |
| Overlap | /3 | |

**Composite:** X.X / 3.0
**Recommendation:** Adopt / Trial / Watch / Skip
**Override applied:** None / [describe]
**Data gaps closed:** [DG-X if applicable]

## What's interesting

<2-3 paragraphs: what makes this tool notable, what problem it solves, how it compares to what's
in the stack. Honest assessment — call out hype, lock-in, and gaps.>

## Source

<Where the operator found it. If VIS-extracted, link to the source note.>

## See also

- [[keelworks-standard-seo-stack]] · [[per-task-tool-recommendations]] · [[_data-gap-register]]
- [[tool-eval-rubric]] · [[_README]]
```

## Intake — closing

Run `gate-peer-reviewer` on the `tool-*.md` note. Then emit the auto-invoke output-quality-loop
block listing the produced artifact(s).

Report back: tool name, recommendation, composite score, any data gaps it closes, whether the
standard stack was updated.

---

## Reporting back to the operator

### Survey mode
End with a terse summary (per `feedback_terse_completion_reports.md`):

- Number of tools surveyed
- Top 3 surprises from the research
- Top recommendation per category for this specific agency context
- Blocked questions if any (e.g., "vendor pricing page was behind a sales-call gate")

### Discovery mode
- Candidates found / evaluated / adopt / trial / watch / skip counts
- Top surprises (tools nobody talks about, significant repricing, new entrants)
- Data sources added to the arena checklist
- Any data gaps that could be closed by an adopt/trial candidate

### Intake mode
- Tool name + composite score + recommendation
- Whether the operator confirmed or overrode
- Stack / register updates made
- Data gaps closed (if any)

Use bullets, not paragraphs. Don't restate what was changed — Oliver can see the diff in the files.

## Things that will make this skill fail

In order of how often they happen:

1. **Skipping the input-confirmation step.** Vague inputs ("survey SEO tools for an agency") produce generic outputs. Always confirm agency size, vertical, current stack, output folder.

2. **Trusting stale pricing.** Most aggregator articles carry stale pricing. Sub-agents must verify against current vendor pages. If a vendor's pricing page is behind a sales-call gate, say so and quote the most recent third-party confirmation with a date.

3. **Generic vertical framing.** "For local-services agencies" works in the canonical exemplar because the canonical exemplar was for a local-services agency. For an e-commerce or SaaS context, rewrite the framing throughout, not just in the executive summary.

4. **Underweighting the AEO/GEO category for local clients.** Most AEO tools are enterprise-priced. The local-specific tools (Local Falcon, Otterly Lite, BrightLocal's AI features) are the right recommendation for local clients — but they're often missed because the funded names dominate the search results.

5. **Writing in marketing voice.** Tools have weaknesses. Vendors have lock-in. Free tiers tighten. Say so. Oliver's memory explicitly captures this preference.

6. **Forgetting the Methodology section.** It's not optional — it's the canonical artifact that lets future-Oliver and future-Claude understand how the recommendations were made and what to update next time.

## Versioning and the canonical exemplar

This skill assumes the canonical exemplar at `~/workspace/second-brain/03_domains/seo/tools/` is the most-recently-validated version. If the operator has updated those files (e.g., quarterly refresh), use the updated versions as the new template. The skill follows the exemplar; the exemplar doesn't follow the skill.

When the AEO/GEO category churns (new funding rounds, new tools, pivots) the exemplar files should be refreshed quarterly. This skill should be invoked for that refresh too — "refresh the SEO tools landscape" is a valid trigger.

## Changelog

### v2.0 (2026-06-15) — Discovery mode + Intake mode + Tool-eval rubric

**Added:**
- **Discovery mode** — recurring scan for new/emerging/obscure tools + free public data sources per MI arena. Dispatches a sub-agent to check Product Hunt, SEO blogs, practitioner YouTube, Reddit, and public registries. Candidates scored against the tool-eval rubric. Produces `tool-*.md` notes + TG-rows + arena source checklist updates.
- **Intake mode** — operator-initiated single-tool evaluation pipeline. Two entry points: in-chat ("digest this tool") and inbox queue (`00_inbox/tools-pending/`). Runs VIS extraction if source is a video/article URL. Scores against tool-eval rubric. Interactive — operator confirms recommendation before commit.
- **Tool-eval rubric** (`references/tool-eval-rubric.md`) — 5-dimension scoring (Value / Time saved / Cost / Fit / Overlap) with weighted composite, adopt/trial/watch/skip thresholds, and override rules (data-gap closer, cost ceiling, enterprise-gated, stack consolidation).
- **Mode selection table** — skill now routes to Survey, Discovery, or Intake based on trigger phrase.
- **Maintenance notes M4, M5** — discovery source freshness + VIS-extraction dependency.
- **See also** — cross-links to tool-eval rubric, mi-arena-source-checklist, _data-gap-register, vis-extraction skill.

**Changed:**
- Skill title → v2.0. Description updated to cover all three modes and new trigger phrases.
- "Reporting back" section split by mode (survey / discovery / intake).

**Unchanged:**
- Survey mode (Phases 1–6) — fully preserved, no modifications.
- All existing maintenance notes (M1–M3) — unchanged.
- Canonical exemplar path and pre-flight recovery logic — unchanged.

**Validated:**
- Discovery mode: real scan on 2026-06-15 found 12 candidates, produced `tool-hubspot-aeo-grader.md` (Adopt), added HubSpot AEO Grader to V3 arena source checklist.
- Intake mode: real evaluation of LocalRank.so on 2026-06-15, produced `tool-localrank-so.md` (Skip, overridden from Watch — business viability risk, declining MRR (monthly recurring revenue), unproven LLM Citations feature).

### v1.0 (2026-05-23) — Initial release

- Full survey mode: 5-file output set (free/paid/AEO-GEO/per-task/stack)
- Canonical exemplar at `~/workspace/second-brain/03_domains/seo/tools/`
- Maintenance notes M1–M3

## Maintenance notes

These are known issues that future-Claude or future-Oliver should be aware of when invoking, debugging, or extending this skill. Documented inline so they're discoverable when something goes wrong rather than hidden in chat history.

### M1: Path dependency on the canonical exemplar (added 2026-05-23, v1.0)

**The issue:** This skill references the canonical exemplar at `~/workspace/second-brain/03_domains/seo/tools/` by literal path in multiple places (the Pre-flight section, the methodology references, the "See also" section, the recovery instructions). If that folder is moved or renamed, this skill will fail to read its exemplar on first run.

**How it surfaces:** Read tool errors with "file not found" against the canonical paths during Phase 2 / Phase 3 synthesis.

**How to fix:**

1. The Pre-flight section has explicit recovery guidance — search the vault by filename, update paths, proceed.
2. After recovering, do a find-and-replace across this SKILL.md to update all references to the new canonical path so future invocations don't need to re-recover. The literal string to search for is the path above.

**Why it wasn't designed away:** Hardcoding the canonical exemplar path is the simplest design that works today. The alternatives (querying a registry, scanning the vault for `tags: [tool, seo, inventory]` frontmatter) are more durable but heavier; they don't pay back at one canonical instance. If the path moves more than once, refactor to dynamic discovery.

### M2: Vertical calibration is residential-services-shaped at v1.0 (added 2026-05-23, v1.0)

**The issue:** This skill was authored using a residential-services agency (Keelworks serving electricians and contractors) as the calibration target. The skill body says to "rewrite the framing throughout" for other verticals, but the underlying tool recommendations, tier transitions, and skip-lists are residential-services-flavored.

**How it surfaces:** Outputs will read as "off-vertical" — e.g., recommending BrightLocal as a default for an e-commerce agency where it's irrelevant, or naming Local Falcon as the AEO primary for a B2B SaaS context where local search doesn't apply.

**How to fix when it first happens:**

1. Run the skill on the off-vertical context anyway and capture the first round of outputs.
2. Mark each section that reads as off-vertical and capture the operator's correction.
3. Update this SKILL.md with a vertical-calibration table or branching logic — e.g., "if vertical = e-commerce, default rank tracker becomes Ahrefs not BrightLocal" and similar.
4. Bump skill version to v1.1 and document the verticals it's been validated against.

**Why it wasn't designed away in v1.0:** Without a second vertical to calibrate against, premature abstraction would have produced worse defaults. The residential-services calibration is concrete and known-good; the abstract version comes after the second use case.

### M3: AEO/GEO category churn (added 2026-05-23, v1.0)

**The issue:** The AEO/GEO category churns fast. Tools featured prominently in this skill's documentation (Profound at $1B valuation, Peec AI doubling ARR (annual recurring revenue), Local Falcon as the local primary) may pivot, get acquired, shut down, or be displaced by new entrants on a quarterly cadence.

**How it surfaces:** Sub-agent research returns reports that "Profound was acquired by [X]" or "Local Falcon discontinued the AEO module" or similar. Or a new dominant tool emerges that the skill doesn't mention.

**How to fix:**

1. The skill itself is fine — the sub-agent research phase is designed to surface current category state, not to assume the 2026-05 snapshot is current.
2. Refresh the canonical exemplar quarterly (the skill's "Versioning" section above already documents this expectation).
3. If a category-shaping event happens (e.g., Google launches its own AEO tracking product, or one of the funded names goes public), update this SKILL.md's "Sub-agent 2: AEO/GEO tools" default tool list so future research is anchored against current state.

### M4: Discovery mode sub-agent source freshness (added 2026-06-15, v2.0)

**The issue:** The discovery sub-agent's source list (Product Hunt, specific YouTube channels, specific blogs) will go stale as channels rename, blogs shut down, or new authoritative sources emerge.

**How it surfaces:** Discovery scans return thin candidate lists despite the category being active, or miss tools that practitioners are discussing on platforms the sub-agent isn't checking.

**How to fix:**
1. After a thin discovery scan, manually check 2-3 of the listed sources to confirm they're still active and producing relevant content.
2. Update the source list in the "Discovery — research phase" section. Add new sources; remove dead ones.
3. Ask the operator: "Are there SEO communities or channels I should be scanning that aren't on my list?"

**Why it wasn't designed away:** Hardcoding sources is the simplest design for v2.0. A dynamic source-discovery mechanism (scanning for "top SEO blogs 2026" each run) would add latency and complexity. The manual refresh at quarterly cadence is sufficient.

### M5: Intake mode VIS-extraction dependency (added 2026-06-15, v2.0)

**The issue:** Intake mode calls `vis-extraction` for YouTube/article URLs. If `vis-extraction` is unavailable, broken, or produces unexpected output format, the intake pipeline stalls.

**How it surfaces:** Intake invocation with a YouTube URL fails or produces a `tool-*.md` note with empty "What's interesting" section because VIS output wasn't parsed correctly.

**How to fix:**
1. Fall back to direct sub-agent research (same as the "tool name only" path). The VIS extraction is a quality enhancer, not a hard dependency.
2. Note in the `tool-*.md` that VIS extraction was skipped and the assessment is based on sub-agent research only.

**Why it wasn't designed away:** VIS extraction adds significant value (structured intelligence from video/article sources) and is worth the dependency. The fallback path exists; it just needs to be exercised.

### M6: Rubric-contract follow-through not gate-enforced (added 2026-06-15, v2.0)

**The issue:** The tool-eval rubric defines explicit post-score actions per recommendation tier (Adopt → add to stack + register TG-row; Watch → status: evaluating; etc.). Nothing in the current gate infrastructure verifies that these actions were actually taken. In the MI-6 validation run, three rubric-contract violations survived the initial gate-peer-reviewer pass: (1) HubSpot AEO Grader scored Adopt but was never added to `keelworks-standard-seo-stack.md`, (2) same tool scored Adopt but no TG-row was registered in `_data-gap-register.md`, (3) LocalRank.so had `status: killed` in frontmatter but `Recommendation: Watch` in the rubric block — an undocumented override.

**How it surfaces:** Tool notes pass the gate (frontmatter valid, no placeholders, links resolve) but the rubric's own action column is silently ignored. The stack and register drift from the tool notes.

**How to fix (future work, not this session):**
1. `G-chat-close` / omission-check-registry needs an OC-17 "rubric-contract-follow-through" check: for every `tool-*.md` written in the session, verify the recommendation tier's action column was executed (stack updated if Adopt, TG-row registered if Adopt/Trial, status matches recommendation or override is documented).
2. `gate-type-registry` needs `seo-tooling-landscape-research` registered as a gate type so discovery/intake runs get a purpose-built gate instead of G-default.
3. `output-quality-loop` spec-routing-table needs a `tool-*.md` entry that checks status/recommendation mapping consistency.

**Why it wasn't designed away in v2.0:** The rubric and modes were the v2.0 deliverable. Gate integration is a separate handoff (it touches gate-peer-reviewer, omission-check-registry, and output-quality-loop — three different skills). Documented here so the gap is visible and trackable.

### How to add a new maintenance note

When the skill errors or produces a calibration miss in production, add a new entry here following the pattern: **Issue → How it surfaces → How to fix → Why it wasn't designed away.** Date-stamp the entry. This is how future-Claude learns from past failures without re-hitting the same wall.

## See also (inside the vault — for the model invoking this skill)

- `~/workspace/second-brain/_meta/conventions.md` — KOS naming and frontmatter conventions
- `~/workspace/second-brain/_meta/plain-language-conventions.md` — plain-language rules
- `~/workspace/skills/plain-language-translation/SKILL.md` — retroactive plain-language pass if needed
- `~/workspace/skills/meta-document-primer/SKILL.md` — for generating a primer if the destination folder lacks one
- `~/workspace/skills/seo-tooling-landscape-research/references/tool-eval-rubric.md` — the scoring rubric used by discovery and intake modes
- `~/workspace/second-brain/_meta/handoffs/market-intelligence/mi-arena-source-checklist.md` — per-arena source checklist that discovery mode appends to
- `~/workspace/second-brain/_meta/handoffs/market-intelligence/_data-gap-register.md` — tool-gap register that both modes feed
- `~/workspace/skills/vis-extraction/SKILL.md` — VIS extraction used by intake mode for video/article sources
