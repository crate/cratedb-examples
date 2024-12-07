"""
Using `records` with CrateDB: All data types.

    pip install --upgrade records sqlalchemy-cratedb

An end-to-end lifecycle, defining a table, inserting data, and querying it.
This example uses all data types supported by CrateDB.

- https://pypi.org/project/records/
- https://cratedb.com/docs/crate/reference/en/latest/general/ddl/data-types.html#supported-types
"""

from copy import deepcopy

import pytest
import records


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
    object={"for": "bar"},
    geopoint=[85.43, 66.23],
    geoshape="POLYGON ((5 5, 10 5, 10 10, 5 10, 5 5))",
    float_vector=[1.0, 2.0, 3.0],
)

# When querying it, a few values will be canonicalized.
RECORD_OUT = deepcopy(RECORD_IN)
RECORD_OUT.update(
    dict(
        bit="B'01010101'",
        char="foo  ",
        timestamp_tz=82800000,
        timestamp_notz=86400000,
        geopoint=[pytest.approx(85.43), pytest.approx(66.23)],
        geoshape={
            "coordinates": [
                [[5.0, 5.0], [5.0, 10.0], [10.0, 10.0], [10.0, 5.0], [5.0, 5.0]]
            ],
            "type": "Polygon",
        },
    )
)


def records_ddl_dml_dql():
    """
    Validate all types of CrateDB.

    https://cratedb.com/docs/crate/reference/en/latest/general/ddl/data-types.html#supported-types
    """
    db = records.Database("crate://", echo=True)

    # DDL
    db.query("DROP TABLE IF EXISTS testdrive.example;")
    db.query("""
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
        char CHARACTER(5),
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
    db.query(
        """
    INSERT INTO testdrive.example (
        null_integer,
        integer,
        bigint,
        float,
        double,
        decimal,
        bit,
        bool,
        text,
        char,
        timestamp_tz,
        timestamp_notz,
        ip,
        "array",
        "object",
        geopoint,
        geoshape,
        float_vector
    ) VALUES (
        :null_integer,
        :integer,
        :bigint,
        :float,
        :double,
        :decimal,
        :bit,
        :bool,
        :text,
        :char,
        :timestamp_tz,
        :timestamp_notz,
        :ip,
        :array,
        :object,
        :geopoint,
        :geoshape,
        :float_vector
    );
    """,
        **RECORD_IN,
    )

    # DQL
    db.query("REFRESH TABLE testdrive.example")
    rows = db.query("SELECT * FROM testdrive.example")
    data = rows.all()
    return data
