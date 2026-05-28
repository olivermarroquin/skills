---
name: client-fact-research
description: Produce a Tier client-fact brief — per-client only — that the Phase 3c scaffolder (`scaffold-client-data.py`) consumes to author `data/client-<client-slug>.json` plus a credentials checklist. Triggers on phrases like "research this client," "produce a client-fact brief for X," "run client-fact research on Y," "write the client brief for Z," "client-research <slug>," "extract a client brief from these meeting notes," or any time the operator wants a per-client (not service-level, not city-level) factual research output that captures business identity, brand surface, contact data, service catalog, pricing tier, reviews, service area, licensing, current website tech, accounts ownership, lead sources, and growth target. Two inputs: (1) meeting-notes file path or pasted text, (2) the client's domain URL. Output: a single markdown file at second-brain/05_shared-intelligence/research-briefs/clients/<client-slug>/brief.md following the locked template at second-brain/05_shared-intelligence/research-briefs/_template-client-brief.md. Per-client subfolder so the brief can carry sidecar artifacts (intake forms, mining notes) without polluting the clients folder root.
---

# Client-fact Research

A reusable workflow for producing client-fact briefs. The briefs
sit at
`second-brain/05_shared-intelligence/research-briefs/clients/` and
feed the Phase 3c scaffolder for every Keelworks client. One brief
per client — never reused across clients.

This skill was authored as part of Phase 2d of the
[[client-seo-onboarding-automation]] blueprint. The first briefs
produced from it are EV Electric Services and S&H Contracting —
refer to those when this skill's instructions are unclear; they're
the worked examples.

This skill is a **sibling** to [[service-seo-research]] (Tier 1)
and [[city-base-research]] (Tier 2), and complements
[[competitor-deep-research]] (which does per-client competitive
analysis, not per-client fact gathering). The four skills sit at
different corners of the (client × service × city × competitor)
research cube. This one focuses on the client dimension.

---

## When to use

Trigger this skill when the operator wants client-level (not
service-level, not city-level, not service-by-city) factual
intelligence about a specific client. Typical triggers:

- "Research this client" + meeting notes attached
- "Produce a client-fact brief for [client]"
- "Run client-fact research on [client]"
- "Write the client brief for [client]"
- "Extract a client brief from these meeting notes"
- "Client-research <slug>" (terse form)
- A new client's onboarding kicked off and the operator wants a
  structured brief before scaffolding their data file

Do **not** use this skill for:

- Per-service research (use [[service-seo-research]])
- Per-city research (use [[city-base-research]])
- Per-(service × city) research (use Phase 2c intersection
  research engine — TBD)
- Per-client competitive analysis (use [[competitor-deep-research]])

---

## Inputs the skill needs

Confirm these with the operator before researching. Present as
plain text — do not use AskUserQuestion (it's been glitching in
Cowork per Oliver's standing feedback memory).

1. **Client slug.** kebab-case, lowercase, matches the project
   folder slug at `04_projects/clients/_active/<client-slug>/`
   (e.g. `ev-electric-services`, `s-and-h-contracting`).

2. **Meeting notes.** File path inside the vault (typically under
   `04_projects/clients/_active/<client-slug>/communications/meeting-notes/`)
   OR pasted text. If the client has no formal meeting notes yet,
   the project README's "Confirmed at kickoff" section is the
   acceptable substitute.

3. **Domain URL.** The client's primary website (e.g.
   `https://evelectric.pro/`, `https://shcontractingunlimited.com/`).
   Used for the live-site assessment in §9.

4. **Existing project context.** Has a project README been written?
   Are there admin-extracts already in
   `04_projects/clients/_active/<client-slug>/admin-extracts/`?
   Has Oliver run a competitor-deep-research pass that surfaces
   competitive context? Carry forward what exists — most of §1, §3,
   §7, §8, and §10 may already be documented in the README's
   decision archaeology.

5. **Output folder.** Default:
   `~/workspace/second-brain/05_shared-intelligence/research-briefs/clients/`.
   Override only if the operator wants the brief written
   somewhere else (rare).

6. **Time budget.** Useful to know up-front. Typical budget for a
   client brief from scratch with a comprehensive README + admin
   extracts already in the vault: 30-45 minutes (mostly synthesis
   of existing material plus a live-site assessment). Cold —
   meeting notes only, no prior research, no admin extracts:
   60-90 minutes.

