"""
Use an LLM to query a database in human language.
Example code using LlamaIndex with vanilla Open AI and Azure Open AI.
"""

import os
import openai
import sqlalchemy as sa

from dotenv import load_dotenv
from langchain_openai import AzureOpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.langchain import LangchainEmbedding
from llama_index.core.utilities.sql_wrapper import SQLDatabase
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.core import Settings


def configure_llm():
    """
    Configure LLM. Use either vanilla Open AI, or Azure Open AI.
    """

    openai.api_type = os.getenv("OPENAI_API_TYPE")
    openai.azure_endpoint = os.getenv("OPENAI_AZURE_ENDPOINT")
    openai.api_version = os.getenv("OPENAI_AZURE_API_VERSION")
    openai.api_key = os.getenv("OPENAI_API_KEY")

    if openai.api_type == "openai":
        llm = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.0
        )
    elif openai.api_type == "azure":
        llm = AzureOpenAI(
            engine=os.getenv("LLM_INSTANCE"),
            azure_endpoint=os.getenv("OPENAI_AZURE_ENDPOINT"),
            api_key = os.getenv("OPENAI_API_KEY"),
            api_version = os.getenv("OPENAI_AZURE_API_VERSION"),
            temperature=0.0
        )
    else:
        raise ValueError(f"Open AI API type not defined or invalid: {openai.api_type}")

    Settings.llm = llm
    if openai.api_type == "openai":
        Settings.embed_model = LangchainEmbedding(OpenAIEmbeddings())
    elif openai.api_type == "azure":
        Settings.embed_model = LangchainEmbedding(
            AzureOpenAIEmbeddings(
                azure_endpoint=os.getenv("OPENAI_AZURE_ENDPOINT"),
                model=os.getenv("EMBEDDING_MODEL_INSTANCE")
            )
        )


def main():
    """
    Use an LLM to query a database in human language.
    """

    # Configure application.
    load_dotenv()
    configure_llm()

    # Configure database connection and query engine.
    print("Connecting to CrateDB")
    engine_crate = sa.create_engine(os.getenv("CRATEDB_SQLALCHEMY_URL"))
    engine_crate.connect()

    print("Creating LlamaIndex QueryEngine")
    sql_database = SQLDatabase(engine_crate, include_tables=[os.getenv("CRATEDB_TABLE_NAME")])
    query_engine = NLSQLTableQueryEngine(
        sql_database=sql_database,
        tables=[os.getenv("CRATEDB_TABLE_NAME")],
        llm=Settings.llm
    )

    # Invoke an inquiry.
    print("Running query")
    QUERY_STR = "What is the average value for sensor 1?"
    answer = query_engine.query(QUERY_STR)
    print(answer.get_formatted_sources())
    print("Query was:", QUERY_STR)
    print("Answer was:", answer)
    print(answer.metadata)


if __name__ == "__main__":
    main()
