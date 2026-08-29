#!/usr/bin/env sh
DIR="$(CDPATH= cd "$(dirname "$0")" && pwd)"
curl -fsSL --max-time 40 -A 'Mozilla/5.0' "https://www.rontec-servicestations.co.uk/fuel-prices/data/fuel_prices_data.json" -o "$DIR/prices.json"
