#!/usr/bin/env sh
DIR="$(CDPATH= cd "$(dirname "$0")" && pwd)"
curl -fsSL --max-time 40 -A 'Mozilla/5.0' "https://www.morrisons.com/fuel-prices/fuel.json" -o "$DIR/prices.json"
