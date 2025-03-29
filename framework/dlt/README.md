# dlt with CrateDB example

## About
Demonstrate connectivity from dlt to CrateDB.

## Configuration
Configure database connection address and credentials in `.dlt/secrets.toml`.
Please make sure to use valid credentials matching your environment.

For [CrateDB] on localhost, a default configuration snippet looks like this.
```toml
[destination.cratedb.credentials]
host = "localhost"                       # CrateDB server host.
port = 5432                              # CrateDB PostgreSQL TCP protocol port, default is 5432.
username = "crate"                       # CrateDB username, default is usually "crate".
password = ""                            # CrateDB password, if any.
```

For [CrateDB Cloud], a configuration snippet looks like this.
```toml
[destination.cratedb.credentials]
host = "<CLUSTERNAME>.eks1.eu-west-1.aws.cratedb.net"    # CrateDB server host.
port = 5432                                              # CrateDB PostgreSQL TCP protocol port, default is 5432.
username = "admin"                                       # CrateDB username, default is usually "admin".
password = "<PASSWORD>"                                  # CrateDB password, if any.
```

## Usage

Install dependencies.
```shell
pip install -r requirements.txt
```

Invoke two example pipelines.
```shell
python basic.py
python pokemon.py
```

## Appendix

### CrateDB on localhost
Start a CrateDB instance on your machine.
```shell
docker run -it --rm \
  --publish=4200:4200 --publish=5432:5432 \
  --env=CRATE_HEAP_SIZE=2g \
  crate:latest -Cdiscovery.type=single-node
```

### Sandbox
Acquire `cratedb-example` repository, and set up a development sandbox.
```shell
git clone https://github.com/crate/cratedb-examples
cd cratedb-examples
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Software tests
Invoke the integration test cases.
```shell
ngr test framework/dlt
```


[CrateDB]: https://github.com/crate/crate
[CrateDB Cloud]: https://console.cratedb.cloud/
