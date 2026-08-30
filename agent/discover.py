#!/usr/bin/env python3
"""Autonomous source hunt. A curated list of candidate open fuel-price portals;
curl-validate each; when one responds with data AND isn't already in the repo,
write <CC>/<source>/source.json + a TODO note for map wiring. Mirrors the gtfs
scrape_* discovery pattern. Extend CANDIDATES over time -> coverage self-grows.
No key stored here; key_required sources are recorded but only probed keylessly."""
import os, json, subprocess, glob

REPO = os.environ.get("FUEL_REPO", "/home/ubuntu/fuel")

# candidate portals not yet integrated. probe = substring expected in a good response.
CANDIDATES = [
 # cc, slug, url, format, per_station, realtime, key_required, license, probe, method, body
 ("PT","dgeg","https://precoscombustiveis.dgeg.gov.pt/api/PrecoComb/GetDadosPostoMap?qtdPorPagina=5&pagina=1",
   "json-api", True, True, False, "DGEG open data", "resultado", "GET", ""),
 ("CY","consumer","https://cyprusfuelprices.info/api/stations",
   "json-api", True, True, False, "Cyprus Consumer Service", "station", "GET", ""),
 ("HR","mingor","https://mzoe-gor.gov.hr/UserDocsImages/OGP/cijene-goriva.json",
   "json", True, False, False, "MINGOR open data", "cijena", "GET", ""),
 ("EE","fuelprices","https://www.fuelprices.ee/api/v1/stations",
   "json-api", True, True, False, "fuelprices.ee", "price", "GET", ""),
 ("NZ","pumped","https://www.pumped.co.nz/api/prices",
   "json-api", True, True, False, "community", "price", "GET", ""),
 ("PL","gov-otwarte","https://api.dane.gov.pl/1.4/datasets?q=ceny+paliw",
   "json-api", False, False, False, "dane.gov.pl", "data", "GET", ""),
 ("JP","enecho","https://www.enecho.meti.go.jp/statistics/petroleum_and_lpgas/pl007/results.html",
   "html", False, True, False, "METI weekly", "", "GET", ""),
 ("TW","cpc","https://vipmember.tmtd.cpc.com.tw/openinfo/API/OpenData/ListPrice/Data",
   "json-api", False, True, False, "CPC Taiwan open", "", "GET", ""),
]

def probe(c):
    cc, slug, url, fmt, ps, rt, key, lic, sig, method, body = c
    cmd = ["curl", "-sL", "-m", "20", "-A", "Mozilla/5.0"]
    if method == "POST":
        cmd += ["-X", "POST", "-H", "Content-Type: application/json", "-d", body or "{}"]
    cmd.append(url)
    try:
        out = subprocess.run(cmd, capture_output=True, timeout=30).stdout.decode("utf-8", "ignore")
    except Exception:
        return None
    if not out or len(out) < 40:
        return None
    low = out.lower()
    if "<html" in low[:200] and fmt != "html":
        return None  # got an error page, not the feed
    if sig and sig.lower() not in low:
        return None
    return out[:200]

def main():
    existing = {os.path.basename(os.path.dirname(p)) + "@" +
                os.path.basename(os.path.dirname(os.path.dirname(p)))
                for p in glob.glob(os.path.join(REPO, "*", "*", "source.json"))}
    added = []
    for c in CANDIDATES:
        cc, slug, url, fmt, ps, rt, key, lic, sig, method, body = c
        keyname = slug + "@" + cc
        if keyname in existing:
            continue
        sample = probe(c)
        if sample is None:
            continue
        d = {"source": {
            "name": "%s (%s)" % (slug, lic),
            "country": cc, "url": url, "format": fmt, "license": lic,
            "key_required": key, "realtime": rt, "per_station": ps,
            "coverage": "national" if ps else "national-avg",
            "fuels": ["gazole", "sp95", "sp98", "gplc"],
        }, "status": "discovered",
           "_map_wired": False,
           "_note": "auto-discovered; validate schema + wire a fuel_api branch in map_server.py",
           "_sample": sample}
        dd = os.path.join(REPO, cc, slug)
        os.makedirs(dd, exist_ok=True)
        json.dump(d, open(os.path.join(dd, "source.json"), "w"),
                  ensure_ascii=False, indent=2)
        added.append(keyname)
    print(json.dumps({"discovered": added, "probed": len(CANDIDATES)}, ensure_ascii=False))

if __name__ == "__main__":
    main()
