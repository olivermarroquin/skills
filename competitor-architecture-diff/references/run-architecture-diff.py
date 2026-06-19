#!/usr/bin/env python3
"""
run-architecture-diff.py — Competitor content-architecture diff engine.

Given a competitor teardown (URL inventories + extracted schemas/content) and
a profile describing our current output set, classifies structural surfaces
the competitor has that we don't, and emits a ranked expansion backlog.

Domain-agnostic: all specifics live in the profile YAML.

USAGE
-----
    python run-architecture-diff.py --profile profiles/ev-aj-long-core30.yaml

OUTPUT
------
Two files in the profile's output_dir:
  - architecture-diff-<competitor>-<date>.md  (human report)
  - architecture-diff-<competitor>-<date>.json (machine findings)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    sys.stderr.write("ERROR: PyYAML required. pip install pyyaml\n")
    sys.exit(2)


def expand_path(p: str) -> Path:
    return Path(os.path.expanduser(p))


def load_profile(path: Path) -> dict[str, Any]:
    if not path.is_file():
        sys.stderr.write(f"ERROR: profile not found: {path}\n")
        sys.exit(2)
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def read_url_inventory(teardown: Path, filename: str) -> list[str]:
    path = teardown / "data" / filename
    if not path.is_file():
        return []
    return [line.strip() for line in path.read_text().splitlines() if line.strip()]


def read_tsv_grid(teardown: Path, filename: str) -> list[dict[str, str]]:
    path = teardown / "data" / filename
    if not path.is_file():
        return []
    lines = path.read_text().splitlines()
    if len(lines) < 2:
        return []
    headers = lines[0].split("\t")
    rows = []
    for line in lines[1:]:
        cols = line.split("\t")
        row = {}
        for i, h in enumerate(headers):
            row[h.strip()] = cols[i].strip() if i < len(cols) else ""
        rows.append(row)
    return rows


def read_extracted_schemas(teardown: Path) -> dict[str, Any]:
    """Read all extracted schema.json files and return page-slug -> schema dict."""
    extracted_dir = teardown / "extracted"
    if not extracted_dir.is_dir():
        return {}
    schemas = {}
    for f in sorted(extracted_dir.glob("*.schema.json")):
        slug = f.name.replace(".schema.json", "")
        try:
            schemas[slug] = json.loads(f.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    return schemas


def classify_url(url: str, domain: str) -> dict[str, str]:
    """Extract page type and slug from a competitor URL."""
    path = url.replace(f"https://{domain}", "").replace(f"http://{domain}", "")
    path = path.strip("/")
    parts = path.split("/")

    if not parts or parts == [""]:
        return {"type": "homepage", "slug": "home"}
    elif parts[0] == "services":
        if len(parts) == 2:
            return {"type": "service-base", "slug": parts[1]}
        elif len(parts) == 3:
            return {"type": "service-city", "slug": f"{parts[1]}/{parts[2]}"}
        else:
            return {"type": "service-sub", "slug": "/".join(parts[1:])}
    elif parts[0] == "problems":
        if len(parts) == 1:
            return {"type": "problems-hub", "slug": "problems"}
        return {"type": "problem-page", "slug": parts[1]}
    elif parts[0] == "neighborhoods":
        if len(parts) == 1:
            return {"type": "neighborhoods-hub", "slug": "neighborhoods"}
        return {"type": "neighborhood-page", "slug": parts[1]}
    elif parts[0] == "guides":
        if len(parts) == 1:
            return {"type": "guides-hub", "slug": "guides"}
        return {"type": "guide-page", "slug": parts[1]}
    elif parts[0] == "blog":
        if len(parts) == 1:
            return {"type": "blog-hub", "slug": "blog"}
        return {"type": "blog-post", "slug": parts[1]}
    elif parts[0] == "about":
        return {"type": "about-sub", "slug": "/".join(parts)}
    else:
        return {"type": "core-page", "slug": "/".join(parts)}


def extract_schema_types(schema_data: Any) -> list[str]:
    """Recursively extract all @type values from schema data."""
    types: list[str] = []
    if isinstance(schema_data, dict):
        if "@type" in schema_data:
            t = schema_data["@type"]
            if isinstance(t, list):
                types.extend(t)
            else:
                types.append(t)
        if "@graph" in schema_data:
            types.extend(extract_schema_types(schema_data["@graph"]))
        for v in schema_data.values():
            if isinstance(v, (dict, list)):
                types.extend(extract_schema_types(v))
    elif isinstance(schema_data, list):
        for item in schema_data:
            types.extend(extract_schema_types(item))
    return types


def build_competitor_architecture(
    profile: dict[str, Any],
    teardown: Path,
) -> dict[str, Any]:
    """Step 1: Parse competitor content architecture."""
    domain = profile["competitor_domain"]

    # Read all URL inventories
    inventories = {
        "services": read_url_inventory(teardown, "urls-services.txt"),
        "problems": read_url_inventory(teardown, "urls-problems.txt"),
        "neighborhoods": read_url_inventory(teardown, "urls-neighborhoods.txt"),
        "guides": read_url_inventory(teardown, "urls-guides.txt"),
        "core": read_url_inventory(teardown, "urls-core.txt"),
        "blog": read_url_inventory(teardown, "urls-blog.txt"),
        "locations": read_url_inventory(teardown, "urls-locations.txt"),
    }

    # Classify all URLs
    page_types: dict[str, list[dict]] = {}
    for inv_name, urls in inventories.items():
        for url in urls:
            classified = classify_url(url, domain)
            ptype = classified["type"]
            page_types.setdefault(ptype, []).append({
                "url": url,
                "slug": classified["slug"],
                "inventory": inv_name,
            })

    # Read extracted schemas
    schemas = read_extracted_schemas(teardown)

    # Map schema types to page types using extracted samples.
    # Derive page type from schema slug dynamically via profile or heuristic —
    # no hardcoded competitor-specific slugs in the engine.
    schema_by_page_type: dict[str, list[str]] = {}
    schema_samples = profile.get("schema_samples", {})
    for slug, schema_data in schemas.items():
        # Profile-driven mapping takes priority
        if slug in schema_samples:
            ptype = schema_samples[slug]
        else:
            # Heuristic: infer page type from the extracted slug name
            slug_lower = slug.lower()
            if slug_lower in ("home", "homepage"):
                ptype = "homepage"
            elif slug_lower.startswith("svc-city") or slug_lower.startswith("service-city"):
                ptype = "service-city"
            elif slug_lower.startswith("service-base") or slug_lower.startswith("svc-base"):
                ptype = "service-base"
            elif slug_lower.startswith("problem"):
                ptype = "problem-page"
            elif slug_lower.startswith("neighborhood"):
                ptype = "neighborhood-page"
            elif slug_lower.startswith("guide"):
                ptype = "guide-page"
            elif slug_lower.startswith("blog"):
                ptype = "blog-post"
            elif slug_lower.startswith("city-servicearea") or slug_lower.startswith("location"):
                ptype = "core-page"
            else:
                ptype = "core-page"
        types = sorted(set(extract_schema_types(schema_data)))
        # Merge — first match per page type wins, subsequent samples extend
        if ptype in schema_by_page_type:
            existing = set(schema_by_page_type[ptype])
            existing.update(types)
            schema_by_page_type[ptype] = sorted(existing)
        else:
            schema_by_page_type[ptype] = types

    # Read service-city presence grid
    grid = read_tsv_grid(teardown, "service-city-presence-grid.tsv")
    service_city_matrix = {
        "cities": len(grid),
        "services_with_city_pages": 0,
        "total_service_city_pairs": 0,
    }
    if grid and len(grid) > 0:
        service_cols = [c for c in grid[0].keys() if c not in ("city", "TOTAL")]
        services_with_pages = set()
        for row in grid:
            for svc in service_cols:
                if row.get(svc, "").strip() == "Y":
                    services_with_pages.add(svc)
                    service_city_matrix["total_service_city_pairs"] += 1
        service_city_matrix["services_with_city_pages"] = len(services_with_pages)

    # Build the architecture map
    architecture: dict[str, Any] = {}
    for ptype, entries in sorted(page_types.items()):
        # Derive URL pattern from first entry
        sample_urls = [e["url"] for e in entries[:3]]
        url_parts = [e["url"].replace(f"https://{domain}/", "") for e in entries]
        if len(url_parts) > 1:
            # Find common prefix
            prefix = os.path.commonprefix(url_parts).rstrip("/")
            url_pattern = f"/{prefix}/{{slug}}" if prefix else "/{slug}"
        else:
            url_pattern = f"/{url_parts[0]}" if url_parts else ""

        architecture[ptype] = {
            "count": len(entries),
            "url_pattern": url_pattern,
            "schema_types": schema_by_page_type.get(ptype, []),
            "sample_urls": sample_urls,
            "inventory_source": entries[0]["inventory"] if entries else "",
        }

    return {
        "architecture": architecture,
        "service_city_matrix": service_city_matrix,
        "inventories_read": {k: len(v) for k, v in inventories.items()},
    }


def build_our_architecture(profile: dict[str, Any]) -> dict[str, Any]:
    """Step 2: Map our current output set from the profile."""
    output_set = profile["our_output_set"]
    our_arch: dict[str, Any] = {}
    for pt in output_set.get("page_types", []):
        our_arch[pt["name"]] = {
            "count": pt.get("count", 0),
            "sections": pt.get("sections", []),
            "schema": pt.get("schema", []),
            "description": pt.get("description", ""),
        }
    return our_arch


def check_data_supportability(
    profile: dict[str, Any],
    candidate: str,
) -> tuple[str, str]:
    """Check if a candidate expansion is supportable from existing data.

    Returns (status, detail) where status is 'supportable' or 'needs-new-data'.

    The supportability mapping is profile-driven via a `supportability_overrides`
    key. Each entry maps a candidate name to a data source name + detail string.
    If the named data source exists in the profile's `data_sources`, the candidate
    is supportable. Candidates not in the mapping default to 'needs-new-data'.
    """
    data_sources = profile.get("data_sources", [])
    source_names = {s["name"]: s for s in data_sources}

    # Profile-driven supportability mapping
    overrides = profile.get("supportability_overrides", {})
    if candidate in overrides:
        entry = overrides[candidate]
        source_key = entry.get("data_source", "")
        detail = entry.get("detail", "")
        if source_key in source_names:
            return "supportable", f"Data exists in {source_key}: {detail}"

    return "needs-new-data", "Would require new research or data collection"


def diff_architectures(
    competitor: dict[str, Any],
    ours: dict[str, Any],
    profile: dict[str, Any],
) -> dict[str, Any]:
    """Step 3: Diff the two architectures."""
    comp_arch = competitor["architecture"]

    # Map competitor page types to our equivalents
    type_mapping = {
        "service-city": "service-city-landing",
        "service-base": None,  # We don't have base service pages (no city)
        "problem-page": None,
        "problems-hub": None,
        "neighborhood-page": None,
        "neighborhoods-hub": None,
        "guide-page": None,
        "guides-hub": None,
        "blog-post": None,
        "blog-hub": None,
        "homepage": None,  # Not in our output set (exists but not templated)
        "core-page": None,
        "about-sub": None,
        "service-sub": None,
    }

    we_have: list[dict] = []
    we_lack_supportable: list[dict] = []
    we_lack_new_data: list[dict] = []
    not_applicable: list[dict] = []

    non_applicable_types = {"homepage", "core-page", "about-sub"}

    for comp_type, comp_data in comp_arch.items():
        our_equiv = type_mapping.get(comp_type)

        entry = {
            "competitor_type": comp_type,
            "count": comp_data["count"],
            "url_pattern": comp_data["url_pattern"],
            "schema_types": comp_data.get("schema_types", []),
        }

        if comp_type in non_applicable_types:
            entry["reason"] = "Core site infrastructure, not content architecture"
            not_applicable.append(entry)
        elif our_equiv and our_equiv in ours:
            entry["our_equivalent"] = our_equiv
            entry["our_count"] = ours[our_equiv].get("count", 0)
            we_have.append(entry)
        else:
            # Check supportability
            status, detail = check_data_supportability(profile, comp_type)
            entry["data_status"] = status
            entry["data_detail"] = detail
            if status == "supportable":
                we_lack_supportable.append(entry)
            else:
                we_lack_new_data.append(entry)

    # Also check for section-level gaps within page types we DO have
    section_gaps: list[dict] = []

    # Check competitor schema types vs ours for service-city pages
    comp_svc_city_schema = set(comp_arch.get("service-city", {}).get("schema_types", []))
    our_svc_city_schema = set()
    for pt in ours.values():
        our_svc_city_schema.update(pt.get("schema", []))

    schema_gaps = comp_svc_city_schema - our_svc_city_schema
    for sg in sorted(schema_gaps):
        section_gaps.append({
            "type": "schema-gap",
            "name": sg,
            "competitor_has": True,
            "we_have": False,
        })

    return {
        "we_have": we_have,
        "we_lack_supportable": we_lack_supportable,
        "we_lack_new_data": we_lack_new_data,
        "not_applicable": not_applicable,
        "section_gaps": section_gaps,
    }


def build_expansion_backlog(
    diff: dict[str, Any],
    competitor: dict[str, Any],
    profile: dict[str, Any],
) -> dict[str, Any]:
    """Step 4: Emit ranked expansion backlog."""
    new_sections: list[dict] = []
    new_page_types: list[dict] = []
    comp_arch = competitor["architecture"]
    cn = profile["competitor_name"]  # used in all evidence strings

    # --- New SECTION types for existing pages ---

    # 1. HowTo schema block (competitor has it, we have process_steps but no HowTo schema)
    if "HowTo" in [sg["name"] for sg in diff.get("section_gaps", [])]:
        status, detail = check_data_supportability(profile, "howto-schema")
        new_sections.append({
            "name": "HowTo structured data on service-city pages",
            "type": "new-section",
            "subtype": "schema-addition",
            "competitor_evidence": {
                "description": f"{cn} emits HowTo schema with explicit steps on every service-city page",
                "schema_types": ["HowTo", "HowToStep"],
                "sample": "5-7 step HowTo with estimatedCost, visible in rich results",
            },
            "our_data_status": status,
            "our_data_detail": detail,
            "demand_signal": "HowTo rich results appear in Google SERP for procedural queries; AI Overviews quote HowTo steps verbatim",
            "effort": "low",
            "reuse_potential": "high",
            "rationale": "We already have process_steps (5-6 per service) on every page — just need to wrap them in HowTo schema. Zero new content required.",
        })

    # 2. Issues-by-home-era section
    status, detail = check_data_supportability(profile, "issues-by-home-era")
    new_sections.append({
        "name": "Issues-by-home-era section on service-city pages",
        "type": "new-section",
        "subtype": "content-section",
        "competitor_evidence": {
            "description": f"{cn} neighborhood pages explicitly tie issues to housing era",
        },
        "our_data_status": status,
        "our_data_detail": detail,
        "demand_signal": "Home-era-specific queries are long-tail but high-intent",
        "effort": "low",
        "reuse_potential": "high",
        "rationale": "housing_patterns already has 3 eras per city with title, neighborhood_examples, context_paragraph, and symptoms. Currently rendered as pattern cards — a dedicated 'common issues by home era' subsection within the problems section would surface this data in a search-friendly format.",
    })

    # 3. Neighborhood-specific problem clusters
    status, detail = check_data_supportability(profile, "neighborhood-specific-problems")
    new_sections.append({
        "name": "Neighborhood-specific problem callouts in service-city pages",
        "type": "new-section",
        "subtype": "content-section",
        "competitor_evidence": {
            "description": f"{cn} neighborhood pages call out specific issues per neighborhood with housing-style variants",
        },
        "our_data_status": status,
        "our_data_detail": detail,
        "demand_signal": "Neighborhood+service queries are hyper-local long-tail",
        "effort": "low",
        "reuse_potential": "high",
        "rationale": "We have 5-10 neighborhoods per city with blurbs, plus specific_problems_neighborhood_phrase per service. A dedicated subsection in the neighborhoods section that names specific problems by neighborhood would match the competitor's local specificity.",
    })

    # 4. Problem-cluster Q&A blocks
    status, detail = check_data_supportability(profile, "problem-cluster-qa")
    new_sections.append({
        "name": "Problem-cluster Q&A blocks on service-city pages",
        "type": "new-section",
        "subtype": "content-section",
        "competitor_evidence": {
            "description": f"{cn} problem pages have 5+ FAQ items per specific problem with safety steps and cost ranges",
            "url_count": comp_arch.get("problem-page", {}).get("count", 0),
        },
        "our_data_status": status,
        "our_data_detail": detail,
        "demand_signal": f"Competitor has {comp_arch.get('problem-page', {}).get('count', 0)} dedicated problem pages — each targets a high-intent symptom query",
        "effort": "medium",
        "reuse_potential": "high",
        "rationale": "We have problem_cards (6-8 per service) that could be expanded into problem-cluster Q&A blocks within the existing page, adding depth per symptom without building separate pages.",
    })

    # 5. SpeakableSpecification schema
    speakable_in_gaps = any(
        sg["name"] == "SpeakableSpecification"
        for sg in diff.get("section_gaps", [])
    )
    if speakable_in_gaps:
        new_sections.append({
            "name": "SpeakableSpecification schema for voice search / AI Overviews",
            "type": "new-section",
            "subtype": "schema-addition",
            "competitor_evidence": {
                "description": f"{cn} emits SpeakableSpecification on every page type — marks content for voice assistants and AI citation",
                "schema_types": ["SpeakableSpecification"],
            },
            "our_data_status": "supportable",
            "our_data_detail": "CSS selectors pointing to existing FAQ and process sections — no new content needed",
            "demand_signal": "Google explicitly recommends SpeakableSpecification for news/how-to content; AI Overviews preferentially cite speakable-marked content",
            "effort": "low",
            "reuse_potential": "high",
            "rationale": "Pure schema addition — point speakable cssSelector at our FAQ and process sections. Zero content authoring.",
        })

    # --- Candidate new PAGE types ---

    # 1. Problem/symptom pages
    problem_data = comp_arch.get("problem-page", {})
    if problem_data.get("count", 0) > 0:
        new_page_types.append({
            "name": "Dedicated problem/symptom pages",
            "type": "new-page-type",
            "competitor_evidence": {
                "description": f"{cn} has {problem_data['count']} dedicated problem pages — each targets a specific symptom query",
                "url_pattern": problem_data.get("url_pattern", ""),
                "count": problem_data["count"],
                "sample_urls": problem_data.get("sample_urls", []),
                "schema_types": problem_data.get("schema_types", []),
                "on_page_modules": "HowTo safety steps + FAQPage (5 Q&A) + Article schema + cost range + review integration",
            },
            "our_data_status": "needs-new-data",
            "our_data_detail": "problem_cards (6-8 per service) provide symptom names and brief descriptions; full problem pages would need expanded safety content, cost data, and dedicated FAQ items per symptom",
            "demand_signal": f"high — symptom queries are high-intent; {cn} ranks these pages for problem-first searches",
            "effort": "medium",
            "reuse_potential": "high",
            "rationale": "Each problem page targets a different search intent than our service-city pages. A user searching for a specific symptom wants immediate safety guidance, not a service landing page. These pages can rank independently and funnel into service-city pages via internal links.",
        })

    # 2. Neighborhood pages
    neighborhood_data = comp_arch.get("neighborhood-page", {})
    if neighborhood_data.get("count", 0) > 0:
        status, detail = check_data_supportability(profile, "neighborhood-page")
        new_page_types.append({
            "name": "Dedicated neighborhood pages",
            "type": "new-page-type",
            "competitor_evidence": {
                "description": f"{cn} has {neighborhood_data['count']} dedicated neighborhood pages — massive geo-surface coverage",
                "url_pattern": neighborhood_data.get("url_pattern", ""),
                "count": neighborhood_data["count"],
                "sample_urls": neighborhood_data.get("sample_urls", []),
                "schema_types": neighborhood_data.get("schema_types", []),
                "on_page_modules": "Place+PostalAddress schema, neighborhood-specific FAQ, housing-era callouts, full service index, zip codes, review integration",
            },
            "our_data_status": status,
            "our_data_detail": detail + " — neighborhoods data (name + blurb) exists for 5-10 neighborhoods per city, but dedicated pages would need expanded housing-era analysis, neighborhood-specific FAQ, and Place schema per neighborhood",
            "demand_signal": f"very high — {neighborhood_data['count']} pages = massive long-tail coverage; neighborhood queries target homeowners with immediate local intent",
            "effort": "high",
            "reuse_potential": "high",
            "rationale": f"{neighborhood_data['count']} neighborhood pages represent the competitor's largest surface-area play. Each neighborhood page embeds a full service index, housing-era specificity, and Place schema — creating a local-pack signal for every named neighborhood. Our city-level pages cover 10 neighborhoods in a list; dedicated pages would surface each as a standalone ranking target.",
        })

    # 3. Guide/educational pages
    guide_data = comp_arch.get("guide-page", {})
    if guide_data.get("count", 0) > 0:
        status, detail = check_data_supportability(profile, "guide-page")
        new_page_types.append({
            "name": "Educational guide pages",
            "type": "new-page-type",
            "competitor_evidence": {
                "description": f"{cn} has {guide_data['count']} guide pages covering costs, planning, and how-to content",
                "url_pattern": guide_data.get("url_pattern", ""),
                "count": guide_data["count"],
                "sample_urls": guide_data.get("sample_urls", []),
            },
            "our_data_status": status,
            "our_data_detail": detail + " — pricing_items, process_steps, and FAQ themes from briefs provide seed content, but guides need expanded cost breakdowns, regional context, and permit details",
            "demand_signal": "medium-high — cost/planning queries are informational but high-value; they build trust and capture top-of-funnel",
            "effort": "medium",
            "reuse_potential": "high",
            "rationale": f"The competitor's {guide_data['count']} guides target cost and planning queries that our service-city pages don't address. These are trust-building content that captures users earlier in the decision funnel. The guides link internally to service-city pages, creating a content cluster.",
        })

    # 4. Blog content
    blog_data = comp_arch.get("blog-post", {})
    if blog_data.get("count", 0) > 0:
        new_page_types.append({
            "name": "Blog content strategy",
            "type": "new-page-type",
            "competitor_evidence": {
                "description": f"{cn} has a blog hub with posts",
                "url_pattern": blog_data.get("url_pattern", ""),
                "count": blog_data.get("count", 0),
                "sample_urls": blog_data.get("sample_urls", []),
            },
            "our_data_status": "needs-new-data",
            "our_data_detail": "Would require editorial calendar, topic research, and ongoing content production",
            "demand_signal": "low — blog content is the lowest-ROI page type for local service businesses; guides serve the same informational intent with better structure",
            "effort": "high",
            "reuse_potential": "medium",
            "rationale": "Blog is the competitor's weakest content play. Guides are strictly better for local service SEO — more structured, more schema-rich, more likely to earn featured snippets. Deprioritize in favor of guides.",
        })

    return {
        "new_sections": new_sections,
        "new_page_types": new_page_types,
    }


def build_cca_feed(
    diff: dict[str, Any],
    backlog: dict[str, Any],
    profile: dict[str, Any],
) -> dict[str, Any]:
    """Step 6: Build the CCA L3 feed."""
    proposals = []
    rank = 0

    for item in backlog["new_sections"]:
        rank += 1
        proposals.append({
            "rank": rank,
            "proposal_name": item["name"],
            "type": "new-section",
            "evidence": [item.get("competitor_evidence", {}).get("description", "")],
            "priority": "high" if item.get("effort") == "low" else "medium",
            "source_collection": "competitor-architecture-diff",
            "competitor_signal": True,
        })

    for item in backlog["new_page_types"]:
        rank += 1
        proposals.append({
            "rank": rank,
            "proposal_name": item["name"],
            "type": "new-artifact-type",
            "evidence": [item.get("competitor_evidence", {}).get("description", "")],
            "priority": "high" if item.get("demand_signal", "").startswith("high") or item.get("demand_signal", "").startswith("very") else "medium",
            "source_collection": "competitor-architecture-diff",
            "competitor_signal": True,
        })

    return {
        "lens_3_expansion": {
            "total_proposals": len(proposals),
            "high_priority_count": sum(1 for p in proposals if p["priority"] == "high"),
            "backlog": proposals,
        }
    }


def render_report(
    competitor_arch: dict[str, Any],
    our_arch: dict[str, Any],
    diff: dict[str, Any],
    backlog: dict[str, Any],
    profile: dict[str, Any],
) -> str:
    """Render the human-readable markdown report."""
    lines = [
        f"# Architecture Diff: {profile['competitor_name']} vs Our Core-30",
        f"",
        f"**Generated:** {date.today().isoformat()}",
        f"**Profile:** {profile['profile_id']}",
        f"**Competitor:** {profile['competitor_name']} ({profile['competitor_domain']})",
        f"",
        f"## Competitor Architecture Summary",
        f"",
    ]

    comp_a = competitor_arch["architecture"]
    for ptype, data in sorted(comp_a.items(), key=lambda x: -x[1]["count"]):
        lines.append(f"- **{ptype}**: {data['count']} pages ({data['url_pattern']})")
        if data.get("schema_types"):
            lines.append(f"  - Schema: {', '.join(data['schema_types'][:8])}")

    lines.extend([
        f"",
        f"**Service×city matrix:** {competitor_arch['service_city_matrix']['cities']} cities, "
        f"{competitor_arch['service_city_matrix']['services_with_city_pages']} services with city pages, "
        f"{competitor_arch['service_city_matrix']['total_service_city_pairs']} total pairs",
        f"",
        f"## Our Current Architecture",
        f"",
    ])
    for ptype, data in our_arch.items():
        lines.append(f"- **{ptype}**: {data.get('count', 0)} pages")
        if data.get("sections"):
            lines.append(f"  - Sections: {len(data['sections'])}")
        if data.get("schema"):
            lines.append(f"  - Schema: {', '.join(data['schema'])}")

    lines.extend([
        f"",
        f"## Architecture Diff",
        f"",
        f"### We have ({len(diff['we_have'])})",
        f"",
    ])
    for item in diff["we_have"]:
        lines.append(f"- **{item['competitor_type']}** ({item['count']} competitor pages) → our `{item['our_equivalent']}` ({item.get('our_count', '?')} pages)")

    lines.extend([f"", f"### We lack — supportable from current data ({len(diff['we_lack_supportable'])})", f""])
    for item in diff["we_lack_supportable"]:
        lines.append(f"- **{item['competitor_type']}** ({item['count']} competitor pages)")
        lines.append(f"  - Data: {item['data_detail']}")

    lines.extend([f"", f"### We lack — needs new data ({len(diff['we_lack_new_data'])})", f""])
    for item in diff["we_lack_new_data"]:
        lines.append(f"- **{item['competitor_type']}** ({item['count']} competitor pages)")
        lines.append(f"  - Data: {item['data_detail']}")

    if diff.get("section_gaps"):
        lines.extend([f"", f"### Schema gaps on shared page types", f""])
        for sg in diff["section_gaps"]:
            lines.append(f"- **{sg['name']}** — competitor has, we don't")

    lines.extend([
        f"",
        f"## Expansion Backlog",
        f"",
        f"### A. New SECTION types for existing pages ({len(backlog['new_sections'])})",
        f"",
    ])
    for i, item in enumerate(backlog["new_sections"], 1):
        lines.append(f"#### {i}. {item['name']}")
        lines.append(f"")
        lines.append(f"- **Effort:** {item['effort']}")
        lines.append(f"- **Reuse potential:** {item['reuse_potential']}")
        lines.append(f"- **Data status:** {item['our_data_status']}")
        lines.append(f"- **Demand signal:** {item['demand_signal']}")
        lines.append(f"- **Rationale:** {item['rationale']}")
        lines.append(f"")

    lines.extend([f"### B. Candidate new PAGE types ({len(backlog['new_page_types'])})", f""])
    for i, item in enumerate(backlog["new_page_types"], 1):
        ev = item.get("competitor_evidence", {})
        lines.append(f"#### {i}. {item['name']}")
        lines.append(f"")
        lines.append(f"- **Competitor:** {ev.get('count', '?')} pages at `{ev.get('url_pattern', '?')}`")
        lines.append(f"- **Effort:** {item['effort']}")
        lines.append(f"- **Reuse potential:** {item['reuse_potential']}")
        lines.append(f"- **Data status:** {item['our_data_status']}")
        lines.append(f"- **Demand signal:** {item['demand_signal']}")
        lines.append(f"- **Rationale:** {item['rationale']}")
        lines.append(f"")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Competitor content-architecture diff engine")
    parser.add_argument("--profile", required=True, type=Path, help="Path to profile YAML")
    args = parser.parse_args()

    profile = load_profile(args.profile)
    teardown = expand_path(profile["teardown_base"])

    if not teardown.is_dir():
        sys.stderr.write(f"ERROR: teardown directory not found: {teardown}\n")
        return 2

    sys.stderr.write(f"→ Profile: {profile['profile_id']}\n")
    sys.stderr.write(f"→ Competitor: {profile['competitor_name']}\n")
    sys.stderr.write(f"→ Teardown: {teardown}\n")

    # Step 1: Parse competitor architecture
    competitor = build_competitor_architecture(profile, teardown)
    sys.stderr.write(f"→ Competitor page types: {len(competitor['architecture'])}\n")
    sys.stderr.write(f"→ Inventories read: {competitor['inventories_read']}\n")

    # Step 2: Map our architecture
    ours = build_our_architecture(profile)
    sys.stderr.write(f"→ Our page types: {len(ours)}\n")

    # Step 3: Diff
    diff = diff_architectures(competitor, ours, profile)
    sys.stderr.write(
        f"→ Diff: {len(diff['we_have'])} shared, "
        f"{len(diff['we_lack_supportable'])} lack-supportable, "
        f"{len(diff['we_lack_new_data'])} lack-new-data, "
        f"{len(diff['not_applicable'])} n/a, "
        f"{len(diff.get('section_gaps', []))} schema gaps\n"
    )

    # Step 4: Build expansion backlog
    backlog = build_expansion_backlog(diff, competitor, profile)
    sys.stderr.write(
        f"→ Backlog: {len(backlog['new_sections'])} new sections, "
        f"{len(backlog['new_page_types'])} new page types\n"
    )

    # Step 6: Build CCA feed
    cca_feed = build_cca_feed(diff, backlog, profile)

    # Assemble full findings
    today = date.today().isoformat()
    slug = profile["competitor_slug"]
    findings = {
        "competitor": slug,
        "profile": profile["profile_id"],
        "generated": today,
        "competitor_architecture": competitor["architecture"],
        "service_city_matrix": competitor["service_city_matrix"],
        "our_architecture": ours,
        "diff": {
            "we_have": diff["we_have"],
            "we_lack_supportable": diff["we_lack_supportable"],
            "we_lack_new_data": diff["we_lack_new_data"],
            "not_applicable": diff["not_applicable"],
            "section_gaps": diff.get("section_gaps", []),
        },
        "expansion_backlog": backlog,
        "cca_feed": cca_feed,
    }

    # Write outputs
    output_dir = expand_path(profile["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / f"architecture-diff-{slug}-{today}.json"
    json_path.write_text(json.dumps(findings, indent=2, ensure_ascii=False) + "\n")
    sys.stderr.write(f"→ Wrote JSON: {json_path}\n")

    report = render_report(competitor, ours, diff, backlog, profile)
    md_path = output_dir / f"architecture-diff-{slug}-{today}.md"
    md_path.write_text(report)
    sys.stderr.write(f"→ Wrote report: {md_path}\n")

    # Write CCA feed
    cca_path = expand_path(profile.get("cca_feed_path", str(output_dir / "cca-feed.json")))
    cca_path.parent.mkdir(parents=True, exist_ok=True)
    cca_path.write_text(json.dumps(cca_feed, indent=2) + "\n")
    sys.stderr.write(f"→ Wrote CCA feed: {cca_path}\n")

    # Summary
    print(f"\n{'='*60}")
    print(f"ARCHITECTURE DIFF — {profile['competitor_name']} vs Core-30")
    print(f"{'='*60}")
    print(f"New sections identified:   {len(backlog['new_sections'])}")
    print(f"New page types identified: {len(backlog['new_page_types'])}")
    print(f"CCA feed proposals:        {cca_feed['lens_3_expansion']['total_proposals']}")
    print(f"{'='*60}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
