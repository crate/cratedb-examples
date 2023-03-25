#######################################
Apache Kafka, Apache Flink, and CrateDB
#######################################

*Building industrial IoT applications with open-source components.*


*****
About
*****

Introduction
============

`Apache Kafka`_, `Apache Flink`_, and `CrateDB`_, are each distributed systems
that provide elastic scaling, fault tolerance, and high-throughput, low-latency
performance via parallel processing. Particularly, the use of CrateDB makes the
stack an extremely good fit for handling industrial time-series workloads.

The front line of the stack is Apache Kafka, used to queue messages received
from IoT sensors and devices, making that data highly available to other
systems for further processing.

Apache Flink is a stream processing framework that executes data pipelines,
i.e. stateful computations over data streams. Flink jobs consist of multiple
components including source, sink, and the set of transformation/processing
operators that are applied to a data stream.

CrateDB is a distributed SQL database focusing on industrial data acquisition
applications. It will store data that has been processed and enriched by Apache
Flink, and will allow you to query it efficiently.

What's inside
=============

This tutorial shows how to build a simple data ingestion pipeline with open
source software components. It accompanies the article `Build a data ingestion
pipeline using Kafka, Flink, and CrateDB`_.

It will outline how to acquire and publish data to Kafka, process it using
Flink, and store the data stream into CrateDB, both using a `CrateDB`_ instance
running on your machine, or using `CrateDB Cloud`_.

The system is part of the CrateDB reference architecture and can be used as a
blueprint for building own applications.

The following versions of software components are used:

- Apache Flink 1.16
- Apache Kafka 3.2 (Confluent 7.3)
- CrateDB 5.2
- CrateDB JDBC driver 2.6.0

How it works
============

The Flink pipeline job will subscribe to the Kafka topic ``rides`` in order to
consume the data feed and store its records into the CrateDB table ``taxi_rides``.

Following the `Kafka + Flink: A Practical, How-To Guide`_, there is an example
job implementing this at `Apache Flink jobs for CrateDB`_. It uses those
connectors and drivers to conclude its job:

- `CrateDB JDBC driver`_
- `Flink Apache Kafka Connector`_
- `Flink JDBC Connector`_


*****
Usage
*****

Workstation
===========

In order to run this recipe on your workstation, please follow the
corresponding guidelines:

- ``README.Unix.rst``
- ``README.Windows.rst``

There is also a test program ``test.sh`` which exercises the commands as an
end-to-end test. It can be invoked like::

    bash test.sh

Mostly, you want to keep the service containers running, in order to invoke the
test program repeatedly without incurring too much overhead. Use the
``--keepalive`` option for that::

    bash test.sh --keepalive

In order to run specific subcommands/functions defined within the file, invoke,
for example::

    bash test.sh stop-services

If, by chance, the ``verify-data`` test step fails, resources are currently not
cleaned up. In order to do that, run::

    bash test.sh teardown

CrateDB Cloud
=============

1. In order to spin up a database cluster on `CrateDB Cloud`_, head over to the
   `CrateDB Cloud Console`_.

2. Edit the "Data sink configuration (CrateDB Cloud)" section within the ``.env``
   configuration file, and activate the relevant settings. Alternatively, export
   the corresponding environment variables within your terminal session::

       export=CRATEDB_HTTP_SCHEME=https
       export=CRATEDB_HOST=example.aks1.westeurope.azure.cratedb.net
       export=CRATEDB_USERNAME='admin'
       export=CRATEDB_PASSWORD='<PASSWORD>'

3. Invoke ``test.sh`` as outlined in the previous documentation section.


*******
Details
*******

Foundation infrastructure
=========================

The simplest possible way to set up and start all software components on a
developer workstation is to use Docker Compose and Docker. Thus, this tutorial
does not address topics like high-availability, fault-tolerance, scalability
and other performance considerations.

Both Apache Flink and CrateDB offer graphical user interfaces. You can navigate
to them by using:

