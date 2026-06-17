---
name: opportunity-teardown
version: 1.0
status: active
created: 2026-06-16
updated: 2026-06-16
description: The general-purpose engine that turns one opportunity (a product, offer, funded startup, open-source AI skill, or MCP/connector) into a beefy quick pass, then — on keepers only — a full report covering the teardown, the level-up, the money/go-to-market plan, and a build-vs-buy-vs-use-as-is decision, then ranks it and routes it into the idea-factory or a capability home. Use this skill whenever the operator drops a product/URL/"I keep seeing X" and wants it vetted and torn down, says "run the teardown on this," "opportunity teardown," "should I build/buy/use this," "level this up," "what's the money play on this tool," or wants an external thing decomposed into a build-it-better plan. Profile-driven (products/offers = profile #1); [OR-2] startups, [OR-4] open-source skills, and [OR-5] MCPs inherit the same engine via config. Composes vis-extraction (ingest one source), idea-factory-prompter (route), prioritization + scoring-rubric (rank), and gate-peer-reviewer + output-quality-loop (gates). Do NOT use for per-client SEO competitor-beating — that is market-intelligence-engine.
triggers:
  - operator drops a product / URL / "I keep seeing X" and wants it vetted + torn down (Lane A manual-add)
  - phrases like "run the teardown on this," "opportunity teardown," "tear this down," "level this up," or "build it better"
  - asks should I build, buy, or just use this — or what's the money play on this tool
  - a discovery finder ([OR-1.1]) hands a vetted candidate down for the deep dive
  - any opportunity-radar profile run (products / startups / open-source skills / MCPs)
composes-with:
  - vis-extraction (per-source ingest — read any one URL/page; do not rebuild transcript/page pull)
  - idea-factory-prompter (route a pursued teardown into repos/idea-factory as an Idea-stage extraction)
  - prioritization + _meta/scoring-rubric.md (rank candidates; build-for-myself-first is a first-class tag)
  - competitor-deep-research (borrow the "decompose a winner" discipline; do NOT bend CDR — it is per-client SEO scope)
  - gate-peer-reviewer (G-default or registered gate) + output-quality-loop (every teardown + registry write)
  - reference-finder pattern [DI-7] (discovery lanes live in [OR-1.1], not here)
tags: [skill, opportunity-radar, opportunity-teardown, engine, profile-driven, general-purpose, teardown, level-up, build-vs-buy, money-map, reusable-substrate]
---

# `opportunity-teardown` skill v1.0 — the engine

> **Authority:** this skill is built to `second-brain/_meta/handoffs/opportunity-radar/spec-opportunity-teardown-engine.md`.
> If this file and the spec ever disagree, **the spec wins** until amended there. Section references below (§5, §6,
> §7, §8, §12, §14) point at that spec.

The single, general-purpose engine that powers the whole `opportunity-radar` program. It takes **one opportunity**
and runs a **two-tier teardown** — a meaty quick pass for vetting, then a full report only on the keepers — designs a
**better version** with a real build plan, decides **build-vs-buy-vs-use-as-is**, ranks it, and **files it wired into
the rest of the vault** so the best ones get built (for Oliver's own use first, sold later).

**Designed once, reused four ways.** Products/offers are the **first profile**. Funded startups (`[OR-2]`), open-source
AI skills/repos (`[OR-4]`), and Claude/ChatGPT MCP connectors (`[OR-5]`) are **additional profiles** that plug into this
same engine — different sources, different gates, different destinations, identical teardown discipline. Nothing is
built twice. The profile is config; the engine logic does not change.

## What this skill is and is NOT

**It IS** the orchestrating brain: the two-tier flow, the contracts that define each output, the level-up engine, the
money layer, and the build/buy/use decision. These contracts are the genuinely new work.

**It is NOT** a discovery tool, an ingest tool, a ranker, a router, or a gate. Those already exist — this skill
**composes** them (§14). Build only what's new; reuse the rest:

| Step | Owned by | This skill's job |
|---|---|---|
| Discover candidates | `reference-finder` pattern `[DI-7]` → built in `[OR-1.1]` | Accept a candidate (Lane A: operator drops one); do not rebuild discovery |
| Ingest one source | `vis-extraction` | Call it to read the URL/page; consume its output |
| Teardown + level-up + money + build/buy/use | **this skill (new)** | The contracts in `references/` |
| Rank | `prioritization` + `_meta/scoring-rubric.md` | Hand candidates over with the scoring profile |
| Route | `idea-factory-prompter` → `repos/idea-factory/` | Hand a pursued teardown over for a spawn prompt |
| Gates | `gate-peer-reviewer` + `output-quality-loop` | Dispatch on every teardown + registry write |

**Do NOT use this skill for** per-client SEO competitor-beating — that is `market-intelligence-engine` (`[MI-5]`).
Keep the boundary clean; share teardown vocabulary where it helps, but this engine scans the *outside world for things
worth building*, not a *named client's local competitors*.

## Invocation modes

The skill runs in one of three modes. The operator (or an upstream chat) names the mode; default is `quick-pass`.

- **`quick-pass`** — run the §5 beefy preview on one or more candidates and stop at the operator gate. Cheap. The
  default for anything freshly added or freshly discovered.
- **`deep-dive`** — run the full §6 report + §6.2 build/buy/use + §6.3 money layer + §7 level-up on **one** keeper the
  operator has flagged worth pursuing. Expensive. Only runs post-gate.
- **`full`** — quick pass → present at the operator gate → on a go, continue straight into the deep dive + level-up +
  decision + score + route, for one candidate. Use when the operator already trusts the candidate (e.g. a Lane A
  manual-add of something they keep seeing).

Always state the active mode and profile at the top of any run.

## The pipeline (one line)

> **Discover → Quick Pass (vet) → [operator gate] → Deep Dive (full report) → Level-up → Decide (build/buy/use) → Score → Registry → Route → build-for-myself-first.**

Two depths on purpose. The beefy-but-cheap quick pass runs over everything; the expensive full report runs **only** on
candidates the operator and the engine agree are worth pursuing. This is the core defense against a firehose of noise:
depth where it pays, breadth held in check.

The engine **proposes; the operator disposes.** It never auto-ingests, never auto-promotes past Research, and never
spends money on its own (it can *recommend* a paid trial; Oliver makes the purchase).

---

## Step 0 — Set the profile

A **profile** is config: which discovery lanes apply, which extra fields/gates apply, and where output is filed. Read
`references/profiles.md` and select the profile. v1.0 ships **profile #1: product/offer** (first run = **AI content
tools**). The engine logic below is identical for every profile; only the config differs.

If invoked with no profile named, default to **product/offer** and say so.

**Design rule (non-negotiable):** zero hardcoded sources, fields, gates, or destinations in the engine. If you find
yourself writing "AI content" into the engine logic, stop — that belongs in the profile config. Every profile must be
provable from config on a second source before its build is called done
(`feedback_tools_reusable_across_project_types`, `feedback_no_half_finished_build_for_reuse`).

## Step 1 — Intake the candidate (Lane A in v1.0)

v1.0 ships **Lane A — operator manual-add (always on):** Oliver drops a product / URL / "I keep seeing X" and it goes
straight into the quick pass. This is the VIS-ingestion shape applied to opportunities — highest value, zero
reachability risk, ships first. Lanes B/C/D (AI-surface scan, marketplace pull, expansion) are the discovery finder's
job (`[OR-1.1]`) and are not built here; the engine simply accepts whatever candidate arrives.

To read the source, **call `vis-extraction`** — do not write a new transcript/page puller. If the sandbox can't reach
the URL, route the pull to the host machine; never fake the read (`feedback_heavy_collection_hostside_not_cowork`,
`feedback_verify_substrate_and_escalate_webfetch` — an empty WebFetch on a JS page is a tool limitation, escalate to
Claude-in-Chrome, never log-and-defer).

Record **provenance** on intake: lane + source + date.

## Step 2 — Quick Pass (beefy preview) — `references/quick-pass-contract.md`

Produce the §5 quick pass for the candidate. It is **not a stub** — it must let Oliver decide "dig deeper?" with
confidence. Fields (verbatim from §5): **what it is · the value & the interest · why it's a good idea · how it makes
money · fresh/growing read · how crowded · provenance.**

What the quick pass deliberately **holds back** for cost control (these come only after the operator flags a keeper):
the paid hands-on trial, diagrams/visuals, the deep business/money plan, and the full level-up.

**Noise-filter discipline (§4):** the "fresh + growing" read is a lightweight 3-factor score (recency · velocity ·
saturation penalty), not heavy scraping. **No undefended zeros / single-source claims** — any "0 / empty / saturated /
nobody's doing this" reading needs **≥2 sources + an adversarial check** that tries to disprove it
(`feedback_no_undefended_zeros_enumerate_sources`).

## Step 3 — Operator gate (mandatory stop)

Present the quick pass and **stop**. The operator decides: pursue (→ deep dive), park, or skip. The engine never
self-advances from quick pass to deep dive. In `full` mode the operator may pre-authorize the continue, but the gate is
still shown.

## Step 4 — Deep Dive (full report) — `references/deep-dive-contract.md`

Runs only on a flagged keeper. **Format = a full report:** plain-language, intellectual-but-understandable
explanations a decision can be made from, **plus diagrams/visuals where they help (keepers only — §6.4).** Two-file
output: a **human markdown report + a machine-readable YAML block** (`reference_pattern_two_file_artifact_split`).

The deep dive has three layers; all are defined field-by-field in `references/deep-dive-contract.md`:

1. **§6.1 The teardown** — angle/positioning, creative & marketing hooks, the problem + **what the pain actually looks
   like in real life** (concrete examples), a **use walk-through** (not a description), the rare-and-valuable core, how
   they likely build it, replication requirements, value→money mechanism, **the one key money-making insight** (single
   sentence: *why this prints money*), why buyers are pulled in, moat & gaps, **build-for-myself-first fit** (the
   north-star filter), **effort-to-clone** (S/M/L), and an **evidence/confidence tag per claim**.
2. **§6.2 The build-vs-buy-vs-use-as-is decision** — recommend whether it's worth paying for a month to try hands-on
   (Oliver buys, not the engine), then the honest three-way call: **rebuild ourselves** (does it actually save money?)
   · **use it as-is to make money faster** (the engine must be willing to say *don't rebuild, just use it and earn* —
   the built-in guard against the over-build-the-factory trap; CLAUDE.md Core Principle *when in doubt, ship*) · **skip.**
3. **§6.3 The money / go-to-market layer** — sectors & pains worth real money, where to plug it in, **who to pitch +
   price + the honest ROI math** (their benefit in real dollars vs. what they'd pay Oliver), the Keelworks-service
   path, short-term vs. long-term play, and the **crawl → walk → run** playbook.

**Evidence discipline (no hype laundering):** tag every claim `verifiable` / `partially-verifiable` / `unverifiable` /
`likely-fake` (the idea-factory `INGESTION-PROTOCOL` quality bar). Strip guru optimism. Use real numbers in the ROI
math, not vibes.

**§6.4 Visuals:** on vetted keepers only, generate simple diagrams where they aid a decision (how it works, or what the
better version looks like). Image/diagram generation that must land in the vault runs **host-side**, not from the
Cowork sandbox (`reference_cowork_chrome_screenshots_not_vault_reachable`) — generate in Cowork only as inline
previews; flag anything that needs to be a committed vault asset for host-side rendering.

## Step 5 — Level-up (design the superior version) — `references/level-up-frameworks.md`

Creative on the **idea**, disciplined on the **plan**. Run the §7 **framework checklist every time** (jobs-to-be-done ·
10x-not-10% · unbundle/rebundle · make-the-boring-part-disappear · verticalize · AI-native rebuild) plus **one
free-form wildcard** so it isn't purely mechanical. Output **1–3 ranked "superior version" concepts**, each with:

1. **The creative leap** — which lever it pulls and why it's more valuable.
2. **What you'd have to build to make it real** — the components; "is this even possible, and how."
3. **A strategic build plan** — a real sequence, not a daydream.
4. **A hard buildability gate** — it must name what it'd take *Oliver* to ship it with the current stack, or it's
   flagged **speculative**, not a real candidate. **No fantasy.**
5. **Market-crowding check on the better idea too** — are others already doing *this* improved version, how many, still
   early? Run on both the original and our version (crowded-and-late kills more ideas than bad ideas do).

## Step 6 — Score & prioritize (§8)

Hand the candidate(s) to the `prioritization` skill with `_meta/scoring-rubric.md`. Factors: fresh/growing score,
**build-for-myself-first fit** (first-class tag), effort-to-clone (inverse), money potential (short + long), market
headroom (inverse of saturation), and strategic fit with current focus (`project_priority_client_seo_traffic` for
client-routable ideas). Use the rubric's tier (1–4) / relevance (1–5) / actionability (1–5) / monetization
(high/med/low/none) scales — do not invent new scales.

## Step 7 — Registry + route (§9 / §10)

This skill **does not own** the registry or the routing build — those are `[OR-1.3]` and `[OR-1.0]`. When they exist,
this engine hands off:

- **Money profiles (product/offer, startups):** a pursued teardown → `idea-factory-prompter` drafts a fully-loaded
  spawn prompt → enters `repos/idea-factory/strategies/_inbox/` as an **Idea-stage** extraction with `source-type`
  provenance. Respects the **one-Active-at-a-time cap** and `decisions.md` **dedup**; **never auto-promotes past
  Research** (the skeptic enforces this). Plus a line in the scannable **build-it-better candidates registry** in
  `05_shared-intelligence/`.
- **Capability profiles (open-source skills `[OR-4]`, MCPs `[OR-5]`):** file to capability homes instead — the
  `skills/` library + a vault-integration map — with an idea-factory spark only when there's a clear money play.

**Vault wiring is non-negotiable (§9.1):** every registry entry cross-links into the rest of the vault — tools already
ingested (past VIS runs in `03_domains/*/insights/` + `05_shared-intelligence/tools/`) that could help build it, skills
that apply, projects it could serve (EV, S&H, Keelworks), and related candidates. Slug-only `[[wikilinks]]`; link to a
parent context + at least one peer (Vault Stewardship rule 4, `feedback_check_folder_structure_before_writing`).

Until `[OR-1.0]`/`[OR-1.3]` land, the engine writes the deep-dive report to disk and **describes the intended routing**
(what spawn prompt it would generate, what registry row it would add) rather than writing into idea-factory blind.

## Step 8 — Safety & trust gate (capability profiles only — §11)

For `[OR-4]` repos and `[OR-5]` MCPs, before anything touches the vault or Oliver's accounts: **legit & real?**
(provenance, maintainer, activity, not a typosquat) · **safe?** (no malicious code, no data-exfiltration patterns, no
prompt-injection traps — Claude will not integrate harmful code; `[OR-5]` carries the **highest** bar because
connectors touch accounts and data) · **license OK?** · **maintained?** Rejections are **logged with reasons, never
silently dropped** (`feedback_verify_live_not_vault_and_no_silent_skips`). The product/offer profile does not run this
gate; it is profile config.

## Quality gates (§12) — every output

Run `gate-peer-reviewer` (**G-default**, or a registered gate type if one applies) **and** `output-quality-loop` on
every teardown and every registry write. **Full-artifact sweep before grading, not section spot-checks**
(`feedback_full_artifact_sweep_not_spot_checks`) — grep the whole report for unresolved placeholders, untagged claims,
and broken links before declaring it done.

**Producer ↔ peer-review pairing (this skill's own build + any orchestrated run that ships an artifact):** the producer
ships and appends a `ready-for-review` row to `_meta/_event-log.md`, **then** an independent reviewer is spawned as a
**separate** chat. The **reviewer authors the verdict — the producer may not self-gate**
(`feedback_dont_self_gate_run_independent_review`, `feedback_peer_review_chat_spawn_discipline`). Don't spawn the
reviewer mid-run; spawn at the event-log ready signal.

## Quality bar (the discipline that makes the output worth reading)

- **Compose, don't reinvent.** VIS ingests; this skill tears down; prompter routes; prioritization ranks. Build only
  the contracts + the orchestration.
- **General-purpose / profile-driven.** Zero hardcoded "AI content" assumptions in the engine; the slice is config. A
  second profile must be a config change, not a fork.
- **Buildability is a hard gate.** Every level-up names what it'd take Oliver to ship it, or is flagged speculative.
- **No hype laundering.** Evidence/confidence tag per claim; strip guru optimism.
- **"Just use it" is a valid winning answer.** The build/buy/use call must be willing to say *don't rebuild, use it and
  earn.*
- **Plain language** (`feedback_plain_language_default`). Full reports are intellectual-but-understandable and
  decision-ready; gloss jargon inline.
- **The engine proposes; the operator disposes.** No auto-ingest, no auto-promote, no autonomous spending.

## How the other profiles inherit this (§15)

| Profile | Handoff | Swap in config | Extra gate | Destination |
|---|---|---|---|---|
| Product / offer (v1.0) | `[OR-1.x]` | Lanes A–D (A built here) | — | `repos/idea-factory/` + registry |
| Startup / funding | `[OR-2]` | funding-source lanes; add "why funded / why now" lens | — | idea-factory + funding/trend directory |
| Open-source AI skill | `[OR-4]` | GitHub/skill-directory lanes | **safety + trust gate** | `skills/` library + vault enhancement |
| MCP / connector | `[OR-5]` | connector-registry lanes | **highest safety bar** | vault-integration map + idea-factory sparks |

`[OR-3]` publishing is a **consumer, not a profile** — it turns these outputs into reports/video/newsletter (deferred).

## Files in this skill

```
opportunity-teardown/
├── SKILL.md                              ← this file (the engine + orchestration)
├── references/
│   ├── quick-pass-contract.md            ← §5 fields verbatim (beefy preview)
│   ├── deep-dive-contract.md             ← §6 + §6.2 + §6.3 + §6.4 (two-file output)
│   ├── level-up-frameworks.md            ← §7 framework checklist + wildcard + buildability gate
│   └── profiles.md                       ← §2 profile config shape; product profile + OR-2/4/5 stubs
└── examples/
    └── opus-clip-worked-example.md       ← full engine run on one real AI content tool (Lane A)
```

## What this skill does NOT do

- Does not discover candidates (that's `[OR-1.1]`, the reference-finder pattern).
- Does not pull transcripts/pages itself (that's `vis-extraction`).
- Does not build the registry or the idea-factory wiring (that's `[OR-1.3]`/`[OR-1.0]`); it hands off to them.
- Does not promote anything past Research, auto-ingest, or spend money.
- Does not handle per-client SEO competitor work (that's `market-intelligence-engine`).
