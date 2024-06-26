from streamlit.testing.v1 import AppTest


def test_read_sys_summits():
    """
    Verify reading CrateDB's built-in `sys.summits` database table through Streamlit.
    """

    # Invoke Streamlit application.
    at = AppTest.from_file("basic_sys_summits.py").run()

    # There should not be an exception.
    assert not at.exception

    # Probe dataframe output.
    df = at.dataframe.values[0]
    mountains = df["mountain"].values
    assert "Mont Blanc" in mountains
    assert "Matterhorn" in mountains

    # Probe table output.
    df = at.table.values[0]
    mountains = df["mountain"].values
    assert "Mont Blanc" in mountains
    assert "Matterhorn" in mountains

    # Probe Markdown output.
    assert "Mont Blanc" in at.markdown.values
    assert "Monte Rosa" in at.markdown.values