If any input is missing, ask the operator before researching.
Underspecified inputs are the most common failure mode for this
skill.

---

## Pre-flight: read the canonical template and worked examples

Before producing anything new, read:

1. The locked template:
   `~/workspace/second-brain/05_shared-intelligence/research-briefs/_template-client-brief.md`
   — every section, every "What this feeds" line, every
   consumption contract with the Phase 3c scaffolder.

2. The worked examples (when they exist):
   `~/workspace/second-brain/05_shared-intelligence/research-briefs/clients/ev-electric-services/brief.md`
   and
   `~/workspace/second-brain/05_shared-intelligence/research-briefs/clients/s-and-h-contracting/brief.md`
   — what finished briefs look like for a well-instrumented
   client (EV) and a cold-research client (S&H).

3. The scaffolder data shape:
   `~/workspace/repos/ai-agency-core/scripts/data/client-ev-electric-services.json`
   — the JSON contract the brief feeds. Every JSON field needs a
   matching brief section.

4. The project README for the client being researched:
   `~/workspace/second-brain/04_projects/clients/_active/<client-slug>/README.md`
   — usually the densest single source of pre-existing client
   knowledge. The decision-archaeology section is gold.

5. The folder conventions:
   `~/workspace/second-brain/_meta/conventions.md` — frontmatter
   and naming rules.

6. The plain-language conventions:
   `~/workspace/second-brain/_meta/plain-language-conventions.md`.

If the template has moved or been renamed, search the vault by
filename (Glob `_template-client-brief.md`). If not found, the
template's content is described in the template file linked above —
fall back to that.

---

## High-level workflow

The skill runs in eight phases. Each phase produces a section of
the final brief; don't skip phases — the Phase 3c scaffolder and
the Tier-3 credentials vault setup depend on every section.

1. **Confirm inputs** (above).
2. **Inventory existing knowledge** — pull every fact already in
   the project README, decision archaeology, admin-extracts, and
   competitor-deep-research outputs.
3. **Business identity + brand surface + contact NAP** — sections
   1, 2, 3 of the template.
4. **Service catalog + pricing + reviews + service area** —
   sections 4, 5, 6, 7.
5. **Licensing + current website + accounts ownership** —
   sections 8, 9, 10. Section 10 is the load-bearing one for the
   credentials checklist.
6. **Lead sources baseline + growth target** — sections 11, 12.
7. **Synthesis and write-up** — assemble sections 1-14 of the
   template, in order, plus the scaffolder-consumption table.
8. **Verification + reporting** — see the verification checklist
   below.

Mark each phase as a task in the operator's task list so they can
see progress.

---

## Phase 1 — Confirm inputs

Present the input list as plain text. Wait for the operator's
answers before proceeding. Underspecified inputs ruin the output.

If a comprehensive project README exists, read it end-to-end before
asking for inputs — most of what the skill needs may already be
documented and the operator only needs to confirm the slug + domain.

---

## Phase 2 — Inventory existing knowledge

For a well-instrumented client (one Oliver has been working with
for weeks), most of the brief is synthesis of material already in
the vault. Before researching anything fresh, pull:

1. **Project README** at
   `04_projects/clients/_active/<client-slug>/README.md` — the
   "Confirmed at kickoff" section, the decision archaeology, the
   current site assessment, the goals + pricing structure
   sections.

2. **Meeting notes** at
   `04_projects/clients/_active/<client-slug>/communications/meeting-notes/`
   — every kickoff and follow-up call.

3. **Admin extracts** at
   `04_projects/clients/_active/<client-slug>/admin-extracts/` —
   GBP baseline, GSC baseline, GA4 baseline, plugin baseline,
   performance audit, competitor-research synthesis.

4. **Communications** at
   `04_projects/clients/_active/<client-slug>/communications/` —
   access-request emails, prior-contractor handoffs.

5. **Business context** at
   `04_projects/clients/_active/<client-slug>/business-context/`
   — prior-marketing-outreach, lead-sources, actual-service-mix
   notes.

6. **Tier-3 pointer** — check whether
   `04_projects/clients/_active/<client-slug>/credentials.reference.md`
   exists and points to a tier-3 vault entry. Note the pointer in
   §10b; don't read the tier-3 file itself.

