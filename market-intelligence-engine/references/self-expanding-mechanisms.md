---
type: skill-reference
skill: market-intelligence-engine
created: 2026-06-16
updated: 2026-06-16
tags: [skill-reference, market-intelligence, self-expanding, data-gap-register]
---

# Self-expanding mechanisms — `market-intelligence-engine`

The operator's directive: *better data = better results; leverage more tools that give valuable insight.*
Discovery is a **standing phase, not a fixed checklist.** Five mechanisms keep the engine growing.

---

## 1. Living data-gap register

**Location:** `_data-gap-register.md` in the market-intelligence handoff folder.

- Every run **appends** newly-spotted gaps: "things the leaders expose that our schema has no field
  for yet."
- **Never reset.** The register is append-only and cumulative.
- Each entry includes: gap ID (DG-#), description, which arena it affects, discovery source,
  proposed data source, status (open / closed / deferred), and closing evidence.
- The engine is **structurally forbidden from declaring full coverage** — enforced by G-market-intel
  check #3 (data-gap + tool-gap sections must always be non-empty).

**Integration:** Phase 9 (gap-discovery pass) appends new entries. Phase 12 (residuals queue)
references open entries.

## 2. Gap-discovery pass (Phase 9)

Not "check these N gaps" but "look at what the winners measure/do that our current arena schema
can't capture, and propose new fields/arenas."

- The schema grows itself over time.
- New fields may become new arenas or sub-dimensions of existing arenas.
- Each proposed field includes: what it measures, why it matters (which leader exposed it),
  proposed data source, and estimated effort to collect.

## 3. Emerging-tool discovery mode

**Owner:** `seo-tooling-landscape-research` v2.0 (discovery mode, added by [MI-6]).

- Recurring scan: deep-research + Product Hunt + AEO/SEO blogs + practitioner YouTube + Reddit.
- Evaluates candidates against the tool-eval rubric (value / time-saved / cost / fit).
- Outputs: `tool-*.md` notes in `03_domains/seo/tools/` + TG-rows in `_data-gap-register` +
  `mi-arena-source-checklist` updates.
- Catches tools not yet on the standard lists (the AEO/GEO space turns over monthly).

**Engine integration:** Phase 9 routes tool-gap findings to this mode. The engine reads discoveries
but does not re-implement scanning.

## 4. Operator tool-intake pipeline

**Owner:** `seo-tooling-landscape-research` v2.0 (intake mode, added by [MI-6]).

- When the operator finds a tool (Facebook, a creator demo, a random tab), they drop the link / name /
  video URL into `00_inbox/tools-pending/` **or** paste it in any chat with "digest this tool."
- The system runs `vis-extraction` if it's a video/article, scores against the tool-eval rubric,
  writes a `tool-*.md` note, and gives an adopt/skip recommendation.
- Manual discovery becomes structured intel instead of a forgotten tab.

**Engine integration:** always-on / on-demand. The engine benefits from newly-adopted tools on
subsequent runs.

## 5. Scheduled cadence ([MI-8])

- **Monthly:** emerging-tool scan (mechanism #3).
- **Quarterly:** full data-gap + arena re-score (dovetails with `local-seo-growth` G5 quarterly refresh).
- **Always-on:** tool-intake (mechanism #4).

Both cadences append to the register + ping the operator with findings. The engine compounds
research across runs rather than being one-and-done.

---

## Structural enforcement

G-market-intel check #3 prevents the engine from ever claiming full coverage:

> **The data-gap + tool-gap sections are non-empty** — the engine may never claim full coverage;
> it must always answer "what don't we know yet?"

A run that declares "no gaps remain" fails the gate.
