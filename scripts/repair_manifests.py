"""Repair L3 manifests in place-of a corpus re-roll (X-12).

The generator's planted list was built with a bare `value in text` check, so an
UNRENDERED draw (first2/last2/en_*/...) that coincides with template prose
became a false PII claim — he first2=חיים matched the insurance template's own
`ביטוח חיים` ("life insurance"), and the claim then reads as a LEAK the moment
the masker is precise enough to leave that prose readable (5 false LEAKs in the
he L3 [0:1000] slice, 2026-07-27). The generator is now slot-gated, but it is
UNSEEDED — regenerating would re-roll every text and void the baselines mid-
gate. This tool instead re-anchors each existing record to its template,
recovers the slot values that were actually rendered, and rebuilds `planted`
with the same slot-aware semantics as the fixed generator. Texts are untouched.

Usage:
  python repair_manifests.py --staging DIR [langs...]   # write repaired manifests + report
  (swap the staged files into data/ only when no scan is running)
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generate_raw_data as gen

DATA = "/home/yehoshua_sus/Projects/owltable/owlmask-maskbench/data"
CAT_INDEX = {"implicit": 4, "edge_case": 5, "longform": 6, "new_domains": 7, "normal": 8}
SLOT_RE = re.compile(r"(\{[A-Za-z_0-9]+\})")

# Shape-anchored patterns for structured slots (mirrors gen_* output formats).
# Without these, a lazy (.*?) mis-splits two-word values against numeric
# neighbours: "ברחוב אבן גבירול 3" parsed as street="אבן", num="גבירול 3".
TYPED = {
    "num": r"\d{1,2}",
    "id": r"[0-9A-Za-z][0-9A-Za-z \-]{4,24}",
    "ID": r"[0-9A-Za-z][0-9A-Za-z \-]{4,24}",
    "phone": r"[+(\d][\d\-\s()]{5,22}\d",
    "dob": r"\d{1,2}/\d{1,2}/\d{4}",
    "ip": r"\d{1,3}(?:\.\d{1,3}){3}",
    "mac": r"[0-9A-Fa-f]{2}(?::[0-9A-Fa-f]{2}){5}",
    "iban": r"[A-Z]{2}[0-9A-Za-z]{10,34}",
    "part_he": r"\d{9}",
    "part_en": r"\d{3}-\d{2}-\d{4}",
    # Given names are single tokens in every pool; surnames may be multi-word
    # ("בן דוד", "De Luca"). Letting first_u absorb %20-joins made the greedy
    # engine split "שרה%20בן%20דוד" as ("שרה%20בן","דוד"), losing the real
    # claim on שרה and inventing a bare דוד. No-join first, joins-allowed last
    # resolves the ambiguity the way the pools actually are.
    "first_u": r"[^\s&=?%]+",
    "last_u": r"[^\s&=?%]+(?:%20[^\s&=?%]+)*",
}

def pool_pat(values):
    """Exact alternation over a generator pool, longest-first so "De Luca"
    wins over "Luca" and "Pine St" over "Pine". Recovery of name-ish slots is
    then unambiguous BY CONSTRUCTION — every rendered value must be a pool
    member, so nothing is left to greedy/lazy guessing (which mis-split
    "Pine St, Los Angeles" and "שרה%20בן%20דוד" in the first two attempts)."""
    return "(?:" + "|".join(re.escape(v) for v in
                            sorted(values, key=len, reverse=True)) + ")"

def build_pools(lang):
    firsts, lasts, cities, streets, *_ = gen.LANG_DATA[lang]
    enc = lambda vs, f: [f(v) for v in vs]
    return {
        "first": pool_pat(firsts), "first2": pool_pat(firsts),
        "last": pool_pat(lasts), "last2": pool_pat(lasts),
        "FIRST": pool_pat(enc(firsts, str.upper)),
        "LAST": pool_pat(enc(lasts, str.upper)),
        "first_e": pool_pat(enc(firsts, lambda v: v.replace(" ", ""))),
        "last_e": pool_pat(enc(lasts, lambda v: v.replace(" ", ""))),
        "first_u": pool_pat(enc(firsts, lambda v: v.replace(" ", "%20"))),
        "last_u": pool_pat(enc(lasts, lambda v: v.replace(" ", "%20"))),
        "en_first": pool_pat(gen.en_first_names),
        "en_last": pool_pat(gen.en_last_names),
        "en_city": pool_pat(gen.en_cities),
        "city": pool_pat(cities), "street": pool_pat(streets),
    }

def compile_template(t, pools):
    parts = SLOT_RE.split(t)
    pat, slots = [], []
    for p in parts:
        if SLOT_RE.fullmatch(p):
            name = p[1:-1]
            slots.append(name)
            pat.append("(" + pools.get(name, TYPED.get(name, ".+?")) + ")")
        else:
            pat.append(re.escape(p))
    return re.compile("".join(pat) + r"\Z", re.DOTALL), slots

def recover(text, templates):
    hits = []
    for t, (rx, slots) in templates.items():
        m = rx.match(text)
        if m:
            hits.append((t, dict(zip(slots, m.groups())), len(t) - sum(len(g) for g in m.groups() if g)))
    if not hits:
        return None, None
    hits.sort(key=lambda h: -h[2])  # longest fixed text wins on ambiguity
    return hits[0][0], hits[0][1]

def rebuild(lang, template, slotvals, text):
    ntype = gen.NATIONAL_ID_TYPE[lang]
    passport_ctx = any(w in template for w in gen._PASSPORT_WORDS)
    part_t = "PASSPORT" if passport_ctx else "PART_NUMBER"
    def dec(v): return v.replace("%20", " ") if v else v
    cand = []
    def add(etype, val, identifying=True):
        if val: cand.append((etype, val, identifying))
    for s, v in slotvals.items():
        if s in ("first", "last", "first2", "last2", "en_first", "en_last",
                 "FIRST", "LAST", "first_e", "last_e"):
            add("PERSON", v)
        elif s in ("first_u", "last_u"):
            add("PERSON", dec(v))
        elif s in ("city", "en_city", "street"):
            add("LOCATION", v)
        elif s in ("id", "ID"):
            add(ntype, v)
        elif s == "phone":
            add("PHONE_NUMBER", v)
        elif s == "dob":
            add("DATE_TIME", v)
        elif s == "ip":
            add("IP_ADDRESS", v)
        elif s == "mac":
            add("MAC_ADDRESS", v)
        elif s == "iban":
            add("IBAN_CODE", v)
        elif s in ("part_he", "part_en"):
            add(part_t, v, passport_ctx)
    planted, seen = [], set()
    for etype, value, identifying in cand:
        if value and value in text and (etype, value) not in seen:
            seen.add((etype, value))
            planted.append({"entityType": etype, "value": value,
                            "identifying": identifying})
    for m in gen._EMAIL_RE.findall(text):
        if ("EMAIL_ADDRESS", m) not in seen:
            seen.add(("EMAIL_ADDRESS", m))
            planted.append({"entityType": "EMAIL_ADDRESS", "value": m,
                            "identifying": True})
    return planted

def main():
    args = sys.argv[1:]
    assert args and args[0] == "--staging", "first arg must be --staging DIR"
    staging = args[1]; langs = args[2:] or ["he", "en", "de", "es", "fr", "it"]
    os.makedirs(staging, exist_ok=True)
    for lang in langs:
        data = gen.LANG_DATA[lang]
        pools = build_pools(lang)
        tmap = {}
        for cat, idx in CAT_INDEX.items():
            tmap[cat] = {t: compile_template(t, pools) for t in data[idx]}
        texts = [r for r in open(f"{DATA}/texts-to-mask-{lang}.txt", encoding="utf-8").read().split("\n\n---\n\n") if r.strip()]
        man = [json.loads(l) for l in open(f"{DATA}/texts-to-mask-{lang}.manifest.jsonl", encoding="utf-8")]
        out, unmatched, dropped, added = [], 0, [], []
        for rec in man:
            i, cat = rec["record"], rec["category"]
            text = texts[i].rstrip("\n")
            template, slotvals = recover(text, tmap[cat])
            if template is None:
                unmatched += 1
                out.append(rec)  # keep as-is; report loudly
                continue
            new_planted = rebuild(lang, template, slotvals, text)
            old = {(p["entityType"], p["value"]) for p in rec["planted"]}
            new = {(p["entityType"], p["value"]) for p in new_planted}
            for x in old - new: dropped.append((i, *x))
            for x in new - old: added.append((i, *x))
            out.append({"record": i, "category": cat, "planted": new_planted})
        with open(f"{staging}/texts-to-mask-{lang}.manifest.jsonl", "w", encoding="utf-8") as f:
            for rec in out:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        STRUCT = {"PHONE_NUMBER", "DATE_TIME", "IP_ADDRESS", "MAC_ADDRESS",
                  "IBAN_CODE", gen.NATIONAL_ID_TYPE[lang]}
        struct_bad = [x for x in dropped if x[1] in STRUCT]
        print(f"{lang}: {len(man)} records, unmatched={unmatched}, "
              f"claims dropped={len(dropped)}, added={len(added)}, "
              f"STRUCT-DROPPED={len(struct_bad)} (must be 0)")
        for i, et, v in dropped[:8]:
            print(f"   - dropped rec {i}: {et} {v!r}")
        for i, et, v in added[:8]:
            print(f"   + added   rec {i}: {et} {v!r}")

if __name__ == "__main__":
    main()
