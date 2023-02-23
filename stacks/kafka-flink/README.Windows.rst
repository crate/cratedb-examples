#################################################
Apache Kafka, Apache Flink and CrateDB on Windows
#################################################


*****
About
*****

This document will outline how to run the tutorial on Windows 10, using
PowerShell. On Windows 10, please use those commands with PowerShell 3+
(pwsh) and `Docker Desktop for Windows`_.


*****
Setup
*****

Prerequisites
=============

In order to exercise the command walkthrough successfully, please make sure
those programs are installed/available on your machine / in your environment.

- docker
- tar

Infrastructure
==============

In order to start Kafka, Flink and CrateDB, invoke::

    Set-Variable -Name DOCKER_COMPOSE_URL -value "https://raw.githubusercontent.com/crate/cratedb-examples/0.1.0/stacks/kafka-flink/docker-compose.yml"
    Invoke-WebRequest -Uri "${DOCKER_COMPOSE_URL}" -OutFile "docker-compose.yml"
    docker compose up

In order to shut down the services, and clear their state completely, use::

    docker compose down --remove-orphans

Pre-flight checks
-----------------

In order to check if the Kafka subsystem works, have a look at the "Kafka"
section within the ``notes.rst`` document. It is really worth the detour,
because it will introduce you to excellent debug tooling for Kafka.


Resources
=========

Create a Kafka topic for publishing messages and a CrateDB table to receive
data from the taxi rides data feed::

    docker compose run --rm create-topic
    docker compose run --rm create-table

.. note::

    In order to drop the database table, try ``docker compose run --rm drop-table``.

Pipeline job
============

Acquire and invoke the Flink job::

    Set-Variable -Name HERE (Get-Location)

    # Acquire Flink job JAR file.
    docker compose run --rm --volume=${HERE}:/src download-job

    # Submit and invoke Flink job.
    docker compose run --rm --volume=${HERE}:/src submit-job

    # List running jobs.
    docker compose run --rm list-jobs


*****
Usage
*****

This section outlines how to acquire the NYC Taxi 2017 dataset in JSON format
and feed it to the Kafka topic ``rides``. After or while data is processed,
the number of records in the target database table will be inquired.

Obtain raw data::

    # Acquire NYC Taxi 2017 dataset in JSON format (~90 MB)
    Invoke-WebRequest -Uri "https://gist.github.com/kovrus/328ba1b041dfbd89e55967291ba6e074/raw/7818724cb64a5d283db7f815737c9e198a22bee4/nyc-yellow-taxi-2017.tar.gz" -OutFile "nyc-yellow-taxi-2017.tar.gz"

    # Extract archive
    tar -xvf nyc-yellow-taxi-2017.tar.gz

    # Create a subset of the data (5000 records) for concluding the first steps
    gc ./nyc-yellow-taxi-2017.json | select -first 5000 > nyc-yellow-taxi-2017-subset.ndjson

Subscribe to the Kafka topic to receive messages::

    docker compose run --rm subscribe-topic

Publish data to the Kafka topic::

    gc nyc-yellow-taxi-2017-subset.ndjson | docker compose run --rm --no-TTY publish-data

Check the number of records in database, and display a few samples::

    docker compose run --rm httpie \
        http "cratedb:4200/_sql?pretty" stmt='SELECT COUNT(*) FROM "taxi_rides";'

    docker compose run --rm httpie \
        http "cratedb:4200/_sql?pretty" stmt='SELECT * FROM "taxi_rides" LIMIT 5;'


.. _Docker Desktop for Windows: https://docs.docker.com/desktop/install/windows-install/
