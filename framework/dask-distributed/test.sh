#!/bin/sh
set -e

# Use Dask with CrateDB.

# The miniature stack defines {Docker,Podman} services and tasks to spin
# up CrateDB and a Dask cluster, and run an I/O job on it.

# https://github.com/crate/crate
# https://github.com/dask/distributed

# Start services.
export BUILDKIT_PROGRESS=plain
docker compose up --detach --wait

# Pre-flight request to fix Dask accounting.
# https://github.com/dask/distributed/issues/9253
docker compose run --rm --quiet-build --env="mode=ping" verify

# Run I/O example.
docker compose run --rm --quiet-build export-to-deltalake

# Verify task was invoked properly.
docker compose run --rm --quiet-build verify
