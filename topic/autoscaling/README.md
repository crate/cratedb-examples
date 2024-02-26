###############################
How to run the autoscale script
###############################

*****
About
*****

This python script can be used to autoscale a CrateDB Cloud Cluster. This script monitors the amount of shards that are on the nodes in the cluster. 
When this crosses a threshold the cluster will add a node or when the threshold goes under a curtain number the cluster will be scaled-back.

For more depth and background on this please see the commity post about autoscaling. <ADD LINK>

*****
Usage
*****

Run dedicated cluster in CrateDB Cloud::

    https://console.cratedb.cloud/

Install script::

    git clone https://github.com/crate/cratedb-examples
    cd cratedb-examples/topic/autoscaling


Change script::
  Make sure to edit the script before running it. 
  Update line 7, 10 and 11 with your API credentials, organization id and cluster id. 

Run script::

    python autscale.py


