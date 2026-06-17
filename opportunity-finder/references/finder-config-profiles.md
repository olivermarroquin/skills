---
type: skill-reference
skill: opportunity-finder
version: 1.0
created: 2026-06-17
updated: 2026-06-17
tags: [skill-reference, opportunity-finder, profiles, config, general-purpose, lane-set, scoring-weights, second-corpus-proof]
---

# Finder config profiles — the lane-set + scoring weights are config (general-purpose)

The finder's engine logic (`SKILL.md`) is **identical across profiles.** Only this file changes per profile. A profile
declares: which **lanes** run, the **category/window** to scan, any **scoring-weight overrides**, the **dedup target**
(which registry to dedup against, alongside the always-on candidate cache), and where keepers route.

**This config mirrors the engine's `opportunity-teardown/references/profiles.md`** — the finder lane-set for a profile
is the discovery half of the same profile the engine files into. Keep the two in sync (same `profile:` slug).

## Profile config shape

```yaml
profile: <slug>                  # product-offer | startup-funding | oss-skill | mcp-connector
default_category: <string>       # the slice to scan by default (e.g. "AI content tools")
default_window: <string>         # recency window for Lane B (e.g. "12 months")
lanes: [B, C, D]                 # which finder lanes run (A lives in the engine, always available)
lane_sources:                    # per-lane source list for this profile
  B: <sonar prompt category framing>
  C: [<board/marketplace urls>]
  D: <expansion framing>
scoring_weights:                 # override the §4 defaults; omit to use 0.35/0.40/0.25
  recency: 0.35
  velocity: 0.40
  saturation_headroom: 0.25
dedup_target: 05_shared-intelligence/opportunity-radar/<build-it-better-registry>   # owned by [OR-1.3]; cache is always-on
keeper_route: <where a picked keeper goes after the engine deep dive>   # informational; the engine owns routing
special_note: <e.g. safety-gate applies in the engine for this profile>
```

---

## Profile #1 — product / offer (DEFAULT, exercised in v1.0)

```yaml
profile: product-offer
default_category: "AI content tools"
default_window: "12 months"
lanes: [B, C, D]
lane_sources:
  B: "AI content tools (script/video/image/copy generation, repurposing, automation)"
  C:
    - "https://www.producthunt.com/topics/artificial-intelligence"
    - "https://www.producthunt.com/topics/content"
    - "https://appsumo.com/browse/?search=ai+content"
    - "https://gumroad.com/discover?query=ai%20content"
  D: "alternatives-to / vs / same-maker expansion from a keeper"
scoring_weights: { recency: 0.35, velocity: 0.40, saturation_headroom: 0.25 }
dedup_target: 05_shared-intelligence/opportunity-radar/<build-it-better-registry>   # [OR-1.3]; absent during v1.0 dry-run → wired-but-deferred-proof
keeper_route: repos/idea-factory/strategies/_inbox/   # money play, via idea-factory-prompter (engine owns this)
special_note: "no safety gate (products don't touch Oliver's accounts/code)"
```

---

## Profile #2 — startup / funding (`[OR-2]`) — the 2nd-lane-set PROOF (config-only, no skill change)

This profile is the v1.0 **general-purpose proof**: the finder runs the `[OR-2]` startup-funding lane-set **from this
config alone**, with **zero edits to `SKILL.md` or any other reference.** It demonstrates the lane-set + weights are
truly config. (`[OR-2]` later adds the funding-teardown *lens* in the engine; the discovery half is fully expressed
here.)

```yaml
profile: startup-funding
default_category: "recently-funded startups (a YC batch or a funding-DB cohort)"
default_window: "6 months"
lanes: [B, C, D]
lane_sources:
  B: "recently funded / fast-growing startups in {sector}; who funded them, why now"
  C:
    - "https://www.ycombinator.com/companies?batch=<recent>"
    - "https://startups.gallery"
    - "<a funding-DB listing, e.g. a Crunchbase/PitchBook public page>"
  D: "co-investors' other bets / the founders' prior companies / category neighbors"
scoring_weights:                 # funding cares more about velocity+recency, less about saturation headroom
  recency: 0.40
  velocity: 0.45
  saturation_headroom: 0.15
dedup_target: 05_shared-intelligence/opportunity-radar/<build-it-better-registry>
keeper_route: "repos/idea-factory/strategies/_inbox/ + a funding/trend directory (engine, per [OR-2])"
special_note: "engine adds the 'why funded / why now / who backed it' lens at deep-dive; discovery half is config-only here"
```

