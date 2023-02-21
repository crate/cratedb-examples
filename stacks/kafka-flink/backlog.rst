#######
Backlog
#######


*************
Functionality
*************

Data type mapping
=================
- [o] Currently, both ``pickup_datetime`` and ``dropoff_datetime`` are stored
  as ``TEXT`` within an ``OBJECT(DYNAMIC)``. Can this be improved?
- [o] ``Unknown column type for column 1`` warnings::

    kafka-flink-flink-taskmanager-1   | 2023-02-21 17:52:45,229 WARN  org.apache.flink.connector.jdbc.utils.JdbcUtils              [] -
    Unknown column type for column 1. Best effort approach to set its value: {fare_amount=6.0, total_amount=8.8, vendor_id=2, pickup_location_id=41, pickup_datetime=2017-06-07T06:25:23Z, passenger_count=1, tip_amount=1.0, tolls_amount=0.0, dropoff_location_id=41, dropoff_datetime=2017-06-07T06:30:57Z, trip_distance=0.9}.

Misc
====
- [o] Support ``flink stop`` command. Currently, it errors out with
  ``Config key [state.savepoints.dir] is not set. Property [targetDirectory] must be provided.``
- [o] No error message when data is **not** actually written to CrateDB?::


    flood stage disk watermark [95%] exceeded on [ZNRb6FDRRNmLlQChTb_zcA][Grand Mont][/data/data/nodes/0] free: 2.8gb[4%], all indices on this node will be marked read-only


***********
Maintenance
***********

- [o] Update all software components to their most recent versions
- [o] Add CI configuration
- [o] Add RTD configuration
