"""
Demonstrate conversational memory with CrateDB.

Synopsis::

    # Install prerequisites.
    pip install -U -r requirements.txt

    # Start database.
    docker run --rm -it --publish=4200:4200 crate/crate:nightly

    # Run program.
    export CRATEDB_CONNECTION_STRING="crate://crate@localhost/?schema=doc"
    python conversational_memory.py
"""
import os
from pprint import pprint

from langchain_cratedb.chat_history import CrateDBChatMessageHistory


CONNECTION_STRING = os.environ.get(
    "CRATEDB_CONNECTION_STRING",
    "crate://crate@localhost/?schema=doc"
)


def main():

    chat_history = CrateDBChatMessageHistory(
        session_id="test_session",
        connection=CONNECTION_STRING,
    )
    chat_history.add_user_message("Hello")
    chat_history.add_ai_message("Hi")
    pprint(chat_history.messages)


if __name__ == "__main__":
    main()
