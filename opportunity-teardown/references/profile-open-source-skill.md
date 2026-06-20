---
type: skill-reference
skill: opportunity-teardown
profile: oss-skill
version: 1.0
created: 2026-06-19
updated: 2026-06-19
program: opportunity-radar
handoff: "[[handoff-2026-06-16-or4-open-source-skill-intelligence]]"
engine-freeze: "this file is profile CONFIG; it adds zero logic to opportunity-teardown/SKILL.md or opportunity-finder/SKILL.md (both md5-frozen for [OR-4])"
tags: [skill-reference, opportunity-teardown, profile, oss-skill, open-source, github, safety-trust-gate, capability-home, super-vault, config]
---

# Profile #3 — open-source AI skill / repo (`oss-skill`) — the "super-vault" profile

> **Authority:** `spec-opportunity-teardown-engine.md` §2 (profiles), §9/§9.1 (registry + wiring), §11 (safety
> gate), §15 (inheritance). This file is the **full** config for the `oss-skill` profile; the one-line index entry
> lives in `[[profiles]]` Profile #3. **It is config, not engine logic** — the `opportunity-teardown` engine and the
> `opportunity-finder` engine are both **logic-frozen** for `[OR-4]`. If anything here would require editing either
> `SKILL.md`, the profile boundary is wrong (that's a bug in the engine, not the profile).

This profile points the **proven** engine (`[OR-1.2]` shipped pass 236, `[OR-1.4]` capstone PASS pass 255) at
**open-source AI skills and repos**: find them → **safety-vet them BEFORE anything touches the vault** → tear down the
clean ones → design a better version → file them into Oliver's **capability home** (the `skills/` library + a vault
"super-vault" map) so his own capability compounds. *A super-vault stocked with the best of what others built, made his
and improved.*

What `[OR-4]` adds beyond config (and nothing else): the **§11 safety + trust gate logic** and **capability-home
routing**. The teardown, level-up, money layer, build-vs-buy-vs-use decision, scoring, and registry roll-up are
**unchanged** — they come from the engine.

---

## Profile config block

```yaml
profile: oss-skill
first_run_slice: "agentic-coding / AI task-management skills"   # worked example: claude-task-master (2026-06-19)
lanes: [A, B, C, D]             # A always on; B/C/D are the finder's job ([OR-1.1]) — see finder-config-profiles.md Profile #3
extra_fields:                   # profile-specific deep-dive fields beyond the standard §6.1 teardown
  - license                     # SPDX id + any rider (e.g. Commons Clause) + attribution requirement
  - maintainer-activity         # last commit/release, issue responsiveness, contributor count, archived?
  - stars-forks-slope           # the velocity signal for repos (growth rate, not just absolute count)
  - provenance                  # canonical owner/repo, is-fork, network-root — the typosquat anchor
  - install-surface             # what adopting it actually runs (npm/pip/MCP server/skill file) — feeds the safety gate
special_gate: safety-trust      # §11 — runs BEFORE the quick pass files anything; product/offer profile has none
destination:
  primary: ~/workspace/skills/  # CAPABILITY HOME — the engine PROPOSES an integration plan; the OPERATOR installs
  analysis_note: 05_shared-intelligence/opportunity-radar/teardowns/   # the teardown/analysis note
  capability_note: 05_shared-intelligence/tools/                       # the tools-as-notes capability library entry
  registry: 05_shared-intelligence/opportunity-radar/build-it-better-candidates-registry.md   # all-profiles roll-up
  safety_log: 05_shared-intelligence/opportunity-radar/_safety-trust-gate-log.md   # every vet, every reject + reason
  idea_factory_spark: only-when-clear-money-play   # NOT default; a "build it better" angle alone is NOT a money play
scoring_weights_override: { recency: 0.30, velocity: 0.45, saturation_headroom: 0.25 }   # stars/forks slope = velocity
```

