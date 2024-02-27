import requests
import time
from datetime import datetime
from requests.auth import HTTPBasicAuth

# Authentication for API requests
auth_data = HTTPBasicAuth('YOUR API KEY', 'YOUR API SECRET')

# Organization and cluster IDs (to be filled by the user)
organization_id = 'FILL IN YOUR ORGANIZATION ID'
cluster_id = 'FILL IN YOUR CLUSTER ID'

# Date format for parsing datetime strings
date_format = '%Y-%m-%dT%H:%M:%S.%f'

# Function to fetch metrics from CrateDB Cloud for a specific organization
def get_metrics(organization_id):
    api_url = f'https://console.cratedb.cloud/api/v2/organizations/{organization_id}/metrics/prometheus/'
    headers = {'accept': 'plain/text'}
    response = requests.get(api_url, auth=auth_data)
    return response.text

# Function to calculate the average number of shards per node for a given cluster
def num_shards(metrics, cluster_id):
    headers = {'accept': 'plain/text'}
    api_url = f"https://console.cratedb.cloud/api/v2/organizations/{organization_id}/metrics/prometheus/"
    response = requests.get(api_url, auth=auth_data, headers=headers)
    if response.status_code == 200:
        lines = response.text.split('\n')
        total_shard_count = 0
        shard_count_instances = 0
        for line in lines:
            if "crate_node" in line and "shard_stats" in line and cluster_id in line and "property=\"total\"" in line:
                shard_count = float(line.split()[1])
                total_shard_count += shard_count
                shard_count_instances += 1
        if shard_count_instances == 0:
            return None  # Return None if no shard counts were found
        else:
            return total_shard_count / shard_count_instances  # Calculate and return the average
    else:
        print(f"Failed to retrieve metrics. Status code: {response.status_code}")
        return None

# Function to get the current status of a cluster
def get_cluster_status(cluster_id):
    api_url = f'https://console.cratedb.cloud/api/v2/clusters/{cluster_id}/'
    return requests.get(api_url, auth=auth_data).json()

# Function to get the current running operation in a cluster
def get_cluster_running_op(cluster_status, cluster_id):
    if (datetime.now() - datetime.strptime(cluster_status['health']['last_seen'], date_format)).seconds > 30:
        cluster_status = get_cluster_status(cluster_id)
    return cluster_status['health']['running_operation']

# Function to get the current number of nodes minus one in a cluster
def get_cluster_num_nodes(cluster_status, cluster_id):
    if (datetime.now() - datetime.strptime(cluster_status['health']['last_seen'], date_format)).seconds > 30:
        cluster_status = get_cluster_status(cluster_id)
    return cluster_status['num_nodes'] - 1

# Configuration for delay and shard count thresholds
delay_seconds = 5
max_num_shard = 30

# Main loop to monitor and adjust cluster size based on shard count
while True:
    metrics = get_metrics(organization_id)  # Fetch metrics for the organization
    cluster_status = get_cluster_status(cluster_id)  # Fetch current cluster status
    num = num_shards(metrics, cluster_id)  # Calculate average shard count
    if num is not None:
        print(f'Current avg number of shards: {num}')
        if num > (0.8 * max_num_shard):
            num_nodes = get_cluster_num_nodes(cluster_status, cluster_id)
            print(f'Start scaling out from {num_nodes + 1} to {num_nodes + 2}')
            requests.put(f'https://console.cratedb.cloud/api/v2/clusters/{cluster_id}/scale/', json={'product_unit': num_nodes + 1}, auth=auth_data)
            time.sleep(delay_seconds)
            while get_cluster_running_op(cluster_status, cluster_id) != '':
                time.sleep(delay_seconds)
                cluster_status = get_cluster_status(cluster_id)
            print('Scaled up successfully!')
        elif num < (0.5 * max_num_shard):
            num_nodes = get_cluster_num_nodes(cluster_status, cluster_id)
            print(f'Start scaling down from {num_nodes + 1} to {num_nodes}')
            requests.put(f'https://console.cratedb.cloud/api/v2/clusters/{cluster_id}/scale/', json={'product_unit': num_nodes - 1}, auth=auth_data)
            time.sleep(delay_seconds)
            while get_cluster_running_op(cluster_status, cluster_id) != '':
                cluster_status = get_cluster_status(cluster_id)
            print('Scaled down successfully!')
        else:
            print('Nothing to do!')
    else:
        print('Failed to retrieve shard metrics.')
    time.sleep(delay_seconds)
