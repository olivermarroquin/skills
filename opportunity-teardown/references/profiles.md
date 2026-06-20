---
type: skill-reference
skill: opportunity-teardown
version: 1.0
created: 2026-06-16
updated: 2026-06-16
tags: [skill-reference, opportunity-teardown, profiles, config, general-purpose]
---

# Profiles (§2) — one engine, four source ecosystems

A **profile is config.** It declares which discovery lanes run, which extra fields/gates apply, and where output is
filed. **The engine logic in `SKILL.md` is identical across every profile** — only this config differs. This is how the
substrate is *inherited, not forked* (`feedback_tools_reusable_across_project_types`).

**Design rule (non-negotiable):** zero hardcoded sources, fields, gates, or destinations in the engine. Anything
profile-specific lives here. A new profile must be **provable from config on a second source** before its build is
called done (`feedback_no_half_finished_build_for_reuse`).

## Profile config shape

Every profile is one block with these keys:

```yaml
profile: <slug>                 # product-offer | startup-funding | oss-skill | mcp-connector
first_run_slice: <string>       # the concrete first slice to prove the profile (e.g. "AI content tools")
lanes:                          # which discovery lanes are active (built in [OR-1.1]; Lane A always on)
  - A   # operator manual-add (always on, every profile)
  - B   # AI-surface scan (Perplexity Sonar)
  - C   # marketplace / launch-board pull
  - D   # expansion from a keeper
extra_fields: [<field>, ...]    # profile-specific deep-dive fields beyond §6.1 (e.g. "why-funded / why-now")
special_gate: <none | safety-trust | safety-trust-strict>   # §11 gate; product/offer = none
destination:
  primary: <path>               # where pursued candidates are filed
  registry: 05_shared-intelligence/<build-it-better-registry>   # the scannable roll-up (all profiles)
scoring_weights_override: { ... }   # optional per-profile tweaks to §8 factors; omit to use defaults
```

---

## Profile #1 — product / offer (SHIPPED in v1.0)

The first profile and the one this skill's worked example exercises. First run = **AI content tools.**

```yaml
profile: product-offer
first_run_slice: "AI content tools"
lanes: [A]                      # v1.0 ships Lane A (manual-add) only; B/C/D arrive with [OR-1.1]
extra_fields: []                # uses the standard §6.1 teardown fields, no profile-specific additions
special_gate: none              # products don't touch Oliver's accounts/code; no safety gate
destination:
  primary: repos/idea-factory/strategies/_inbox/   # money play → Idea-stage extraction via idea-factory-prompter
  registry: 05_shared-intelligence/<build-it-better candidates registry>   # owned by [OR-1.3]
scoring_weights_override: {}    # default §8 factors
```

Notes:
- **Money profile** → routes to `repos/idea-factory/` (one-Active cap, `decisions.md` dedup, never auto-promote past
  Research) via `idea-factory-prompter`, plus a registry roll-up line.
- Lane A is the always-on operator manual-add: Oliver drops a product/URL/"I keep seeing X" → straight to the quick
  pass. Discovery lanes B/C/D are the finder's job (`[OR-1.1]`), not built here.

### Profile #1 — category variants (the slice is config, not logic)

`first_run_slice` is a **config parameter**, not engine logic. The same `product-offer` profile runs over any product
category by swapping this one string (and, on the finder side, the matching `default_category` / `lane_sources` in
`finder-config-profiles.md`). The engine's teardown / level-up / money / build-buy-use contracts are identical across
categories. Proven categories:

```yaml
# product-offer category variants — only the category string + finder lane framing differ; engine logic unchanged
categories:
  - slice: "AI content tools"          # 1st category (default) — first real run: BrandWell (2026-06-17), Opus Clip
  - slice: "AI developer tools"        # 2nd category — [OR-1.4] duplicability proof (config-only): Lovable (2026-06-17)
    note: >
      Same profile (product-offer), same lanes/gates/destination/scoring. ONLY the category string changes here +
      the matching default_category/lane_sources in finder-config-profiles.md. No SKILL.md edit. This is the spec §2
      "provable from config on a second source" test for the ENGINE, exercised at the [OR-1.4] capstone.
```

> **[OR-1.4] duplicability note:** the AI-developer-tools category was run end-to-end on **Lovable** with **zero edits
> to `SKILL.md`** — only this config block + the matching finder config block changed. If the engine had required a
> code change to handle a dev-tool (vs a content tool), the slice would not be config and OR-1.4 would log a
> generality finding. It did not. See the worked proof: `examples/` is unchanged; the proof artifact lives in the
> vault at `05_shared-intelligence/opportunity-radar/teardowns/teardown-2026-06-17-lovable-duplicability-proof.md`.

