import shlex
import sys
from collections import OrderedDict

import pytest
import typing as t
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


@pytest.fixture()
def drop_testing_tables():
    """
    Drop tables used for testing purposes, to let each test case have a blank canvas.
    """

    db = DatabaseAdapter("crate://localhost:4200/")

    table_names = [
        "from-influxdb.air-sensor-data",
        "from-mongodb.books",
        "from-mongodb.city_inspections",
        "from-mongodb.companies",
        "from-mongodb.countries-big",
        "from-mongodb.countries-small",
        "from-mongodb.covers",
        "from-mongodb.grades",
        "from-mongodb.products",
        "from-mongodb.profiles",
        "from-mongodb.restaurant",
        "from-mongodb.students",
    ]

    for table_name in table_names:
        db.drop_table(table_name)


def get_table_cardinalities(db: DatabaseAdapter, table_names: t.List[str]) -> t.Dict[str, int]:
    """
    Inquire table cardinalities for given table names.
    """
    cardinalities = OrderedDict()
    for table_name in table_names:
        # Synchronize writes.
        db.refresh_table(table_name)
        # Inquire table count.
        cardinalities[table_name] = db.count_records(table_name)
    return cardinalities


def test_ctk_load_table_influxdb_lp(drop_testing_tables):
    """
    Probe importing data from InfluxDB Line Protocol file.
    """

    db = DatabaseAdapter("crate://localhost:4200/?schema=from-influxdb")

    # Define table cardinalities used in validation step.
    table_cardinalities = {
        "air-sensor-data": 5288,
    }

    # Define path to source data.
    influxdb_files_path = platformdirs.user_cache_path("cratedb-examples") / "influxdb_files"
    influxdb_files_path.mkdir(parents=True, exist_ok=True)

    # Define resource of source data.
    influxdb_lp_url = "https://github.com/influxdata/influxdb2-sample-data/raw/master/air-sensor-data/air-sensor-data.lp"

    # Invoke data transfer.
    command = f"""
influxio copy \
    {influxdb_lp_url} \
    "crate://localhost:4200/from-influxdb/air-sensor-data"
    """
    print(f"Invoking CTK: {command}", file=sys.stderr)
    subprocess.check_call(shlex.split(command))

    # Validate data in target database.
    cardinalities = get_table_cardinalities(db, table_cardinalities.keys())
    assert cardinalities == table_cardinalities


def test_ctk_load_table_mongodb_json(drop_testing_tables):
    """
    Probe importing data from MongoDB Extended JSON files.
    """

    db = DatabaseAdapter("crate://localhost:4200/?schema=from-mongodb")

    # Define table cardinalities used in validation step.
    table_cardinalities = {
        "books": 431,
        "city_inspections": 81047,
        "companies": 18801,
        "countries-big": 21640,
        "countries-small": 248,
        "covers": 5071,
        "grades": 280,
        "products": 11,
        "profiles": 1515,
        "restaurant": 2548,
        "students": 200,
    }

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

        # The `countries-big.json` file contains bogus characters.
        countries_big_path = datasets_path / "countries-big.json"
        payload = countries_big_path.read_text()
        payload = payload.replace("\ufeff", "")
        countries_big_path.write_text(payload)

    # Invoke data transfer.
    command = f"""
ctk load table \
    "file+bson://{datasets_path}/*.json?batch-size=2500" \
    --cratedb-sqlalchemy-url="crate://localhost:4200/from-mongodb" \
    --transformation=zyp-mongodb-json-files.yaml
"""
    print(f"Invoking CTK: {command}", file=sys.stderr)
    subprocess.check_call(shlex.split(command))

    # Validate data in target database.
    cardinalities = get_table_cardinalities(db, table_cardinalities.keys())
    assert cardinalities == table_cardinalities
