#!/usr/bin/env python3
"""Decode website pages: JSON-LD schema + content extraction.

Supports three content-extraction paths (auto-detected per page):
  1. Next.js RSC (self.__next_f.push) — Next.js 13+ App Router
  2. Next.js __NEXT_DATA__ — Next.js 12 and below (Pages Router)
  3. HTML fallback — WordPress, Hugo, Jekyll, static HTML, any non-Next.js site

JSON-LD extraction works on all paths (it's framework-agnostic).
"""
import json, re, sys, os, glob, html as htmlmod


# ---------------------------------------------------------------------------
# JSON-LD extraction (universal — works on any site)
# ---------------------------------------------------------------------------

def extract_ldjson(html):
    blocks = re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', html, re.DOTALL)
    out = []
    for b in blocks:
        b = b.strip()
        try:
            out.append(json.loads(b))
        except Exception:
            try:
                out.append(json.loads(htmlmod.unescape(b)))
            except Exception:
                pass
    return out


def summarize_ldjson(objs):
    types = {}
    faqs = []
    def walk(o):
        if isinstance(o, dict):
            t = o.get('@type')
            if t:
                key = t if isinstance(t, str) else "/".join(t)
                types[key] = types.get(key, 0) + 1
            if o.get('@type') == 'Question':
                q = o.get('name', '')
                a = o.get('acceptedAnswer', {})
                atext = a.get('text', '') if isinstance(a, dict) else ''
                faqs.append((q, atext))
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    for o in objs:
        walk(o)
    return types, faqs


# ---------------------------------------------------------------------------
# Path 1: Next.js RSC (App Router, Next.js 13+)
# ---------------------------------------------------------------------------

def extract_rsc_text(html):
    """Pull self.__next_f.push([1,"..."]) payloads, unescape, return readable text chunks."""
    pushes = re.findall(r'self\.__next_f\.push\(\[\d+,\s*"((?:[^"\\]|\\.)*)"\]\)', html, re.DOTALL)
    decoded = []
    for p in pushes:
        try:
            s = json.loads('"' + p + '"')
        except Exception:
            s = p.encode().decode('unicode_escape', errors='ignore')
        decoded.append(s)
    blob = "".join(decoded)
    candidates = re.findall(r'[A-Z][^"\\<>{}]{24,}?[.!?:](?=\s|"|$)', blob)
    fields = re.findall(
        r'"(?:title|heading|description|content|text|answer|question|body|name|excerpt|metaDescription|h1|h2|intro)'
        r'"\s*:\s*"((?:[^"\\]|\\.){15,})"', blob
    )
    fields = [json.loads('"' + f + '"') if '\\' in f else f for f in fields]
    return blob, candidates, fields


# ---------------------------------------------------------------------------
# Path 2: Next.js __NEXT_DATA__ (Pages Router, Next.js ≤12)
# ---------------------------------------------------------------------------

def extract_next_data(html):
    """Pull <script id="__NEXT_DATA__"> JSON blob — Next.js Pages Router."""
    m = re.search(r'<script\s+id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.DOTALL)
    if not m:
        return None, [], []
    try:
        data = json.loads(m.group(1))
    except Exception:
        return None, [], []
    blob = json.dumps(data, ensure_ascii=False)
    # Extract page props content fields
    fields = re.findall(
        r'"(?:title|heading|description|content|text|answer|question|body|name|excerpt|metaDescription|h1|h2|intro)'
        r'"\s*:\s*"((?:[^"\\]|\\.){15,})"', blob
    )
    fields = [json.loads('"' + f + '"') if '\\' in f else f for f in fields]
    candidates = re.findall(r'[A-Z][^"\\<>{}]{24,}?[.!?:](?=\s|"|$)', blob)
    return blob, candidates, fields


# ---------------------------------------------------------------------------
# Path 3: HTML fallback (WordPress, Hugo, static HTML, anything else)
# ---------------------------------------------------------------------------

def extract_html_text(html):
    """Fallback: strip tags and pull readable text from raw HTML body."""
    # Extract <title>
    title_m = re.search(r'<title[^>]*>(.*?)</title>', html, re.DOTALL | re.IGNORECASE)
    title = htmlmod.unescape(title_m.group(1).strip()) if title_m else ""

    # Extract meta description
    meta_m = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', html, re.IGNORECASE)
    if not meta_m:
        meta_m = re.search(r'<meta[^>]*content=["\']([^"\']*)["\'][^>]*name=["\']description["\']', html, re.IGNORECASE)
    meta_desc = htmlmod.unescape(meta_m.group(1).strip()) if meta_m else ""

    # Extract headings
    headings = re.findall(r'<h[1-6][^>]*>(.*?)</h[1-6]>', html, re.DOTALL | re.IGNORECASE)
    headings = [re.sub(r'<[^>]+>', '', h).strip() for h in headings]
    headings = [htmlmod.unescape(h) for h in headings if h]

    # Strip all tags, pull paragraph-like text
    body_m = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL | re.IGNORECASE)
    body_html = body_m.group(1) if body_m else html
    # Remove script/style blocks
    body_clean = re.sub(r'<(script|style|noscript)[^>]*>.*?</\1>', '', body_html, flags=re.DOTALL | re.IGNORECASE)
    # Strip tags
    text = re.sub(r'<[^>]+>', ' ', body_clean)
    text = htmlmod.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()

    candidates = re.findall(r'[A-Z][^"\\<>{}]{24,}?[.!?:](?=\s|"|$)', text)

    fields = []
    if title:
        fields.append(f"[title] {title}")
    if meta_desc:
        fields.append(f"[meta-description] {meta_desc}")
    for h in headings[:50]:
        fields.append(f"[heading] {h}")

    return text, candidates, fields


