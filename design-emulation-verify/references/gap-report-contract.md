---
type: reference
status: active
created: 2026-06-19
updated: 2026-06-19
version: "1.0"
tags: [reference, design-emulation-verify, gap-report, output-contract]
---

# Gap report contract (v1.0)

> **Downstream consumers bind to this contract.** The gap report is the output of
> `design-emulation-verify` — a structured diff of a rendered build against a reference
> design. Claude Code reads the report to close gaps in iteration; the operator reads it
> to verify emulation quality before launch.

## When a gap report is produced

A gap report is produced every time `diff_build_vs_reference.mjs` runs. One report per
invocation (one build URL × one reference URL × one page scope).

## Output files

Each run produces **two files** at the specified output path:

| File | Format | Purpose |
|---|---|---|
| `verify-<build-slug>-<date>.md` | Markdown | Human-readable gap report (4 sections + legal boundary) |
| `verify-<build-slug>-<date>.json` | JSON | Machine-readable sidecar for programmatic gap parsing |

`<build-slug>` is derived from the build URL hostname. `<date>` is ISO date (YYYY-MM-DD).

## Markdown report structure

### Section 1 — Summary

| Field | Description |
|---|---|
| Reference URL | The reference site being compared against |
| Build URL | The build being verified |
| Mode | `full`, `structural-only`, `stylistic-only`, or `pattern-only` |
| Policy | `strict-match`, `brand-differentiation-allowed`, or `pattern-only-emulation` |
| Generated | ISO timestamp |

**Verdict table:** per-axis verdict (PASS / NEEDS-WORK) + total gap count + critical count.

**Overall verdict:**
- `PASS` — all four axes pass
- `NEEDS-WORK` — one or more axes have unresolved critical gaps

A build passes when:
- Zero critical structural gaps (or every structural difference is intentional)
- Stylistic gaps either closed OR within the brand-differentiation policy
- All expected patterns from the composition doc are present
- Zero legal-boundary findings

### Section 2 — Structural gaps

Each gap contains:

| Field | Description |
|---|---|
| `description` | What's different (e.g., "reference has 12 sections; build has 9") |
| `severity` | `critical` (section missing entirely), `moderate` (wrong order/count), `minor` (semantic mismatch but visual equivalent) |
| `refValue` | What the reference has |
| `buildValue` | What the build has |
| `fix` | Actionable fix suggestion for Claude Code |

**Diff method:** Both pages are rendered in Playwright. Semantic sections (`header`, `nav`,
`main`, `section`, `article`, `aside`, `footer`, ARIA roles) are extracted into a tree.
Section count, tag distribution, heading hierarchy, and depth are compared.

### Section 3 — Stylistic gaps

Each gap contains:

| Field | Description |
|---|---|
| `description` | Property + element + ref vs build values |
| `element` | Which probe element (body, h1, hero, cta, card, footer, etc.) |
| `property` | CSS property name (fontFamily, fontSize, color, backgroundColor, borderRadius, etc.) |
| `severity` | `critical` (wrong font family, off-palette by >100 RGB distance), `moderate` (size off by >4px, spacing broken), `minor` (1-2px off, slight shade difference) |
| `refValue` | Reference computed value |
| `buildValue` | Build computed value |
| `withinPolicy` | `true` if the gap is allowed under the active policy |
| `fix` | What to change (or "intentional under policy") |

**Diff method:** `getComputedStyle` on matched probe elements (body text, headings, hero,
CTA, card, footer, nav). Palette comparison against the dossier's extracted hex values.
Font comparison against the dossier's identified font families.

**Policies:**
- `strict-match` — every difference is a gap, nothing within policy
- `brand-differentiation-allowed` (default) — color and font-family diffs are within policy (brand choices)
- `pattern-only-emulation` — all stylistic diffs are within policy (only structure + patterns must match)

### Section 4 — Pattern presence gaps

Each gap contains:

| Field | Description |
|---|---|
| `pattern` | Pattern name from the composition doc or dossier |
| `status` | `missing`, `present-but-different`, `present-correctly` (only gaps are reported) |
| `severity` | `critical` (missing), `moderate` (present but degraded) |
| `notes` | Detection details |
| `fix` | How to implement or correct the pattern |

