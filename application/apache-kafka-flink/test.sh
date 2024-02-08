#!/bin/bash

# =====
# About
# =====

# End-to-end test feeding data through a pipeline implemented with Apache Kafka,
# Apache Flink, and CrateDB. The data source is a file in NDJSON format, the
# data sink is a database table in CrateDB.


# ============
# Main program
# ============

source .env
set -e


# ----------------------------
# Infrastructure and resources
# ----------------------------

function start-services() {
  title "Starting services"
  docker compose up --detach
}

function stop-services() {
  title "Stopping services"
  docker compose down --remove-orphans
}

function setup() {
  title "Creating CrateDB table"
  docker compose run --rm create-table
  title "Creating Kafka topic"
  docker compose run --rm create-topic
}

function teardown() {
  title "Cancelling Flink jobs"
  flink-cancel-all-jobs
  title "Deleting Kafka topic"
  docker compose run --rm --no-TTY delete-topic
  title "Dropping CrateDB table"
  docker compose run --rm drop-table
}


# --------
# Pipeline
# --------

function invoke-job() {

  # Delete downloaded JAR file upfront.
  # TODO: This is a little bit hard-coded. Improve!
  #rm cratedb-flink-jobs-*.jar || true

  # Acquire Flink job JAR file.
  if ! test -f "${FLINK_JOB_JAR_FILE}"; then
    title "Acquiring Flink job JAR file"
    docker compose run --rm --volume=$(pwd):/src download-job
  fi

  # Submit and invoke Flink job.
  title "Submitting job to Flink"
  docker compose run --rm --volume=$(pwd):/src submit-job

  # List running jobs.
  title "Listing running Flink jobs"
  docker compose run --rm list-jobs
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
  cat nyc-yellow-taxi-2017-subset.ndjson | docker compose run --rm --no-TTY publish-data
  echo

  # Wait a bit for the data to transfer and converge successfully.
  sleep 3
}


# ---------
# Data sink
# ---------

function display-data() {

  title "Displaying data in CrateDB"

  docker compose run --rm httpie \
    http "${CRATEDB_HTTP_URL}/_sql?pretty" stmt='REFRESH TABLE "taxi_rides";' --ignore-stdin > /dev/null

  docker compose run --rm httpie \
    http "${CRATEDB_HTTP_URL}/_sql?pretty" stmt='SELECT * FROM "taxi_rides" LIMIT 5;' --ignore-stdin

  docker compose run --rm httpie \
    http "${CRATEDB_HTTP_URL}/_sql?pretty" stmt='SELECT COUNT(*) FROM "taxi_rides";' --ignore-stdin

}

function verify-data() {
  title "Verifying data in CrateDB"
  size_reference=5000
  size_actual=$(
    docker compose run --rm httpie \
      http "${CRATEDB_HTTP_URL}/_sql?pretty" stmt='SELECT COUNT(*) FROM "taxi_rides";' --ignore-stdin \
    | jq .rows[0][0]
  )
  if [[ ${size_actual} = ${size_reference} ]]; then
    echo -e "${BGREEN}SUCCESS: Database table contains expected number of ${size_reference} records.${NC}"
  else
    echo -e "${BRED}ERROR:   Expected database table to contain ${size_reference} records, but it contains ${size_actual} records.${NC}"
    exit 2
  fi
}


# ------
# Recipe
# ------

function main() {

  # Start services and setup resources.
  start-services
  setup

  # Acquire and submit Flink job, feed data to Kafka topic,
  # and verify data has been stored into CrateDB.
  invoke-job
  feed-data
  display-data
  verify-data

  # Clean up resources.
  teardown

  # Tear down only when `--keepalive` option has not been given.
  test -z "${KEEPALIVE}" && stop-services
}

function start_subcommand() {
  if test -n "${SUBCOMMAND}"; then
    ${SUBCOMMAND}
    exit
  fi
}

function start() {
  read_options
  init_colors
  start_subcommand
  main
}


# =================
# Utility functions
# =================

# https://dustymabe.com/2013/05/17/easy-getopt-for-a-bash-script/
options=$(getopt --options k --longoptions keepalive -- "$@")
function read_options() {

  # Call getopt to validate the provided input.
  [ $? -eq 0 ] || {
      echo "Incorrect options provided"
      exit 1
  }
  eval set -- "$options"
  while true; do
      case "$1" in
      -k)
          KEEPALIVE=true
          shift
          continue
          ;;
      --keepalive)
          KEEPALIVE=true
          shift
          continue
          ;;
      --)
          shift
          break
          ;;
      esac
      shift
  done
  SUBCOMMAND=$1

}

function flink-get-job-ids() {
  jobids=$(
    curl --silent http://localhost:${PORT_FLINK_JOBMANAGER}/jobs/overview \
    | jq -r '.jobs[] | select(.state == "RUNNING").jid'
  )
  echo $jobids
}

function flink-cancel-job() {
  jobid=$1
  echo "Cancelling job $jobid"
  docker run --rm --network=scada-demo flink:${FLINK_VERSION} \
    flink cancel ${jobid} --jobmanager=flink-jobmanager:${PORT_FLINK_JOBMANAGER}
}

function flink-cancel-all-jobs() {
  for jobid in $(flink-get-job-ids); do
    flink-cancel-job $jobid
  done
}

function title() {
  text=$1
  len=${#text}
  guard=$(printf "%${len}s" | sed 's/ /=/g')
  echo
  echo ${guard}
  echo -e "${BYELLOW}${text}${NC}"
  echo ${guard}
}

function init_colors() {
  # Reset
  NC='\033[0m'

  # Regular
  RED='\033[0;31m'
  GREEN='\033[0;32m'
  YELLOW='\033[0;33m'
  BLUE='\033[0;34m'
  PURPLE='\033[0;35m'
  CYAN='\033[0;36m'
  WHITE='\033[0;37m'

  # Bold
  BBLACK='\033[1;30m'
  BRED='\033[1;31m'
  BGREEN='\033[1;32m'
  BYELLOW='\033[1;33m'
  BBLUE='\033[1;34m'
  BPURPLE='\033[1;35m'
  BCYAN='\033[1;36m'
  BWHITE='\033[1;37m'
}


start
