# Azure Function - Event hub triggered

This is a sample Azure Function in Python programming model v2 consuming Event hub batches, enriching them and inserting into CrateDB. The processed data will end up in one or more of the following tables: raw, reading or error. 

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
    "RAW_TABLE": "enrichment.raw",
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
  <summary>enrichment.raw</summary>

  ```sql
  
CREATE TABLE IF NOT EXISTS "enrichment"."raw" (
   "insert_ts" TIMESTAMP WITH TIME ZONE,
   "payload" OBJECT(IGNORED),
   "trace_id" TEXT
)
  ```
</details>
<details>
  <summary>enrichment.error</summary>

  ```sql
  
CREATE TABLE IF NOT EXISTS "enrichment"."error" (
   "error" OBJECT(IGNORED),
   "payload" OBJECT(IGNORED),
   "insert_ts" TIMESTAMP WITH TIME ZONE,
   "type" TEXT,
   "trace_id" TEXT
)
  ```
</details>
<details>
  <summary>enrichment.ls_reading</summary>

  ```sql
  
CREATE TABLE IF NOT EXISTS "enrichment"."reading" (
   "country" TEXT,
   "value" REAL,
   "insert_ts" TIMESTAMP WITH TIME ZONE,
   "reading_ts" TIMESTAMP WITH TIME ZONE,
   "trace_id" TEXT,
   "id" TEXT
)
  ```
</details>

### Deploy the Azure Function in VS Code
In the Azure plugin tab in the VS Code, there is an option to deploy the function to your already-created Function App. You can find the details [here](https://learn.microsoft.com/en-us/azure/azure-functions/functions-develop-vs-code?tabs=node-v4%2Cpython-v2%2Cisolated-process%2Cquick-create&pivots=programming-language-python#republish-project-files). This should send your function to your Azure account.

### Manually trigger event in Event Hub
The Event hub is not connected to any source, so to test your function after it is configured and deployed, you go to Event Hubs Instance > Data Explorer > Send events. In the payload text box, write the following json:
```json
{
    "country":"PT",
    "type":"light_sensor",
    "value":"1",
    "id":"ABC001",
    "reading_ts":"1732703748223"
}
  ```
This should result in new records in both `enrichment.raw` and `enrichment.reading` but no errors.
If you want to trigger an error, run the following payload:
```json
[
  {
    "country":"PT",
    "type":"light_sensor",
    "value":"1",
    "id":"ABC001",
    "reading_ts":"1732703748223"
  },
  {
    "country":"AU",
    "type":"light_sensor",
    "value":"ABC",
    "id":"ABC001",
    "reading_ts":"1732703748223"
  }
]
  ```
The second payload has a string value instead of a numeric one. With that, you should see two new records in `enrichment.raw`, one in `enrichment.reading` and one in `enrichment.error`.