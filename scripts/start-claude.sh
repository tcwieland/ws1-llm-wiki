#!/usr/bin/env bash
# Startet Claude Code mit dem Anthropic-API-Zugang aus .env.
set -euo pipefail
cd "$(dirname "$0")/.."
if [ -f .env ]; then set -a; . ./.env; set +a; fi
: "${ANTHROPIC_API_KEY:?Bitte ANTHROPIC_API_KEY in .env eintragen}"
export ANTHROPIC_API_KEY
exec claude "$@"
