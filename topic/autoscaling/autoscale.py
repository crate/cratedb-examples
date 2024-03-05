"""
An example of how to scale your CrateDB Cloud cluster automatically,
based on its Prometheus metrics endpoint.
"""

import argparse
import logging
import os
import time
from datetime import datetime
from functools import reduce

import requests
from prometheus_client.parser import text_string_to_metric_families
from requests.auth import HTTPBasicAuth

# Date format for parsing datetime strings
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

parser = argparse.ArgumentParser()
parser.add_argument(
    "-o",
    "--organization_id",
    help="The ID of your CrateDB Cloud organization",
    required=True,
)
parser.add_argument(
    "-c",
    "--cluster_id",
    help="The ID of your CrateDB Cloud cluster",
    required=True,
)
args = parser.parse_args()

auth_data = HTTPBasicAuth(
    os.getenv("CRATEDB_CLOUD_API_KEY"),
    os.getenv("CRATEDB_CLOUD_API_SECRET"),
)


def num_shards():
    "Calculate the average number of shards per node for a given cluster"
    api_url = f"https://console.cratedb.cloud/api/v2/organizations/{args.organization_id}/metrics/prometheus/"
    response = requests.get(api_url, auth=auth_data, timeout=60)

    samples = []
    for family in text_string_to_metric_families(response.text):
        for sample in family.samples:
            if (
                sample.name == "crate_node"
                and sample.labels["name"] == "shard_stats"
                and args.cluster_id in sample.labels["pod_name"]
                and sample.labels["property"] == "total"
            ):
                samples.append(sample.value)

    if len(samples) == 0:
        return None

    return reduce(lambda a, b: a + b, samples) / len(samples)


def get_cluster_status():
    """Function to get the current status of a cluster"""
    api_url = f"https://console.cratedb.cloud/api/v2/clusters/{args.cluster_id}/"
    return requests.get(api_url, auth=auth_data, timeout=60).json()


def get_cluster_running_op(cluster_status):
    """Function to get the current running operation in a cluster"""
    if (
        datetime.now()
        - datetime.strptime(cluster_status["health"]["last_seen"], DATE_FORMAT)
    ).seconds > 30:
        cluster_status = get_cluster_status()
    return cluster_status["health"]["running_operation"]


def get_cluster_num_nodes(cluster_status):
    """Function to get the current number of nodes minus one in a cluster"""
    if (
        datetime.now()
        - datetime.strptime(cluster_status["health"]["last_seen"], DATE_FORMAT)
    ).seconds > 30:
        cluster_status = get_cluster_status()
    return cluster_status["num_nodes"] - 1


def scale_cluster(num, cluster_status, max_num_shard):
    """Function to scale out of back when reaching the treshold(s)"""
    operation_in_progress_msg = "Scaling operation in progress."
    if num > (0.8 * max_num_shard):
        num_nodes = get_cluster_num_nodes(cluster_status)
        logging.info(f"Start scaling out from {num_nodes + 1} to {num_nodes + 2}")
        requests.put(
            f"https://console.cratedb.cloud/api/v2/clusters/{args.cluster_id}/scale/",
            json={"product_unit": num_nodes + 1},
            auth=auth_data,
            timeout=60,
        )
        logging.info(operation_in_progress_msg)
        while get_cluster_running_op(cluster_status) != "":
            time.sleep(10)  # Check every 10 seconds instead of immediately looping back
            # Optionally, log at intervals rather than trying to print dots
            logging.info(operation_in_progress_msg)
        logging.info("Scaled up successfully!")
    elif num < (0.5 * max_num_shard):
        num_nodes = get_cluster_num_nodes(cluster_status)
        logging.info(f"Start scaling down from {num_nodes + 1} to {num_nodes}")
        requests.put(
            f"https://console.cratedb.cloud/api/v2/clusters/{args.cluster_id}/scale/",
            json={"product_unit": num_nodes - 1},
            auth=auth_data,
            timeout=60,
        )
        logging.info(operation_in_progress_msg)
        while get_cluster_running_op(cluster_status) != "":
            time.sleep(10)  # Check every 10 seconds
            # Optionally, log at intervals rather than trying to print dots
            logging.info(operation_in_progress_msg)
        logging.info("Scaled down successfully!")
    else:
        logging.info("Nothing to do!")


DELAY_SECONDS = 5
MAX_NUM_SHARDS = 30

# Main loop to monitor and adjust cluster size based on shard count
while True:
    try:
        status = get_cluster_status()  # Fetch current cluster status
        number_shards = num_shards()  # Calculate average shard count
        if number_shards is not None:
            logging.info(f"Current avg number of shards: {number_shards}")
            scale_cluster(number_shards, status, MAX_NUM_SHARDS)
        else:
            logging.error("Failed to retrieve shard metrics.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    time.sleep(DELAY_SECONDS)
