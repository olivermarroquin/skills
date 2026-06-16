---
type: skill-reference
skill: market-intelligence-engine
created: 2026-06-16
updated: 2026-06-16
tags: [skill-reference, market-intelligence, output-contract, gap-plan]
---

# Output contract B — Per-client gap-to-action plan

**Purpose:** the instance. For a given client: current score per arena, gap vs the perfect profile,
prioritized action list with routing.

**Produced by:** `multi-source-synthesis` (client-driven shape), fed by this engine's Phase 11.

---

## Required sections

### 1. Routing legend

```
[WF]  = website-factory (page/content build)
[LSG] = local-seo-growth (GBP, reviews, citations, paid)
[T/D] = tool or data change (new tool, data collection, credential)
```

### 2. Per-client score card (one section per client)

For each client in the run config:

#### Score vs perfect profile table

```
| Arena | Client score | Perfect profile threshold | Gap | Priority |
|---|---|---|---|---|
| V1 | 0 (0 top-3) | >=73 top-3 | full build needed | high |
| ...  |              |                          |     |          |
```

#### Prioritized action list

Ordered by leverage (highest-impact gaps first). Each action includes:
1. **What** — the specific action.
2. **Route** — `[WF]`, `[LSG]`, or `[T/D]`.
3. **Why top** — what makes this higher leverage than the next item.
4. **Depends on** — any prerequisite actions.

### 3. Cross-client priority summary table (if >1 client)

```
| # | Action | Client(s) | Route | Why top |
|---|---|---|---|---|
```

### 4. High-leverage findings (plain language)

Two or more findings stated plainly for operator consumption. Example from the electrician run:
- "7 competitors run 10+ Google ads; both clients run zero — threat + opportunity."
- "S&H GBP is geocoded to Iowa — structural lock-out of all NoVA local pack results."

### 5. Routing handoffs

Which downstream programs consume which actions:
- `website-factory` ← page/content ideas.
- `local-seo-growth` ← GBP optimization, review engine, citations, paid program.
- Tool/data changes ← credential acquisition, tool subscriptions.

Coordinate, don't duplicate.

### 6. New gaps surfaced during synthesis

Any new DG-# entries discovered while writing the gap plan. Appended to `_data-gap-register.md`.

### 7. Gate verdict

Two layers kept honestly distinct:
1. **Producer-side self-check** (sub-agent, dispatched by producer chat) — runs G-market-intel
   checks, explicitly NOT the independent gate.
2. **Independent G-market-intel review** (separate external pass) — the actual gate.

A run may not mark its own gate PASS. See standing rule from MI-3b lessons — see `[[mi3-limitations-and-lessons-2026-06-14]]` §L2.

---

## Validation rules (G-market-intel enforced)

- Every client score traces to the same sourced cells as Output A (check #1).
- Gap sections are non-empty (check #3).
- No undefended zeros in client score tables (check #4).
- Routing present on every action item.
- High-leverage findings present and grounded in data.

---

## Worked example

See `worked-example-electrician.md` — the [MI-4] Output B (`mi4-per-client-gap-plans-2026-06-16.md`)
is the canonical first instance: EV Electric (6/40) + S&H Contracting (8/40) gap plans with
7-item cross-client priority summary.
