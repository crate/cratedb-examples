# About
Tutorial about migrating data from InfluxDB to CrateDB.

# Status
This is a work in progress.

# Plan

- For creating data, use [tutorial_sine_wave.py].
- For exporting data, use [influxdb-fetcher].
- For importing data, use [influxdb-write-to-postgresql].

[tutorial_sine_wave.py]: https://github.com/influxdata/influxdb-python/blob/master/examples/tutorial_sine_wave.py
[influxdb-fetcher]: https://github.com/hgomez/influxdb
[influxdb-write-to-postgresql]: https://github.com/eras/influxdb-write-to-postgresql


# Setup
```sh
# Install sine wave generator
python3 -m venv .venv
source .venv/bin/activate
pip install influxdb
wget https://raw.githubusercontent.com/influxdata/influxdb-python/master/examples/tutorial_sine_wave.py
# Comment out the line `client.drop_database(DBNAME)` at line 60/61.

# Install InfluxDB Fetcher
wget --no-clobber --output-document=/usr/local/bin/influxdb-fetcher https://raw.githubusercontent.com/hgomez/influxdb-fetcher/develop/bin/influxdb-fetcher
chmod +x /usr/local/bin/influxdb-fetcher

# Install iw2pg: Build Docker image
git clone https://github.com/eras/influxdb-write-to-postgresql
cd influxdb-write-to-postgresql; docker build --tag iw2pg .; cd ..
```


# Run with PostgreSQL
```sh
# Run databases and iw2pg side by side
docker run -it --rm --publish 8086:8086 influxdb:1.8.3
docker run -it --rm --env "POSTGRES_HOST_AUTH_METHOD=trust" --publish 5432:5432 --name postgresql postgres:13.1
docker run -it --rm --publish 8087:8086 --link postgresql --volume $PWD/iw2pg-config-postgresql.yaml:/app/config.yaml iw2pg --verbosity=info

# Create data
python tutorial_sine_wave.py

# Export data
influxdb-fetcher http://localhost:8086 root root tutorial "SELECT * FROM foobar" > foobar.wireproto

# Import data
psql postgres://postgres:postgres@localhost --command='CREATE DATABASE tutorial;'
cat foobar.wireproto | http http://localhost:8087/write?db=tutorial

# Verify data
psql postgres://postgres:postgres@localhost/tutorial --command='SELECT * FROM foobar;'
```

# Run with CrateDB
```sh
# Run databases and iw2pg side by side
docker run -it --rm --publish 8086:8086 influxdb:1.8.3
docker run -it --rm --publish 5432:5432 --name cratedb crate/crate:nightly
docker run -it --rm --publish 8087:8086 --link cratedb --volume $PWD/iw2pg-config-cratedb.yaml:/app/config.yaml iw2pg --verbosity=info

# Create data
python tutorial_sine_wave.py

# Export data
influxdb-fetcher http://localhost:8086 root root tutorial "SELECT * FROM foobar" > foobar.wireproto

# Import data
cat foobar.wireproto | http http://localhost:8087/write?db=tutorial
```


## Bummer
```text
Result status PGRES_FATAL_ERROR unexpected (expected status:PGRES_TUPLES_OK); ERROR:  Relation 'pg_indexes' unknown
```