# ---------------------------------------------------------------------------
# Framework detection
# ---------------------------------------------------------------------------

def detect_framework(html):
    """Detect the site framework from HTML content. Returns one of: 'nextjs-rsc', 'nextjs-data', 'html'."""
    if 'self.__next_f.push' in html:
        return 'nextjs-rsc'
    if '__NEXT_DATA__' in html:
        return 'nextjs-data'
    # Fingerprint checks (informational — still uses html fallback)
    return 'html'


def detect_platform_hints(html):
    """Return platform hints for the output header."""
    hints = []
    if 'self.__next_f.push' in html:
        hints.append('Next.js RSC (App Router)')
    if '__NEXT_DATA__' in html:
        hints.append('Next.js Pages Router')
    if 'wp-content' in html or 'wp-includes' in html:
        hints.append('WordPress')
    if re.search(r'<meta[^>]*generator[^>]*Hugo', html, re.IGNORECASE):
        hints.append('Hugo')
    if re.search(r'<meta[^>]*generator[^>]*Jekyll', html, re.IGNORECASE):
        hints.append('Jekyll')
    if re.search(r'<meta[^>]*generator[^>]*Gatsby', html, re.IGNORECASE):
        hints.append('Gatsby')
    if re.search(r'<meta[^>]*generator[^>]*Starfield|Go Daddy Website Builder', html, re.IGNORECASE):
        hints.append('GoDaddy Website Builder')
    if re.search(r'<meta[^>]*generator[^>]*Wix', html, re.IGNORECASE) or 'wixsite.com' in html:
        hints.append('Wix')
    if re.search(r'<meta[^>]*generator[^>]*Squarespace', html, re.IGNORECASE) or 'squarespace' in html.lower()[:5000]:
        hints.append('Squarespace')
    if 'data-reactroot' in html or 'data-reactid' in html:
        hints.append('React')
    if '_nuxt' in html or '__NUXT__' in html:
        hints.append('Nuxt.js')
    if 'svelte' in html.lower()[:5000]:
        hints.append('Svelte/SvelteKit')
    return hints or ['Unknown/Static HTML']


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    pdir = sys.argv[1] if len(sys.argv) > 1 else "raw/payloads"
    outdir = sys.argv[2] if len(sys.argv) > 2 else "extracted"
    os.makedirs(outdir, exist_ok=True)

    for f in sorted(glob.glob(os.path.join(pdir, "*.html"))):
        name = os.path.splitext(os.path.basename(f))[0]
        html = open(f, encoding='utf-8', errors='ignore').read()
        if len(html) < 500:
            print(f"{name}: SKIP ({len(html)} bytes)")
            continue

        # JSON-LD (always)
        objs = extract_ldjson(html)
        types, faqs = summarize_ldjson(objs)

        # Content extraction (framework-dependent)
        framework = detect_framework(html)
        platform_hints = detect_platform_hints(html)

        if framework == 'nextjs-rsc':
            blob, cands, fields = extract_rsc_text(html)
            extraction_method = "Next.js RSC (self.__next_f.push)"
        elif framework == 'nextjs-data':
            blob, cands, fields = extract_next_data(html)
            if blob is None:
                blob, cands, fields = extract_html_text(html)
                extraction_method = "Next.js __NEXT_DATA__ (parse failed, fell back to HTML)"
            else:
                extraction_method = "Next.js __NEXT_DATA__ (Pages Router)"
        else:
            blob, cands, fields = extract_html_text(html)
            extraction_method = f"HTML fallback (platform: {', '.join(platform_hints)})"

        # Write schema
        json.dump(objs, open(os.path.join(outdir, f"{name}.schema.json"), "w"), indent=1, ensure_ascii=False)

        # Write readable extract
        with open(os.path.join(outdir, f"{name}.content.txt"), "w", encoding='utf-8') as o:
            o.write(f"# {name}\n")
            o.write(f"bytes={len(html)}  ldjson_objs={len(objs)}  content_chars={len(blob) if blob else 0}\n")
            o.write(f"extraction_method: {extraction_method}\n")
            o.write(f"platform_hints: {', '.join(platform_hints)}\n\n")

            o.write("## SCHEMA @types\n")
            for t, c in sorted(types.items(), key=lambda x: -x[1]):
                o.write(f"  {c:3} {t}\n")

            o.write(f"\n## FAQ pairs ({len(faqs)})\n")
            for q, a in faqs:
                o.write(f"Q: {q}\nA: {a}\n\n")

            o.write(f"\n## Content fields ({len(fields)})\n")
            for x in fields[:120]:
                o.write(f"- {x}\n")

            o.write(f"\n## Readable sentence candidates ({len(cands)})\n")
            seen = set()
            for x in cands:
                x = x.strip()
                if x not in seen:
                    seen.add(x)
                    o.write(f"- {x}\n")

        print(f"{name}: [{framework}] schema_objs={len(objs)} types={len(types)} faqs={len(faqs)} fields={len(fields)} cands={len(cands)}")
