class ValueCache:
    """
    ValueCache class is used to structure enriched data for insert.
    """

    def __init__(self):
        self.errors = []
        self.readings = []

    def add_error(self, payload, message, type):
        self.errors.append(
            {
                "payload": payload,
                "error": {"message": message, "type": type},
                "type": type,
            }
        )

    def add_reading(self, payload, location, timestamp, sensor_id):
        self.readings.append(
            {
                "location": location,
                "sensor_id": sensor_id,
                "reading_ts": timestamp,
                "reading": payload,
            }
        )
