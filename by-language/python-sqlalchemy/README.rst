.. highlight: console

############################################################
Connect to CrateDB and CrateDB Cloud using Python/SQLAlchemy
############################################################


*****
About
*****

Example programs demonstrating CrateDB's SQLAlchemy adapter and dialect.

This section and examples are mostly about `DataFrame operations with SQLAlchemy`_,
specifically about how to insert data into `CrateDB`_ efficiently using `pandas`_ and
`Dask`_.



*****
Usage
*****

The CrateDB Python driver provides a convenience function ``insert_bulk``. It
can be used like this::

    # CrateDB Cloud
    # DBURI = "crate://admin:<PASSWORD>@example.aks1.westeurope.azure.cratedb.net:4200?ssl=true"

    # CrateDB Self-Managed
    # DBURI = "crate://crate@localhost:4200/"

    import sqlalchemy as sa
    from crate.client.sqlalchemy.support import insert_bulk

    # pandas
    engine = sa.create_engine(DBURI, **kwargs)
    df.to_sql(
        name="testdrive",
        con=engine,
        if_exists="append",
        index=False,
        chunksize=5_000,
        method=insert_bulk,
    )

    # Dask
    ddf.to_sql(
        "testdrive",
        uri=DBURI,
        index=False,
        if_exists="replace",
        chunksize=10_000,
        parallel=True,
        method=insert_bulk,
    )



*****
Setup
*****

To start a CrateDB instance on your machine for evaluation purposes, invoke::

    docker run -it --rm --publish=4200:4200 --publish=5432:5432 crate

Navigate to example program directory, and install prerequisites::

    # Acquire sources.
    git clone https://github.com/crate/cratedb-examples
    cd cratedb-examples/by-language/python-sqlalchemy
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade --requirement requirements.txt


********
Examples
********

The ``insert`` example programs are about efficient data loading::

    time python insert_efficient.py cratedb multirow
    time python insert_efficient.py cratedb batched

    time python insert_pandas.py
    time python insert_pandas.py --mode=basic --insertmanyvalues-page-size=5000
    time python insert_pandas.py --mode=bulk --bulk-size=20000 --num-records=75000

    time python insert_dask.py

The ``sync`` and ``async`` example programs demonstrate SQLAlchemy's
low-level table/core API using both the HTTP-based transport driver
using ``urllib3``, as well as the canonical ``asyncpg`` and ``psycopg3``
drivers using the PostgreSQL wire protocol::

    time python sync_table.py urllib3 psycopg
    time python async_table.py asyncpg psycopg
    time python async_streaming.py asyncpg psycopg

Connect to CrateDB Cloud
========================

By default, the example programs will connect to CrateDB on ``localhost``.
In order to connect to any other database instance, for example on CrateDB
Cloud::

    export DBURI="crate://crate@localhost:4200/"
    export DBURI="crate://admin:<PASSWORD>@example.aks1.westeurope.azure.cratedb.net:4200?ssl=true"
    time python insert_pandas.py --dburi="${DBURI}"

.. TIP::

    For more information, please refer to the header sections of each of the
    provided example programs.


*****
Tests
*****

To test the accompanied example programs all at once, invoke the software tests::

    pytest


.. _CrateDB: https://github.com/crate/crate
.. _Dask: https://www.dask.org/
.. _DataFrame operations with SQLAlchemy: https://cratedb.com/docs/python/en/latest/by-example/sqlalchemy/dataframe.html
.. _pandas: https://pandas.pydata.org/
