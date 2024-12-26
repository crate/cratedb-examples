# Source:
# https://docs.marimo.io/guides/working_with_data/dataframes.html
# https://github.com/marimo-team/marimo/blob/main/examples/sql/querying_dataframes.py

# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "duckdb",
#     "marimo",
#     "pandas==2.2.3",
#     "sqlalchemy-cratedb",
#     "sqlalchemy==2.0.36",
# ]
# ///

import marimo

__generated_with = "0.10.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        # Querying CrateDB using dataframes

        This notebook shows how to use Marimo and CrateDB, with Python dataframes and SQL.

        First, we create a dataframe called `df`, populated with content from CrateDB's
        built-in `sys.summits` table.
        """
    )
    return


@app.cell
def _():
    import pandas as pd
    import sqlalchemy as sa

    engine = sa.create_engine("crate://")
    df = pd.read_sql(sql="SELECT * FROM sys.summits ORDER BY height DESC", con=engine)

    print(df)
    df
    return df, engine, pd, sa


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        f"""
        Next, we **create a SQL cell**.

        Create a SQL cell in one of two ways:

        1. Click the {mo.icon("lucide:database")} `SQL` button at the **bottom of your notebook**
        2. **Right-click** the {mo.icon("lucide:circle-plus")} button to the **left of a cell**, and choose `SQL`.

        In the SQL cell, you can query dataframes in your notebook as if they were tables — just reference them by name.
        For querying a data frame using SQL, Marimo uses DuckDB.
        """
    )
    return


@app.cell
def _(df, mo):
    result = mo.sql(
        f"""
        SELECT * FROM df WHERE region LIKE 'Bernina%' ORDER BY height DESC
        """,
        output=False,
    )
    return (result,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        The query output is returned to Python as a dataframe (Polars if you have it installed, Pandas otherwise).

        Choose the dataframe name via the **output variable** input in the bottom-left of the cell. If the name starts with an underscore, it won't be made available to other cells.

        In this case, we've named the output `result`.
        """
    )
    return


@app.cell
def _(result):
    print(result)
    result
    return


if __name__ == "__main__":
    app.run()
