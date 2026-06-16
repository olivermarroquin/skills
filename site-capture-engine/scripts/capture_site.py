#!/usr/bin/env python3
"""site-capture-engine — main orchestrator.

Universal site capture with context-aware output.

Usage:
    python3 capture_site.py <domain> <output-dir> [options]

Context detection (from output-dir path):
    .../website-archive/old/...           → restoration context (SingleFile + restore package)
    .../competitor-research/...-teardown/ → teardown context (analysis + reproduction blueprint)

Escape hatches:
    --force-restore    Force restoration context regardless of path
    --force-teardown   Force teardown context regardless of path
    --design-capture   Enable design-capture context (additive — multi-breakpoint screenshots,
                       computed-style tokens, motion/component inventory, a11y/contrast)

Context auto-detection for design-capture:
    .../website-design/inspiration/...  → design-capture enabled automatically
    .../design-reference/...            → design-capture enabled automatically
    .../design-capture/...              → design-capture enabled automatically

Options:
    --skip-screenshots     Skip Playwright screenshot capture
    --skip-singlefile      Skip SingleFile CLI capture
    --skip-wp-export       Skip WP-cli database export
    --include-large-media  Include media files >50MB (default: metadata-only)
    --wp-url <url>         WordPress admin URL for WP-cli export
    --wp-user <user>       WordPress admin username
    --wp-pass <pass>       WordPress admin password
    --sitemap-url <url>    Custom sitemap URL (default: /sitemap.xml)
    --depth-cap <n>        Max crawl depth for recursive discovery (default: 3)
"""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request
import urllib.error
import ssl
import socket
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse, urljoin

# ---------------------------------------------------------------------------
# Context detection
# ---------------------------------------------------------------------------

def detect_context(output_dir: str, force_restore: bool = False, force_teardown: bool = False,
                   design_capture: bool = False) -> tuple:
    """Detect output context from folder path.

    Returns (primary_context, design_capture_enabled) where:
    - primary_context is 'restoration' or 'teardown'
    - design_capture_enabled is True if the design-capture context should also run (additive)

    Rules:
    - --force-restore / --force-teardown override primary context
    - .../website-archive/old/... → restoration
    - .../competitor-research/...-teardown/... → teardown
    - Ambiguous → teardown (safer default)
    - --design-capture OR design-reference paths → design_capture_enabled=True (additive)
    """
    if force_restore:
        primary = "restoration"
    elif force_teardown:
        primary = "teardown"
    else:
        normalized = output_dir.replace("\\", "/")

        if "/website-archive/old/" in normalized:
            primary = "restoration"
        elif "/competitor-research/" in normalized and "-teardown" in normalized:
            primary = "teardown"
        else:
            print(f"[context-detection] Path does not match known patterns — defaulting to 'teardown'")
            print(f"  Path: {normalized}")
            print(f"  Use --force-restore to produce a restoration package")
            primary = "teardown"

    # Design-capture: explicit flag OR path auto-detection (additive — stacks with primary)
    normalized = output_dir.replace("\\", "/")
    dc_enabled = design_capture
    if not dc_enabled:
        dc_patterns = ["/website-design/inspiration/", "/design-reference/", "/design-capture/"]
        for pat in dc_patterns:
            if pat in normalized:
                dc_enabled = True
                print(f"[context-detection] Design-capture auto-detected from path pattern: {pat}")
                break

    return primary, dc_enabled


# ---------------------------------------------------------------------------
# Sitemap discovery
# ---------------------------------------------------------------------------

