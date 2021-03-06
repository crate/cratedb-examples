#####################################################
Building IoT applications with open-source components
#####################################################


**********************************************
Part 1: Apache Kafka, Apache Flink and CrateDB
**********************************************


Introduction
============

Kafka, Flink, and CrateDB are all distributed systems that provide elastic
scaling, fault tolerance, and high-throughput, low-latency performance via
parallel processing. Particularly, the use of CrateDB makes the stack an
extremely good fit for handling industrial time-series workloads.

The front line of the stack is Apache Kafka, used to queue messages received
from the IoT sensors and devices, making that data highly available to systems
that need it.

Apache Flink is a stream processing framework that executes data pipelines,
i.e. stateful computations over the data streams.
Flink jobs consist of multiple components including source, sink, and the set
of transformation operators that are applied to a data stream.

CrateDB is a new kind of distributed SQL database built for IIoT applications.
It will store and query data that has been processed and enriched by Apache
Flink.


About
=====

This tutorial shows how to build a simple data ingestion pipeline with open
source software components.
It will outline how to acquire and publish data to Kafka, process it using
Flink and store the data stream into CrateDB.
It describes this system as a part of the CrateDB reference architecture and
can be used as a blueprint for building own applications.

The following versions of software components are used:

- Confluent Kafka 6.1.1
- Apache Flink 1.12
- CrateDB 4.5.0
- Apache Kafka Connector for Flink 1.12.2
- JDBC Connector for Flink 1.12.2
- CrateDB JDBC driver 2.6.0


Overview
========

The Flink pipeline job will subscribe to the Kafka topic ``rides`` in order to
consume the data feed and store its records into the CrateDB table
``taxi_rides``.

Following the `Kafka + Flink: A Practical, How-To Guide`_, there is an example job
for importing the NYC taxi dataset at https://github.com/crate/cratedb-flink-jobs.
It uses those connectors and drivers to conclude its job:

- `Apache Kafka Connector for Flink`_
- `JDBC Connector for Flink`_
- `CrateDB JDBC driver`_


Details
=======

Foundation infrastructure
-------------------------

The simplest possible way to setup and start all software components on a
developer workstation is to use Docker Compose and Docker. Thus, this tutorial
does not address topics like high-availability, fault-tolerance, scalability
and performance considerations.

Both Apache Flink and CrateDB offer graphical user interfaces. You can navigate
to them by using:

:Apache Flink Dashboard: http://localhost:8081/
:CrateDB Admin UI: http://localhost:4200/

Notes
-----

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

    1. Install `Docker on Windows`_ and `enable WSL integration`_.
    2. If your Docker Compose version (check with ``docker-compose --version``)
       is <1.27.0, please upgrade it by invoking::

           # Install Docker Compose 1.27.0
           sudo curl -L "https://github.com/docker/compose/releases/download/1.27.0/docker-compose-$(uname -s)-$(uname -m)" \
               -o /usr/local/bin/docker-compose
           sudo chmod +x /usr/local/bin/docker-compose

           # Restart your terminal

.. _Docker on Windows: https://desktop.docker.com/win/stable/amd64/Docker%20Desktop%20Installer.exe
.. _enable WSL integration: https://docs.docker.com/docker-for-windows/wsl/


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


Usage
=====

In order to run this recipe on your workstation, please follow the
corresponding guides:

- ``README.Unix.rst``
- ``README.Windows.rst``


----

-- Derived from: ``Building IoT applications with open-source tools.pdf``.


.. _Apache Kafka Connector for Flink: https://ci.apache.org/projects/flink/flink-docs-stable/dev/connectors/kafka.html
.. _CrateDB JDBC driver: https://github.com/crate/crate-jdbc
.. _JDBC Connector for Flink: https://ci.apache.org/projects/flink/flink-docs-stable/dev/connectors/jdbc.html
.. _Kafka + Flink\: A Practical, How-To Guide: https://www.ververica.com/blog/kafka-flink-a-practical-how-to
