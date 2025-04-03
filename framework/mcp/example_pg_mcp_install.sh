#!/bin/sh
# Acquire MCP server part of `pg-mcp`.
# https://github.com/stuzero/pg-mcp-server
# https://github.com/crate-workbench/pg-mcp-server

# FIXME: Improve installation after packaging has been improved.
#        https://github.com/stuzero/pg-mcp-server/issues/10

set -e
TARGET="/tmp/pg-mcp-server"
rm -rf ${TARGET}
git clone --depth 1 --no-checkout --filter=blob:none \
  https://github.com/crate-workbench/pg-mcp-server.git \
  ${TARGET}
cd ${TARGET}
git checkout 82733d1a886bf1a14592d1fbb305205901f2bb35 -- pyproject.toml uv.lock server test.py
cat pyproject.toml | grep -v requires-python | sponge pyproject.toml
uv pip install .

# /Users/amo/dev/crate-workbench/sources/pg-mcp-server
# https://github.com/crate-workbench/pg-mcp.git
