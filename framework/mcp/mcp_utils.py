import io
import json
import mcp.types as types
from typing import Any

import pydantic_core
import yaml
from mcp import ClientSession, McpError
from pydantic import AnyUrl


class McpDatabaseConversation:
    """
    Wrap database conversations through MCP servers.
    """
    def __init__(self, session: ClientSession):
        self.session = session

    def decode_items(self, items):
        return list(map(self.decode_item, json.loads(pydantic_core.to_json(items))))

    @staticmethod
    def decode_item(item):
        try:
            item["text"] = json.loads(item["text"])
        except Exception:
            pass
        return item

    def list_items(self, items):
        buffer = io.StringIO()
        if items:
            data = self.decode_items(items)
            buffer.write("```yaml\n")
            buffer.write(yaml.dump(data, sort_keys=False, width=100))
            buffer.write("```\n")
        return buffer.getvalue()

    async def inquire(self):
        print("# MCP server inquiry")
        print()

        # List available prompts
        print("## Prompts")
        try:
            print(self.list_items((await self.session.list_prompts()).prompts))
        except McpError as e:
            print(f"Not implemented on this server: {e}")
        print()

        # List available resources
        print("## Resources")
        print(self.list_items((await self.session.list_resources()).resources))
        print()

        # List available tools
        print("## Tools")
        print(self.list_items((await self.session.list_tools()).tools))
        print()

    async def call_tool(
        self, name: str, arguments: dict[str, Any] | None = None
    ) -> types.CallToolResult:
        print(f"Calling tool: {name} with arguments: {arguments}")
        result = await self.session.call_tool(name, arguments)
        print(self.list_items(result.content))
        print()
        return result

    async def get_prompt(
        self, name: str, arguments: dict[str, str] | None = None
    ) -> types.GetPromptResult:
        print(f"Getting prompt: {name} with arguments: {arguments}")
        result = await self.session.get_prompt(name, arguments)
        print(self.list_items(result.messages))
        print()
        return result

    async def read_resource(self, uri: AnyUrl) -> types.ReadResourceResult:
        print(f"Reading resource: {uri}")
        result = await self.session.read_resource(uri)
        print(self.list_items(result.contents))
        print()
        return result
