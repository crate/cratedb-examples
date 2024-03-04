"A very simple wrapper around the CrateDB Cloud API"

import logging
import time

import requests


class CrateDBCloudAPI:
    "A very partial implementation of some endpoints from the CrateDB Cloud API"

    BASE_ENDPOINT = "https://console.cratedb.cloud/api/v2"
    DELAY_SECONDS = 10

    def __init__(self, api_key, api_secret, organization_id, cluster_id):
        self.__auth = requests.auth.HTTPBasicAuth(api_key, api_secret)
        self.organization_id = organization_id
        self.cluster_id = cluster_id

    def get_metrics(self):
        "Returns Prometheus metrics for the given organization"
        return self.__get(f"organizations/{self.organization_id}/metrics/prometheus/")

    def get_cluster_status(self):
        "Returns the status for a given cluster"
        return self.__get(f"clusters/{self.cluster_id}/").json()

    def scale(self, target_nodes):
        "Sends a request to scale to the CrateDB Cloud API"
        requests.put(
            f"{self.BASE_ENDPOINT}/clusters/{self.cluster_id}/scale/",
            json={"product_unit": target_nodes},
            auth=self.__auth,
            timeout=60,
        )

    def wait_for_operation(self):
        "Sleeps until there is no running operation"
        # Initial wait to allow a just triggered operation to be reflected
        time.sleep(self.DELAY_SECONDS)
        cluster_status = self.get_cluster_status()

        while cluster_status["health"]["running_operation"] != "":
            logging.info("Scaling operation in progress.")
            # Wait to allow the operation to progress
            time.sleep(self.DELAY_SECONDS)
            cluster_status = self.get_cluster_status()

    def __get(self, endpoint):
        return requests.get(
            f"{self.BASE_ENDPOINT}/{endpoint}",
            auth=self.__auth,
            timeout=60,
        )