---

## Profile #2 — startup / funding (`[OR-2]`, STUB — inherits this engine)

Same engine, swap lanes to funding sources, add the "why funded / why now" lens. Defined fully by `[OR-2]`; sketched
here so the inheritance path is obvious.

```yaml
profile: startup-funding
first_run_slice: "<a funding cohort, e.g. recent YC batch>"
lanes: [A, B, C, D]             # B/C/D point at YC, startups.gallery, funding DBs, press
extra_fields: ["why-funded", "why-now", "who-backed-it"]
special_gate: none
destination:
  primary: repos/idea-factory/strategies/_inbox/
  registry: 05_shared-intelligence/<build-it-better candidates registry>
  plus: <a funding/trend directory + a recurring "where the money is going" synthesis>
```

What `[OR-2]` adds beyond config: the funding-teardown lens and the trend-synthesis destination. The teardown,
level-up, money layer, and build/buy/use decision are **unchanged** — they come from this engine.

---

## Profile #3 — open-source AI skill / repo (`[OR-4]`, ACTIVE v1.0 — full config in `[[profile-open-source-skill]]`)

> **Built `[OR-4]` 2026-06-19.** Full config + the §11 safety+trust gate logic + capability-home routing live in the
> dedicated file `references/profile-open-source-skill.md`. Proven end-to-end (config-only, no `SKILL.md` edit) on
> **`claude-task-master`** — see `[[teardown-2026-06-19-claude-task-master]]` + the gate run in `[[_safety-trust-gate-log]]`.

Same engine; lanes point at GitHub / skill directories / awesome-lists; **safety + trust gate ON** (§11); destination
is a **capability home** (the `skills/` library + vault enhancement), not idea-factory by default.

```yaml
profile: oss-skill
first_run_slice: "<a skill category, e.g. agent-orchestration skills>"
lanes: [A, B, C, D]             # C/D point at GitHub, skill directories, awesome-lists
extra_fields: ["license", "maintainer-activity", "stars-forks-slope"]
special_gate: safety-trust      # §11: no malicious code / license OK / maintained / not a typosquat
destination:
  primary: ~/workspace/skills/   # capability home (the library)
  registry: 05_shared-intelligence/<build-it-better candidates registry>
  plus: <vault-integration "super-vault" map>
  idea_factory_spark: only-when-clear-money-play
```

What `[OR-4]` adds beyond config: the §11 safety+trust gate logic and capability-home routing. Rejections logged with
reasons, never silently dropped.

---

## Profile #4 — MCP / connector (`[OR-5]`, STUB — inherits this engine)

Same engine; lanes point at the Claude connector registry / OpenAI-GPT directories / MCP indexes; **highest safety
bar** (§11) because connectors touch accounts and data; destination is a vault-integration map + idea-factory money
sparks for Oliver's Claude/ChatGPT accounts.

```yaml
profile: mcp-connector
first_run_slice: "<a connector category, e.g. data/analytics connectors>"
lanes: [A, B, C, D]
extra_fields: ["account-scopes-touched", "data-access-surface", "auth-model"]
special_gate: safety-trust-strict   # §11 highest bar: account + data exfiltration scrutiny strictest of all profiles
destination:
  primary: <vault-integration map>
  registry: 05_shared-intelligence/<build-it-better candidates registry>
  idea_factory_spark: when-clear-money-play (wiring a connector into Oliver's accounts)
```

What `[OR-5]` adds beyond config: the strict safety bar (account/data scopes) and integration-map routing.

---

## Adding a new profile (the inheritance contract)

1. Add a profile block here with the four config keys (`lanes`, `extra_fields`, `special_gate`, `destination`).
2. If the profile needs a new gate, register it (e.g. safety+trust) — but the engine calls it generically; don't fork
   the engine.
3. Prove it: run the engine end-to-end on the profile's `first_run_slice` from config alone. **No engine code changes
   allowed** — if the engine needs editing to support the profile, the profile boundary is wrong.
4. Confirm a second source in the same profile works from config too (`feedback_no_half_finished_build_for_reuse`).

If you can't instantiate a profile by editing only this file, the engine has leaked profile-specific assumptions —
that's a bug in the engine, not the profile.

## Related
- `[[SKILL]]` (the engine that reads this config) · `[[deep-dive-contract]]` · `[[quick-pass-contract]]` · `[[level-up-frameworks]]`
- spec `[[spec-opportunity-teardown-engine]]` §2 (profiles) + §15 (how the other profiles inherit)
