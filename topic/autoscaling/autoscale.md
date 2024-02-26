How to scale your CrateDB Cloud cluster using REST API
======================================================

> Goal: The goal of the demo is to show how easy it is to scale out a CrateDBCloud Cluster using a simple Python script.

Introduction:
-------------
CrateDB's fully managed solution comes with a REST API which enables you to automate a lot of tasks. As CrateDB is world famous for its, highly scalable architecture, one of those tasks could be to scale a cluster out (horizontally) when needed, during a peak, for example, and back when possible to save costs. 

This small blog shows how you can use the API to scale out and scale back a cluster when needed. 

Prerequisites:
--------------
> *  A running CrateDBCloud Cluster. If you don't have one yet, please follow this link to get [started][]. Note: In order to be able to scale a cluster you need to have a dedicated cluster. 
> *  Admin UI access to the Cluster. 
> *   An active API Key/Secret combination. See [API-KEY][] for more info. Note: These keys are cloud-dependent. So, if you have multiple clusters across different cloud vendors, you need to generate different keys. 
> *   You will need both the organization ID and the cluster ID to be able to execute the correct API calls.
> *   A tool from which you are able to run a Jupyter Notebook. Like [VSCode][] or else.

[started]: https://cratedb.com/lp-crfree
[API-KEY]: https://cratedb.com/blog/introducing-api-tokens-for-cratedb-cloud
[VSCode]: https://code.visualstudio.com/download

Horizontal scaling [manual]
-------------------
Let's do things step by step first to give you a "feel" of what is possible.

Open a terminal and execute the following:

``` bash 
export APIKEY='USE YOUR API_KEY'
export APISECRET='USE YOUR API_SECRET'
export auth_data=${APIKEY}:${APISECRET}
```

Now that the authorization is defined, we can start calling APIs. For example: 

``` bash
curl -s -u  $auth_data \
https://console.cratedb.cloud/api/v2/organizations/ | jq
```

Output:
``` json
[
  {
    "dc": {
      "created": "2023-08-24T13:53:34.691000+00:00",
      "modified": "2023-10-05T09:30:54.109000+00:00"
    },
    "email": "wierd@nonofyourbusiness.org",
    "id": "2b99b347-8055-4c48-b332-d06d583c1999",
    "name": "My Organization",
    "notifications_enabled": true,
    "plan_type": 3,
    "project_count": 1,
    "role_fqn": "org_admin"
  }
]
```

Or if you want to know the current amount of nodes in your cluster. Here, you need to use the organization ID that was projected in the previous API call. For the next steps to work fluently, we can populate some variables. 

```bash
orgid=$(curl -s -u $auth_data https://console.cratedb.cloud/api/v2/organizations/ | jq -r '.[0].id')
echo ${orgid}
```

If you have multiple clusters running you need to filter using that cluster_name to get the clusterid.

```bash
# Replace these values with your authentication data and the name of the cluster you want to select
cluster_name="autoscaling-demo"

# Use jq to filter the output based on the cluster name and extract its ID
clusterid=$(curl -s -u $auth_data https://console.cratedb.cloud/api/v2/clusters/ | jq -r '.[] | select(.name == '\"$cluster_name\"') | .id')
echo ${clusterid}
```

Get the number of nodes
``` bash
numnodes=$(curl -s -u $auth_data https://console.cratedb.cloud/api/v2/clusters/${clusterid}/ | jq -r '.num_nodes')
echo ${numnodes}
```
Output
```json
3
```


So, if you want to scale out, you can call the scale API. Note that the clusterid is needed. 

```bash
curl -u $auth_data -X PUT "https://console.cratedb.cloud/api/v2/clusters/${clusterid}/scale/" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"product_unit\":2}"
```

Extra info: 
```product_unit``` is the number of nodes minus 1 as 1 is considered the minimum number. In case you want to increase a 3 node cluster you need to use 3 as the value for product_unit.

```bash
jobid=$(curl -u $auth_data -X PUT "https://console.cratedb.cloud/api/v2/clusters/${clusterid}/scale/" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"product_unit\":$numnodes}" | jq -r '.last_async_operation.id')
```
The job can be used to query the operations API to get the info on the status. 

