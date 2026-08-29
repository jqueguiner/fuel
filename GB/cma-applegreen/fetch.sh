#!/usr/bin/env sh
DIR="$(CDPATH= cd "$(dirname "$0")" && pwd)"
curl -fsSL --max-time 40 -A 'Mozilla/5.0' "https://applegreenstores.com/fuel-prices/data.json" -o "$DIR/prices.json"
