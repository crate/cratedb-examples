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

# Invoke Elasticsearch tests.
function test_elasticsearch() {
  sh elasticsearch-demo.sh
}

setup
test_elasticsearch
