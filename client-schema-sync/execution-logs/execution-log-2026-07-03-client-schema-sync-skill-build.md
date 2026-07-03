---
type: execution-log
status: draft
created: 2026-07-03
updated: 2026-07-03
venture: cross-project (agnostic skill)
tier: Productize
chat-id: client-schema-sync-skill-build-202607021900
tags: [execution-log, skill-build, schema, json-ld, client-schema-sync, productize]
---

## 2026-07-03 — Build `client-schema-sync` skill (agnostic, config-driven)

**What was built:** A reusable, config-driven skill that packages the proven [G3] WordPress
JSON-LD schema procedure into an agnostic engine + per-client profiles. The engine runs the
full 8-step schema sync (detect render store, verify 3 entities, sync AggregateRating,
inject LocalBusiness via keelworks-jsonld-head, detect duplicate org, inject HowTo, inject
SpeakableSpecification, cache-busted verify + gate verdict) from a client slug alone.

**Tier:** Productize (first Wave C skill build, first PR-1 dogfood).

## Steps (B1 — repeatable procedure)

1. **Survey + naming decision.** Read `client-seo-onboarding` (11-step one-time pipeline),
   Core-30 scaffold/publish scripts, `gate-peer-reviewer` (21 registered gate types, no
   G-schema). Decided: NEW separate skill `client-schema-sync` (different trigger cadence,
   data sources, execution model vs. onboarding). Operator confirmed.

2. **Read source scripts.** `ev_schema_inject_v2.py` (200L — curl subprocess, @graph
   extension, HowTo + Speakable builders) + `ev_schema_audit.py` (205L — recursive type
   collection, multi-block extraction, duplicate detection). Identified EV-specific parts
   (hardcoded page IDs, CSS class names) vs. generalizable engine (curl+REST, @graph
   manipulation, type collection).

3. **Read existing config contracts.** Client configs (`data/client-*.json` — EV, S&H,
   Asian Delight), profile system (`profiles/electrician/schema-template.json`), SOP
   (`sop-local-schema-markup.md`), pattern doc.

4. **Build agnostic engine.** `schema_sync_engine.py` (550L) — 5 CLI commands (`audit`,
   `verify`, `sync-rating`, `inject`, `inject-lb`), all dry-run by default. Zero hardcoded
   client values. All WP REST via curl subprocess (WAF workaround). Handles both
   `content.raw` and `_kw_jsonld` render stores. `copy.deepcopy` + `ensure_graph_wrapper`
   for Elementor flat JSON-LD.

5. **Seed 3 profiles.** EV (41 pages, all WP IDs), S&H (30 pages, WP IDs pending), Asian
   Delight (4 pages, restaurant type, placeholder — 2nd-client proof).

6. **Write SKILL.md.** Skill definition with config schema, command examples, safety rules,
   human-in-loop steps, gate integration, provenance.

7. **Verify.** Syntax check PASS, CLI help PASS, 14 unit tests PASS (JSON-LD extraction,
   type collection, graph manipulation, step extraction, node builders, entity verification,
   duplicate detection, gate verdict, restaurant profile differentiation).

## Engine / config split (B2)

**Engine (reusable, zero client values):**
- `repos/ai-agency-core/scripts/schema_sync_engine.py` — the 550L Python engine
- Functions: `wp_get_page`, `wp_put_page`, `extract_jsonld_blocks`, `collect_types`,
  `build_local_business_node`, `verify_core_entities`, `detect_duplicate_org`,
  `extract_process_steps`, `build_howto_node`, `build_speakable_node`, `sync_aggregate_rating`,
  `inject_howto_speakable`, `inject_local_business_kw_jsonld`, `verify_all_pages`,
  `build_gate_verdict`

**Config (per-client/instance-specific):**
- `repos/ai-agency-core/scripts/data/client-<slug>.json` — business facts (NAP, hours,
  rating, credentials, business-type-specific fields)
- `skills/client-schema-sync/references/profiles/<slug>.json` — schema-sync config
  (WP domain + creds, page list with WP IDs + render store, CSS selectors for HowTo/Speakable,
  human-in-loop step definitions)

## Config schema (B3)

### Client config (`data/client-<slug>.json`)

