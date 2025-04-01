"""
Example program connecting to CrateDB [1] using turbodbc [2].

[1] https://cratedb.com/database
[2] https://turbodbc.readthedocs.io/
"""

import os
import sys

from turbodbc import connect


def main():
    # Connect to database.
    # https://turbodbc.readthedocs.io/en/latest/pages/getting_started.html#establish-a-connection-with-your-database

    # Either connect per data source name defined within the ODBC configuration,
    # connection = connect(dsn="postgresql", server="localhost", database="testdrive", uid="crate", pwd=None)

    # ... or connect per connection string, referencing a driver file directly.
    if sys.platform == "linux":
        candidates = [
            # archlinux
            "/usr/lib/psqlodbcw.so",
            # Debian
            "/usr/lib/x86_64-linux-gnu/odbc/psqlodbcw.so",
            # Red Hat
            "/usr/lib64/psqlodbcw.so",
        ]
        driver_file = find_program(candidates)
        if driver_file is None:
            raise ValueError(f"Unable to detect driver file at {candidates}")
    elif sys.platform == "darwin":
        driver_file = "/usr/local/lib/psqlodbcw.so"
    else:
        raise NotImplementedError(f"Platform {sys.platform} not supported yet")

    connection_string = (
        f"Driver={driver_file};Server=localhost;Port=5432;Database=testdrive;Uid=crate;Pwd=;"
    )
    print(f"INFO: Connecting to '{connection_string}'")
    connection = connect(connection_string=connection_string)
    print()

    # Query `sys.summits`.
    print("sys.summits")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sys.summits ORDER by height DESC LIMIT 10")
    for row in cursor:
        print(row)
    cursor.close()
    print()

    # Insert data.
    print("doc.testdrive")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS testdrive (id INT PRIMARY KEY, data TEXT);")
    cursor.execute("DELETE FROM testdrive;")
    cursor.execute("INSERT INTO testdrive VALUES (0, 'zero'), (1, 'one'), (2, 'two');")
    cursor.executemany(
        "INSERT INTO testdrive VALUES (?, ?);", [(3, "three"), (4, "four"), (5, "five")]
    )
    cursor.execute("REFRESH TABLE testdrive;")
    cursor.close()

    # Query data.
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM testdrive ORDER BY id")

    print("Column metadata:")
    print(cursor.description)

    print("Results by row:")
    for row in cursor:
        print(row)

    cursor.close()
    print()

    # Terminate database connection.
    connection.close()


def find_program(candidates):
    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate


if __name__ == "__main__":
    main()