**Non-destructive default:** the engine **never copies third-party code into `skills/`**. It writes an analysis note +
an integration/adoption plan and *proposes* installation; **Oliver installs.** (Spec §2 destination + §9 line 231 +
`feedback_no_half_finished_build_for_reuse` non-destructive default.)

---

## Discovery lanes (config; mechanics live in the frozen finder engine)

The finder's `oss-skill` lane-set is in `[[finder-config-profiles]]` Profile #3 (keep the `profile:` slug in sync).
This block records what each lane points at for *this* profile:

- **Lane A — operator manual-add (always on).** Oliver drops a repo/skill URL or "I keep seeing X skill" → it goes
  straight to the **safety gate**, then the quick pass. Highest value, zero reachability risk. *(Worked example used
  Lane A: operator-picked `claude-task-master`.)*
- **Lane B — AI-surface scan.** Perplexity Sonar (`reference_perplexity_sonar_only`): *"newly popular / fast-growing
  open-source AI skills/repos in {category}; star growth, maintenance status."* → candidate list + provenance.
- **Lane C — GitHub + directories.** GitHub trending / topic / search, `awesome-*` lists, skill directories (the
  Anthropic skills marketplace, MCP indexes, smithery-style registries). **JS-heavy pages escalate to Claude-in-Chrome
  or host-side — never accept a silent empty WebFetch** (`feedback_verify_substrate_and_escalate_webfetch`).
- **Lane D — expansion.** From a keeper: the author's other repos, notable forks, dependent projects, "alternatives to."

**Fresh + growing read (§4), repo-flavored.** Recency = last commit/release date + "new" signals. **Velocity =
stars/forks slope** (growth rate + npm/pip download trend), the dominant signal for repos (weight 0.45). Saturation
penalty = how many maintained equivalents already exist. **No undefended zeros** — any "abandoned / nobody uses this /
no equivalents" reading needs ≥2 sources + an adversarial check (`feedback_no_undefended_zeros_enumerate_sources`).
**Heavy/deep repo inspection runs host-side or in Chrome, not the 45s Cowork sandbox**, and fails loud about every
limitation in the headline (`feedback_heavy_collection_hostside_not_cowork`).

---

## §11 — The safety + trust gate (the genuinely new logic this profile adds)

**This gate RUNS — it is not a description.** It executes on **every** `oss-skill` candidate **before the quick pass
files anything and before any code is read in depth or adopted.** Nothing enters the vault unvetted. **Every rejection
is logged with a reason code in `_safety-trust-gate-log.md` — no silent drops**
(`feedback_verify_live_not_vault_and_no_silent_skips`). Claude will **not** integrate harmful code, full stop, no
matter how useful the skill looks.

### The four checks (run in order; first hard-fail short-circuits to REJECT)

1. **Legit & real? (provenance + typosquat)**
   - Resolve the **canonical** owner/repo; confirm it's the one the community actually uses (cross-check the package
     registry "repository" field ↔ the GitHub repo ↔ what directories/links point to).
   - Confirm the maintainer is a **real account with history** (not a days-old throwaway).
   - **Typosquat / look-alike check:** is the name a near-collision with a popular package, or an identical-description
     clone by a *different* owner? If you searched a generic name and got several identical repos, you must verify you
     are on the **canonical** one before proceeding. Look-alikes that aren't the canonical → `provenance-ambiguous`
     (HOLD) or `typosquat-lookalike` (REJECT) per evidence.
