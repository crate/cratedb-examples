#!/bin/sh

# Use Grafana with CrateDB.

# The miniature stack defines {Docker,Podman} services and tasks to spin
# up CrateDB and Grafana, provision data into CrateDB, and a corresponding
# data source and dashboard into Grafana.

# https://github.com/grafana/grafana
# https://github.com/crate/crate

# Start services.
docker compose up --detach --wait

# Run weather data example.
docker compose run --rm example-weather
