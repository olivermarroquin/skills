---
name: reference-library
version: 1.0
description: >
  Domain-agnostic curated-library engine. Manages two intake lanes (high-performing full dossier +
  design-only swipe), cache/dedup, standing ingestion queue, operator review gate (training-mode
  default), and catalog-graduation workflow. The engine is config-driven — website-design inspiration
  is the first instantiation; any future swipe file (copywriting, app UIs, decks, cold emails) is
  created from a config profile alone, no code changes. Use this skill whenever someone says "add
  [site/item] to the library," "ingest this reference," "check what's in the library," "graduate
  this pattern to the catalog," or any time a captured reference needs to be filed, deduped, or
  promoted through the curation pipeline.
composes-with: [site-capture-engine, design-fingerprint, design-emulation-verify, design-pattern-synthesis, reference-finder]
---

# Reference Library (v1.0)

> **v1.0 (2026-06-18)** — Initial build. The "collect sites I like and reuse them" system Oliver
> described on 2026-05-23, operationalized. Domain-agnostic curated-library engine with two intake
> lanes, cache/dedup (VIS discipline), standing queue, review gate, catalog-graduation, and
> config-driven profiles. Website-design inspiration is the default profile; a 2nd instantiation
> (copywriting swipe file) is documented as proof of reuse. Composes [DI-1] site-capture-engine +
> [DI-2] design-fingerprint upstream; feeds [DI-4] design-emulation-verify + [DI-6]
> design-pattern-synthesis + [DI-7] reference-finder downstream.

A reusable skill that manages a **curated reference library** — the pipeline from "I found
something worth keeping" through filing, dedup, review, and eventual catalog-graduation. The
engine handles intake, the config defines *what* kind of library.

**Composes with:**
- **Upstream:** `site-capture-engine` (v2.1+) — captures the raw artifact; `design-fingerprint`
  (v1.0) — turns the capture into a structured dossier/note
- **Downstream:** `design-emulation-verify` ([DI-4]) — uses filed dossiers as comparison baselines;
  `design-pattern-synthesis` ([DI-6]) — reads trait sidecars for cross-corpus analysis;
  `reference-finder` ([DI-7]) — discovers new candidates and feeds the intake registry
- **VIS discipline:** cache/dedup + standing queue + review gate (training-mode default) patterns
  borrowed from `vis-extraction` (v1.2)

---

## When to use

Trigger this skill when:
- "Add [site/item] to the library"
- "Ingest this reference into [library-name]"
- "Check if [site] is already in the library"
- "What's in the [high-performing / design-only] library?"
- "Graduate [pattern] to the catalog"
- "What's queued for ingestion?"
- Any time a captured reference needs to be filed, deduped, reviewed, or promoted

Do **not** use this skill for:
- Capturing a site (use `site-capture-engine`)
- Fingerprinting a capture into a dossier (use `design-fingerprint`)
- Discovering new references to add (use `reference-finder` / [DI-7])
- Verifying a build against a reference (use `design-emulation-verify`)

---

## Core concepts

### Two intake lanes

Every library profile defines two lanes with different bars and output formats:

| Lane | Bar | Upstream skills | Output format | Destination |
|---|---|---|---|---|
| **High-performing** | Must clear ALL inclusion criteria (e.g., rankings + CWV + content depth + visual quality for website-design) | `site-capture-engine` → `design-fingerprint` (depth: full) | Full dossier + trait sidecar | `<library-root>/high-performing/` |
| **Design-only (swipe)** | Must clear the visual/quality bar only; performance not verified | `site-capture-engine` (lightweight) → `design-fingerprint` (depth: light) | Light note + trait sidecar | `<library-root>/design-only/` |

The lane split exists so the methodology doesn't accidentally treat a beautiful-but-non-performing
reference as a performance reference. Each lane has its own bar defined in its folder `_README.md`.

### Cache / dedup (VIS discipline)

Before capturing or filing any reference:

1. **Check the library.** Grep `<library-root>/` for the domain/identifier. If a dossier or note
   already exists, surface it: "This reference already exists at `<path>`. Options: (a) skip,
   (b) update the existing entry, (c) create a new version with a date suffix."
2. **Check the ingestion queue.** Grep `<queue-file>` for the domain/identifier. If it's already
   queued, note its position.
3. **Never silently re-capture or overwrite.** Calibrated work (operator-reviewed dossiers) is
   expensive to reproduce. Dedup before intake, always.

### Standing ingestion queue

