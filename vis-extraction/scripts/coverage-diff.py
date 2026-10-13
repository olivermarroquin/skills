#!/usr/bin/env python3
"""coverage-diff.py  (VIS phase 6, fixes F1 and F3 helpers; live 2026-10-13)

Plain idea: the speaker said things that are easy to check by machine
(dollar amounts, percentages, numbers with units, names and brands, and
"for example" style stories). This lists the ones the note never mentions.
No model reading, so it costs almost no tokens.

Usage:
  python3 coverage-diff.py <transcript.md> <note.md> [--max-per-section N]
      exit 0 = CLEAN, 1 = possible misses, 2 = bad input
  python3 coverage-diff.py <transcript.md> --density
      prints words, figures, names, example cues, and DENSE yes/no
  python3 coverage-diff.py <transcript.md> --split 900 <outdir>
      writes chunk-01.txt, chunk-02.txt ... (about 900 words, cut at sentence ends)
New in v1.8 (2026-10-13, from the Saraev Part 2 run):
  python3 coverage-diff.py <transcript> --questions
      lists every question the speaker asked, with position, so the Q&A table can be checked
  python3 coverage-diff.py <transcript> --find "phrase" [--wps 3.75]
  python3 coverage-diff.py <transcript> --pivots [--wps 3.75]
      word position + ESTIMATED time of a phrase (or of common topic-switch phrases such as
      "next major step"). Use it to confirm where a part really ends before chunking.
  python3 coverage-diff.py <transcript> --time-at 12345 [--wps 3.75]
      estimated time for a word position (captions with no timestamps). Always label as estimate.
  python3 coverage-diff.py <inventory.md> <note.md> --inventory-check
      lists inventory lines whose key words never reached the note (run before the first squeeze)
  python3 coverage-diff.py <note.md> --links [<vault-root>]
      checks every [[wikilink]]: missing, ambiguous (same name in 2+ places), or [[_README]]
  Extra flag for the normal diff:  --aliases <file>
      one rule per line:  "Higsfield = Higgsfield" (caption spelling = right spelling, must be in note)
                          "Okay ! filler" (ignore on purpose, reason required; counted in the output)
                          "cue:28 ! covered in Build A" (a story cue flagged at ~28% in, already in the note)
The normal diff now ignores the note's "Coverage-diff record" and "Inventory disposition"
sections, so spelling a miss out there can no longer make a flag disappear.
Limits: spelled-out numbers ("twelve") are not checked. The story-cue check is
a word-overlap guess: treat those as leads to eyeball, not proof.
"""
import re, sys, collections, os

MULT = {"k": 1e3, "thousand": 1e3, "m": 1e6, "million": 1e6, "b": 1e9, "billion": 1e9}
NUM = r"\d[\d,]*(?:\.\d+)?"
MONEY = re.compile(r"\$\s?(" + NUM + r")\s?(k|m|b|thousand|million|billion)?\b|\b(" + NUM + r")\s?(dollars|bucks)\b", re.I)
PCT = re.compile(r"\b(" + NUM + r")\s?(%|percent)", re.I)
UNIT = re.compile(r"\b(" + NUM + r")\s?(k|m|thousand|million|billion|x|times|views|followers|subscribers|minutes|hours|days|weeks|months|years|seconds|posts|videos|pieces|people|figures)\b", re.I)
ANYNUM = re.compile(r"(" + NUM + r")\s?(k|m|thousand|million|billion)?\b", re.I)
CUES = re.compile(r"\b(for example|for instance|like when|let me give you|here'?s an example|say you|imagine|case in point|one time|the other day|i remember|good example|bad example|versus|instead of)\b", re.I)
CAPS_STOP = set("""I I'm I'll I've I'd And But So Yes No Now Well Okay OK The A An It It's That's This There Here What Why How When Where Who
Monday Tuesday Wednesday Thursday Friday Saturday Sunday January February March April May June July August September October November December
You You're You'll Your We We're They He She If Or Because Then Also Just Like Let Let's Don't Do Did Is Are Was Were Can Will""".split())
WORD_STOP = set("""about after again because before being between could doing during every first going great really right should something still their there these thing things think those through under until where which while would your""".split())

