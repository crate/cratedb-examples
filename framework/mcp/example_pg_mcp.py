# PG-MCP Model Context Protocol Server for CrateDB
# https://github.com/stuzero/pg-mcp-server
# https://github.com/crate-workbench/pg-mcp-server
#
# Derived from:
# https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#writing-mcp-clients
from cratedb_toolkit.util.database import DatabaseAdapter
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import where

from mcp_utils import McpDatabaseConversation


async def run():
    # Create server parameters for stdio connection.
    server_params = StdioServerParameters(
        command=where.first("python"),
        args=["example_pg_mcp_server.py"],
        env={},
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
            read, write
        ) as session:
            # Initialize the connection.
            await session.initialize()

            client = McpDatabaseConversation(session)
            await client.inquire()

            print("## MCP server conversations")
            print()

            # Provision database content.
            db = DatabaseAdapter("crate://crate@localhost:4200/")
            db.run_sql("CREATE TABLE IF NOT EXISTS mcp_pg_mcp (id INT, data TEXT)")
            db.run_sql("INSERT INTO mcp_pg_mcp (id, data) VALUES (42, 'Hotzenplotz')")
            db.refresh_table("mcp_pg_mcp")

            # Call a few tools.
            connection_string = "postgresql://crate@localhost/doc"

            # Connect to the database, receiving the connection UUID.
            response = await client.call_tool("connect", arguments={"connection_string": connection_string})
            conn_id = client.decode_json_text(response)["conn_id"]

            # Query and explain, using the connection id.
            await client.call_tool("pg_query", arguments={
                "query": "SELECT * FROM sys.summits ORDER BY height DESC LIMIT 3",
                "conn_id": conn_id,
            })
            await client.call_tool("pg_explain", arguments={
                "query": "SELECT * FROM mcp_pg_mcp",
                "conn_id": conn_id,
            })

            # Read a few resources.
            schema = "sys"
            table = "summits"
            await client.read_resource(f"pgmcp://{conn_id}/")
            await client.read_resource(f"pgmcp://{conn_id}/schemas")
            await client.read_resource(f"pgmcp://{conn_id}/schemas/{schema}/tables")
            await client.read_resource(f"pgmcp://{conn_id}/schemas/{schema}/tables/{table}/columns")
            #await client.read_resource(f"pgmcp://{conn_id}/schemas/{schema}/tables/{table}/indexes")
            #await client.read_resource(f"pgmcp://{conn_id}/schemas/{schema}/tables/{table}/constraints")
            #await client.read_resource(f"pgmcp://{conn_id}/schemas/{schema}/tables/{table}/indexes/{index}")
            #await client.read_resource(f"pgmcp://{conn_id}/schemas/{schema}/tables/{table}/constraints/{constraint}")
            #await client.read_resource(f"pgmcp://{conn_id}/schemas/{schema}/extensions")
            #await client.read_resource(f"pgmcp://{conn_id}/schemas/{schema}/extensions/{extension}")
            await client.read_resource(f"pgmcp://{conn_id}/schemas/{schema}/tables/{table}/sample")
            await client.read_resource(f"pgmcp://{conn_id}/schemas/{schema}/tables/{table}/rowcount")

            # Invoke a prompt.
            await client.get_prompt("nl_to_sql_prompt", arguments={
                "query": "Give me 5 Austria mountains",
            })

            # Disconnect again.
            await client.call_tool("disconnect", arguments={"conn_id": conn_id,})


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
