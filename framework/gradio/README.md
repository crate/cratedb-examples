# Gradio with CrateDB Example

## About
Demonstrate connectivity from Gradio to CrateDB.

## Configuration
Configure database connection address and credentials by using
an SQLAlchemy connection string, see variable `CRATEDB_SQLALCHEMY_URL`
in `basic_sys_summits.py`. Please make sure to use valid credentials
matching your environment.

## Usage

### CrateDB on localhost
To start a CrateDB instance on your machine, invoke:
```shell
docker run -it --rm \
  --publish=4200:4200 --publish=5432:5432 \
  --env=CRATE_HEAP_SIZE=2g \
  crate:latest -Cdiscovery.type=single-node
```

### CrateDB Cloud
Please have a look at the [basic_sys_summits.py](basic_sys_summits.py) program
as a blueprint. It includes a `CRATEDB_SQLALCHEMY_URL` variable definition
that configures the application to connect to CrateDB Cloud.
```python
CRATEDB_SQLALCHEMY_URL = "crate://admin:g_,8.F0fNbVSk0.*!n54S5c,@example.gke1.us-central1.gcp.cratedb.net:4200?ssl=true"```
```

Install dependencies.
```shell
pip install -r requirements.txt
```

Invoke Gradio to serve the application.
```shell
gradio basic_sys_summits.py
```

## Screenshot

Enjoy the list of mountains.

![image](https://github.com/crate/cratedb-examples/assets/453543/af417966-b694-45ec-9391-f0e99a2ac014)


## Development

Acquire `cratedb-example` repository, and set up development sandbox.
```shell
git clone https://github.com/crate/cratedb-examples
cd cratedb-examples
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Invoke the integration test cases.
```shell
ngr test framework/gradio
```
