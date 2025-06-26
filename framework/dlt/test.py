import logging

import pytest
from cratedb_toolkit.util.database import DatabaseAdapter
from pueblo.sfa.core import run

logger = logging.getLogger()


@pytest.fixture(scope="session")
def db():
    return DatabaseAdapter("crate://")


def test_basic_load_api(db):
    """
    Verify dlt pipeline loading data from an API.
    """

    # Invoke database import.
    run("basic.py:load_api_data", {})

    # Validate database content.
    db.refresh_table("doc.chess_players")
    records = db.run_sql("SELECT * FROM doc.chess_players", records=True)
    assert len(records) >= 2
    names = [record["name"] for record in records]
    assert "Magnus Carlsen" in names
    assert "Praggnanandhaa Rameshbabu" in names


def test_basic_load_pandas(db):
    """
    Verify dlt pipeline loading data from a pandas dataframe that has been populated from CSV data.
    """

    # Invoke database import.
    run("basic.py:load_pandas_data", {})

    # Validate database content.
    db.refresh_table("doc.natural_disasters")
    records = db.run_sql("SELECT * FROM doc.natural_disasters", records=True)
    assert len(records) >= 837
    entities = [record["entity"] for record in records]
    assert "Flood" in entities
    assert "Landslide" in entities
    assert "Wildfire" in entities


def test_basic_load_sql(db):
    """
    Verify dlt pipeline loading data from an SQL database.
    """

    # Invoke database import.
    run("basic.py:load_sql_data", {})

    # Validate database content.
    db.refresh_table("doc.genome")
    records = db.run_sql("SELECT * FROM doc.genome", records=True)
    assert len(records) >= 1000


def test_basic_load_github(db):
    """
    Verify dlt pipeline loading data from GitHub.
    """

    # Invoke database import.
    run("basic.py:load_github_data", {})

    # Validate database content.
    db.refresh_table("doc.github_api_data")
    records = db.run_sql("SELECT * FROM doc.github_api_data", records=True)
    assert len(records) >= 50


# TODO: Investigate Pokemon API integration failure.
@pytest.mark.skip(reason="Pokemon API integration broken - stopped working on 24 Jun 2025 - needs investigation.")
def test_pokemon(db):
    """
    Verify the dlt pokemon example.
    """

    # Invoke database import.
    run("pokemon.py:main", {})

    # Validate database content.
    db.refresh_table("doc.pokemon")
    records = db.run_sql("SELECT * FROM doc.pokemon", records=True)
    assert len(records) >= 20
