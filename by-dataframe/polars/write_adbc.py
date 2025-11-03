"""
Import a Parquet file into CrateDB using Polars and ADBC.

FIXME: Will currently not work with CrateDB, as it uses `COPY FROM STDIN`.

Install dependencies:

  pip install polars pyarrow adbc-driver-postgresql
"""

import polars as pl


CRATEDB_URI = "postgresql://crate:crate@localhost:5432/?sslmode=disable"
TABLE_NAME = "testdrive_polars"
FILE_URI = "https://cdn.crate.io/downloads/datasets/cratedb-datasets/timeseries/yc.2019.07-tiny.parquet"


def main():
    df = pl.read_parquet(FILE_URI)

    df.write_database(
        engine="adbc",
        connection=CRATEDB_URI,
        table_name="testdrive_polars",
        if_table_exists="replace",
    )
    print(f"Records written to database table: {TABLE_NAME}")  # pragma: nocover

    # We can also write from other file types, polars have:

    # polars.read_database
    # polars.read_csv
    # polars.read_avro
    # polars.read_delta
    # polars.read_excel
    # polars.read_ods
    # polars.read_json
    # polars.read_ndjson


if __name__ == "__main__":
    main()
