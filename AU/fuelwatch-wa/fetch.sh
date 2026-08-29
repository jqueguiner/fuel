#!/usr/bin/env sh
DIR="$(CDPATH= cd "$(dirname "$0")" && pwd)"
curl -fsSL --max-time 40 "https://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Product=1" -o "$DIR/ulp.xml"