7. **Competitor-deep-research outputs** — if Oliver has run a
   competitor synthesis, pull the competitor list and where the
   client sits in the price-tier landscape (feeds §5b).

For a cold client (one with only a kickoff meeting and a domain),
this phase is shorter — read whatever exists and proceed to the
live-site assessment.

---

## Phase 3 — Business identity + brand surface + contact NAP

This phase populates Sections 1, 2, and 3 of the template.

### 3a. Business identity (§1)

Tools:

- **Project README + meeting notes** — usually has the legal
  name, DBA, owner name, owner title, established date, employee
  count.
- **State business-entity lookup** — confirms legal entity name,
  filing status, registered agent (Virginia: SCC; DC: DCRA; MD:
  SDAT).
- **Client website /about/ page** — confirms how the owner
  describes themselves (e.g. "Master Electrician," "Licensed
  General Contractor").
- **LinkedIn** (if the owner has a profile) — confirms title,
  background, established date.

### 3b. Brand surface (§2)

Tools:

- **Live site visual sample** — use
  `mcp__Claude_in_Chrome__navigate` + `get_page_text` if the
  site renders client-side, or `mcp__workspace__web_fetch`
  otherwise. Sample brand colors via DevTools or a competitor-
  visual-fingerprint pass.
- **WP media library or CDN inspection** — find the logo file and
  brand reference photos. Document URLs.
- **Hero gradient extraction** — if the client uses the Core 30
  page-template, sample the gradient stops from an existing live
  page.

### 3c. Contact NAP audit (§3)

Tools:

- **Live website footer + header + contact page** — capture every
  phone number, every address line, every email shown.
- **GBP listing** — capture the canonical phone, address, hours.
- **HireNimbus / Thumbtack / Pro Referral / Yelp / Angi / BBB
  profiles** — capture the phone and address each shows.
- **Invoice template** (if shared in admin extracts) — capture
  the address and phone the client puts on invoices.

Build the NAP-inconsistency table. Every drift gets a fix-or-accept
action.

Don't make NAP recommendations without seeing what GBP actually
shows — GBP is the canonical source for most consumer-facing
queries.

---

## Phase 4 — Service catalog + pricing + reviews + service area

This phase populates Sections 4, 5, 6, and 7.

### 4a. Service catalog (§4)

Tools:

- **Meeting notes "service focus" section** — usually has the
  priority order and the explicit out-of-scope list.
- **GBP services list** — what the client offers per Google. Note
  any divergence from what they say in meetings (sometimes GBP
  has outdated or rep-added services).
- **Invoices + estimates** in admin extracts — reveals the actual
  service mix from real jobs, sometimes broader than what the
  owner casually names.
- **Owner quotes from meetings** — capture how the owner
  describes each service in their own words; useful for
  scaffolder voice anchoring.

### 4b. Pricing tier (§5)

Tools:

- **Meeting notes "current business metrics" section** — usually
  has average ticket per service.
- **Invoices** in admin extracts — confirms or corrects the
  averages.
- **Competitor-deep-research outputs** — for the local
  positioning bucket (§5b).
- **Phone-call notes** — for the pricing-visibility preference
  (§5c). Capture the owner's rationale verbatim.

### 4c. Reviews surface (§6)

Tools:

- **GBP reviews extract** in admin extracts — count + rating +
  sample reviews.
- **HireNimbus / Thumbtack / Yelp profiles** — counts per source.
- **Review-mining tool output** if Oliver has run one — recurring
  praise themes, recurring complaint themes.
- **Direct webfetch of each review profile** to confirm current
  counts.

Default to GBP as the canonical AggregateRating source unless the
client has a stronger off-Google review base.

### 4d. Service area (§7)

Tools:

- **Meeting notes** — primary, secondary, avoid lists.
- **GBP service-area configuration** — what Google actually thinks
  the client serves.
- **Decision archaeology** for any service-area corrections
  (e.g. EV Electric's 2026-05-18 "service-area-corrected-to-30-
  mile-radius" entry, or the 2026-05-21 "dc-md-service-area-final-
  direction" entry).

---

## Phase 5 — Licensing + current website + accounts ownership

This phase populates Sections 8, 9, and 10. Section 10 is the
load-bearing one for the Phase 3c credentials checklist.

### 5a. Licensing (§8)

Tools:

- **State licensing lookup** — Virginia DPOR for VA contractors,
  DCRA for DC, DLLR for MD, equivalent for other states.
- **Meeting notes** for any pending license expansions.
- **Insurance certificate** (if shared) — for the carrier name
  and coverage limits.

### 5b. Current website tech (§9)

Tools:

- **Hostinger / hosting provider HTTP headers** — `curl -I` to
  the domain reveals the platform server (LiteSpeed, Nginx),
  panel (hPanel for Hostinger), and sometimes the platform header
  directly.
- **WordPress detection** — check `/wp-admin/`, `/wp-content/`,
  view-source for `wp-content/themes/<theme>/`, look for
  Elementor / Divi / Bricks footprints in the rendered HTML.
- **DNS lookup** (`dig`, `nslookup`) — reveals nameservers,
  registrar hints.
- **Plugin baseline extract** in admin extracts (if WP admin
  access exists) — full active-plugin inventory.
- **Browser console** — open the live site in Chrome devtools and
  scan for 404s, JS errors, stale references.
- **PageSpeed Insights** — LCP, CLS, TBT readings for performance
  defects.
- **Visual defect scan** — open each top-level page and note
  placeholder text, broken images, broken links, stale year in
  footer, star-count drift, missing schema (use
  schema.org Validator or Rich Results Test).

### 5c. Accounts ownership (§10)

Tools:

- **Access-verification checklist** at
  `04_projects/clients/_active/<client-slug>/admin-extracts/access-verification-checklist.md`
  if it exists.
- **Communications / emails** for access-request threads and
  ownership-transfer status.
- **GBP "People and access" panel** (Manager view) — confirms
  current owners and managers.
- **GSC "Users and permissions"** — confirms current Owners,
  Full, and Restricted users.
- **GA4 Admin → Account / Property Access** — confirms current
  Admins.
- **Domain WHOIS** — reveals registrar; ownership info usually
  redacted by privacy services.
- **Hosting panel "Account holder"** view — confirms who pays
  for hosting.

Every account where ownership is unclear or held by a third party
(prior contractor, agency, sales rep) gets a `⚠️` flag in §10a.
This is the load-bearing list — Phase 3c surfaces it to the
operator as the "before this pipeline can proceed" gate.

**Tier-3 vault pointer.** Per Oliver's standing convention (per
the `reference_tier3_vault.md` memory), sensitive credentials live
at `~/workspace/second-brain-tier3/clients/<client-slug>/credentials.md`
— NOT in this brief. Drop a pointer in §10b and never read or
write the tier-3 file from a Cowork session.

---

## Phase 6 — Lead sources baseline + growth target

This phase populates Sections 11 and 12.

### 6a. Lead sources baseline (§11)

Tools:

- **Meeting notes** — call volume per source, owner sentiment per
  source.
- **Business-context notes** at
  `04_projects/clients/_active/<client-slug>/business-context/context-lead-sources.md`
  if it exists — usually the densest source.
- **GBP performance dashboard** — direct phone-call counts from
  GBP, broken down by month.
- **Email correspondence with Thumbtack / Pro Referral** — lead
  counts and cost-per-lead.
- **HireNimbus dashboard** — inbound volume from review-driven
  customers.

If the client doesn't tag leads by source, capture the gap in
§11b and recommend a call-tracking setup as a follow-up.

### 6b. Growth target (§12)

Tools:

- **Meeting notes** — usually has the owner's explicit growth
  target ("2-3 Google-sourced customers per month").
- **Project README "Goals" section** — usually consolidates the
  growth target with the strategic frame.
- **Strategic-insight decision-archaeology entries** — e.g. EV
  Electric's 2026-05-13 "strategic-insight-thumbtack-displacement"
  entry adds context to the growth target.

Quote the owner's wording verbatim where possible. The
scaffolder uses the owner's own words to anchor the about-section
copy.

---

## Phase 7 — Synthesis and write-up

Open the locked template
(`~/workspace/second-brain/05_shared-intelligence/research-briefs/_template-client-brief.md`)
and produce a brief at
`~/workspace/second-brain/05_shared-intelligence/research-briefs/clients/<client-slug>/brief.md`
following the template exactly.

Apply these rules:

### File structure and frontmatter

```yaml
---
type: research-brief
brief-tier: client
status: draft
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
client-slug: <client-slug>
client-name: <Client Business Name>
owner-name: <Owner Full Name>
research-date: <YYYY-MM-DD>
researcher: client-fact-research-skill
tools-used: [<list of tools actually consulted>]
sources-cited: <integer>
tags: [research-brief, client-fact, <domain-slug>, <client-slug>]
---
```

Filename: `<client-slug>.md` — no `brief-` prefix. Matches the
project folder slug.

### Required sections

All 14 sections from the locked template, in order:

1. Business identity
2. Brand surface
3. Contact surface (NAP consistency)
4. Service catalog (priority order)
5. Pricing tier and positioning
6. Reviews surface
7. Service area
8. Licensing and insurance
9. Current website tech
10. Accounts ownership
11. Lead sources baseline
12. Growth target
13. Sources cited
14. Methodology

Plus the "How the scaffolder consumes this brief" table at the
bottom (lift from template — same for every brief).

Each section opens with the template's **What this feeds** line so
the Phase 3c scaffolder reader knows which JSON fields the
section serves.

### Source-attribution requirement

Every claim in the brief must trace to a source — meeting notes,
project README, decision-archaeology entry, admin extract, live-
site fetch, GBP screenshot, public licensing lookup. Inline
citation format:

```
[source: <type> <reference> on YYYY-MM-DD]
```

Examples:

- `[source: meeting-notes 2026-05-13 kickoff]`
- `[source: README decision-archaeology 2026-05-18 gbp-mystery-resolved]`
- `[source: webfetch evelectric.pro on 2026-05-27]`
- `[source: GBP profile screenshot on 2026-05-19]`
- `[source: Virginia DPOR contractor lookup on 2026-05-27]`

Section 13 (Sources cited) is the roll-up of all inline citations,
grouped by source type. The brief's `sources-cited:` frontmatter
field is the count of distinct sources in that roll-up.

### Plain-language requirement

Per [[plain-language-conventions]], write the brief in plain
language. Gloss jargon inline the first time it appears (NAP, AHJ,
DPOR, GBP, GSC, GA4, LCP, etc.). The brief is read by Oliver
(operator) and by the Phase 3c scaffolder — neither benefits from
dense whitepaper voice.

### Honest-assessment requirement

Per Oliver's standing preferences captured across multiple
memories: call out when an account's ownership is unclear, when a
site defect is severe, when a license expansion is gating revenue,
when a lead-source baseline shows the engagement starting from
zero. Don't sugarcoat. Don't pad weak data with confident-sounding
prose.

### Wikilink rules

Slug-only wikilinks for files with unique filenames:
`[[plain-language-conventions]]`. Path-based wikilinks for
ambiguous filenames like project READMEs:
`[[ev-electric-services/README]]`,
`[[s-and-h-contracting/README]]`.

Every brief must link to:

- The parent folder README (`[[clients/_README]]`)
- The locked template (`[[_template-client-brief]]`)
- The blueprint (`[[client-seo-onboarding-automation]]`)
- The project README for the client
- The plain-language conventions
- The Tier-3 vault pointer (if it exists)

### Sensitive-information rule

Do NOT include in the brief: passwords, recovery codes, API keys,
2FA seed phrases, personal home addresses (the client's BUSINESS
address is fine — that's public via GBP). All of those live in
the tier-3 vault. The brief carries pointers, not secrets.

---

## Closing step — Auto-invoke output-quality-loop

After the client-fact brief is written, the credentials checklist is shipped to the tier-3 path, and any discovery-call agenda is surfaced, emit the standard auto-invoke block per `~/workspace/skills/output-quality-loop/references/auto-invoke-convention.md` and `~/workspace/second-brain/_meta/conventions.md` § "Output quality". This is the closing step every artifact-producing skill emits before declaring the chat done. Convention shipped Phase 5 of the output-quality-loop project (2026-05-28).

**Artifact list for this skill.** The client-fact brief itself (e.g., `~/workspace/second-brain/04_projects/clients/_active/<client-slug>/<client-slug>--fact-brief.md`). The credentials checklist file is NOT included in the evaluation — it lives in the tier-3 vault which `output-quality-loop` cannot read by design.

**The block to emit (verbatim):**

````markdown
## Auto-invoke output-quality-loop

This skill produced the following artifact(s):
- `<client-fact-brief-path>`

[output-quality-loop:eval] — for each artifact, run output-quality-loop in EVALUATE mode. If PASS, declare the chat done. If NEEDS REVISION or FAIL, ingest the revision prompt as if it were operator input and regenerate the artifact, then re-invoke output-quality-loop. Cap at 3 iterations; on the 3rd FAIL, escalate to the operator with the evaluation report.
````

Required-element discipline per the convention spec: heading text matches verbatim (`## Auto-invoke output-quality-loop`); one bullet per artifact with full path in backticks; directive opens with `[output-quality-loop:eval]` and includes the iteration-cap discipline language.

**Iterate or declare done.** All PASS → declare done. Any NEEDS REVISION (minor / substantive) → Mode 2 auto-fires a revision prompt; ingest as operator input, apply fixes to the brief (fill a gap, fix a frontmatter field, mark a snapshot-mined claim as confirmed vs unconfirmed, tighten the discovery-call agenda), re-emit the block, loop. Any FAIL → revision prompt includes root-cause analysis; address the root cause (often: secrets leaked into Tier 1/2 by mistake, decision-archaeology section missing, no provenance trail on claims), regenerate, re-emit, loop.

**Iteration cap (3 max).** Track count via the folder-quality-log's per-artifact section before each regeneration. If three iteration entries exist and the verdict is still not PASS, **escalate** to the operator with the evaluation report and stop. Don't run a fourth iteration — that's the load-bearing cost-control discipline.

**Operator bypass.** Include `--bypass-quality-loop` (or "skip the quality loop") in the original brief request to skip the block for that invocation. The bypass records to the closest folder's `_quality-log.md` under `### Bypassed (manual override)`.

---

## Vault stewardship

Per the [[vault-stewardship-principles]]:

1. **Check folder structure before writing.** The brief lives at
   `second-brain/05_shared-intelligence/research-briefs/clients/<client-slug>/brief.md`.
   The folder exists; the `_README.md` exists. Don't write the
   brief anywhere else.

2. **Update the folder `_README.md` if needed.** When the brief
   adds the first or second client to the folder, propose an edit
   to `clients/_README.md` to list it. Non-destructive — never
   overwrite existing content.

3. **Cross-reference related notes.** The brief's "Related"
   section must wikilink to the project README, the parent folder,
   the template, the blueprint, and sibling client briefs (other
   clients in the same domain — e.g. EV Electric and S&H are
   both residential electrical).

4. **Non-destructive on existing project content.** The brief
   READS from the project README, decision archaeology, and
   admin extracts. It does NOT modify them. If the brief surfaces
   a discrepancy with the README (e.g. a phone number changed),
   flag it in §3b but do not edit the README from this skill
   invocation. Updating the README is a separate operator action.

---

## Verification — before declaring done

1. **Frontmatter check** — frontmatter is valid YAML, has all
   required fields (`type`, `brief-tier`, `status`, `created`,
   `updated`, `client-slug`, `client-name`, `owner-name`,
   `research-date`, `researcher`, `tools-used`, `sources-cited`,
   `tags`).

2. **Section completeness** — all 14 template sections present,
   each opens with its "What this feeds" line.

3. **Source-attribution check** — every claim has an inline
   citation. Run a grep for sentences with numbers (phone digits,
   review counts, ratings, dollar amounts) and confirm each has a
   `[source: …]` tag.

4. **Wikilink check** — extract wikilinks via grep and confirm
   peer links resolve.

5. **Plain-language scan** — scan for unglossed jargon. NAP, AHJ,
   DPOR, GBP, GSC, GA4, LCP should be defined inline on first
   use.

6. **JSON-shape compatibility check** — walk the "How the
   scaffolder consumes this brief" table at the bottom and
   confirm the brief surfaces data for every JSON field in
   `data/client-ev-electric-services.json` (the reference shape).
   Any gap is a brief defect.

7. **Credentials-flag check** — open §10a and confirm every
   account whose ownership is unclear, contested, or held by a
   third party has an explicit `⚠️` or `❓` flag. This is the
   load-bearing output of the brief — if §10a is empty for a
   client with a known prior contractor, the brief is incomplete.

8. **Sensitive-information scan** — grep for password-shaped
   strings, recovery codes, API keys. None should appear in the
   brief. If anything sensitive accidentally landed, redact and
   add to the tier-3 vault pointer instead.

9. **Plain-language pass on a sample paragraph.** Pick the
   densest paragraph in the brief and confirm it reads as plain
   language. If not, run the [[plain-language-translation]]
   skill on the brief retroactively.

---

## Reporting back to the operator

End with a terse summary (per `feedback_terse_completion_reports.md`):

- Brief written to `<path>`
- Sections with `⚠️` flags (credentials gaps, NAP drift, license
  pending)
- Top 3 surprises from the research (e.g. "client's GBP and
  invoice template show different addresses," "owner has a
  pending license that gates 30% of his potential service area")
- Blocked questions if any (e.g. "domain WHOIS returned redacted
  data; ownership of the registrar account is still unknown")

Use bullets, not paragraphs. Don't restate the brief content —
Oliver can read the file.

---

## Working principles

These are the rules of the road. They shaped the first invocations
(EV Electric and S&H Contracting on 2026-05-27) and should shape
every future use.

1. **Per-client by design.** A client-fact brief lives until the
   client churns or pivots their business. It does NOT get
   reused across clients. Don't bake cross-client facts into a
   client brief; those go in Tier 1, 2, or 3.

2. **Synthesis-heavy, research-light for instrumented clients.**
   For a client Oliver has been working with for weeks, the brief
   is mostly synthesis of existing material (README, decision
   archaeology, admin extracts). Don't re-research what's already
   documented; cite it forward.

3. **Cold-research-heavy for new clients.** For a client where
   only a kickoff meeting + a domain exists, the brief is mostly
   primary research (live-site assessment, public licensing
   lookups, directory profile audits). Budget accordingly.

4. **Honest about gaps.** Section 14 (Methodology) names every
   research dimension that couldn't be completed, with the
   reason. The brief's credibility comes from admitting its gaps,
   not pretending they don't exist.

5. **Section 10 is load-bearing.** Accounts ownership is the
   section Phase 3c keys the credentials checklist off of. Every
   account whose ownership is unclear, contested, or held by a
   third party gets an explicit flag. If §10a is empty for a
   client with a known prior contractor, the brief is incomplete.

6. **Locked template.** Don't restructure the template per
   invocation. The Phase 3c scaffolder reads briefs sequentially
   — if the section order or naming drifts, the scaffolder breaks.
   If the template needs an update, propose it as a separate
   change, then update every existing brief in lockstep.

7. **Plain language.** The brief is read by humans and by the
   scaffolder. Both benefit from conversational prose. No jargon
   walls.

8. **Sensitive-information discipline.** Credentials live in
   tier-3 only. The brief carries pointers, not secrets.

9. **Non-destructive on existing project content.** Read the
   README; don't edit it from this skill. If the brief surfaces a
   discrepancy, flag it in §3b or §14 — do not silently update
   the source.

---

## Reference files

When you need them, read these:

- `~/workspace/second-brain/05_shared-intelligence/research-briefs/_template-client-brief.md`
  — the locked template
- `~/workspace/second-brain/05_shared-intelligence/research-briefs/_README.md`
  — folder index explaining the three-tier research model
- `~/workspace/second-brain/05_shared-intelligence/research-briefs/clients/_README.md`
  — clients folder README
- `~/workspace/second-brain/05_shared-intelligence/research-briefs/clients/ev-electric-services/brief.md`
  — worked example, instrumented client
- `~/workspace/second-brain/05_shared-intelligence/research-briefs/clients/s-and-h-contracting/brief.md`
  — worked example, cold-research client
- `~/workspace/repos/ai-agency-core/scripts/data/client-ev-electric-services.json`
  — the JSON shape the brief feeds
- `~/workspace/skills/service-seo-research/SKILL.md` — Tier 1
  sibling skill
- `~/workspace/skills/city-base-research/SKILL.md` — Tier 2
  sibling skill
- `~/workspace/skills/competitor-deep-research/SKILL.md` — per-
  client competitive-research skill

---

## Maintenance notes

### M1: Template path dependency (added 2026-05-27, v1.0)

**The issue:** This skill references the canonical template at
`second-brain/05_shared-intelligence/research-briefs/_template-client-brief.md`
by literal path in multiple places. If that file is moved or
renamed, this skill will fail on Pre-flight.

**How to fix:** Search the vault by filename (Glob
`_template-client-brief.md`). Update the paths in this SKILL.md
once the new location is confirmed.

**Why it wasn't designed away:** Single canonical instance is the
simplest design. If the template moves more than once, refactor
to dynamic discovery.

### M2: Decision-archaeology mining is high-leverage but easy to skip (added 2026-05-27, v1.0)

**The issue:** For a well-instrumented client, the README's
decision-archaeology section often has more useful brief content
than any other source. It's easy to skim past because it's
chronological prose rather than structured data.

**How it surfaces:** A brief misses key facts (a pricing change, a
service-area correction, a credentials transfer) that are
documented in the README.

**How to fix:** Always read the full decision archaeology before
writing §3-§12. Treat each entry as a candidate source citation.

**Why it wasn't designed away:** The decision archaeology is the
single best summary of client knowledge that doesn't follow a
template. Reading it can't be skipped.

### M4: Always mine archived snapshots, don't rely on existing audits (added 2026-05-27, v1.0)

**The issue:** When a client folder has an archived HTML
snapshot (`website-archive/old/snapshot-*-source.html`), the
existing audit notes are summarizations of what the auditor
considered worth capturing — not the full data the snapshot
holds. Skipping a fresh mining pass against the snapshot itself
leaves gaps that the source data could fill.

**How it surfaces:** Brief §2 (brand colors, logo URL),
§6 (review themes), and §4 (service mix from review-content)
have "TBD" placeholders even though the data exists in the
snapshot.

**How to fix:** When `website-archive/old/snapshot-*-source.html`
exists, mine it with regex + Python in addition to reading
the audit notes. Specifically:

- `grep -oiE '#[0-9a-f]{6}' SNAPSHOT | sort | uniq -c | sort -rn`
  — frequency-counted brand color extraction
- `python3 ... re.findall(r'<!-- R-CONTENT -->(.*?)<!-- R-CONTENT -->', html)`
  — TrustIndex / review-widget review-text extraction
- JSON-LD chunk extraction via
  `re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', html, re.DOTALL)`
- Logo / favicon: grep for `link rel="(icon|shortcut|apple)"`
- Email addresses: grep with the standard email regex; surfaces
  contact emails AND third-party contractor emails (Haris
  Mughal was recovered this way for S&H)

**Why it wasn't designed away:** Phase 2 of the workflow says
"inventory existing knowledge" which I initially interpreted
as "read the audit notes." The snapshot itself is part of the
existing knowledge — it just requires structured mining rather
than reading. Phase 2 step should be: "Read the audit notes
AND run a fresh mining pass against any archived snapshots."

### M3: Credentials section drifts as accounts change hands (added 2026-05-27, v1.0)

**The issue:** §10 captures ownership at a point in time. Account
ownership can change weekly during onboarding (manager added,
prior contractor transfers, GBP ownership transferred). The
brief gets stale fast.

**How it surfaces:** The credentials checklist Phase 3c produces
points at an account that's since changed owner.

**How to fix:** Refresh trigger in the brief's Methodology
section. Default: refresh §10 when any account changes owner.
The refresh is cheap (§10 is the only section affected most of
the time).

**Why it wasn't designed away:** Ownership is intrinsically
mutable. The fix is fast refreshes, not a static brief.

---

## How to add a new maintenance note

When the skill errors or produces a calibration miss in
production, add a new entry following the pattern:
**Issue → How it surfaces → How to fix → Why it wasn't designed
away.** Date-stamp the entry. This is how future-Claude learns
from past failures without re-hitting the same wall.

---

## See also (inside the vault)

- `[[client-seo-onboarding-automation]]` — the roadmap this skill
  serves (Phase 2d)
- `[[_template-client-brief]]` — the locked template
- `[[_README]]` — research-briefs folder index
- `[[clients/_README]]` — client-fact folder index
- `[[service-seo-research]]` — Tier 1 sibling skill
- `[[city-base-research]]` — Tier 2 sibling skill
- `[[competitor-deep-research]]` — per-client competitive research
- `[[plain-language-conventions]]` — voice rules
- `[[conventions]]` — KOS naming and frontmatter rules
- `[[plain-language-translation]]` — for retroactive translation
  passes
