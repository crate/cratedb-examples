"""
Use MLflow to track the events and outcome of an ML experiment program using Merlion.
"""
import os

import numpy as np
import pandas as pd
from crate import client
from crate.client.exceptions import ProgrammingError
from merlion.evaluate.anomaly import TSADMetric
from merlion.models.defaults import DefaultDetector, DefaultDetectorConfig
from merlion.utils import TimeSeries

import mlflow

# Importing `mlflow_cratedb` is important for
# amalgamating MLflow with adjustments for CrateDB.
import mlflow_cratedb


def connect_database():
    """
    Connect to CrateDB, and return database connection object.
    """
    dburi = os.getenv("CRATEDB_HTTP_URL", "http://crate@localhost:4200")
    return client.connect(dburi)


def provision_data():
    """
    Download Numenta Anomaly Benchmark data, and load into database.
    """
    data = pd.read_csv(
        "https://raw.githubusercontent.com/numenta/NAB/master/data/realKnownCause/machine_temperature_system_failure.csv"
    )

    # Connecting to CrateDB.
    conn = connect_database()
    try:
        conn.cursor().execute("SELECT * FROM machine_data LIMIT 1;")
        return
    except ProgrammingError as ex:
        if "Relation 'machine_data' unknown" not in str(ex):
            raise

    # Split the data into chunks of 1000 rows each for better insert performance
    chunk_size = 1000
    chunks = np.array_split(data, int(len(data) / chunk_size))

    # Insert the data into CrateDB
    with conn:
        cursor = conn.cursor()
        # Create the table if it doesn't exist.
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS machine_data "
            "(timestamp TIMESTAMP, temperature DOUBLE)"
        )
        # Insert the data in chunks.
        for chunk in chunks:
            cursor.executemany(
                "INSERT INTO machine_data (timestamp, temperature) VALUES (?, ?)",
                list(chunk.itertuples(index=False, name=None)),
            )


def read_data() -> pd.DataFrame:
    """
    Read data from database into pandas DataFrame.
    """
    conn = connect_database()
    with conn:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT 
         DATE_BIN('5 min'::INTERVAL, "timestamp", 0) AS timestamp,
         max(temperature) as value
         FROM machine_data
         group by timestamp
         order by timestamp asc"""
        )
        data = cursor.fetchall()

    # Convert database response to pandas DataFrame.
    time_series = pd.DataFrame(
        [
            {"timestamp": pd.Timestamp.fromtimestamp(item[0] / 1000), "value": item[1]}
            for item in data
        ]
    )
    # Set the timestamp as the index
    time_series = time_series.set_index("timestamp")
    return time_series


def run_experiment(time_series: pd.DataFrame):
    """
    Run experiment on DataFrame, using Merlion. Track it using MLflow.
    """
    mlflow.set_experiment("numenta-merlion-experiment")

    with mlflow.start_run():
        train_data = TimeSeries.from_pd(
            time_series[time_series.index < pd.to_datetime("2013-12-15")]
        )
        test_data = TimeSeries.from_pd(
            time_series[time_series.index >= pd.to_datetime("2013-12-15")]
        )

        model = DefaultDetector(DefaultDetectorConfig())
        model.train(train_data=train_data)

        test_pred = model.get_anomaly_label(time_series=test_data)

        # Prepare the test labels
        time_frames = [
            ["2013-12-15 17:50:00.000000", "2013-12-17 17:00:00.000000"],
            ["2014-01-27 14:20:00.000000", "2014-01-29 13:30:00.000000"],
            ["2014-02-07 14:55:00.000000", "2014-02-09 14:05:00.000000"],
        ]

        time_frames = [
            [pd.to_datetime(start), pd.to_datetime(end)] for start, end in time_frames
        ]
        time_series["test_labels"] = 0
        for start, end in time_frames:
            time_series.loc[
                (time_series.index >= start) & (time_series.index <= end), "test_labels"
            ] = 1

        test_labels = TimeSeries.from_pd(time_series["test_labels"])

        p = TSADMetric.Precision.value(ground_truth=test_labels, predict=test_pred)
        r = TSADMetric.Recall.value(ground_truth=test_labels, predict=test_pred)
        f1 = TSADMetric.F1.value(ground_truth=test_labels, predict=test_pred)
        mttd = TSADMetric.MeanTimeToDetect.value(
            ground_truth=test_labels, predict=test_pred
        )
        print(
            f"Precision: {p:.4f}, Recall: {r:.4f}, F1: {f1:.4f}\n"
            f"Mean Time To Detect: {mttd}"
        )

        mlflow.log_metric("precision", p)
        mlflow.log_metric("recall", r)
        mlflow.log_metric("f1", f1)
        mlflow.log_metric("mttd", mttd.total_seconds())
        mlflow.log_param("anomaly_threshold", model.config.threshold.alm_threshold)
        mlflow.log_param("min_alm_window", model.config.threshold.min_alm_in_window)
        mlflow.log_param(
            "alm_window_minutes", model.config.threshold.alm_window_minutes
        )
        mlflow.log_param(
            "alm_suppress_minutes", model.config.threshold.alm_suppress_minutes
        )
        mlflow.log_param("ensemble_size", model.config.model.combiner.n_models)

        # Save the model to mlflow
        model.save("model")
        mlflow.log_artifact("model")


def main():
    """
    Provision dataset, and run experiment.
    """
    provision_data()
    df = read_data()
    run_experiment(df)


if __name__ == "__main__":
    main()