def load(path):
    t = open(path, encoding="utf-8", errors="ignore").read()
    if "## Transcript" in t:
        t = t.split("## Transcript", 1)[1]
        t = t.split("\n", 1)[1] if "\n" in t else t
    return t

def val(num, mult):
    try:
        v = float(num.replace(",", ""))
    except ValueError:
        return None
    return round(v * MULT.get((mult or "").lower(), 1), 4)

def sentences(text):
    text = re.sub(r"\[[^\]]*\]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return [s.strip() for s in re.split(r"(?<=[.?!])\s+", text) if s.strip()]

def scan(tr, note, aliases=None, ignored=None):
    aliases = aliases or {}
    nl = note.lower()
    nvals = {val(m.group(1), m.group(2)) for m in ANYNUM.finditer(note)}
    sents = sentences(tr)
    total = max(len(sents), 1)
    where = lambda i: int(100 * i / total)
    miss = collections.OrderedDict((k, []) for k in ("Money", "Percent", "Number with unit", "Names and brands", "Story or example cues"))
    seen = set()
    for i, s in enumerate(sents):
        for kind, rx in (("Money", MONEY), ("Percent", PCT), ("Number with unit", UNIT)):
            for m in rx.finditer(s):
                g = m.groups()
                v = (val(g[0], g[1]) if g[0] else val(g[2], None)) if kind == "Money" else val(g[0], g[1] if kind == "Number with unit" else None)
                if v is None or (kind, v) in seen or v in nvals:
                    continue
                seen.add((kind, v))
                miss[kind].append((m.group(0).strip(), s[:150], where(i)))
    names = collections.defaultdict(lambda: [0, "", 0])
    for i, s in enumerate(sents):
        toks = [t for t in (x.strip(".'-&") for x in re.findall(r"[A-Za-z][A-Za-z'&.\-]*", s)) if t]
        run = []
        for j, w in enumerate(toks + [""]):
            internal = bool(re.search(r"[a-z][A-Z]", w)) or (w.isupper() and len(w) > 1)
            if w[:1].isupper() and w not in CAPS_STOP and (j > 0 or internal):
                run.append(w)
            else:
                if run:
                    e = names[" ".join(run)]; e[0] += 1
                    if not e[1]: e[1], e[2] = s[:150], where(i)
                run = []
    for nm, (cnt, ctx, pos) in sorted(names.items(), key=lambda x: -x[1][0]):
        if nm.lower() in nl or all(p.lower() in nl for p in nm.split()):
            continue
        rule = aliases.get(nm.lower())
        if rule is not None:
            if rule[0] == "=" and rule[1].lower() in nl:
                continue
            if rule[0] == "!":
                if ignored is not None: ignored.append((nm, rule[1]))
                continue
        miss["Names and brands"].append((f"{nm} (said {cnt}x)", ctx, pos))
    freq = collections.Counter(w for w in re.findall(r"[a-z]{5,}", tr.lower()) if w not in WORD_STOP)
    for i, s in enumerate(sents):
        if not CUES.search(s):
            continue
        blob = " ".join(sents[i:i + 2]).lower()
        words = sorted({w for w in re.findall(r"[a-z]{5,}", blob) if w not in WORD_STOP}, key=lambda w: freq[w])[:4]
        if len(words) >= 2 and sum(1 for w in words if w in nl) * 2 < len(words):
            rule = aliases.get(f"cue:{where(i)}")
            if rule is not None and rule[0] == "!":
                if ignored is not None: ignored.append((f"cue at {where(i)}%", rule[1]))
                continue
            miss["Story or example cues"].append((CUES.search(s).group(0), " ".join(sents[i:i + 2])[:220], where(i)))
    return miss

def density(tr, raw):
    miss = scan(tr, "")
    words = len(tr.split())
    figs = sum(len(miss[k]) for k in ("Money", "Percent", "Number with unit"))
    names, cues = len(miss["Names and brands"]), len(miss["Story or example cues"])
    chapters = bool(re.search(r"(?mi)^(#+\s*chapter|\d{1,2}:\d{2}(:\d{2})?\s)", tr))
    dense = words >= 3000 and ((not chapters) or figs >= 20 or names >= 15 or cues >= 3)
    print(f"words={words} figures={figs} names={names} example_cues={cues} chapters={'yes' if chapters else 'no'}")
    print("DENSE: " + ("yes" if dense else "no"))

def split(tr, size, outdir):
    os.makedirs(outdir, exist_ok=True)
    sents = sentences(tr)
    chunks, cur, n = [], [], 0
    for s in sents:
        cur.append(s); n += len(s.split())
        if n >= size:
            chunks.append(cur); cur, n = [], 0
    if cur:
        if chunks and n < size // 3: chunks[-1] += cur
        else: chunks.append(cur)
    for i, c in enumerate(chunks, 1):
        open(os.path.join(outdir, f"chunk-{i:02d}.txt"), "w").write(" ".join(c) + "\n")
    print(f"wrote {len(chunks)} chunks to {outdir}")

def load_aliases(path):
    out = {}
    for ln in open(path, encoding="utf-8", errors="ignore"):
        ln = ln.strip()
        if not ln or ln.startswith("#"): continue
        m = re.match(r"^(.+?)\s*([=!])\s*(.+)$", ln)
        if m: out[m.group(1).strip().lower()] = (m.group(2), m.group(3).strip())
    return out

def strip_records(note):
    """Drop sections that only record decisions, so they cannot hide a miss."""
    keep, skip = [], False
    for ln in note.split("\n"):
        if re.match(r"^#{1,6}\s", ln):
            skip = bool(re.match(r"^#{1,6}\s*(coverage-diff record|inventory disposition)", ln, re.I))
        if not skip: keep.append(ln)
    return "\n".join(keep)

def fmt_time(sec):
    sec = int(round(sec)); h, r = divmod(sec, 3600); m, s_ = divmod(r, 60)
    return f"{h}:{m:02d}:{s_:02d}" if h else f"{m}:{s_:02d}"

def wps_arg(a):
    return float(a[a.index("--wps") + 1]) if "--wps" in a else 3.75

def questions(tr):
    sents = sentences(tr); total = max(len(sents), 1); n = 0
    print("# Questions the speaker asked (check each is answered or noted as open)\n")
    for i, s in enumerate(sents):
        if s.endswith("?") and len(s.split()) >= 4:
            n += 1; print(f"{n}. (~{int(100*i/total)}% in) {s[:200]}")
    print(f"\nTOTAL: {n} questions")

def find_phrase(tr, pats, wps):
    words = tr.split(); hits = 0
    for pat in pats:
        rx = re.compile(pat, re.I)
        for m in rx.finditer(tr):
            pos = len(tr[:m.start()].split())
            ctx = " ".join(words[max(0, pos - 12): pos + 25])
            hits += 1
            print(f"word {pos} (~{fmt_time(pos / wps)} ESTIMATED at {wps} words/sec): ...{ctx}...")
    print(f"\n{hits} hit(s). Times are estimates from word position, not caption timestamps.")

PIVOTS = [r"next major step", r"done with", r"move on to", r"moving on", r"next up", r"let'?s move", r"now that we'?ve", r"that'?s (it|all) for", r"in the next (section|chapter|part)"]

def key_terms(line):
    toks = re.findall(r"[A-Za-z0-9$%][A-Za-z0-9$%'.\-]*", line)
    out = []
    for j, t in enumerate(toks):
        tl = t.lower().strip(".'-")
        if re.search(r"\d", t): out.append(tl)
        elif j > 0 and t[:1].isupper() and tl not in CAPS_STOP: out.append(tl)
        elif len(tl) >= 7 and tl not in WORD_STOP: out.append(tl)
    return list(dict.fromkeys(out))

def inventory_check(inv_path, note_path):
    nl = strip_records(open(note_path, encoding="utf-8", errors="ignore").read()).lower()
    n = lines = 0
    print(f"# Inventory vs note: {os.path.basename(note_path)}\n")
    for ln in open(inv_path, encoding="utf-8", errors="ignore"):
        raw = ln.strip()
        if len(raw) < 20 or raw.startswith("#"): continue
        lines += 1
        kt = key_terms(raw)
        if len(kt) < 2: continue
        missing = [k for k in kt if k not in nl]
        if len(missing) * 2 > len(kt):
            n += 1; print(f"- {raw[:160]}\\n    not in note: {', '.join(missing[:8])}".replace("\\n", "\n"))
    print(f"\nRESULT: {n} of {lines} inventory lines look missing from the note (leads to eyeball, not proof)")
    sys.exit(0 if n == 0 else 1)

def check_links(note_path, root):
    idx = collections.defaultdict(list)
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in (".git", "node_modules", ".obsidian")]
        for f in fn:
            if not f.endswith(".md"): continue
            full = os.path.join(dp, f); idx[f[:-3].lower()].append(full)
            try:
                head = open(full, encoding="utf-8", errors="ignore").read(1500)
            except OSError: continue
            m = re.search(r"^aliases:\s*(\[.*?\]|(?:\n\s*-\s*.+)+)", head, re.M)
            if m:
                for al in re.findall(r"[^,\[\]\n\-]+", m.group(1)):
                    al = al.strip().strip("\"'")
                    if al: idx.setdefault("alias:" + al.lower(), []).append(full)
    text = strip_records(open(note_path, encoding="utf-8", errors="ignore").read())
    links = list(dict.fromkeys(re.findall(r"\[\[([^\]|#]+)", text)))
    bad = 0
    for l in links:
        k = l.strip().lower()
        if k == "_readme": print(f"- [[{l}]] AMBIGUOUS BY NAME: many folders have a _README. Link the specific MOC instead."); bad += 1; continue
        hits = idx.get(k, [])
        if not hits and ("alias:" + k) in idx: continue
        if not hits: print(f"- [[{l}]] MISSING: no note or alias with this name"); bad += 1
        elif len(hits) > 1: print(f"- [[{l}]] AMBIGUOUS: {len(hits)} notes share this name"); bad += 1
    print(f"\nRESULT: {len(links)} links checked, {bad} problem(s)")
    sys.exit(0 if bad == 0 else 1)

