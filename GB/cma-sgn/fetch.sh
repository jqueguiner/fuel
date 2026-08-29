#!/usr/bin/env sh
DIR="$(CDPATH= cd "$(dirname "$0")" && pwd)"
curl -fsSL --max-time 40 -A 'Mozilla/5.0' "https://www.shell.co.uk/fuel-prices-data.html" -o "$DIR/prices.json"
