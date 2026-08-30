#!/usr/bin/env python3
"""Health-check every catalog source URL (HTTP status). Writes agent/health.json
{source_key: code}. Flags dead feeds so they can be pruned/refreshed. No key use."""
import os, json, csv, subprocess

REPO = os.environ.get("FUEL_REPO", "/home/ubuntu/fuel")

def code(url):
    try:
        r = subprocess.run(["curl","-sL","-m","15","-o","/dev/null","-w","%{http_code}",
                            "-A","Mozilla/5.0", url], capture_output=True, timeout=20)
        return r.stdout.decode().strip()
    except Exception:
        return "000"

def main():
    cat = os.path.join(REPO, "catalog.csv")
    if not os.path.exists(cat):
        print("{}"); return
    health, dead = {}, []
    for row in csv.DictReader(open(cat, encoding="utf-8")):
        k = row["country"] + "/" + row["source"]
        c = code(row["url"])
        health[k] = c
        if c in ("000", "404", "410", "500", "502", "503"):
            dead.append(k)
    json.dump({"health": health, "dead": dead},
              open(os.path.join(REPO, "agent", "health.json"), "w"), indent=1)
    print(json.dumps({"checked": len(health), "dead": dead}, ensure_ascii=False))

if __name__ == "__main__":
    main()
