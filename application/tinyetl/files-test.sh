#!/usr/bin/env sh

set -eu

export BUILDKIT_PROGRESS=plain
export COMPOSE_REMOVE=true
export COMPOSE_REMOVE_ORPHANS=true

echo "Starting services"
docker compose --file files-compose.yml up --detach --wait

echo "Reset data in CrateDB"
docker compose --file files-compose.yml run cratedb-reset

echo "Importing files into CrateDB"
docker compose --file files-compose.yml run cratedb-import

echo "Querying imported data in CrateDB"
docker compose --file files-compose.yml run cratedb-query

echo "Verify amount of imported data in CrateDB"
docker compose --file files-compose.yml run cratedb-verify

echo "Exporting data from CrateDB"
docker compose --file files-compose.yml run cratedb-export

echo "Shutting down services"
docker compose --file files-compose.yml down

echo "Demo completed successfully!"
