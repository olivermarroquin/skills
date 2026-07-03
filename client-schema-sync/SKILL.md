---
skill: client-schema-sync
version: 1.0.0
status: active
engine: repos/ai-agency-core/scripts/schema_sync_engine.py
created: 2026-07-03
updated: 2026-07-03
tier: productize
business_types: [electrician, restaurant]
tags: [skill, schema, json-ld, wordpress, localbusiness, aggregaterating, structured-data, agnostic]
---

# client-schema-sync — agnostic WordPress JSON-LD schema synchronization

Packages the proven [G3] WordPress schema procedure into a config-driven, client-agnostic
skill. Given a client slug, the engine runs the full 8-step schema sync procedure using
only the client facts file (`data/client-<slug>.json`) and a per-client schema-sync profile
(`references/profiles/<slug>.json`). Zero hardcoded client values, slugs, NAP, counts, or
domains in the engine.

## What it does

| Step | Action | Render store |
|------|--------|-------------|
| 1 | **Detect render store** per page (content.raw vs Elementor `_kw_jsonld` vs SEO-plugin head) | Auto-detected |
| 2 | **Verify 3 core entities** (LocalBusiness/subtype + Service + FAQPage) on all pages | Both |
| 3 | **Sync AggregateRating** to live Google count (human-in-loop GBP read) | Both |
| 4 | **Add LocalBusiness** to Elementor pages via `keelworks-jsonld-head` plugin (`_kw_jsonld`) | Elementor |
| 5 | **Detect duplicate org schema** (SEO-plugin vs scaffolder collision) | Both |
| 6 | **Inject HowTo** (ONLY on pages with genuinely visible process steps) | Both |
| 7 | **Inject SpeakableSpecification** | Both |
| 8 | **Verify live, cache-busted**, report "X of Y", emit gate verdict | Live HTML |

## Engine

```
repos/ai-agency-core/scripts/schema_sync_engine.py
```

## Config files

| File | Purpose |
|------|---------|
| `repos/ai-agency-core/scripts/data/client-<slug>.json` | Client business facts (NAP, hours, rating, etc.) |
| `skills/client-schema-sync/references/profiles/<slug>.json` | Per-client schema-sync config (WP creds, page list, selectors, human-in-loop steps) |

### Profile schema

```json
{
  "client_slug": "string — matches client-<slug>.json",
  "wordpress": {
    "domain": "string — bare domain, no protocol",
    "api_user": "string — WP REST API user",
    "api_password_env": "string — env var name holding the WP app password",
    "seo_plugin": "aioseo | yoast"
  },
  "schema_config": {
    "business_type_schema": "LocalBusiness | Electrician | Restaurant | string",
    "canonical_business_id": "string — e.g. https://domain/#business",
    "howto_step_selectors": [{"combined_pattern": "regex"}],
    "speakable_css_selectors": ["string CSS selectors"],
    "skip_widget_patterns": ["string glob patterns"]
  },
  "pages": [
    {
      "url": "string — full URL",
      "class": "core-home | core-about | hub | leaf | ...",
      "wp_id": "int | null",
      "store": "content_raw | elementor_kw_jsonld"
    }
  ],
  "human_in_loop_steps": [
    {
      "step": "string ID",
      "description": "string — what the human must do",
      "output_needed": "string — what value to provide"
    }
  ]
}
```

## Commands

All commands default to **dry-run**. Pass `--live` to execute writes.

### Audit all pages (read-only)

```bash
python3 repos/ai-agency-core/scripts/schema_sync_engine.py audit \
  --client ev-electric-services
```

### Full verification + gate verdict

```bash
python3 repos/ai-agency-core/scripts/schema_sync_engine.py verify \
  --client ev-electric-services \
  --verdict-file .review-gate/state/verdict-schema-sync.json \
  --run-id client-schema-sync-ev-202607031900
```

### Sync AggregateRating (human-in-loop count)

```bash
# HUMAN-IN-LOOP: Read live GBP count first (not headless-fetchable)
python3 repos/ai-agency-core/scripts/schema_sync_engine.py sync-rating \
  --client ev-electric-services --rating 5.0 --count 91 --live
```

### Inject HowTo + SpeakableSpecification

```bash
python3 repos/ai-agency-core/scripts/schema_sync_engine.py inject \
  --client ev-electric-services --live
```

### Inject LocalBusiness into Elementor pages