| Field | Type | Required | Example |
|-------|------|----------|---------|
| `business_type` | string | yes | `"electrician"`, `"restaurant"` |
| `client_slug` | string | yes | `"ev-electric-services"` |
| `name` | string | yes | `"EV Electric Services"` |
| `phone_e164` | string | yes | `"+1-571-500-6637"` |
| `email` | string | yes | `"Contact@evelectric.pro"` |
| `website_url` | string | yes | `"https://evelectric.pro/"` |
| `address` | object | yes | `{street, locality, region, postal_code, country}` |
| `geo` | object | yes | `{latitude, longitude}` |
| `hours` | array | yes | `[{days, opens, closes}]` |
| `review_count` | int | no | `87` (0 or absent = omit AggregateRating) |
| `review_rating` | string | no | `"5.0"` |
| `brand_areas_served` | array | no | `["Vienna", "Fairfax"]` |
| `owner_name` | string | no | `"Ahmad Shaban"` |
| `<business_type>` | object | no | Type-specific (electrician: license; restaurant: cuisine, menu) |

### Schema-sync profile (`references/profiles/<slug>.json`)

| Field | Type | Required | Example |
|-------|------|----------|---------|
| `client_slug` | string | yes | `"ev-electric-services"` |
| `wordpress.domain` | string | yes | `"evelectric.pro"` |
| `wordpress.api_user` | string | yes | `"oliver@keelworks.ai"` |
| `wordpress.api_password_env` | string | yes | `"WP_APP_PASSWORD_EV"` |
| `wordpress.seo_plugin` | string | yes | `"aioseo"` or `"yoast"` |
| `schema_config.business_type_schema` | string | yes | `"LocalBusiness"`, `"Restaurant"` |
| `schema_config.canonical_business_id` | string | yes | `"https://evelectric.pro/#business"` |
| `schema_config.howto_step_selectors` | array | yes | `[{combined_pattern: "regex"}]` (empty = skip HowTo) |
| `schema_config.speakable_css_selectors` | array | yes | `[".evp-faq-list", "h1"]` |
| `pages` | array | yes | `[{url, class, wp_id, store}]` |
| `human_in_loop_steps` | array | yes | `[{step, description, output_needed}]` |

## 2nd-instance verdict (B4)

**Verdict: PASS.** Asian Delight (restaurant type) runs from config alone with zero engine
code changes. Proven by unit tests:

