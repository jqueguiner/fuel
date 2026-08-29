#!/usr/bin/env sh
# fetch NSW FuelCheck (data.nsw.gov.au, free API key) (AU) live prices -> this dir
DIR="$(CDPATH= cd "$(dirname "$0")" && pwd)"
# needs free key: OAuth then GET FuelPriceCheck/v1/fuel/prices
