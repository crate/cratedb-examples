#!/usr/bin/env sh

export COMPOSE_REMOVE_ORPHANS=true

docker compose --file elasticsearch-compose.yml up --detach --wait
docker compose --file elasticsearch-compose.yml run es-create-index
docker compose --file elasticsearch-compose.yml run es-import
docker compose --file elasticsearch-compose.yml run cratedb-import
docker compose --file elasticsearch-compose.yml run cratedb-query
docker compose --file elasticsearch-compose.yml down