**Why this proves general-purpose:** swapping `product-offer` → `startup-funding` changed only (a) the lanes' source
lists, (b) the category/window, and (c) the scoring weights. The lane *mechanics* (Sonar query → parse, fetch →
escalate-to-Chrome, expansion-from-keeper), the dedup, the §4 scoring math, the cap-5 shortlist, and the operator-triage
flow are **unchanged**. If `[OR-2]` had required a code change in `SKILL.md`, the profile boundary would be wrong — a
bug in the finder, not the profile (`feedback_no_half_finished_build_for_reuse`).

The proof was **exercised** (a real config-only `discover` pass on the `startup-funding` `lane_sources`, no `SKILL.md`
edits) and persisted — see `[[_run-log-2026-06-17]]` § "Lane B — OR-2 startup-funding profile" (verdict: PASS, 9
funded-startup candidates, disjoint from the product set). Re-confirmed at the `[OR-1.4]` integration capstone.

---

## Profile #3 — open-source AI skill / repo (`[OR-4]`, STUB)

```yaml
profile: oss-skill
default_category: "a skill category, e.g. agent-orchestration skills"
default_window: "12 months"
lanes: [B, C, D]
lane_sources:
  B: "newly popular open-source AI skills/repos in {category}; star growth, maintenance"
  C: ["GitHub trending/search for {category}", "awesome-* lists", "skill directories"]
  D: "the author's other repos / forks / dependent projects"
scoring_weights: { recency: 0.30, velocity: 0.45, saturation_headroom: 0.25 }   # stars/forks slope = velocity
dedup_target: 05_shared-intelligence/opportunity-radar/<build-it-better-registry>
keeper_route: "~/workspace/skills/ (capability home) + vault map (engine, per [OR-4])"
special_note: "engine applies the §11 safety+trust gate (no malicious code / license / maintained / not typosquat)"
```

## Profile #4 — MCP / connector (`[OR-5]`, STUB)

```yaml
profile: mcp-connector
default_category: "a connector category, e.g. data/analytics connectors"
default_window: "12 months"
lanes: [B, C, D]
lane_sources:
  B: "new MCP/connectors for Claude/ChatGPT in {category}; what they unlock"
  C: ["Claude connector registry", "OpenAI/GPT directories", "MCP indexes"]
  D: "the maker's other connectors / the registry's related entries"
scoring_weights: { recency: 0.35, velocity: 0.40, saturation_headroom: 0.25 }
dedup_target: 05_shared-intelligence/opportunity-radar/<build-it-better-registry>
keeper_route: "vault-integration map + idea-factory money sparks (engine, per [OR-5])"
special_note: "engine applies the §11 HIGHEST safety bar (connectors touch accounts + data)"
```

## Adding a new profile (the inheritance contract)

1. Add a profile block here with the config keys above.
2. Switch on/off lanes in `lanes:` (e.g. enable a deferred ad-library lane once built).
3. Prove it: run the finder `discover` mode on the profile's `default_category` **from config alone — no `SKILL.md`
   edits.** If the finder needs editing to support the profile, the boundary is wrong.
4. Keep the `profile:` slug in sync with `opportunity-teardown/references/profiles.md` so discovery → teardown compose.

## Related
- `[[SKILL]]` · `[[discovery-lanes]]` · `[[fresh-growing-scoring]]` · `[[dedup-rejection-sourceyield]]`
- engine config `[[profiles]]` (keep slugs in sync) · spec `[[spec-opportunity-teardown-engine]]` §2 + §15
