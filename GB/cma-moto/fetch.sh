#!/usr/bin/env sh
DIR="$(CDPATH= cd "$(dirname "$0")" && pwd)"
curl -fsSL --max-time 40 -A 'Mozilla/5.0' "https://moto-way.com/fuel-price/fuel_prices.json" -o "$DIR/prices.json"
