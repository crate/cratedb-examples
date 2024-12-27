# Azure Function - Event hub triggered

This is a sample Azure Function in Python programming model v2 consuming Event hub batches, enriching them and inserting into CrateDB. The processed data will end up in one of the following tables: reading or error. 

## Set up the Azure Function example

### Clone Azure function folder
Clone the "Azure Function" folder locally and open VS Code with the Azure plugin installed.

### Create Azure resources
Once you have this function locally, you should set up your Azure account with the required resources:

- Azure Function App
- Event Hub

### Set Azure Function variables
You have to configure the Environment variables in the Function app to ensure it connects with CrateDB with the right table references and connects with the Event Hub as well. It can be done in Function App > Settings > Environment variables.
```json
{
  "EVENT_HUB_CONNECTION_STRING": "Endpoint=sb://<YourEventHubNamespace>.servicebus.windows.net/;SharedAccessKeyName=<YourPolicyName>;SharedAccessKey=<YourKey>",
    "READING_TABLE": "enrichment.reading",
    "ERROR_TABLE": "enrichment.error",
    "HOST": "<HOST-URL>:4200",
    "DB_USER": "azure_demo",
    "DB_PASSWORD": "<PASSWORD>"
}
  ```
You can find the connection string in Event Hub namespace > Shared access policies.

### Create Tables
You should create the following tables in your CrateDB instance:

<details>
  <summary>enrichment.error</summary>

  ```sql
  
CREATE TABLE IF NOT EXISTS "enrichment"."error" (
   "error" OBJECT(IGNORED),
   "payload" OBJECT(IGNORED),
   "insert_ts" TIMESTAMP WITH TIME ZONE,
   "type" TEXT
)
  ```
</details>
<details>
  <summary>enrichment.reading</summary>

  ```sql
  
CREATE TABLE IF NOT EXISTS "enrichment"."reading" (
   "location" TEXT,
   "sensor_id" TEXT,
   "reading_ts" TIMESTAMP WITHOUT TIME ZONE,
   "reading" OBJECT(DYNAMIC),
   "insert_ts" TIMESTAMP WITHOUT TIME ZONE
)
  ```
</details>

### Deploy the Azure Function in VS Code
In the Azure plugin tab in the VS Code, there is an option to deploy the function to your already-created Function App. You can find the details [here](https://learn.microsoft.com/en-us/azure/azure-functions/functions-develop-vs-code?tabs=node-v4%2Cpython-v2%2Cisolated-process%2Cquick-create&pivots=programming-language-python#republish-project-files). This should send your function to your Azure account.

### Manually trigger event in Event Hub
The Event hub is not connected to any source, so to test your function after it is configured and deployed, go to Event Hubs Instance > Data Explorer > Send events. In the payload text box, write the following json:
```json
[
  {
    "id":"ABC001",
    "location": "BR",
    "ts":"1735231892159",
    "temperature":1.23,
    "humidity":72.3,
    "light":"high"
  }
]
  ```
This should result in a new record in the `enrichment.reading` table but no errors.
If you want to trigger an error, run the following payload:
```json
[
  {
    "id":"ABC002",
    "location": "BR",
    "ts":"ABC",
    "temperature":1.27,
    "humidity":72.7,
    "light":"high"
  }
]
  ```
This second payload has a string value instead of a timestamp. With that, you should see one new record in the `enrichment.error` table. Finally, test with more than one event at the same time.

```json
[
  {
    "id":"ABC552",
    "location": "US",
    "ts":"ABC",
    "temperature":1.27,
    "humidity":52.7,
    "light":"high"
  },
  {
    "id":"ABC762",
    "location": "PT",
    "ts":"1735232089882",
    "temperature":15.7,
    "humidity":82.7,
    "light":"high"
  }
]
  ```
The batch above should result in two new records: one in `enrichment.reading` and the other in `enrichment.error`, because of the string value for the timestamp column again.

## Wrap-up
It is simple to set up an Azure Function to consume the Event Hub events. To achieve that, use the [crate client](https://cratedb.com/docs/python/en/latest/index.html) to connect with your CrateDB cluster as you saw in the `cratedb_writer.py` script.