```bash
# PREREQUISITE: keelworks-jsonld-head plugin installed on the WP site
python3 repos/ai-agency-core/scripts/schema_sync_engine.py inject-lb \
  --client ev-electric-services --live
```

## Human-in-loop steps (not silently skipped)

These steps require human action. The engine surfaces them explicitly and blocks
(or documents the gap) rather than silently skipping.

| Step | Why human-required | Engine behavior |
|------|-------------------|-----------------|
| **GBP review count read** | Google Business Profile is not headless-fetchable | `sync-rating` command requires `--rating` + `--count` args; errors with instructions if missing |
| **keelworks-jsonld-head plugin install** | Per-site WP plugin upload | `inject-lb` documents the prerequisite; operator uploads manually |
| **WP page ID population** | New client profiles need WP IDs from REST API | Profile has `wp_id: null` entries with a human_in_loop_steps instruction |

## Safety rules (baked into the engine)

1. **WAF workaround**: All WP REST calls use `curl` subprocess, not Python `urllib`/`requests`
   (Hostinger/LiteSpeed WAF returns 403 to Python's default User-Agent)
2. **`safe_json_for_script()`**: All `json.dumps` output that enters `<script>` tags or
   `_kw_jsonld` meta (which the keelworks plugin echoes into `<script>`) is post-processed
   to replace `</` with `<\/` — the standard web-safe JSON-in-HTML approach equivalent to
   PHP's `JSON_HEX_TAG`. Prevents `</script>` breakout / stored XSS.
3. **Live-not-vault verification**: `audit` and `verify` commands fetch live URLs with
   `?nocache=<timestamp>` cache-busting
4. **`filter_skip_widgets()`**: Content sweeps filter out HTML elements whose class matches
   `skip_widget_patterns` globs (e.g. `ti-review-*`) before scanning for process steps.
   Nesting-aware: tracks open/close tag depth so sibling elements are preserved.
5. **Elementor flat JSON-LD**: `copy.deepcopy()` + `ensure_graph_wrapper()` restructures
   flat JSON-LD into `@graph` before adding nodes (avoids circular-reference errors)
6. **Surgical per-page edits**: `sync-rating` edits only the AggregateRating values, never
   re-scaffolds live pages (preserves post-publish image/localization fixes)
7. **Backup before write**: Engine reads full page content before any write (the GET is
   the backup — log the pre-edit state)
8. **Dry-run default**: All write commands default to dry-run; `--live` flag required

## Gate integration

The `verify` command emits a gate-peer-reviewer return contract (JSON) when
`--verdict-file` is provided. Gate type: **G-schema**.

Verdict mapping:
- **APPROVE**: All core entities present on all expected pages, no blocking findings
- **REJECT-AND-REDO**: Missing core entities, duplicate business nodes, or fetch errors

## Seeded profiles

| Client | Business type | Status |
|--------|--------------|--------|
| `ev-electric-services` | electrician (LocalBusiness) | Full — 41 pages, all WP IDs populated |
| `s-and-h-contracting` | electrician (LocalBusiness) | Partial — WP IDs need population |
| `asian-delight` | restaurant (Restaurant) | Placeholder — 2nd-client proof, site not yet live |

## Onboarding a new client

1. Create `data/client-<slug>.json` with business facts (or reuse existing)
2. Create `references/profiles/<slug>.json` with WP creds, page list, selectors
3. Run `audit --client <slug>` to establish baseline
4. Run `verify --client <slug>` to check entity coverage
5. Fix gaps with `sync-rating`, `inject`, `inject-lb` as needed
6. Re-run `verify` with `--verdict-file` to emit gate verdict

## Provenance

- Lifted from `repos/ev-electric-services/.kos/scripts/ev_schema_inject_v2.py` (injection)
  + `ev_schema_audit.py` (audit)
- Generalized from the [G3] EV + S&H schema verification runs (2026-06-20 + 2026-06-24)
- Pattern: [[pattern-wordpress-jsonld-injection-and-verification]]
- SOP: [[sop-local-schema-markup]]
- Plugin: `repos/ai-agency-core/wordpress-plugins/keelworks-jsonld-head/`

## See also

- [[sop-local-schema-markup]] — the SOP this skill automates
- [[pattern-wordpress-jsonld-injection-and-verification]] — the injection+verify pattern
- [[blueprint-local-seo-growth-program]] — the program this feeds
- [[handoff-2026-06-20-client-schema-sync-skill]] — the build handoff
- [[handoff-2026-06-20-g3b-ev-duplicate-organization-reconciliation]] — dup-org follow-up
