"""
Using `records` with CrateDB: Basic usage.

    pip install --upgrade records sqlalchemy-cratedb

A few basic operations using the `records` library with CrateDB.

- https://pypi.org/project/records/
"""

import records


def records_select_sys_summits():
    """
    Query CrateDB's built-in `sys.summits` table.
    :return:
    """
    db = records.Database("crate://", echo=True)
    rows = db.query("SELECT * FROM sys.summits ORDER BY height DESC LIMIT 3")
    data = rows.all()
    return data


def records_export_sys_summits_pandas():
    """
    Query CrateDB's built-in `sys.summits` table, returning a pandas dataframe.
    """
    db = records.Database("crate://", echo=True)
    rows = db.query("SELECT * FROM sys.summits ORDER BY height DESC LIMIT 3")
    data = rows.export("df")
    return data


def records_export_sys_summits_csv():
    """
    Query CrateDB's built-in `sys.summits` table, returning CSV.
    """
    db = records.Database("crate://", echo=True)
    rows = db.query("SELECT * FROM sys.summits ORDER BY height DESC LIMIT 3")
    data = rows.export("csv")
    return data


def records_get_table_names():
    """
    Inquire table names of the system schema `sys`.
    """
    db = records.Database("crate://?schema=sys", echo=True)
    table_names = db.get_table_names()
    return table_names


if __name__ == "__main__":
    print(records_select_sys_summits())
    print(records_export_sys_summits_pandas())
    print(records_export_sys_summits_csv())
    print(records_get_table_names())
