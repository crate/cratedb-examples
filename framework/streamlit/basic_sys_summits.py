"""
A basic Streamlit application connecting to CrateDB using SQLAlchemy.

It reads the built-in `sys.summits` table into a dataframe, and
displays its contents.

- https://docs.streamlit.io/develop/tutorials/databases
- https://cratedb.com/docs/sqlalchemy-cratedb/
"""
import streamlit as st

# Set a title for the page.
st.title("Streamlit with CrateDB Example")

# Connect to CrateDB, and read the built-in `sys.summits` table.
conn = st.connection("cratedb", type="sql")
df = conn.query('SELECT * FROM "sys"."summits";', ttl="10m")

# Output data as dataframe and table.
st.dataframe(df)
st.table(df)

# Output data as Markdown.
for row in df.itertuples():
    st.write(f"{row.mountain}")
