#!/usr/bin/env bash

# Test Open WebUI configuration via HTTP API.

# Runtime options.
set -euo pipefail

# Uncomment for local debugging, but **never** in automated runs.
# set -x

# Load configuration.
source .env

# Sign in to receive JWT token.
token=$( http --ignore-stdin POST ${OPEN_WEBUI_URL}/api/v1/auths/signin email= password= | jq -r .token )
if [[ -z "${token}" ]]; then
  echo "FATAL: Could not obtain JWT token from Open WebUI" >&2
  exit 1
fi

# Check for a canonical available model to validate that Open WebUI configuration worked.
http ${OPEN_WEBUI_URL}/api/models Authorization:"Bearer $token" refresh==true | \
    grep '"id":"gpt-4.1"' >/dev/null 2>&1 || {
        echo "ERROR: Model gpt-4.1 not available"
        exit 1
    }

echo "gpt-4.1 model found"
echo "Ready."
