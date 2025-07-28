"""
Use an LLM to query a database in human language via NLSQLTableQueryEngine.
Example code using LlamaIndex with vanilla Open AI and Azure Open AI.
"""

import os
import sqlalchemy as sa

from dotenv import load_dotenv
from llama_index.core.utilities.sql_wrapper import SQLDatabase
from llama_index.core.query_engine import NLSQLTableQueryEngine

from boot import configure_llm


def main():
    """
    Use an LLM to query a database in human language.
    """

    # Configure application.
    load_dotenv()
    llm, embed_model = configure_llm()

    # Configure database connection and query engine.
    print("Connecting to CrateDB")
    engine_crate = sa.create_engine(os.getenv("CRATEDB_SQLALCHEMY_URL"))
    engine_crate.connect()

    print("Creating LlamaIndex QueryEngine")
    sql_database = SQLDatabase(engine_crate, include_tables=[os.getenv("CRATEDB_TABLE_NAME")])
    query_engine = NLSQLTableQueryEngine(
        sql_database=sql_database,
        # tables=[os.getenv("CRATEDB_TABLE_NAME")],
        llm=llm,
        embed_model=embed_model,
    )

    # Invoke an inquiry.
    print("Running query")
    QUERY_STR = os.getenv("DEMO_QUERY", "What is the average value for sensor 1?")
    answer = query_engine.query(QUERY_STR)
    print(answer.get_formatted_sources())
    print("Query was:", QUERY_STR)
    print("Answer was:", answer)
    print(answer.metadata)


if __name__ == "__main__":
    main()
