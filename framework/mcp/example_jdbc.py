# Quarkus Model Context Protocol Server for JDBC
# https://github.com/quarkiverse/quarkus-mcp-servers/tree/main/jdbc#readme
#
# Derived from:
# https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#writing-mcp-clients
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from mcp_utils import McpDatabaseConversation

# Create server parameters for stdio connection.
server_params = StdioServerParameters(
    command="jbang",
    args=[
        # "--quiet",
        "run",
        "--java=21",
        "jdbc@quarkiverse/quarkus-mcp-servers",
        "jdbc:postgresql://localhost:5432/doc",
        "-u", "crate"],
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
            await client.call_tool("database_info")
            # FIXME: This operation currently blocks.
            # await client.call_tool("list_tables", arguments={})
            await client.call_tool("describe_table", arguments={"schema": "sys", "table": "summits"})
            await client.call_tool("read_query", arguments={"query": "SELECT * FROM sys.summits ORDER BY height DESC LIMIT 3"})
            await client.call_tool("create_table", arguments={"query": "CREATE TABLE IF NOT EXISTS testdrive.mcp_jdbc (id INT, data TEXT)"})
            await client.call_tool("write_query", arguments={"query": "INSERT INTO testdrive.mcp_jdbc (id, data) VALUES (42, 'foobar')"})

            # Get a few prompts.
            await client.get_prompt("er_diagram")
            await client.get_prompt("sample_data", arguments={"topic": "wind energy"})


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
