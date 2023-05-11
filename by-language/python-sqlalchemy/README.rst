.. highlight: console

############################################################
Connect to CrateDB and CrateDB Cloud using Python/SQLAlchemy
############################################################


*****
About
*****

Example programs demonstrating CrateDB's SQLAlchemy adapter and dialect.


*****
Usage
*****

To start a CrateDB instance on your machine for evaluation purposes, invoke::

    docker run -it --rm --publish=4200:4200 --publish=5432:5432 crate

Navigate to example program directory, and install prerequisites::

    # Acquire sources.
    git clone https://github.com/crate/cratedb-examples
    cd cratedb-examples/by-language/python-sqlalchemy
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade click colorlog 'crate[sqlalchemy]' dask pandas sqlalchemy

Run example programs::

    # Connect to CrateDB on localhost.

    time python insert_efficient.py cratedb multirow
    time python insert_efficient.py cratedb batched

    time python insert_pandas.py
    time python insert_pandas.py --mode=basic --insertmanyvalues-page-size=5000
    time python insert_pandas.py --mode=bulk --bulk-size=20000 --num-records=75000

    # Connect to CrateDB Cloud.
    time python insert_pandas.py --dburi='crate://admin:<PASSWORD>@example.aks1.westeurope.azure.cratedb.net:4200?ssl=true'

.. TIP::

    For more information, please refer to the header section of each of the provided example programs.
