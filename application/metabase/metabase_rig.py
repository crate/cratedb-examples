import time
from functools import lru_cache

import requests
from metabase_api import Metabase_API


class MetabaseRig:
    """
    Support end-to-end testing of CrateDB and Metabase.

    https://www.metabase.com/docs/latest/api-documentation

    Authenticate your requests with a session token
    https://www.metabase.com/learn/metabase-basics/administration/administration-and-operation/metabase-api#authenticate-your-requests-with-a-session-token
    """
    def __init__(self, url: str):
        self.username = "foobar@example.org"
        self.password = "123456metabase"
        self.mb = None

        self.url = url
        self.api_url = f"{url.rstrip('/')}/api"
        self.session = requests.Session()
        self.session_token = None

    def get_setup_token(self) -> str:
        response = self.session.get(f"{self.api_url}/session/properties")
        return response.json()["setup-token"]

    def setup(self):
        """
        Run Metabase setup, create admin user, and return a session ID.

        https://www.metabase.com/docs/latest/api/setup#post-apisetup
        https://discourse.metabase.com/t/rest-api-for-initial-setup-process/3419
        """
        response = self.session.post(f"{self.api_url}/setup", json={
            "prefs": {
                "allow_tracking": "false",
                "site_locale": "en",
                "site_name": "Hotzenplotz",
            },
            "user": {
                "password": self.password,
                "password_confirm": self.password,
                "email": self.username,
            },
            "token": self.get_setup_token(),
        })
        self.session_token = response.json()["id"]

    def login(self):
        self.session.post(f"{self.api_url}/session", json={
            "username": self.username,
            "password": self.password,
        })
        self.mb = Metabase_API(self.url, self.username, self.password)

    def get_databases(self):
        return self.session.get(f"{self.api_url}/database").json()

    def database(self, name: str) -> "MetabaseDatabase":
        return MetabaseDatabase(rig=self, name=name)


class MetabaseDatabase:
    def __init__(self, rig: MetabaseRig, name: str):
        self.rig = rig
        self.name = name
        self.timeout = 15

    @property
    @lru_cache(maxsize=None)
    def id(self):
        return self.rig.mb.get_item_id("database", self.name)

    def create(self):
        """
        https://www.metabase.com/docs/latest/api/database#post-apidatabase
        """
        self.rig.session.post(
            f"{self.rig.api_url}/database",
            json={
                "engine": "postgres",
                "name": self.name,
                "details": {
                    "host": "cratedb",
                    "port": 5432,
                    "user": "crate",
                },
            },
        )

    def exists(self):
        try:
            response = self.rig.session.get(f"{self.rig.api_url}/database/{self.id}")
            return response.status_code == 200
        except ValueError as ex:
            if "There is no DB with the name" not in str(ex):
                raise
        return False

    def schema(self, name: str):
        response = self.rig.session.get(f"{self.rig.api_url}/database/{self.id}/schema/{name}")
        response.raise_for_status()
        return response.json()

    def table_names(self, schema_name: str):
        names = []
        for item in self.schema(name=schema_name):
            names.append(f"{item['schema']}.{item['name']}")
        return names

    def table_id_by_name(self, name: str):
        return self.rig.mb.get_item_id("table", name)

    def query(self, table: str):
        response = self.rig.session.post(
            f"{self.rig.api_url}/dataset",
            json={
                "database": self.id,
                "query": {
                    "source-table": self.table_id_by_name(table),
                },
                "type": "query",
                "parameters": [],
            }
        )
        return response.json()

    def wait_database(self):
        def condition():
            return self.exists()
        return self._wait(condition, f"Database not found: {self.name}")

    def wait_schema(self, name: str):
        def condition():
            try:
                if schema := self.schema(name):
                    return schema
            except requests.RequestException:
                pass
            return False
        return self._wait(condition, f"Database schema '{name}' not found in database '{self.name}'")

    def wait_table(self, schema: str, name: str):
        def condition():
            if schema_info := self.wait_schema(schema):
                for item in schema_info:
                    if item["name"] == name and item["initial_sync_status"] == "complete":
                        return True
        return self._wait(condition, f"Table not found: {schema}.{name}")

    def _wait(self, condition, timeout_message):
        timeout = self.timeout
        while True:
            if result := condition():
                return result
            if timeout == 0:
                raise TimeoutError(timeout_message)
            timeout -= 1
            time.sleep(1)
