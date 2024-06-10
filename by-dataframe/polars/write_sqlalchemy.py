"""
Import a parquet file into CrateDB using polars + sqlalchemy

Install the dependencies to run this program::

    pip install --upgrade pandas polars pyarrow sqlalchemy-cratedb
"""

import polars

CRATE_URI = 'crate://localhost:4200'
FILE_PATH = '/home/taxi_data.parquet'

df = polars.read_parquet(FILE_PATH)
df.write_database(table='ny_taxi',
                  connection=CRATE_URI,
                  if_table_exists='append')
