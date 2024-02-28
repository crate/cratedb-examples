import logging
import requests
import time
from datetime import datetime
from requests.auth import HTTPBasicAuth

# Authentication for API requests
auth_data = HTTPBasicAuth("YOUR API KEY", "YOUR API SECRET")

# Organization and cluster IDs (to be filled by the user)
organization_id = "FILL IN YOUR ORGANIZATION ID"
cluster_id = "FILL IN YOUR CLUSTER ID"

# Date format for parsing datetime strings
date_format = "%Y-%m-%dT%H:%M:%S.%f"

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_metrics(organization_id):
    api_url = f"https://console.cratedb.cloud/api/v2/organizations/{organization_id}/metrics/prometheus/"
    headers = {"Accept": "text/plain"}
    response = requests.get(api_url, auth=auth_data)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(
            f"Failed to fetch metrics with status code: {response.status_code}"
        )


def num_shards(metrics, cluster_id):
    # Function to calculate the average number of shards per node for a given cluster
    headers = {"accept": "plain/text"}
    api_url = f"https://console.cratedb.cloud/api/v2/organizations/{organization_id}/metrics/prometheus/"
    response = requests.get(api_url, auth=auth_data, headers=headers)
    if response.status_code == 200:
        lines = response.text.split("\n")
        total_shard_count = 0
        shard_count_instances = 0
        for line in lines:
            if (
                "crate_node" in line
                and "shard_stats" in line
                and cluster_id in line
                and 'property="total"' in line
            ):
                shard_count = float(line.split()[1])
                total_shard_count += shard_count
                shard_count_instances += 1
        if shard_count_instances == 0:
            return None  # Return None if no shard counts were found
        else:
            return (
                total_shard_count / shard_count_instances
            )  # Calculate and return the average
    else:
        logging.info(f"Failed to retrieve metrics. Status code: {response.status_code}")
        return None


def get_cluster_status(cluster_id):
    # Function to get the current status of a cluster
    api_url = f"https://console.cratedb.cloud/api/v2/clusters/{cluster_id}/"
    return requests.get(api_url, auth=auth_data).json()


def get_cluster_running_op(cluster_status, cluster_id):
    # Function to get the current running operation in a cluster
    if (
        datetime.now()
        - datetime.strptime(cluster_status["health"]["last_seen"], date_format)
    ).seconds > 30:
        cluster_status = get_cluster_status(cluster_id)
    return cluster_status["health"]["running_operation"]


def get_cluster_num_nodes(cluster_status, cluster_id):
    # Function to get the current number of nodes minus one in a cluster
    if (
        datetime.now()
        - datetime.strptime(cluster_status["health"]["last_seen"], date_format)
    ).seconds > 30:
        cluster_status = get_cluster_status(cluster_id)
    return cluster_status["num_nodes"] - 1


def scale_cluster(num, cluster_status, cluster_id, max_num_shard, delay_seconds):
    operation_in_progress_msg = "Scaling operation in progress."
    if num > (0.8 * max_num_shard):
        num_nodes = get_cluster_num_nodes(cluster_status, cluster_id)
        logging.info(f"Start scaling out from {num_nodes + 1} to {num_nodes + 2}")
        requests.put(
            f"https://console.cratedb.cloud/api/v2/clusters/{cluster_id}/scale/",
            json={"product_unit": num_nodes + 1},
            auth=auth_data,
        )
        logging.info(operation_in_progress_msg)
        while get_cluster_running_op(cluster_status, cluster_id) != "":
            time.sleep(10)  # Check every 10 seconds instead of immediately looping back
            # Optionally, log at intervals rather than trying to print dots
            logging.info(operation_in_progress_msg)
        logging.info("Scaled up successfully!")
    elif num < (0.5 * max_num_shard):
        num_nodes = get_cluster_num_nodes(cluster_status, cluster_id)
        logging.info(f"Start scaling down from {num_nodes + 1} to {num_nodes}")
        requests.put(
            f"https://console.cratedb.cloud/api/v2/clusters/{cluster_id}/scale/",
            json={"product_unit": num_nodes - 1},
            auth=auth_data,
        )
        logging.info(operation_in_progress_msg)
        while get_cluster_running_op(cluster_status, cluster_id) != "":
            time.sleep(10)  # Check every 10 seconds
            # Optionally, log at intervals rather than trying to print dots
            logging.info(operation_in_progress_msg)
        logging.info("Scaled down successfully!")
    else:
        logging.info("Nothing to do!")


# Configuration for delay and shard count thresholds
delay_seconds = 5
max_num_shard = 30

while True:
    # Main loop to monitor and adjust cluster size based on shard count
    try:
        metrics = get_metrics(organization_id)  # Fetch metrics for the organization
        cluster_status = get_cluster_status(cluster_id)  # Fetch current cluster status
        num = num_shards(metrics, cluster_id)  # Calculate average shard count
        if num is not None:
            logging.info(f"Current avg number of shards: {num}")
            scale_cluster(
                num, cluster_status, cluster_id, max_num_shard, delay_seconds
            )  # Refactored scaling logic into this function
        else:
            logging.error("Failed to retrieve shard metrics.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    time.sleep(delay_seconds)
