from sqlframe.base.catalog import Table

from example_basic import (
    sqlframe_export_sys_summits_csv,
    sqlframe_export_sys_summits_pandas,
    sqlframe_get_table_names,
    sqlframe_select_sys_summits,
)
from example_types import RECORD_OUT, sqlframe_ddl_dml_dql


def test_sys_summits():
    """
    Read built-in data from CrateDB's `sys` table through `sqlframe`.
    """
    data = sqlframe_select_sys_summits().collect()
    assert data[0]["mountain"] == "Ortler"


def test_get_table_names():
    """
    Validate inquiry of tables from `sys´ schema.
    """
    data = sqlframe_get_table_names()
    assert (
        Table(
            name="nodes",
            catalog="crate",
            namespace=["sys"],
            description=None,
            tableType="MANAGED",
            isTemporary=False,
        )
        in data
    )
    assert (
        Table(
            name="shards",
            catalog="crate",
            namespace=["sys"],
            description=None,
            tableType="MANAGED",
            isTemporary=False,
        )
        in data
    )
    assert len(data) > 10


def test_export_sys_summits_pandas():
    """
    Validate exporting to pandas data frame works.
    """
    data = sqlframe_export_sys_summits_pandas()
    assert list(data["mountain"]) == ["Ortler", "Königspitze", "Monte Cevedale"]


def test_export_sys_summits_csv():
    """
    Validate exporting to CSV works.
    """
    data = sqlframe_export_sys_summits_csv()
    assert "classification,coordinates,country" in data
    assert "Mont Blanc,4695,U-Savoy/Aosta" in data


def test_ddl_dml_dql():
    """
    Validate an end-to-end lifecycle, defining a table, inserting data, and querying it.
    This example uses all data types supported by CrateDB.
    """
    data = sqlframe_ddl_dml_dql()
    assert data[0].asDict() == RECORD_OUT
