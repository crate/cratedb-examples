#!/bin/bash
#
# Run SQL payload on CrateDB, all with Docker.
# Here: Import a subset of the NYC Yellowcab data set from a gzipped CSV file on AWS S3.
#
# Requirements: Bash, Docker
#
# Synopsis:
#
#   curl https://raw.githubusercontent.com/crate/cratedb-examples/main/spikes/testbench-yellowcab/cratedb-import-nyc-yellowcab.sh | bash
#

# 0. Define variables.
CONTAINER=cratedb

# 0. Define incantations.
crash="docker run --interactive --rm --network=host crate/crate:nightly crash"
cratedb_start="docker run --detach --rm --publish=4200:4200 --publish=5432:5432 --health-cmd=\"curl http://localhost:4200\" --health-interval=1s --health-start-period=5s --name=${CONTAINER} crate/crate:nightly -Cdiscovery.type=single-node"
cratedb_stop="docker stop ${CONTAINER}"
cratedb_status="docker inspect -f {{.State.Health.Status}} ${CONTAINER}"
echo=$(which echo)

# 1. Start CrateDB and wait for availability.
$cratedb_status > /dev/null 2>&1
if [ $? -ne 0 ]; then
  echo "Starting CrateDB."
  sh -c "$cratedb_start"
else
  echo "CrateDB already running."
fi
echo "Waiting for availability of CrateDB."
until [[ $($cratedb_status) = "healthy" ]]; do
  $echo -n .
  sleep 0.1
done;
echo

# 2. Insert NYC Yellowcab data.
time $crash <<EOF
CREATE TABLE IF NOT EXISTS "nyc_taxi"
  ("congestion_surcharge" REAL, "dolocationid" INTEGER, "extra" REAL, "fare_amount" REAL, "improvement_surcharge" REAL, "mta_tax" REAL, "passenger_count" INTEGER, "payment_type" INTEGER, "pickup_datetime" TIMESTAMP WITH TIME ZONE, "pulocationid" INTEGER, "ratecodeid" INTEGER, "store_and_fwd_flag" TEXT, "tip_amount" REAL, "tolls_amount" REAL, "total_amount" REAL, "trip_distance" REAL, "vendorid" INTEGER)
  WITH ("column_policy" = 'dynamic', "number_of_replicas" = '0', "refresh_interval" = 10000);

COPY "nyc_taxi"
  FROM 'https://s3.amazonaws.com/crate.sampledata/nyc.yellowcab/yc.2019.07.gz'
  WITH (compression = 'gzip');

REFRESH TABLE "nyc_taxi";
EOF
echo

# 3. Inspect database.
echo "Total number of records in database:"
$crash <<EOF
SELECT COUNT(*) FROM nyc_taxi;
EOF
echo

# 4. Shut down database again.
$cratedb_stop
