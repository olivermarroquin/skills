---
name: index-status-diagnose
version: 1.0
status: active
created: 2026-06-25
updated: 2026-06-25
description: Pull per-page index status + reason from the GSC URL Inspection API for any client, classify results (indexed / crawled-not-indexed / discovered / unknown / blocked), and produce an actionable report. Config-driven, zero hardcoded client values.
engine: repos/ai-agency-core/scripts/gsc_url_inspection.py
compose-targets:
  - gsc_search_analytics.py (shared auth + config pattern)
  - gsc_indexing.py (shared auth pattern)
  - client-seo-onboarding (consumes report in indexation-verify phase)
triggers:
  - "diagnose index status for <client>"
  - "index-status-diagnose <client-slug>"
  - "why aren't my pages indexed"
  - "check indexation for <client>"
  - "url inspection for <client>"
tags: [skill, gsc, url-inspection, indexation, diagnosis, client-growth, reusable]
resolves: CG-001
---

# index-status-diagnose — GSC URL Inspection index-status engine

## Purpose

Answers "why aren't my pages indexed?" with definitive per-page data from Google's URL Inspection API. Replaces the A2-era proxy method (GSC impressions + `site:` SERP) with the authoritative source.

For each URL, returns:
- **Coverage state** — the exact reason Google gives (Submitted and indexed / Crawled - currently not indexed / Discovered - currently not indexed / URL is unknown to Google / Excluded by noindex / etc.)
- **Crawl metadata** — last crawl time, crawled as (MOBILE/DESKTOP), page fetch state
- **Canonical signals** — Google-selected canonical vs user-declared canonical (populated only for indexed pages)
- **Discovery signals** — referring URLs, sitemap presence

Outputs two files:
1. **Markdown report** — summary table + per-category breakdown with actionable interpretation
2. **JSON companion** — machine-readable, for downstream automation

## Prerequisites

- GSC property configured in client config (`gsc_property` key)
- ADC authenticated with the `webmasters` scope (full, not readonly):
  ```
  gcloud auth application-default login \
    --scopes=https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/indexing,https://www.googleapis.com/auth/webmasters
  gcloud auth application-default set-quota-project keelworks-seo-automation
  ```
- Oliver must be Owner on the GSC property for the client

## Config

Uses the existing `repos/ai-agency-core/scripts/<client-slug>.config.json`. Required key:

```json
{
  "gsc_property": "sc-domain:evelectric.pro"
}
```

No additional config keys needed — the skill reads auth from ADC and the property from the existing config.

### Proven clients

| Client | Config file | Property | Verified |
|--------|------------|----------|----------|
| EV Electric | `ev-electric.config.json` | `sc-domain:evelectric.pro` | 2026-06-25 (IDX-1) — 55 URLs |
| S&H Contracting | `s-and-h-contracting.config.json` | `https://shcontractingunlimited.com/` | 2026-06-25 (IDX-1) — 35 URLs |

## Usage

### CLI

```bash
cd ~/workspace/repos/ai-agency-core/scripts

# Inspect specific URLs
python gsc_url_inspection.py ev-electric-services \
  https://evelectric.pro/panel-upgrade-vienna-va/ \
  https://evelectric.pro/ev-charger-vienna-va/

# Inspect from a file (one URL per line, # comments allowed)
python gsc_url_inspection.py s-and-h-contracting --from-file sh-urls.txt
```

### Python API

```python
from gsc_url_inspection import inspect_url, pull_client_index_report, write_client_index_report

# Single URL
result = inspect_url(
    "https://evelectric.pro/panel-upgrade-vienna-va/",
    "sc-domain:evelectric.pro"
)

# Full client report
urls = ["https://evelectric.pro/page1/", "https://evelectric.pro/page2/"]
report = pull_client_index_report("ev-electric-services", urls)
md_path, json_path = write_client_index_report("ev-electric-services", report)
```

## Output interpretation

| Coverage state | What it means | Action |
|---------------|---------------|--------|
| Submitted and indexed | In Google's index. Working. | None needed. |
| Crawled - currently not indexed | Google crawled it and chose NOT to index. Quality/authority signal. | Check content quality, canonical tags, domain authority. |
| Discovered - currently not indexed | Google knows the URL but hasn't crawled it yet. Crawl budget. | Wait + improve crawl signals (internal links, sitemap). |
| URL is unknown to Google | Google has never seen this URL. Discovery failure. | Check sitemap inclusion + internal linking. |
| Excluded by noindex | Page has a noindex directive. | Remove noindex if the page should be indexed. |
| Blocked by robots.txt | robots.txt blocks crawling. | Update robots.txt if the page should be indexed. |

### Canonical data availability

The API returns `googleCanonical` and `userCanonical` fields **only for indexed pages**. For non-indexed pages, these fields are absent — the API does not expose what Googlebot saw for canonical during its crawl. This is a known limitation; use direct page fetches to verify canonical tags on non-indexed pages.

### Crawl agent pattern

Pages crawled as DESKTOP only (not MOBILE) on a mobile-first-indexing site indicate Google did a preliminary scan but hasn't promoted the page to the full indexing pipeline. This is typical for low-authority sites.

## Rate limiting

The script inserts a 0.3s delay between API calls by default. The URL Inspection API has a quota of ~600 requests/day per property (undocumented but observed). For a typical client with 30-60 pages, one full scan uses ~10% of the daily quota.

## Composability

This skill composes with:
- **gsc-performance-pull** — run the performance pull first to identify which pages have impressions, then run this skill on the pages with 0 impressions to diagnose why
- **client-seo-onboarding** — the indexation-verify phase should use this skill instead of the A2 proxy method
- **gsc_indexing.py** — after diagnosis, submit "unknown to Google" pages via the Indexing API to accelerate discovery

## History

- **v1.0 (2026-06-25):** Built by [IDX-1]. Resolves CG-001 (the A2 capability gap where URL Inspection was blocked by auth scope). Auth fix: ADC with `webmasters` scope works on gcloud's OAuth client — the A2 diagnosis ("client doesn't support the scope") was wrong; the token just needed re-auth. Proven on EV (55 URLs) + S&H (35 URLs) with full per-page diagnosis.
