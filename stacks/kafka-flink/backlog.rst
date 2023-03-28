#######
Backlog
#######


*************
Functionality
*************

Data type mapping
=================
- [o] Currently, the DDL schema is ``CREATE TABLE "taxi_rides" ("payload" OBJECT(DYNAMIC))``.
  Shall there be an advanced version, where data is stored into individual columns?
- [o] Currently, both ``pickup_datetime`` and ``dropoff_datetime`` are stored
  as ``TEXT`` within an ``OBJECT(DYNAMIC)``. Can this be improved?
- [o] ``Unknown column type for column 1`` warnings::

    kafka-flink-flink-taskmanager-1   | 2023-02-21 17:52:45,229 WARN  org.apache.flink.connector.jdbc.utils.JdbcUtils              [] -
    Unknown column type for column 1. Best effort approach to set its value: {fare_amount=6.0, total_amount=8.8, vendor_id=2, pickup_location_id=41, pickup_datetime=2017-06-07T06:25:23Z, passenger_count=1, tip_amount=1.0, tolls_amount=0.0, dropoff_location_id=41, dropoff_datetime=2017-06-07T06:30:57Z, trip_distance=0.9}.

General
=======
- [o] Only *optionally* use ``flink run --detach`` option: When using ``--detach``, there is no
  output/feedback about any eventual failures happening when submitting the job.
- [o] How to inquire job metrics?
- [o] Evaluate performance options
- [o] Support ``flink stop`` command. Currently, it errors out with
  ``Config key [state.savepoints.dir] is not set. Property [targetDirectory] must be provided.``
- [o] No error message when data is **not** actually written to CrateDB?::

    flood stage disk watermark [95%] exceeded on [ZNRb6FDRRNmLlQChTb_zcA][Grand Mont][/data/data/nodes/0] free: 2.8gb[4%], all indices on this node will be marked read-only

- [o] Use a solid fake data generator for producing/feeding data on the fly
  See https://github.com/aiven/python-fake-data-producer-for-apache-kafka

- [o] Exercise an example with Flink's "JSON Format" adapter? See:

  - https://nightlies.apache.org/flink/flink-docs-master/docs/connectors/table/formats/json/
  - https://nightlies.apache.org/flink/flink-docs-master/docs/dev/table/functions/systemfunctions/#json-functions
- [o] Exercise an example with Flink's new "JSON TABLE SQL functions"? See:

  - https://aiven.io/blog/preview-JSON-SQL-functions-apache-flink-1.15.0
  - https://aiven.io/flink
- [o] Have a look at other tutorials

  - https://www.baeldung.com/kafka-flink-data-pipeline
  - https://github.com/eugenp/tutorials/tree/master/apache-kafka


**************
Infrastructure
**************

- [x] Modernize environment setup
- [/] Windows (PS): Use environment variables from python-dotenv formatted .env file
  https://gist.github.com/grenzi/82e6cb8215cc47879fdf3a8a4768ec09
- [/] Windows (PS): Verify if https://github.com/rajivharris/Set-PsEnv actually works
- [x] Add CI configuration
- [x] Update all software components to their most recent versions
- [o] Add RTD configuration
