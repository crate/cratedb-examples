"""
Using `sqlframe` with CrateDB: All data types.

    pip install --upgrade sqlframe

An end-to-end lifecycle, defining a table, inserting data, and querying it.
This example uses all data types supported by CrateDB.

- https://pypi.org/project/sqlframe/
- https://cratedb.com/docs/crate/reference/en/latest/general/ddl/data-types.html#supported-types
"""

import datetime as dt
from copy import deepcopy
from unittest import mock

from psycopg2 import connect
from sqlframe import activate

from patch import monkeypatch


def connect_spark():
    # Connect to database.
    conn = connect(
        dbname="crate",
        user="crate",
        password="",
        host="localhost",
        port="5432",
    )
    # Activate SQLFrame to run directly on CrateDB.
    activate("postgres", conn=conn)

    from pyspark.sql import SparkSession

    spark = SparkSession.builder.getOrCreate()
    return spark


# The record that is inserted into the database.
RECORD_IN = dict(
    null_integer=None,
    integer=42,
    bigint=42,
    float=42.42,
    double=42.42,
    decimal=42.42,
    bit="01010101",
    bool=True,
    text="foobar",
    char="foo",
    timestamp_tz="1970-01-02T00:00:00+01:00",
    timestamp_notz="1970-01-02T00:00:00",
    ip="127.0.0.1",
    array=["foo", "bar"],
    object={"foo": "bar"},
    geopoint=[85.43, 66.23],
    geoshape="POLYGON ((5 5, 10 5, 10 10, 5 10, 5 5))",
    float_vector=[1.0, 2.0, 3.0],
)

# When querying it, a few values will be canonicalized.
RECORD_OUT = deepcopy(RECORD_IN)
RECORD_OUT.update(
    dict(
        char="foo  ",
        timestamp_tz=dt.datetime(1970, 1, 1, 23, 0, tzinfo=dt.timezone.utc),
        timestamp_notz=dt.datetime(1970, 1, 2, 0, 0, tzinfo=dt.timezone.utc),
        # FIXME: `geopoint` comes back as string, `'(85.42999997735023,66.22999997343868)'`
        # geopoint=[pytest.approx(85.43), pytest.approx(66.23)],
        geopoint=mock.ANY,
        geoshape={
            "coordinates": [
                [[5.0, 5.0], [5.0, 10.0], [10.0, 10.0], [10.0, 5.0], [5.0, 5.0]]
            ],
            "type": "Polygon",
        },
    )
)


def sqlframe_ddl_dml_dql():
    """
    Validate all types of CrateDB.

    https://cratedb.com/docs/crate/reference/en/latest/general/ddl/data-types.html#supported-types
    """
    spark = connect_spark()
    run_sql = spark._connection.cursor().execute

    FRAME_IN = spark.createDataFrame([RECORD_IN])

    # DDL
    run_sql("DROP TABLE IF EXISTS testdrive.example")
    run_sql("""
    CREATE TABLE testdrive.example (
        -- Numeric types
        null_integer INT,
        integer INT,
        bigint BIGINT,
        float FLOAT,
        double DOUBLE,
        decimal DECIMAL(8, 2),
        -- Other scalar types
        bit BIT(8),
        bool BOOLEAN,
        text TEXT,
        char CHAR(5),
        timestamp_tz TIMESTAMP WITH TIME ZONE,
        timestamp_notz TIMESTAMP WITHOUT TIME ZONE,
        ip IP,
        -- Container types
        "array" ARRAY(STRING),
        "object" OBJECT(DYNAMIC),
        -- Geospatial types
        geopoint GEO_POINT,
        geoshape GEO_SHAPE,
        -- Vector type
        "float_vector" FLOAT_VECTOR(3)
    );
    """)

    # DML
    FRAME_IN.write.saveAsTable("testdrive.example", mode="append")

    # DQL
    run_sql("REFRESH TABLE testdrive.example")
    data = spark.sql("SELECT * FROM testdrive.example").collect()
    return data


monkeypatch()


if __name__ == "__main__":
    print(sqlframe_ddl_dml_dql())
