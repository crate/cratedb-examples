"""
A basic Gradio application connecting to CrateDB using SQLAlchemy.

It reads the built-in `sys.summits` table into a dataframe, and
displays its contents.

- https://www.gradio.app/guides/connecting-to-a-database
- https://www.gradio.app/docs/gradio/dataframe
- https://cratedb.com/docs/sqlalchemy-cratedb/
"""
import gradio as gr
import pandas as pd

# Connect to CrateDB on localhost.
CRATEDB_SQLALCHEMY_URL = "crate://localhost:4200"

# Connect to CrateDB Cloud.
# CRATEDB_SQLALCHEMY_URL = "crate://admin:g_,8.F0fNbVSk0.*!n54S5c,@example.gke1.us-central1.gcp.cratedb.net:4200?ssl=true"


def get_sys_summits():
    """
    Query the database using pandas.
    """
    return pd.read_sql('SELECT * FROM "sys"."summits";', con=CRATEDB_SQLALCHEMY_URL)


def get_dataframe():
    """
    Create a dataframe widget.
    """
    df = get_sys_summits()
    return gr.DataFrame(df)


# Define the Gradio interface.
demo = gr.Interface(
    fn=get_dataframe,
    inputs=[],
    outputs=["dataframe"],
    title="Gradio with CrateDB Example",
    live=True,
    allow_flagging="never",
)


if __name__ == "__main__":
    demo.launch()
