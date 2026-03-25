# DBHub Model Context Protocol Server for PostgreSQL
# https://github.com/bytebase/dbhub
#
# Derived from:
# https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#writing-mcp-clients
from cratedb_toolkit.util.database import DatabaseAdapter
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pueblo.mcp.client import McpConversation


# Create server parameters for stdio connection.
server_params_npx = StdioServerParameters(
    command="npx",
    args=[
        "-y",
        "@bytebase/dbhub@0.19.1",
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

            client = McpConversation(session)
            await client.inquire()

            print("## MCP server conversations")
            print()

            # Call a few tools.
            await client.call_tool("execute_sql", arguments={"sql": "SELECT * FROM sys.summits ORDER BY height DESC LIMIT 3"})
            await client.call_tool("search_objects", arguments={"object_type": "table", "schema": "sys", "detail_level": "names"})

            # Populate database.
            db = DatabaseAdapter("crate://crate@localhost:4200/")
            db.run_sql("CREATE TABLE IF NOT EXISTS testdrive.mcp_dbhub (id INT, data TEXT)")
            db.run_sql("INSERT INTO testdrive.mcp_dbhub (id, data) VALUES (42, 'Hotzenplotz')")
            db.refresh_table("testdrive.mcp_dbhub")

            # Inquire database.
            await client.call_tool("search_objects", arguments={"object_type": "table", "schema": "testdrive", "detail_level": "full"})


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
