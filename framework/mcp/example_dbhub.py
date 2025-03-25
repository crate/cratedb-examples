# DBHub Model Context Protocol Server for PostgreSQL
# https://github.com/bytebase/dbhub
#
# Derived from:
# https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#writing-mcp-clients
from cratedb_toolkit.util import DatabaseAdapter
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from mcp_utils import McpDatabaseConversation

# Create server parameters for stdio connection.
server_params_npx = StdioServerParameters(
    command="npx",
    args=[
        "-y",
        "@bytebase/dbhub@0.1",
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
            db.run_sql("CREATE TABLE IF NOT EXISTS public.testdrive (id INT, data TEXT)")
            db.run_sql("INSERT INTO public.testdrive (id, data) VALUES (42, 'Hotzenplotz')")
            db.refresh_table("public.testdrive")

            # Read a few resources.
            # FIXME: Only works on schema=public, because the PostgreSQL adapter hard-codes `WHERE table_schema = 'public'`.
            # https://github.com/bytebase/dbhub/blob/09424c8513c8c7bef7f66377b46a2b93a69a57d2/src/connectors/postgres/index.ts#L89-L107
            await client.read_resource("db://tables")

            # Get a few prompts.
            await client.get_prompt("generate_sql", arguments={"description": "Please enumerate the highest five mountains.", "dialect": "postgres"})
            await client.get_prompt("explain_db", arguments={"target": "testdrive"})


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
