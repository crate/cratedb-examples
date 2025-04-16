#!/usr/bin/env sh

# Connect to CrateDB using SSL, with host name verification turned off.
uvx crash -v --hosts https://localhost:4200 \
  --user=crate --format=dynamic \
  --verify-ssl=false \
  --command "SELECT 42"
