
import os
import sys
import json
import logging

import azure.functions as func

from enrichment import start_enrichment
from crate_writer import CrateWriter
from value_cache import ValueCache


app = func.FunctionApp()

@app.event_hub_message_trigger(arg_name="event", event_hub_name="demo-event-ce",
                               connection="EVENT_HUB_CONNECTION_STRING") 
def enrich_events(event: func.EventHubEvent):
    crate_db = CrateWriter(
        {
            "raws": os.getenv("RAW_TABLE"),
            "readings": os.getenv("READING_TABLE"),
            "errors": os.getenv("ERROR_TABLE"),
        },
        os.getenv("HOST"),
        os.getenv("DB_USER", None),
        os.getenv("DB_PASSWORD", None),
    )

    try:
        if event is None:
            return 
        insert_value_cache = ValueCache()
        # enrich all elements in current batch
        raw_event = json.loads(event.get_body().decode("utf-8"))
        #enrich payload
        start_enrichment(raw_event, insert_value_cache)
        # insert raw, metric and error
        crate_db.insert_values(insert_value_cache)
    except Exception as e:
        # when any exception occurred, the function must exit unsuccessfully for events to be retried
        logging.error(f"error: {e}")
        sys.exit(1)