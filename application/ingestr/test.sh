#!/usr/bin/env bash

# ingestr integration test backplane.

set -eu

export INGESTR_DISABLE_TELEMETRY=true

# Install `uv`.
function setup() {
  if ! command -v uv >/dev/null 2>&1; then
    pip install uv
  fi
  if ! command -v xonsh >/dev/null 2>&1; then
    uv tool install xonsh
  fi
}

# Invoke Kafka tests.
function test_kafka() {
  # Use specific version of Xonsh until #6354 is resolved.
  # https://github.com/xonsh/xonsh/issues/6354
  uvx 'xonsh==0.23.1' kafka-demo.xsh
}

# Invoke Elasticsearch tests.
function test_elasticsearch() {
  sh elasticsearch-demo.sh
}

setup
test_kafka
test_elasticsearch
