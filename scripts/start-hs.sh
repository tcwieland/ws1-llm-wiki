#!/usr/bin/env bash
# Startet Claude Code gegen den Dienst der Hochschule Coburg statt gegen die Anthropic-API.
# Claude Code bleibt dasselbe Werkzeug – nur das Modell dahinter wechselt.
set -euo pipefail
cd "$(dirname "$0")/.."
if [ -f .env ]; then set -a; . ./.env; set +a; fi
: "${HS_BASE_URL:?Bitte HS_BASE_URL in .env eintragen (ohne /v1)}"
: "${HS_MODEL:?Bitte HS_MODEL in .env eintragen}"
unset ANTHROPIC_API_KEY
export ANTHROPIC_BASE_URL="$HS_BASE_URL"
export ANTHROPIC_AUTH_TOKEN="${HS_API_KEY:-unbenutzt}"
export ANTHROPIC_MODEL="$HS_MODEL"
export ANTHROPIC_DEFAULT_OPUS_MODEL="$HS_MODEL"
export ANTHROPIC_DEFAULT_SONNET_MODEL="$HS_MODEL"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="$HS_MODEL"
export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1
echo "Claude Code mit HS-Dienst: $HS_MODEL @ $HS_BASE_URL"
exec claude "$@"