def fetch_url(url: str, timeout: int = 30) -> str | None:
    """Fetch a URL and return text content, or None on failure."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "site-capture-engine/2.0"})
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  [fetch] FAIL {url}: {e}")
        return None


def discover_sitemap_urls(domain: str, sitemap_url: str | None = None) -> list[str]:
    """Discover all page URLs from sitemaps, robots.txt, or recursive crawl."""
    urls = set()
    base = domain.rstrip("/")

    # 1. Try explicit sitemap
    sitemap = sitemap_url or f"{base}/sitemap.xml"
    urls.update(_parse_sitemap(sitemap, base))

    # 2. Try robots.txt for additional sitemaps
    robots_text = fetch_url(f"{base}/robots.txt")
    if robots_text:
        for line in robots_text.splitlines():
            if line.strip().lower().startswith("sitemap:"):
                sm_url = line.split(":", 1)[1].strip()
                urls.update(_parse_sitemap(sm_url, base))

    # 3. If no URLs found, fall back to homepage
    if not urls:
        urls.add(f"{base}/")
        print(f"  [sitemap] No sitemap found — falling back to homepage only")

    return sorted(urls)


def _strip_cdata(text: str) -> str:
    """Strip CDATA wrapper if present: <![CDATA[url]]> → url."""
    m = re.match(r"<!\[CDATA\[(.*?)\]\]>", text.strip())
    return m.group(1) if m else text.strip()


def _parse_sitemap(url: str, base: str) -> set[str]:
    """Parse a sitemap (or sitemap index) and return all <loc> URLs."""
    urls = set()
    content = fetch_url(url)
    if not content:
        return urls

    # Extract all <loc> values, stripping CDATA wrappers
    raw_locs = re.findall(r"<loc>\s*(.*?)\s*</loc>", content, re.DOTALL)
    cleaned_locs = [_strip_cdata(loc) for loc in raw_locs]

    # Check if this is a sitemap index
    if "<sitemapindex" in content:
        print(f"  [sitemap] Index at {url} — {len(cleaned_locs)} sub-sitemaps")
        for sub in cleaned_locs:
            urls.update(_parse_sitemap(sub, base))
    else:
        urls.update(cleaned_locs)
        print(f"  [sitemap] {url} — {len(cleaned_locs)} URLs")

    return urls


# ---------------------------------------------------------------------------
# Capture modules (universal — run for any context)
# ---------------------------------------------------------------------------

def capture_robots_and_llms(domain: str, out_dir: str):
    """Capture robots.txt and llms.txt."""
    base = domain.rstrip("/")
    for fname in ["robots.txt", "llms.txt"]:
        content = fetch_url(f"{base}/{fname}")
        if content:
            Path(out_dir, fname).write_text(content, encoding="utf-8")
            print(f"  [capture] {fname} — {len(content)} bytes")
        else:
            print(f"  [capture] {fname} — not found (skipped)")


def capture_raw_html(url: str, out_dir: str) -> str | None:
    """Fetch raw HTML for a single URL. Returns content or None."""
    content = fetch_url(url)
    if content:
        slug = url_to_slug(url)
        fpath = Path(out_dir, "html", f"{slug}.html")
        fpath.parent.mkdir(parents=True, exist_ok=True)
        fpath.write_text(content, encoding="utf-8")
        return content
    return None


def extract_meta(html: str, url: str, out_dir: str):
    """Extract meta-data from HTML: title, meta description, OG tags, canonical, JSON-LD."""
    slug = url_to_slug(url)
    meta = {"url": url, "slug": slug}

    # Title
    m = re.search(r"<title[^>]*>(.*?)</title>", html, re.DOTALL | re.IGNORECASE)
    meta["title"] = m.group(1).strip() if m else ""

    # Meta description
    m = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', html, re.IGNORECASE)
    if not m:
        m = re.search(r'<meta[^>]*content=["\']([^"\']*)["\'][^>]*name=["\']description["\']', html, re.IGNORECASE)
    meta["meta_description"] = m.group(1).strip() if m else ""

    # Canonical
    m = re.search(r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']*)["\']', html, re.IGNORECASE)
    meta["canonical"] = m.group(1).strip() if m else ""

    # OG tags
    og = {}
    for m in re.finditer(r'<meta[^>]*property=["\']og:(\w+)["\'][^>]*content=["\']([^"\']*)["\']', html, re.IGNORECASE):
        og[m.group(1)] = m.group(2)
    meta["og"] = og

    # JSON-LD
    ld_blocks = re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', html, re.DOTALL)
    schemas = []
    for block in ld_blocks:
        try:
            schemas.append(json.loads(block.strip()))
        except json.JSONDecodeError:
            pass
    meta["json_ld"] = schemas
    meta["json_ld_types"] = _extract_schema_types(schemas)

    fpath = Path(out_dir, "meta", f"{slug}-meta.json")
    fpath.parent.mkdir(parents=True, exist_ok=True)
    json.dump(meta, open(fpath, "w"), indent=2, ensure_ascii=False)
    return meta


def _extract_schema_types(schemas: list) -> list[str]:
    """Walk JSON-LD and collect all @type values."""
    types = set()
    def walk(o):
        if isinstance(o, dict):
            t = o.get("@type")
            if t:
                types.add(t if isinstance(t, str) else "/".join(t))
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    for s in schemas:
        walk(s)
    return sorted(types)


def extract_internal_links(html: str, url: str, domain: str) -> dict:
    """Extract internal links from a page: outgoing links + anchor text."""
    parsed_domain = urlparse(domain)
    base_host = parsed_domain.netloc or parsed_domain.path

    links = []
    for m in re.finditer(r'<a\s[^>]*href=["\']([^"\'#]*)["\'][^>]*>(.*?)</a>', html, re.DOTALL | re.IGNORECASE):
        href = m.group(1).strip()
        anchor = re.sub(r"<[^>]+>", "", m.group(2)).strip()

        # Skip non-HTTP schemes (mailto:, tel:, javascript:, data:, etc.)
        if re.match(r"^(mailto|tel|javascript|data|ftp|sms):", href, re.IGNORECASE):
            continue

        # Resolve relative URLs
        full_url = urljoin(url, href)
        parsed = urlparse(full_url)

        # Only internal HTTP(S) links
        if parsed.scheme and parsed.scheme not in ("http", "https"):
            continue
        if parsed.netloc and parsed.netloc != base_host:
            continue

        links.append({
            "target": full_url,
            "anchor_text": anchor[:200],
            "path": parsed.path
        })

    return {
        "source_url": url,
        "source_slug": url_to_slug(url),
        "outgoing_internal_links": links,
        "outgoing_count": len(links)
    }


def extract_forms(html: str, url: str) -> list[dict]:
    """Extract form inventory: location, fields, action/method.

    Note: JS-rendered form plugins (WordPress CF7, Gravity Forms, WPForms) embed
    fields via shortcodes that only render in the browser. Raw HTML capture gets
    the <form> tag + action but fields may be empty. The form_plugin field
    identifies the plugin so downstream knows to expect JS-rendered fields.
    """
    forms = []
    for m in re.finditer(r"<form\s([^>]*)>(.*?)</form>", html, re.DOTALL | re.IGNORECASE):
        attrs = m.group(1)
        body = m.group(2)

        action = ""
        am = re.search(r'action=["\']([^"\']*)["\']', attrs, re.IGNORECASE)
        if am:
            action = am.group(1)

        method = "GET"
        mm = re.search(r'method=["\']([^"\']*)["\']', attrs, re.IGNORECASE)
        if mm:
            method = mm.group(1).upper()

        # Detect form plugin from class/id/action patterns
        form_plugin = None
        if "wpcf7" in attrs or "wpcf7" in action:
            form_plugin = "WordPress Contact Form 7"
        elif "gform" in attrs or "gravityform" in attrs:
            form_plugin = "Gravity Forms"
        elif "wpforms" in attrs:
            form_plugin = "WPForms"
        elif "forminator" in attrs:
            form_plugin = "Forminator"

        fields = []
        for fm in re.finditer(r'<(?:input|select|textarea)\s[^>]*(?:name=["\']([^"\']*)["\'])?[^>]*', body, re.IGNORECASE):
            name = fm.group(1) or ""
            type_m = re.search(r'type=["\']([^"\']*)["\']', fm.group(0), re.IGNORECASE)
            ftype = type_m.group(1) if type_m else "text"
            if name and ftype not in ("hidden", "submit"):
                fields.append({"name": name, "type": ftype})

        entry = {
            "action": action,
            "method": method,
            "fields": fields,
            "field_count": len(fields),
        }
        if form_plugin:
            entry["form_plugin"] = form_plugin
            if not fields:
                entry["fields_note"] = f"Fields are JS-rendered by {form_plugin}; raw HTML capture gets the form tag but not the inputs. Use Playwright/SingleFile for full field extraction."
        forms.append(entry)

    return forms


def extract_embeds(html: str) -> list[dict]:
    """Extract embed inventory: iframes, YouTube, maps, social embeds."""
    embeds = []

    # iframes
    for m in re.finditer(r'<iframe\s[^>]*src=["\']([^"\']*)["\'][^>]*>', html, re.IGNORECASE):
        src = m.group(1)
        etype = "iframe"
        if "youtube.com" in src or "youtu.be" in src:
            etype = "youtube"
        elif "google.com/maps" in src or "maps.google" in src:
            etype = "google-maps"
        elif "vimeo.com" in src:
            etype = "vimeo"
        elif "facebook.com" in src or "fb.com" in src:
            etype = "facebook"
        elif "twitter.com" in src or "x.com" in src:
            etype = "twitter"
        embeds.append({"type": etype, "src": src})

    return embeds


def extract_tracking_pixels(html: str) -> list[dict]:
    """Extract pixel/tracking script inventory: GTM, GA4, FB Pixel, Hotjar, etc."""
    trackers = []

    patterns = [
        (r"googletagmanager\.com/gtm\.js\?id=(GTM-[A-Z0-9]+)", "GTM"),
        (r"googletagmanager\.com/gtag/js\?id=((?:G|GT|AW)-[A-Z0-9]+)", "Google Tag"),
        (r"gtag\(['\"]config['\"],\s*['\"]((?:G|GT|AW)-[A-Z0-9]+)['\"]", "Google Tag"),
        (r"connect\.facebook\.net/[^/]*/fbevents\.js", "Facebook Pixel"),
        (r"fbq\('init',\s*'(\d+)'", "Facebook Pixel"),
        (r"static\.hotjar\.com/c/hotjar-(\d+)", "Hotjar"),
        (r"clarity\.ms/tag/([a-z0-9]+)", "Microsoft Clarity"),
        (r"snap\.licdn\.com/li\.lms-analytics", "LinkedIn Insight"),
        (r"bat\.bing\.com/bat\.js", "Bing UET"),
        (r"plausible\.io/js/plausible", "Plausible"),
        (r"cdn\.segment\.com/analytics\.js", "Segment"),
        (r"js\.hs-scripts\.com/(\d+)", "HubSpot"),
        (r"intercomcdn\.com/intercom", "Intercom"),
    ]

    for pattern, name in patterns:
        m = re.search(pattern, html, re.IGNORECASE)
        if m:
            tracker = {"name": name}
            if m.lastindex and m.lastindex >= 1:
                tracker["id"] = m.group(1)
            trackers.append(tracker)

    return trackers


def capture_dns_records(domain: str, out_dir: str):
    """Capture DNS records via dig."""
    parsed = urlparse(domain)
    hostname = parsed.netloc or parsed.path

    records = {}
    for rtype in ["A", "AAAA", "CNAME", "MX", "TXT", "NS"]:
        try:
            result = subprocess.run(
                ["dig", "+short", hostname, rtype],
                capture_output=True, text=True, timeout=15
            )
            lines = [l.strip() for l in result.stdout.strip().splitlines() if l.strip()]
            records[rtype] = lines
        except Exception as e:
            records[rtype] = [f"ERROR: {e}"]

    fpath = Path(out_dir, "dns-records.json")
    json.dump(records, open(fpath, "w"), indent=2)
    print(f"  [capture] DNS records — {sum(len(v) for v in records.values())} total entries")
    return records


def capture_whois(domain: str, out_dir: str):
    """Capture WHOIS snapshot. Follows referral if the first response is a TLD registry."""
    parsed = urlparse(domain)
    hostname = parsed.netloc or parsed.path

    try:
        # First query
        result = subprocess.run(
            ["whois", hostname],
            capture_output=True, text=True, timeout=30
        )
        content = result.stdout

        # If we got a TLD registry response with a refer: field, query the registrar directly
        refer_match = re.search(r"^refer:\s+(\S+)", content, re.MULTILINE)
        if refer_match and "Registrar:" not in content:
            registrar_server = refer_match.group(1)
            result2 = subprocess.run(
                ["whois", "-h", registrar_server, hostname],
                capture_output=True, text=True, timeout=30
            )
            if result2.stdout.strip():
                content = content + "\n\n--- Registrar WHOIS ---\n\n" + result2.stdout

        fpath = Path(out_dir, "whois.txt")
        fpath.write_text(content, encoding="utf-8")

        # Extract key fields (case-insensitive, handles varying formats)
        info = {}
        field_patterns = [
            ("Registrar", r"(?:Registrar|Sponsoring Registrar)\s*:\s*(.+)"),
            ("Registry Expiry Date", r"(?:Registry Expiry Date|Expir(?:y|ation) Date|paid-till)\s*:\s*(.+)"),
            ("Updated Date", r"(?:Updated Date|Last Updated|last-modified)\s*:\s*(.+)"),
            ("Creation Date", r"(?:Creation Date|Created|created)\s*:\s*(.+)"),
            ("Domain Status", r"(?:Domain Status|status)\s*:\s*(.+)"),
            ("Name Server", r"(?:Name Server|nserver)\s*:\s*(.+)"),
            ("Registrant", r"(?:Registrant Organization|Registrant Name|registrant)\s*:\s*(.+)"),
        ]
        for label, pattern in field_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
            if matches:
                info[label] = [m.strip() for m in matches]

        json.dump(info, open(Path(out_dir, "whois-summary.json"), "w"), indent=2)
        print(f"  [capture] WHOIS — {len(content)} bytes, {len(info)} fields extracted")
    except Exception as e:
        print(f"  [capture] WHOIS — FAILED: {e}")


def capture_ssl_cert(domain: str, out_dir: str):
    """Capture SSL certificate snapshot."""
    parsed = urlparse(domain)
    hostname = parsed.netloc or parsed.path

    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=10) as sock:
            with ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()

        info = {
            "subject": dict(x[0] for x in cert.get("subject", ())),
            "issuer": dict(x[0] for x in cert.get("issuer", ())),
            "notBefore": cert.get("notBefore", ""),
            "notAfter": cert.get("notAfter", ""),
            "serialNumber": cert.get("serialNumber", ""),
            "version": cert.get("version", ""),
            "subjectAltName": [x[1] for x in cert.get("subjectAltName", ())],
        }

        fpath = Path(out_dir, "ssl-certificate.json")
        json.dump(info, open(fpath, "w"), indent=2)
        print(f"  [capture] SSL cert — issuer: {info['issuer'].get('organizationName', 'unknown')}, expires: {info['notAfter']}")
    except Exception as e:
        print(f"  [capture] SSL cert — FAILED: {e}")


def check_redirects(url: str) -> list[dict]:
    """Follow redirects for a URL and record the chain."""
    chain = []
    current = url
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    for _ in range(10):  # max redirect depth
        try:
            req = urllib.request.Request(current, method="HEAD",
                                         headers={"User-Agent": "site-capture-engine/2.0"})
            handler = urllib.request.HTTPSHandler(context=ctx)
            opener = urllib.request.build_opener(handler, urllib.request.HTTPRedirectHandler)
            # Don't follow redirects automatically
            class NoRedirect(urllib.request.HTTPRedirectHandler):
                def redirect_request(self, req, fp, code, msg, headers, newurl):
                    return None
            opener = urllib.request.build_opener(handler, NoRedirect)
            resp = opener.open(req, timeout=15)
            chain.append({"url": current, "status": resp.status, "final": True})
            break
        except urllib.error.HTTPError as e:
            if e.code in (301, 302, 307, 308):
                location = e.headers.get("Location", "")
                chain.append({"url": current, "status": e.code, "redirect_to": location})
                if location:
                    current = urljoin(current, location)
                else:
                    break
            else:
                chain.append({"url": current, "status": e.code, "error": str(e)})
                break
        except Exception as e:
            chain.append({"url": current, "error": str(e)})
            break

    return chain


def check_broken_links(html: str, url: str, domain: str) -> list[dict]:
    """Check all links in HTML for broken ones (4xx/5xx)."""
    parsed_domain = urlparse(domain)
    base_host = parsed_domain.netloc or parsed_domain.path
    broken = []

    hrefs = set()
    for m in re.finditer(r'href=["\']([^"\'#]+)["\']', html, re.IGNORECASE):
        href = m.group(1).strip()
        full = urljoin(url, href)
        parsed = urlparse(full)
        # Only check same-domain links
        if parsed.netloc and parsed.netloc == base_host:
            hrefs.add(full)

    for link in sorted(hrefs):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        try:
            req = urllib.request.Request(link, method="HEAD",
                                         headers={"User-Agent": "site-capture-engine/2.0"})
            with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
                if resp.status >= 400:
                    broken.append({"url": link, "status": resp.status, "source_page": url})
        except urllib.error.HTTPError as e:
            if e.code >= 400:
                broken.append({"url": link, "status": e.code, "source_page": url})
        except Exception:
            pass  # Network errors are not "broken links"

    return broken


# ---------------------------------------------------------------------------
# WP-cli / WP REST API database export (restoration context, optional)
# ---------------------------------------------------------------------------

def export_wp_database(domain: str, out_dir: str, wp_url: str, wp_user: str, wp_pass: str) -> dict:
    """Export WordPress database via WP REST API (application password auth).

    Exports: posts, pages, media library metadata, plugin list, site options.
    Falls back to wp-content/uploads enumeration if API auth fails.
    Returns a summary dict for the manifest.
    """
    wp_dir = Path(out_dir, "wp-export")
    wp_dir.mkdir(parents=True, exist_ok=True)

    base_api = domain.rstrip("/") + "/wp-json/wp/v2"
    auth_header = _wp_auth_header(wp_user, wp_pass)
    summary = {"method": "wp-rest-api", "exports": {}, "errors": []}

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # Export each endpoint
    endpoints = {
        "pages": "/pages?per_page=100&_fields=id,title,slug,status,date,modified,link,content,excerpt",
        "posts": "/posts?per_page=100&_fields=id,title,slug,status,date,modified,link,content,excerpt,categories,tags",
        "media": "/media?per_page=100&_fields=id,title,slug,date,source_url,media_type,mime_type,alt_text,caption",
    }

    for name, endpoint in endpoints.items():
        all_items = []
        page = 1
        while True:
            url = f"{base_api}{endpoint}&page={page}"
            try:
                req = urllib.request.Request(url, headers={
                    "User-Agent": "site-capture-engine/2.0",
                    "Authorization": auth_header,
                })
                with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
                    items = json.loads(resp.read().decode("utf-8"))
                    if not items:
                        break
                    all_items.extend(items)
                    total_pages = int(resp.headers.get("X-WP-TotalPages", 1))
                    if page >= total_pages:
                        break
                    page += 1
            except urllib.error.HTTPError as e:
                summary["errors"].append(f"{name}: HTTP {e.code}")
                break
            except Exception as e:
                summary["errors"].append(f"{name}: {e}")
                break

        if all_items:
            fpath = wp_dir / f"wp-{name}.json"
            json.dump(all_items, open(fpath, "w"), indent=2, ensure_ascii=False)
            summary["exports"][name] = len(all_items)
            print(f"    {name}: {len(all_items)} items")

    # Export plugins list (requires admin)
    try:
        url = domain.rstrip("/") + "/wp-json/wp/v2/plugins"
        req = urllib.request.Request(url, headers={
            "User-Agent": "site-capture-engine/2.0",
            "Authorization": auth_header,
        })
        with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
            plugins = json.loads(resp.read().decode("utf-8"))
            fpath = wp_dir / "wp-plugins.json"
            json.dump(plugins, open(fpath, "w"), indent=2, ensure_ascii=False)
            summary["exports"]["plugins"] = len(plugins)
            print(f"    plugins: {len(plugins)} items")
    except Exception as e:
        summary["errors"].append(f"plugins: {e}")

    # Export site settings/options (public subset)
    try:
        url = domain.rstrip("/") + "/wp-json"
        req = urllib.request.Request(url, headers={"User-Agent": "site-capture-engine/2.0"})
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            site_info = json.loads(resp.read().decode("utf-8"))
            fpath = wp_dir / "wp-site-info.json"
            json.dump(site_info, open(fpath, "w"), indent=2, ensure_ascii=False)
            summary["exports"]["site_info"] = 1
            print(f"    site-info: captured")
    except Exception as e:
        summary["errors"].append(f"site_info: {e}")

    # Write summary
    json.dump(summary, open(wp_dir / "wp-export-summary.json", "w"), indent=2)
    return summary


def _wp_auth_header(user: str, password: str) -> str:
    """Build HTTP Basic auth header for WP application passwords."""
    import base64
    credentials = f"{user}:{password}"
    encoded = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    return f"Basic {encoded}"


# ---------------------------------------------------------------------------
# SingleFile capture (universal — self-contained HTML per page)
# ---------------------------------------------------------------------------

def detect_singlefile_cli() -> str | None:
    """Find the single-file CLI binary. Returns path or None."""
    for name in ["single-file", "singlefile"]:
        result = subprocess.run(["which", name], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    return None


def detect_chromium_path() -> str | None:
    """Find a Chromium binary for SingleFile. Checks Playwright cache first."""
    # Playwright Chromium
    pw_base = os.path.expanduser("~/Library/Caches/ms-playwright")
    if os.path.isdir(pw_base):
        for d in sorted(os.listdir(pw_base), reverse=True):
            if d.startswith("chromium-"):
                candidate = os.path.join(
                    pw_base, d, "chrome-mac-arm64",
                    "Google Chrome for Testing.app", "Contents", "MacOS",
                    "Google Chrome for Testing"
                )
                if os.path.isfile(candidate):
                    return candidate
                # Try x64
                candidate_x64 = os.path.join(
                    pw_base, d, "chrome-mac",
                    "Google Chrome for Testing.app", "Contents", "MacOS",
                    "Google Chrome for Testing"
                )
                if os.path.isfile(candidate_x64):
                    return candidate_x64

    # System Chrome
    system_chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if os.path.isfile(system_chrome):
        return system_chrome

    return None


def capture_singlefile(url: str, out_path: str, sf_cli: str, browser_path: str,
                       timeout_sec: int = 90) -> bool:
    """Capture a single page as a self-contained HTML file via SingleFile CLI.
    Returns True on success, False on failure."""
    try:
        cmd = [
            sf_cli,
            f"--browser-executable-path={browser_path}",
            url,
            out_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_sec)
        if result.returncode == 0 and os.path.isfile(out_path):
            size = os.path.getsize(out_path)
            if size > 1000:  # Sanity check — a real page is >1KB
                return True
            else:
                print(f"    SingleFile produced {size} bytes (too small, treating as failure)")
        else:
            stderr = result.stderr.strip()[:200] if result.stderr else ""
            print(f"    SingleFile exit {result.returncode}{': ' + stderr if stderr else ''}")
        return False
    except subprocess.TimeoutExpired:
        print(f"    SingleFile timeout ({timeout_sec}s)")
        return False
    except Exception as e:
        print(f"    SingleFile error: {e}")
        return False


# ---------------------------------------------------------------------------
# v1.1 plugin hooks (no-op — credentials missing → skipped)
# ---------------------------------------------------------------------------

def extract_asset_urls(html: str, url: str) -> list[dict]:
    """Extract image, font, video, and linked media URLs from HTML."""
    assets = []
    seen = set()

    def add(asset_url: str, asset_type: str):
        full = urljoin(url, asset_url)
        if full not in seen and full.startswith("http"):
            seen.add(full)
            assets.append({"url": full, "type": asset_type})

    # Images: <img src>, <source srcset>, og:image, CSS background-image
    for m in re.finditer(r'<img[^>]*\ssrc=["\']([^"\']+)["\']', html, re.IGNORECASE):
        add(m.group(1), "image")
    for m in re.finditer(r'srcset=["\']([^"\']+)["\']', html, re.IGNORECASE):
        for entry in m.group(1).split(","):
            parts = entry.strip().split()
            if parts:
                add(parts[0], "image")
    for m in re.finditer(r'<meta[^>]*property=["\']og:image["\'][^>]*content=["\']([^"\']+)["\']', html, re.IGNORECASE):
        add(m.group(1), "image")

    # Fonts: local url() references in inline styles/CSS
    for m in re.finditer(r'url\(["\']?([^"\')\s]+\.(?:woff2?|ttf|otf|eot))["\']?\)', html, re.IGNORECASE):
        add(m.group(1), "font")

    # Google Fonts: <link href="https://fonts.googleapis.com/css?family=...">
    for m in re.finditer(r'<link[^>]*href=["\']([^"\']*fonts\.googleapis\.com/css[^"\']*)["\']', html, re.IGNORECASE):
        gf_url = m.group(1).replace("&amp;", "&")
        add(gf_url, "google-fonts-css")

    # Videos: <video src>, <source src> within <video>
    for m in re.finditer(r'<(?:video|source)[^>]*\ssrc=["\']([^"\']+)["\']', html, re.IGNORECASE):
        src = m.group(1)
        if any(src.lower().endswith(ext) for ext in (".mp4", ".webm", ".ogg", ".mov")):
            add(src, "video")

    # Linked media: <a href="...pdf/doc/xls...">
    for m in re.finditer(r'<a[^>]*\shref=["\']([^"\']+)["\']', html, re.IGNORECASE):
        href = m.group(1)
        if any(href.lower().endswith(ext) for ext in (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".csv", ".zip")):
            add(href, "document")

    # Favicons
    for m in re.finditer(r'<link[^>]*rel=["\'](?:icon|shortcut icon|apple-touch-icon)["\'][^>]*href=["\']([^"\']+)["\']', html, re.IGNORECASE):
        add(m.group(1), "favicon")

    return assets


def download_assets(assets: list[dict], out_dir: str, include_large: bool = False,
                    size_limit_mb: int = 50) -> list[dict]:
    """Download assets to out_dir/assets/. Returns inventory with file sizes."""
    asset_dir = Path(out_dir, "assets")
    asset_dir.mkdir(parents=True, exist_ok=True)
    inventory = []

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    for asset in assets:
        url = asset["url"]
        atype = asset["type"]

        # Google Fonts CSS: fetch the CSS, parse out woff2 URLs, download those
        if atype == "google-fonts-css":
            try:
                # Google Fonts serves woff2 when User-Agent indicates a modern browser
                req = urllib.request.Request(url, headers={
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
                })
                with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
                    css_text = resp.read().decode("utf-8", errors="replace")

                # Save the CSS itself
                family_match = re.search(r"family=([^&:]+)", url)
                family_slug = (family_match.group(1).replace("+", "-").lower() if family_match
                               else "unknown-font")
                css_path = asset_dir / "font" / f"{family_slug}.css"
                css_path.parent.mkdir(parents=True, exist_ok=True)
                css_path.write_text(css_text, encoding="utf-8")
                inventory.append({
                    "url": url, "type": "google-fonts-css",
                    "file": str(css_path.relative_to(out_dir)),
                    "size_bytes": len(css_text), "status": "downloaded"
                })

                # Extract and download woff2 files from the CSS
                font_urls = re.findall(r"url\((https://fonts\.gstatic\.com/[^)]+)\)", css_text)
                for furl in font_urls:
                    fname = os.path.basename(urlparse(furl).path) or "font.woff2"
                    fpath = asset_dir / "font" / fname
                    try:
                        freq = urllib.request.Request(furl, headers={"User-Agent": "site-capture-engine/2.0"})
                        with urllib.request.urlopen(freq, timeout=15, context=ctx) as fresp:
                            fdata = fresp.read()
                            fpath.write_bytes(fdata)
                            inventory.append({
                                "url": furl, "type": "font",
                                "file": str(fpath.relative_to(out_dir)),
                                "size_bytes": len(fdata), "status": "downloaded"
                            })
                    except Exception as fe:
                        inventory.append({
                            "url": furl, "type": "font",
                            "file": str(fpath.relative_to(out_dir)),
                            "size_bytes": 0, "status": f"failed: {fe}"
                        })
            except Exception as e:
                inventory.append({
                    "url": url, "type": "google-fonts-css",
                    "file": "", "size_bytes": 0, "status": f"failed: {e}"
                })
            continue

        parsed = urlparse(url)
        fname = os.path.basename(parsed.path) or "unknown"
        fpath = asset_dir / atype / fname
        fpath.parent.mkdir(parents=True, exist_ok=True)

        try:
            req = urllib.request.Request(url, headers={"User-Agent": "site-capture-engine/2.0"})
            with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
                content_length = resp.headers.get("Content-Length")
                size_bytes = int(content_length) if content_length else 0

                # Skip large files unless opted in
                if size_bytes > size_limit_mb * 1024 * 1024 and not include_large:
                    inventory.append({
                        "url": url, "type": atype, "file": str(fpath.relative_to(out_dir)),
                        "size_bytes": size_bytes, "status": "skipped-large"
                    })
                    continue

                data = resp.read()
                fpath.write_bytes(data)
                inventory.append({
                    "url": url, "type": atype, "file": str(fpath.relative_to(out_dir)),
                    "size_bytes": len(data), "status": "downloaded"
                })
        except Exception as e:
            inventory.append({
                "url": url, "type": atype, "file": str(fpath.relative_to(out_dir)),
                "size_bytes": 0, "status": f"failed: {e}"
            })

    return inventory


def hook_lighthouse(url: str, out_dir: str):
    """v1.1 hook: Lighthouse / PageSpeed snapshot per page."""
    # TODO v1.1 — requires Lighthouse CLI or PageSpeed API credentials
    print(f"  [v1.1-hook] lighthouse — credentials missing → skipped")


def hook_axe_accessibility(url: str, out_dir: str):
    """v1.1 hook: axe-core accessibility audit per page."""
    # TODO v1.1 — requires axe-core CLI or Playwright axe integration
    print(f"  [v1.1-hook] axe-accessibility — credentials missing → skipped")


def hook_ga4_traffic(url: str, out_dir: str):
    """v1.1 hook: GA4 historical traffic snapshot per URL."""
    # TODO v1.1 — requires GA4 credentials (service account + property ID)
    print(f"  [v1.1-hook] ga4-traffic — credentials missing → skipped")


def hook_gsc_indexed_pages(domain: str, out_dir: str):
    """v1.1 hook: GSC indexed-pages snapshot."""
    # TODO v1.1 — requires GSC credentials (service account + verified property)
    print(f"  [v1.1-hook] gsc-indexed-pages — credentials missing → skipped")


def hook_gbp_listing(domain: str, out_dir: str):
    """v1.1 hook: GBP listing snapshot per location."""
    # TODO v1.1 — requires GBP API credentials + multi-location loop
    print(f"  [v1.1-hook] gbp-listing — credentials missing → skipped")


def hook_dataforseo_backlinks(domain: str, out_dir: str):
    """v1.1 hook: DataForSEO backlink-profile snapshot."""
    # TODO v1.1 — requires DataForSEO Backlinks subscription
    print(f"  [v1.1-hook] dataforseo-backlinks — credentials missing → skipped")


def hook_cookie_inventory(url: str, out_dir: str):
    """v1.1 hook: Cookie inventory (needs live browser session)."""
    # TODO v1.1 — requires Playwright live session + cookie extraction
    print(f"  [v1.1-hook] cookie-inventory — credentials missing → skipped")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def url_to_slug(url: str) -> str:
    """Convert a URL to a filesystem-safe slug."""
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    if not path:
        return "homepage"
    return re.sub(r"[^a-zA-Z0-9\-]", "-", path).strip("-") or "page"


def write_sitemap_manifest(urls: list[str], metas: list[dict], out_dir: str):
    """Write sitemap.json manifest with per-page metadata."""
    manifest = []
    for url in urls:
        slug = url_to_slug(url)
        meta = next((m for m in metas if m.get("slug") == slug), {})
        manifest.append({
            "url": url,
            "slug": slug,
            "title": meta.get("title", ""),
            "meta_description": meta.get("meta_description", ""),
            "canonical": meta.get("canonical", ""),
            "json_ld_types": meta.get("json_ld_types", []),
        })

    fpath = Path(out_dir, "sitemap.json")
    json.dump(manifest, open(fpath, "w"), indent=2, ensure_ascii=False)
    print(f"  [manifest] sitemap.json — {len(manifest)} pages")
    return manifest


# ---------------------------------------------------------------------------
# Restoration package builder (client context only)
# ---------------------------------------------------------------------------

def build_restoration_package(domain: str, out_dir: str, singlefile_results: list,
                              all_metas: list, wp_export_summary: dict | None,
                              total_pages: int = 0) -> str | None:
    """Build a zipped restoration package with SingleFile pages + raw-HTML fallback.

    For pages where SingleFile failed, falls back to the raw HTML capture with a
    disclosure in the README. Returns the zip path, or None on failure.
    """
    import zipfile

    sf_dir = Path(out_dir, "singlefile")
    html_dir = Path(out_dir, "html")

    date_str = datetime.now().strftime("%Y-%m-%d")
    pkg_dir = Path(out_dir, "restoration-package")
    pkg_dir.mkdir(parents=True, exist_ok=True)

    # Classify pages: SingleFile OK vs fallback to raw HTML
    sf_ok_slugs = set()
    sf_fail_slugs = set()
    for r in singlefile_results:
        if r["status"] == "ok":
            sf_ok_slugs.add(r["slug"])
        else:
            sf_fail_slugs.add(r["slug"])

    # Collect pages for the package
    pages_in_pkg = []  # (slug, filename, source_type)
    if sf_dir.exists():
        for sf in sorted(sf_dir.glob("*.html")):
            pages_in_pkg.append((sf.stem, sf.name, "singlefile", sf))

    # Raw-HTML fallback for failed SingleFile pages
    fallback_pages = []
    if html_dir.exists() and sf_fail_slugs:
        for slug in sorted(sf_fail_slugs):
            raw_path = html_dir / f"{slug}.html"
            if raw_path.exists():
                fallback_pages.append((slug, f"{slug}.raw.html", "raw-html-fallback", raw_path))
                pages_in_pkg.append((slug, f"{slug}.raw.html", "raw-html-fallback", raw_path))

    if not pages_in_pkg:
        print("  [restore] No pages to package — skipping restoration package")
        return None

    total_in_pkg = len(pages_in_pkg)
    sf_count = sum(1 for p in pages_in_pkg if p[2] == "singlefile")
    fallback_count = sum(1 for p in pages_in_pkg if p[2] == "raw-html-fallback")

    # 1. Generate restore-README.md
    parsed = urlparse(domain)
    site_name = parsed.netloc or domain

    # Build page list with source indicators
    page_list = ""
    for slug, fname, source, _ in pages_in_pkg:
        meta = next((m for m in all_metas if m.get("slug") == slug), {})
        title = meta.get("title", slug)
        if source == "singlefile":
            page_list += f"- **{title}** — open `pages/{fname}` in your browser\n"
        else:
            page_list += f"- **{title}** — open `pages/{fname}` *(raw HTML — see note below)*\n"

    # Fallback disclosure section
    fallback_section = ""
    if fallback_pages:
        fallback_list = "\n".join(f"- `{f[1]}` ({f[0]})" for f in fallback_pages)
        fallback_section = f"""
