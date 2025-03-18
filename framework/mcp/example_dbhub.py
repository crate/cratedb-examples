# DBHub Model Context Protocol Server for PostgreSQL
# https://github.com/bytebase/dbhub
#
# Derived from:
# https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#writing-mcp-clients
import shlex

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pprint import pprint


# Create server parameters for stdio connection.
server_params_npx = StdioServerParameters(
    command="npx",
    args=[
        "-y",
        "@bytebase/dbhub",
        "--transport=stdio",
        #"--transport=sse",
        #"--port=8080",
        "--dsn=postgres://crate@localhost:5432/doc",
    ],
    env=None,
)

docker_command = """
docker run --rm --init \
   --name dbhub \
   --publish 8080:8080 \
   bytebase/dbhub:latest \
   --transport sse \
   --port 8080 \
   --dsn="postgres://crate@host.docker.internal:5432/doc?sslmode=disable"
"""
server_params_docker = StdioServerParameters(
    command="npx",
    args=shlex.split(docker_command),
    env=None,
)


async def run():
    async with stdio_client(server_params_npx) as (read, write):
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

            print("Calling tool: run_query")
            result = await session.call_tool("run_query", arguments={"query": "SELECT * FROM sys.summits ORDER BY height DESC LIMIT 3"})
            pprint(result)
            print()

            print("Calling tool: list_connectors")
            result = await session.call_tool("list_connectors", arguments={})
            pprint(result)
            print()

            # Read a resource
            # FIXME: Does not work, because the PostgreSQL adapters hard-codes `WHERE table_schema = 'public'`.
            # https://github.com/bytebase/dbhub/blob/09424c8513c8c7bef7f66377b46a2b93a69a57d2/src/connectors/postgres/index.ts#L89-L107
            """
            print("Reading resource: tables")
            content, mime_type = await session.read_resource("db://tables")
            print("MIME type:", mime_type)
            pprint(content)
            """


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
