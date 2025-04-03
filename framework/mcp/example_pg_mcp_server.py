if __name__ == "__main__":
    # FIXME: Improve invocation after packaging has been improved.
    #        https://github.com/stuzero/pg-mcp/issues/10
    from server.app import logger, mcp

    # TODO: Bring flexible invocation (sse vs. stdio) to mainline.
    logger.info("Starting MCP server with STDIO transport")
    mcp.run(transport="stdio")
