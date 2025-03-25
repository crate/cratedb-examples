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
            db.run_sql("CREATE TABLE IF NOT EXISTS public.testdrive (id INT, data TEXT)")
            db.run_sql("INSERT INTO public.testdrive (id, data) VALUES (42, 'Hotzenplotz')")
            db.refresh_table("public.testdrive")

            # Read a few resources.
            # FIXME: Only works on schema=public, because the PostgreSQL adapter hard-codes `WHERE table_schema = 'public'`.
            # https://github.com/bytebase/dbhub/blob/09424c8513c8c7bef7f66377b46a2b93a69a57d2/src/connectors/postgres/index.ts#L89-L107
            await client.read_resource("postgres://crate@localhost:5432/testdrive/schema")


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
