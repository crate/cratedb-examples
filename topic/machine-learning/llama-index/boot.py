import os
from typing import Tuple

import openai
from langchain_openai import AzureOpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.llms import LLM
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.langchain import LangchainEmbedding


MODEL_NAME = "gpt-4o"


def configure_llm() -> Tuple[LLM, BaseEmbedding]:
    """
    Configure LLM. Use either vanilla Open AI, or Azure Open AI.
    """

    openai.api_type = os.getenv("OPENAI_API_TYPE")
    openai.azure_endpoint = os.getenv("OPENAI_AZURE_ENDPOINT")
    openai.api_version = os.getenv("OPENAI_AZURE_API_VERSION")
    openai.api_key = os.getenv("OPENAI_API_KEY")

    if openai.api_type == "openai":
        llm = OpenAI(
            model=MODEL_NAME,
            temperature=0.0,
            api_key=os.getenv("OPENAI_API_KEY"),
        )
    elif openai.api_type == "azure":
        llm = AzureOpenAI(
            model=MODEL_NAME,
            temperature=0.0,
            engine=os.getenv("LLM_INSTANCE"),
            azure_endpoint=os.getenv("OPENAI_AZURE_ENDPOINT"),
            api_key = os.getenv("OPENAI_API_KEY"),
            api_version = os.getenv("OPENAI_AZURE_API_VERSION"),
        )
    else:
        raise ValueError(f"Open AI API type not defined or invalid: {openai.api_type}")

    if openai.api_type == "openai":
        embed_model = LangchainEmbedding(OpenAIEmbeddings(model=MODEL_NAME))
    elif openai.api_type == "azure":
        embed_model = LangchainEmbedding(
            AzureOpenAIEmbeddings(
                azure_endpoint=os.getenv("OPENAI_AZURE_ENDPOINT"),
                model=os.getenv("EMBEDDING_MODEL_INSTANCE")
            )
        )
    else:
        embed_model = None

    return llm, embed_model
