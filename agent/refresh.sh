#!/usr/bin/env bash
# Autonomous fuel-catalog growth. Mirrors gtfs agent/hourly_report.sh:
#   pull -> discover new open portals -> health-check -> rebuild catalog ->
#   coverage gaps -> email jl@ the delta -> commit+push jqueguiner/fuel if changed.
# Cron (staggered off gtfs): 17 */6 * * *
set -uo pipefail
REPO="${FUEL_REPO:-/home/ubuntu/fuel}"
LOG=/tmp/fuel_refresh.log
cd "$REPO" || exit 1
export FUEL_REPO="$REPO"
{
echo "=== $(date -u) fuel refresh ==="
git pull --quiet --ff-only 2>&1 | tail -1 || true

python3 agent/discover.py        || true   # hunt new open portals
python3 agent/build_catalog.py   || true   # tree -> catalog.csv + README
python3 agent/health.py          || true   # status of every source
python3 agent/coverage_gaps.py 20 > /tmp/fuel_gaps.txt 2>/dev/null || true

SUBJECT=$(python3 agent/report_delta.py)
python3 /data/addresses/agent/mailer.py "$SUBJECT" /tmp/fuel_delta.html jl@gladia.io || true

if ! git diff --quiet || [ -n "$(git status --porcelain)" ]; then
  git add -A
  git commit -q -m "fuel refresh: ${SUBJECT}" || true
  TOK=$(gh auth token 2>/dev/null)
  if [ -n "$TOK" ]; then
    git push --quiet "https://x-access-token:${TOK}@github.com/jqueguiner/fuel.git" HEAD:main || true
  else
    git push --quiet || true
  fi
fi
echo "done: $SUBJECT"
} >> "$LOG" 2>&1
