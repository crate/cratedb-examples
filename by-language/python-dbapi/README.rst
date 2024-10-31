.. highlight: console

########################################################
Connect to CrateDB and CrateDB Cloud using Python DB API
########################################################


*****
About
*****

Example programs demonstrating CrateDB's DB API adapter,
for the HTTP protocol.


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

    ngr test by-language/python-dbapi


********
Examples
********

Run an example program::

    time python select_basic.py
    time python insert_basic.py

.. TIP::

    For more information, please refer to the header sections of each of the
    provided example programs.


*****
Tests
*****

To test the accompanied example programs all at once, invoke the software tests::

    pytest


.. _CrateDB: https://github.com/crate/crate
