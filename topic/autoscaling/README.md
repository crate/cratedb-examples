How to run the autoscale script
===============================

*****
About
*****

This Python script can be used to autoscale a CrateDB Cloud Cluster. This script monitors the number of shards that are on the nodes in the cluster. 
When this crosses a threshold the cluster will add a node and when it goes back down below another threshold the cluster will be scaled-back.

For more depth and background on this please see the community post about autoscaling. <ADD LINK>

*****
Usage
*****

Run a dedicated cluster in CrateDB Cloud:

    https://console.cratedb.cloud/

The script uses a couple of python libraries. Make sure you have installed those::

    pip install datetime
    pip install requests
    pip install prometheus_client


Install script::

    git clone https://github.com/crate/cratedb-examples
    cd cratedb-examples/topic/autoscaling


Change script::
  Make sure to edit the script before running it. 
  Update lines 7, 10, and 11 with your API credentials, organization id and cluster id. 

Run script::

    python autoscale.py


