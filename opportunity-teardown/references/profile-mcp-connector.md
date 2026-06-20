---
type: skill-reference
skill: opportunity-teardown
profile: mcp-connector
version: 1.0
created: 2026-06-20
updated: 2026-06-20
program: opportunity-radar
handoff: "[[handoff-2026-06-16-or5-mcp-connector-intelligence]]"
engine-freeze: "this file is profile CONFIG; it adds zero logic to opportunity-teardown/SKILL.md or opportunity-finder/SKILL.md (both md5-frozen for [OR-5]: teardown c975d797eb5e7fb4063237423154add8, finder 75a14c487fde49408c3862bb807898cf)"
tags: [skill-reference, opportunity-teardown, profile, mcp-connector, mcp, connectors, claude, chatgpt, safety-trust-strict, account-scope, integration-map, config]
---

# Profile #4 — MCP / connector (`mcp-connector`) — the strict account-scope profile

> **Authority:** `spec-opportunity-teardown-engine.md` §2 (profiles), §9/§9.1 (registry + wiring), §11 (safety
> gate — **highest bar**), §15 (inheritance). This file is the **full** config for the `mcp-connector` profile; the
> one-line index entry lives in `[[profiles]]` Profile #4. **It is config, not engine logic** — the
> `opportunity-teardown` engine and the `opportunity-finder` engine are both **logic-frozen** for `[OR-5]`. If anything
> here would require editing either `SKILL.md`, the profile boundary is wrong (a bug in the engine, not the profile).

This profile points the **proven, frozen** engine (`[OR-1.2]` shipped pass 236, `[OR-1.4]` capstone PASS pass 255,
`[OR-4]` consumed pass 277) at **MCP servers and connectors that extend Claude and ChatGPT**: find the good ones →
**safety-vet them at the highest bar BEFORE anything is wired into Oliver's accounts** → tear down the clean ones →
design a better version → file them into a **vault integration map** (what's wired, the exact scopes it holds, what it
unlocks) so Oliver's setup keeps getting more capable, with an **idea-factory money spark only when there's a clear
play.** *A connected operating system whose every plug has been scope-audited before it touches an account.*

What `[OR-5]` adds beyond config (and nothing else): the **§11 strict safety + trust gate logic** at the
**account-scope bar** (`safety-trust-strict`) and **integration-map routing**. The teardown, level-up, money layer,
build-vs-buy-vs-use decision, scoring, and registry roll-up are **unchanged** — they come from the engine.

**Distinct from `[OR-4]` (operator-required).** `[OR-4]` is open-source AI **skills/repos** (passive code files);
`[OR-5]` is **MCP servers / connectors** (live plugs that hold credentials and act on accounts + data). They **share
the safety-gate pattern, not the profile.** The `[OR-5]` gate is **strictly higher**: it adds an **account-scope /
permission / data-access** dimension that a passive skill file does not have. The shared pattern is captured at
`[[pattern-safety-vetted-capability-ingestion]]` (promoted at `[OR-5]`; note the stricter account-scope bar there).

**Nothing in this profile wires a connector.** The engine produces *intelligence + a safe-to-wire recommendation with
the exact least-privilege scope it should be granted.* **Oliver does the wiring.** The engine never connects an MCP to
an account, never spends money, never auto-installs (`feedback_no_half_finished_build_for_reuse` non-destructive
default; CLAUDE.md "engine proposes, operator disposes").

---

## Profile config block

