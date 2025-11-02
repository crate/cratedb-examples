# DBHub Model Context Protocol Server for PostgreSQL
# https://github.com/bytebase/dbhub
#
# Derived from:
# https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#writing-mcp-clients
from cratedb_toolkit.util.database import DatabaseAdapter
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from mcp_utils import McpDatabaseConversation

# Create server parameters for stdio connection.
server_params_npx = StdioServerParameters(
    command="npx",
    args=[
        "-y",
        "@bytebase/dbhub@0.11.6",
        "--transport=stdio",
        #"--transport=sse",
        #"--port=8080",
        "--dsn=postgres://crate@localhost:5432/doc",
    ],
    env=None,
)

async def run():
    async with stdio_client(server_params_npx) as (read, write):
        async with ClientSession(
            read, write
        ) as session:
            # Initialize the connection
            await session.initialize()

            client = McpDatabaseConversation(session)
            await client.inquire()

            print("## MCP server conversations")
            print()

            # Call a few tools.
            await client.call_tool("run_query", arguments={"query": "SELECT * FROM sys.summits ORDER BY height DESC LIMIT 3"})
            await client.call_tool("list_connectors", arguments={})

            # Validate database content.
            db = DatabaseAdapter("crate://crate@localhost:4200/")
            db.run_sql("CREATE TABLE IF NOT EXISTS testdrive.mcp_dbhub (id INT, data TEXT)")
            db.run_sql("INSERT INTO testdrive.mcp_dbhub (id, data) VALUES (42, 'Hotzenplotz')")
            db.refresh_table("testdrive.mcp_dbhub")

            # Read available resources.
            await client.read_resource("db://schemas")

            # Invoke available prompts.
            await client.get_prompt("generate_sql", arguments={
                "description": "Please enumerate the highest five mountains.",
                "dialect": "postgres",
                "schema": "sys",
            })
            await client.get_prompt("explain_db", arguments={"schema": "testdrive"})
            await client.get_prompt("explain_db", arguments={"schema": "testdrive", "table": "mcp_dbhub"})


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
