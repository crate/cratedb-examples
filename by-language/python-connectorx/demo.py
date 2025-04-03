"""
Example program connecting to CrateDB [1] using ConnectorX [2],
using its PostgreSQL interface [3].

[1] https://cratedb.com/database
[2] https://sfu-db.github.io/connector-x/
[3] https://sfu-db.github.io/connector-x/databases/postgres.html
"""

# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "connectorx<0.5",
#     "pandas>2,<3",
# ]
# ///

from pprint import pprint
import connectorx as cx


def main():
    data = cx.read_sql(
        "postgresql://crate@localhost/",
        "SELECT country, height, mountain, range, region FROM sys.summits ORDER BY height DESC LIMIT 10",
        protocol="cursor",
    )
    pprint(data)


if __name__ == "__main__":
    main()
