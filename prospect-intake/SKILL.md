---
name: prospect-intake
version: 1.0
description: >
  Turn a prospective client into a call-ready folder from a single line. Given a business name +
  domain URL (+ optional lead source), this orchestrator scaffolds a prospect folder and runs the
  pre-sale analysis pipeline end-to-end: captures the homepage, produces a domain-only client-fact
  brief, runs a homepage SEO audit, runs a LIGHT competitor glance, then synthesizes a call
  one-pager (talking points), a proposed engagement plan, and ballpark pricing — and logs the
  prospect in the pipeline tracker. Use whenever the operator says "new prospect," "research this
  lead before the call," "prep me for a discovery call with X," "analyze this prospect's website,"
  "intake <business>," "add a prospect," or pastes a business name + URL in a sales/pre-client
  context. Also use in BATCH mode when given a list or CSV of prospects to triage before deciding
  who's worth a call. This is the pre-sale sibling to client-fact-research (which is for signed
  clients) — it composes existing skills in a lighter, public-sources-only mode and never commits
  pricing or issues an invoice. On signing, the prospect is promoted to _active/ and the full
  onboarding workflow + invoice-generation take over.
---

# Prospect Intake (v1.0)

A composing skill. It does not invent new research methods — it orchestrates skills you already
have ([[client-fact-research]], [[sop-homepage-seo-audit]], [[competitor-deep-research]]) in a
**pre-sale mode** and writes everything into the prospect workspace at
`~/workspace/second-brain/04_projects/clients/_prospects/<slug>/`.

The goal is to remove friction: one instruction in, a call-ready folder out. You walk into the
discovery call already knowing the prospect's site, their gaps, who's beating them, what you'd
propose, and roughly what you'd charge.

**Worked examples to model output on:** the signed-client briefs for EV Electric Services and S&H
Contracting (`~/workspace/second-brain/05_shared-intelligence/research-briefs/clients/`). A
prospect's `analysis/brief.md` is the same shape, just researched from public sources only.

---

## When to use

- "New prospect: <business>, <url>" / "intake <business>"
- "Research this lead before our call"
- "Prep me for the discovery call with <business>"
- "Analyze this prospect's website and give me talking points"
- A business name + URL pasted in a sales / pre-client context
- A list or CSV of leads to triage (→ BATCH mode)

Do **not** use this skill for:

- Signed clients → use [[client-fact-research]] + [[checklist-new-client-onboarding]].
- A full competitive teardown → use [[site-capture-engine]] or the full [[competitor-deep-research]] run.
- Issuing a real invoice → use [[invoice-generation]] (only after signing).

---

## Inputs

Confirm as **plain text** — do NOT use AskUserQuestion (it's been glitching in Cowork per Oliver's
standing feedback). Only the first two are required; the rest sharpen the output.

1. **Business name** (required) — e.g. "AJ Long Electric".
2. **Domain URL** (required) — e.g. `https://ajlongelectric.com/`.
3. **Lead source** — referral / inbound / outbound / cold / event. Defaults to `unknown`.
4. **Slug** — derived from the business name (kebab-case) unless overridden. Must match the eventual
   `_active/<slug>/` slug so promotion is a rename-free copy.
5. **Service focus + service area** — if known, narrows the competitor glance. If not, infer from
   the site.
6. **Known competitors** — if the operator names any, skip discovery for those.
7. **Call date** — for the pipeline row, if scheduled.

If only name + URL are given, proceed — infer the rest from the site and flag inferences as
"confirm on the call."

---

## Pre-flight reads

Before running, read:

- `~/workspace/second-brain/04_projects/clients/_prospects/_README.md` — the folder contract.
- `~/workspace/second-brain/04_projects/clients/_prospects/_TEMPLATE/` — the skeleton you'll copy.
- `~/workspace/skills/prospect-intake/references/synthesis-guide.md` — how to write talking points + plan.
- `~/workspace/skills/prospect-intake/references/pricing-anchors.md` — the EV/S&H pricing model.
- `~/workspace/second-brain/_meta/conventions.md` and `plain-language-conventions.md` — voice + naming.

Create a task-list entry per phase so the operator can watch progress.

---

## The pipeline (single prospect)

### Phase 1 — Scaffold the prospect folder

1. Copy `_prospects/_TEMPLATE/` → `_prospects/<slug>/` (recursive, non-destructive — if the folder
   already exists, stop and ask; never overwrite an existing prospect).
2. Replace every placeholder in the copied files: `<prospect-slug>`, `<Business Name>`, `<url>`,
   `<source>`, `<YYYY-MM-DD>` (today = run date), stage `lead`.
3. Add a row to `_prospects/_prospect-pipeline.md` under "Open prospects" (stage `researching`).

### Phase 2 — Capture the homepage

The homepage SEO audit works against **source HTML**, so capture it first.

