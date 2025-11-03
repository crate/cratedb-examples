"""
Import a Parquet file into CrateDB using Polars and SQLAlchemy.

Install dependencies:

  pip install --upgrade pandas polars pyarrow sqlalchemy-cratedb
"""

import polars as pl
import sqlalchemy as sa

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
    )
    print(f"Records written to database table: {TABLE_NAME}")


if __name__ == "__main__":
    main()
