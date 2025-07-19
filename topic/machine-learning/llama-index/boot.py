import os

import openai
from langchain_openai import AzureOpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from llama_index.core import Settings
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.langchain import LangchainEmbedding


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
