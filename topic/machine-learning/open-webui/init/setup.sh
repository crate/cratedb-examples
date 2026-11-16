#!/usr/bin/env bash

# Configure Open WebUI via HTTP API.

# Runtime options.
set -euo pipefail

# Uncomment for local debugging, but **never** in automated runs.
# set -x

# Load configuration.
source .env

# -------
# CrateDB
# -------

# Provision database.
crash --hosts ${CRATEDB_URL} < init.sql

# ----------
# Open WebUI
# ----------

# Call the Open WebUI API, and stop with its answer when it refuses the request.
api() {
  local path=$1; shift
  local response
  response=$( http --ignore-stdin --check-status "${OPEN_WEBUI_URL}${path}" "$@" ) || {
    echo "FATAL: Open WebUI refused the request to ${path}: ${response}" >&2
    exit 1
  }
  echo "${response}"
}

# Sign in to receive JWT token.
token=$( api /api/v1/auths/signin email= password= | jq -r '.token // empty' )
if [[ -z "${token}" ]]; then
  echo "FATAL: Could not obtain JWT token from Open WebUI" >&2
  exit 1
fi

# Inquire health.
api /health

# List available tools.
api /api/v1/tools/ Authorization:"Bearer $token"

# Configure system prompt.
api /api/v1/users/user/settings/update Authorization:"Bearer $token" \
    ui[system]="$( cratedb-mcp show-prompt )" \
    ui[params][function_calling]="native" \
    ui[params][temperature]:=0.0 \
    ui[notificationEnabled]="true"

# Configure CrateDB MCP server.
api /api/v1/configs/tool_servers Authorization:"Bearer $token" \
    "@tool-servers.json"

# Configure chat model.
api /api/v1/configs/models Authorization:"Bearer $token" \
    DEFAULT_MODELS="gpt-4.1" DEFAULT_PINNED_MODELS="" MODEL_ORDER_LIST:='[]'

# Configure embedding model. The answer holds the OpenAI API key, so it is not shown.
api /api/v1/retrieval/embedding/update Authorization:"Bearer $token" \
    RAG_EMBEDDING_ENGINE="openai" RAG_EMBEDDING_MODEL="text-embedding-3-small" >/dev/null
