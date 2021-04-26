#########################################################
Notes for Apache Kafka, Apache Flink and CrateDB tutorial
#########################################################


*****
Kafka
*****

In order to check the Kafka subsystem, you can use the ``kafkacat`` program to
submit and receive messages to/from the broker, like::

    # Install program
    brew install kafkacat

    # Define a message
    export MESSAGE="The quick brown fox jumps over the lazy dog."

    # Publish message to topic
    echo $MESSAGE | kafkacat -b localhost:9094 -P -t testdrive

    # Consume messages from topic
    kafkacat -b localhost:9094 -C -t testdrive -o end

    # Show topics
    kafkacat -L -b localhost:9094

If you can't install ``kafkacat`` on your machine, you can also use Docker to
invoke it::

    # Publish message to topic
    echo $MESSAGE | docker run -i --network=scada-demo edenhill/kafkacat:1.6.0 kafkacat -b kafka-broker -P -t testdrive

    # Consume messages from topic
    docker run -it --network=scada-demo edenhill/kafkacat:1.6.0 kafkacat -b kafka-broker -C -t testdrive -o end


*****
Flink
*****

Flink job administration::

    docker run -it --network=scada-demo flink:1.12 \
        flink list --jobmanager=flink-jobmanager:8081

    docker run -it --network=scada-demo flink:1.12 \
        flink cancel 873828a960f9ed8a4e71b7ec7e980b0d --jobmanager=flink-jobmanager:8081


*******
CrateDB
*******

When running low on disk space, the indexes will be made read-only [1]::

    ClusterBlockException[blocked by: [FORBIDDEN/12/index read-only / allow delete (api)];]

In order to make them writable again, invoke::

    http "localhost:4200/_sql?pretty" stmt='ALTER TABLE "taxi_rides" SET ("blocks.read_only_allow_delete" = FALSE)'


[1] https://community.crate.io/t/node-in-read-only-mode-after-low-diskspace/166
