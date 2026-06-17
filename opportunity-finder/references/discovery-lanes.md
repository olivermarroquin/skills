---
type: skill-reference
skill: opportunity-finder
version: 1.0
created: 2026-06-17
updated: 2026-06-17
tags: [skill-reference, opportunity-finder, discovery-lanes, lanes, provenance, sonar, web-fetch, claude-in-chrome]
---

# Discovery lanes (§3) — method, template, and provenance per lane

Each lane emits a **candidate + a provenance note**. The provenance is non-negotiable (§3 + SKILL discipline #7): a
candidate with no provenance is not a candidate. The candidate shape every lane produces:

```yaml
- name: <product/offer name>
  url: <canonical url>            # used as the dedup key (normalized: strip utm/query, lowercase host)
  one_line: <what it is, one plain sentence>          # enough to dedup + decide "score it?"
  raw_signal:                     # the cheap evidence the scorer (§4) will read — collect what the lane surfaces
    launch_or_first_seen: <date or "unknown">
    velocity_hint: <upvotes / review-count / rank / stars / "new badge" / press cadence — whatever the lane gives>
    crowding_hint: <how many similar things the lane surfaced alongside it>
  provenance:
    lane: <A | B | C | D>
    source: <exact source: "Perplexity Sonar (sonar-pro)" | "Product Hunt /topics/ai" | "AppSumo browse" | "expansion from <keeper>">
    date: <YYYY-MM-DD>
    method: <"sonar query" | "web_fetch" | "Claude-in-Chrome (JS-escalated)">
```

The lane-set that runs is **profile config** (`finder-config-profiles.md`). Below are the v1 lanes for the default
product / AI-content profile.

---

## Lane A — operator manual-add (always on; lives in the engine, not here)

Oliver drops a product/URL/"I keep seeing X" → straight into the `opportunity-teardown` quick pass. The finder does
**not** implement Lane A — it's the engine's intake. The finder's relationship to Lane A: when the operator picks a
keeper from the finder's shortlist, that keeper is handed to the engine **exactly as a Lane A item would be** (same
candidate shape above). Documented here only so the lane numbering matches the spec.

---

## Lane B — AI-surface scan (Perplexity Sonar)

**Method.** Ask the AI surface "what's newly launched / growing fast in {category}" and parse named products + the
"why it's growing" hint into candidates. Sonar returns cited synthesis, so it doubles as a recency/velocity signal
source for §4.

**Reachability.** Confirmed reachable from the Cowork sandbox (`reference_ai_surface_reachability_from_cowork`,
`reference_perplexity_sonar_only`). Invoke:

```bash
cd /sessions/<session>/mnt/workspace/second-brain-tier3/automation/scripts
python3 perplexity_sonar.py "<the lane prompt below>"
```

**Prompt template (parametrized by `{category}` + `{window}`):**

> "List 8–12 **specific, named** {category} products or tools that **launched or started growing fast in the last
> {window}** (e.g. 12 months). For each: the product name, its URL, one sentence on what it does, any signal it's
> *growing* (funding, press, rank climb, fast-rising user/review counts, frequent shipping), and roughly how crowded
> that niche is (how many direct competitors). Prefer genuinely newer/rising tools over established incumbents. Cite
> sources. If you are unsure a tool is real or current, say so rather than inventing one."

**Indie prompt template (run ALONGSIDE the trending one, not instead — gives the trending-vs-indie contrast):**

> "List 8–10 **newly launched, under-the-radar, INDIE** {category} tools (last {window}) that have **few direct
> competitors or occupy a narrow niche** — the kind most people haven't heard of yet, NOT the popular/trending ones.
> For each: name, URL, one sentence, an **early-traction** signal (early adoption climbing, not mass scale), and why
> the niche is relatively uncrowded. Cite sources. If unsure a tool is real, say so."

The two pulls feed the **trending-vs-indie comparison** (`_trending-vs-indie-*.md`): the trending pull shows demand, the
indie pull shows headroom. **Saturation/headroom is the contrast axis** (see `fresh-growing-scoring.md`).

**Anti-hallucination.** Sonar can name plausible-but-fake tools. Every Lane-B candidate's `url` is **confirmed
resolvable** (a quick `web_fetch` HEAD-equivalent or a second Sonar/WebSearch cross-check) before it enters the cache.
Unconfirmed names are logged to `_rejection-log.md` with reason `unverified-existence`, not shortlisted.

