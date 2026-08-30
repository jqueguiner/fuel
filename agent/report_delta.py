#!/usr/bin/env python3
"""Compute source/country/live delta vs last snapshot. Writes /tmp/fuel_delta.html,
updates agent/.snapshot.json, prints the email SUBJECT. Mirrors gtfs report_delta.py."""
import os, json, csv, glob

REPO = os.environ.get("FUEL_REPO", "/home/ubuntu/fuel")
SNAP = os.path.join(REPO, "agent", ".snapshot.json")

def stat():
    countries, live, sources = set(), set(), 0
    for sj in glob.glob(os.path.join(REPO, "*", "*", "source.json")):
        try:
            s = json.load(open(sj, encoding="utf-8")).get("source", {})
        except Exception:
            continue
        sources += 1
        cc = (s.get("country") or "").upper()
        countries.add(cc)
        if s.get("per_station") and s.get("realtime"):
            live.add(cc)
    return {"sources": sources, "countries": sorted(countries), "live": sorted(live)}

def main():
    cur = stat()
    prev = {}
    if os.path.exists(SNAP):
        try: prev = json.load(open(SNAP))
        except Exception: prev = {}
    p_c, p_l = set(prev.get("countries", [])), set(prev.get("live", []))
    new_c = sorted(set(cur["countries"]) - p_c)
    new_l = sorted(set(cur["live"]) - p_l)
    gaps = {}
    if os.path.exists("/tmp/fuel_gaps.json"):
        try: gaps = json.load(open("/tmp/fuel_gaps.json"))
        except Exception: gaps = {}

    subj = "fuel: %d sources / %d countries / %d live" % (
        cur["sources"], len(cur["countries"]), len(cur["live"]))
    if new_c or new_l:
        subj += " (+%dc +%d live)" % (len(new_c), len(new_l))

    html = ["<h2>fuel catalog — coverage</h2>",
        "<p><b>%d</b> sources · <b>%d</b> countries · <b>%d</b> live per-station</p>" % (
            cur["sources"], len(cur["countries"]), len(cur["live"]))]
    if new_c: html.append("<p>🆕 new countries: %s</p>" % ", ".join(new_c))
    if new_l: html.append("<p>⛽ new live per-station: %s</p>" % ", ".join(new_l))
    if gaps.get("hunt_none"):
        html.append("<p><b>next hunt targets</b> (no data): %s</p>" % ", ".join(gaps["hunt_none"][:15]))
    if gaps.get("upgrade_avg"):
        html.append("<p><b>upgrade avg→live</b>: %s</p>" % ", ".join(gaps["upgrade_avg"][:15]))
    html.append("<p>live: %s</p>" % ", ".join(cur["live"]))
    open("/tmp/fuel_delta.html", "w", encoding="utf-8").write("\n".join(html))

    os.makedirs(os.path.dirname(SNAP), exist_ok=True)
    json.dump(cur, open(SNAP, "w"))
    print(subj)

if __name__ == "__main__":
    main()
