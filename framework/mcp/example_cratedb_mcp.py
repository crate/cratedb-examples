# CrateDB MCP Server
# https://github.com/crate/cratedb-mcp
#
# Derived from:
# https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#writing-mcp-clients
from cratedb_toolkit.util.database import DatabaseAdapter
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from mcp_utils import McpDatabaseConversation

# Create server parameters for stdio connection.
server_params = StdioServerParameters(
    command="cratedb-mcp",
    args=[],
    env={
        "CRATEDB_MCP_HTTP_URL": "http://localhost:4200",
        "CRATEDB_MCP_TRANSPORT": "stdio",
    },
)


async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
            read, write
        ) as session:
            # Initialize the connection
            await session.initialize()

            client = McpDatabaseConversation(session)
            await client.inquire()

            print("## MCP server conversations")
            print()

            # Provision database.
            db = DatabaseAdapter("crate://crate@localhost:4200/")
            db.run_sql("CREATE TABLE IF NOT EXISTS public.mcp_builtin (id INT, data TEXT)")
            db.run_sql("INSERT INTO public.mcp_builtin (id, data) VALUES (42, 'Hotzenplotz')")
            db.refresh_table("public.mcp_builtin")

            # Call a few tools.
            await client.call_tool("query_sql", arguments={"query": "SELECT * FROM sys.summits ORDER BY height DESC LIMIT 3"})
            await client.call_tool("get_table_metadata", arguments={})
            await client.call_tool("get_health", arguments={})


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
