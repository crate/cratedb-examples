# Verify Apache Superset with CrateDB

## About

This folder includes software integration tests for verifying
that Apache Superset works well together with CrateDB.

## Setup

You can also exercise the configuration and setup steps manually.

Start CrateDB.
```bash
docker run --rm -it --name=cratedb \
  --publish=4200:4200 --publish=5432:5432 \
  --env=CRATE_HEAP_SIZE=4g crate:latest -Cdiscovery.type=single-node
```

Setup sandbox and install packages.
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Configure and initialize Apache Superset.
```bash
export FLASK_APP=superset
export SUPERSET_CONFIG_PATH=superset_config.py
superset db upgrade
superset fab create-admin --username=admin --password=admin --firstname=admin --lastname=admin --email=admin@example.org
superset init
```

Run Superset server.
```bash
superset run -p 8088 --with-threads
open http://127.0.0.1:8088/
```

## API Usage

```bash
# Authenticate and acquire a JWT token.
AUTH_TOKEN=$(http http://localhost:8088/api/v1/security/login username=admin password=admin provider=db | jq -r .access_token)

# Create a data source item / database connection.
http http://localhost:8088/api/v1/database/ database_name="CrateDB Testdrive" engine=crate sqlalchemy_uri=crate://crate@localhost:4200 Authorization:"Bearer ${AUTH_TOKEN}"
```

```bash
# Create datasets and probe them.
crash < data.sql
http http://127.0.0.1:8088/api/v1/dataset/ Authorization:"Bearer ${AUTH_TOKEN}" database=1 schema=doc table_name=devices_info
http http://127.0.0.1:8088/api/v1/dataset/ Authorization:"Bearer ${AUTH_TOKEN}" database=1 schema=doc table_name=devices_readings
cat probe-1.json | http http://127.0.0.1:8088/api/v1/chart/data Authorization:"Bearer ${AUTH_TOKEN}"
cat probe-2.json | http http://127.0.0.1:8088/api/v1/chart/data Authorization:"Bearer ${AUTH_TOKEN}"
```
