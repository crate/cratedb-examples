"""
Writes a parquet file to CrateDB using polars + adbc

Install the dependencies with:

```
$ pip install polars pyarrow adbc-driver-postgresql
```
"""

import polars

CRATE_URI = 'postgresql://crate@localhost:5432'
FILE_PATH = '/data/yellow_tripdata_2023-01.parquet'

df = polars.read_parquet('/data/yellow_tripdata_2023-01.parquet')

df.write_database(table_name='ny_taxi',
                  connection=CRATE_URI,
                  if_table_exists='append',
                  engine='adbc')

# We can also write from other file types, polars have:

# polars.read_database
# polars.read_csv
# polars.read_avro
# polars.read_delta
# polars.read_excel
# polars.read_ods
# polars.read_json
# polars.read_ndjson
