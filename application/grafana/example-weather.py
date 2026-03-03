"""
Example program demonstrating how to work with CrateDB and Grafana using
[grafana-client] and [grafanalib].

[grafana-client]: https://github.com/grafana-toolbox/grafana-client
[grafanalib]: https://github.com/weaveworks/grafanalib
"""
import dataclasses
import json
import logging

from cratedb_toolkit.datasets import load_dataset
from grafana_client import GrafanaApi
from grafana_client.client import GrafanaClientError
from grafana_client.model import DatasourceIdentifier
from grafana_client.util import setup_logging
from grafanalib._gen import DashboardEncoder
from grafanalib.core import (SHORT_FORMAT, Dashboard, Graph, GridPos,
                             SqlTarget, Time, YAxes, YAxis)
from yarl import URL

logger = logging.getLogger(__name__)


DATASOURCE_UID = "cratedb-v2KYBt37k"
DASHBOARD_UID = "cratedb-weather-demo"
CRATEDB_SQLALCHEMY_URL = "crate://crate:crate@cratedb:4200/"
CRATEDB_GRAFANA_URL = "cratedb:5432"
GRAFANA_URL = "http://grafana:3000"


@dataclasses.dataclass
class PanelInfo:
    """
    Minimal information defining a minimal graph panel.
    """
    title: str
    field: str
    unit: str


def provision(grafana: GrafanaApi):
    """
    Provision CrateDB and Grafana.

    - Load example weather data into CrateDB.
    - Provision Grafana with data source and dashboard.
    """

    logger.info("Loading data into CrateDB")

    # Load example data into CrateDB.
    dataset = load_dataset("tutorial/weather-basic")
    dataset.dbtable(dburi=CRATEDB_SQLALCHEMY_URL, table="example.weather_data").load()

    logger.info("Provisioning Grafana data source and dashboard")

    # Create Grafana data source.
    try:
        grafana.datasource.get_datasource_by_uid(DATASOURCE_UID)
        grafana.datasource.delete_datasource_by_uid(DATASOURCE_UID)
    except GrafanaClientError as ex:
        if ex.status_code != 404:
            raise
    grafana.datasource.create_datasource(
        {
            "uid": DATASOURCE_UID,
            "name": "CrateDB",
            "type": "postgres",
            "access": "proxy",
            "url": CRATEDB_GRAFANA_URL,
            "jsonData": {
                "database": "doc",
                "postgresVersion": 1200,
                "sslmode": "disable",
            },
            "user": "crate",
            "secureJsonData": {
                "password": "crate",
            },
        }
    )

    # Create Grafana dashboard.
    dashboard = Dashboard(
        uid=DASHBOARD_UID,
        title="CrateDB example weather dashboard",
        time=Time('2023-01-01T00:00:00Z', '2023-09-01T00:00:00Z'),
        refresh=None,
    )
    panel_infos = [
        PanelInfo(title="Weather » Temperature", field="temperature", unit="celsius"),
        PanelInfo(title="Weather » Humidity", field="humidity", unit="humidity"),
        PanelInfo(title="Weather » Wind speed", field="wind_speed", unit="velocitykmh"),
    ]
    for panel_info in panel_infos:
        column_name = panel_info.field
        unit = panel_info.unit
        dashboard.panels.append(
            Graph(
                title=f"{panel_info.title}",
                dataSource=DATASOURCE_UID,
                targets=[
                    SqlTarget(
                        rawSql=f"""
                        SELECT
                            $__timeGroupAlias("timestamp", $__interval),
                            "location",
                            MEAN("{column_name}") AS "{column_name}"
                        FROM "example"."weather_data"
                        WHERE $__timeFilter("timestamp")
                        GROUP BY "time", "location"
                        ORDER BY "time"
                        """,
                        refId="A",
                    ),
                ],
                yAxes=YAxes(
                    YAxis(format=unit),
                    YAxis(format=SHORT_FORMAT),
                ),
                gridPos=GridPos(h=8, w=24, x=0, y=9),
            )
        )
    # Encode grafanalib `Dashboard` entity to dictionary.
    dashboard_payload = {
        "dashboard": json.loads(json.dumps(dashboard, sort_keys=True, cls=DashboardEncoder)),
        "overwrite": True,
        "message": "Updated by grafanalib",
    }
    response = grafana.dashboard.update_dashboard(dashboard_payload)

    # Display dashboard URL.
    dashboard_url = URL(f"{grafana.url}{response['url']}").with_user(None).with_password(None)
    logger.info(f"Dashboard URL: {dashboard_url}")


def validate_datasource(grafana: GrafanaApi):
    """
    Validate Grafana data source.
    """
    logger.info("Validating data source")
    health = grafana.datasource.health_inquiry(DATASOURCE_UID)
    logger.info("Health status: %s", health.status)
    logger.info("Health message: %s", health.message)
    assert health.success is True, "Grafana data source is not healthy"


def validate_dashboard(grafana: GrafanaApi):
    """
    Validate Grafana dashboard by enumerating and executing all panel targets' `rawSql` expressions.
    """
    logger.info("Validating dashboard")
    dashboard = grafana.dashboard.get_dashboard(DASHBOARD_UID)
    for panel in dashboard["dashboard"].get("panels", []):
        for target in panel.get("targets", []):
            logger.info("Validating SQL target:\n%s", target["rawSql"])

            response = grafana.datasource.smartquery(DatasourceIdentifier(uid=DATASOURCE_UID), target["rawSql"])
            status = response["results"]["test"]["status"]
            queries = [frame["schema"]["meta"]["executedQueryString"] for frame in response["results"]["test"]["frames"]]
            logger.info("Status: %s", status)
            logger.info("Executed queries:\n%s", "\n".join(queries))

            assert status == 200, "Dashboard query status is not 200"


if __name__ == "__main__":
    """
    Boilerplate bootloader. Create a `GrafanaApi` instance and run example.
    """

    # Setup logging.
    setup_logging(level=logging.INFO)

    # Create a `GrafanaApi` instance.
    grafana_client = GrafanaApi.from_url(GRAFANA_URL)

    # Invoke example conversation.
    provision(grafana_client)

    # Validate Grafana data source and dashboard.
    validate_datasource(grafana_client)
    validate_dashboard(grafana_client)
