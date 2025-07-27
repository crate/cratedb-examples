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

# Sign in to receive JWT token.
token=$( http --ignore-stdin POST ${OPEN_WEBUI_URL}/api/v1/auths/signin email= password= | jq -r .token )
if [[ -z "${token}" ]]; then
  echo "FATAL: Could not obtain JWT token from Open WebUI" >&2
  exit 1
fi

# Inquire health.
http --ignore-stdin ${OPEN_WEBUI_URL}/health

# List available tools.
http --ignore-stdin ${OPEN_WEBUI_URL}/api/v1/tools/ Authorization:"Bearer $token"

# Configure system prompt.
http --ignore-stdin ${OPEN_WEBUI_URL}/api/v1/users/user/settings/update Authorization:"Bearer $token" \
    ui[system]="$( cratedb-mcp show-prompt )" \
    ui[params][function_calling]="native" \
    ui[params][temperature]=0 \
    ui[notificationEnabled]="true"

# Configure CrateDB MCPO server.
http --ignore-stdin ${OPEN_WEBUI_URL}/api/v1/configs/tool_servers Authorization:"Bearer $token" \
    "@tool-servers.json"

# Configure chat model.
http --ignore-stdin ${OPEN_WEBUI_URL}/api/v1/configs/models Authorization:"Bearer $token" \
    DEFAULT_MODELS="gpt-4.1" MODEL_ORDER_LIST="[]"

# Configure embedding model.
http --ignore-stdin ${OPEN_WEBUI_URL}/api/v1/retrieval/embedding/update Authorization:"Bearer $token" \
    embedding_engine="openai" embedding_model="text-embedding-3-small"
