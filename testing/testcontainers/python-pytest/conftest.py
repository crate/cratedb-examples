"""
Using "Testcontainers for Python" with CrateDB and pytest

pytest fixtures providing CrateDB containers. `CRATEDB_VERSION` selects the
CrateDB version, for example `6.3`, and defaults to `nightly`.

https://github.com/testcontainers/testcontainers-python
"""
import os

import pytest
from testcontainers.community.cratedb import CrateDBContainer

CRATEDB_VERSION = os.environ.get("CRATEDB_VERSION") or "nightly"
# Nightly builds are published as `crate/crate`, releases as the official `crate` image.
CRATEDB_IMAGE = "crate/crate:nightly" if CRATEDB_VERSION == "nightly" else f"crate:{CRATEDB_VERSION}"


@pytest.fixture(scope="session")
def cratedb():
    """
    One CrateDB container, started once and shared by every test in the session.
    """
    with CrateDBContainer(CRATEDB_IMAGE) as container:
        yield container


@pytest.fixture
def private_cratedb():
    """
    A CrateDB container of its own for a single test, discarded afterwards.
    """
    with CrateDBContainer(CRATEDB_IMAGE) as container:
        yield container


@pytest.fixture
def cratedb_http_url(cratedb):
    """
    The address of the shared container's HTTP interface.
    """
    return f"http://{cratedb.get_container_host_ip()}:{cratedb.get_exposed_port(4200)}"
