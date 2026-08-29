#!/usr/bin/env sh
DIR="$(CDPATH= cd "$(dirname "$0")" && pwd)"
curl -fsSL --max-time 30 "https://goriva.si/api/v1/search/?format=json" -o "$DIR/prices.json"