def main():
    a = sys.argv
    if len(a) < 3:
        print(__doc__); sys.exit(2)
    if "--inventory-check" in a:
        return inventory_check(a[1], a[2])
    if "--links" in a:
        i = a.index("--links")
        root = a[i + 1] if len(a) > i + 1 and not a[i + 1].startswith("--") else ("second-brain" if os.path.isdir("second-brain") else ".")
        return check_links(a[1], root)
    tr = load(a[1])
    if "--density" in a: return density(tr, a[1])
    if "--split" in a:
        i = a.index("--split"); return split(tr, int(a[i + 1]), a[i + 2])
    if "--questions" in a: return questions(tr)
    if "--pivots" in a: return find_phrase(tr, PIVOTS, wps_arg(a))
    if "--find" in a:
        return find_phrase(tr, [r"\s+".join(re.escape(w) for w in a[a.index("--find") + 1].split())], wps_arg(a))
    if "--time-at" in a:
        pos = int(a[a.index("--time-at") + 1]); w = wps_arg(a)
        print(f"word {pos} = about {fmt_time(pos / w)} ESTIMATED at {w} words/sec (captions had no timestamps)"); return
    aliases = load_aliases(a[a.index("--aliases") + 1]) if "--aliases" in a else {}
    cap = int(a[a.index("--max-per-section") + 1]) if "--max-per-section" in a else 40
    ignored = []
    miss = scan(tr, strip_records(open(a[2], encoding="utf-8", errors="ignore").read()), aliases, ignored)
    n = 0
    print(f"# Coverage diff: {os.path.basename(a[2])}\n")
    for kind, items in miss.items():
        print(f"## {kind}: {len(items)} possible miss(es)")
        for what, ctx, pos in items[:cap]:
            print(f"- [{what}] (~{pos}% in) \"{ctx}\"")
        if len(items) > cap: print(f"- ...and {len(items) - cap} more (raise --max-per-section)")
        n += len(items); print()
    if ignored:
        print(f"## Ignored on purpose by the alias file: {len(ignored)}")
        for nm, why in ignored: print(f"- {nm}: {why}")
        print()
    print("RESULT: " + ("CLEAN" if n == 0 else f"{n} possible misses to review"))
    sys.exit(0 if n == 0 else 1)

main()
