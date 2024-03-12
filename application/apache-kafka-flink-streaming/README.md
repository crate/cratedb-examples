# Streaming data with Apache Kafka, Apache Flink and CrateDB.

## About

This example showcases what a data-streaming architecture leveraging Kafka and Flink could look
like.

We use.

- Kafka (confluent)
- Apache Flink
- CrateDB 
- Python >=3.7<=3.11
- 
[img of the thing]

## Overview

An HTTP call is scheduled to run every 60 seconds on `weather_producer`, the API returns a JSON
with the specified city's weather, the json is then sent through `Kafka`.

`flink_consumer` is a flink application consuming the same kafka topic;
upon receiving data, it sends the resulting datastream to the sink, which is `CrateDB`

Both `flink_consumer` and `weather_producer` are written using their respective Python Wrappers.

[kafka-python](https://kafka-python.readthedocs.io/en/master/)

[apache-flink](https://nightlies.apache.org/flink/flink-docs-master/docs/dev/python/overview/)

Everything is customizable via environment variables, the API schedule, the topic, credentials...
etc.

See `.env` more details.

## How to use

There is ready-to-use docker-compose, fill in the .env with the API
Key (Get it here https://www.weatherapi.com/).

### Run the docker compose (and build the images)

`docker compose up -d --build`

### Stop the docker compose

`docker compose down`

### Poetry

`poetry install`

### Pip

`pip install -r requirements.txt`

## Notes

### CrateDB initial settings.

CrateDB stores the shard indexes on the file system by mapping a file into memory (mmap)
You might need to set `max_map_count` to something higher than the usual default, like `262144`.

You can do it by running `sysctl -w vm.max_map_count=262144`,
for more information see: [this](https://cratedb.com/docs/guide/admin/bootstrap-checks.html#linux)

### Mock API call.

If you don't want to register in the weather api we use, you can use the
provided `mock_fetch_weather_data`, call this instead in the scheduler call.

This is what it'd look like.

```python
scheduler.enter(
    RUN_EVERY_SECONDS,
    1,
    schedule_every,
    (RUN_EVERY_SECONDS, mock_fetch_weather_data, scheduler)
)
```

*after changing this, re-build the docker compose.*

### Initial kafka topic.

In this example the `Kafka` topic is only initialized the first data is sent to it, because of this
the flink job could fail if it exceeds the default timeout (60) seconds, this might only happen
if the API takes too long to respond *the very first time this project*.

To solve this, you should [configure](https://kafka.apache.org/quickstart#quickstart_createtopic)
the
topics on boot time. This is recommended for production scenarios.

If you are just testing things around, you can solve this by re-running `docker compose up -d`, it
will only start `flink_job` and assuming everything went ok, the topic should already exist and
work as expected.

If it still fails, check if any other container/service is down,
it could be a symptom of a wrong api token or an unresponsive Kafka server, for example.

## Data and schema

See `example.json` for the schema, as you can see in `weather_producer` and `flink_consumer`, schema
manipulation is minimum,
thanks to CrateDB's dynamic objects we only need to map `location` and `current` keys.

For more information on dynamic objects
see: [this](https://cratedb.com/blog/handling-dynamic-objects-in-cratedb)

In `weather_producer` the `Kafka` producer directly serializes the json into a string.

```python
KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVER,
              value_serializer=lambda m: json.dumps(m).encode('utf-8'))
```

In `flink_consumer` we use a `JSON` serializer and only specify the two main keys,
`location` and `current`

```python
row_type_info = Types.ROW_NAMED(['location', 'current'], [Types.STRING(), Types.STRING()])
json_format = JsonRowDeserializationSchema.builder().type_info(row_type_info).build()
```

If your format is not json, or if you want to specify the whole schema, adapt it as needed.

[Here](https://nightlies.apache.org/flink/flink-docs-master/api/python/examples/datastream/connectors.html)
you can find example of other formats like `csv` or `avro`.

## Jars and versions.

Jars are downloaded at build time to /app/jars, versions are pinned in the .env

There is a `JARS_PATH` in `flink_consumer`, change it if you have the jars somewhere else.
