
class ValueCache:
    """
    ValueCache class is used to structure enriched data for insert.
    """

    def __init__(self):
        self.errors = []
        self.errors_empty = []
        self.readings = []

    def add_error(self, payload, message, type):
        error_ = {
            "payload": payload,
            "error": {"message": message, "type": type},
            "type": type,
        }
        if payload is None or payload == {}:
            self.errors_empty.append(error_)
        else:
            self.errors.append(error_)

    def add_reading(self, payload, location, timestamp, sensor_id):
        self.readings.append(
            {
                "location" : location,
                "sensor_id" : sensor_id,
                "reading_ts" : timestamp,
                "reading": payload
            }
        )