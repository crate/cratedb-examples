#!/usr/bin/env sh

# Using `records` with CrateDB: Basic usage.
#
#   pip install --upgrade records sqlalchemy-cratedb
#
# A few basic operations using the `records` program with CrateDB.
#
# - https://pypi.org/project/records/

# Define database connection URL, suitable for CrateDB on localhost.
# For CrateDB Cloud, use `crate://<username>:<password>@<host>`.
export DATABASE_URL="crate://"

# Basic query, tabular output.
records "SELECT * FROM sys.summits ORDER BY height DESC LIMIT 3"

# Query with parameters.
records "SELECT * FROM sys.summits WHERE region ILIKE :region" region="ortler%"

# Export data.
# Supported formats: csv tsv json yaml html xls xlsx dbf latex ods
records "SELECT * FROM sys.summits ORDER BY height DESC LIMIT 3" csv
records "SELECT * FROM sys.summits ORDER BY height DESC LIMIT 3" json
records "SELECT * FROM sys.summits LIMIT 42" html > "${TMPDIR}/sys_summits.html"
records "SELECT * FROM sys.summits LIMIT 42" ods > "${TMPDIR}/sys_summits.ods"
records "SELECT * FROM sys.summits LIMIT 42" xlsx > "${TMPDIR}/sys_summits.xlsx"

# Insert data.
records "DROP TABLE IF EXISTS testdrive.example"
records "CREATE TABLE testdrive.example (data OBJECT(DYNAMIC))"
records "INSERT INTO testdrive.example (data) VALUES (:data)" data='{"temperature": 42.42, "humidity": 84.84}'
records "REFRESH TABLE testdrive.example"
records "SELECT * FROM testdrive.example"