1. `mcp__workspace__web_fetch` the domain → save raw HTML to
   `_prospects/<slug>/analysis/snapshot-homepage-<date>-source.html`.
2. If the fetch returns a client-rendered shell (Next.js / Wix / Squarespace — little body, "enable
   JavaScript", empty content), escalate to Claude in Chrome (`navigate` → `get_page_text` /
   `read_page`) to get the rendered content. Note in the audit which method was used.
3. Modern Next.js/React sites embed full content as JSON-LD + RSC flight data in the HTML — the raw
   fetch usually still yields schema, meta, and content even when it looks sparse. Check before
   escalating.

### Phase 3 — Domain-only client-fact brief

Invoke [[client-fact-research]] with the **output override** pointed at
`_prospects/<slug>/analysis/brief.md`, in **domain-only mode**:

- Inputs are the domain + public sources only — there are no meeting notes, no project README, no
  admin extracts (this is a prospect, not a client). Skip the "inventory existing vault knowledge"
  phase; there's nothing there yet.
- Populate from: the captured homepage + key pages (about, services, contact), the prospect's GBP
  public listing, directory profiles (Yelp / Angi / Thumbtack / BBB), public review counts, and
  public state licensing lookups (VA DPOR, DC, MD).
- Sections 1–9 are researchable from public sources. §10 (accounts ownership) is **inferred / best
  guess** — flag everything as "confirm on the call." §12 (growth target) becomes **our growth
  hypothesis**, not the owner's stated target.
- Mark every gap `<confirm on call>`. The brief's job pre-sale is to be 80% right and honest about
  the 20%, not to be airtight.
- Keep the brief frontmatter `prospect: true` and `status: draft`.

### Phase 4 — Homepage SEO audit

Run [[sop-homepage-seo-audit]] grep commands against the captured source snapshot, writing findings
to `_prospects/<slug>/analysis/audit-homepage-seo.md` (the template stub is already there).

- Pull title, meta, canonical, JSON-LD schema, H1, phone/address (NAP), copyright year, generator,
  `wp-content/plugins/` paths, social links.
