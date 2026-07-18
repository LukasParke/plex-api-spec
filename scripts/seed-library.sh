#!/usr/bin/env bash
# Seed the throwaway test PMS with one library section so contract-test
# workflows that assert on sections have meaningful data (e.g.
# browse-library requires MediaContainer.size > 0).
#
# Required env: PLEX_TOKEN (from the plex-harness action output).
# Optional env: PMS_URL (default http://localhost:32400),
#               SECTION_NAME, SECTION_LOCATION.
set -euo pipefail

BASE="${PMS_URL:-http://localhost:32400}"
TOKEN="${PLEX_TOKEN:?PLEX_TOKEN is required}"
SECTION_NAME="${SECTION_NAME:-CI Movies}"
SECTION_LOCATION="${SECTION_LOCATION:-/data/media/movies}"

# ./test-data/media is mounted read-only at /data/media in the container;
# create the location on the host so the path exists for PMS.
mkdir -p "$(cd "$(dirname "$0")/.." && pwd)/test-data/media/movies"

try_create() { # $1=scanner $2=agent
  # -G moves --data-urlencode pairs to the query string, which is what PMS
  # parses for section creation.
  curl -sf -G -X POST "$BASE/library/sections" \
    -H "X-Plex-Token: $TOKEN" \
    --data-urlencode "name=$SECTION_NAME" \
    --data-urlencode "type=movie" \
    --data-urlencode "location=$SECTION_LOCATION" \
    --data-urlencode "language=en" \
    --data-urlencode "scanner=$1" \
    --data-urlencode "agent=$2" \
    -o /dev/null
}

# Modern agent first, legacy fallback; agent availability varies by PMS version.
for combo in "Plex Movie|tv.plex.agents.movie" "Plex Movie Scanner|com.plexapp.agents.imdb"; do
  IFS='|' read -r scanner agent <<<"$combo"
  if try_create "$scanner" "$agent"; then
    echo "Created section '$SECTION_NAME' (scanner='$scanner', agent='$agent')"
    exit 0
  fi
  echo "Section creation failed with scanner='$scanner' agent='$agent'; trying next" >&2
done

echo "::error::Could not create library section with any known scanner/agent combo"
exit 1
