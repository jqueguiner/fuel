#!/usr/bin/env python3
"""Classify every target country: LIVE (per-station real-time feed) / AVG (only a
national-average number) / NONE. Rank the gaps by population -> next hunt targets.
Mirrors gtfs coverage_gaps.py. Writes /tmp/fuel_gaps.json, prints top N."""
import os, json, csv, sys, glob

REPO = os.environ.get("FUEL_REPO", "/home/ubuntu/fuel")

# ~100 countries worth covering, population (millions) for ranking.
POP = {
 "CN":1410,"IN":1430,"US":340,"ID":278,"PK":241,"NG":224,"BR":216,"BD":173,
 "RU":144,"MX":129,"JP":124,"ET":127,"PH":118,"EG":112,"VN":99,"CD":102,
 "TR":85,"IR":89,"DE":84,"TH":72,"GB":68,"FR":66,"IT":59,"ZA":60,"TZ":67,
 "MM":54,"KE":55,"KR":52,"CO":52,"ES":48,"UG":48,"AR":46,"DZ":45,"SD":48,
 "UA":37,"IQ":45,"AF":42,"PL":38,"CA":39,"MA":37,"SA":37,"UZ":35,"PE":34,
 "AO":36,"MY":34,"MZ":33,"GH":34,"YE":34,"NP":30,"VE":28,"MG":30,"CM":28,
 "CI":28,"AU":26,"NE":26,"LK":22,"BF":23,"ML":22,"RO":19,"MW":21,"CL":19,
 "KZ":19,"ZM":20,"EC":18,"SY":22,"NL":18,"SN":18,"TD":18,"SO":18,"GT":18,
 "ZW":16,"CU":11,"BE":12,"TN":12,"BO":12,"BI":13,"HT":12,"RW":14,"GR":10,
 "PT":10,"CZ":11,"HU":10,"SE":10,"AZ":10,"AE":10,"HN":10,"BY":9,"AT":9,
 "IL":9,"CH":9,"TG":9,"SL":8,"LA":8,"BG":6,"RS":7,"DK":6,"FI":6,"NO":5,
 "SG":6,"IE":5,"NZ":5,"HR":4,"LU":0.7,"SI":2,"LT":3,"LV":2,"EE":1,
}

def main():
    topn = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    live, avg = set(), set()
    for sj in glob.glob(os.path.join(REPO, "*", "*", "source.json")):
        try:
            s = json.load(open(sj, encoding="utf-8")).get("source", {})
        except Exception:
            continue
        cc = (s.get("country") or "").upper()
        if s.get("per_station") and s.get("realtime"):
            live.add(cc)
    try:
        na = json.load(open(os.path.join(REPO, "world_national_averages.json"), encoding="utf-8"))
        avg = set((na.get("prices") or {}).keys())
    except Exception:
        pass

    tiers = {"live": [], "avg_only": [], "none": []}
    for cc, pop in POP.items():
        if cc in live:
            tiers["live"].append(cc)
        elif cc in avg:
            tiers["avg_only"].append((cc, pop))
        else:
            tiers["none"].append((cc, pop))
    tiers["avg_only"].sort(key=lambda x: -x[1])
    tiers["none"].sort(key=lambda x: -x[1])

    out = {
        "live": sorted(tiers["live"]),
        "n_live": len(tiers["live"]),
        # biggest population with NO data at all -> highest-value hunt targets
        "hunt_none": [c for c, _ in tiers["none"][:topn]],
        # have only a national average -> upgrade to per-station if a feed exists
        "upgrade_avg": [c for c, _ in tiers["avg_only"][:topn]],
    }
    json.dump(out, open("/tmp/fuel_gaps.json", "w"), ensure_ascii=False, indent=1)
    print("LIVE per-station (%d): %s" % (out["n_live"], ", ".join(out["live"])))
    print("\nTOP HUNT TARGETS (no data, by population):")
    for c, p in tiers["none"][:topn]:
        print("  %s  ~%sM" % (c, p))
    print("\nUPGRADE (avg-only -> seek per-station):")
    print("  " + ", ".join(c for c, _ in tiers["avg_only"][:topn]))

if __name__ == "__main__":
    main()
