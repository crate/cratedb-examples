# Streamlit with CrateDB Example

## About
Demonstrate connectivity from Streamlit to CrateDB.

## Configuration
Configure database connection address and credentials within
`.streamlit/secrets.toml` in your working directory. Please
make sure to use valid credentials matching your environment.

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
Please have a look at the [secrets-cratedb-cloud.toml](.streamlit/secrets-cratedb-cloud.toml)
file as a blueprint. It includes a configuration snippet that is essential for
connecting to CrateDB Cloud.
```toml
[connections.cratedb.create_engine_kwargs.connect_args]
ssl = true
```

Install dependencies.
```shell
pip install -r requirements.txt
```

Invoke Streamlit to serve the application.
```shell
streamlit run basic_sys_summits.py
```

## Screenshot

Enjoy the list of mountains.

![image](https://github.com/crate/cratedb-examples/assets/453543/7dc54224-06d0-4cfb-a5e0-b216c03bf3d2)


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
ngr test framework/streamlit
```
