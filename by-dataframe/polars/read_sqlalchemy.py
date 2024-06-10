"""
Install the dependencies to run this program::

    pip install --upgrade polars sqlalchemy-cratedb
"""

import polars
from sqlalchemy import create_engine

CRATE_URI = 'crate://localhost:4200'
QUERY = 'SELECT * FROM ny_taxi'

# LIMITATION: This uses the http protocol, 1.9GB is the max amount of data you can
# select, use batches, `COPY TO`, or Postgres wire protocol to circumvent this limitation.


df = polars.read_database(
    query=QUERY,
    connection=create_engine(CRATE_URI).connect(),
)
