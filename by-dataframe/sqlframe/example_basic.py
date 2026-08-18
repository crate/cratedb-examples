"""
Using `sqlframe` with CrateDB: Basic usage.

    pip install --upgrade sqlframe

A few basic operations using the `sqlframe` library with CrateDB.

- https://pypi.org/project/sqlframe/
"""

from psycopg2 import connect
from sqlframe import activate
from sqlframe.base.functions import col

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


def sqlframe_select_sys_summits():
    """
    Query CrateDB's built-in `sys.summits` table.
    :return:
    """
    spark = connect_spark()
    df = spark.sql(
        spark.table("sys.summits")
        .where(col("region").ilike("ortler%"))
        .sort(col("height").desc())
        .limit(3)
    )
    print(df.sql())
    df.show()
    return df


def sqlframe_export_sys_summits_pandas():
    """
    Query CrateDB's built-in `sys.summits` table, returning a pandas dataframe.
    """
    spark = connect_spark()
    df = spark.sql(
        spark.table("sys.summits")
        .where(col("region").ilike("ortler%"))
        .sort(col("height").desc())
        .limit(3)
    ).toPandas()
    return df


def sqlframe_export_sys_summits_csv():
    """
    Query CrateDB's built-in `sys.summits` table, saving the output to CSV.
    """
    spark = connect_spark()
    df = spark.sql(
        spark.table("sys.summits")
        .where(col("region").ilike("ortler%"))
        .sort(col("height").desc())
        .limit(3)
    )
    df.write.csv("summits.csv", mode="overwrite")
    return df


def sqlframe_get_table_names():
    """
    Inquire table names of the system schema `sys`.
    """
    spark = connect_spark()
    tables = spark.catalog.listTables(dbName="sys")
    return tables


monkeypatch()


if __name__ == "__main__":
    print(sqlframe_select_sys_summits())
    print(sqlframe_export_sys_summits_pandas())
    print(sqlframe_export_sys_summits_csv())
    print(sqlframe_get_table_names())