```bash
# check status:
curl -s -u $auth_data https://console.cratedb.cloud/api/v2/clusters/${clusterid}/operations/ | jq --arg jobid "$jobid" '.operations[] | select(.id == $jobid)'
```
```json
# status should change from "status": "IN_PROGRESS" to "status": "SUCCEEDED"
{
  "dc": {
    "created": "2024-02-23T13:04:22.960000+00:00",
    "modified": "2024-02-23T13:06:52.157000+00:00"
  },
  "entity": "CLUSTER",
  "entity_id": "97ebb337-b44e-446f-adca-a092fd1df0aa",
  "feedback_data": {
    "message": "Successfully scaled cluster to 4 nodes."
  },
  "id": "10df77e7-3d33-4c4a-8c9c-93202931ed1c",
  "non_sensitive_data": {
    "current_num_nodes": 3,
    "current_product_unit": 2,
    "target_num_nodes": 4,
    "target_product_unit": 3
  },
  "status": "SUCCEEDED",
  "type": "SCALE"
}
```


Autoscaling in action
=====================

We created a Jupyter Notebook that can be used as a starting point to enable autoscaling (out and back). In this script, we check the number of shards in a cluster, and when this crosses a threshold, the cluster will be scaled out. When the threshold goes a certain number, the cluster will be scaled back.

Download the autoscaling script here [github][] and open using [VSCode][].

Add your ```API_KEY``` and ```API_SECRET``` in the ```auth_data``` variable (line 4) plus the ```organization_id``` and ```cluster_id```.

You can control the autoscale behavior by defining the ```max_num_shard``` and by tweaking the number of shards in the cluster, for example, by creating an extra table with x number of shards to see the autoscale in action. In the notebook, the ```max_num_shard``` is set to 30, but this can be changed to a number of your liking. It is also good to understand that the script will trigger a scale-out when the number of shards is higher than 80% of the ```max_num_shard```. Assuming the default number of 30, this will mean that when the number of shards exceeds 24, the autoscale will kick in. 

In this example, I created a 3-node CrateDB Cloud cluster and created this table:

``` sql
CREATE TABLE ta (
    "keyword" TEXT INDEX using fulltext 
    ,"ts" TIMESTAMP
    ,"day" TIMESTAMP GENERATED ALWAYS AS date_trunc('day', ts)
    ) 
CLUSTERED INTO 24 SHARDS;
```

This will create 8 primary shards per node plus 8 replicas. This can be checked by looking at the number of shards. This can be done for example using the console by running this:

```sql
select node ['name'], count(*) from sys.shards 
group by node ['name']
order by 1
limit 100;
```

In this example the amount of shards is 16 per node.

```sql
node['name']	    count(*)
data-hot-0	        16
data-hot-1	        16
data-hot-2	        16
```

Run the Jupyter Notebook, assuming you filled in the ```API_KEY``` ```API_SECRET``` ```organization_id``` and ```cluster_id```.

To trigger the scale-out you can add a table. For example:

```sql
CREATE TABLE tb (
    "keyword" TEXT INDEX using fulltext 
    ,"ts" TIMESTAMP
    ,"day" TIMESTAMP GENERATED ALWAYS AS date_trunc('day', ts)
    ) 
CLUSTERED INTO 18 SHARDS;
```
As you can see in the output of the running Jupyter Notebook this change is triggering a scale-out:

```text
Current avg number of shards: 16.8
Nothing to do!
Current avg number of shards: 28.0
Start scaling out from 3 to 4
Scaled up successfully!
Current avg number of shards: 21.0
Nothing to do!
```

The scaling of a cluster takes time depending on the amount of data that needs to be rebalanced. In this example, we don't really have any data, so that will be pretty quick (+/- 3mins). 

Conclusion:
==========

With this simple example, I showed how easy it is to scale out a CrateDB cluster either through an API call or using a Jupyter Notebook.


[github]: https://github.com/crate/cratedb-examples/blob/803de3c727f4326ebc079fdb3a15390f1692a738/topic/autoscaling/autoscaling_script.ipynb