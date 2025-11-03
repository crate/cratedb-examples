"""
Read from CrateDB using Polars and ConnectorX.

Install dependencies:

  pip install polars connectorx
"""

import polars as pl

CRATEDB_URI = "postgresql://crate:crate@localhost:5432/?sslmode=disable"
SQL_QUERY = "SELECT mountain, height, latitude(coordinates), longitude(coordinates) FROM sys.summits ORDER BY height DESC LIMIT 3"


def main():
    df = pl.read_database_uri(query=SQL_QUERY, uri=CRATEDB_URI, protocol="cursor")
    print(df)


if __name__ == "__main__":
    main()
