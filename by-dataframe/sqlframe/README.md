# Verify the `sqlframe` library with CrateDB

Turning PySpark Into a Universal DataFrame API

## About

This folder includes software integration tests for verifying
that the [SQLFrame] Python library works well together with [CrateDB].

SQLFrame implements the [PySpark] DataFrame API in order to enable running
transformation pipelines directly on database engines - no Spark clusters
or dependencies required.

## What's Inside

- `example_basic.py`: A few examples that read CrateDB's `sys.summits` table.
  An example inquiring existing tables.

- `example_types.py`: An example that exercises all data types supported by
  CrateDB.

## Synopsis

```shell
pip install --upgrade sqlframe
```
```python
from psycopg2 import connect
from sqlframe import activate
from sqlframe.base.functions import col

# Define database connection parameters, suitable for CrateDB on localhost.
# For CrateDB Cloud, use `crate://<username>:<password>@<host>`.
conn = connect(
    dbname="crate",
    user="crate",
    password="",
    host="localhost",
    port="5432",
)
# Activate SQLFrame to run directly on CrateDB.
activate("postgres", conn=conn)

from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

# Invoke query.
df = spark.sql(
    spark.table("sys.summits")
    .where(col("region").ilike("ortler%"))
    .sort(col("height").desc())
    .limit(3)
)
print(df.sql())
df.show()
```

## Tests

Set up sandbox and install packages.
```bash
pip install uv
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt -r requirements-test.txt
```

Run integration tests.
```bash
pytest
```


[CrateDB]: https://cratedb.com/database
[PySpark]: https://spark.apache.org/docs/latest/api/python/
[SQLFrame]: https://pypi.org/project/sqlframe/
