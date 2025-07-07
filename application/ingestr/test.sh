#!/usr/bin/env bash

# ingestr integration test backplane.

set -eu

export INGESTR_DISABLE_TELEMETRY=true

# Install `uv`.
function setup() {
  if ! command -v uv >/dev/null 2>&1; then
    pip install uv
  fi
}

# Invoke Kafka tests.
function test_kafka() {
  bash kafka-cmd.sh
}

setup
test_kafka
