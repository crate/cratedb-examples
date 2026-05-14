"""
Periodic tasks with CrateDB.

- Query `sys.summits` table.
- Import data from HTTP and export data to S3 bucket.

## References

- For time-based scheduling options with Apache Airflow, see:
  https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/timetable.html

- A detailed tutorial is available at:
  https://community.crate.io/t/cratedb-and-apache-airflow-automating-data-export-to-s3/901

- The original source is available at:
  https://github.com/crate/cratedb-airflow-tutorial/blob/main/dags/table_export_dag.py
"""
import os
from airflow import DAG
from airflow.sdk import chain, task
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from cratedb_toolkit.io.router import IoRouter
from cratedb_toolkit.model import DatabaseAddress, InputOutputResource


with DAG(
    dag_id="sys_summits",
    description="Example DAG for plain-text SQL task.",
    default_args={"conn_id": "cratedb_connection"},
    schedule="*/1 * * * *",  # @continuous, @daily
    catchup=False,
    max_active_runs=1,
):
    """A basic DAG with a single task that emits an SQL DQL command."""

    @task.sql(split_statements=True, return_last=False)
    def execute_query_taskflow():
        return "SELECT * FROM sys.summits ORDER BY height DESC LIMIT 3;"

    execute_query_taskflow()


with DAG(
    dag_id="import_export",
    description="Example DAG for SQLExecuteQueryOperator",
    default_args={"conn_id": "cratedb_connection"},
    schedule="*/5 * * * *",  # @continuous, @daily
    catchup=False,
    max_active_runs=1,
):
    """
    A DAG with three chained tasks that emit SQL commands implementing a data movement pipeline.
    
    1. Create database table with SQL DDL using `CREATE TABLE`.
    2. Import CSV from HTTP location into CrateDB table using `COPY FROM`.
    3. Export table from CrateDB into S3 bucket using `COPY TO`.
    """

    params = {
        "table": "testdrive.weather_data",
    }

    ddl = SQLExecuteQueryOperator(
        task_id="submit_ddl",
        conn_id="cratedb_connection",
        sql="""
        CREATE TABLE IF NOT EXISTS {{params.table}} (
            "timestamp" TIMESTAMP,
            "location" VARCHAR,
            "temperature" DOUBLE,
            "humidity" DOUBLE,
            "wind_speed" DOUBLE
        );
        """,
        params=params,
    )

    insert = SQLExecuteQueryOperator(
        task_id="import_from_http",
        conn_id="cratedb_connection",
        sql="""
        COPY {{params.table}}
        FROM 'https://cdn.crate.io/downloads/datasets/cratedb-datasets/cloud-tutorials/data_weather.csv.gz'
        WITH (format='csv', compression='gzip', empty_string_as_null=true)
        RETURN SUMMARY;
        """,
        params=params,
    )

    export = SQLExecuteQueryOperator(
        task_id="export_to_s3",
        conn_id="cratedb_connection",
        sql="""
        COPY {{params.table}}
        TO DIRECTORY 's3://{{params.access}}:{{params.secret}}@{{params.host}}:{{params.port}}/{{params.bucket}}/{{params.path}}'
        WITH (protocol='http', use_path_style_access=true);
        """,
        params={
            **params,
            "host": "rustfs",
            "port": "9000",
            "bucket": "testdrive",
            "path": "weather_data",
            "access": "accesskey",
            "secret": "secretkey",
        },
    )

    # Execute tasks in order.
    chain(ddl, insert, export)


with DAG(
    dag_id="export_deltalake",
    description="Example DAG for CrateDB Toolkit I/O",
    default_args={"conn_id": "cratedb_connection"},
    schedule="*/5 * * * *",  # @continuous, @daily
    catchup=False,
    max_active_runs=1,
):
    """
    """
    # ctk save "crate://crate:crate@cratedb:4200/sys/summits" "file+deltalake:///var/delta/summits?mode=overwrite"
    io = IoRouter()
    io.save_table(
        source=DatabaseAddress(os.getenv("CRATEDB_SQLALCHEMY_URL", "crate://") + "/sys/summits"),
        target=InputOutputResource(url="file+deltalake:///tmp/delta/summits?mode=overwrite"),
    )