## Important Note About Some Pages

{fallback_count} of {total_in_pkg} pages could not be saved as fully self-contained files
(the capture tool timed out on these pages). They are included as raw HTML files instead,
which means they may need an internet connection to display images and styling correctly.

These pages have `.raw.html` in their filename:

{fallback_list}

The content (text, headings, contact information) is fully preserved in these files.
Only the visual presentation may differ when viewed offline.
"""

    wp_section = ""
    if wp_export_summary and wp_export_summary.get("exports"):
        exports = wp_export_summary["exports"]
        wp_section = f"""
## WordPress Database Export

A copy of your WordPress content is saved in the `wp-export/` folder:
- **Pages:** {exports.get('pages', 0)} pages exported
- **Posts:** {exports.get('posts', 0)} posts exported
- **Media library:** {exports.get('media', 0)} media items cataloged
- **Plugins:** {exports.get('plugins', 'not exported')} plugins recorded

These are JSON files exported via the WordPress REST API. They contain your
page content, media library catalog, and plugin configuration. A web developer
can use them to rebuild your site's content on any platform.

Note: This export uses the WordPress REST API (not a full database dump).
It captures page/post content, media metadata, and plugin list, but not
database-level settings (wp_options, post metadata, custom tables). For a
complete database-level backup, ask your hosting provider for a MySQL/phpMyAdmin
export, or use WP-CLI with SSH access to the server.
"""

    readme_content = f"""# How to View Your Website Backup

