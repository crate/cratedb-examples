#!/usr/bin/env sh

set -eu

export COMPOSE_REMOVE_ORPHANS=true

echo "Starting Elasticsearch and CrateDB services"
docker compose --file elasticsearch-compose.yml up --detach --wait

echo "Creating Elasticsearch index"
docker compose --file elasticsearch-compose.yml run es-create-index

echo "Importing CSV data into Elasticsearch"
docker compose --file elasticsearch-compose.yml run es-import

echo "Migrating data from Elasticsearch to CrateDB"
docker compose --file elasticsearch-compose.yml run cratedb-import

echo "Querying imported data in CrateDB"
docker compose --file elasticsearch-compose.yml run cratedb-query

echo "Verify amount of imported data in CrateDB"
docker compose --file elasticsearch-compose.yml run cratedb-verify

echo "Shutting down services"
docker compose --file elasticsearch-compose.yml down

echo "Demo completed successfully!"
