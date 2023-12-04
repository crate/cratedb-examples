# AutoML with PyCaret and CrateDB

This folder provides examples, tutorials and runnable code on how to use CrateDB
with PyCaret to automatically create high-performing machine learning models.

The tutorials and examples focus on being easy to understand and use. They
are a good starting point for your own projects.

## About PyCaret

[PyCaret] is a Python library that makes it easy to create and train machine
learning models in Python. The outstanding features of PyCaret are its AutoML
capabilities.

PyCaret is a high-level interface on top of popular machine learning frameworks.
Amongst them are scikit-learn, xgboost, ray, lightgbm, and many more.

PyCaret provides a universal interface to utilize these libraries without
needing to know the details of the underlying model architectures and
parameters.

The general concept of PyCaret - and for the matter of fact for AutoML in
general - is rather simple: One takes the raw data, splits it into a training
and a test set and then trains a number of different models on the training
set. The models are then evaluated on the test set and the best performing
model is selected. This process gets repeated for tuning the hyperparameters
of the best models. Again, this process is highly empirical. The parameters are
changed, the model is retrained and evaluated again. This process is repeated
until the best performing parameters are found.

Modern algorithms for executing all these experiments are - amongst others -
GridSearch, RandomSearch and BayesianSearch. For a quick introduction into
these methods, see [Introduction to hyperparameter tuning].

In the past, all these trial-and-error experiments had to be done manually -
which is a tedious and time-consuming task. PyCaret automates this process
and provides a simple interface to execute all these experiments in a
straightforward way. This notebook shows how.


## What's inside

[![Made with Jupyter](https://img.shields.io/badge/Made%20with-Jupyter-orange?logo=Jupyter)](https://jupyter.org/try) [![Made with Markdown](https://img.shields.io/badge/Made%20with-Markdown-1f425f.svg?logo=Markdown)](https://commonmark.org)

This folder provides guidelines and runnable code to get started with [PyCaret]
and [CrateDB].

- [README.md](README.md): The file you are currently reading contains a
  walkthrough about how to get started with the PyCaret framework and CrateDB,
  and guides you to corresponding example programs on how to train different
  models.

- [requirements.txt](requirements.txt): For pulling the required dependencies to
  run the example programs.

- `automl_classification_with_pycaret.ipynb` [![Open on GitHub](https://img.shields.io/badge/Open%20on-GitHub-lightgray?logo=GitHub)](automl_classification_with_pycaret.ipynb) [![Open in Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crate/cratedb-examples/blob/main/topic/machine-learning/automl/automl_classification_with_pycaret.ipynb)

  This notebook explores the PyCaret framework and shows how to use it to
  train different classification models - using a user churn dataset as an
  example. The notebook demonstrates the usage of PyCaret to automatically train
  and benchmark a multitude of models and at the end select the best performing
  model. The notebook also shows how to use CrateDB as storage for both the raw
  data and the expirement tracking and model registry data.

- `automl_timeseries_forecasting_with_pycaret.ipynb` [![Open on GitHub](https://img.shields.io/badge/Open%20on-GitHub-lightgray?logo=GitHub)](automl_timeseries_forecasting_with_pycaret.ipynb) [![Open in Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crate/cratedb-examples/blob/main/topic/machine-learning/automl/automl_timeseries_forecasting_with_pycaret.ipynb)

  This notebook explores the PyCaret framework and shows how to use it to
  train various timeseries forecasting models - using a real-world sales dataset
  as an example. The notebook demonstrates the usage of PyCaret to automatically
  train and benchmark a multitude of models and at the end select the best
  performing model. The notebook also shows how to use CrateDB as storage for
  both the raw data and the expirement tracking and model registry data.

- Accompanied to the Jupyter Notebook files, there are also basic standalone
  program variants of the above examples.
  - [automl_timeseries_forecasting_with_pycaret.py](automl_timeseries_forecasting_with_pycaret.py),
  - [automl_classification_with_pycaret.py](automl_classification_with_pycaret.py).


## Software Tests

The resources are validated by corresponding software tests on CI. You can
also use those on your workstation. For example, to invoke the test cases
validating the Notebook about timeseries classification with PyCaret, run:

```shell
pytest -k automl_classification_with_pycaret.ipynb
```

Alternatively, you can validate all resources in this folder by invoking a
test runner program on the top-level folder of this repository. This is the
same code path the CI jobs are taking.
```shell
pip install -r requirements.txt
ngr test topic/machine-learning/automl
```


[CrateDB]: https://github.com/crate/crate
[Introduction to hyperparameter tuning]: https://medium.com/analytics-vidhya/comparison-of-hyperparameter-tuning-algorithms-grid-search-random-search-bayesian-optimization-5326aaef1bd1
[PyCaret]: https://github.com/pycaret/pycaret