2. **Safe? (the highest-stakes check — no malicious code, no exfiltration, no prompt-injection traps)**
   - **Malicious code patterns:** outbound network calls to attacker domains, obfuscated/`eval`'d remote payloads,
     credential/env/secret harvesting (`~/.ssh`, `~/.aws`, `.npmrc`, env tokens), base64/hex blobs that decode to code,
     install-time scripts (`postinstall`) that do more than build.
   - **Data-exfiltration patterns:** silent BCC/forward/upload of user data, telemetry that ships content off-box,
     "phone-home" beacons. *(Real precedent: the `postmark-mcp` npm MCP server added a silent BCC to exfiltrate every
     email — `[[_safety-trust-gate-log]]` REJECT row.)*
   - **Prompt-injection traps (skills/agents specifically):** hidden instructions in skill/agent prompt files,
     `ignore previous instructions` payloads, tool-permission escalation, "read this secret and send it" tool chains,
     instructions that try to widen the agent's scope or exfiltrate via a tool. *(Real precedent: the Sandworm_Mode
     typosquat campaign weaponized rogue MCP servers to exfiltrate SSH/AWS/npm secrets via prompt injection.)*
   - **Depth rule:** the on-surface scan (README, manifest, install scripts, declared scopes) runs here; **deep
     line-by-line code audit of anything non-trivial runs host-side** and is required before any code is *adopted*. A
     candidate that *passes the surface scan but hasn't had its code deep-read* is **PASS-for-filing-the-analysis-note**
     but **HOLD-for-installation** — the note says "deep-read required before install."
3. **License OK?**
   - A **usable** license must be present (MIT/Apache-2.0/BSD/MPL/etc.); **no license = all-rights-reserved = REJECT
     for adoption** (note only).
   - **Record any rider** that changes what Oliver can do — e.g. **Commons Clause** (can use/modify/self-host but
     **cannot resell the software itself or offer it as a hosted service**), AGPL (network-copyleft), non-commercial
     clauses. This directly gates the money play: a Commons-Clause skill **cannot become a resold product** — only an
     internal capability or a service whose value isn't substantially the software itself. Note attribution required.
4. **Maintained / alive?**
   - Recent commits/releases, responsive issues, multiple contributors, **not archived**. An abandoned repo (no commits
     in ~12+ months, archived, dead issues) → `abandoned` REJECT unless there's a strong reason to fork-and-own it.

### Verdict states (logged for every candidate)

| Verdict | Meaning | What happens |
|---|---|---|
| **PASS** | clean on all four (surface-safe; deep-read flagged if code is non-trivial) | proceed to quick pass → teardown → capability-home routing |
| **HOLD** | one check needs host-side depth (deep code read) or provenance disambiguation | logged; surfaced to operator with exactly what's needed; **nothing filed as adopted** |
| **REJECT** | a hard fail on any check | logged with a **reason code**; **never enters the vault as a capability**; rejection itself is the record |

### Reason codes (safety-gate log)

| Reason code | Meaning |
|---|---|
| `malicious-code` | malicious code / install-time payload detected |
| `data-exfiltration` | silent data egress (BCC/forward/upload/beacon) |
| `prompt-injection-trap` | hidden/scope-widening/exfil instructions in skill/agent prompts |
| `typosquat-lookalike` | name/identity collision with a popular package by a different owner, evidence of deception |
| `provenance-ambiguous` | look-alike/fork by a different owner; canonical not confirmed → HOLD, not a hard reject |
| `no-usable-license` | no license, or a license incompatible with the intended use |
| `abandoned` | dead/archived/unmaintained, no fork-and-own case |
| `out-of-category` | not actually an open-source AI skill/repo in the scanned slice |
| `already-in-library` | already a tool-note / installed skill — dedup, link, don't re-surface |

**The product/offer profile does not run this gate** — it is `oss-skill`/`mcp-connector` config. `[OR-5]` reuses this
gate at the **strict** bar (account/data scopes) via `special_gate: safety-trust-strict`.

---

## How the standard teardown maps onto a skill (engine reused, fields filled the skill way)

The engine's §6.1 fields are filled as follows for a vetted `oss-skill` keeper (everything else — §6.2 build/buy/use,
§6.3 money, §6.4 visuals, §7 level-up, §8 score — is **unchanged engine logic**):

