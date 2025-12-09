#!/bin/sh

# Using Pgpool-II with CrateDB.

# The miniature stack defines {Docker,Podman} services and tasks to spin
# up CrateDB and Pgpool-II, and to query a CrateDB system table through
# Pgpool's in-memory cache.

# https://github.com/pgpool/pgpool2
# https://github.com/crate/crate
# https://github.com/crate/cratedb-examples/tree/main/application/pgpool

# Start services: CrateDB and Pgpool-II.
docker compose up --detach

# Polyfill a missing function in CrateDB.
# BACKEND Error: "Unknown function: pg_catalog.has_function_privilege('crate', 'pgpool_regclass(cstring)', 'execute')"
docker compose run --rm provision-functions

# Query data from CrateDB.
# docker compose run --rm cratedb-query-data

# Query data via Pgpool.
docker compose run --rm pgpool-query-data
