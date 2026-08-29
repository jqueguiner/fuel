#!/usr/bin/env sh
# fetch Tankerkönig (MTS-K official data, free API key) (DE) live prices -> this dir
DIR="$(CDPATH= cd "$(dirname "$0")" && pwd)"
# needs free API key: curl "https://creativecommons.tankerkoenig.de/json/list.php?lat=LAT&lng=LNG&rad=5&type=all&apikey=$TANKERKOENIG_KEY"
