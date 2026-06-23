---
name: gsc-performance-pull
version: 1.0
status: active
created: 2026-06-23
updated: 2026-06-23
description: Pull GSC Search Analytics data for any client and produce a dated performance report (top queries, top pages, striking-distance position 5–20, CTR outliers) + a machine-readable JSON companion. Engine-first, per-client config, zero hardcoded client values. Downstream consumers: A2 next-20 page selection, monthly client report SOP (S11).
engine: repos/ai-agency-core/scripts/gsc_search_analytics.py
compose-targets:
  - gsc_indexing.py (shared auth pattern — SA-first / ADC-fallback)
  - client-seo-onboarding (consumes report in research-wave)
triggers:
  - "pull GSC performance for <client>"
  - "gsc-performance-pull <client-slug>"
  - "run GSC report for <client>"
  - "search analytics for <client>"
tags: [skill, gsc, search-analytics, performance, reporting, client-growth, reusable]
---

# gsc-performance-pull — GSC Search Analytics report engine

## Purpose

One command pulls Google Search Console Search Analytics data for a client property and produces two outputs:

1. **Human-readable markdown report** — plain-language summary on top, then top queries, top pages, the position 5–20 striking-distance set (primary input to A2 page selection), and CTR outliers.
2. **Machine-readable JSON companion** — same data structure, for downstream automation (A2 next-20 selection, monthly client report SOP).

Zero hardcoded client values. Reads everything from client config.

## Config

Per-client config is the existing `repos/ai-agency-core/scripts/<client-slug>.config.json`. This skill requires one additional key:

```json
{
  "gsc_property": "sc-domain:evelectric.pro"
}
```

**Property format:**
- **Domain property** (preferred — full history): `"sc-domain:example.com"`
- **URL-prefix property** (fallback): `"https://example.com/"`

The auth keys (`gsc_indexing`, SA/ADC config) are already in the client config from the Indexing API build.

### Property-access notes

| Client | Property | Access level | Notes |
|--------|----------|-------------|-------|
| EV Electric | `sc-domain:evelectric.pro` | Oliver = Full user | Domain property, full history. Aisha-owned. |
| S&H Contracting | `https://shcontractingunlimited.com/` | Oliver = Owner | URL-prefix only. Domain property may be under prior contractor. Sufficient for new-page performance; thinner long-term trend history. |

## Usage

### CLI

```bash
cd ~/workspace/repos/ai-agency-core/scripts
python gsc_search_analytics.py ev-electric-services        # 28-day default
python gsc_search_analytics.py s-and-h-contracting 14      # 14-day window
```

### Python API

```python
from gsc_search_analytics import pull_client_report, write_client_report

report = pull_client_report("ev-electric-services", window_days=28)
md_path, json_path = write_client_report("ev-electric-services", report)
```

### Low-level query

```python
from gsc_search_analytics import query_search_analytics

rows = query_search_analytics(
    property_url="sc-domain:evelectric.pro",
    start_date="2026-05-26",
    end_date="2026-06-20",
    dimensions=["query", "page"],
    row_limit=1000,
)
```

## Output

Reports are written to:
```
second-brain/04_projects/clients/_active/<client-slug>/reports/
  gsc-performance-<YYYY-MM-DD>.md    # human-readable
  gsc-performance-<YYYY-MM-DD>.json  # machine-readable
```

### Report sections

1. **Summary** — total clicks, impressions, average CTR, weighted avg position. Thin-data warning if impressions < 100 (honest about new sites).
2. **Top Queries by Impressions** — top 20 queries driving visibility.
3. **Top Pages by Impressions** — top 20 pages earning search exposure.
4. **Striking Distance (Position 5–20)** — queries close to page 1. This is the primary input to A2 page selection: which city×service combinations have GSC signal but aren't yet on page 1?
5. **CTR Outliers** — queries/pages ranking well but with unusually low CTR relative to position. Title/meta optimization opportunities.

### Thin-data honesty

Pages are ~15 days old for both clients. If clicks are near-zero, the report says so plainly and leans on impressions (which appear before clicks in the GSC lifecycle). No fabricated signal.

## Auth

Mirrors `gsc_indexing.py` auth (SA-first, ADC-fallback):
1. **Service account** (non-expiring) — loaded from tier-3 if available.
2. **ADC** (user-level, expires) — `gcloud auth application-default login` with scope `webmasters.readonly`.

Quota project `keelworks-seo-automation` is already set in the ADC file. If a 401 appears, re-auth:
```bash
gcloud auth application-default login \
  --scopes=https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/webmasters.readonly
```

## Dependencies

- Python 3.10+
- `requests` (already installed for gsc_indexing.py)
- `google-auth` (already installed)
- Valid GSC access (ADC or SA) with `webmasters.readonly` scope

## Downstream consumers

- **[A2] Indexation verify + next-20 selection** — reads `gsc-performance-<date>.json` to rank city×service combinations by impression signal + demand matrix.
- **[S11] Monthly client report SOP** — consumes this as the GSC section, avoiding a duplicate pull.
- **Any future per-client analytics** — the `query_search_analytics()` function is a general-purpose GSC query wrapper.

## Limitations

- GSC data lags ~3 days; the script uses `today - 3` as end date.
- S&H uses URL-prefix property (not domain) — no pre-build history.
- API returns max 25,000 rows per query; for sites with very high query diversity, multiple calls with filters would be needed (not an issue for our clients' scale).
- CTR benchmarks in the outlier detection are rough industry averages; they serve as directional signals, not precise thresholds.
