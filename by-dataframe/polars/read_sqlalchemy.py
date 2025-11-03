"""
Read from CrateDB using Polars and SQLAlchemy.

Install dependencies:

  pip install polars sqlalchemy-cratedb
"""

import polars as pl
import sqlalchemy as sa

CRATEDB_URI = "crate://crate:crate@localhost:4200"
SQL_QUERY = "SELECT * FROM sys.summits ORDER BY height DESC LIMIT 3"


def main():
    # LIMITATION:
    # This uses the HTTP protocol; 1.9GB is the max amount of data you can
    # select; use batches, `COPY TO`, or the PostgreSQL wire protocol to
    # overcome this limitation.
    engine = sa.create_engine(CRATEDB_URI)
    df = pl.read_database(
        query=SQL_QUERY,
        connection=engine,
    )
    print(df)


if __name__ == "__main__":
    main()