```yaml
profile: mcp-connector
first_run_slice: "SEO / search-data connectors for Claude"   # worked example: DataForSEO MCP (2026-06-20)
lanes: [A, B, C, D]             # A always on; B/C/D are the finder's job ([OR-1.1]) — see finder-config-profiles.md Profile #4
extra_fields:                   # profile-specific deep-dive fields beyond the standard §6.1 teardown
  - account-scopes-touched      # the EXACT OAuth scopes / API-key permissions it requests (least-privilege analysis)
  - data-access-surface         # what data it can read AND write/delete; can it touch data outside its stated job?
  - auth-model                  # OAuth 2.1 (+PKCE, revocable consent)? API key? restricted/read-only key offered?
  - token-handling              # where the credential lives (env/plaintext/remote server); who else can see the token
  - transport                   # local stdio vs remote HTTP/SSE; remote = bigger surface + the server sees your token
  - write-capability            # does it write/move money/delete by DEFAULT, or is it read-only?
  - publisher-provenance        # first-party vendor? community? canonical vs spoof/look-alike
special_gate: safety-trust-strict   # §11 HIGHEST bar — account + data scope scrutiny, strictest of all profiles
destination:
  primary: 05_shared-intelligence/connector-integration-map.md   # the VAULT INTEGRATION MAP (capability home for connectors)
  analysis_note: 05_shared-intelligence/opportunity-radar/teardowns/   # the teardown/analysis note
  capability_note: 05_shared-intelligence/tools/                       # the tools-as-notes capability library entry
  registry: 05_shared-intelligence/opportunity-radar/build-it-better-candidates-registry.md   # all-profiles roll-up
  safety_log: 05_shared-intelligence/opportunity-radar/_safety-trust-gate-log.md   # every vet, every reject + reason
  idea_factory_spark: only-when-clear-money-play   # NOT default; wiring a connector into Oliver's accounts to SELL a service
scoring_weights_override: { recency: 0.35, velocity: 0.40, saturation_headroom: 0.25 }   # connector adoption/maintenance = velocity
```

**Non-destructive default:** the engine **never wires a connector into an account and never copies connector code into
the vault.** It writes an analysis note + an integration plan **with the exact least-privilege scope to grant** and
*proposes* wiring; **Oliver wires.** (Spec §2 destination + §9 line 231; `feedback_verify_destructive_admin_actions`
spirit — name the scope explicitly, recommend the least-privilege option that does the job.)

---

## Discovery lanes (config; mechanics live in the frozen finder engine)

The finder's `mcp-connector` lane-set is in `[[finder-config-profiles]]` Profile #4 (keep the `profile:` slug in sync).
This block records what each lane points at for *this* profile:

- **Lane A — operator manual-add (always on).** Oliver drops a connector/MCP URL or "I keep seeing X connector" → it
  goes straight to the **strict safety gate**, then the quick pass. Highest value, zero reachability risk. *(Worked
  example used Lane A: operator-picked the DataForSEO MCP.)*
- **Lane B — AI-surface scan.** WebSearch / Perplexity Sonar (`reference_perplexity_sonar_only`): *"best / newest MCP
  servers or connectors for Claude/ChatGPT in {use}; adoption, maintenance, who publishes them."* → candidate list +
  provenance.
- **Lane C — connector directories + open MCP indexes.** The official MCP registry (`registry.modelcontextprotocol.io`),
  GitHub's MCP Registry (`github.com/mcp`), `awesome-mcp-servers`, Smithery, PulseMCP, the OpenAI/GPT connector
  directory, vendor "works with Claude/ChatGPT" pages. **JS-heavy directories escalate to Claude-in-Chrome or
  host-side — never accept a silent empty WebFetch** (`feedback_verify_substrate_and_escalate_webfetch`).
- **Lane D — expansion.** From a keeper: the publisher's other connectors, the registry's "related" entries,
  "alternatives to," notable forks.

> ⚠️ **Lane reachability note (`[OR-5]` build, 2026-06-20 — no silent skip).** The **Claude connector-registry MCP**
> (`mcp__mcp-registry__search_mcp_registry`), named in the handoff as a Lane-C surface, returned **empty in-session**
> even for ubiquitous connectors (slack/github/gmail) — it is logged here as a **currently-unreachable lane, NOT
> silently substituted** (`feedback_verify_live_not_vault_and_no_silent_skips`,
> `feedback_consult_reference_memories_before_infrastructure_claims`). The working lanes used were **WebSearch**, **web
> fetch over the open MCP indexes / vendor docs / GitHub**, and **Claude-in-Chrome** for JS-heavy directories. Re-probe
> the registry MCP on the next run before relying on it.

