# Verify the `records` program with CrateDB

Records: SQL for Humans™

## About

This folder includes software integration tests for verifying
that the [Records] Python program works well together with [CrateDB].

Records is a very simple, but powerful, library for making raw SQL
queries to most relational databases. It uses [SQLAlchemy].

Records is intended for report-style exports of database queries, and
has not yet been optimized for extremely large data dumps.

## What's Inside

- `example.sh`: A few examples that read CrateDB's `sys.summits` table
  using the `records` program. A single example that inserts data into
  a column using CrateDB's `OBJECT` column.

## Install

Set up sandbox and install packages.
```bash
pip install uv
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

## Synopsis
Install packages.
```shell
pip install --upgrade records sqlalchemy-cratedb
```
Define database connection URL, suitable for CrateDB on localhost.
For CrateDB Cloud, use `crate://<username>:<password>@<host>`.
```shell
export DATABASE_URL="crate://"
```
Invoke query.
```shell
records "SELECT * FROM sys.summits WHERE region ILIKE :region" region="ortler%"
```

## Tests

Run integration tests.
```bash
sh test.sh
```


[CrateDB]: https://cratedb.com/database
[Records]: https://pypi.org/project/records/
[SQLAlchemy]: https://www.sqlalchemy.org/
