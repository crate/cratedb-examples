# Built-in Model Context Protocol Server for PostgreSQL
# https://www.npmjs.com/package/@modelcontextprotocol/server-postgres
#
# Derived from:
# https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#writing-mcp-clients
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pprint import pprint


# Create server parameters for stdio connection.
server_params = StdioServerParameters(
    command="npx",
    args=[
        "-y",
        "@modelcontextprotocol/server-postgres",
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

            # List available prompts
            # TODO: Not available on this server.
            #print("Prompts:")
            #pprint(await session.list_prompts())
            #print()

            # List available resources
            print("Resources:")
            pprint(await session.list_resources())
            print()

            # List available tools
            print("Tools:")
            pprint(await session.list_tools())
            print()

            print("Calling tool: read_query")
            result = await session.call_tool("query", arguments={"sql": "SELECT * FROM sys.summits ORDER BY height DESC LIMIT 3"})
            pprint(result)
            print()



if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
