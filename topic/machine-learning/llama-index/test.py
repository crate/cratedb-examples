from pathlib import Path

import pytest

from cratedb_toolkit.util.database import DatabaseAdapter
from dotenv import load_dotenv
from llama_index.core.base.llms.types import ChatMessage, MessageRole, ToolCallBlock
from llama_index.core.embeddings import MockEmbedding
from llama_index.core.llms import CompletionResponse, CustomLLM, LLMMetadata
from llama_index.core.llms.mock import MockFunctionCallingLLM

HERE = Path(__file__).parent

SQL_AVERAGE = "SELECT AVG(value) FROM time_series_data WHERE sensor_id = 1"


class ScriptedLLM(CustomLLM):
    """
    Language model that answers each completion with the next scripted reply.
    """

    replies: list

    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata()

    def complete(self, prompt, formatted=False, **kwargs) -> CompletionResponse:
        return CompletionResponse(text=self.replies.pop(0))

    def stream_complete(self, prompt, formatted=False, **kwargs):
        yield self.complete(prompt)


def scripted_tool_call(messages, **kwargs) -> ChatMessage:
    """
    Call the SQL tool of the MCP server once, then repeat what the tool returned.
    """
    results = [m.content for m in messages if m.role == MessageRole.TOOL]
    if results:
        return ChatMessage(role=MessageRole.ASSISTANT, content=f"Tool result: {results[-1]}")
    call = ToolCallBlock(tool_name="query_sql", tool_kwargs={"query": SQL_AVERAGE})
    return ChatMessage(role=MessageRole.ASSISTANT, blocks=[call])


@pytest.fixture()
def cratedb() -> DatabaseAdapter:
    return DatabaseAdapter(dburi="crate://crate@localhost:4200")


@pytest.fixture(scope="function", autouse=True)
def init_database(cratedb):
    """
    Initialize database.
    """
    cratedb.run_sql("DROP TABLE IF EXISTS time_series_data;")
    cratedb.run_sql((HERE / "init.sql").read_text())


def test_nlsql(cratedb, capsys, monkeypatch):
    """
    Execute `demo_nlsql.py` with a scripted model, and verify the database result reaches the output.
    """

    load_dotenv("env.standalone")

    import demo_nlsql

    llm = ScriptedLLM(replies=[f"SQLQuery: {SQL_AVERAGE}", "The average was computed."])
    monkeypatch.setattr(demo_nlsql, "configure_llm", lambda: (llm, MockEmbedding(embed_dim=8)))

    # Invoke the workload, in-process.
    demo_nlsql.main()

    # Verify the outcome.
    out = capsys.readouterr().out
    assert "17.03" in out


def test_mcp(cratedb, capsys, monkeypatch):
    """
    Execute `demo_mcp.py` with a scripted model, and verify the MCP tool result reaches the output.
    """

    load_dotenv("env.standalone")

    import demo_mcp

    llm = MockFunctionCallingLLM(response_generator=scripted_tool_call)
    monkeypatch.setattr(demo_mcp, "configure_llm", lambda: (llm, None))

    # Invoke the workload, in-process.
    demo_mcp.main()

    # Verify the outcome.
    out = capsys.readouterr().out
    assert "17.03" in out
