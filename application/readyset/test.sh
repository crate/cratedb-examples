#!/bin/sh

# Using Readyset with CrateDB.
# https://github.com/readysettech/readyset
# https://github.com/crate/crate

# The miniature stack defined as {Docker,Podman} services and tasks spins
# up CrateDB and Readyset, and queries a CrateDB system table through
# Readyset's in-memory cache.

# Start services: CrateDB and Readyset.
docker compose up --detach
exitcode=$?

# Query data from CrateDB.
# docker compose run --rm cratedb-query-data

# Query data via Readyset.
docker compose run --rm readyset-query-data

# Display logs.
docker compose logs readyset -n 15

# Propagate the proper exitcode.
exit $exitcode
