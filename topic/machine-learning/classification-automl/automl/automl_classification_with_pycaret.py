import os
import dotenv
import sqlalchemy as sa
import pandas as pd
import mlflow_cratedb  # We need this import to use the CrateDB MLflow store
from pycaret.classification import *
from mlflow.sklearn import log_model

if os.path.exists(".env"):
    dotenv.load_dotenv(".env", override=True)


def fetch_data():
    dburi = f"crate://{os.environ['CRATE_USER']}:{os.environ['CRATE_PASSWORD']}@{os.environ['CRATE_HOST']}:4200?ssl={os.environ['CRATE_SSL']}"
    engine = sa.create_engine(dburi, echo=True)

    with engine.connect() as conn:
        with conn.execute(sa.text("SELECT * FROM pycaret_churn")) as cursor:
            data = pd.DataFrame(cursor.fetchall(), columns=cursor.keys())
    os.environ["MLFLOW_TRACKING_URI"] = f"{dburi}&schema=mlflow"


def run_experiment(data):
    s = setup(
        data,
        target="Churn",
        ignore_features=["customerID"],
        log_experiment=True,
        fix_imbalance=True,
    )

    best_models = compare_models(sort="AUC", exclude=["lightgbm"], n_select=3)
    tuned_models = [tune_model(model) for model in best_models]
    _ = [ensemble_model(i, method="Bagging") for i in tuned_models]

    def try_ensemble_model(model):
        try:
            print(type(model))
            # Attempt to ensemble the model with Boosting method
            return ensemble_model(model, method="Boosting")
        except Exception as e:
            print("Can't apply boosting.")
            return None

    _ = [try_ensemble_model(i) for i in tuned_models]
    _ = blend_models(estimator_list=tuned_models)
    best_model = automl(optimize="AUC")

    evaluate_model(best_model)
    final_model = finalize_model(best_model)

    if not os.path.exists("model"):
        os.makedirs("model")

    # Save the model to disk
    _ = save_model(final_model, "model/classification_model")
    predict_model(final_model, s.X_test)

    _ = log_model(
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
