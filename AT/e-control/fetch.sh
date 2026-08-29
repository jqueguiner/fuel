#!/usr/bin/env sh
# fetch E-Control Spritpreisrechner (regulated, free, rate-limited) (AT) live prices -> this dir
DIR="$(CDPATH= cd "$(dirname "$0")" && pwd)"
curl -fsSL --max-time 30 "https://api.e-control.at/sprit/1.0/search/gas-stations/by-region?code=WIEN&type=DIE" -o "$DIR/prices.json"
