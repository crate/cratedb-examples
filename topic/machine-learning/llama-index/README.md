# Connecting CrateDB Data to an LLM with LlamaIndex and Azure OpenAI

This folder contains the codebase for [this tutorial](https://community.cratedb.com/t/how-to-connect-your-cratedb-data-to-llm-with-llamaindex-and-azure-openai/1612) on the CrateDB community forum.  You should read the tutorial for instructions on how to set up the components that you need on Azure, and use this README for setting up CrateDB and the Python code.

This has been tested using:

* Python 3.12
* macOS
* CrateDB 5.8 and higher

## Database Setup

You will need a CrateDB Cloud database: sign up [here](https://console.cratedb.cloud/) and use the free "CRFREE" tier.

Make a note of the hostname, username and password for your database.  You'll need those when configuring the environment file later.

If you don't use CrateDB Cloud, you can also provide an instance for testing
purposes like this:

```shell
docker run --rm -it --name=cratedb \
  --publish=4200:4200 --publish=5432:5432 \
  --env=CRATE_HEAP_SIZE=2g crate:latest -Cdiscovery.type=single-node
```

Create a table in CrateDB:

```sql
CREATE TABLE IF NOT EXISTS time_series_data (
    timestamp TIMESTAMP,
    value DOUBLE,
    location STRING,
    sensor_id INT
);
```

Add some sample data:

```sql
INSERT INTO time_series_data (timestamp, value, location, sensor_id)
VALUES
    ('2023-09-14T00:00:00', 10.5, 'Sensor A', 1),
    ('2023-09-14T01:00:00', 15.2, 'Sensor A', 1),
    ('2023-09-14T02:00:00', 18.9, 'Sensor A', 1),
    ('2023-09-14T03:00:00', 12.7, 'Sensor B', 2),
    ('2023-09-14T04:00:00', 17.3, 'Sensor B', 2),
    ('2023-09-14T05:00:00', 20.1, 'Sensor B', 2),
    ('2023-09-14T06:00:00', 22.5, 'Sensor A', 1),
    ('2023-09-14T07:00:00', 18.3, 'Sensor A', 1),
    ('2023-09-14T08:00:00', 16.8, 'Sensor A', 1),
    ('2023-09-14T09:00:00', 14.6, 'Sensor B', 2),
    ('2023-09-14T10:00:00', 13.2, 'Sensor B', 2),
    ('2023-09-14T11:00:00', 11.7, 'Sensor B', 2);
```

## Python Project Setup

Create and activate a virtual environment:

```
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Configure your Environment

To configure your environment, copy the provided [`env.azure`](./env.azure) or [`env.standalone`](./env.standalone) file to a new file named `.env`, then open it with a text editor.

Set the values in the file as follows:

```
OPENAI_API_KEY=<Your key from Azure>
OPENAI_API_TYPE=azure
OPENAI_AZURE_ENDPOINT=https://<Your endpoint from Azure e.g. myendpoint.openai.azure.com>
OPENAI_AZURE_API_VERSION=2024-08-01-preview
LLM_INSTANCE=<The name of your Chat GPT 3.5 turbo instance from Azure>
EMBEDDING_MODEL_INSTANCE=<The name of your Text Embedding Ada 2.0 instance from Azure>
CRATEDB_SQLALCHEMY_URL="crate://<Database user name>:<Database password>@<Database host>:4200/?ssl=true"
CRATEDB_TABLE_NAME=time_series_data
```

Save your changes. 

## Run the Code

Run the code like so:

```bash
python demo_nlsql.py
```

Here's the expected output:

```
Creating SQLAlchemy engine...
Connecting to CrateDB...
Creating SQLDatabase instance...
Creating QueryEngine...
Running query...
> Source (Doc id: b2b0afac-6fb6-4674-bc80-69941a8c10a5): [(17.033333333333335,)]
Query was: What is the average value for sensor 1?
Answer was: The average value for sensor 1 is 17.033333333333335.
{
    'b2b0afac-6fb6-4674-bc80-69941a8c10a5': {
        'sql_query': 'SELECT AVG(value) FROM time_series_data WHERE sensor_id = 1', 
        'result': [
            (17.033333333333335,)
        ], 
        'col_keys': [
            'avg(value)'
        ]
    }, 
    'sql_query': 'SELECT AVG(value) FROM time_series_data WHERE sensor_id = 1', 
    'result': [
        (17.033333333333335,)
    ], 
    'col_keys': [
        'avg(value)'
    ]
}
```