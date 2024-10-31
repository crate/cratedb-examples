"""
About
=====

Example program to demonstrate connecting to CrateDB using
its Python DB API driver, and the HTTP protocol.


Setup
=====
::

    pip install --upgrade crate


Synopsis
========
::

    # Run CrateDB
    docker run --rm -it --publish=4200:4200 crate

    # Invoke example program.
    time python select_basic.py

"""
import sys
from pprint import pprint

import crate.client


def select_basic():
    """
    Demonstrate a basic conversation with CrateDB, querying its built-in `sys.summits` table.
    """
    connection = crate.client.connect("http://localhost:4200")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sys.summits LIMIT 3;")
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    pprint(results)


if __name__ == "__main__":
    select_basic()
