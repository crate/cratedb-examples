# Use CrateDB with ingestr

## About

[ingestr] is a command-line application that allows copying data
from any source into any destination database.

## What's inside

This folder includes runnable examples that use ingestr with CrateDB.
They are also used as integration tests to ensure software components
fit together well.

- `.env`: Environment variable definitions
- `kafka-compose.yml`: Service composition file for Kafka and CrateDB
- `kafka-demo.xsh`: The demonstration program

## Prerequisites

For executing the commands in this walkthrough, you need a working
installation of Docker and Python.

## Synopsis

```shell
ingestr ingest --yes \
  --source-uri "kafka://?bootstrap_servers=localhost:9092&group_id=test_group&value_type=json&select=value" \
  --source-table "demo" \
  --dest-uri "cratedb://crate:crate@localhost:5432/?sslmode=disable" \
  --dest-table "doc.kafka_demo"
```

## Usage

To start cycling without tearing down the backend stack each time,
use the `KEEPALIVE` environment variable.
```shell
export KEEPALIVE=true
sh test.sh
```


[ingestr]: https://bruin-data.github.io/ingestr/
