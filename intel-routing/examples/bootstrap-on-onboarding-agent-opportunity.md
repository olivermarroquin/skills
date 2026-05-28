# Worked example: BOOTSTRAP on the onboarding-agent opportunity

Test run 2026-05-28. Tests BOOTSTRAP against an opportunity that doesn't clearly fit any existing project — the promote-to-project happy path. Validates the full flow from Gate 1 scaffold proposal through chained PULL pre-population to source-artifact update, including the `(future)` archetype promotion friction surface.

## Test framing

The source artifact is `00_inbox/decisions-pending/opportunity-onboarding-agent-productized-service.md` — a high-confidence (tier 1) opportunity to productize an onboarding agent for coaches and consultants. Hypothesis: "Coaches and consultants with 50+ leads/month will pay $2k setup + $500/mo for an onboarding agent that lifts booked-call conversion by 15%+."

Pre-existing context: Oliver's `repos/idea-factory/.kos/` already lives in the vault as `04_projects/personal/idea-factory/`. The opportunity body says "worst case = blueprint for AI Factory" but does NOT name idea-factory directly. The opportunity has a clear productized-service shape distinct from idea-factory's mission. This makes it a partial-overlap case at best — promote-to-project is the right recommendation.

## Inputs

**Source artifact:** `~/workspace/second-brain/00_inbox/decisions-pending/opportunity-onboarding-agent-productized-service.md`
**Operator-proposed slug:** none provided (executor derives)
**Today (as-if):** 2026-05-28

### Source frontmatter (read at Step 2)

