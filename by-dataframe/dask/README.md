# Connect to CrateDB and CrateDB Cloud using pandas


## About
Example programs demonstrating connectivity with [Dask] and [CrateDB].

This section and examples are mostly about [DataFrame operations with SQLAlchemy],
specifically about how to insert data into [CrateDB] efficiently.


## Usage

The CrateDB Python driver provides a convenience function `insert_bulk`,
which allows you to efficiently insert multiple rows of data into a CrateDB
database table in a single operation. It can be used like this:

```python
# CrateDB Cloud
# DBURI = "crate://admin:<PASSWORD>@<CLUSTERNAME>.aks1.westeurope.azure.cratedb.net:4200?ssl=true"

# CrateDB Self-Managed
# DBURI = "crate://crate@localhost:4200/"

import sqlalchemy as sa
from crate.client.sqlalchemy.support import insert_bulk

ddf.to_sql(
    "testdrive",
    uri=DBURI,
    index=False,
    if_exists="replace",
    chunksize=10_000,
    parallel=True,
    method=insert_bulk,
)
```


## Setup

To start a CrateDB instance on your machine, invoke:
```shell
docker run -it --rm \
  --publish=4200:4200 --publish=5432:5432 \
  --env=CRATE_HEAP_SIZE=4g \
  crate:latest -Cdiscovery.type=single-node
```

Acquire `cratedb-example` repository, and set up sandbox:
```shell
git clone https://github.com/crate/cratedb-examples
cd cratedb-examples
python3 -m venv .venv
source .venv/bin/activate
```

Then, invoke the integration test cases:
```shell
ngr test by-dataframe/dask
```


## Examples
The `insert` example programs are about efficient data loading:
```shell
time python insert_dask.py
time python insert_dask.py --mode=basic
time python insert_dask.py --mode=bulk --bulk-size=20000 --num-records=75000
```


## Connect to CrateDB Cloud

By default, the example programs will connect to CrateDB on `localhost`.
In order to connect to any other database instance, for example to [CrateDB
Cloud]:

```shell
export DBURI="crate://crate@localhost:4200/"
export DBURI="crate://admin:<PASSWORD>@example.aks1.westeurope.azure.cratedb.net:4200?ssl=true"
time python insert_dask.py --dburi="${DBURI}"
```

```{tip}
For more information, please refer to the header sections of each of the
provided example programs.
```


## Tests

To test the accompanied example programs all at once, invoke the software tests:
```shell
pytest
```


[CrateDB]: https://github.com/crate/crate
[CrateDB Cloud]: https://console.cratedb.cloud/
[Dask]: https://www.dask.org/
[DataFrame operations with SQLAlchemy]: https://cratedb.com/docs/python/en/latest/by-example/sqlalchemy/dataframe.html
