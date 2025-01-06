import logging

KEY_MAPPING = TARGET_MAP = {
    "ts": "reading_ts",
    "time": "reading_ts",
    "current_ts": "reading_ts",
    "timestamp": "reading_ts",
    "id": "sensor_id",
    "loc": "location",
}


def transform(raw_payload, value_cache):
    """
    This function takes a single event and transform it, checking for errors.
    The result is saved in the value_cache variable.

    Args:
        raw_payload: event from an Event Hub
        value_cache: ValueCache object to transfer values to the database writer
    """
    if raw_payload is None:
        return

    try:
        event_t = transform_payload(raw_payload)
        location = event_t.get("location")
        sensor_id = event_t.get("sensor_id")
        timestamp = event_t.get("reading_ts")
        payload = {
            "temperature": event_t.get("temperature"),
            "humidity": event_t.get("humidity"),
            "light": event_t.get("light"),
        }

        value_cache.add_reading(payload, location, timestamp, sensor_id)

    except (ValueError, KeyError) as e:
        logging.info(f"enrichment error: {e}" f"-- payload: {raw_payload}")
        value_cache.add_error(raw_payload, str(e), type(e).__name__)


def transform_payload(event):
    # remove empty keys
    event = remove_empty_keys(event)
    # change column names
    event = rename_keys(event)
    # check for sensor_id, timestamp, location keys
    check_fields(event)
    return event


def remove_empty_keys(event):
    if "" in event:
        value = event.pop("")
    return event


def rename_keys(event):
    for key in list(event.keys()):
        if key in KEY_MAPPING.keys():
            event[KEY_MAPPING[key]] = event.pop(key)

    return event


def check_fields(event):
    if not event.keys() >= {"location", "sensor_id", "reading_ts"}:
        raise KeyError("missing key in payload")
