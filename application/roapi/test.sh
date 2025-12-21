#!/bin/sh

# Using ROAPI with CrateDB.
# https://github.com/roapi/roapi
# https://github.com/crate/crate

# The miniature stack defined as {Docker,Podman} services and tasks registers a
# few data sources with ROAPI, mounts them as CrateDB tables using its PostgreSQL
# JDBC foreign data wrapper, then queries them.

# Start services: CrateDB and ROAPI.
docker compose up --build --detach --wait

# Register data files with ROAPI.
docker compose run --rm roapi-register-data

# Probe if data sources exist in ROAPI.
# docker compose run --rm roapi-query-data

# Mount table using foreign data wrappers.
docker compose run --rm cratedb-register-data

# Query foreign table `doc.uk_cities` from CrateDB.
docker compose run --rm cratedb-query-data
