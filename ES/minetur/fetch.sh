#!/usr/bin/env sh
# fetch Ministerio (sedeaplicaciones.minetur.gob.es) — Estaciones Terrestres (ES) live prices -> this dir
DIR="$(CDPATH= cd "$(dirname "$0")" && pwd)"
curl -fsSL --max-time 90 "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/" -o "$DIR/prices.json"
