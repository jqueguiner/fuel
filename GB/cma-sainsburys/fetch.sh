#!/usr/bin/env sh
DIR="$(CDPATH= cd "$(dirname "$0")" && pwd)"
curl -fsSL --max-time 40 -A 'Mozilla/5.0' "https://api.sainsburys.co.uk/v1/exports/latest/fuel_prices_data.json" -o "$DIR/prices.json"
