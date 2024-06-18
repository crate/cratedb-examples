# MLflow and CrateDB


## About MLflow

[MLflow] is an open source platform to manage the ML lifecycle, including
experimentation, reproducibility, deployment, and a central model registry.
MLflow currently offers four components:

- [MLflow Tracking]\: Record and query experiments: code, data, config, and results
- [MLflow Projects]\: Package data science code in a format to reproduce runs on any platform
- [MLflow Models]\: Deploy machine learning models in diverse serving environments
- [MLflow Model Registry]\: Store, annotate, discover, and manage models in a central repository.

An [MLflow Model][MLflow Models] is a standard format for packaging machine
learning models that can be used in a variety of downstream tools—for example,
real-time serving through a REST API or batch inference on Apache Spark. The
format defines a convention that lets you save a model in different "flavors"
that can be understood by different downstream tools.


## What's inside

This folder provides guidelines and runnable code to get started with [MLflow]
and [CrateDB].

- [readme.md](readme.md): The file you are currently reading contains a walkthrough
  about how to install an MLflow stack, and how to use the [MLflow Tracking]
  subsystem on behalf on an experiment run.
- [requirements.txt](requirements.txt): Pulls in a patched version of MLflow,
  [mlflow-cratedb], and the [Merlion] library. MLflow has been adjusted not to
  invoke the database provisioning based on SQLAlchemy and Alembic, but uses a
  traditional approach by running a bunch of SQL DDL statements, fitted to be
  usable with CrateDB.
- [tracking_merlion.py](tracking_merlion.py): The example program uses [Merlion],
  a Python library for time series intelligence, which can be used for time series
  anomaly detection and forecasting. Before running an experiment for demonstration
  purposes, it will import the `machine_temperature_system_failure.csv` dataset
  from the [Numenta Anomaly Benchmark] data.


## Install

In order to properly setup a development sandbox environment, it is advised
to create a Python virtualenv, and install the dependencies there. In this
way, it is easy to wipe your virtualenv and start from scratch anytime.

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -U -r requirements.txt
```


## Setup

The upcoming commands expect that you are working on a terminal with
activated virtualenv.
```shell
source .venv/bin/activate
```

### CrateDB on localhost

In order to spin up a CrateDB instance without further ado, you can use
Docker or Podman.
```shell
docker run --rm -it \
  --name=cratedb --publish=4200:4200 --publish=5432:5432 \
  --env=CRATE_HEAP_SIZE=4g crate -Cdiscovery.type=single-node
```

Start the MLflow server, pointing it to your [CrateDB] instance,
running on `localhost`.
```shell
mlflow-cratedb server --backend-store-uri='crate://crate@localhost'
```

You can use `crash` to query for database records. Please note that the fork
of MLflow adjusted for CrateDB stores its tables into the `mlflow` schema,
so you will need to specify it when querying for data.
```shell
crash --command 'SELECT * FROM "mlflow"."experiments";'
crash --command 'SELECT * FROM "mlflow"."runs";'
```

### CrateDB Cloud

Prepare a few environment variables for convenience purposes. Replace `<PASSWORD>`
and `<CLUSTERNAME>` to match yours, and optionally also adjust `CRATEDB_USERNAME`.
```shell
export CRATEDB_USERNAME='admin'
export CRATEDB_PASSWORD='<PASSWORD>'
export CRATEDB_HOSTNAME='<CLUSTERNAME>.aks1.westeurope.azure.cratedb.net'
export CRATEDB_HTTP_URL="https://${CRATEDB_USERNAME}:${CRATEDB_PASSWORD}@${CRATEDB_HOSTNAME}:4200"
export CRATEDB_SQLALCHEMY_URL="crate://${CRATEDB_USERNAME}:${CRATEDB_PASSWORD}@${CRATEDB_HOSTNAME}:4200?ssl=true"
```

Start the MLflow server, connecting it to your [CrateDB Cloud] instance.
```shell
mlflow-cratedb server --backend-store-uri="${CRATEDB_SQLALCHEMY_URL}"
```

Use `crash` to connect to the CrateDB Cloud instance, and inquire the relevant
MLflow database tables.
```shell
crash --hosts "${CRATEDB_HTTP_URL}" --command 'SELECT * FROM "mlflow"."experiments";'
crash --hosts "${CRATEDB_HTTP_URL}" --command 'SELECT * FROM "mlflow"."runs";'
```

### Operations
In order to run SQL DDL statements manually, you can use the `crash` program.
```shell
crash < mlflow/store/tracking/dbmodels/ddl/cratedb.sql
crash < mlflow/store/tracking/dbmodels/ddl/drop.sql
```


## Run Experiment

In another terminal, run the Python program which defines the experiment. You can
point it towards the MLflow server you just started, using the `MLFLOW_TRACKING_URI`
environment variable, so the program will send events and outcomes from experiment
runs, and the MLflow server will record them.

```shell
# Use MLflow Tracking Server
export MLFLOW_TRACKING_URI=http://127.0.0.1:5000

python tracking_merlion.py
```

You can also record an experiment without running the MLflow Tracking Server.

```shell
# Use CrateDB database directly
export MLFLOW_TRACKING_URI="crate://crate@localhost/?schema=mlflow"

python tracking_merlion.py
```



[CrateDB]: https://github.com/crate/crate
[CrateDB Cloud]: https://console.cratedb.cloud/
[Merlion]: https://pypi.org/project/salesforce-merlion/
[MLflow]: https://mlflow.org/
[mlflow-cratedb]: https://github.com/crate-workbench/mlflow
[MLflow Models]: https://mlflow.org/docs/latest/models.html
[MLflow Model Registry]: https://mlflow.org/docs/latest/model-registry.html
[MLflow Projects]: https://mlflow.org/docs/latest/projects.html
[MLflow Tracking]: https://mlflow.org/docs/latest/tracking.html
[Numenta Anomaly Benchmark]: https://github.com/numenta/NAB
