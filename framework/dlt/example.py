from dlt.common.schema import typing

# default dlt columns
typing.C_DLT_ID = "__dlt_id"
"""unique id of current row"""
typing.C_DLT_LOAD_ID = "__dlt_load_id"
"""load id to identify records loaded in a single load package"""

import dlt
from dlt.sources.helpers import requests

# Create a dlt pipeline that will load
# chess player data to the DuckDB destination
pipeline = dlt.pipeline(
    pipeline_name='chess_pipeline',
    destination=dlt.destinations.sqlalchemy("crate://crate:@localhost/"),
    #destination=dlt.destinations.postgres("postgresql://postgres:@localhost/"),
    dataset_name='doc',
)

# Grab some player data from Chess.com API
data = []
for player in ['magnuscarlsen', 'rpragchess']:
    response = requests.get(f'https://api.chess.com/pub/player/{player}')
    response.raise_for_status()
    data.append(response.json())

# Extract, normalize, and load the data
if __name__ == "__main__":
    pipeline.run(data,
        table_name='player',
    )
