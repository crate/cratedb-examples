# Use CrateDB with ingestr

## About

[ingestr] is a command-line application that allows copying data
from any source into any destination database.

## What's inside

This folder includes runnable examples that use ingestr with CrateDB.
They are also used as integration tests to ensure software components
fit together well.

- `.env`: Environment variable definitions
- `elasticsearch-compose.yml`: Service composition file for Elasticsearch and CrateDB
- `elasticsearch-demo.sh`: The demonstration program

## Prerequisites

For executing the commands in this walkthrough, you need a working
installation of Docker and Python.

## Synopsis

Import data from CSV into Elasticsearch.
```shell
ingestr ingest --yes \
  --source-uri "csv://taxi_details.csv" \
  --source-table "data" \
  --dest-uri "elasticsearch://elasticsearch:9200?secure=false" \
  --dest-table "example"
```

Import data from Elasticsearch into CrateDB.
```shell
ingestr ingest --yes \
  --source-uri "elasticsearch://elasticsearch:9200?secure=false" \
  --source-table "example" \
  --dest-uri "cratedb://crate:crate@cratedb:5432" \
  --dest-table "doc.example"
```

## Usage

To start cycling without tearing down the backend stack each time,
use the `KEEPALIVE` environment variable.
```shell
export KEEPALIVE=true
sh test.sh
```


[ingestr]: https://bruin-data.github.io/ingestr/
