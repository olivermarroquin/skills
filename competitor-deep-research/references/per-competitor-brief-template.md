# Per-competitor brief template

Copy this template for each Tier-1 competitor. Fill in every section. If a section truly doesn't apply, write "Not applicable because…" rather than skipping silently — operators need to know whether a gap is in the competitor or in your audit.

The template uses **11 sections in a fixed order** (Sections 3.5 and 7.5 were added by the 2026-06-03 enhancements; the section numbering preserves the original sequence so synthesis-reading code stays compatible). Keeping the order consistent across all competitors is what makes the synthesis writable later.

For Tier-1 **primaries**, fill every section including 3.5 (≥5 audited pages) and 7.5 (5–10 top-trafficked pages). For Tier-1 **secondaries**, Section 3.5 is required (2–3 audited pages minimum) and Section 7.5 is optional (drop it if budget is short, but note the omission).

For **Tier-2 light-scan competitors**, do NOT use this template — they get a single structured row inside the synthesis's Tier-2 light-scan table instead.

---

```markdown
---
type: competitor-research
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
project: <client-slug>
competitor-slug: <competitor-slug>
competitor-tier: primary | secondary
relevant-projects: [<client-slug>]
tags: [competitor-research, <client-slug>, <geography>, <industry>]
---

# Competitor Brief: <Business Name>

**Research date:** YYYY-MM-DD
**Researcher:** <agent name or person>
**Tier:** Primary deep dive | Secondary (lighter-touch)
**Source URLs audited:** <list URLs fetched, with date>

---

## Identity & positioning

- **Business name:**
- **Domain:**
- **Years in business:** (if discoverable; note "not displayed" if not)
- **Service area claimed:**
- **Tagline / hero positioning:**
- **Phone:**
- **Address:** (real physical address vs. service-area-business — note which)
- **Licenses displayed:** (state license numbers shown in footer or about page; this is a trust signal)

**Positioning angle:** One paragraph on what this competitor's brand voice and target customer segment look like. Are they premium? Discount? Family-narrative? Corporate? Founder-led? Faceless?

---

## Tech stack

The most important technical section. Fingerprint specifically — don't hand-wave.

- **Platform/CMS:** WordPress | static site generator | enterprise CMS | other. Evidence used: URL patterns, meta-generator tag, asset paths.
- **Hosting:** Identified via HTTP headers (`server:`, `x-powered-by:`, `x-nf-request-id:`, etc.).
- **Page builder/theme:** Elementor | Divi | Beaver Builder | custom | none. Evidence.
- **SEO plugin:** Yoast | AIOSEO | Rank Math | none visible. Evidence.
- **Cache plugin/CDN:** NitroPack | WP Rocket | LiteSpeed | Netlify Edge | other.
- **Schema markup:** Did you find JSON-LD blocks in the fetched HTML? What types (LocalBusiness, AggregateRating, Service, FAQPage)? Or none visible?
- **Image format:** WebP | AVIF | JPG/PNG only. This affects speed and modernness signal.
- **Analytics:** Google Tag Manager (with container ID if visible) | GA4 | other.
- **Lead capture:** Booking form? Live chat? Phone-only?
- **Agency credit (if present):** "Website by [agency]" footer credits tell you who's executing their SEO.
- **Other notable plugin/tool signatures:**

**What this means for the client:** One paragraph on how this competitor's tech stack compares to the client's, and what (if anything) is structurally hard to compete with vs. what's a non-issue.

---

## Content structure

Where the content moat lives — or doesn't.

- **Total indexed pages (from sitemap.xml):**
- **Breakdown by URL path tier:** Use a small table.

| Path | Page count | What this is |
|---|---|---|
| `/services/...` | N | Service pages |
| `/<region>-services/...` | N | Location pages |
| `/blog/...` | N | Blog posts |

- **City/location page depth (typical example):** Audit one location page. Word count estimate, what sections it includes, whether it names specific neighborhoods, permit offices, local-code references, case studies. Quote a representative snippet.
- **Service page depth (typical example):** Audit one service page. Word count estimate, sections, FAQs embedded, transparent pricing, internal-linking density.
- **Word count per typical page:** Estimate range (e.g., 1,500–2,000 for service pages, 600–1,000 for city pages).
- **Internal linking pattern:** Spider-web (service × city × neighborhood all interlink) | hub-and-spoke (services hub → city pages) | flat (no contextual interlinks).
- **Blog content (if any):** Topic mix, regional tagging, word count, refresh frequency. Are blog posts capturing research-stage queries?
- **FAQs:** Embedded inline on service/city pages? Centralized at a `/faq` URL only? None?

---

## Per-page deep audit

*(2026-06-03 enhancement — the "stalker-level" detail layer.)*

Run the per-page audit per `competitor-deep-research/SKILL.md` Phase 3 Step 8. One row per audited page. Tier-1 primaries: 5+ rows minimum (homepage + 2 service pages + 2 city pages). Tier-1 secondaries: 2–3 rows minimum.

Annotate the **Method** for each row (DataForSEO / free-toolkit-PageSpeed-Insights / mixed) so the data lineage stays auditable.

| URL | Page type | Words | Sents | Paras | H1 / H2 / H3 | Images | Alt-quality | Schema types | FAQs | Int. links (in-body) | Ext. links | Page load | LCP / INP / CLS | Pricing pub? | Method |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| / | homepage | | | | | | | | | | | | | | |
| /services/<svc>/ | service | | | | | | | | | | | | | | |
| /<region>/<city>/ | city | | | | | | | | | | | | | | |
| /services/<svc2>/ | service | | | | | | | | | | | | | | |
| /<region>/<city2>/ | city | | | | | | | | | | | | | | |

**Cross-page observations:**

Once 5+ rows are filled, scan the columns vertically. What's consistent across this competitor's pages? Examples to surface:

- "All 5 of AJ Long's audited pages share a 5-FAQ inline structure."
- "Mr. Electric's homepage is 1,400 words but the city pages drop to 620 — content depth is concentrated at the top."
- "Schema types are identical across the 5 audited pages (LocalBusiness + Service); FAQPage absent from every one."
- "Alt-text quality is high on the homepage hero (descriptive) but generic on service-page screenshots."

These per-page observations seed the Section 7.5 top-5-pages-pattern detection.

---

## SEO signals

- **Title tag patterns:** Quote 2–3 actual titles you observed and identify the pattern (e.g., `[keyword] [city] | [brand]`).
- **Meta description patterns:** Quote 1–2 actual descriptions. Do they include phone, review count, calls-to-action, or are they generic?
- **Top keywords targeted:** Inferred from H1s, titles, meta descriptions, and URL paths. List the 5–10 most visible target keywords.
- **FAQ patterns answered:** What questions does this competitor answer on service pages? Pricing transparency? Permit info? Timeline? Brand-name dropping?
- **Schema markup audit:** Restate from the tech stack section, but framed for SEO: what rich-result opportunities are they capturing or missing?
- **Heading hierarchy:** Clean (one H1, logical H2/H3) or messy?
- **Internal linking:** Restate from content section, framed for SEO topical-authority.

---

## Reviews / social proof

- **Google reviews count + rating:** From the source (BrightLocal, competitor's homepage claim, etc. — cite the source).
- **Reviews on own domain?** Yes/no. If yes, where (testimonials page, embedded on service pages, both)?
- **Other review platforms:** Yelp, BBB, Angi, HomeAdvisor, etc.
- **Testimonials format:** Customer name + last initial + source + date? Photo? Video?
- **Review schema markup:** AggregateRating JSON-LD present? Captures rich-result review stars or not?

---

## Backlink hints

Free-tools only by default — Ahrefs Free Backlink Checker, BrightLocal scan if the operator has one, manual citation checks.

- **Total links (source + date):**
- **Domain authority score (source):**
- **Most likely backlink sources (inferred):** Citation directories, Chamber of Commerce, contractor directories, blog mentions, BBB, Angi.
- **Citation presence (NAP signals):** Are Name/Address/Phone consistent across the major directories? Quick spot-checks on the highest-value ones.

---

## What's working for them (synthesis)

5–8 bullets. Each one must satisfy at least one of:

1. Hard data confirms it (page count, review count, rank, etc.)
2. It explains a ranking outcome (the data shows they rank, and this feature plausibly contributes)
3. It's a customer-trust mechanism even outside SEO (warranty, history, transparent pricing)

Lead with the strongest 2–3. Operators reading this for the first time should grasp the competitor's main strengths from the first three bullets alone.

---

## Top-5-pages pattern (what their best pages systematically do)

*(2026-06-03 enhancement — required for Tier-1 primaries; optional for secondaries.)*

Run per `competitor-deep-research/SKILL.md` Phase 3 Step 9. Identify the 5–10 most-trafficked pages on this competitor's site (DataForSEO Labs `relevant_pages/live` / SimilarWeb free / sitemap + nav-heuristic / operator-named). Apply the Section 3.5 audit columns to each. Document the structural traits present in **≥80% of the audited top pages** (4 of 5, 8 of 10).

**Top-5 (or top-10) pages audited:**

1. <URL> — <page type> — <one-line "what this page is">
2. <URL> — …
3. <URL> — …
4. <URL> — …
5. <URL> — …

**Shared structural traits (present in ≥80%):**

| Trait | Page-share | What the trait looks like in practice |
|---|---|---|
| Word count band | 4 of 5 | "3,500–4,000 words" |
| Why-choose-us tile structure | 5 of 5 | "6-tile grid above the fold" |
| Named-neighborhood density | 5 of 5 | "5+ specific neighborhoods named" |
| FAQ count | 4 of 5 | "Exactly 5 FAQs inline" |
| Case studies | 5 of 5 | "1 case study with named city + scenario" |
| Schema types | 5 of 5 | "LocalBusiness + Service; FAQPage absent" |
| Internal-link density | 5 of 5 | "≥10 sibling city-page links in body" |
| Image treatment | 4 of 5 | "Hero photo of real technician on job site" |

**What this tells us:**

One paragraph naming the structural blueprint. Example: "AJ Long's winning pattern is the city-localized service-deep page: 3,500-word body, 6-tile differentiators, 5 named neighborhoods, embedded permit references, 5 FAQs, 1 case study, dense internal linking. Every top-trafficked page matches this template; their lower-trafficked pages (blog posts, generic service pages) don't. Reproducing this blueprint is what the client's Core 30 build should match-or-beat."

**Source of traffic data:**

- `<source name + date + URL when applicable>` — `<which method used: DataForSEO Labs / SimilarWeb free / sitemap-heuristic / operator-named>`

---

## What's NOT working / opportunities for <client>

5–8 bullets. Each one must be:

1. Exploitable by the client (not just "any flaw" — flaws the client can credibly out-execute with their actual resources and strategy)
2. Confirmable in source (point to specific evidence)
3. Aligned with the client's strategic intent (don't list "no founder face" as a gap if the client's strategy is to be a faceless corporate brand)

End with a sub-bullet titled **"Pages where <client> could realistically outrank them"** that lists 3–5 specific query types or page topics where the gap is exploitable.

---

## Sources audited

- [Homepage](url) (fetched YYYY-MM-DD)
- [Service page](url) (fetched YYYY-MM-DD)
- [Location page](url) (fetched YYYY-MM-DD)
- [Sitemap](url) (N URLs indexed, fetched YYYY-MM-DD)
- Other inputs (BrightLocal scan, prior audit, etc. — cite with path)

Sibling briefs in this folder:
- [[<other-competitor-slug>]]
- [[<other-competitor-slug>]]
- [[synthesis-YYYY-MM-DD]]
```
