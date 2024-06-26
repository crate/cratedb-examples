# Streamlit with CrateDB Example

## About
Demonstrate connectivity from Streamlit to CrateDB.

## Configuration
Configure database connection address and credentials within
`.streamlit/secrets.toml` in your working directory. Please
make sure to use valid credentials matching your environment.

## Usage
To start a CrateDB instance on your machine, invoke:
```shell
docker run -it --rm \
  --publish=4200:4200 --publish=5432:5432 \
  --env=CRATE_HEAP_SIZE=2g \
  crate:latest -Cdiscovery.type=single-node
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
