"""
Use an LLM to query a database in human language via MCP.
Example code using LlamaIndex with vanilla Open AI and Azure Open AI.

https://github.com/run-llama/llama_index/tree/main/llama-index-integrations/tools/llama-index-tools-mcp

## Start CrateDB MCP Server
```
export CRATEDB_CLUSTER_URL="http://localhost:4200/"
cratedb-mcp serve --transport=http
```

## Usage
```
source env.standalone
export OPENAI_API_KEY=sk-XJZ7pfog5Gp8Kus8D--invalid--0CJ5lyAKSefZLaV1Y9S1
python demo_mcp.py
```
"""
import asyncio
import os

from cratedb_about.prompt import GeneralInstructions

from dotenv import load_dotenv
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.llms import LLM
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec

from boot import configure_llm


class Agent:

    def __init__(self, llm: LLM):
        self.llm = llm

    async def get_tools(self):
        # Connect to the CrateDB MCP server using the `http` transport.
        mcp_url = os.getenv("CRATEDB_MCP_URL", "http://127.0.0.1:8000/mcp/")
        mcp_client = BasicMCPClient(mcp_url)
        mcp_tool_spec = McpToolSpec(
            client=mcp_client,
            # Optional: Filter the tools by name
            # allowed_tools=["tool1", "tool2"],
            # Optional: Include resources in the tool list
            # include_resources=True,
        )
        return await mcp_tool_spec.to_tool_list_async()

    async def get_agent(self):
        return FunctionAgent(
            name="DemoAgent",
            description="CrateDB text-to-SQL agent",
            llm=self.llm,
            tools=await self.get_tools(),
            system_prompt=GeneralInstructions().render(),
        )

    async def aquery(self, query):
        return await (await self.get_agent()).run(query)

    def query(self, query):
        print("Inquiring MCP server")
        return asyncio.run(self.aquery(query))


def main():
    """
    Use an LLM to query a database in human language.
    """

    # Configure application.
    load_dotenv()
    llm, embed_model = configure_llm()

    # Use an agent that uses the CrateDB MCP server.
    agent = Agent(llm)

    # Invoke an inquiry.
    print("Running query")
    QUERY_STR = os.getenv("DEMO_QUERY", "What is the average value for sensor 1?")
    answer = agent.query(QUERY_STR)
    print("Query was:", QUERY_STR)
    print("Answer was:", answer)


if __name__ == "__main__":
    main()
