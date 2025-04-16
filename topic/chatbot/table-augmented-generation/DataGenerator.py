# Timeseries Data Generator - Expanded Version
import os
import numpy as np
import pandas as pd
from crate import client
from dotenv import load_dotenv
from datetime import datetime, timedelta

# === Load environment variables ===
load_dotenv()

CRATEDB_HOST = os.getenv("CRATEDB_HOST")
CRATEDB_PORT = os.getenv("CRATEDB_PORT")
CRATEDB_USER = os.getenv("CRATEDB_USER")
CRATEDB_PASSWORD = os.getenv("CRATEDB_PASSWORD")
CRATEDB_SCHEMA = os.getenv("CRATEDB_SCHEMA")

# ----- PARAMETERS -----
NUM_MACHINES = 10
DAYS = 30
FREQ = "15min"  # 15-minute intervals

# Calculate number of readings
total_readings = int((24 * 60 / 15) * DAYS * NUM_MACHINES)  # ~10K

# ----- DATA GENERATION -----
def generate_timeseries_data():
    dfs = []
    now = datetime.now()
    length = int((24 * 60 / 15) * DAYS)

    for i in range(NUM_MACHINES):
        start = pd.Timestamp(now - timedelta(minutes=15 * length))
        timestamps = pd.date_range(start, periods=length, freq=FREQ)

        # Generate data
        vibration = 0.75 + 0.25 * np.sin(np.linspace(0, 20, length)) + np.random.normal(0, 0.05, length)
        temperature = 50 + 10 * np.sin(np.linspace(0, 10, length)) + np.random.normal(0, 1, length)
        rotations = 1500 + 100 * np.cos(np.linspace(0, 15, length)) + np.random.normal(0, 10, length)

        # Inject anomalies
        if np.random.rand() > 0.3:
            anomaly_index = np.random.randint(100, length - 100)
            vibration[anomaly_index:anomaly_index + 5] += np.random.uniform(1, 2)
            temperature[anomaly_index:anomaly_index + 5] += np.random.uniform(10, 20)

        df = pd.DataFrame({
            "timestamp": timestamps,
            "vibration": vibration,
            "temperature": temperature,
            "rotations": rotations,
            "machine_id": i
        })
        dfs.append(df)
    return pd.concat(dfs)


# ----- STORE IN CRATEDB -----
def store_in_cratedb(df):
    connection = client.connect(
        f"https://{CRATEDB_HOST}:{CRATEDB_PORT}",
        username=CRATEDB_USER,
        password=CRATEDB_PASSWORD
    )
    cursor = connection.cursor()

    # Create table if not exists
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {CRATEDB_SCHEMA}.motor_readings (
        machine_id INTEGER,
        timestamp TIMESTAMP,
        vibration DOUBLE,
        temperature DOUBLE,
        rotations DOUBLE
    )
    """)

    # Insert data
    data = [(int(row.machine_id), row.timestamp.to_pydatetime(), float(row.vibration), float(row.temperature), float(row.rotations)) for _, row in df.iterrows()]
    cursor.executemany(f"""
        INSERT INTO {CRATEDB_SCHEMA}.motor_readings 
        (machine_id, timestamp, vibration, temperature, rotations) 
        VALUES (?, ?, ?, ?, ?)
        """, data)
    connection.close()
    print(f"✅ Stored {len(df)} rows in CrateDB.")


# ----- MAIN -----
if __name__ == "__main__":
    df = generate_timeseries_data()
    print(df.head())

    store_in_cratedb(df)

    print(f"Total generated readings: {len(df)}")