Each library profile has a standing queue file (e.g., `_ingestion-queue.md`) that tracks:
- Items waiting to be captured and filed
- Items in progress
- Items completed (struck through + linked to the resulting dossier/note)

The queue is a working document. Items are appended as they're discovered, struck through as
they're completed. The queue feeds capture; capture feeds this skill.

### Candidates registry (intake registry)

The registry is the structured intake funnel that [DI-7] reference-finder feeds into. Status flow:

```
candidate → vetted → queued → ingested → in-library
```

| Status | Meaning | Who moves it |
|---|---|---|
| `candidate` | Discovered, not yet evaluated | [DI-7] reference-finder or operator manual-add |
| `vetted` | Evaluated against the library bars, scored | [DI-7] vetting pipeline |
| `queued` | Approved for ingestion, waiting in the queue | Operator gate |
| `ingested` | Capture + fingerprint complete, dossier/note drafted | This skill |
| `in-library` | Filed, reviewed, stamped | This skill (after operator review) |

**Registry location:** `<library-root>/candidates-registry.md` (one per library profile).
Until [DI-7] ships, the registry is fed by hand (operator + this skill's design-only lane).

**Registry entry format:**
```markdown
| Domain | Status | Lane | Sector | Discovered | Source | Notes |
|---|---|---|---|---|---|---|
| example.com | candidate | high-performing | electrical-services | 2026-06-18 | operator | looks strong |
```

### Cross-sector tags

Every filed dossier/note carries frontmatter tags for cross-corpus analysis:
- `sector:` — industry/domain (e.g., `electrical-services`, `hvac`, `saas`, `fintech`, `agency`)
- `archetype:` — design archetype (e.g., `dark-hero-cta`, `light-minimal`, `dashboard-dense`)

These tags enable [DI-6] synthesis to slice the library by sector and [DI-7] to build coverage maps.

### Review gate

**Training-mode (default):** Every new dossier/note is surfaced to the operator for approval before
being stamped with its final status (`verified` for high-performing, `captured` for design-only).
The dossier is written to disk as `status: draft`, then promoted after operator review.

**Auto mode:** Only on explicit operator say-so (`--review auto`). The dossier is written and
stamped in one step. Use for batch ingestion of pre-vetted references where operator has already
approved the set.

### Catalog-graduation workflow

A pattern from any library entry becomes a catalog entry (`catalog/pattern-<name>.md`) only when:

1. **Used in a real build** — the pattern was applied in at least one client site, OR
2. **Verified via `design-emulation-verify`** — a working implementation passes the diff check

The graduation gate is encoded, not discretionary:
- The builder or verifier writes the catalog entry referencing the source dossier
- The catalog entry carries `verified-via:` frontmatter pointing to the dossier slug
- Premature graduation (no build use, no verification) is a defect — don't promote patterns
  the system hasn't proven

---

## Procedure

### Intake: filing a new reference

#### Step 0 — Dedup check

1. Grep `<library-root>/` for the domain/slug.
2. Grep `<queue-file>` for the domain/slug.
3. If found, surface to operator with options. Do not proceed without operator decision.

#### Step 1 — Determine lane

- If the reference has performance evidence (rankings, CWV, content depth) AND clears all
  inclusion bars → **high-performing lane**
- If the reference has visual quality only → **design-only lane**
- If unclear, ask the operator.

#### Step 2 — Verify upstream artifacts exist

- **High-performing lane:** requires a `design-fingerprint` full dossier (`dossier-<slug>.md` +
  `_traits-<slug>.yaml`). If not present, prompt: "Run `design-fingerprint` (depth: full) first."
- **Design-only lane:** requires at minimum a `design-fingerprint` light note
  (`inspiration-<slug>.md` + `_traits-<slug>.yaml`). If not present, prompt: "Run
  `design-fingerprint` (depth: light) first."

#### Step 3 — File the reference

1. Copy/move the dossier/note + trait sidecar to the appropriate library folder.
2. Verify frontmatter includes `sector:` and `archetype:` tags. Add if missing.
3. Set status:
   - Training mode → `status: draft` (pending operator review)
   - Auto mode → `status: verified` (high-performing) or `status: captured` (design-only)

#### Step 4 — Update the queue

1. In `<queue-file>`, strike through the entry and append `→ [[dossier-slug]]` or
   `→ [[inspiration-slug]]`.
2. If the reference was in the candidates registry, update its status to `in-library`.

#### Step 5 — Review gate

- **Training mode:** Surface the filed dossier/note to the operator. Present:
  - The dossier/note content (or a summary for batch)
  - The trait sidecar summary
  - Any caveats from the fingerprint analysis
  - Ask: "Approve as filed / request changes / reject?"
- On approval: bump status to `verified` / `captured`.
- On rejection: remove from library, note reason in queue.

### Graduation: promoting a pattern to the catalog

#### Step 1 — Identify the pattern

From any filed dossier/note, section 5 ("Patterns worth lifting") names patterns with
`→ catalog/<category>/<pattern-slug>` pointers. These are graduation candidates.

#### Step 2 — Verify the graduation trigger

One of:
- **Build use:** the pattern was used in a real client build (cite the project + the specific
  implementation)
- **Emulation verification:** the pattern was verified via `design-emulation-verify` (cite the
  verification report)

If neither trigger is met, do not graduate. Log the candidate for future graduation.

#### Step 3 — Write the catalog entry

Write `catalog/pattern-<name>.md` per the catalog `_README.md` format. Include:
- `verified-via:` frontmatter pointing to the source dossier
- `times-deployed:` starting at 1
- Real, paste-ready code spec
- Concrete "when to use" / "when NOT to use" conditions

#### Step 4 — Cross-link

Add a `→ graduated to [[pattern-<name>]]` note in the source dossier's patterns section.

---

## Config-driven design

The skill is domain-agnostic. All domain-specific content comes from a **config profile**. See
`references/library-config-profiles.md` for the full profile schema and instantiated profiles.

| What | Where it comes from | NOT hardcoded |
|---|---|---|
| Library root folder | Profile `library_root` | `inspiration/` |
| High-performing subfolder | Profile `high_performing_dir` | `high-performing/` |
| Design-only subfolder | Profile `design_only_dir` | `design-only/` |
| Catalog destination | Profile `catalog_dir` | `catalog/` |
| Queue file | Profile `queue_file` | `_ingestion-queue.md` |
| Registry file | Profile `registry_file` | `candidates-registry.md` |
| Inclusion bars | Profile `inclusion_bars` | The 4-bar test |
| Dossier template | Profile `full_template` | `dossier-template-full.md` |
| Light note template | Profile `light_template` | `dossier-template-light.md` |
| Upstream capture skill | Profile `capture_skill` | `site-capture-engine` |
| Upstream fingerprint skill | Profile `fingerprint_skill` | `design-fingerprint` |

To instantiate a 2nd library (e.g., a copywriting swipe file): create a new profile in
`library-config-profiles.md` with the appropriate folders, templates, and bars. No skill code
changes needed.

---

## Reference files

| File | Purpose |
|---|---|
| `references/intake-lane-contracts.md` | Two-lane intake contract: inputs, outputs, bars, status flow |
| `references/library-config-profiles.md` | Config profiles: website-design default + documented 2nd profile |

---

## Upstream contract

This skill reads dossiers and notes produced by `design-fingerprint` (v1.0+), which in turn reads
capture packages from `site-capture-engine` (v2.1+). The skill does not read capture packages
directly — it operates on the fingerprint output.

For non-website libraries (e.g., copywriting), the upstream skills are different (specified in the
profile) but the intake flow is identical: upstream produces an artifact → this skill files it.

---

## Downstream consumers

| Consumer | What it reads | How |
|---|---|---|
| [DI-4] `design-emulation-verify` | Filed dossiers | Uses as comparison baseline for build verification |
| [DI-6] `design-pattern-synthesis` | Filed trait sidecars | Parses for cross-corpus pattern counting and ranking |
| [DI-7] `reference-finder` | Candidates registry + library contents | Checks coverage, avoids duplicates, feeds new candidates |
| Website-design builds | Catalog entries (graduated patterns) | Picks patterns for client site composition |
| Manual use | Dossiers and notes | Human browses for inspiration |

---

## Related

- [[site-capture-engine]] — upstream capture (v2.1+)
- [[design-fingerprint]] — upstream fingerprint (v1.0)
- [[design-emulation-verify]] — downstream build-vs-reference diff
- [[design-pattern-synthesis]] — downstream cross-corpus analysis
- [[reference-finder]] — upstream discovery + vetting
- [[vis-extraction]] — sibling skill; cache/dedup + queue + review-gate discipline borrowed from here
- `second-brain/03_domains/website-design/inspiration/_README.md` — website-design library root
- `second-brain/03_domains/website-design/catalog/_README.md` — graduation destination
