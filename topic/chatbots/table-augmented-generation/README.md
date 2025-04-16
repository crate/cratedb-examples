# 🛠️ Timeseries QA Assistant with CrateDB, LLMs, and Machine Manuals

This project provides a full interactive pipeline for simulating telemetry data from industrial motors, storing that data in CrateDB, and enabling natural-language querying powered by OpenAI — including RAG-style guidance from machine manuals.

---

## 📦 Features

- **Synthetic Data Generation** for 10 industrial motors over 30 days
- **CrateDB Integration** for timeseries storage and fast querying
- **Fictional Machine Manuals** linked to each machine for RAG-style enrichment
- **LLM-Powered Chat Interface** with context-aware SQL generation
- **Emergency Protocol Suggestions** based on detected anomalies

---

## 🚀 Setup & Installation

1. **Install dependencies**

```bash
pip install -r requirements.txt
```

2. **Create a .env file in the root directory**

``` bash
OPENAI_API_KEY=your_openai_api_key
CRATEDB_HOST=localhost
CRATEDB_PORT=4200
```

3. **Ensure CrateDB is running locally (or adapt host/port to remote)**
You can use docker-compose with this `docker-compose.yml` 
``` yaml
version: "3.9"
services:
  cratedb:
    container_name: cratedb-chatbot
    image: crate
    ports:
      - "4200:4200"
      - "5432:5432"
    environment:
      - CRATE_HEAP_SIZE=1g
    deploy:
      replicas: 1
      restart_policy:
        condition: on-failure%
```

Run docker-compose:
``` bash
docker-compose pull   
docker-compose up -d
```


## Pipeline overview

1. **Generate Timeseries Data**

Creates realistic vibration, temperature, and rotation logs every 15 minutes for 10 machines.

``` bash
python DataGenerator.py
```
Output should look like:

``` bash
                   timestamp  vibration  temperature    rotations  machine_id
0 2025-03-09 10:29:35.015476   0.751030    48.971560  1609.573066           0
1 2025-03-09 10:44:35.015476   0.774157    49.696297  1601.617712           0
2 2025-03-09 10:59:35.015476   0.709293    49.308419  1603.563044           0
3 2025-03-09 11:14:35.015476   0.817229    51.463994  1586.055485           0
4 2025-03-09 11:29:35.015476   0.795769    49.277951  1596.797612           0
✅ Stored 28800 rows in CrateDB.
Total generated readings: 28800
```

2. **Generate & Store Machine Manuals**

Populates machine_manuals with fictional documentation for each machine, including:
	•	Operational limits
	•	Anomaly detection triggers
	•	Emergency protocols
	•	Maintenance schedules

``` bash
python Generate-Manuals.py
```

Output:
``` bash
✅ Fictional machine manuals stored in CrateDB.
```

3. **Run the Q&A Assistant**

Launch the interactive assistant:

``` bash
python tag-motor-chat.py
```

Example output:

``` bash
Timeseries Q&A Assistant (type 'exit' to quit)

Example Questions:
• What is the average temperature when vibration > 1.5?
• What is the average temperature when vibration > 1.5 for motor 5?
• How many anomalies happened last week?
• What was the time of highest vibration for each machine?
• What should I do if machine 2 has an anomaly?
• What does the maintenace plan for machine 1 look like?

Data Overview:
- Total readings: 1000
- Time range: 2025-04-07 11:29:35 to 2025-04-08 12:14:35
- Machines: [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
- Vibration range: 0.76 to 1.11
- Temperature range: 40.69°C to 50.27°C
- Rotations range: 1402 RPM to 1492 RPM
- Anomalies (vibration > 1.5): 0
```

## Supported Queries
Try natural language prompts like:
	•	"Show top 5 vibration events last month"
	•	"When was the last anomaly for each machine?"
	•	"What should I do if machine 3 has an anomaly?"  → Triggers manual-based response
	•	"How many anomalies occurred between March 10 and March 15?"

##  How It Works
	•	The assistant uses OpenAI GPT-3.5 to translate your question into SQL.
	•	SQL is executed directly on CrateDB, pulling up real telemetry.
	•	If anomalies (vibration > 1.5) are found, it retrieves relevant manual sections.
	•	All results are summarized and explained naturally.


## Architecture
            +--------------------------+
            |   generate_timeseries.py |
            |  → motor_readings (SQL)  |
            +--------------------------+
                        ↓
            +------------------------+
            | generate_manuals.py    |
            | → machine_manuals (SQL)|
            +------------------------+
                        ↓
            +--------------------------+
            | rag-motor-chat.py        |
            | - OpenAI Q&A             |
            | - Manual-based Guidance |
            +--------------------------+