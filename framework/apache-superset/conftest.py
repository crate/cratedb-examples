import os
import shlex
import shutil
import subprocess
import time

import pytest
import requests

from util import get_auth_headers


superset_env = {
    "FLASK_APP": "superset",
    "SUPERSET_CONFIG_PATH": "superset_config.py",
}
superset_bin = shutil.which("superset")


uri_database = "http://localhost:8088/api/v1/database/"


# Utility functions.

def invoke_superset(command: str):
    """
    Invoke `superset` command.
    """
    command = f"{superset_bin} {command}"
    subprocess.check_call(shlex.split(command), env=superset_env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


# Test suite fixtures.

@pytest.fixture(scope="session")
def fix_greenlet():
    """
    Install more recent greenlet, because Playwright installs version 3.0.1, which breaks Superset.
    """
    os.system("pip install --upgrade greenlet")


@pytest.fixture(scope="session")
def playwright_install_firefox():
    """
    Playwright needs a browser.
    """
    os.system("playwright install firefox")


@pytest.fixture(scope="session")
def initialize_superset():
    """
    Run the Apache Superset setup procedure.
    """
    invoke_superset("db upgrade")
    invoke_superset("fab create-admin --username=admin --password=admin --firstname=admin --lastname=admin --email=admin@example.org")
    invoke_superset("init")


@pytest.fixture(scope="session")
def reset_superset():
    """
    Reset database connections and datasets.
    """
    resources_to_delete = [
        "http://localhost:8088/api/v1/dataset/1",
        "http://localhost:8088/api/v1/dataset/2",
        "http://localhost:8088/api/v1/database/1",
        "http://localhost:8088/api/v1/database/2",
    ]
    for resource_to_delete in resources_to_delete:
        response = requests.delete(resource_to_delete, headers=get_auth_headers())
        assert response.status_code in [200, 404], response.json()


@pytest.fixture(scope="session")
def start_superset():
    """
    Start the Apache Superset server.
    """
    command = f"{superset_bin} run -p 8088 --with-threads"
    daemon = subprocess.Popen(shlex.split(command), env=superset_env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # Give the server time to start
    time.sleep(4)
    # Check it started successfully
    assert not daemon.poll(), daemon.stdout.read().decode("utf-8")
    yield daemon
    # Shut it down at the end of the pytest session
    daemon.terminate()


@pytest.fixture(scope="session")
def provision_superset(start_superset):
    """
    Provision Superset by creating a database connection object for CrateDB.
    """

    # Create a data source item / database connection.
    response = requests.post(
        uri_database,
        headers=get_auth_headers(),
        json={"database_name": "CrateDB Testdrive", "engine": "crate", "sqlalchemy_uri": "crate://crate@localhost:4200"},
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "result": {
            "configuration_method": "sqlalchemy_form",
            "database_name": "CrateDB Testdrive",
            "driver": "crate-python",
            "expose_in_sqllab": True,
            "sqlalchemy_uri": "crate://crate@localhost:4200",
        },
    }


@pytest.fixture(scope="session", autouse=True)
def do_setup(
        fix_greenlet,
        playwright_install_firefox,
        initialize_superset,
        start_superset,
        reset_superset,
        provision_superset,
):
    """
    Provide a fully configured and provisioned Apache Superset instance to the test suite.
    """
    pass
