# Quarkus Model Context Protocol Server for JDBC
# https://github.com/quarkiverse/quarkus-mcp-servers/tree/main/jdbc#readme
#
# Derived from:
# https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#writing-mcp-clients
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pprint import pprint


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

            # List available prompts
            print("Prompts:")
            pprint(await session.list_prompts())
            print()

            # List available resources
            print("Resources:")
            pprint(await session.list_resources())
            print()

            # List available tools
            print("Tools:")
            pprint(await session.list_tools())
            print()

            # Call a tool
            print("Calling tool: database_info")
            result = await session.call_tool("database_info")
            pprint(result)
            print()

            # FIXME: This operation currently blocks.
            #print("Calling tool: list_tables")
            #result = await session.call_tool("list_tables")
            #pprint(result)
            #print()

            print("Calling tool: describe_table")
            result = await session.call_tool("describe_table", arguments={"schema": "sys", "table": "summits"})
            pprint(result)
            print()

            print("Calling tool: read_query")
            result = await session.call_tool("read_query", arguments={"query": "SELECT * FROM sys.summits ORDER BY height DESC LIMIT 3"})
            pprint(result)
            print()

            print("Calling tool: create_table")
            result = await session.call_tool("create_table", arguments={"query": "CREATE TABLE IF NOT EXISTS testdrive (id INT, data TEXT)"})
            pprint(result)
            print()

            print("Calling tool: write_query")
            result = await session.call_tool("write_query", arguments={"query": "INSERT INTO testdrive (id, data) VALUES (42, 'foobar')"})
            pprint(result)
            print()

            # Read a resource
            #content, mime_type = await session.read_resource("file://some/path")

            # Get a prompt
            #prompt = await session.get_prompt(
            #    "example-prompt", arguments={"arg1": "value"}
            #)



if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
