# MCP Alchemy Model Context Protocol Server for CrateDB
# https://github.com/runekaagaard/mcp-alchemy
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

    # Incantation assuming software is installed.
    server_params = StdioServerParameters(
        command=where.first("mcp-alchemy"),
        args=[],
        env={"DB_URL": "crate://crate@localhost:4200/?schema=testdrive"},
    )

    # Incantation using `uvx`.
    server_params_uvx = StdioServerParameters(
        command="uvx",
        args=["--with", "sqlalchemy-cratedb>=0.42.0.dev2", "mcp-alchemy"],
        env={"DB_URL": "crate://crate@localhost:4200/?schema=testdrive"},
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
            db.run_sql("CREATE TABLE IF NOT EXISTS mcp_alchemy (id INT, data TEXT)")
            db.run_sql("INSERT INTO mcp_alchemy (id, data) VALUES (42, 'Hotzenplotz')")
            db.refresh_table("mcp_alchemy")

            # Call a few tools.
            await client.call_tool("execute_query", arguments={"query": "SELECT * FROM sys.summits ORDER BY height DESC LIMIT 3"})
            await client.call_tool("all_table_names", arguments={})
            await client.call_tool("filter_table_names", arguments={"q": "mcp"})
            await client.call_tool("schema_definitions", arguments={"table_names": ["mcp_alchemy"]})


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
