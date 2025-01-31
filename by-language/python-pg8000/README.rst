.. highlight: console

#################################################
Connect to CrateDB and CrateDB Cloud using pg8000
#################################################


*****
About
*****

Example programs demonstrating CrateDB with pg8000,
for the PostgreSQL protocol.


*****
Setup
*****

To start a CrateDB instance on your machine for evaluation purposes, invoke::

    docker run --publish 4200:4200 --publish 5432:5432 --env CRATE_HEAP_SIZE=1g crate:latest -Cdiscovery.type=single-node

Navigate to the example program directory, and install prerequisites::

    # Acquire sources.
    git clone https://github.com/crate/cratedb-examples
    cd cratedb-examples
    python3 -m venv .venv
    source .venv/bin/activate
	pip install pg8000


********
Examples
********

Run an example program::

    python basic.py