**Fresh + growing read (§4), connector-flavored.** Recency = last release / "new" registry badge. **Velocity** =
adoption + maintenance cadence (registry installs, GitHub stars/commits slope, vendor-published vs community). Saturation
penalty = how many maintained equivalents already exist for the same job. **No undefended zeros** — any "abandoned /
nobody uses this / no equivalents" reading needs ≥2 sources + an adversarial check
(`feedback_no_undefended_zeros_enumerate_sources`). **Heavy/deep inspection runs host-side or in Chrome, not the 45s
Cowork sandbox**, failing loud about every limitation in the headline (`feedback_heavy_collection_hostside_not_cowork`).

---

## §11 — The STRICT safety + trust gate (`safety-trust-strict`) — the genuinely new logic this profile adds

**This gate RUNS — it is not a description.** It executes on **every** `mcp-connector` candidate **before the quick
pass files anything and before any wiring into an account.** Nothing is wired unvetted. **Every rejection is logged with
a reason code in `[[_safety-trust-gate-log]]` — no silent drops** (`feedback_verify_live_not_vault_and_no_silent_skips`).
Claude will **not** recommend wiring a connector whose scopes or behavior are unsafe, no matter how useful it looks.

**Why this is the highest bar in the program.** An open-source skill (`[OR-4]`) is passive code you read. A **connector
holds a live credential and acts on an account** — it can read your mail, write your data, move money, or be tricked
(via prompt injection / tool poisoning) into doing so. So the `[OR-5]` gate adds a check `[OR-4]` does not have: **the
account-scope / permission / data-access dimension.** A connector with perfectly clean code that simply **asks for far
more account access than its job needs** FAILS this gate even though it would clear `[OR-4]`'s bar.

### The five checks (run in order; first hard-fail short-circuits to REJECT)

1. **Legit & real? (provenance + impersonation/spoofing)**
   - Resolve the **canonical** publisher: first-party vendor (e.g. `stripe/…`, `dataforseo/…`) vs community. Confirm
     the registry entry, the repo, and the vendor's own "works with Claude/ChatGPT" page all point to the **same**
     owner.
   - **Server-spoofing / token-theft check (connector-specific):** a rogue server can register a **name nearly
     identical** to a trusted one to intercept tokens. A name collision with a popular connector by a *different* owner
     → `provenance-ambiguous` (HOLD) or `server-spoofing-risk` (REJECT) per evidence. (Kaspersky Securelist; Descope
     "server spoofing & token theft".)
