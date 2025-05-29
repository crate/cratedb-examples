# Verify the `records` library with CrateDB

Records: SQL for Humans™

## About

This folder includes software integration tests for verifying
that the [Records] Python library works well together with [CrateDB].

Records is a very simple, but powerful, library for making raw SQL
queries to most relational databases. It uses [SQLAlchemy].

Records is intended for report-style exports of database queries, and
has not yet been optimized for extremely large data dumps.

## What's Inside

- `example_basic.py`: A few examples that read CrateDB's `sys.summits` table.
  An example inquiring existing tables.

- `example_types.py`: An example that exercises all data types supported by
  CrateDB.

## Install

Set up sandbox and install packages.
```bash
pip install uv
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt -r requirements-test.txt
```

## Synopsis
```shell
pip install --upgrade records sqlalchemy-cratedb
```
```python
from pprint import pprint
import records

# Define database connection URL, suitable for CrateDB on localhost.
# For CrateDB Cloud, use `crate://<username>:<password>@<host>:4200?ssl=true`.
db = records.Database("crate://")

# Invoke query.
rows = db.query("SELECT * FROM sys.summits ORDER BY height DESC LIMIT 3")
data = rows.all()
pprint(data)
```

## Tests

Run integration tests.
```bash
pytest
```


[CrateDB]: https://cratedb.com/database
[Records]: https://pypi.org/project/records/
[SQLAlchemy]: https://www.sqlalchemy.org/