- Mark the plugin list **"partial — public-source visible only"** (source scraping misses ~40–50%
  of plugins; full inventory needs admin access we don't have pre-sale).
- End with the **priority fix list** — the 3 most visible, most pitchable defects. These become
  talking points.

### Phase 5 — Competitor glance (LIGHT — default)

This is the **Tier-2 light pass** of [[competitor-deep-research]], NOT the 12–16h full run.

- Web-search the prospect's core service + city (e.g. "panel upgrade Fairfax VA"). Take the top
  organic + map-pack results.
- Name 3–5 businesses outranking the prospect, one line each on why they win (more pages, schema,
  reviews, GBP strength).
- Write the **headline gap** — the single most exploitable difference — to
  `_prospects/<slug>/analysis/competitor-glance.md`.
- Time budget: ~15–20 min. If the operator explicitly wants depth, offer the full
  competitor-deep-research run as a separate step (don't silently upgrade).

### Phase 6 — Synthesize the call materials

Per `references/synthesis-guide.md` and `references/pricing-anchors.md`, write:

- `talking-points.md` — the one-screen call sheet: 30-second read, three specific things to point
  at (lifted from the audit + competitor gap), discovery questions, the one-sentence pitch,
  objection prep.
- `engagement-plan.md` — proposed outcome + phased plan + what we need from them + why us.
- `proposal/draft-pricing.md` — **proposed** numbers anchored to the EV/S&H model (onboarding fee +
  value-based retainer that starts on first booked job; client pays tooling/community directly).
  Propose, then leave it for the operator to edit. Never present this as final.

### Phase 7 — Update state + report

- Set `_status.md` and `_state/prospect.json` to stage `ready-for-call`, flip the analysis flags.
- Update the pipeline row's stage + next action.
- Report terse (see Reporting).

---

## Batch mode

When given a list or CSV of prospects (columns: `name, domain, source` — see
`references/batch-mode.md`):

1. Confirm the list back as plain text and the per-prospect depth (default: light competitor pass).
2. Run Phases 1–6 for each row. Keep each prospect self-contained in its own folder.
3. Produce a single combined view in the pipeline tracker, then recommend a **triage order** —
   which prospects look highest-fit / highest-pain / most-winnable — so the operator spends call
   time on the best leads first.
4. Honest triage: flag any prospect that looks like a poor fit (out of service area, no fixable
   gap, dead site) rather than padding the list.

---

## Output locations

```
_prospects/<slug>/
├── README.md                              (hub — identity, stage, links)
├── _status.md                             (stage snapshot)
├── _state/prospect.json                   (machine state)
├── analysis/
│   ├── snapshot-homepage-<date>-source.html
│   ├── brief.md                           (Phase 3)
│   ├── audit-homepage-seo.md              (Phase 4)
│   └── competitor-glance.md               (Phase 5)
├── talking-points.md                      (Phase 6)
├── engagement-plan.md                     (Phase 6)
└── proposal/draft-pricing.md              (Phase 6)
```

Pipeline row → `_prospects/_prospect-pipeline.md`.

On signing → promote per `_prospects/_README.md` (copy into `_active/<slug>/`, promote brief to
`research-briefs/clients/<slug>/brief.md`, hand to onboarding + invoice-generation).

---

## Pre-sale-mode deltas (how this differs from the signed-client skills)

| Dimension | Signed-client flow | Prospect-intake (pre-sale) |
|---|---|---|
| Sources | Meeting notes + README + admin extracts + access | Public website + public profiles only |
| Brief §10 ownership | Verified from admin panels | Inferred; "confirm on call" |
| Brief §12 growth target | Owner's stated target | Our hypothesis |
| Competitor depth | Full deep research (12–16h) | Light glance (~15–20 min) |
| Pricing | Real invoice via invoice-generation | Proposed ballpark only |
| Quality loop | Full output-quality-loop | Optional / on-demand (default off for speed) |
| Folder | `_active/<slug>/` | `_prospects/<slug>/` |

---

## Vault stewardship

1. **Non-destructive.** Never overwrite an existing `_prospects/<slug>/`. If it exists, ask whether
   to refresh in place or pick a new slug.
2. **Don't touch `_active/`, `_TEMPLATE/`, or any signed-client file** from this skill.
3. **Cross-link.** Every file the skill writes already links to its parent (`README` ↔ analysis ↔
   pipeline) via the template — preserve those wikilinks when filling placeholders.
4. **Plain language.** Write brief + talking points in plain language; gloss jargon (NAP, GBP, GSC,
   schema/JSON-LD) inline on first use.
5. **Honest assessment.** Mark inferences, call out dead sites or poor fit. Pre-sale confidence is
   lower by design; say so.

---

## Verification — before declaring done

1. Folder exists at `_prospects/<slug>/` with all template files, every placeholder replaced (grep
   for leftover `<` `>` tokens — none should remain except intentional `<confirm on call>` flags).
2. `analysis/` has the snapshot, brief, audit, and competitor glance; each has valid frontmatter.
3. `talking-points.md` fits one screen and every "thing to point at" traces to a real audit or
   competitor finding (no invented defects).
4. `draft-pricing.md` numbers are present and anchored to the pricing-anchors reference, clearly
   marked **proposed**.
5. Pipeline row added; `_status.md` + `prospect.json` stage = `ready-for-call`.
6. No secrets, no real invoice, nothing written outside `_prospects/<slug>/` (except the pipeline row).

---

## Reporting back

Terse, per `feedback_terse_completion_reports`:

- Folder: `_prospects/<slug>/` — stage `ready-for-call`.
- The 3 lead talking points (one line each).
- The headline competitor gap.
- Proposed pricing in one line.
- Confidence flags / poor-fit warning if any.
- Open questions to confirm on the call.

Don't restate the files — the operator can open them.

---

## Working principles

1. **Compose, don't reinvent.** This skill's value is sequencing existing skills, not new research
   logic. If a sub-skill improves, this one inherits it.
2. **Speed over completeness pre-sale.** 80% right + honest about gaps beats airtight-but-slow. The
   call fills the gaps.
3. **Never commit.** Pricing is proposed, ownership is inferred, the plan is a pitch. Commitment
   happens at signing, through the onboarding + invoice skills.
4. **Triage honestly in batch.** The point of batch mode is to NOT waste call time on bad leads.

---

## See also

- [[_README]] — prospects folder guide
- [[client-fact-research]] — signed-client sibling (domain-only mode reused here)
- [[sop-homepage-seo-audit]] — Phase 4 engine
- [[competitor-deep-research]] — Phase 5 engine (light pass)
- [[invoice-generation]] — fires on signing, not here
- [[checklist-new-client-onboarding]] — takes over on promotion
- [[conventions]] / [[plain-language-conventions]]

---

## Maintenance notes

### M1: Homepage capture depends on web_fetch / Claude in Chrome (added 2026-06-11, v1.0)

**The issue:** Phase 2 needs source HTML. Client-rendered sites return a shell from web_fetch.
**How to fix:** Escalate to Claude in Chrome `get_page_text`. Check for embedded JSON-LD/RSC first —
often the raw fetch is enough even when it looks empty.

### M2: Slug must match the eventual active slug (added 2026-06-11, v1.0)

**The issue:** If the prospect slug differs from the slug used when they sign, promotion isn't a
clean copy and links break.
**How to fix:** Derive the slug the same way client folders are named (kebab-case business name) and
confirm it with the operator before scaffolding.
