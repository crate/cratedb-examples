import shlex
import sys

import requests
import logging
import platformdirs
from cratedb_toolkit.util import DatabaseAdapter
from git import Repo, RemoteProgress
import subprocess

logger = logging.getLogger(__name__)


class GitProgressPrinter(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=""):
        print(
            op_code,
            cur_count,
            max_count,
            cur_count / (max_count or 100.0),
            message or "NO MESSAGE",
            file=sys.stderr,
        )


def test_ctk_load_table_mongodb_json():
    """
    Probe importing data from MongoDB Extended JSON files.
    """

    # Define table names used for testing.
    table_names = [
        "books",
        "city_inspections",
        "companies",
        "countries-big",
        "countries-small",
        "covers",
        "grades",
        "products",
        "profiles",
        "restaurant",
        "students",
    ]

    # Define table cardinalities used in validation step.
    table_cardinalities = {
        "books": 431,
        "city_inspections": 81047,
        "companies": 2537,
        "countries-big": 21640,
        "countries-small": 248,
        "covers": 5071,
        "grades": 280,
        "products": 11,
        "profiles": 1515,
        "restaurant": 2548,
        "students": 200,
    }

    db = DatabaseAdapter("crate://localhost:4200/?schema=from-mongodb")

    # Drop tables for blank canvas.
    for table_name in table_names:
        db.drop_table(table_name)

    # Define path to source data.
    mongodb_json_files_path = platformdirs.user_cache_path("cratedb-examples") / "mongodb_json_files"
    datasets_path = mongodb_json_files_path / "datasets"

    # Acquire source data.
    if not datasets_path.exists():
        repository_url = "https://github.com/ozlerhakan/mongodb-json-files"
        print(f"Downloading repository: {repository_url}", file=sys.stderr)
        Repo.clone_from(
            url="https://github.com/ozlerhakan/mongodb-json-files",
            to_path=mongodb_json_files_path,
            progress=GitProgressPrinter(),
        )

    # Invoke data transfer.
    command = f"""
ctk load table \
    "file+bson://{datasets_path}/*.json?batch-size=2500" \
    --cratedb-sqlalchemy-url="crate://localhost:4200/from-mongodb"
"""
    print(f"Invoking CTK: {command}", file=sys.stderr)
    subprocess.check_call(shlex.split(command))

    # Validate data in database.
    results = db.run_sql("SHOW TABLES", records=True)
    results = [item["table_name"] for item in results]
    assert results == table_names

    cardinalities = {}
    for table_name, cardinality in table_cardinalities.items():
        cardinalities[table_name] = db.count_records(table_name)
    assert cardinalities == table_cardinalities
