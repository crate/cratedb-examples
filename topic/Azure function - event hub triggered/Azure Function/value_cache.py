import logging

class ValueCache:
    """
    ValueCache class is used to structure enriched data for insert.
    """

    def __init__(self):
        self.errors = []
        self.errors_empty = []
        self.readings = []
        self.raws = []

    def add_error(self, payload, error, trace_id):
        error_ = {
            "payload": payload,
            "trace_id": trace_id,
            "error": error,
            "type": error["type"],
        }
        if payload is None or payload == {}:
            self.errors_empty.append(error_)
        else:
            self.errors.append(error_)

    def add_reading(self, payload, trace_id, timestamp):
        self.readings.append(
            {
                "trace_id" : trace_id,
                "value" : payload["value"],
                "country" : payload["country"],
                "id" : payload["id"],
                "reading_ts" : payload["reading_ts"]
            }
        ) 

    def add_raw(self, payload, trace_id):
        raw = {"payload": payload, "trace_id": trace_id}
        self.raws.append(raw)

    def get_payload_from_raw(self, trace_id):
        for raw in self.raws:
            if raw["trace_id"] == trace_id:
                return raw["payload"]

        logging.info(
            f"Payload corresponding to trace_id {trace_id} not found: payload = NULL"
        )

    def remove_reading(self, trace_id):
        for reading in self.readings:
            if reading["trace_id"] == trace_id:
                self.readings.remove(reading)
                return

    def validate_errors_empty(self):
        for error_empty in self.errors_empty:
            for error in self.errors:
                trace_id = error["trace_id"]
                if error_empty["trace_id"] == trace_id:
                    self.errors_empty.remove(error_empty)
                    logging.info(
                        f"Removed duplicated trace_id errors with empty payload - {trace_id}"
                    )
                    break

        if len(self.errors_empty) > 0:
            self.errors.append(self.errors_empty)