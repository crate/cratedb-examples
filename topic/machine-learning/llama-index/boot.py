import os
from typing import Tuple

import openai
import llama_index.core
from langchain_openai import AzureOpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.llms import LLM
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.llms.ollama import Ollama
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.langchain import LangchainEmbedding


def configure_llm(debug: bool = False) -> Tuple[LLM, BaseEmbedding]:
    """
    Configure LLM. Use either vanilla Open AI, or Azure Open AI.
    """

    llm_backend = os.getenv("LLM_BACKEND")
    llm_model = os.getenv("LLM_MODEL")

    if not llm_backend:
        raise ValueError("LLM_BACKEND environment variable is required")
    if not llm_model:
        raise ValueError("LLM_MODEL environment variable is required")

    # https://docs.llamaindex.ai/en/stable/understanding/tracing_and_debugging/tracing_and_debugging/
    if debug:
        llama_index.core.set_global_handler("simple")

    if llm_backend == "openai":
        llm = OpenAI(
            model=llm_model,
            temperature=0.0,
            api_key=os.getenv("OPENAI_API_KEY"),
        )
    elif llm_backend == "azure":
        llm = AzureOpenAI(
            model=llm_model,
            temperature=0.0,
            engine=os.getenv("LLM_INSTANCE"),
            azure_endpoint=os.getenv("OPENAI_AZURE_ENDPOINT"),
            api_key = os.getenv("OPENAI_API_KEY"),
            api_version = os.getenv("OPENAI_AZURE_API_VERSION"),
        )
    elif llm_backend == "ollama":
        # https://docs.llamaindex.ai/en/stable/api_reference/llms/ollama/
        llm = Ollama(
            model=llm_model,
            temperature=0.0,
            request_timeout=120.0,
            keep_alive=-1,
        )
    else:
        raise ValueError(f"LLM backend not defined or invalid: {llm_backend}")

    if llm_backend == "openai":
        embed_model = LangchainEmbedding(OpenAIEmbeddings(model=llm_model))
    elif llm_backend == "azure":
        embed_model = LangchainEmbedding(
            AzureOpenAIEmbeddings(
                azure_endpoint=os.getenv("OPENAI_AZURE_ENDPOINT"),
                model=llm_model,
            )
        )
    else:
        embed_model = None

    return llm, embed_model