2. **Account-scope & permissions? — THE load-bearing `[OR-5]` check (no checkmark without logged reasoning)**
   - **What EXACT scopes/permissions does it request?** Enumerate the OAuth scopes or API-key permissions. Map each to
     the connector's *stated function*. **Over-broad scopes are a REJECT even if the code is clean** — e.g. a connector
     that requests the full `https://mail.google.com/` scope ("read, compose, send, and **permanently delete** all your
     email") for what is really read-only work, when granular scopes (`gmail.readonly`, `gmail.modify`) exist. Reason
     code `excessive-account-scope` / `over-broad-oauth`. (Google scope docs; OWASP MCP07:2025; Descope "all emails /
     all files" overscoping.)
   - **Read vs write vs delete / data it shouldn't touch.** Does it write or delete by default when read-only would do?
     Can it reach data outside its job? A read-only need stored behind a read/write/delete token is a finding
     (`write-by-default-no-scoping`).
   - **Auth model.** OAuth 2.1 with PKCE + a **revocable** consent + granular per-resource permissions = good. Bare
     long-lived secret key / no granularity = worse. **Is a restricted / read-only key offered?** If the only auth is
     a full-power secret key with no restricted option, that is a hard limitation (`no-restricted-key-option`).
   - **Token handling + transport.** Where does the credential live — env var, plaintext, or a **remote server that
     sees your token**? Remote HTTP/SSE servers are a bigger surface than local stdio; a server bound to `0.0.0.0`
     ("NeighborJacking") or storing tokens in plaintext is a finding (`remote-token-exposure`). (Backslash Security
     NeighborJack; Descope token-theft.)
   - **The gate's output is a SCOPE PRESCRIPTION**, not a yes/no: it states *the exact least-privilege scope to grant*
     (e.g. "OAuth read-only consent" or "restricted key, resource X = Read, everything else = None").
3. **Safe? (malicious code / exfiltration / prompt-injection — connector-flavored)**
   - **Malicious code / install payload, data exfiltration** (silent BCC/forward/upload/beacon — the `postmark-mcp`
     case), **prompt-injection + tool-poisoning** (hidden instructions in *tool descriptions* the LLM ingests — "line
     jumping"), **cross-server shadowing** (a malicious co-installed server hijacking a trusted one's calls), and
     **rug-pull** (a trusted connector turning toxic in an update, e.g. `mcp-remote` CVE-2025-6514 RCE). Surface scan
     here; **deep audit host-side before wiring.**
4. **License / terms OK?** Usable license + vendor terms allow the intended use (incl. reselling a *service* built on
   it, if that's the money play). No license = REJECT for adoption (analysis note only). Record any rider.
5. **Maintained / alive?** Recent releases, responsive issues, real adoption, not archived. Abandoned/archived →
   `abandoned` REJECT unless there's a fork-and-own case.

**Depth rule.** The on-surface scan (registry entry, repo README/manifest, **declared scopes + tool list**, auth docs,
transport) runs here. **A deep line-by-line audit of the connector's code/tool-descriptions runs host-side and is
required before any connector is wired.** A candidate that passes the surface scan but hasn't had its code deep-read is
**PASS-for-filing-the-analysis-note** but **HOLD-for-wiring** — the note says "deep-read + scope-restrict before wiring."

### Verdict states (logged for every candidate)

| Verdict | Meaning | What happens |
|---|---|---|
| **PASS** | clean on all five at the strict bar (surface-safe; deep-read flagged; least-privilege scope prescribed) | proceed to quick pass → teardown → integration-map routing |
| **PASS-with-restricted-scope** | legit + safe **only if** wired with a restricted/read-only scope; the default surface is too broad | filed **with a mandatory scope prescription**; the recommendation is conditional on least-privilege wiring |
| **HOLD** | needs host-side deep-read, provenance disambiguation, or a scope clarification | logged; surfaced to operator with exactly what's needed; **nothing filed as wired** |
| **REJECT** | a hard fail on any check (incl. **over-broad account scope**, even with clean code) | logged with a **reason code**; **never recommended for wiring**; the rejection is the record |

### Reason codes (safety-gate log) — `[OR-5]` adds the account-scope family

| Reason code | Meaning | New for `[OR-5]`? |
|---|---|---|
| `excessive-account-scope` | requests far broader account access than its function needs | **NEW (the OR-5-distinct reject)** |
| `over-broad-oauth` | over-broad OAuth scopes (e.g. full-mailbox r/w/delete for read-only work) | **NEW** |
| `write-by-default-no-scoping` | writes/deletes/moves money by default; no read-only/restricted path | **NEW** |
| `no-restricted-key-option` | only a full-power secret key; no restricted/read-only key offered | **NEW** |
| `remote-token-exposure` | remote server holds the token / plaintext token / `0.0.0.0` bind | **NEW** |
| `server-spoofing-risk` | name collision / impersonation enabling token interception | **NEW (connector form of typosquat)** |
| `data-exfiltration` | silent data egress (BCC/forward/upload/beacon) | shared w/ `[OR-4]` |
| `prompt-injection-trap` | hidden/scope-widening/exfil instructions in tool descriptions (tool poisoning) | shared w/ `[OR-4]` |
| `malicious-code` | malicious code / install-time payload / rug-pull RCE | shared w/ `[OR-4]` |
| `provenance-ambiguous` | look-alike/community fork; canonical not confirmed → HOLD | shared w/ `[OR-4]` |
| `no-usable-license` · `abandoned` · `out-of-category` · `already-wired` | as in `[OR-4]` (`already-wired` = the connector form of `already-in-library`) | shared |

### Connector threat taxonomy the gate screens for (cited — June 2026)

The strict gate is built against documented MCP/connector attack classes, not abstractions:
**tool poisoning / "line jumping"** (Trail of Bits) · **NeighborJacking** — `0.0.0.0`-bound servers (Backslash Security,
June 2025) · **cross-server shadowing** (Elena Cross, "The S in MCP Stands for Security") · **server spoofing + token
theft** (Kaspersky Securelist) · **the "Lethal Trifecta"** — over-privileged Supabase `service_role` MCP data leak
(General Analysis, June 2025; Simon Willison) · **rug-pull** — `mcp-remote` RCE, CVE-2025-6514 · **over-scoping** —
"MCP servers often request expansive scopes ('all emails', 'all files')" (Descope, OWASP MCP07:2025). Full citations in
`[[_safety-trust-gate-log]]`.

**The product/offer profile does not run this gate** — it is `mcp-connector` / `oss-skill` config. `[OR-4]` runs the
**`safety-trust`** bar (code safety); `[OR-5]` runs **`safety-trust-strict`** = that bar **plus** the account-scope
family above.

---

## How the standard teardown maps onto a connector (engine reused, fields filled the connector way)

The engine's §6.1 fields are filled as follows for a vetted `mcp-connector` keeper (everything else — §6.2
build/buy/use, §6.3 money, §6.4 visuals, §7 level-up, §8 score — is **unchanged engine logic**):

- **Why it works / rare-and-valuable core** → what capability wiring it into Claude/ChatGPT gives Oliver that he
  doesn't have (e.g. live data inside the agent loop).
- **How they likely build it** → the actual architecture (MCP server → vendor API; tools exposed; auth/transport).
- **Replication requirements** → what it'd take to rebuild the connector vs. wire the official one — feeds
  **build-vs-buy-vs-use-as-is**.
- **The benefit** → concretely which of Oliver's domains/projects it enhances (the §9.1 wiring targets) — e.g.
  client-SEO (`project_priority_client_seo_traffic`), market-intelligence, the website-factory.
- **How to integrate it into Oliver's setup** → the **integration plan + the exact least-privilege scope** (the
  integration-map deliverable): which client, what scope/key, transport, what to watch, deep-read-before-wiring.
- **The level-up** → a better/own version where worth it (a thin wrapper, a vault-aware connector, an aggregator) —
  standard §7 framework + hard buildability gate.
- **Money play (only if clear)** → spark idea-factory **only** when wiring the connector into Oliver's accounts opens a
  **stated, terms-compatible** revenue path (e.g. a Keelworks service the connector powers); otherwise integration-map
  only.

**Build-vs-buy-vs-use, connector flavor:** **use-as-is** (wire the official connector, scoped) · **rebuild** (write our
own better/safer connector) · **skip**. "Just wire it (scoped) and earn" is a valid winning answer (CLAUDE.md Core
Principle: *when in doubt, ship*).

---

## Integration-map + money-spark routing (§9 / §9.1)

A vetted **PASS** (or **PASS-with-restricted-scope**) keeper produces, in order:

1. **Analysis/teardown note** → `opportunity-radar/teardowns/teardown-<date>-<slug>.md` (the full engine output).
2. **Vault integration map entry** → `05_shared-intelligence/connector-integration-map.md` (the capability home for
   connectors): the at-a-glance list of *what's wired / proposed*, the **exact scope it holds**, what it unlocks, and
   which domains/projects it serves. **This is the `mcp-connector` analogue of the `[OR-4]` `tools/` library** — but
   scope-centric, because connectors touch accounts.
3. **Capability-home tool-note** → `05_shared-intelligence/tools/tool-<slug>.md` (the tools-as-notes entry,
   `status: noted` until the operator wires it) — with the integration plan + scope prescription.
4. **Registry roll-up line** → `[[build-it-better-candidates-registry]]` (+ its `.data.yaml`), `profile: mcp-connector`.
5. **Safety-gate log row(s)** → `[[_safety-trust-gate-log]]` (the PASS/PASS-with-restricted-scope, plus every REJECT
   from the same run).
6. **Wiring** → **operator action.** The note proposes the connector + the least-privilege scope; **Oliver wires it.**
   The engine never connects an MCP to an account.
7. **idea-factory spark** → **only** on a clear, terms-compatible money play (e.g. a Keelworks service the connector
   powers). A "build it better" angle alone is **not** a money play. Route via `idea-factory-prompter` (Path-4,
   Idea-stage, one-Active cap, `decisions.md` dedup, no auto-promote past Research).

**§9.1 vault wiring is non-negotiable.** Every note cross-links (slug-only `[[wikilinks]]`) to: a **parent context**
(the integration map, the registry, or the spec) + **≥1 peer** + the **domains/projects/skills/ideas it enhances**
(e.g. ``market-intelligence``, ``competitor-deep-research``, the EV/S&H/Keelworks projects, related connectors). An
island note is a stewardship fail (Vault Stewardship rule 4, `feedback_check_folder_structure_before_writing`).

---

## Worked example (Lane A, end-to-end)

`[[teardown-2026-06-20-dataforseo-mcp]]` — the full profile run on the **official DataForSEO MCP server**
(`dataforseo/mcp-server-typescript`): strict gate **PASS** (with a logged account-scope analysis: API-credential auth,
read-only data modules, `ENABLED_MODULES` least-privilege, billing-exposure caveat) → quick pass → deep dive →
level-up → score → integration-map routing (`[[connector-integration-map]]` + `[[tool-dataforseo-mcp]]` + registry row)
→ **idea-factory spark** (a clear client-SEO money play). The same run logged **Stripe MCP** as
**PASS-with-restricted-scope** (gate-log only), a **net-new account-scope REJECT** (a Gmail/email connector requesting
full `https://mail.google.com/` for read-only work), and **freshly re-cited** the `postmark-mcp` (exfiltration) and
`SANDWORM_MODE` (typosquat + prompt-injection) precedents. See `[[_safety-trust-gate-log]]` for the gate run evidence.

---

## Adding the next connector in this profile (the duplicability contract)

A second `mcp-connector` source must run from **config alone** — no `SKILL.md` edit, no edit to *this* file's gate
logic (only new log/teardown/tool notes + an integration-map entry + a registry row). If the engine or finder needs
editing to vet/teardown another connector, the profile boundary leaked
(`feedback_no_half_finished_build_for_reuse`).

## Related
- **Parent / authority:** `[[spec-opportunity-teardown-engine]]` (§2, §9.1, §11, §15) · `[[SKILL]]` (the frozen engine) · `[[profiles]]` (index, Profile #4)
- **Finder half:** `[[finder-config-profiles]]` Profile #4 (`mcp-connector` lane-set — keep slug in sync)
- **Sibling profile (shared gate pattern, not the profile):** `[[profile-open-source-skill]]` (`oss-skill`, `[OR-4]` — code safety; this profile adds the account-scope bar on top)
- **Outputs:** `[[_safety-trust-gate-log]]` · `[[teardown-2026-06-20-dataforseo-mcp]]` · `[[tool-dataforseo-mcp]]` · `[[connector-integration-map]]` · `[[build-it-better-candidates-registry]]`
- **Pattern (shared w/ [OR-4], stricter here):** `[[pattern-safety-vetted-capability-ingestion]]` (promote at [OR-5]; account-scope bar is the [OR-5] increment)
