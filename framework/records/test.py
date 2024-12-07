from example_basic import (
    records_select_sys_summits,
    records_get_table_names,
    records_export_sys_summits_csv,
    records_export_sys_summits_pandas,
)
from example_types import records_ddl_dml_dql, RECORD_OUT


def test_sys_summits():
    """
    Read built-in data from CrateDB's `sys` table through `records`.
    """
    data = records_select_sys_summits()
    assert data[0]["mountain"] == "Mont Blanc"


def test_get_table_names():
    data = records_get_table_names()
    assert "nodes" in data
    assert "shards" in data
    assert len(data) > 10


def test_export_sys_summits_pandas():
    data = records_export_sys_summits_pandas()
    assert list(data["mountain"]) == ["Mont Blanc", "Monte Rosa", "Dom"]


def test_export_sys_summits_csv():
    data = records_export_sys_summits_csv()
    assert "classification,coordinates,country" in data
    assert "Mont Blanc,4695,U-Savoy/Aosta" in data


def test_ddl_dml_dql():
    """
    Validate an end-to-end lifecycle, defining a table, inserting data, and querying it.
    This example uses all data types supported by CrateDB.
    """
    data = records_ddl_dml_dql()
    assert data[0].as_dict() == RECORD_OUT
