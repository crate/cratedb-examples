#################################################
Apache Kafka, Apache Flink and CrateDB on Windows
#################################################

*****
About
*****

This document will outline how to run the tutorial on Windows 10, using PowerShell.
On Windows 10, please use those commands with PowerShell 3+ (pwsh) and `Docker Desktop on Windows`_.


*****
Setup
*****

Prepare a sandbox directory::

    New-Item sandbox/kafka-flink-cratedb -ItemType Directory -ErrorAction SilentlyContinue
    cd ./sandbox/kafka-flink-cratedb/


Infrastructure
==============

In order to start Kafka, Flink and CrateDB, invoke::

    Set-Variable -Name DOCKER_COMPOSE_URL -value "https://raw.githubusercontent.com/crate/cratedb-examples/amo/kafka-flink/spikes/kafka-flink/docker-compose.yml"
    Invoke-WebRequest -Uri "${DOCKER_COMPOSE_URL}" -OutFile "docker-compose.yml"
    docker-compose up

Resources
=========

Create a Kafka topic for publishing messages and a CrateDB table to receive
data from the taxi rides data feed::

    # Create Kafka topic
    docker run -it --network=scada-demo confluentinc/cp-kafka:6.1.1 `
        kafka-topics --bootstrap-server kafka-broker:9092 --create --replication-factor 1 --partitions 1 --topic rides

    # Create CrateDB table
    docker run -it --network=scada-demo westonsteimel/httpie `
        http "cratedb:4200/_sql?pretty" stmt='CREATE TABLE "taxi_rides" ("payload" OBJECT(DYNAMIC))'



Pipeline job
============

Acquire and invoke the Flink job::

    # Acquire Flink job
    Set-Variable -Name VERSION -value 0.2
    Set-Variable -Name JARFILE -value "cratedb-flink-jobs-${VERSION}.jar"
    Set-Variable -Name JARURL -value "https://github.com/crate/cratedb-flink-jobs/releases/download/${VERSION}/${JARFILE}"
    Set-Variable -Name HERE (Get-Location)
    Invoke-WebRequest -Uri "${JARURL}" -OutFile "${JARFILE}"

    # Invoke Flink job
    docker run -it --network=scada-demo --volume=${HERE}/${JARFILE}:/${JARFILE} flink:1.12 `
        flink run --jobmanager=flink-jobmanager:8081 /${JARFILE} `
            --kafka.servers kafka-broker:9092 `
            --kafka.topic rides `
            --crate.hosts cratedb:5432 `
            --crate.table taxi_rides


*****
Usage
*****

This section outlines how to acquire the NYC Taxi 2017 dataset in JSON format
and feed it to the Kafka topic ``rides``. After or while data is processed,
the number of records in the target database table will be inquired.

Obtain raw data::

    # Acquire NYC Taxi 2017 dataset in JSON format
    Invoke-WebRequest -Uri "https://gist.github.com/kovrus/328ba1b041dfbd89e55967291ba6e074/raw/7818724cb64a5d283db7f815737c9e198a22bee4/nyc-yellow-taxi-2017.tar.gz" -OutFile "nyc-yellow-taxi-2017.tar.gz"

    # Extract archive
    tar -xvf nyc-yellow-taxi-2017.tar.gz

    # Create a subset of the data (5000 records) for concluding the first steps
    gc ./nyc-yellow-taxi-2017.json | select -first 5000 > nyc-yellow-taxi-2017-subset.json

Subscribe to the topic to receive messages::

    docker run -it --network=scada-demo edenhill/kafkacat:1.6.0 kafkacat -b kafka-broker -C -t rides -o end

Publish data to the Kafka topic::

    gc nyc-yellow-taxi-2017-subset.json | docker run -i --network=scada-demo confluentinc/cp-kafka:6.1.1 `
        kafka-console-producer --bootstrap-server kafka-broker:9092 --topic rides

Check the number of records in database::

    docker run -it --network=scada-demo westonsteimel/httpie `
        http "cratedb:4200/_sql?pretty" stmt='SELECT COUNT(*) FROM "taxi_rides"'



.. _Docker Desktop on Windows: https://docs.docker.com/docker-for-windows/install/
