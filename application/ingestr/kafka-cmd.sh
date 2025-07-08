#!/usr/bin/env bash

# =====
# About
# =====

# End-to-end test feeding data through a pipeline implemented with Apache Kafka,
# ingestr, and CrateDB. The data source is a file in NDJSON format, the
# data sink is a database table in CrateDB.


# ============
# Main program
# ============

set -eu

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/.env"
source "${SCRIPT_DIR}/util.sh"

COMPOSE_FILE="${SCRIPT_DIR}/kafka-compose.yml"

# ----------------------------
# Infrastructure and resources
# ----------------------------

function start-services() {
  title "Starting services"
  docker compose --file ${COMPOSE_FILE} up --detach
}

function stop-services() {
  title "Stopping services"
  docker compose --file ${COMPOSE_FILE} down --remove-orphans
}

function setup() {
  delete-topic
  # drop-table    # Please do not drop tables with ingestr
  # create-table  # ingestr creates the table itself
  create-topic
}

function teardown() {
  delete-topic
  # drop-table    # Please do not drop tables with ingestr
}


# -----------
# Data source
# -----------

function create-topic() {
  title "Creating Kafka topic"
  docker compose --file ${COMPOSE_FILE} run --rm create-topic
  echo "Done."
}

function delete-topic() {
  title "Deleting Kafka topic"
  docker compose --file ${COMPOSE_FILE} run --rm --no-TTY delete-topic
  echo "Done."
}


# --------
# Pipeline
# --------

function invoke-job() {

  # Invoke ingestr job.
  title "Invoking ingestr job"

  uvx --python="3.12" --prerelease="allow" --with-requirements="requirements.txt" ingestr ingest --yes \
    --source-uri "kafka://?bootstrap_servers=localhost:${PORT_KAFKA_BROKER_EXTERNAL}&group_id=test_group" \
    --source-table "demo" \
    --dest-uri "cratedb://crate:crate@localhost:5432/?sslmode=disable" \
    --dest-table "doc.kafka_demo"

  echo "Done."
}

function feed-data() {

  if [[ ! -f nyc-yellow-taxi-2017-subset.ndjson ]]; then

    title "Acquiring NDJSON data"

    # Acquire NYC Taxi 2017 dataset in JSON format (~90 MB).
    wget --no-clobber --continue https://gist.githubusercontent.com/kovrus/328ba1b041dfbd89e55967291ba6e074/raw/7818724cb64a5d283db7f815737c9e198a22bee4/nyc-yellow-taxi-2017.tar.gz

    # Extract archive.
    tar -xvf nyc-yellow-taxi-2017.tar.gz

    # Create a subset of the data (5000 records) for concluding the first steps.
    cat nyc-yellow-taxi-2017.json | head -n 5000 > nyc-yellow-taxi-2017-subset.ndjson

  fi

  # Publish data to the Kafka topic.
  title "Publishing NDJSON data to Kafka topic"
  cat nyc-yellow-taxi-2017-subset.ndjson | docker compose --file ${COMPOSE_FILE} run --rm --no-TTY publish-data
  echo "Done."

  # Wait a bit for the data to transfer and converge successfully.
  sleep 3
}


# ---------
# Data sink
# ---------

function create-table() {
  title "Creating CrateDB table"
  docker compose --file ${COMPOSE_FILE} run --rm create-table
  echo "Done."
}

function display-data() {

  title "Displaying data in CrateDB"

  docker compose --file ${COMPOSE_FILE} run --rm httpie \
    http "${CRATEDB_HTTP_URL}/_sql?pretty" stmt='REFRESH TABLE "kafka_demo";' --ignore-stdin > /dev/null

  docker compose --file ${COMPOSE_FILE} run --rm httpie \
    http "${CRATEDB_HTTP_URL}/_sql?pretty" stmt='SELECT * FROM "kafka_demo" LIMIT 5;' --ignore-stdin

  docker compose --file ${COMPOSE_FILE} run --rm httpie \
    http "${CRATEDB_HTTP_URL}/_sql?pretty" stmt='SELECT COUNT(*) FROM "kafka_demo";' --ignore-stdin

}

function verify-data() {
  title "Verifying data in CrateDB"
  size_reference=5000
  size_actual=$(
    docker compose --file ${COMPOSE_FILE} run --rm httpie \
      http "${CRATEDB_HTTP_URL}/_sql?pretty" stmt='SELECT COUNT(*) FROM "kafka_demo";' --ignore-stdin \
    | jq .rows[0][0]
  )
  if [[ "${size_actual}" = "${size_reference}" ]]; then
    echo -e "${BGREEN}SUCCESS: Database table contains expected number of ${size_reference} records.${NC}"
  else
    echo -e "${BRED}ERROR:   Expected database table to contain ${size_reference} records, but it contains ${size_actual} records.${NC}"
    exit 2
  fi
}

function drop-table() {
  title "Dropping CrateDB table"
  docker compose --file ${COMPOSE_FILE} run --rm drop-table
  echo "Done."
}


# ------
# Recipe
# ------

function main() {

  # Start services and setup resources.
  start-services
  setup

  # Acquire data, feed data to Kafka topic, invoke import job,
  # and verify data has been stored into CrateDB.
  feed-data
  invoke-job
  display-data
  verify-data

  # Clean up resources.
  # teardown  # Do not tear down, for inspection purposes.

  # Tear down only when `--keepalive` option has not been given.
  test -z "${KEEPALIVE-}" && stop-services
}

function start_subcommand() {
  if test -n "${SUBCOMMAND-}"; then
    ${SUBCOMMAND-}
    exit
  fi
}

function start() {
  #read_options
  init_colors
  start_subcommand
  main
}

start
