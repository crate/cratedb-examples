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


CRATEDB_URL = "http://localhost:4200"


def vector_io():
    """
    Demonstrate a basic conversation with CrateDB, inserting and querying vector embeddings.
    """
    connection = crate.client.connect(CRATEDB_URL)

    # Insert.
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS testdrive.foo;")
    cursor.execute("CREATE TABLE testdrive.foo (id INT, embedding FLOAT_VECTOR(3));")
    cursor.execute("INSERT INTO testdrive.foo (id, embedding) VALUES (42, [42.42, 43.43, 44.44]);")
    cursor.execute("INSERT INTO testdrive.foo (id, embedding) VALUES (43, ?);", parameters=[[84.84, 85.85, 86.86]])
    cursor.execute("REFRESH TABLE testdrive.foo;")
    cursor.close()

    # Select.
    cursor = connection.cursor()

    # Literal `knn_match`.
    print("knn_match: literal")
    cursor.execute(
        "SELECT * FROM testdrive.foo WHERE knn_match(embedding, [1.1, 2.2, 3.3], 1);")
    results = cursor.fetchall()
    pprint(results)

    # `knn_match` with parameters.
    print("knn_match: with parameters")
    cursor.execute(
        "SELECT * FROM testdrive.foo WHERE knn_match(embedding, ?, 1);", parameters=[[1.1, 2.2, 3.3]])
    results = cursor.fetchall()
    pprint(results)

    # Literal `vector_similarity`.
    print("vector_similarity: literal")
    cursor.execute(
        "SELECT *, vector_similarity(embedding, [1.1, 2.2, 3.3]) AS _score "
        "FROM testdrive.foo ORDER BY _score DESC;")
    results = cursor.fetchall()
    pprint(results)

    # `vector_similarity` with parameters.
    print("vector_similarity: with parameters")
    cursor.execute(
        "SELECT *, vector_similarity(embedding, ?) AS _score "
        "FROM testdrive.foo ORDER BY _score DESC;", parameters=[[1.1, 2.2, 3.3]])
    results = cursor.fetchall()
    pprint(results)

    # All together now.
    print("knn_match and vector_similarity")
    cursor.execute(
        "SELECT id, embedding, vector_similarity(embedding, ?) AS _score FROM testdrive.foo "
        "WHERE knn_match(embedding, ?, ?) ORDER BY _score DESC LIMIT ?;",
        parameters=[[1.1, 2.2, 3.3], [1.1, 2.2, 3.3], 1, 1])
    results = cursor.fetchall()
    pprint(results)

    cursor.close()
    connection.close()


if __name__ == "__main__":
    vector_io()
