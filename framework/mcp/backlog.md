# MCP CrateDB backlog

## Iteration +1
- Builtin: Submit a CrateDB adapter, getting rid of the
  `Could not roll back transaction: error`
- JDBC: Tool `list_tables` currently blocks.
- JDBC: Tool `describe_table` does not work.
  Problem with `SELECT current_database()`.
  https://github.com/crate/crate/issues/17393
- DBHub: Reading resource `tables` does not work,
  because `WHERE table_schema = 'public'`
- PG-MCP: Improve installation after packaging has been improved.
  https://github.com/stuzero/pg-mcp-server/issues/10
- PG-MCP: Resource `pgmcp://{conn_id}/` makes `asyncpg` invoke
  `WITH RECURSIVE typeinfo_tree`, which fails on CrateDB.
  - https://github.com/crate/crate/issues/11757
  - https://github.com/crate/crate/issues/12544
- PG-MCP: Fix `/rowcount endpoint`
  https://github.com/stuzero/pg-mcp-server/issues/10

## Iteration +2
- General: Evaluate all connectors per `stdio` and `sse`, where possible
- General: Improve test cases to not just look at stdout/stderr streams,
  do regular method-based testing instead

## Iteration +3
- Provide a premium connector, like available for other databases.
  Examples:
  - Tinybird MCP server
    https://github.com/tinybirdco/mcp-tinybird
  - MongoDB Lens
    https://github.com/modelcontextprotocol/servers/pull/892
    https://github.com/furey/mongodb-lens
- Provide database specifics per "resources", like [SQLite Explorer] and
  DBHub are doing it.

## Done
- DBHub: https://github.com/bytebase/dbhub/issues/5
  Resolved: https://github.com/bytebase/dbhub/pull/6
- General: Evaluate available prompts, there are no test cases yet


[SQLite Explorer]: https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#sqlite-explorer
