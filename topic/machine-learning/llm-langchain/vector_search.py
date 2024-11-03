"""
Use CrateDB Vector Search with OpenAI embeddings.

As input data, the example uses the canonical `state_of_the_union.txt`.

Synopsis::

    # Install prerequisites.
    pip install -U -r requirements.txt

    # Start database.
    docker run --rm -it --publish=4200:4200 crate/crate:nightly

    # Configure: Set environment variables.
    # Correct OpenAI API key should be used. SQL connection string fits a local instance of CrateDB.
    export OPENAI_API_KEY="<API KEY>"
    export CRATEDB_CONNECTION_STRING="crate://crate@localhost/?schema=doc"

    # Run program.
    python vector_search.py
"""  # noqa: E501

from langchain_community.vectorstores import CrateDBVectorSearch
from langchain_openai import OpenAIEmbeddings

import nltk
from pueblo.nlp.resource import CachedWebResource


def main():

    nltk.download("averaged_perceptron_tagger_eng")
    nltk.download("punkt_tab")

    # Load a document, and split it into chunks.
    url = "https://github.com/langchain-ai/langchain/raw/v0.0.325/docs/docs/modules/state_of_the_union.txt"
    documents = CachedWebResource(url).langchain_documents(chunk_size=1000, chunk_overlap=0)

    # Embed each chunk, and load them into the vector store.
    db = CrateDBVectorSearch.from_documents(documents, OpenAIEmbeddings())

    # Invoke a query, and display the first result.
    query = "What did the president say about Ketanji Brown Jackson"
    docs = db.similarity_search(query)
    print(docs[0].page_content)


if __name__ == "__main__":
    main()