- **Why it works / rare-and-valuable core** → what capability it gives Oliver's setup that he doesn't have.
- **How they likely build it** → the actual architecture (the skill is open — read it, don't guess).
- **Replication requirements** → what it'd take to rebuild vs. adopt — feeds **build-vs-adopt-vs-use-as-is**.
- **The benefit** → concretely, which of Oliver's domains/projects/skills it enhances (the §9.1 wiring targets).
- **How to integrate it into Oliver's setup** → the **integration/adoption plan** (the capability-home deliverable):
  install path, where it slots in, what to configure, what to watch (license rider, deep-read-before-install).
- **The level-up** → build a better version *using their example* — the standard §7 framework + buildability gate.
- **Money play (only if clear)** → spark idea-factory **only** when there's a stated path to revenue **compatible with
  the license**; otherwise capability-home only.

**Build-vs-buy-vs-use, skill flavor:** **use-as-is** (adopt/install the skill) · **rebuild** (write our own better
version) · **skip**. "Just adopt it" is a valid winning answer (CLAUDE.md Core Principle: *when in doubt, ship*).

---

## Capability-home routing (§9 / §9.1)

A vetted **PASS** keeper produces, in order:

1. **Analysis/teardown note** → `opportunity-radar/teardowns/teardown-<date>-<slug>.md` (the full engine output).
2. **Capability-home tool-note** → `05_shared-intelligence/tools/tool-<slug>.md` (the tools-as-notes library entry,
   `status: noted` until the operator adopts) — with the **integration/adoption plan**.
3. **Registry roll-up line** → `build-it-better-candidates-registry.md` (+ its `.data.yaml`), `profile: oss-skill`.
4. **Safety-gate log row** → `_safety-trust-gate-log.md` (the PASS, plus every REJECT from the same run).
5. **`skills/` install** → **operator action.** The note proposes; Oliver installs. The engine does not auto-copy code.
6. **idea-factory spark** → **only** on a clear, license-compatible money play (not the default for a capability).

**§9.1 vault wiring is non-negotiable.** Every note cross-links (slug-only `[[wikilinks]]`) to: a **parent context**
(the registry or the spec) + **≥1 peer** + the **domains/projects/skills/ideas it enhances** (e.g. ``idea-factory``,
``execution-planner``, ``multi-chat-coordination``, EV/S&H/Keelworks projects, related tools already in the
library). An island note is a stewardship fail (Vault Stewardship rule 4, `feedback_check_folder_structure_before_writing`).

---

## Worked example (Lane A, end-to-end)

`[[teardown-2026-06-19-claude-task-master]]` — the full profile run on **`claude-task-master`** (eyaltoledano): safety
gate PASS (with two real REJECTs + look-alike HOLD logged in the same run) → quick pass → deep dive → level-up → score
→ capability-home routing (`[[tool-claude-task-master]]` + registry row). See `[[_safety-trust-gate-log]]` for the gate
run evidence.

---

## Adding the next source in this profile (the duplicability contract)

A second `oss-skill` source must run from **config alone** — no `SKILL.md` edit, no edit to *this* file's gate logic
(only new log/teardown/tool notes + a registry row). If the engine or finder needs editing to vet/teardown another
skill, the profile boundary leaked (`feedback_no_half_finished_build_for_reuse`).

## Related
- **Parent / authority:** `[[spec-opportunity-teardown-engine]]` (§2, §9.1, §11, §15) · `[[SKILL]]` (the frozen engine) · `[[profiles]]` (index, Profile #3)
- **Finder half:** `[[finder-config-profiles]]` Profile #3 (`oss-skill` lane-set — keep slug in sync)
- **Sibling profile:** `[[handoff-2026-06-16-or5-mcp-connector-intelligence]]` (`mcp-connector`, strict safety bar — reuses this gate)
- **Outputs:** `[[_safety-trust-gate-log]]` · `[[teardown-2026-06-19-claude-task-master]]` · `[[tool-claude-task-master]]` · `[[build-it-better-candidates-registry]]`
- **Pattern (shared with [OR-5]):** ``pattern-safety-vetted-capability-ingestion` (pattern candidate — 1st instance; promote at [OR-5])` (promote if it generalizes)
