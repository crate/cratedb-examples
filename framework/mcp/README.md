# Verify MCP with CrateDB

## About

This folder includes Python programs that use the [Model Context Protocol
Python SDK], implementing MCP clients that hold conversations with MCP servers
wrapping database access.

In this case, the focus is on [CrateDB], by using relevant PostgreSQL adapter
implementations provided by the MCP ecosystem, because CrateDB is compatible
with PostgreSQL.

[MCP], the Model Context Protocol, is an open protocol that enables seamless
integration between LLM applications and external data sources and tools.

MCP clients call servers by either invoking them as a subprocess and
communicate with stdio, or by using SSE, which implements TCP socket
communication.

## What's Inside

The Python programs have been derived from the [Writing MCP Clients] example
program.

- `example_builtin.py`: Exercise the basic built-in Model Context Protocol server
  [@modelcontextprotocol/server-postgres] that provides read-only access to
  PostgreSQL databases per `query` tool. This server enables LLMs to inspect
  database schemas and execute read-only queries. It is written in TypeScript,
  to be invoked with [npx].

- `example_dbhub.py`: Exercise communication using [DBHub], a universal database
  gateway implementing the Model Context Protocol (MCP) server interface. This
  gateway allows MCP-compatible clients to connect to and explore different databases.

- `example_jdbc.py`: Exercise JDBC communication using the [Model Context Protocol
  Server for JDBC] from the [quarkus-mcp-servers] package, providing a range
  of tools. It is written in Java, to be invoked with [JBang].

- `example_mcp_alchemy.py`: Exercise communication using the [MCP Alchemy] MCP
  server package, providing a range of tools. It is written in Python, and uses
  [SQLAlchemy] and the [CrateDB SQLAlchemy dialect].

- `example_pg_mcp.py`:
  The [PG-MCP] server is specialised to talk to PostgreSQL servers. With a few adjustments,
  the adapter can also talk to CrateDB. The project offers rich MCP server capabilities,
  and includes advanced client programs for Claude and Gemini that work out of the box.
  It is written in Python, optionally to be invoked with `uv` or `uvx`.

- `example_cratedb_mcp.py`:
  The [CrateDB MCP Server] specialises on advanced CrateDB SQL operations by blending in
  knowledge base resources from CrateDB's documentation about query optimizations.
  It is written in Python, optionally to be invoked with `uv` or `uvx`.

## Resources

- Read a [brief introduction to MCP] by ByteByteGo.
- Read the canonical [Introduction to MCP].
- Read about the [MCP Python SDK].
- Read about configuring those servers with other MCP clients.
  - [Claude Desktop configuration]
  - [oterm configuration]
- [Connecting to an already running MCP server] seems to become possible
  with [MCP SSE]. As of 2025, not all servers implement that just yet.
- [Model Context Protocol (MCP) @ CrateDB]

## Setup

Start a CrateDB instance on your machine.
```shell
docker run -it --rm \
  --publish=4200:4200 --publish=5432:5432 \
  --env=CRATE_HEAP_SIZE=2g \
  crate:latest -Cdiscovery.type=single-node
```

Install the [uv] package manager and launcher.
```shell
{brew,pip} install uv
```

Install the [JBang] package manager and launcher.
```shell
{asdf,choco,dnf,brew,scoop,sdk} install jbang
```

## Install

Acquire sources, set up sandbox, and install packages.
```bash
git clone https://github.com/crate/cratedb-examples
cd cratedb-examples/framework/mcp
uv pip install -r requirements.txt -r requirements-test.txt
```

## Synopsis

```shell
uv run example_builtin.py
```
```shell
uv run example_dbhub.py
```
```shell
uv run example_jdbc.py
```

## Tests

Run integration tests.
```bash
uv run pytest
```

Run tests selectively.
```bash
uv run pytest -k dbhub
```

## Development

`ctk tail` is a handy command to follow the progress of CrateDB's `sys.jobs_log`,
which is applicable for all sorts of driver, adapter, and connector explorations.
After providing authentication information, just use uv's `uvx` launcher to invoke
CrateDB Toolkit's tail command without installation.
```shell
export CRATEDB_SQLALCHEMY_URL=crate://crate@localhost:4200/
```
```shell
uvx --from=cratedb-toolkit ctk tail -n 3 --follow --format=log-pretty sys.jobs_log
```

## Outlook

A future iteration may provide a premium MCP database adapter for CrateDB,
unlocking more details and features.


[brief introduction to MCP]: https://blog.bytebytego.com/i/159075598/what-is-mcp
[Claude Desktop configuration]: https://github.com/modelcontextprotocol/servers?tab=readme-ov-file#using-an-mcp-client
[connecting to an already running MCP server]: https://github.com/modelcontextprotocol/python-sdk/issues/145
[CrateDB]: https://cratedb.com/database
[CrateDB MCP Server]: https://github.com/crate/cratedb-mcp
[CrateDB SQLAlchemy dialect]: https://cratedb.com/docs/sqlalchemy-cratedb/
[DBHub]: https://github.com/bytebase/dbhub
[Introduction to MCP]: https://modelcontextprotocol.io/introduction
[JBang]: https://www.jbang.dev/
[MCP]: https://modelcontextprotocol.io/
[MCP Alchemy]: https://github.com/runekaagaard/mcp-alchemy
[MCP Python SDK]: https://github.com/modelcontextprotocol/python-sdk
[MCP SSE]: https://github.com/sidharthrajaram/mcp-sse
[Model Context Protocol (MCP) @ CrateDB]: https://github.com/crate/crate-clients-tools/discussions/234
[Model Context Protocol Python SDK]: https://pypi.org/project/mcp/
[Model Context Protocol Server for JDBC]: https://github.com/quarkiverse/quarkus-mcp-servers/tree/main/jdbc#readme
[@modelcontextprotocol/server-postgres]: https://www.npmjs.com/package/@modelcontextprotocol/server-postgres
[npx]: https://docs.npmjs.com/cli/v11/commands/npx
[oterm configuration]: https://ggozad.github.io/oterm/tools/mcp/
[PG-MCP]: https://github.com/stuzero/pg-mcp-server
[quarkus-mcp-servers]: https://github.com/quarkiverse/quarkus-mcp-servers
[SQLAlchemy]: https://sqlalchemy.org/
[uv]: https://docs.astral.sh/uv/
[Writing MCP Clients]: https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#writing-mcp-clients
