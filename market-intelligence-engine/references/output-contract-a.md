---
type: skill-reference
skill: market-intelligence-engine
created: 2026-06-16
updated: 2026-06-16
tags: [skill-reference, market-intelligence, output-contract, perfect-company-profile]
---

# Output contract A — Field-level perfect company profile

**Purpose:** the reusable asset. Per-field, cached, reused per client. The field-level market data
is identical for all clients sharing a field; only the per-client gap plan (Output B) differs.

**Produced by:** `multi-source-synthesis` (cross-cluster shape), fed by this engine's Phase 10.

---

## Required sections

### 1. Composite at a glance

Table: all scored competitors + clients, ranked by composite (Sigma/40), with arena(s) led noted.

```
| Rank | Competitor | V1 | V2 | V3 | V4 | V5 | M1 | M2 | A1 | Sigma/40 | Arena(s) led |
|---|---|---|---|---|---|---|---|---|---|---|---|
```

### 2. Per-arena perfect profile (8 sections, one per arena)

For each arena (V1, V2, V3, V4, V5, M1, M2, A1):

1. **Winning attribute observed** — what the arena leader actually does.
   - Must name the **competitor** and the **real number** (e.g., "Root Electric: 916 ranked keywords,
     73 top-3 positions, $10.5K ETV").
2. **Target threshold** — the number/state needed to beat the current leader.
   - Expressed as a concrete metric (e.g., ">=73 NoVA top-3 / ~$10K ETV").
3. **Why it wins** — the mechanism (e.g., "deep service x city matrix built on WordPress with
   inter-linked hub pages generating topical authority").
4. **Page/content ideas + new-page ideas** it implies for a build.
   - Routed to `[WF]` website-factory or `[LSG]` local-seo-growth.

### 3. Synthesis — the unbeatable company profile

The union of all arena leaders' strengths. Structured as:
- **Foundation half** — what the organic/authority leader brings.
- **Front-of-house half** — what the reviews/conversion/local leader brings.
- **Open arenas** — arenas nobody currently dominates (opportunity spaces).

### 4. Consumable idea lists

Two separate sections, each with routing tags:
- **Website-factory ideas** → `[WF]` (page types, content clusters, landing pages, conversion elements).
- **Local-SEO-growth / authority actions** → `[LSG]` (GBP, review engine, citations, paid program).

### 5. Limitations (mandatory headline section — standing rule L0)

**Must appear as a headline-level section, not buried.** Contents:
- Data gaps remaining (with DG-# references to `_data-gap-register`).
- Tool gaps (tools needed but not yet available).
- Substrate limitations hit (what couldn't be collected and why).
- Coverage threshold: which arenas are below full coverage.

### 6. Gate verdict

Deferred to Output B or run as combined gate. References G-market-intel checks 1-8.

---

## Validation rules (G-market-intel enforced)

- Every arena score traces to a cited source (check #1).
- Every perfect-profile attribute names the competitor (check #2).
- Limitations section is non-empty (check #3).
- No undefended zeros in the composite table (check #4).
- Source checklist filled per arena (check #5).
- Adversarial completeness pass documented (check #6).
- Completion-vs-plan ledger present (check #7).

---

## Worked example

See `worked-example-electrician.md` — the [MI-4] Output A (`mi4-perfect-company-profile-2026-06-16.md`)
is the canonical first instance of this contract.
