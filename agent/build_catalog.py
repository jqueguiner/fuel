#!/usr/bin/env python3
"""Walk <CC>/<source>/source.json -> regenerate catalog.csv + README coverage line.
Deterministic tree->index, mirrors gtfs build_repo.py. No network."""
import os, json, csv, re, glob

REPO = os.environ.get("FUEL_REPO", "/home/ubuntu/fuel")

def main():
    rows = []
    countries = set()
    live = set()  # per_station + realtime (a real per-pump feed)
    for sj in sorted(glob.glob(os.path.join(REPO, "*", "*", "source.json"))):
        try:
            d = json.load(open(sj, encoding="utf-8"))
        except Exception:
            continue
        s = d.get("source", d)
        cc = (s.get("country") or os.path.basename(os.path.dirname(os.path.dirname(sj)))).upper()
        src = os.path.basename(os.path.dirname(sj))
        countries.add(cc)
        ps = bool(s.get("per_station"))
        rt = bool(s.get("realtime"))
        if ps and rt:
            live.add(cc)
        rows.append({
            "country": cc, "source": src, "name": s.get("name", ""),
            "format": s.get("format", ""),
            "key_required": "yes" if s.get("key_required") else "no",
            "realtime": "yes" if rt else "no",
            "per_station": "yes" if ps else "no",
            "coverage": s.get("coverage", ""), "url": s.get("url", ""),
        })
    rows.sort(key=lambda r: (r["country"], r["source"]))
    cat = os.path.join(REPO, "catalog.csv")
    with open(cat, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["country","source","name","format",
            "key_required","realtime","per_station","coverage","url"])
        w.writeheader(); w.writerows(rows)

    # update README coverage headline
    rd = os.path.join(REPO, "README.md")
    if os.path.exists(rd):
        t = open(rd, encoding="utf-8").read()
        line = "## Coverage (%d sources, %d countries)" % (len(rows), len(countries))
        t2 = re.sub(r"## Coverage \([^\n]*\)", line, t, count=1)
        if t2 != t:
            open(rd, "w", encoding="utf-8").write(t2)
    print(json.dumps({"sources": len(rows), "countries": len(countries),
                      "live_per_station": sorted(live)}, ensure_ascii=False))

if __name__ == "__main__":
    main()
