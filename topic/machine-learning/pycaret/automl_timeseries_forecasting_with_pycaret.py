import pandas as pd
import sqlalchemy as sa
import os
import mlflow_cratedb  # Required to enable the CrateDB MLflow adapter.
from dotenv import load_dotenv
from mlflow.sklearn import log_model

from pycaret.time_series import (
    setup,
    compare_models,
    tune_model,
    blend_models,
    finalize_model,
    save_model,
)

if os.path.isfile(".env"):
    load_dotenv(".env", override=True)

# Configure to connect to CrateDB server on localhost.
CONNECTION_STRING = os.environ.get(
    "CRATEDB_CONNECTION_STRING",
    "crate://crate@localhost/?ssl=false",
)

# Compute derived connection strings for SQLAlchemy use vs. MLflow use.
DBURI_DATA = f"{CONNECTION_STRING}&schema=testdrive"
DBURI_MLFLOW = f"{CONNECTION_STRING}&schema=mlflow"

# Propagate database connectivity settings.
engine = sa.create_engine(DBURI_DATA, echo=bool(os.environ.get("DEBUG")))
os.environ["MLFLOW_TRACKING_URI"] = DBURI_MLFLOW


def prepare_data():
    target_data = pd.read_csv(
        "https://data.4tu.nl/file/539debdb-a325-412d-b024-593f70cba15b/a801f5d4-5dfe-412a-ace2-a64f93ad0010"
    )
    related_data = pd.read_csv(
        "https://data.4tu.nl/file/539debdb-a325-412d-b024-593f70cba15b/f2bd27bd-deeb-4933-bed7-29325ee05c2e",
        header=None,
    )
    related_data.columns = ["item", "org", "date", "unit_price"]
    data = target_data.merge(related_data, on=["item", "org", "date"])
    data["total_sales"] = data["unit_price"] * data["quantity"]
    data["date"] = pd.to_datetime(data["date"])

    # Insert the data into CrateDB
    engine = sa.create_engine(DBURI_DATA, echo=bool(os.environ.get("DEBUG")))

    with engine.connect() as conn:
        data.to_sql(
            "sales_data_for_forecast",
            conn,
            index=False,
            chunksize=1000,
            if_exists="replace",
        )

        # Refresh table to make sure the data is available for querying - as CrateDB
        # is eventually consistent
        conn.execute(sa.text("REFRESH TABLE sales_data_for_forecast;"))


def fetch_data():
    query = """
        SELECT
            DATE_TRUNC('month', DATE) AS MONTH,
            SUM(total_sales) AS total_sales
        from sales_data_for_forecast
        group by month
        order by month
    """

    with engine.connect() as conn:
        with conn.execute(sa.text(query)) as cursor:
            data = pd.DataFrame(cursor.fetchall(), columns=cursor.keys())

    data["month"] = pd.to_datetime(data["month"], unit="ms")
    return data


def run_experiment(data):
    setup(data = data, fh=15, target="total_sales", index="month", log_experiment=True)
    if "PYTEST_CURRENT_TEST" in os.environ:
        best_models = compare_models(sort="MASE",
                                    include=["arima", "ets", "exp_smooth"],
                                    n_select=3)
    else:
        best_models = compare_models(sort="MASE", n_select=3)

    tuned_models = [tune_model(model) for model in best_models]
    blend = blend_models(estimator_list=tuned_models)
    best_model = blend
    final_model = finalize_model(best_model)
    os.makedirs("model", exist_ok=True)

    save_model(final_model, "model/timeseriesforecast_model")

    log_model(
        sk_model=final_model,
        artifact_path="model/timeseriesforecast_model",
        registered_model_name="timeseriesforecast_model",
    )


def main():
    """
    Provision dataset, and run experiment.
    """
    prepare_data()
    df = fetch_data()
    run_experiment(df)


if __name__ == "__main__":
    main()
