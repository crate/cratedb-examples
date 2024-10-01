"""
About
=====

Evaluate reading data from CrateDB into pandas dataframes.

Example program to demonstrate reading data in batches from CrateDB into
pandas, using SQLAlchemy, supporting urllib3 vs. psycopg3.


Setup
=====
::

    pip install --upgrade click pandas 'sqlalchemy-cratedb[all]'


Synopsis
========
::

    # Run CrateDB.
    docker run --rm -it --publish=4200:4200 --publish=5432:5432 crate:latest

    # Use CrateDB, either talking HTTP, or PostgreSQL wire protocol.
    python read_pandas.py --dburi='crate+urllib3://crate@localhost:4200'
    python read_pandas.py --dburi='crate+psycopg://crate@localhost:5432'

    # Use bulk size parameter to exercise paging.
    python read_pandas.py --bulk-size 50

    # Use CrateDB Cloud.
    python read_pandas.py --dburi='crate://admin:<PASSWORD>@example.aks1.westeurope.azure.cratedb.net:4200?ssl=true'


Details
=======
To watch the HTTP traffic to your local CrateDB instance, invoke::

    sudo ngrep -d lo0 -Wbyline port 4200

"""
import logging

import click
import pandas as pd
import sqlalchemy as sa
from pueblo.util.logging import setup_logging

logger = logging.getLogger(__name__)


SQLALCHEMY_LOGGING = True


class DatabaseWorkload:

    table_name = "testdrive_pandas"

    def __init__(self, dburi: str):
        self.dburi = dburi

    def get_engine(self, **kwargs):
        return sa.create_engine(self.dburi, **kwargs)

    def process(self, bulk_size: int):
        """
        Exercise different insert methods of pandas, SQLAlchemy, and CrateDB.
        """

        logger.info(f"Connecting to {self.dburi}")
        logger.info(f"Reading data with bulk_size={bulk_size}")

        engine = self.get_engine()
        frames = pd.read_sql(sql="SELECT * FROM sys.summits;", con=engine, chunksize=bulk_size)
        for df in frames:
            print(df)


def tweak_log_levels(level=logging.INFO):

    # Enable SQLAlchemy logging.
    if SQLALCHEMY_LOGGING:
        logging.getLogger("sqlalchemy").setLevel(level)


@click.command()
@click.option("--dburi", type=str, default="crate://localhost:4200", required=False, help="SQLAlchemy database connection URI.")
@click.option("--bulk-size", type=int, default=5_000, required=False, help="Bulk size / chunk size.")
@click.help_option()
def main(dburi: str, bulk_size: int):
    setup_logging()
    tweak_log_levels()
    dbw = DatabaseWorkload(dburi=dburi)
    dbw.process(bulk_size)


if __name__ == "__main__":
    main()
