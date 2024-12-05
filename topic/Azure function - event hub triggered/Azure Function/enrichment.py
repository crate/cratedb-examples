import uuid
import logging
import copy
from schemas import (
    READING
)

# TARGET_MAP maps the schema and the type to a target
TARGET_MAP = {
    "light_sensor": {
        "schema": READING,
        "type": "light_sensor",
    },
}

def start_enrichment(raw_payload, value_cache):
    """
    This function takes the current batch of events from eventhub
    and starts the enrichment. The result is saved in the value_cache variable.

    Args:
        raw_event: event from an Event Hub
        value_cache: ValueCache object to transfer values to the database writer
    """
    if raw_payload is None:
        return

    if isinstance(raw_payload, list):
        events = raw_payload
    else:
        events = [raw_payload]

    for event in events:
        target = str(event.get("type", "")).lower()

        trace_id = str(uuid.uuid4())

        #if target == "light_sensor":
        enricher = BaseEnrichment(event, target)

        try:
            enricher.transform()
        except (ValueError, KeyError) as e:
            logging.info(
                f"enrichment error: {e} -- target: {target} -- "
                f"enricher: {type(enricher).__name__} -- payload: {enricher.payload}"
            )
            enricher.error["message"] = str(e)
            value_cache.add_error(enricher.payload, enricher.error, trace_id)

        if not enricher.has_error:
            value_cache.add_reading(
                enricher.enriched_payload,
                trace_id,
                enricher.timestamp
            )
        value_cache.add_raw(enricher.payload, trace_id)


class BaseEnrichment:
    """
    The BaseEnrichment class implements the basic enrichment logic. There are three steps performed:

    Remove empty keys:
        payload is searched for empty keys
    Match schema:
        the top level keys of the payload are matched against the schema, if a key is not
        present in the schema it is removed.
    Get timestamp:
        timestamp is read from payload.reading_ts
    """

    def __init__(self, payload, target):
        self.payload = payload
        self.enriched_payload = {}
        self.timestamp = 0
        self.target = target
        self.has_error = False
        self.error = {"type": "", "message": ""}

    def transform(self):
        self._remove_empty_keys()
        self._match_schema()
        self._get_timestamp()

    def _remove_empty_keys(self):
        if "" in self.payload:
            value = self.payload.pop("")
            self.has_error = True
            self.error["type"] = "Enrichment Error"
            raise ValueError(f"raw message included empty key with value: {value}")

    def _match_schema(self):
        if self.target not in TARGET_MAP or self.has_error:
            return
        schema = TARGET_MAP[self.target]["schema"]
        for key, value in self.payload.items():
            if key in schema:
                self.enriched_payload[key] = copy.deepcopy(value)

    def _get_timestamp(self):
        if self.target not in TARGET_MAP:
            return
        if "reading_ts" in self.payload:
            self.timestamp = self.payload["reading_ts"]
        else:
            self.has_error = True
            self.error["type"] = "Enrichment Error"
            raise KeyError("'reading_ts' property missing in payload")