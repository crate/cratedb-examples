"""
Exercise LangChain/LangGraph with the CrateDB MCP server.

## Synopsis

# Install prerequisites.
pip install -U -r requirements.txt

# Start database.
docker run --rm -it --publish=4200:4200 crate/crate:nightly

# Provision database.
crash < init.sql

# Start MCP server.
export CRATEDB_MCP_TRANSPORT=streamable-http
export CRATEDB_MCP_HOST=0.0.0.0
export CRATEDB_MCP_PORT=8000
export CRATEDB_CLUSTER_URL=http://crate:crate@localhost:4200/
docker run --rm -it --network=host --publish=8000:8000 ghcr.io/crate/cratedb-mcp:pr-50

# Run program.
export OPENAI_API_KEY=<your_openai_api_key>
python agent_with_mcp.py
"""
import asyncio

from cratedb_about.instruction import GeneralInstructions
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent


async def amain():
    client = MultiServerMCPClient(
        {
            "cratedb": {
                "transport": "streamable_http",
                "url": "http://localhost:8000/mcp/"
            },
        }
    )
    tools = await client.get_tools()
    agent = create_react_agent(
        model="openai:gpt-4.1",
        tools=tools,
        prompt=GeneralInstructions().render(),
    )

    QUERY_STR = "What is the average value for sensor 1?"
    response = await agent.ainvoke({"messages": QUERY_STR})
    answer = response["messages"][-1].content

    print("Query was:", QUERY_STR)
    print("Answer was:", answer)


def main():
    asyncio.run(amain())


if __name__ == "__main__":
    main()
