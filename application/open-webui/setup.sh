#!/usr/bin/env bash

# Configure Open WebUI via HTTP API.

# Runtime options.
set -e
set -x

# Load variables.
source .env

# Sign in to receive JWT token.
token=$( http --ignore-stdin POST ${OPEN_WEBUI_URL}/api/v1/auths/signin email= password= | jq -r .token )
echo "JWT token: ${token}"

# Inquire health.
http --ignore-stdin ${OPEN_WEBUI_URL}/health

# Inquire available models.
#http ${OPEN_WEBUI_URL}/api/models Authorization:"Bearer $token"

# List available tools.
http --ignore-stdin ${OPEN_WEBUI_URL}/api/v1/tools/ Authorization:"Bearer $token"

# Configure system prompt.
http --ignore-stdin ${OPEN_WEBUI_URL}/api/v1/users/user/settings/update Authorization:"Bearer $token" ui[system]="$( cratedb-mcp show-prompt )" ui[notificationEnabled]="true"

# Configure CrateDB MCPO server.
http --ignore-stdin ${OPEN_WEBUI_URL}/api/v1/configs/tool_servers Authorization:"Bearer $token" "@tool-servers.json"

# Configure chat model.
http --ignore-stdin ${OPEN_WEBUI_URL}/api/v1/configs/models Authorization:"Bearer $token" DEFAULT_MODELS="gpt-4.1" MODEL_ORDER_LIST="[]"

# Configure embedding model.
http --ignore-stdin ${OPEN_WEBUI_URL}/api/v1/retrieval/embedding/update Authorization:"Bearer $token" embedding_engine="openai" embedding_model="text-embedding-3-small"

# Provision database
crash --hosts ${CRATEDB_URL} < init.sql
