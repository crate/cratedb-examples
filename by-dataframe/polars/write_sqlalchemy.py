"""
Efficient data imports using CrateDB, Polars, and SQLAlchemy.

The `insert_bulk` utility provides efficient bulk data transfers
when using dataframe libraries like pandas, Dask, and Polars.

You will observe that the optimal chunk size highly depends on the
shape of your data, specifically the width of each record, i.e. the
number of columns and their individual sizes, which will in the end
determine the total size of each batch/chunk.

https://cratedb.com/docs/sqlalchemy-cratedb/support.html#bulk-support-for-pandas-and-dask
https://cratedb.com/docs/sqlalchemy-cratedb/dataframe.html#efficient-insert-operations-with-pandas
https://cratedb.com/docs/crate/reference/en/latest/interfaces/http.html#bulk-operations

Install dependencies:

  pip install --upgrade pandas polars pyarrow sqlalchemy-cratedb
"""

import polars as pl
import sqlalchemy as sa
from sqlalchemy_cratedb import insert_bulk

CRATEDB_URI = "crate://crate:crate@localhost:4200"
TABLE_NAME = "testdrive_polars"
FILE_URI = "https://cdn.crate.io/downloads/datasets/cratedb-datasets/timeseries/yc.2019.07-tiny.parquet"


def main():
    df = pl.read_parquet(FILE_URI, use_pyarrow=True)
    engine = sa.create_engine(CRATEDB_URI)
    df.write_database(
        engine="sqlalchemy",
        connection=engine,
        table_name=TABLE_NAME,
        if_table_exists="replace",
        engine_options={
            "method": insert_bulk,
            "chunksize": 20_000,
        },
    )
    print(f"Records written to database table: {TABLE_NAME}")


if __name__ == "__main__":
    main()