- `load_client_config('asian-delight')` + `load_sync_profile('asian-delight')` — both load
- `build_local_business_node` produces `@type: Restaurant` with `servesCuisine` field
- No `hasCredential` (restaurants don't have electrician licenses — correctly absent)
- Empty `howto_step_selectors` = HowTo injection correctly skipped
- Different `speakable_css_selectors` (restaurant-specific: `.menu-section`, `main h2`)
- 4 pages (vs. 41 for EV) — page list is pure config

**What's different between electrician and restaurant profiles:**
- `business_type_schema`: `"LocalBusiness"` vs `"Restaurant"`
- `howto_step_selectors`: populated (electrician process steps) vs empty (restaurants)
- `speakable_css_selectors`: electrician-design-system selectors vs restaurant selectors
- Business-type-specific fields: `hasCredential` + `license` (electrician) vs `servesCuisine` + `hasMenu` (restaurant)
- All differences are config-driven, no code branches.

## Safety / quality rules (B5)

| # | Failure mode | Guard | Where enforced |
|---|-------------|-------|----------------|
| 1 | WAF 403 from Python urllib | All WP REST calls use `curl` subprocess | `wp_get_page`, `wp_put_page`, `_fetch_live_html` |
| 2 | XSS via `</script>` in injected JSON | `safe_json_for_script()` post-processes all `json.dumps` output that enters `<script>` tags or `_kw_jsonld` meta (which the plugin echoes into `<script>`), replacing `</` with `<\/` — the standard web-safe JSON-in-HTML approach equivalent to PHP's `JSON_HEX_TAG` | `_sync_rating_in_content`, `_inject_hs_content_raw` (script tags), `_sync_rating_in_kw_jsonld`, `inject_local_business_kw_jsonld`, `_inject_hs_kw_jsonld` (meta→plugin→script) |
| 3 | Circular-reference error on Elementor flat JSON-LD | `copy.deepcopy()` before manipulation + `ensure_graph_wrapper()` restructures into @graph | `_sync_rating_in_kw_jsonld`, `inject_local_business_kw_jsonld`, `_inject_hs_kw_jsonld` |
| 4 | Stale cache masking schema state | All `audit`/`verify` use `?nocache=<timestamp>` cache-busting | `audit_page_live` |
| 5 | Re-scaffolding live pages to change a value | `sync-rating` does surgical per-field edits only | `_sync_rating_in_content`, `_sync_rating_in_kw_jsonld` |
| 6 | Silent skip of human-required steps | `sync-rating` errors with explicit instructions if `--rating`/`--count` missing; profiles document all human steps | `cmd_sync_rating`, `human_in_loop_steps` in profiles |
| 7 | Accidental live write | All write commands default to dry-run; `--live` flag required | `argparse` default + all `dry_run` params |
| 8 | HowTo on pages without visible steps | Only injects if `extract_process_steps` finds real matches in rendered HTML | `_inject_hs_content_raw`, `_inject_hs_kw_jsonld` |

## Skill-candidacy verdict (B6)

**Verdict: Yes — this IS the skill.** This run IS the skill build (not a pre-skill run that
generates a handoff). The skill is built and registered at `skills/client-schema-sync/`.
The originating handoff is `handoff-2026-06-20-client-schema-sync-skill.md`.

## Deliverable manifest

| # | Deliverable | Path | Assertion | Check |
|---|---|---|---|---|
| 1 | Execution log with repeatable steps (B1) | `skills/client-schema-sync/execution-logs/execution-log-2026-07-03-client-schema-sync-skill-build.md` | exists + non-stub + has-steps-section | OC-1 + B1 |
| 2 | Engine/config split documented (B2) | (this exec log) | contains-engine-config-section | B2 |
| 3 | Config schema (B3) | (this exec log + SKILL.md) | contains-config-table | B3 |
| 4 | 2nd-instance verdict (B4) | (this exec log) | contains-duplicability-verdict + PASS | B4 |
| 5 | Safety/quality rules (B5) | (this exec log + SKILL.md) | contains-safety-section | B5 |
| 6 | Skill-candidacy verdict (B6) | (this exec log) | contains-skill-verdict + Yes | B6 |
| 7 | Engine script | `repos/ai-agency-core/scripts/schema_sync_engine.py` | exists + syntax-valid + CLI --help | — |
| 8 | SKILL.md | `skills/client-schema-sync/SKILL.md` | exists + has-commands-section + has-config-schema | — |
| 9 | EV profile | `skills/client-schema-sync/references/profiles/ev-electric-services.json` | exists + valid JSON + 41 pages | — |
| 10 | S&H profile | `skills/client-schema-sync/references/profiles/s-and-h-contracting.json` | exists + valid JSON + 30 pages | — |
| 11 | Asian Delight profile (2nd-client proof) | `skills/client-schema-sync/references/profiles/asian-delight.json` | exists + valid JSON + business_type_schema=Restaurant | — |
| 12 | Unit tests pass | (inline in this session) | 14/14 PASS | — |

## Decisions made

- **Separate skill, not extension of client-seo-onboarding.** Rationale: different trigger
  cadence (recurring vs one-time), different data sources (live WP pages vs intake forms),
  different execution model (targeted commands vs 11-step pipeline).
- **Profile per client, not per business type.** A restaurant and an electrician on the same
  WP host have different page lists, selectors, WP IDs — these are per-client, not per-type.
  The business-type differences (Restaurant vs LocalBusiness @type, servesCuisine vs
  hasCredential) come from the client config's `business_type` field.
- **S&H WP IDs left null.** Populating requires a live REST API call; documented as a
  human-in-loop step rather than guessing.

## Pattern candidates

- **Reusable: Yes** — the engine IS the skill. No additional pattern extraction needed;
  the SKILL.md and SOP (`sop-local-schema-markup`) already document the pattern.
  Existing pattern `pattern-wordpress-jsonld-injection-and-verification` covers the
  foundational mechanics; this skill is the executable form of that pattern.

## Open items

- S&H WP page IDs need population (human-in-loop step in profile)
- G-schema gate type not yet registered in `gate-type-registry.md` (follow-up)
- Asian Delight site not live — profile proves config-only execution, actual sync deferred
