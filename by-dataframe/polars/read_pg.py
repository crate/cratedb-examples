"""
Install the dependencies with:

```
$ pip install polars connectorx
```
"""

import polars as pl

CRATE_URI = 'postgresql://crate@localhost:5432'
QUERY = 'SELECT * FROM ny_taxi'

df = pl.read_database_uri(QUERY, CRATE_URI, protocol='cursor')