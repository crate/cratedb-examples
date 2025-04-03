# Built-in Model Context Protocol Server for PostgreSQL
# https://www.npmjs.com/package/@modelcontextprotocol/server-postgres
#
# Derived from:
# https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#writing-mcp-clients
from cratedb_toolkit.util import DatabaseAdapter
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from mcp_utils import McpDatabaseConversation

# Create server parameters for stdio connection.
server_params = StdioServerParameters(
    command="npx",
    args=[
        "-y",
        "@modelcontextprotocol/server-postgres@0.6",
        "postgresql://crate@localhost:5432/doc",
    ],
    env=None,
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

            # Call a few tools.
            await client.call_tool("query", arguments={"sql": "SELECT * FROM sys.summits ORDER BY height DESC LIMIT 3"})

            # Validate database content.
            db = DatabaseAdapter("crate://crate@localhost:4200/")
            db.run_sql("CREATE TABLE IF NOT EXISTS public.mcp_builtin (id INT, data TEXT)")
            db.run_sql("INSERT INTO public.mcp_builtin (id, data) VALUES (42, 'Hotzenplotz')")
            db.refresh_table("public.mcp_builtin")

            # Read a few resources.
            await client.read_resource("postgres://crate@localhost:5432/mcp_builtin/schema")


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
