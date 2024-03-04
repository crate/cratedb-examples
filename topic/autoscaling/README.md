# Autoscaling

## Introduction

Autoscaling is the process of scaling up and down your CrateDB Cluster
on demand.

## About

This Python program can be used to autoscale a CrateDB Cloud Cluster.

The program monitors the number of shards that are on the nodes in the
cluster. If that number crosses a threshold, a new node will be added
to the database cluster.

When the number of shards goes back down below another threshold, the
cluster will be scaled-back, by decommissioning excess nodes again.

For more depth and background on this please see the community post
about autoscaling. 
> <https://community.cratedb.com/t/autoscale-a-cratedb-cloud-cluster/1731>

## Usage

Run a dedicated cluster in CrateDB Cloud:

> <https://console.cratedb.cloud/>

### Install

The script uses a couple of Python libraries. Make sure you have installed those:
```shell
pip install datetime
pip install requests
```

```shell
git clone https://github.com/crate/cratedb-examples
cd cratedb-examples/topic/autoscaling
```

### Configure

Make sure to edit the script before running it. Update lines 7, 10,
and 11 with your API credentials, organization id and cluster id.

### Run
```shell
python autoscale.py
```
