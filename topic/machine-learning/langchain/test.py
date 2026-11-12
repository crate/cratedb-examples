import time
from pathlib import Path

import pytest

from cratedb_toolkit.util.database import DatabaseAdapter
from langchain_core.embeddings import DeterministicFakeEmbedding
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from nbclient.exceptions import CellExecutionError
from pueblo.testing.folder import str_list, list_python_files
from pueblo.testing.notebook import generate_tests
from pueblo.testing.snippet import pytest_module_function
from testbook import testbook

HERE = Path(__file__).parent

SQL_AVERAGE = "SELECT AVG(value) FROM time_series_data WHERE sensor_id = 1"

# Examples with a dedicated test, because they need a scripted model.
MODEL_EXAMPLES = ("agent_with_mcp.py", "vector_search.py")


class ScriptedToolModel(BaseChatModel):
    """
    Chat model that calls the SQL tool of the MCP server once, then repeats what the tool returned.
    """

    @property
    def _llm_type(self) -> str:
        return "scripted-tool-model"

    def bind_tools(self, tools, **kwargs):
        return self

    def _generate(self, messages, stop=None, run_manager=None, **kwargs) -> ChatResult:
        results = [m.content for m in messages if isinstance(m, ToolMessage)]
        if results:
            message = AIMessage(content=f"Tool result: {results[-1]}")
        else:
            call = {"name": "query_sql", "args": {"query": SQL_AVERAGE}, "id": "call-1"}
            message = AIMessage(content="", tool_calls=[call])
        return ChatResult(generations=[ChatGeneration(message=message)])


@pytest.fixture()
def cratedb() -> DatabaseAdapter:
    return DatabaseAdapter(dburi="crate://crate@localhost:4200")


@pytest.fixture(scope="function", autouse=True)
def reset_database(cratedb):
    """
    Initialize database.
    """
    cratedb.run_sql("DROP TABLE IF EXISTS mlb_teams_2012;")
    cratedb.run_sql("DROP TABLE IF EXISTS text_data;")
    time.sleep(0.01)


@pytest.fixture(scope="function", autouse=True)
def init_database(cratedb):
    """
    Initialize database.
    """
    cratedb.run_sql((HERE / "init.sql").read_text())


def pytest_generate_tests(metafunc):
    """
    Generate pytest test case per Jupyter Notebook.
    """
    here = Path(__file__).parent
    generate_tests(metafunc, path=here)


def test_notebook(notebook):
    """
    Execute Jupyter Notebook, one test case per .ipynb file.
    """
    # Skip Vertex AI examples, because authenticating is more complicated.
    if "vertexai" in notebook.name:
        raise pytest.skip(f"Skipping Vertex AI due to lack of authentication: {notebook.name}")

    with testbook(notebook) as tb:
        try:
            tb.execute()

        # Skip notebook if `pytest.exit()` is invoked, usually by
        # `getenvpass()`, when authentication token is not given.
        except CellExecutionError as ex:
            msg = str(ex)
            if "[skip-notebook]" in msg:
                raise pytest.skip(msg)
            raise


@pytest.mark.parametrize(
    "pyfile", [f for f in str_list(list_python_files(HERE)) if not f.endswith(MODEL_EXAMPLES)]
)
def test_file(request, cratedb, pyfile: Path):
    """
    From individual Python file, collect and wrap the `main` function into a test case.
    """
    pytest_module_function(request, pyfile)


def test_agent_with_mcp(cratedb, capsys, monkeypatch):
    """
    Execute `agent_with_mcp.py` with a scripted model, and verify the MCP tool result reaches the output.
    """
    monkeypatch.syspath_prepend(HERE)
    import agent_with_mcp

    create_react_agent = agent_with_mcp.create_react_agent
    monkeypatch.setattr(
        agent_with_mcp,
        "create_react_agent",
        lambda **kwargs: create_react_agent(**{**kwargs, "model": ScriptedToolModel()}),
    )

    agent_with_mcp.main()

    out = capsys.readouterr().out
    assert "17.03" in out


def test_vector_search(cratedb, capsys, monkeypatch):
    """
    Execute `vector_search.py` with fake embeddings, and verify the printed chunk comes from the vector store.
    """
    monkeypatch.syspath_prepend(HERE)
    import vector_search

    monkeypatch.setattr(vector_search, "OpenAIEmbeddings", lambda: DeterministicFakeEmbedding(size=8))

    vector_search.main()

    out = capsys.readouterr().out.strip()
    stored = [row["document"] for row in cratedb.run_sql(
        "SELECT document FROM langchain_embedding", records=True)]
    assert stored
    assert out in [document.strip() for document in stored]
