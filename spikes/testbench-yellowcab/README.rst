############################
CrateDB NYC Yellowcab import
############################


*****
About
*****

Import a subset of the NYC Yellowcab data set from a gzipped CSV file on AWS S3
into CrateDB.


*****
Usage
*****

::

    curl https://raw.githubusercontent.com/crate/cratedb-examples/main/spikes/testbench-yellowcab/cratedb-import-nyc-yellowcab.sh | bash


***
SQL
***

The SQL statements used::

    CREATE TABLE IF NOT EXISTS "nyc_taxi"
      ("congestion_surcharge" REAL, "dolocationid" INTEGER, "extra" REAL, "fare_amount" REAL, "improvement_surcharge" REAL, "mta_tax" REAL, "passenger_count" INTEGER, "payment_type" INTEGER, "pickup_datetime" TIMESTAMP WITH TIME ZONE, "pulocationid" INTEGER, "ratecodeid" INTEGER, "store_and_fwd_flag" TEXT, "tip_amount" REAL, "tolls_amount" REAL, "total_amount" REAL, "trip_distance" REAL, "vendorid" INTEGER)
      WITH ("column_policy" = 'dynamic', "number_of_replicas" = '0', "refresh_interval" = 10000);

    COPY "nyc_taxi"
      FROM 'https://s3.amazonaws.com/crate.sampledata/nyc.yellowcab/yc.2019.07.gz'
      WITH (compression = 'gzip');

    REFRESH TABLE "nyc_taxi";

    SELECT COUNT(*) FROM nyc_taxi;
