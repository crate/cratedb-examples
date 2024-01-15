"""
Thanks to Polars, we can seamlessly move data from one Polars' compatible
database to another.
"""


def postgres_to_cratedb(table_name, pg_uri, crate_uri):
    """
    Copies `table_name` from Postgres to CrateDB

    Note:
        When specifying the query for Postgres, you might need to specify the
        database name and schema, for example, `mydatabase.public.ny_taxi` and
        when can leave just 'ny_taxi' in the Crate part, creating the table in
        `doc.ny_taxi`.
    """
    df = polars.read_database_uri(f'SELECT * FROM {table_name}', pg_uri, engine='adbc')
    df.write_database(table_name, crate_uri)


def mysql_to_cratedb(table_name, mysql_uri, crate_uri):
    """Moves `table_name` from Postgres to CrateDB

    Note:
        You will need to install 'adbc-driver-mysql pyarrow'
    """
    df = polars.read_database_uri(f'SELECT * FROM {table_name}', mysql_uri, engine='adbc')
    df.write_database(table_name, crate_uri)


# At this point, you probably see the pattern, if polars can connect to it, we can write
# to CrateDB!
#
# We can change the engine to `sqlalchemy` (or remote the parameter, since it's the default value)
# meaning that any Database that has a sqlalchemy driver can be used to read from.