**Diff method:** Cross-reference expected patterns (from composition doc or dossier's
"patterns worth lifting" section) against detected patterns in the build DOM. Detection
uses keyword matching in headings, class names, and structural probe results.

### Section 5 — Legal boundary check

Each finding contains:

| Field | Description |
|---|---|
| `type` | `text-overlap` or `image-carryover` |
| `severity` | Always `critical` |
| `description` | What was found |
| `refSource` | The reference content that was matched |
| `buildLocation` | Where it appears in the build |

**Check method:**
- **Text overlap:** Sliding-window exact match of 20+ consecutive words from reference
  text blocks against build text blocks. Common/boilerplate phrases may produce false
  positives — the report lists candidates for operator review.
- **Image carryover:** URL pathname comparison of all `<img>` src attributes. Any
  reference image URL found in the build is flagged.

## JSON sidecar schema

```json
{
  "version": "1.0",
  "timestamp": "ISO-8601",
  "buildUrl": "string",
  "refUrl": "string",
  "mode": "full | structural-only | stylistic-only | pattern-only",
  "policy": "strict-match | brand-differentiation-allowed | pattern-only-emulation",
  "verdict": {
    "overall": "PASS | NEEDS-WORK",
    "structural": "PASS | NEEDS-WORK",
    "stylistic": "PASS | NEEDS-WORK",
    "pattern": "PASS | NEEDS-WORK",
    "legal": "PASS | NEEDS-WORK"
  },
  "gaps": {
    "structural": [{ "description": "", "severity": "", "refValue": "", "buildValue": "", "fix": "" }],
    "stylistic": [{ "description": "", "element": "", "property": "", "severity": "", "refValue": "", "buildValue": "", "withinPolicy": false, "fix": "" }],
    "patterns": [{ "pattern": "", "status": "", "severity": "", "notes": "", "fix": "" }],
    "legal": [{ "type": "", "severity": "", "description": "", "refSource": "", "buildLocation": "" }]
  },
  "totals": {
    "structural": 0,
    "stylistic": 0,
    "patterns": 0,
    "legal": 0,
    "total": 0,
    "critical": 0
  }
}
```

## Inputs the engine consumes

| Input | Source | Required |
|---|---|---|
| Build URL | Any renderable URL (localhost, preview, production) | Yes |
| Reference URL | Any renderable URL | Yes |
| Dossier | [DI-2] `design-fingerprint` output (`dossier-<slug>.md`) | Yes |
| Composition doc | Per-client pattern selection from the emulate tactic | No (falls back to dossier patterns) |
| Trait sidecar | [DI-2] `_traits-<slug>.yaml` | No (reserved for future cross-site analysis) |

## Framework-agnostic gate

The engine works on **any rendered build** that Playwright can load. The gate is
"is it renderable + capturable?" — not "is it React/Next.js." This includes:

- Next.js (App Router, Pages Router)
- WordPress (PHP-rendered, no JS dependency)
- Static HTML/CSS
- Any SPA (React, Vue, Svelte, etc.)
- Server-rendered frameworks (Rails, Django, Laravel)
- App webviews

The old restriction ("do not use for WordPress / non-React") is removed as of v1.0.

## Iteration support

When the engine runs multiple times on the same build (iteration cycle), each run
produces a new dated report. Comparing successive reports shows:
- Gaps closed (present in earlier report, absent in later)
- Gaps remaining (present in both)
- New gaps introduced (absent in earlier, present in later)

The JSON sidecar enables programmatic diff between successive runs.

## Versioning

This contract version (`1.0`) matches the engine version. When the contract changes:
1. Bump `version` in this file and in the engine's JSON output.
2. Update the JSON schema above.
3. Downstream consumers check `version` and warn on unknown versions.

## Related

- [[design-fingerprint]] — [DI-2], produces the dossier baseline this engine consumes
- [[site-capture-engine]] — [DI-1], captures both sides
- [[strategy-custom-coded-nextjs-via-ai-with-competitor-inspiration]] — Pillar 3 (Verified Emulation)
- [[tactic-emulate-competitor-design-patterns-with-ai]] — Steps 5-6 invoke this engine
