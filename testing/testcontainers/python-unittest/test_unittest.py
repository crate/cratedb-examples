"""
Using "Testcontainers for Python" with CrateDB and unittest

Start one CrateDB container for the test module, and run a query through the
CrateDB Python driver and through the `crash` command-line client.

https://github.com/testcontainers/testcontainers-python
"""
import os
import subprocess
from unittest import TestCase, addModuleCleanup

from crate import client
from testcontainers.community.cratedb import CrateDBContainer

CRATEDB_VERSION = os.environ.get("CRATEDB_VERSION") or "nightly"
# Nightly builds are published as `crate/crate`, releases as the official `crate` image.
CRATEDB_IMAGE = "crate/crate:nightly" if CRATEDB_VERSION == "nightly" else f"crate:{CRATEDB_VERSION}"

SQL_STATEMENT = "SELECT mountain FROM sys.summits ORDER BY height DESC LIMIT 3"
HIGHEST_SUMMITS = ["Mont Blanc", "Monte Rosa", "Dom"]

cratedb = CrateDBContainer(CRATEDB_IMAGE)
http_url = None


def setUpModule():
    global http_url
    cratedb.start()
    addModuleCleanup(cratedb.stop)
    http_url = f"http://{cratedb.get_container_host_ip()}:{cratedb.get_exposed_port(4200)}"


class CrateDBTest(TestCase):

    def test_sql(self):
        with client.connect(http_url, username="crate") as connection:
            cursor = connection.cursor()
            cursor.execute(SQL_STATEMENT)
            self.assertEqual([row[0] for row in cursor.fetchall()], HIGHEST_SUMMITS)

    def test_crash(self):
        output = subprocess.check_output(
            ["crash", "--hosts", http_url, "--format", "csv", "--command", "SELECT 1 + 1 AS two"],
            text=True,
        )
        self.assertEqual(output.split(), ["two", "2"])
