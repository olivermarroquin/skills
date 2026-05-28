---
name: seo-tooling-landscape-research
description: Survey the SEO tool landscape comprehensively for a given agency context — free tools, paid tools, AEO/GEO bleeding-edge category, per-task tool recommendations, and tiered stack proposals. Triggers on phrases like "survey SEO tools," "research SEO tooling landscape," "what SEO tools should we use for [vertical]," "build an SEO tool stack for [agency size]," "compare SEO tools," "evaluate AEO/GEO tools," "do an SEO tool inventory," or any time the user wants a comprehensive landscape report on SEO tooling for a new agency, vertical, client engagement, or category. Also use when an existing tool stack needs refreshing, when entering a new vertical that needs its own tool calibration, or when assessing a new SEO tool category (AI-search tools, schema tools, citation tools, etc.). Produces a 5-file output set: free tools inventory, paid tools inventory, AEO/GEO survey, per-task recommendations, tiered stack proposal — written into a configurable folder with proper KOS frontmatter, plain-language framing, and honest hype-vs-substance assessment.
---

# SEO Tooling Landscape Research Skill (v1.0)

This skill packages the systematic SEO tool survey methodology Oliver used on 2026-05-23 to evaluate ~47 tools for Keelworks's residential-services SEO work. It produces five interlinked inventory and synthesis files for any agency context.

The canonical exemplar lives at `~/workspace/second-brain/03_domains/seo/tools/`. The five files there are the reference output for this skill — read them before writing anything new.

## What this skill produces

Five Markdown files in the operator-specified output folder:

1. **free-seo-tools-inventory.md** — exhaustive inventory of free SEO tools across keyword research, competitor analysis, site audit, rank tracking, backlinks, schema, content optimization
2. **paid-seo-tools-inventory.md** — major paid tools with current pricing tiers, strengths, weaknesses, who-it's-for, fit-for-context rating
3. **aeo-geo-tools-survey.md** — bleeding-edge category for ranking in AI-generated answers; dedicated tools + emerging players + legacy SEO platform AEO modules
4. **keelworks-standard-seo-stack.md** (or `<agency>-standard-seo-stack.md`) — three-tier stack proposal (Solo / Growing / Scaled) with monthly cost totals and migration triggers
5. **per-task-tool-recommendations.md** — best tool by common SEO use case (keyword research, competitor content analysis, site audit, rank tracking, schema, backlinks, content briefs, citations, AI visibility, GBP audit)

Plus an update to the destination folder's `_README.md` adding a navigation section to the new files.

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

## Phase 6 — Closing step — Auto-invoke output-quality-loop

After Phase 5 verification passes, emit the standard auto-invoke block per `~/workspace/skills/output-quality-loop/references/auto-invoke-convention.md` and `~/workspace/second-brain/_meta/conventions.md` § "Output quality". This is the closing step every artifact-producing skill emits before declaring the chat done. Convention shipped Phase 5 of the output-quality-loop project (2026-05-28).

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

## Reporting back to the operator

End with a terse summary (per `feedback_terse_completion_reports.md`):

- Number of tools surveyed
- Top 3 surprises from the research
- Top recommendation per category for this specific agency context
- Blocked questions if any (e.g., "vendor pricing page was behind a sales-call gate")

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

**The issue:** The AEO/GEO category churns fast. Tools featured prominently in this skill's documentation (Profound at $1B valuation, Peec AI doubling ARR, Local Falcon as the local primary) may pivot, get acquired, shut down, or be displaced by new entrants on a quarterly cadence.

**How it surfaces:** Sub-agent research returns reports that "Profound was acquired by [X]" or "Local Falcon discontinued the AEO module" or similar. Or a new dominant tool emerges that the skill doesn't mention.

**How to fix:**

1. The skill itself is fine — the sub-agent research phase is designed to surface current category state, not to assume the 2026-05 snapshot is current.
2. Refresh the canonical exemplar quarterly (the skill's "Versioning" section above already documents this expectation).
3. If a category-shaping event happens (e.g., Google launches its own AEO tracking product, or one of the funded names goes public), update this SKILL.md's "Sub-agent 2: AEO/GEO tools" default tool list so future research is anchored against current state.

### How to add a new maintenance note

When the skill errors or produces a calibration miss in production, add a new entry here following the pattern: **Issue → How it surfaces → How to fix → Why it wasn't designed away.** Date-stamp the entry. This is how future-Claude learns from past failures without re-hitting the same wall.

## See also (inside the vault — for the model invoking this skill)

- `~/workspace/second-brain/_meta/conventions.md` — KOS naming and frontmatter conventions
- `~/workspace/second-brain/_meta/plain-language-conventions.md` — plain-language rules
- `~/workspace/skills/plain-language-translation/SKILL.md` — retroactive plain-language pass if needed
- `~/workspace/skills/meta-document-primer/SKILL.md` — for generating a primer if the destination folder lacks one
