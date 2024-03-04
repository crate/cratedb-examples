"""
An example of how to scale your CrateDB Cloud cluster automatically,
based on its Prometheus metrics endpoint.
"""

import argparse
import logging
import os
import time
from functools import reduce

from prometheus_client.parser import text_string_to_metric_families

from cratedb_cloud_api import CrateDBCloudAPI

# Configure logging
logging.basicConfig(level=logging.INFO)

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

cloud_api = CrateDBCloudAPI(
    os.getenv("CRATEDB_CLOUD_API_KEY"),
    os.getenv("CRATEDB_CLOUD_API_SECRET"),
    args.organization_id,
    args.cluster_id,
)


def num_shards(cluster_id):
    "Calculate the average number of shards per node for a given cluster"
    response = cloud_api.get_metrics()

    samples = []
    for family in text_string_to_metric_families(response.text):
        for sample in family.samples:
            if (
                sample.name == "crate_node"
                and sample.labels["name"] == "shard_stats"
                and args.cluster_id in sample.labels["pod_name"]
                and cluster_id in sample.labels["pod_name"]
                and sample.labels["property"] == "total"
            ):
                samples.append(sample.value)

    if len(samples) == 0:
        return 0

    return reduce(lambda a, b: a + b, samples) / len(samples)


def get_cluster_num_nodes():
    "Get the current number of nodes in a cluster"
    num_nodes = cloud_api.get_cluster_status()["num_nodes"]

    # The scale unit represents the number of nodes added from a minimum deployment perspective.
    # I.e., it is 0 for a single-node cluster, 1 for a two-nodes cluster,
    # 2 for a three-nodes cluster, ...
    return {
        "nodes": num_nodes,
        "scale_unit": num_nodes - 1,
    }


def scale(increment):
    "Initiates the scaling based on a given increment"
    num_nodes = get_cluster_num_nodes()
    if increment == 0:
        return

    direction = "up" if increment > 0 else "down"

    logging.info(
        "Start scaling %s from %s to %s",
        direction,
        num_nodes["nodes"],
        num_nodes["nodes"] + increment,
    )
    cloud_api.scale(num_nodes["scale_unit"] + increment)
    cloud_api.wait_for_operation()
    logging.info("Scaled %s successfully!", direction)


def scale_cluster(cur_num_shards, max_num_shards):
    "Scale out of back when reaching the treshold(s)"
    shard_ratio = cur_num_shards / max_num_shards

    if shard_ratio > 0.8:
        scale(1)
    elif shard_ratio < 0.5:
        scale(-1)
    else:
        logging.info("Nothing to do!")


DELAY_SECONDS = 10
MAX_NUM_SHARDS = 30


def main():
    "Main loop to monitor and adjust cluster size based on shard count"
    while True:
        # Calculate average shard count
        number_shards = num_shards(args.cluster_id)
        logging.info("Current avg number of shards: %s", number_shards)

        scale_cluster(number_shards, MAX_NUM_SHARDS)

        time.sleep(DELAY_SECONDS)


if __name__ == "__main__":
    main()
