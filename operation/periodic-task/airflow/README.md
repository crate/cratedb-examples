# Periodic tasks with CrateDB and Apache Airflow

This folder includes a collection of examples about how to schedule periodic
tasks alongside CrateDB with [Apache Airflow].

## What's inside

- `compose.yaml`: A service bundle of CrateDB, RustFS, and Airflow.
- `Dockerfile`: Bundles scheduled payload and its requirements.
- `workflows.py`: The Airflow DAG workflow definitions.
- `requirements.txt`: The Python packages needed to run the workflow.

## Launch system

Launch Airflow.
```shell
docker compose up --build scheduler
```

## User interface

Display password for `admin` user.
```shell
docker compose exec scheduler cat simple_auth_manager_passwords.json.generated
```

Navigate to http://localhost:8080/.

## Operate

If your DAGs don't start running, check for any hard errors.
```shell
docker compose exec scheduler sh -c 'airflow dags list-import-errors'
```

List available DAGs.
```shell
docker compose exec scheduler sh -c 'airflow dags list'
```

List runs of specific DAG.
```shell
docker compose exec scheduler sh -c 'airflow dags list-runs sys_summits'
docker compose exec scheduler sh -c 'airflow dags list-runs import_export'
```

Invoke DAG workflow manually.
```shell
docker compose exec scheduler sh -c 'airflow dags trigger import_export'
```

Check state of DAG.
```shell
docker compose exec scheduler sh -c 'airflow tasks state export_job export_to_s3 scheduled__2021-11-11T00:00:11+00:00'
```


[Apache Airflow]: https://airflow.apache.org/
