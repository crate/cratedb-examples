"""
About
=====

Evaluate saving Dask DataFrames into CrateDB.

Usage
=====
::

    docker run --rm -it --publish=4200:4200 --publish=5432:5432 crate
    pip install --upgrade 'crate[sqlalchemy]' dask pandas
    python insert_dask.py

"""
import dask.dataframe as dd
from dask.diagnostics import ProgressBar
from pandas._testing import makeTimeDataFrame


DBURI = "crate://localhost:4200"


def main():
    pbar = ProgressBar()
    pbar.register()

    # Create example Dask DataFrame for testing purposes.
    df = makeTimeDataFrame(nper=125_000, freq="S")
    ddf = dd.from_pandas(df, npartitions=4)

    # Save DataFrame into CrateDB efficiently.

    # Works. Takes ~3 seconds.
    ddf.to_sql("testdrive", uri=DBURI, index=False, if_exists="replace", chunksize=10_000, parallel=True)

    # Works. Takes ~10 seconds.
    # ddf.to_sql("testdrive", uri=DBURI, index=False, if_exists="replace", chunksize=10_000, parallel=True, method="multi")


if __name__ == "__main__":
    main()