- `type: opportunity`
- `status: surfaced`
- `opportunity-type: client-service`
- `confidence: high` (artifact's own confidence, not applicability-confidence)
- `tier: 1`
- `sources: ["[[source-example-onboarding-agent]]"]`
- `applies-to-projects:` — not set
- `applies-to-archetypes:` — not set (pre-Phase-2-migration shape)
- `routed-at:` — not set

### Source body summary (executor read)

Opportunity to productize an "onboarding agent" — Claude API + Make.com + Airtable + Stripe stack — sold as $2k setup + $500/mo to coaches and consultants with measurable intake-leakage pain. Build cost trivial, validation steps already drafted (pick niche → demo → 5 cold demos). High-confidence opportunity but no existing project owns it; idea-factory is mentioned only as the worst-case fallback.

### Existing project READMEs enumerated

11 projects total:

| Project | Area | Archetypes |
|---|---|---|
| ev-electric-services | clients/_active | [services-business, home-services-trade, electrical-contractor, wordpress-site, post-launch-seo, gbp-dependent] |
| s-and-h-contracting | clients/_active | [services-business, home-services-trade, electrical-contractor, wordpress-site, pre-launch-seo, gbp-dependent] |
| ai-agency-core | personal | [infrastructure-tooling, personal-system] |
| app-factory | personal | [infrastructure-tooling, personal-system] |
| dad-businesses | personal | [services-business, professional-services] |
| hire-relay | personal | [saas-product, b2b-saas] |
| idea-factory | personal | [infrastructure-tooling, personal-system] |
| keelworks | personal | [services-business, professional-services] |
| legal-toolkit | personal | [infrastructure-tooling, personal-system] |
| resume-factory | personal | [saas-product, b2c-saas] |
| resume-saas | personal | [saas-product, b2c-saas] |

(Note: archetypes shown are illustrative — actual archetypes per Phase 2 README updates may vary slightly.)

### Vault reconnaissance for pre-population

Executor infers source archetype set from body: `[services-business, professional-services, productized-service, ai-tooling]`. `productized-service` does not exist in conventions yet.

Querying vault for artifacts with any archetype overlap against `[services-business, professional-services, ai-tooling]` (live archetypes only — `productized-service` would be promoted at Gate 1):

- ~47 artifacts match (mostly from automation-systems and marketing clusters tagged `services-business`)
- ~24 are slug-named to keelworks (would surface as archetype-overlap-only on the new project)
- ~12 are speculative routings with confidence `low` or absent

Pre-population estimate: PULL would surface ~47 items at first triage; mostly archetype-overlap-only with a heavy keep/defer ratio expected.

## Stage A — Apply-to-existing detection (Step 3a)

Computing overlap against each project:

- **keelworks (services-business + professional-services):** 2 archetype overlap (services-business, professional-services). Body alignment partial — keelworks is the operator's agency umbrella but onboarding-agent productization is positioned as a distinct offering. **Partial overlap.**
- **dad-businesses (services-business + professional-services):** 2 archetype overlap. Body alignment weak — dad-businesses is two specific small-businesses (auto-repair + auto-sales), not a productization platform. **Partial overlap.**
- **idea-factory (infrastructure-tooling + personal-system):** 0 archetype overlap (productized-service ≠ infrastructure-tooling). Body alignment weak — opportunity mentions idea-factory only as worst-case-blueprint. **No overlap.**
- **All other projects:** 0 archetype overlap; **No overlap.**

**Strong overlap:** none.
**Partial overlap:** keelworks, dad-businesses.
**No overlap:** ai-agency-core, app-factory, hire-relay, idea-factory, legal-toolkit, resume-factory, resume-saas, ev-electric-services, s-and-h-contracting.

**Recommendation:** PROMOTE-TO-PROJECT. No project has strong overlap; partial-overlap projects (keelworks, dad-businesses) have wrong scope for absorbing a distinct productized-service offering.

## Stage A — Scaffold parameters proposal (Step 3b)

**Slug:** `onboarding-agent-productized-service` (derived from source filename, `opportunity-` prefix stripped).

**Slug uniqueness:** unique (no existing project under any `04_projects/<area>/`).

**Area:** `personal/`. Inference: opportunity describes a productized service Oliver builds and sells, not a client engagement. Operator-internal initiative shape.

**Archetypes:** `[services-business, professional-services, productized-service, ai-tooling]`. Hierarchy: `services-business → professional-services`; situational/orthogonal: `productized-service`, `ai-tooling`. Compound-tagged per discipline.

**Conventions check:** `services-business`, `professional-services`, `ai-tooling` are all live. `productized-service` is NOT in conventions hierarchy currently. **Friction observation:** propose adding `productized-service` to conventions as a new orthogonal/situational archetype (services-business-shaped projects that are productized offerings rather than 1:1 client engagements).

**Confidence:** `medium` (default; opportunity's own confidence is `high` but applicability-confidence on the new project README defaults to medium-on-archetype-derivation).

**Founding-artifact:** `[[opportunity-onboarding-agent-productized-service]]`.

**Repo scaffold:** `yes-repo`. Default per `services-business + professional-services + ai-tooling` archetype set — uniform vault shape; productized-service offerings need execution-logs + lessons even before code surface appears.

**Purpose statement (drafted):** "Productize an AI-driven onboarding agent (Claude API + Make.com + Airtable + Stripe stack) as a $2k-setup + $500/mo offering for coaches and consultants with measurable intake-leakage pain. Bootstrapped from intel surfacing a high-confidence productization opportunity with documented pain, low build cost, and existing prospect overlap."

## Gate 1 surface

```
BOOTSTRAP SCAFFOLD PROPOSAL — opportunity-onboarding-agent-productized-service

Source artifact: ~/workspace/second-brain/00_inbox/decisions-pending/opportunity-onboarding-agent-productized-service.md
Type: opportunity
Tier: 1
Body summary (1-2 sentences):
  Productize an "onboarding agent" — Claude API + Make.com + Airtable + Stripe stack — sold
  as $2k setup + $500/mo to coaches and consultants with measurable intake-leakage pain.
  High-confidence opportunity; idea-factory mentioned only as worst-case fallback.

Existing source frontmatter:
  applies-to-projects: not set
  applies-to-archetypes: not set
  applicability-confidence: not set
  routed-at: not set

Apply-to-existing detection:
  Strong overlap with: none
  Partial overlap with: keelworks, dad-businesses
    keelworks: 2 archetype overlap (services-business + professional-services); body alignment
      partial — keelworks is operator's agency umbrella; productized-service shape distinct
    dad-businesses: 2 archetype overlap (services-business + professional-services); body
      alignment weak — dad-businesses is two specific SMBs, not a productization platform
  No overlap with: 9 other projects (ai-agency-core, app-factory, hire-relay, idea-factory,
    legal-toolkit, resume-factory, resume-saas, ev-electric-services, s-and-h-contracting)

Recommendation: PROMOTE-TO-PROJECT
Reason: No existing project has strong overlap. Partial-overlap projects (keelworks,
  dad-businesses) have scope mismatch for absorbing a distinct productized-service
  offering. Body content is project-shaped (productize + sell + scale), not
  apply-to-existing-shaped (build for existing client).

==== PROMOTE-TO-PROJECT proposal ====

Slug:       onboarding-agent-productized-service
  Uniqueness: unique (no collision)
Area:       personal/
  Inference: opportunity describes operator-internal productization, not client engagement
Archetypes: [services-business, professional-services, productized-service, ai-tooling]
  Conventions check: services-business + professional-services + ai-tooling are live;
    productized-service is NOT in conventions hierarchy
Confidence: medium
Founding-artifact: [[opportunity-onboarding-agent-productized-service]]
Repo scaffold: yes-repo
  Default reason: services-business + professional-services archetypes default to yes-repo
    for uniform vault shape (execution-logs + lessons capture)

Purpose (proposed):
  Productize an AI-driven onboarding agent (Claude API + Make.com + Airtable + Stripe stack)
  as a $2k-setup + $500/mo offering for coaches and consultants with measurable
  intake-leakage pain. Bootstrapped from intel surfacing a high-confidence productization
  opportunity with documented pain, low build cost, and existing prospect overlap.

Friction observations:
  - Archetype `productized-service` is NOT in conventions.md hierarchy. Options:
    (1) Promote inline — add `productized-service` as a new orthogonal/situational archetype
        (services-business-shaped projects that are productized offerings rather than 1:1
         client engagements). Single-line conventions.md edit.
    (2) Use closest live archetype — drop `productized-service`; use only
        [services-business, professional-services, ai-tooling]. Loses the productization
        signal but uses only live archetypes.
    (3) Hold — don't promote, but archetype is unsatisfying without it.
    Recommendation: option 1 — productized-service is a genuinely orthogonal shape
    (Oliver's own framing in the opportunity body distinguishes "productize" from
    "agency client work"). Inline promotion is cheap.
  - yes-repo requires a repo at ~/workspace/repos/onboarding-agent-productized-service/.
    Repo does NOT yet exist. BOOTSTRAP will surface the app-factory paste-prompt at Step B1.

Pre-population estimate:
  PULL on the new project would surface ~47 artifacts at first triage.
  Slug-named to other projects (archetype-overlap-only for the new project): ~24
    (mostly keelworks-routed services-business artifacts)
  Speculative routings (low confidence by default): ~12
  Operator should expect Gate 1 on PULL with 47 items, heavy keep + defer ratio
    (new project with no slug-named-direct artifacts yet — all matches are
     archetype-overlap from other projects' libraries).

==== APPLY-TO-EXISTING alternative ====

If you'd rather route this source to an existing project, the strongest match is:
  Target project: keelworks
  Overlap rationale: 2 archetype overlap + partial body alignment (productization is
    plausibly Keelworks-internal R&D; some Keelworks-internal productization is already
    happening via Core 30 + AIOSEO plugin work)
  Suggested invocation:
    "PUSH-route 00_inbox/decisions-pending/opportunity-onboarding-agent-productized-service.md to keelworks"
  (exit BOOTSTRAP; source artifact stays in 00_inbox/decisions-pending/; PUSH routes
   bridge note to keelworks/ instead)

Confirm promote / confirm apply-to-existing for keelworks / modify <field> /
promote conventions edit for productized-service / promote anyway / reject?
```

**Operator response:** *Confirm promote AND promote conventions edit for productized-service*.

## Stage B — Scaffolding writes

### Step 5a (B1) — Repo scaffold

`~/workspace/repos/onboarding-agent-productized-service/` does NOT exist. Surface the app-factory paste-prompt:

```
The new project needs a repo at ~/workspace/repos/onboarding-agent-productized-service/.

App-factory init-project is the right way to create it. To set up:

1. Open a fresh terminal:
     mkdir -p ~/workspace/repos/onboarding-agent-productized-service
     cd ~/workspace/repos/onboarding-agent-productized-service

2. Open Claude Code in this directory.

3. Paste the following prompt:

---
You are my senior developer helping me bootstrap a new app.

**App name:** onboarding-agent-productized-service
**Description:** Productize an AI-driven onboarding agent (Claude API + Make.com + Airtable
  + Stripe stack) as a $2k-setup + $500/mo offering for coaches and consultants with
  measurable intake-leakage pain.
**Stack:** Node.js + TypeScript backend (Claude API integration) + Airtable as data layer
  + Make.com as workflow orchestrator + Stripe for billing. No frontend at MVP — operator
  + agent runs configuration; clients access via custom onboarding URL produced per engagement.
**Date started:** 2026-05-28
**Stage:** MVP

(Stack-recommendation note: edit before pasting if your preference differs. The proposed
 stack matches the opportunity body's "Tools required" line — Claude API + Airtable + Make.com
 + Stripe — and skips a frontend at MVP since the agent's interface is the onboarding flow
 itself.)

[remainder of standard init-project.md prompt]
---

When the repo is created and Claude Code has scaffolded the docs/ + initial config, type
"repo created" to continue BOOTSTRAP. To skip, type "skip repo init".
```

**Operator response:** *repo created* (assumes operator ran the app-factory init in a separate Claude Code session, repo now exists at `~/workspace/repos/onboarding-agent-productized-service/` with `docs/` + initial config).

### Step 5b (B2) — KOS-setup invocation

```bash
bash ~/workspace/skills/knowledge-os-setup/scripts/init-project-vault.sh \
  ~/workspace/repos/onboarding-agent-productized-service \
  personal \
  ~/workspace/second-brain \
  ~/workspace/skills/knowledge-os-setup/assets
```

Script output:
```
→ Initializing project vault for: onboarding-agent-productized-service
[1/4] Creating .kos/ structure...
  + README.md (from template, placeholders substituted)
  + .vault-config.md (from template, placeholders substituted)
[2/4] Fork-from...
  · no fork-from specified, skipping
[3/4] Creating symlink in second-brain...
  + symlink: ~/workspace/second-brain/04_projects/personal/onboarding-agent-productized-service → ../../../repos/onboarding-agent-productized-service/.kos
[4/4] Done.

✅ Project vault initialized for: onboarding-agent-productized-service
```

### Step 5c (B3) — README customization

Edit `~/workspace/repos/onboarding-agent-productized-service/.kos/README.md` (visible in vault as `04_projects/personal/onboarding-agent-productized-service/README.md` via symlink).

Frontmatter overwrite:
```yaml
---
type: project-readme
project-name: onboarding-agent-productized-service
status: active
created: 2026-05-28
updated: 2026-05-28
client: false
sensitivity: standard
archetypes: [services-business, professional-services, productized-service, ai-tooling]
applicability-confidence: medium
founding-artifact: "[[opportunity-onboarding-agent-productized-service]]"
tags: [project, vault-root, onboarding-agent-productized-service]
---
```

Body Purpose section:
```markdown
## Purpose

Productize an AI-driven onboarding agent (Claude API + Make.com + Airtable + Stripe stack)
as a $2k-setup + $500/mo offering for coaches and consultants with measurable intake-leakage
pain. Bootstrapped from intel surfacing a high-confidence productization opportunity with
documented pain, low build cost, and existing prospect overlap.
```

Promotion log:
```markdown
## Promotion log
- 2026-05-28 — project bootstrapped from [[opportunity-onboarding-agent-productized-service]] via intel-routing BOOTSTRAP
```

### Step 5d (B4) — Inbox file instantiation

Create `~/workspace/second-brain/04_projects/personal/onboarding-agent-productized-service/_intel-inbox.md` (via symlink, lands in `~/workspace/repos/onboarding-agent-productized-service/.kos/_intel-inbox.md`).

Substitutions applied:
- `<% tp.date.now("YYYY-MM-DD") %>` → `2026-05-28` (frontmatter)
- `<project-slug>` → `onboarding-agent-productized-service` (frontmatter + tags)
- `<Project name>` → `onboarding-agent-productized-service` (H1)
- `archetypes: []` → `archetypes: [services-business, professional-services, productized-service, ai-tooling]`

### Step 5e (B5) — Conventions.md edit

Operator confirmed inline promotion of `productized-service`. Edit `~/workspace/second-brain/_meta/conventions.md`:

Add `productized-service` to the Situational archetypes block (currently listing `wordpress-site`, `pre-launch-seo`, `post-launch-seo`, `gbp-dependent`):

```markdown
**Situational archetypes** (orthogonal to the hierarchy, used in combination with hierarchy archetypes):

- `wordpress-site` — applies to anything assuming WP plugin or admin access
- `pre-launch-seo` — site has no GBP verification or GSC baseline yet
- `post-launch-seo` — baselines exist, ranking work is active
- `gbp-dependent` — Google Business Profile is a major channel
- `productized-service` — services-business or professional-services offering that's been productized into a sold-as-a-package shape, distinct from 1:1 client-engagement work
```

## Step 6 — Verify writes

Read each touched file:
- `04_projects/personal/onboarding-agent-productized-service/README.md` — frontmatter + Purpose + Promotion log all landed ✓
- `04_projects/personal/onboarding-agent-productized-service/_intel-inbox.md` — substitutions all applied ✓
- `~/workspace/repos/onboarding-agent-productized-service/.kos/README.md` — same content via symlink target ✓
- `~/workspace/repos/onboarding-agent-productized-service/.kos/.vault-config.md` — exists from KOS-setup ✓
- `_meta/conventions.md` — productized-service line added ✓
- Symlink exists and resolves: `ls -la 04_projects/personal/onboarding-agent-productized-service` shows arrow → `../../../repos/onboarding-agent-productized-service/.kos` ✓

## Stage C — Chained PULL pre-population

Invoke PULL on `onboarding-agent-productized-service`. PULL runs its standard workflow:

### PULL Step 1-2: preconditions + inputs

All preconditions pass. README + inbox just instantiated; archetypes match by construction. Query runs against `03_domains/` + `05_shared-intelligence/` + `00_inbox/decisions-pending/` with the new archetype set.

### PULL Step 3a: sync validation

README archetypes: `[ai-tooling, productized-service, professional-services, services-business]` (alphabetized)
Inbox archetypes: same (matched by construction)
**Match: matched ✓**

### PULL Step 3b-3c: tagging + pre-classification

Query returns 47 artifacts (matches pre-population estimate).

- Slug-named to `onboarding-agent-productized-service`: 0 (project is new; no artifact has been routed to it yet)
- Archetype-overlap-only: 47

Pre-classification:
- **APPLY (0):** No slug-named items → no rule 4/5/6/7 matches. All 47 items are archetype-overlap-only → falls to rule 8 (defer) or rule 10 (low-confidence bias).
- **KEEP (0):** Same — no slug-named items.
- **DEFER (44):** 47 minus 3 = 44 items hit rule 8 (archetype-overlap-only + project active) → defer pending review. Examples: tools from automation-systems cluster tagged `[ai-tooling]`; tactics from marketing cluster tagged `[services-business, professional-services]`.
- **NOT APPLICABLE (0):** No situational conflicts (project has no situational archetype declared; `productized-service` is orthogonal, not gating).
- **ALREADY BRIDGED (0):** First triage; no prior bridges.
- **3 items** get bumped by rule 10 (existing confidence `low`) — also defer.

Total: 44 + 3 = 47 → all in defer.

### PULL Gate 1 surface

```
PULL TRIAGE — onboarding-agent-productized-service

Project name: onboarding-agent-productized-service
Project README: 04_projects/personal/onboarding-agent-productized-service/README.md
Inbox file: 04_projects/personal/onboarding-agent-productized-service/_intel-inbox.md
Lookback window: 14 days (suppressing items with routed-at after 2026-05-14)
Last operator triage: first triage

Sync status:
  README archetypes: [ai-tooling, productized-service, professional-services, services-business]
  Inbox archetypes: [ai-tooling, productized-service, professional-services, services-business]
  Match: matched ✓

Items surfaced: 47
  slug-named: 0
  archetype-overlap-only: 47
Items suppressed (routed within lookback): 0
Items already bridged (informational): 0

==== APPLY (proposed: 0) ====
  (none — first triage on a brand-new project with no slug-named direct routings yet)

==== KEEP (proposed: 0) ====
  (none — keep is reserved for slug-named items in engagement context)

==== DEFER (proposed: 47) ====
  - [[tool-make-com]] (tool, confidence: high)
    Workflow orchestrator named in source body as core stack component.
    Reason: archetype match (ai-tooling); body content doesn't naming the new project explicitly
  - [[tool-airtable]] (tool, confidence: high)
    Data layer named in source body as core stack component.
    Reason: archetype match (ai-tooling); body content doesn't name new project explicitly
  - [[tool-claude-code]] (tool, confidence: high)
    Claude Code CLI; foundational tool.
    Reason: archetype match (ai-tooling); body content doesn't name new project explicitly
  - [[tactic-foundationals-first-for-new-sites-link-building]] (tactic, confidence: high)
    Foundational link-building tactic; archetype overlap services-business + professional-services.
    Reason: archetype match, no body-content explicit naming; defer pending review
  - ... (43 more — abbreviated)

==== NOT APPLICABLE (proposed: 0) ====
  (none)

==== ALREADY BRIDGED (informational: 0) ====
  (first triage)

Confirm bins as proposed / move <item> to <bin> / move all <bin> to <bin> /
sharpen archetypes on <item> / lower confidence on <item> to <level> /
refresh bridge on <item> / reject?
```

**Operator response:** *Move `tool-make-com`, `tool-airtable`, `tool-claude-code` to apply* (the three tools explicitly named in the source body's "Tools required" line — apply makes sense; bridges should formalize that these tools are this project's stack). *Confirm bins as proposed otherwise.*

Updated bins:
- APPLY: 3 (the three tools)
- DEFER: 44

### PULL Gate 2 surface (after operator move)

```
BRIDGE-NOTE PROPOSALS — onboarding-agent-productized-service

3 bridges proposed (one per applied artifact):

  1. onboarding-agent-productized-service/bridge-tool-make-com-to-onboarding-agent-productized-service.md
     Action items: 2
     Punchlist: "Adopt Make.com as workflow orchestrator for onboarding-agent productization"

  2. onboarding-agent-productized-service/bridge-tool-airtable-to-onboarding-agent-productized-service.md
     Action items: 2
     Punchlist: "Adopt Airtable as data layer for onboarding-agent productization"

  3. onboarding-agent-productized-service/bridge-tool-claude-code-to-onboarding-agent-productized-service.md
     Action items: 1
     Punchlist: "Adopt Claude Code as build substrate for onboarding-agent productization"

Per-bridge content (expanded):
  --- Bridge 1: tool-make-com ---
  [full bridge body following template]
  --- Bridge 2: tool-airtable ---
  [full bridge body]
  --- Bridge 3: tool-claude-code ---
  [full bridge body]

Confirm all / modify per bridge / skip per bridge / reject all?
```

**Operator response:** *Confirm all*.

### PULL Stage C writes

- 3 bridge files written to `04_projects/personal/onboarding-agent-productized-service/`
- `_punchlist.md` created with 3 entries
- 3 artifacts get `routed-at: 2026-05-28`: `tool-make-com.md`, `tool-airtable.md`, `tool-claude-code.md`
- Inbox `_intel-inbox.md` Last triage section updated:
  ```
  **Date:** 2026-05-28
  **Items surfaced:** 47 (0 slug-named, 47 archetype-overlap-only)
  **Items applied:** 3 → bridge notes filed in this folder; punchlist entries appended
    - [[tool-make-com]]
    - [[tool-airtable]]
    - [[tool-claude-code]]
  **Items kept:** 0
  **Items deferred:** 44
  **Items marked not-applicable:** 0
  ```

### PULL completion report

3 applied + 44 deferred + 0 kept + 0 not-applicable. Captured for BOOTSTRAP completion report.

## Stage D — Source artifact update + completion report

### Step 8a — Source frontmatter writes

Edit `00_inbox/decisions-pending/opportunity-onboarding-agent-productized-service.md`:

```yaml
---
type: opportunity
status: surfaced
created: 2026-04-28
opportunity-type: client-service
estimated-effort: "1-2 weeks"
estimated-value: "$2k setup + $500/mo per client"
confidence: high
sources: ["[[source-example-onboarding-agent]]"]
applies-to-projects: [onboarding-agent-productized-service]
routed-at: 2026-05-28
promoted-to-project: 2026-05-28
tier: 1
tags: [opportunity]
---
```

### Step 8b — Completion report

```
BOOTSTRAP COMPLETE — onboarding-agent-productized-service

Source: 00_inbox/decisions-pending/opportunity-onboarding-agent-productized-service.md
  Frontmatter updated:
    applies-to-projects: [onboarding-agent-productized-service]
    routed-at: 2026-05-28
    promoted-to-project: 2026-05-28

Project scaffolded: personal/onboarding-agent-productized-service
  Path: 04_projects/personal/onboarding-agent-productized-service/
  Repo: ~/workspace/repos/onboarding-agent-productized-service/
  Symlink: 04_projects/personal/onboarding-agent-productized-service → ../../../repos/onboarding-agent-productized-service/.kos

README written: 04_projects/personal/onboarding-agent-productized-service/README.md
  Archetypes: [services-business, professional-services, productized-service, ai-tooling]
  Applicability-confidence: medium
  Founding-artifact: [[opportunity-onboarding-agent-productized-service]]
  Purpose: Productize an AI-driven onboarding agent ($2k setup + $500/mo for coaches/consultants)

Inbox instantiated: 04_projects/personal/onboarding-agent-productized-service/_intel-inbox.md

Pre-population (chained PULL outcome):
  Applied: 3 (tool-make-com, tool-airtable, tool-claude-code)
  Kept: 0
  Deferred: 44
  Not-applicable: 0
  Already-bridged: 0

Bridges written: 3
  04_projects/personal/onboarding-agent-productized-service/bridge-tool-make-com-to-onboarding-agent-productized-service.md
  04_projects/personal/onboarding-agent-productized-service/bridge-tool-airtable-to-onboarding-agent-productized-service.md
  04_projects/personal/onboarding-agent-productized-service/bridge-tool-claude-code-to-onboarding-agent-productized-service.md

Conventions.md edit: yes — added productized-service to Situational archetypes block

Suggested commit (stages by name):

cd ~/workspace/second-brain
git add \
  04_projects/personal/onboarding-agent-productized-service/README.md \
  04_projects/personal/onboarding-agent-productized-service/_intel-inbox.md \
  04_projects/personal/onboarding-agent-productized-service/bridge-tool-make-com-to-onboarding-agent-productized-service.md \
  04_projects/personal/onboarding-agent-productized-service/bridge-tool-airtable-to-onboarding-agent-productized-service.md \
  04_projects/personal/onboarding-agent-productized-service/bridge-tool-claude-code-to-onboarding-agent-productized-service.md \
  04_projects/personal/onboarding-agent-productized-service/_punchlist.md \
  05_shared-intelligence/tools/tool-make-com.md \
  05_shared-intelligence/tools/tool-airtable.md \
  05_shared-intelligence/tools/tool-claude-code.md \
  00_inbox/decisions-pending/opportunity-onboarding-agent-productized-service.md \
  _meta/conventions.md
git status
git commit -m "Bootstrap project onboarding-agent-productized-service from opportunity via intel-routing BOOTSTRAP

Scaffolded under 04_projects/personal/onboarding-agent-productized-service/.
Archetypes: services-business + professional-services + productized-service + ai-tooling.
Confidence: medium. Pre-population PULL: 3 applied (Make.com, Airtable, Claude Code as
stack components per source body), 44 deferred, 0 kept.
Promoted productized-service archetype from absent to live in conventions.md.

Refs: _meta/specs/intel-routing-skill-spec.md"

cd ~/workspace/repos/onboarding-agent-productized-service
git add .kos/README.md .kos/.vault-config.md
git status
git commit -m "Scaffold .kos/ for intel-routing BOOTSTRAP'd project onboarding-agent-productized-service

Bootstrapped from [[opportunity-onboarding-agent-productized-service]] via intel-routing BOOTSTRAP.

Refs: ~/workspace/second-brain/_meta/specs/intel-routing-skill-spec.md"
```

## PASS criteria evaluation

- ✓ Apply-to-existing detection correctly recommended PROMOTE-TO-PROJECT (no project had strong overlap)
- ✓ Scaffold parameters proposal produced operator-acceptable defaults (only modifications were the operator opt-in for productized-service archetype promotion, which BOOTSTRAP correctly surfaced as a friction observation)
- ✓ Slug uniqueness check passed (no collision)
- ✓ Repo paste-prompt surfaced with operator-editable stack recommendation (Node.js + TypeScript + Airtable + Make.com + Stripe matches source body's tools-required line)
- ✓ KOS-setup invocation correctly delegated repo-side scaffolding; symlink created
- ✓ README customized with operator-confirmed archetypes + founding-artifact + purpose
- ✓ Inbox instantiated with substitutions correctly applied
- ✓ Conventions.md edit promoted productized-service correctly (operator confirmed at Gate 1)
- ✓ Chained PULL pre-populated inbox (3 applied, 44 deferred — operator-reasonable outcome for a new project whose stack components are pre-existing tools)
- ✓ Source artifact frontmatter updated with all three fields (applies-to-projects, routed-at, promoted-to-project)
- ✓ Single completion report covers all writes + suggested commit blocks for both repos
- ✓ No half-states: every write either landed atomically or rolled back

**BOOTSTRAP passes the promote-to-project happy path.**

## Calibration observations

1. **Apply-to-existing detection produced the right call.** Partial-overlap with keelworks could have tempted apply-to-existing, but body alignment was the right tiebreaker — opportunity describes operator-internal productization shape, not Keelworks-engagement work. Default-recommend apply-to-existing only on strong overlap is the right calibration.

2. **`(future)` archetype promotion friction is real.** `productized-service` doesn't exist in conventions yet, but the source artifact's shape genuinely needs it. Operator-explicit inline promotion at Gate 1 is the right pattern — the alternative (always falling back to closest live archetype) loses the signal. Single-line conventions edit costs nothing.

3. **Pre-population estimate matched actual PULL surface (47 → 47).** Confirms friction observation #8 maturation discipline: pre-flight reconnaissance gives operator accurate Gate-1-size expectations.

4. **0 slug-named items is the expected first-triage shape for new projects.** PULL pre-classification correctly defaulted everything to defer (since "keep" requires slug-named items in engagement context, which a brand-new project can't have). Operator-driven "move to apply" for the 3 tools explicitly named in source body was the right discipline-aware override. This is the friction-#4 maturation: single-bridge-per-cluster default is preserved (3 tools = 3 bridges, not 3 × tactic-using bridges).

5. **App-factory paste-prompt step is the right design.** Executor produces the fully-filled prompt with stack recommendation derived from source body; operator runs Claude Code in the new repo separately; operator confirms repo-created back to BOOTSTRAP. Cleanly separates the two execution surfaces while integrating into one BOOTSTRAP flow.

6. **Two-repo commit shape (vault + repo) is honest about where files live.** BOOTSTRAP touches both `~/workspace/second-brain/` (vault content) and `~/workspace/repos/<slug>/` (`.kos/` scaffold). Both need commits. Suggesting separate commits per repo is the right operator-readable shape.
