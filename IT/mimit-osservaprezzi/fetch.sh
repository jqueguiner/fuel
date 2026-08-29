#!/usr/bin/env sh
# fetch MIMIT Osservaprezzi Carburanti (prezzo + anagrafica CSV) (IT) live prices -> this dir
DIR="$(CDPATH= cd "$(dirname "$0")" && pwd)"
curl -fsSL --max-time 60 "https://www.mimit.gov.it/images/exportCSV/anagrafica_impianti_attivi.csv" -o "$DIR/stations.csv"; curl -fsSL --max-time 60 "https://www.mimit.gov.it/images/exportCSV/prezzo_alle_8.csv" -o "$DIR/prices.csv"
