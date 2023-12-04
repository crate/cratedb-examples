"""
Example program for exercising the "AutoML with PyCaret and CrateDB" article.
This is a standalone variant. A corresponding .ipynb Jupyter Notebook can usually
be found side-by-side to this file.
"""
import os
import dotenv
import sqlalchemy as sa
import pandas as pd
import mlflow_cratedb  # Required to enable the CrateDB MLflow adapter.
from pycaret.classification import setup, compare_models, tune_model, ensemble_model, blend_models, automl, \
    evaluate_model, finalize_model, save_model, predict_model
from mlflow.sklearn import log_model


if os.path.exists(".env"):
    dotenv.load_dotenv(".env", override=True)


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


def fetch_data():
    """
    Fetch data from CrateDB, using SQL and SQLAlchemy, and wrap result into pandas data frame.
    """
    engine = sa.create_engine(DBURI_DATA, echo=True)

    with engine.connect() as conn:
        with conn.execute(sa.text("SELECT * FROM pycaret_churn")) as cursor:
            data = pd.DataFrame(cursor.fetchall(), columns=cursor.keys())
            return data


def run_experiment(data):
    """
    Run an AutoML experiment using PyCaret, MLflow, and CrateDB.
    """
    s = setup(
        data=data,
        data_func=None,
        target="Churn",
        ignore_features=["customerID"],
        log_experiment=True,
        fix_imbalance=True,
    )

    best_models = compare_models(sort="AUC", exclude=["lightgbm"], n_select=3)
    tuned_models = [tune_model(model) for model in best_models]
    [ensemble_model(i, method="Bagging") for i in tuned_models]

    def try_ensemble_model(model):
        try:
            print(type(model))
            # Attempt to ensemble the model with Boosting method.
            return ensemble_model(model, method="Boosting")
        except Exception as e:
            print("Can't apply boosting.")
            return None

    [try_ensemble_model(i) for i in tuned_models]
    blend_models(estimator_list=tuned_models)
    best_model = automl(optimize="AUC")

    final_model = finalize_model(best_model)

    # Save the model to disk.
    os.makedirs("model", exist_ok=True)
    save_model(final_model, "model/classification_model")
    predict_model(final_model, s.X_test)

    log_model(
        sk_model=best_model,
        artifact_path="model/classification_model",
        registered_model_name=f"classification-model",
    )


def main():
    """
    Provision dataset, and run experiment.
    """
    df = fetch_data()
    run_experiment(df)


if __name__ == "__main__":
    main()