**Website:** {site_name}
**Backup date:** {date_str}
**Total pages in this package:** {total_in_pkg} of {total_pages or total_in_pkg} pages on the live site
**Self-contained pages:** {sf_count}
**Raw HTML fallback pages:** {fallback_count}

## What This Is

This is a complete backup of your website as it appeared on {date_str}.
{"All" if fallback_count == 0 else "Most"} pages have been saved as single, self-contained files that you can
open on any computer — no internet connection needed.

## How to View Your Pages

1. Open the `pages/` folder
2. Double-click any `.html` file
3. It will open in your web browser (Chrome, Firefox, Safari — any will work)
4. The page will look exactly like it did on your live website

Each self-contained file has everything — the text, images, colors, and layout
are all saved inside the single file. No internet connection is required.

## Your Pages

{page_list}
{fallback_section}
{wp_section}
## If You Need to Restore Your Website

A web developer can use these files to rebuild your site. Each page contains:
- All text content
- All images (embedded in self-contained files; linked in raw HTML files)
- The complete design and layout
- Your contact information and business details

The `meta/` folder contains structured data (titles, descriptions, schema)
that helps search engines understand your pages. The `assets/` folder has
your original image files and fonts.

## Questions?

If you need help understanding or using this backup, contact the team
that created it. This backup was made with the site-capture-engine tool.
"""

    readme_path = pkg_dir / "restore-README.md"
    readme_path.write_text(readme_content, encoding="utf-8")
    print(f"  [restore] restore-README.md — {sf_count} self-contained + {fallback_count} raw-HTML fallback")

    # 2. Build the zip
    zip_name = f"restoration-package-{date_str}.zip"
    zip_path = Path(out_dir, zip_name)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(readme_path, "restore-README.md")

        # Add all pages (SingleFile + fallback) under pages/
        for slug, fname, source, fpath in pages_in_pkg:
            zf.write(fpath, f"pages/{fname}")

        # Add meta JSONs
        meta_dir = Path(out_dir, "meta")
        if meta_dir.exists():
            for mf in sorted(meta_dir.glob("*.json")):
                zf.write(mf, f"meta/{mf.name}")

        # Add assets
        asset_dir = Path(out_dir, "assets")
        if asset_dir.exists():
            for root, dirs, files in os.walk(asset_dir):
                for f in files:
                    fp = Path(root, f)
                    arcname = f"assets/{fp.relative_to(asset_dir)}"
                    zf.write(fp, arcname)

        # Add WP export if present
        wp_dir = Path(out_dir, "wp-export")
        if wp_dir.exists():
            for wf in sorted(wp_dir.glob("*.json")):
                zf.write(wf, f"wp-export/{wf.name}")

        # Add capture manifest
        mpath = Path(out_dir, "capture-manifest.json")
        if mpath.exists():
            zf.write(mpath, "capture-manifest.json")

    zip_size = os.path.getsize(zip_path)
    print(f"  [restore] {zip_name} — {zip_size / 1024 / 1024:.1f} MB ({sf_count} self-contained + {fallback_count} fallback + assets)")
    return str(zip_path)


# ---------------------------------------------------------------------------
# Main orchestrator
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="site-capture-engine — universal site capture")
    parser.add_argument("domain", help="Target domain (e.g., https://example.com)")
    parser.add_argument("output_dir", help="Output directory")
    parser.add_argument("--force-restore", action="store_true", help="Force restoration context")
    parser.add_argument("--force-teardown", action="store_true", help="Force teardown context")
    parser.add_argument("--design-capture", action="store_true", help="Enable design-capture context (additive — stacks with restoration/teardown)")
    parser.add_argument("--skip-screenshots", action="store_true")
    parser.add_argument("--skip-singlefile", action="store_true")
    parser.add_argument("--skip-wp-export", action="store_true")
    parser.add_argument("--include-large-media", action="store_true")
    parser.add_argument("--wp-url", default="")
    parser.add_argument("--wp-user", default="")
    parser.add_argument("--wp-pass", default="")
    parser.add_argument("--sitemap-url", default="")
    parser.add_argument("--depth-cap", type=int, default=3)
    args = parser.parse_args()

    domain = args.domain.rstrip("/")
    out_dir = os.path.abspath(args.output_dir)
    os.makedirs(out_dir, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    context, design_capture = detect_context(out_dir, args.force_restore, args.force_teardown, args.design_capture)

    print(f"\n{'='*60}")
    print(f"site-capture-engine v2.1")
    print(f"{'='*60}")
    print(f"Domain:    {domain}")
    print(f"Output:    {out_dir}")
    print(f"Context:   {context}{' + design-capture' if design_capture else ''}")
    print(f"Timestamp: {timestamp}")
    print(f"{'='*60}\n")

    # ---- Phase 1: Discovery ----
    print("[Phase 1] Sitemap discovery...")
    urls = discover_sitemap_urls(domain, args.sitemap_url or None)
    print(f"  Discovered {len(urls)} URLs\n")

    # ---- Phase 2: robots.txt + llms.txt ----
    print("[Phase 2] robots.txt + llms.txt...")
    capture_robots_and_llms(domain, out_dir)
    print()

    # ---- Phase 3: Per-page capture (universal) ----
    print(f"[Phase 3] Per-page capture ({len(urls)} pages)...")
    all_metas = []
    all_links = []
    all_forms = []
    all_embeds = []
    all_trackers = []
    all_redirects = []
    all_broken = []
    all_asset_urls = []

    for i, url in enumerate(urls, 1):
        slug = url_to_slug(url)
        print(f"  [{i}/{len(urls)}] {slug}...")

        # Raw HTML
        html = capture_raw_html(url, out_dir)
        if not html:
            print(f"    SKIP — fetch failed")
            continue

        # Meta-data audit
        meta = extract_meta(html, url, out_dir)
        all_metas.append(meta)

        # Internal links
        links = extract_internal_links(html, url, domain)
        all_links.append(links)

        # Forms
        forms = extract_forms(html, url)
        if forms:
            all_forms.append({"url": url, "slug": slug, "forms": forms})

        # Embeds
        embeds = extract_embeds(html)
        if embeds:
            all_embeds.append({"url": url, "slug": slug, "embeds": embeds})

        # Tracking pixels (only on first page to avoid redundancy — site-wide)
        if i == 1:
            trackers = extract_tracking_pixels(html)
            all_trackers = trackers

        # Asset URLs (collect for batch download after page loop)
        page_assets = extract_asset_urls(html, url)
        all_asset_urls.extend(page_assets)

        # Redirect check
        redirect_chain = check_redirects(url)
        if len(redirect_chain) > 1 or (redirect_chain and redirect_chain[0].get("status") in (301, 302, 307, 308)):
            all_redirects.append({"url": url, "chain": redirect_chain})

        # v1.1 hooks (fire once per page, log skip)
        if i == 1:
            hook_lighthouse(url, out_dir)
            hook_axe_accessibility(url, out_dir)
            hook_ga4_traffic(url, out_dir)
            hook_cookie_inventory(url, out_dir)

    print()

    # ---- Phase 4: Broken link check (all pages, deduplicated) ----
    print(f"[Phase 4] Broken link inventory ({len(urls)} pages)...")
    # Collect all unique internal hrefs across all pages first, then check each once
    all_hrefs_by_source = {}  # href → first source page
    parsed_domain = urlparse(domain)
    base_host = parsed_domain.netloc or parsed_domain.path
    for url in urls:
        slug = url_to_slug(url)
        html_path = Path(out_dir, "html", f"{slug}.html")
        if html_path.exists():
            html_content = html_path.read_text(encoding="utf-8", errors="replace")
            for m in re.finditer(r'href=["\']([^"\'#]+)["\']', html_content, re.IGNORECASE):
                href = m.group(1).strip()
                if re.match(r"^(mailto|tel|javascript|data):", href, re.IGNORECASE):
                    continue
                full = urljoin(url, href)
                p = urlparse(full)
                if p.netloc and p.netloc == base_host and full not in all_hrefs_by_source:
                    all_hrefs_by_source[full] = url

    print(f"  Checking {len(all_hrefs_by_source)} unique internal links...")
    checked = 0
    bl_ctx = ssl.create_default_context()
    bl_ctx.check_hostname = False
    bl_ctx.verify_mode = ssl.CERT_NONE
    for link, source_page in all_hrefs_by_source.items():
        try:
            req = urllib.request.Request(link, method="HEAD",
                                         headers={"User-Agent": "site-capture-engine/2.0"})
            with urllib.request.urlopen(req, timeout=5, context=bl_ctx) as resp:
                if resp.status >= 400:
                    all_broken.append({"url": link, "status": resp.status, "source_page": source_page})
        except urllib.error.HTTPError as e:
            if e.code >= 400:
                all_broken.append({"url": link, "status": e.code, "source_page": source_page})
        except Exception:
            pass
        checked += 1
    print(f"  Found {len(all_broken)} broken links (checked {checked} unique links from {len(urls)} pages)\n")

    # ---- Phase 4b: SingleFile capture (self-contained HTML per page) ----
    sf_cli = detect_singlefile_cli()
    chromium_path = detect_chromium_path()
    singlefile_results = []
    if args.skip_singlefile:
        print("[Phase 4b] SingleFile — skipped (--skip-singlefile)")
    elif not sf_cli:
        print("[Phase 4b] SingleFile — SKIPPED (single-file CLI not found; install: npm install -g single-file-cli)")
    elif not chromium_path:
        print("[Phase 4b] SingleFile — SKIPPED (no Chromium found; install: npx playwright install chromium)")
    else:
        sf_dir = Path(out_dir, "singlefile")
        sf_dir.mkdir(parents=True, exist_ok=True)
        # Dedup URLs by slug — one capture per unique page
        seen_slugs = set()
        unique_sf_urls = []
        for url in urls:
            slug = url_to_slug(url)
            if slug not in seen_slugs:
                seen_slugs.add(slug)
                unique_sf_urls.append((url, slug))
        print(f"[Phase 4b] SingleFile capture ({len(unique_sf_urls)} unique pages from {len(urls)} sitemap URLs)...")
        print(f"  CLI: {sf_cli}")
        print(f"  Browser: {chromium_path}")
        for i, (url, slug) in enumerate(unique_sf_urls, 1):
            sf_path = str(sf_dir / f"{slug}.html")
            ok = capture_singlefile(url, sf_path, sf_cli, chromium_path)
            status = "ok" if ok else "FAIL"
            size = os.path.getsize(sf_path) if ok else 0
            singlefile_results.append({"url": url, "slug": slug, "status": status, "size_bytes": size})
            if ok:
                print(f"  [{i}/{len(unique_sf_urls)}] {slug} — {size:,} bytes")
            else:
                print(f"  [{i}/{len(unique_sf_urls)}] {slug} — FAILED")
        sf_ok = sum(1 for r in singlefile_results if r["status"] == "ok")
        print(f"  SingleFile: {sf_ok}/{len(unique_sf_urls)} unique pages captured\n")
    print()

    # ---- Phase 5: DNS / WHOIS / SSL ----
    print("[Phase 5] Infrastructure snapshots...")
    capture_dns_records(domain, out_dir)
    capture_whois(domain, out_dir)
    capture_ssl_cert(domain, out_dir)

    # v1.1 domain-level hooks
    hook_gsc_indexed_pages(domain, out_dir)
    hook_gbp_listing(domain, out_dir)
    hook_dataforseo_backlinks(domain, out_dir)
    print()

    # ---- Phase 5a: WP database export (if credentials provided) ----
    wp_export_summary = None
    if args.skip_wp_export:
        print("[Phase 5a] WP export — skipped (--skip-wp-export)\n")
    elif not args.wp_user or not args.wp_pass:
        print("[Phase 5a] WP export — skipped (no --wp-user / --wp-pass provided)")
        print("  To export: --wp-user <user> --wp-pass <application-password>\n")
    else:
        print(f"[Phase 5a] WP database export via REST API...")
        print(f"  User: {args.wp_user}")
        wp_export_summary = export_wp_database(domain, out_dir, args.wp_url or domain,
                                                args.wp_user, args.wp_pass)
        if wp_export_summary["errors"]:
            print(f"  Errors: {wp_export_summary['errors']}")
        total_exported = sum(wp_export_summary["exports"].values())
        print(f"  Total exported: {total_exported} items across {len(wp_export_summary['exports'])} endpoints\n")

    # ---- Phase 5b: Asset download ----
    # Deduplicate asset URLs across all pages
    seen_asset_urls = set()
    unique_assets = []
    for a in all_asset_urls:
        if a["url"] not in seen_asset_urls:
            seen_asset_urls.add(a["url"])
            unique_assets.append(a)
    print(f"[Phase 5b] Asset download ({len(unique_assets)} unique assets across {len(all_asset_urls)} refs)...")
    asset_inventory = download_assets(unique_assets, out_dir, args.include_large_media)
    downloaded = sum(1 for a in asset_inventory if a["status"] == "downloaded")
    skipped = sum(1 for a in asset_inventory if a["status"] == "skipped-large")
    failed = sum(1 for a in asset_inventory if a["status"].startswith("failed"))
    print(f"  Downloaded: {downloaded}, Skipped (large): {skipped}, Failed: {failed}\n")

    # ---- Phase 6: Write aggregate outputs ----
    print("[Phase 6] Writing aggregate outputs...")

    # Sitemap manifest
    write_sitemap_manifest(urls, all_metas, out_dir)

    # Internal linking graph
    link_path = Path(out_dir, "internal-link-graph.json")
    json.dump(all_links, open(link_path, "w"), indent=2, ensure_ascii=False)
    print(f"  [output] internal-link-graph.json — {len(all_links)} pages")

    # Redirect map
    redirect_path = Path(out_dir, "redirect-map.json")
    json.dump(all_redirects, open(redirect_path, "w"), indent=2, ensure_ascii=False)
    print(f"  [output] redirect-map.json — {len(all_redirects)} redirects")

    # Broken link inventory
    broken_path = Path(out_dir, "broken-links.json")
    json.dump(all_broken, open(broken_path, "w"), indent=2, ensure_ascii=False)
    print(f"  [output] broken-links.json — {len(all_broken)} broken links")

    # Form inventory
    form_path = Path(out_dir, "form-inventory.json")
    json.dump(all_forms, open(form_path, "w"), indent=2, ensure_ascii=False)
    print(f"  [output] form-inventory.json — {len(all_forms)} pages with forms")

    # Embed inventory
    embed_path = Path(out_dir, "embed-inventory.json")
    json.dump(all_embeds, open(embed_path, "w"), indent=2, ensure_ascii=False)
    print(f"  [output] embed-inventory.json — {len(all_embeds)} pages with embeds")

    # Tracking pixel inventory
    tracker_path = Path(out_dir, "tracking-pixels.json")
    json.dump(all_trackers, open(tracker_path, "w"), indent=2, ensure_ascii=False)
    print(f"  [output] tracking-pixels.json — {len(all_trackers)} trackers")

    # Asset inventory
    asset_inv_path = Path(out_dir, "asset-inventory.json")
    json.dump(asset_inventory, open(asset_inv_path, "w"), indent=2, ensure_ascii=False)
    print(f"  [output] asset-inventory.json — {len(asset_inventory)} assets ({downloaded} downloaded)")

    # SingleFile results
    if singlefile_results:
        sf_results_path = Path(out_dir, "singlefile-results.json")
        json.dump(singlefile_results, open(sf_results_path, "w"), indent=2, ensure_ascii=False)
        sf_ok = sum(1 for r in singlefile_results if r["status"] == "ok")
        print(f"  [output] singlefile-results.json — {sf_ok}/{len(singlefile_results)} pages")

    # Capture manifest
    sf_ok_count = sum(1 for r in singlefile_results if r["status"] == "ok") if singlefile_results else 0
    manifest = {
        "engine": "site-capture-engine",
        "version": "2.0",
        "domain": domain,
        "context": context,
        "timestamp": timestamp,
        "pages_discovered": len(urls),
        "pages_captured": len(all_metas),
        "singlefile_captured": sf_ok_count,
        "singlefile_skipped": not bool(singlefile_results),
        "broken_links_found": len(all_broken),
        "broken_links_pages_checked": len(urls),
        "redirects_found": len(all_redirects),
        "forms_found": sum(len(f["forms"]) for f in all_forms),
        "forms_note": "CF7 shortcode-rendered fields may not be captured from raw HTML; JS rendering needed for complete field extraction",
        "embeds_found": sum(len(e["embeds"]) for e in all_embeds),
        "trackers_found": len(all_trackers),
        "assets_total": len(asset_inventory),
        "assets_downloaded": downloaded,
        "assets_skipped_large": skipped,
        "assets_failed": failed,
        "wp_export": (
            {**wp_export_summary, "method_note": "WP REST API export (pages/media/plugins/site-info). Does NOT include wp_options, postmeta, custom tables, or full DB structure. For complete database-level backup, use wp-cli with SSH or a MySQL/phpMyAdmin export from the hosting provider."}
            if wp_export_summary
            else {"status": "skipped", "reason": "no credentials provided (pass --wp-user and --wp-pass to export)"}
        ),
        "v1_1_hooks_skipped": [
            "lighthouse", "axe-accessibility", "ga4-traffic",
            "gsc-indexed-pages", "gbp-listing", "dataforseo-backlinks",
            "cookie-inventory"
        ],
    }
    manifest_path = Path(out_dir, "capture-manifest.json")
    json.dump(manifest, open(manifest_path, "w"), indent=2)
    print(f"  [output] capture-manifest.json")

    # ---- Phase 7: Context-specific output ----
    restoration_zip = None
    if context == "restoration":
        print("[Phase 7] Building restoration package...")
        restoration_zip = build_restoration_package(
            domain, out_dir, singlefile_results, all_metas, wp_export_summary,
            total_pages=len(urls)
        )
        if restoration_zip:
            manifest["restoration_package"] = restoration_zip
            # Re-write manifest with restoration info
            json.dump(manifest, open(manifest_path, "w"), indent=2)
        print()

    # ---- Phase 7b: Design-capture context (additive) ----
    if design_capture:
        print("[Phase 7b] Design-capture context...")
        scripts_dir = Path(__file__).resolve().parent
        dc_out = os.path.join(out_dir, "design-capture")
        os.makedirs(dc_out, exist_ok=True)

        # 1. Extract design tokens (also writes motion-inventory, component-inventory, a11y-snapshot, design-capture-manifest)
        token_script = scripts_dir / "extract_design_tokens.mjs"
        if token_script.exists():
            print("  [7b.1] Extracting computed-style design tokens...")
            result = subprocess.run(
                ["node", str(token_script), domain, dc_out],
                capture_output=True, text=True, timeout=120
            )
            if result.returncode == 0:
                print(f"  [output] design-tokens.json, design-tokens.md, motion-inventory.json, component-inventory.json, a11y-snapshot.json, design-capture-manifest.json")
                for line in result.stdout.strip().split("\n"):
                    if line.startswith("  "):
                        print(f"    {line.strip()}")
            else:
                print(f"  [WARN] Token extraction failed: {result.stderr[:200]}")
        else:
            print(f"  [WARN] extract_design_tokens.mjs not found at {token_script}")

        # 2. Multi-breakpoint screenshots with design-capture extensions
        screenshot_script = scripts_dir / "capture_screenshots.mjs"
        if screenshot_script.exists() and not args.skip_screenshots:
            print("  [7b.2] Multi-breakpoint design screenshots...")
            sc_args = ["node", str(screenshot_script), domain, dc_out, "--design-capture"]
            # Write a urls.txt from captured page list for the screenshot script
            urls_file = os.path.join(dc_out, "_urls.txt")
            with open(urls_file, "w") as f:
                for u in urls[:20]:  # cap at 20 pages for screenshot pass
                    f.write(u + "\n")
            sc_args.insert(3, urls_file)
            result = subprocess.run(sc_args, capture_output=True, text=True, timeout=600)
            if result.returncode == 0:
                # Count screenshots from output
                sc_lines = [l for l in result.stdout.split("\n") if l.startswith("ok") or "screenshot" in l.lower()]
                print(f"  [output] screenshots/ + screenshot-manifest.json ({len(sc_lines)} log lines)")
            else:
                print(f"  [WARN] Screenshot capture failed: {result.stderr[:200]}")
        elif args.skip_screenshots:
            print("  [7b.2] Design screenshots — SKIPPED (--skip-screenshots)")

        manifest["design_capture"] = {
            "enabled": True,
            "output_dir": dc_out,
            "artifacts": ["design-tokens.json", "design-tokens.md", "motion-inventory.json",
                          "component-inventory.json", "a11y-snapshot.json", "design-capture-manifest.json",
                          "screenshot-manifest.json"],
        }
        json.dump(manifest, open(manifest_path, "w"), indent=2)
        print()

    print(f"\n{'='*60}")
    print(f"Capture complete: {len(all_metas)}/{len(urls)} pages")
    print(f"Context: {context}{' + design-capture' if design_capture else ''}")
    if context == "restoration" and restoration_zip:
        print(f"Restoration package: {restoration_zip}")
    elif context == "teardown":
        print(f"Next: run teardown analysis passes (SKILL.md Pass 1-6)")
    if design_capture:
        print(f"Design-capture: {os.path.join(out_dir, 'design-capture')}/")
    print(f"{'='*60}\n")

    return manifest


if __name__ == "__main__":
    main()
