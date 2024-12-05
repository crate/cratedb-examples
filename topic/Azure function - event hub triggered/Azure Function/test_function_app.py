
import os
import sys
import logging

from enrichment import start_enrichment
from crate_writer import CrateWriter
from value_cache import ValueCache


event = [{"country":"PT","type":"light_sensor","value":"1","id":"ABC001","reading_ts":"1732703748223"}]

crate_db = CrateWriter(
    {   
        "raws": os.getenv("RAW_TABLE", "enrichment.raw"),
        "readings": os.getenv("READING_TABLE","enrichment.ls_reading"),
        "errors": os.getenv("ERROR_TABLE", "enrichment.error"),
    },
    os.getenv("HOST", "localhost:4200"),
    os.getenv("DB_USER", "crate"),
    os.getenv("DB_PASSWORD", None),
)
try:
    insert_value_cache = ValueCache()
    # enrich all elements in current batch
    for event_ in event:
        raw_event = event_
        start_enrichment(raw_event, insert_value_cache)
    # insert raw, reading and error
    crate_db.insert_values(insert_value_cache)
except Exception as e:
    # when any exception occurred, the function must exit unsuccessfully for events to be retried
    logging.error(f"error: {e}")
    sys.exit(1)