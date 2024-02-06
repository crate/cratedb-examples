"""
## About

Test cases for timeseries exploration and analysis examples with CrateDB and PyViz.


## Synopsis

Run all test cases.
```
pytest
```

Run individual test cases.
```
pytest -k file
pytest -k notebook
```
"""
from pathlib import Path
from testbook import testbook

HERE = Path(__file__).parent


def test_cloud_datashader():

    notebook = HERE / "cloud-datashader.ipynb"
    with testbook(str(notebook)) as tb:
        tb.inject(
            """
            df = pd.read_csv("yellow_tripdata_sample.csv")
            """,
            run=False,
            after=9,
        )
        with tb.patch("cratedb_toolkit.ManagedCluster") as mock_cluster:
            tb.execute()
