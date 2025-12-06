#!/bin/sh
set -e

# ----
# Avro
# ----
tinyetl \
  "https://github.com/alrpal/TinyETL/raw/refs/heads/master/examples/10_csv_to_avro/output.avro" \
  "postgresql://crate:crate@localhost/testdrive#avro"

# -----------
# Import: CSV
# -----------
tinyetl \
  "https://cdn2.crate.io/downloads/datasets/cratedb-datasets/timeseries/nab-machine-failure.csv" \
  "postgresql://crate:crate@localhost/testdrive#nab-machine-failure"

tinyetl \
  "https://cdn2.crate.io/downloads/datasets/cratedb-datasets/machine-learning/fulltext/twitter_support_microsoft.csv" \
  "postgresql://crate:crate@localhost/testdrive#tweets"

# --------------
# Import: DuckDB
# --------------
wget "https://github.com/alrpal/TinyETL/raw/refs/heads/master/examples/15_csv_to_duckdb/products.duckdb"
tinyetl \
  "products.duckdb#products" \
  "postgresql://crate:crate@localhost/testdrive#duckdb"

# ---------------
# Import: Parquet
# ---------------
tinyetl \
  "https://cdn2.crate.io/downloads/datasets/cratedb-datasets/misc/cities.parquet" \
  "postgresql://crate:crate@localhost/testdrive#cities"

tinyetl \
  "https://cdn.crate.io/downloads/datasets/cratedb-datasets/timeseries/yc.2019.07-tiny.parquet" \
  "postgresql://crate:crate@localhost/testdrive#yellowcab"

# --------------
# Export: DuckDB
# --------------
tinyetl --truncate "postgresql://crate:@localhost/testdrive#avro" avro.duckdb

# -------
# Cleanup
# -------
rm -f avro.duckdb products.duckdb
