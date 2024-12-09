from metabase_rig import MetabaseRig

pytest_plugins = ["docker_compose"]


def test_api_sys_summits(session_scoped_container_getter):
    """
    End-to-end test reading data from CrateDB through Metabase.
    """
    rig = MetabaseRig("http://localhost:3000/")

    # Login to and optionally provision Metabase.
    try:
        rig.login()
    except:
        rig.setup()
        rig.login()

    # Acquire a database handle, optionally creating a database.
    db = rig.database("cratedb-testdrive")
    if not db.exists():
        db.create()

    # Wait for the `sys` schema to become available.
    db.wait_schema("sys")

    # Validate a table exists in the `sys` schema.
    assert "sys.summits" in db.table_names(schema_name="sys")

    # Wait for the `sys.summits` table to become available.
    db.wait_table("sys", "summits")

    # Query the `sys.summits` table.
    data = db.query("summits")
    assert data["data"]["rows"][0][5] == "Mont Blanc"
