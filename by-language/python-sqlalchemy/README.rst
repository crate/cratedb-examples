.. highlight: console

############################################################
Connect to CrateDB and CrateDB Cloud using Python/SQLAlchemy
############################################################


*****
About
*****

Example programs demonstrating CrateDB's SQLAlchemy adapter and dialect.


*****
Setup
*****

To start a CrateDB instance on your machine for evaluation purposes, invoke::

    docker run -it --rm --publish=4200:4200 --publish=5432:5432 crate:latest

Navigate to example program directory, and install prerequisites::

    # Acquire sources.
    git clone https://github.com/crate/cratedb-examples
    cd cratedb-examples
    python3 -m venv .venv
    source .venv/bin/activate

Then, invoke the integration test cases::

    ngr test by-language/python-sqlalchemy


********
Examples
********

The ``insert`` example programs are about efficient data loading::

    time python insert_efficient.py cratedb multirow
    time python insert_efficient.py cratedb batched

The ``sync`` and ``async`` example programs demonstrate SQLAlchemy's
low-level table/core API using both the HTTP-based transport driver
using ``urllib3``, as well as the canonical ``asyncpg`` and ``psycopg3``
drivers using the PostgreSQL wire protocol::

    time python sync_table.py urllib3 psycopg
    time python async_table.py asyncpg psycopg
    time python async_streaming.py asyncpg psycopg


.. TIP::

    For more information, please refer to the header sections of each of the
    provided example programs.


*****
Tests
*****

To test the accompanied example programs all at once, invoke the software tests::

    pytest


.. _CrateDB: https://github.com/crate/crate