:Apache Flink Dashboard: http://localhost:8081/
:CrateDB Admin UI: http://localhost:4200/

Notes
=====

Please read those admonitions carefully in order to optimally prepare your
system environment to fit the needs of the tutorial.

*Note*

    CrateDB uses a ``mmapfs`` directory by default to store its indices. The
    default operating system limits on mmap counts is likely to be too low,
    which may result in out of memory exceptions.

    On Linux, you can increase the limits by running the following command::

        sudo sysctl -w vm.max_map_count=262144

    To set this value permanently, update the ``vm.max_map_count`` setting in
    ``/etc/sysctl.conf``. To verify after rebooting, run
    ``sysctl vm.max_map_count``.

*Note*

    When running this tutorial on Windows/WSL2, some upfront configuration is
    needed.

    1. Install `Docker Desktop for Windows`_ and `enable WSL integration`_.
    2. Docker Compose version 2 is recommended (``docker compose version``),
       but version 1 should still work (``docker-compose --version``).
       From the end of June 2023, Compose V1 won’t be supported anymore, and
       will be removed from all Docker Desktop versions.
    3. If you need to run Docker Compose version 1, you may consider updating to
       the most recent and last available release 1.29.2. Please note that
       Docker Compose <1.27.0 will not work at all.
       ::

           # Install Docker Compose 1.29.2
           sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" \
               -o /usr/local/bin/docker-compose
           sudo chmod +x /usr/local/bin/docker-compose

           # Restart your terminal


The data
========

Trip records from NYC taxis.

This dataset includes a subset of trip records completed in NYC taxis during
2017. The JSON message payload has the following format::

    {
        "vendor_id": 2,
        "passenger_count": 1,
        "trip_distance": 2.84,
        "fare_amount": 15.5,
        "tip_amount": 6.0,
        "tolls_amount": 0.0,
        "total_amount": 22.3,
        "pickup_location_id": 142
    }

The meanings of those fields are:

:vendor_id: A code indicating the vendor
:passenger_count: The number of passengers in the vehicle
:trip_distance: The elapsed trip distance in miles
:fare_amount: The time-and-distance fare calculated by the meter
:tip_amount: Tip amount
:tolls_amount: The amount of all tolls paid in trip
:total_amount: Total amount charged to passengers, ex. cash tips
:pickup_location_id: Location (lat/lon) where the meter was engaged
:dropoff_location_id: Location (lat/lon) where the meter was disengaged
:pickup_datetime: Date & time meter was engaged
:dropoff_datetime: Date & time meter was disengaged


----

-- Derived from: ``Building IoT applications with open-source tools.pdf``.


.. _Apache Flink: https://flink.apache.org/
.. _Apache Flink jobs for CrateDB: https://github.com/crate/cratedb-flink-jobs
.. _Apache Kafka: https://kafka.apache.org/
.. _Build a data ingestion pipeline using Kafka, Flink, and CrateDB: https://dev.to/crate/build-a-data-ingestion-pipeline-using-kafka-flink-and-cratedb-1h5o
.. _CrateDB: https://crate.io/products/cratedb
.. _CrateDB Cloud: https://crate.io/products/cratedb-cloud
.. _CrateDB Cloud Console: https://console.cratedb.cloud/
.. _CrateDB JDBC driver: https://crate.io/docs/jdbc/
.. _Docker Desktop for Windows: https://docs.docker.com/desktop/install/windows-install/
.. _enable WSL integration: https://docs.docker.com/desktop/windows/wsl/
.. _Flink Apache Kafka Connector: https://nightlies.apache.org/flink/flink-docs-stable/docs/connectors/datastream/kafka/
.. _Flink JDBC Connector: https://nightlies.apache.org/flink/flink-docs-stable/docs/connectors/datastream/jdbc/
.. _Kafka + Flink\: A Practical, How-To Guide: https://www.ververica.com/blog/kafka-flink-a-practical-how-to
