#!/usr/bin/env sh
DIR="$(CDPATH= cd "$(dirname "$0")" && pwd)"
curl -fsSL --max-time 60 "https://publicacionexterna.azurewebsites.net/publicaciones/places" -o "$DIR/places.xml"; curl -fsSL --max-time 60 "https://publicacionexterna.azurewebsites.net/publicaciones/prices" -o "$DIR/prices.xml"