**Provenance.** `lane: B`, `source: "Perplexity Sonar (sonar-pro): '<category>' scan"`, `method: "sonar query"`.

**Fail-loud.** If the Sonar key/endpoint is unreachable, say so in the headline ("Lane B DID NOT RUN — Sonar
unreachable") — do not silently substitute WebSearch and pretend it was Lane B; if you fall back, label it.

---

## Lane C — marketplace / launch-board pull

**Method.** Fetch a launch board / marketplace listing for {category}, parse the listed items into candidates with
their rank/upvote/review signals.

**Default sources (product / AI-content profile):**
- **Product Hunt** — topic/leaderboard pages (e.g. `/topics/artificial-intelligence`). **Note: PH serves real SSR
  content to `web_fetch`** (verified 2026-06-17) — the "Recent launches" + "Trending" blocks are the fresh signal; the
  "Highest rated" list is incumbents. Use `?order=recent_launches` for the indie/newest pull.
- **AppSumo** — **use the SEARCH URL `https://appsumo.com/search/?query=<terms>`** (verified working via Claude-in-Chrome
  2026-06-17). ⚠️ **Do NOT use `/software/<category>/` — that path 404s.** JS-rendered → **escalate to Chrome.**
  AppSumo is the **richest indie/LTD source** found so far (review counts = a cheap traction signal); bias indie runs here.
- **Gumroad** — `gumroad.com/discover?query=<terms>`. **JS-rendered** — `web_fetch` returns a meta/shell only;
  **escalate to Chrome** for listings.
- **Indie-leaning (v1):** AppSumo search, Product Hunt `recent_launches`. **v1.1 (documented, not built):** indie
  directories (e.g. indie-hackers product lists, "tiny tools" roundups), Gumroad bestsellers via Chrome.

**JS escalation (mandatory).** Product Hunt and AppSumo are client-rendered — a `web_fetch` returns a shell with no
listings. On any fetch that returns a shell / loading state / no item data:
1. Do **not** retry the fetch or guess from the partial content.
2. Escalate to Claude-in-Chrome: `mcp__Claude_in_Chrome__navigate` to the listing URL, then
   `mcp__Claude_in_Chrome__get_page_text` to read the rendered listings. (Load these via ToolSearch first.)
3. If Chrome is not connected, **stop and tell the operator in the headline** that Lane C needs Chrome for that source —
   never log an empty fetch as a "residual" (`feedback_verify_substrate_and_escalate_webfetch`).

**ToS/robots-aware.** Respect each source's terms; honor `web_fetch` restrictions (no fallback fetching via
bash/python/curl). Capture provenance for every candidate.

**Provenance.** `lane: C`, `source: "<board> <page>"`, `method: "web_fetch"` or `"Claude-in-Chrome (JS-escalated)"`.

**Fail-loud.** Any source that couldn't be read (JS shell + Chrome unavailable, fetch blocked, rate-limited) is named
explicitly in the dry-run headline as a lane limit — never buried.

---

## Lane D — expansion from a keeper

**Method.** Given a keeper (a product the operator liked, or a high scorer), find adjacent/similar items:
- its **direct competitors** ("alternatives to {keeper}", "{keeper} vs") via Sonar + a fetch,
- the **maker's other products** (same company/creator),
- the **category neighbors** one step out.

Each expansion candidate carries `provenance.source: "expansion from <keeper>"` and `lane: D`. Expansion is how the
funnel compounds without new top-level scans — a single keeper seeds the next batch.

**Run via** `expand` mode. Same dedup + score + shortlist as `discover`.

---

## Deferred lanes (v1.1 — documented, not built)

| Lane | Source | Why deferred |
|---|---|---|
| Ad-library scan | Meta Ad Library, TikTok Creative Center | ToS-sensitive + heavily JS; needs Chrome + a ToS pass. |
| App-store charts | App Store / Play "top/trending" | JS + region-specific; needs Chrome + a parser. |
| Marketplace movers | Amazon Movers & Shakers, Etsy trending | JS + anti-bot; host-side or Chrome only. |

When built, each is added here with its method + escalation note and switched on in the relevant profile's `lanes:`
list — **no engine change** (that's the general-purpose test).

## Related
- `[[SKILL]]` (the engine that runs these lanes) · `[[fresh-growing-scoring]]` (what scores the candidates) ·
  `[[finder-config-profiles]]` (which lanes run per profile) · `[[dedup-rejection-sourceyield]]`
- spec `[[spec-opportunity-teardown-engine]]` §3
