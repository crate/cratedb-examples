"""
About
=====

Evaluate inserting data from Dask dataframes into CrateDB.

Setup
=====
::

    pip install --upgrade click colorlog pandas sqlalchemy-cratedb

Synopsis
========
::

    docker run --rm -it --publish=4200:4200 --publish=5432:5432 crate:latest
    python insert_dask.py
"""
import logging

import click
import dask.dataframe as dd
from dask.diagnostics import ProgressBar
from pueblo.testing.pandas import makeTimeDataFrame
from pueblo.util.logging import setup_logging
from sqlalchemy_cratedb.support import insert_bulk

logger = logging.getLogger(__name__)

SQLALCHEMY_LOGGING = True
TABLE_NAME = "testdrive_dask"


def db_workload(dburi: str, mode: str, num_records: int, bulk_size: int):
    pbar = ProgressBar()
    pbar.register()

    # Create example Dask DataFrame for testing purposes.
    df = makeTimeDataFrame(nper=num_records, freq="S")
    ddf = dd.from_pandas(df, npartitions=4)

    # Save DataFrame into CrateDB efficiently.

    # Works. Takes ~3 seconds.
    if mode == "basic":
        ddf.to_sql(TABLE_NAME, uri=dburi, index=False, if_exists="replace", chunksize=bulk_size, parallel=True)

    # Works. Takes ~10 seconds.
    elif mode == "multi":
        ddf.to_sql(TABLE_NAME, uri=dburi, index=False, if_exists="replace", chunksize=bulk_size, parallel=True, method="multi")

    # Works. Takes ~2 seconds.
    elif mode == "bulk":
        ddf.to_sql(TABLE_NAME, uri=dburi, index=False, if_exists="replace", chunksize=bulk_size, parallel=True, method=insert_bulk)


@click.command()
@click.option("--dburi", type=str, default="crate://localhost:4200", required=False, help="SQLAlchemy database connection URI.")
@click.option("--mode", type=click.Choice(['basic', 'multi', 'bulk']), default="bulk", required=False, help="Insert mode.")
@click.option("--num-records", type=int, default=125_000, required=False, help="Number of records to insert.")
@click.option("--bulk-size", type=int, default=10_000, required=False, help="Bulk size / chunk size.")
@click.help_option()
def main(dburi: str, mode: str, num_records: int, bulk_size: int):
    setup_logging()
    db_workload(dburi=dburi, mode=mode, num_records=num_records, bulk_size=bulk_size)


if __name__ == "__main__":
    main()
