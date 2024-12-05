import time
import logging
from crate import client
from crate.client.exceptions import ProgrammingError, IntegrityError


class CrateWriter:
    """
    The CrateWriter class is used to insert enriched and raw data in to CrateDB
    """

    CONNECTION_POOL_SIZE = 10

    def __init__(self, tables, host, db_user, db_pass):
        self._conn = None
        self._cursor = None
        self._tables = tables
        self._host = host
        self._db_user = db_user
        self._db_pass = db_pass

    def insert_values(self, value_cache):
        self._failed = []
        self._connect()

        if len(value_cache.raws) > 0:
            self._insert_operation(
                value_cache.raws,
                self._tables["raws"],
            )

        if len(value_cache.readings) > 0:
            self._insert_operation(
                value_cache.readings,
                self._tables["readings"],
            )
            self._move_reading_to_error(value_cache)

        if len(value_cache.errors_empty) > 0:
            value_cache.validate_errors_empty()

        if len(value_cache.errors) > 0:
            self._insert_operation(
                value_cache.errors,
                self._tables["errors"],
            )

    @staticmethod
    def _insert_ts():
        return int(time.time() * 1000)

    def _connect(self):
        if self._cursor is None or (self._cursor and getattr(self._cursor, "_closed", True)) or \
       self._conn is None or (self._conn and getattr(self._conn, "_closed", True)):
            self._conn = client.connect(
                self._host,
                username=self._db_user,
                password=self._db_pass,
                pool_size=self.CONNECTION_POOL_SIZE,
            )
            self._cursor = self._conn.cursor()

    def _insert_operation(self, value_list, table_name):
        if self._cursor is  None:
            return
        stmt, parameters = self._prepare_insert_stmt(
            value_list, table_name, (0, len(value_list))
        )
        result = self._cursor.executemany(stmt, parameters)

        for i, row in enumerate(result):
            if row["rowcount"] == -2:
                stmt, parameters = self._prepare_insert_stmt(
                    value_list, table_name, (i, i + 1)
                )
                try:
                    self._cursor.executemany(stmt, parameters)
                # IntegrityError is raised in case of PK violation (e.g. duplicated PK)
                except (ProgrammingError, IntegrityError) as e:
                    self._add_item_to_failed(
                        e,
                        stmt,
                        parameters,
                        value_list[i]["trace_id"],
                        (
                            "Integrity Error"
                            if isinstance(e, IntegrityError)
                            else "Internal Error"
                        ),
                        table_name,
                    )

    def _add_item_to_failed(
        self, error, stmt, parameters, trace_id, error_type, table_name
    ):
        logging.warning(
            f"error: {error} -- stmt: {stmt} -- parameters: {parameters} -- trace_id: {trace_id}"
        )
        self._failed.append(
            {
                "type": table_name,
                "trace_id": trace_id,
                "error": error,
                "error_type": error_type,
            }
        )

    def _move_reading_to_error(self, value_cache):
        for element in self._failed:
            if element["type"] == self._tables["readings"]:
                try:
                    trace_id = element["trace_id"]
                    message = element["error"].message
                    payload = value_cache.get_payload_from_raw(trace_id)

                    value_cache.add_error(
                        payload,
                        {"type": element["error_type"], "message": message},
                        trace_id,
                    )
                    value_cache.remove_reading(trace_id)
                except IndexError:
                    logging.warning(
                        "Unable to move reading to error because it has already been moved (insert raw "
                        "failed)"
                    )

    def _prepare_insert_stmt(self, value_list, table_name, iteration_range):
        stmt = f"INSERT INTO {table_name} (insert_ts, "
        parameters = "?, "
        parameter_list = []
        keys = value_list[0].keys()

        for key in keys:
            stmt += f"{key}, "
            parameters += "?, "
        stmt = stmt.rstrip(", ")
        parameters = parameters.rstrip(", ")

        stmt += f") VALUES ({parameters})"

        for i in range(iteration_range[0], iteration_range[1]):
            parameter_entry = [self._insert_ts()]
            parameter_entry.extend(self._add_entries(value_list, keys, i))
            parameter_list.append(tuple(parameter_entry))

        return stmt, parameter_list

    @staticmethod
    def _add_entries(values, keys, index):
        entries = []
        for key in keys:
            entries.append(values[index][key])
        return entries