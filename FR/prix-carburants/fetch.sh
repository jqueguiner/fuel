#!/usr/bin/env sh
# fetch Prix des carburants — flux instantané (data.economie.gouv.fr) (FR) live prices -> this dir
DIR="$(CDPATH= cd "$(dirname "$0")" && pwd)"
curl -fsSL --max-time 60 "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/prix-des-carburants-en-france-flux-instantane-v2/exports/json" -o "$DIR/prices.json"
