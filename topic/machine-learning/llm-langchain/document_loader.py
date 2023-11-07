"""
Exercise the LangChain/CrateDB document loader.

How to use the SQL document loader, based on SQLAlchemy.

The example uses the canonical `mlb_teams_2012.csv`,
converted to SQL, see `mlb_teams_2012.sql`.

Synopsis::

    # Install prerequisites.
    pip install -r requirements.txt

    # Start database.
    docker run --rm -it --publish=4200:4200 crate/crate:nightly

    # Provide input data: Acquire SQL file and populate database.
    # TODO: Refactor into general purpose package.
    wget https://github.com/crate-workbench/langchain/raw/cratedb/docs/docs/integrations/document_loaders/example_data/mlb_teams_2012.sql
    crash < mlb_teams_2012.sql

    # Run program.
    export CRATEDB_CONNECTION_STRING="crate://crate@localhost/?schema=doc"
    python document_loader.py
"""
import os

from langchain.document_loaders import CrateDBLoader
from pprint import pprint


CONNECTION_STRING = os.environ.get(
    "CRATEDB_CONNECTION_STRING",
    "crate://crate@localhost/?schema=doc"
)


def main():
    loader = CrateDBLoader(
        query="SELECT * FROM doc.mlb_teams_2012 LIMIT 3;",
        url=CONNECTION_STRING,
        include_rownum_into_metadata=True,
    )
    docs = loader.load()
    pprint(docs)


if __name__ == "__main__":
    main()
