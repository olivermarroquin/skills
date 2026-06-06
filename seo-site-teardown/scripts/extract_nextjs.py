#!/usr/bin/env python3
"""Decode AJ Long Next.js pages: JSON-LD schema + RSC flight content -> readable text."""
import json, re, sys, os, glob, html as htmlmod

def extract_ldjson(html):
    blocks = re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', html, re.DOTALL)
    out = []
    for b in blocks:
        b = b.strip()
        try:
            out.append(json.loads(b))
        except Exception:
            # some sites concatenate; try lenient
            try:
                out.append(json.loads(htmlmod.unescape(b)))
            except Exception:
                pass
    return out

def extract_rsc_text(html):
    """Pull self.__next_f.push([1,"..."]) payloads, unescape, return readable text chunks."""
    pushes = re.findall(r'self\.__next_f\.push\(\[\d+,\s*"((?:[^"\\]|\\.)*)"\]\)', html, re.DOTALL)
    decoded = []
    for p in pushes:
        try:
            s = json.loads('"' + p + '"')  # let json unescape
        except Exception:
            s = p.encode().decode('unicode_escape', errors='ignore')
        decoded.append(s)
    blob = "".join(decoded)
    # Pull human-readable sentence-like strings: sequences with letters + spaces, >=25 chars
    candidates = re.findall(r'[A-Z][^"\\<>{}]{24,}?[.!?:](?=\s|"|$)', blob)
    # also longer quoted text fields
    fields = re.findall(r'"(?:title|heading|description|content|text|answer|question|body|name|excerpt|metaDescription|h1|h2|intro)"\s*:\s*"((?:[^"\\]|\\.){15,})"', blob)
    fields = [json.loads('"'+f+'"') if '\\' in f else f for f in fields]
    return blob, candidates, fields

def summarize_ldjson(objs):
    types = {}
    faqs = []
    def walk(o):
        if isinstance(o, dict):
            t = o.get('@type')
            if t:
                key = t if isinstance(t, str) else "/".join(t)
                types[key] = types.get(key,0)+1
            if o.get('@type') == 'Question':
                q = o.get('name','')
                a = o.get('acceptedAnswer',{})
                atext = a.get('text','') if isinstance(a,dict) else ''
                faqs.append((q, atext))
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    for o in objs: walk(o)
    return types, faqs

if __name__ == "__main__":
    pdir = sys.argv[1] if len(sys.argv)>1 else "raw/payloads"
    outdir = sys.argv[2] if len(sys.argv)>2 else "extracted"
    os.makedirs(outdir, exist_ok=True)
    for f in sorted(glob.glob(os.path.join(pdir,"*.html"))):
        name = os.path.splitext(os.path.basename(f))[0]
        html = open(f, encoding='utf-8', errors='ignore').read()
        if len(html) < 1000:
            print(f"{name}: SKIP ({len(html)} bytes)"); continue
        objs = extract_ldjson(html)
        types, faqs = summarize_ldjson(objs)
        blob, cands, fields = extract_rsc_text(html)
        # write schema
        json.dump(objs, open(os.path.join(outdir, f"{name}.schema.json"),"w"), indent=1, ensure_ascii=False)
        # write readable extract
        with open(os.path.join(outdir, f"{name}.content.txt"),"w",encoding='utf-8') as o:
            o.write(f"# {name}\nbytes={len(html)}  ldjson_objs={len(objs)}  rsc_blob_chars={len(blob)}\n\n")
            o.write("## SCHEMA @types\n")
            for t,c in sorted(types.items(), key=lambda x:-x[1]): o.write(f"  {c:3} {t}\n")
            o.write(f"\n## FAQ pairs ({len(faqs)})\n")
            for q,a in faqs: o.write(f"Q: {q}\nA: {a}\n\n")
            o.write(f"\n## Content fields ({len(fields)})\n")
            for x in fields[:120]: o.write(f"- {x}\n")
            o.write(f"\n## Readable sentence candidates ({len(cands)})\n")
            seen=set()
            for x in cands:
                x=x.strip()
                if x not in seen:
                    seen.add(x); o.write(f"- {x}\n")
        print(f"{name}: schema_objs={len(objs)} types={len(types)} faqs={len(faqs)} fields={len(fields)} cands={len(cands)}")
