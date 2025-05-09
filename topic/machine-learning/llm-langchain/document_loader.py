
"""
Exercise the LangChain/CrateDB document loader.

How to use the SQL document loader, based on SQLAlchemy.

The example uses the canonical `mlb_teams_2012.csv`,
converted to SQL, see `mlb_teams_2012.sql`.

Synopsis::

    # Install prerequisites.
    pip install -U -r requirements.txt

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

import requests
import sqlalchemy as sa
from cratedb_toolkit.util.database import DatabaseAdapter
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_cratedb.loaders import CrateDBLoader
from pprint import pprint


CONNECTION_STRING = os.environ.get(
    "CRATEDB_CONNECTION_STRING",
    "crate://crate@localhost/?schema=doc"
)


def import_mlb_teams_2012():
    """
    Import data into database table `mlb_teams_2012`.

    TODO: Refactor into general purpose package.
    """
    cratedb = DatabaseAdapter(dburi=CONNECTION_STRING)
    url = "https://github.com/crate-workbench/langchain/raw/cratedb/docs/docs/integrations/document_loaders/example_data/mlb_teams_2012.sql"
    sql = requests.get(url).text
    cratedb.run_sql(sql)
    cratedb.refresh_table("mlb_teams_2012")


def main():
    # Load data.
    import_mlb_teams_2012()

    db = SQLDatabase(engine=sa.create_engine(CONNECTION_STRING))

    # Query data.
    loader = CrateDBLoader(
        query="SELECT * FROM mlb_teams_2012 LIMIT 3;",
        db=db,
        include_rownum_into_metadata=True,
    )
    docs = loader.load()
    pprint(docs)


if __name__ == "__main__":
    main()
