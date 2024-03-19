# Time Series with CrateDB

This folder provides examples, tutorials and runnable code on how to use CrateDB
for time-series use cases.

The tutorials and examples focus on being easy to understand and use. They
are a good starting point for your own projects.


## What's inside

[![Made with Jupyter](https://img.shields.io/badge/Made%20with-Jupyter-orange?logo=Jupyter)](https://jupyter.org/try) [![Made with Markdown](https://img.shields.io/badge/Made%20with-Markdown-1f425f.svg?logo=Markdown)](https://commonmark.org)

This folder provides guidelines and runnable code to get started with time
series data in [CrateDB]. Please also refer to the other examples in this
repository, e.g. about machine learning, to see predictions and AutoML in action.

- [README.md](README.md): The file you are currently reading contains a
  walkthrough about how to get started with time series and CrateDB,
  and guides you to corresponding example programs and notebooks.

- `timeseries-queries-and-visualization.ipynb` [![Open on GitHub](https://img.shields.io/badge/Open%20on-GitHub-lightgray?logo=GitHub)](timeseries-queries-and-visualization.ipynb) [![Open in Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crate/cratedb-examples/blob/main/topic/timeseries/timeseries-queries-and-visualization.ipynb)

  This notebook explores how to access timeseries data from CrateDB via SQL, 
  load it into pandas data frames, and visualize it using Plotly.
  
  It also demonstrates more advanced time series queries in SQL, e.g. aggregations,
  window functions, interpolation of missing data, common table expressions, 
  moving averages, JOINs and the handling of JSON data.

- `exploratory_data_analysis.ipynb` [![Open on GitHub](https://img.shields.io/badge/Open%20on-GitHub-lightgray?logo=GitHub)](exploratory_data_analysis.ipynb) [![Open in Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crate/cratedb-examples/blob/main/topic/timeseries/exploratory_data_analysis.ipynb)

  This notebook explores how to access timeseries data from CrateDB via SQL, 
  and do the exploratory data analysis (EDA) with PyCaret.
  
  It also shows how you can generate various plots and charts for EDA, helping you understand data distributions, relationships between variables, and identify patterns.
  
- `time-series-decomposition.ipynb` [![Open on GitHub](https://img.shields.io/badge/Open%20on-GitHub-lightgray?logo=GitHub)](time-series-decomposition.ipynb) [![Open in Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crate/cratedb-examples/blob/main/topic/timeseries/time-series-decomposition.ipynb)

  This notebook illustrates how to extract data from CrateDB and how to use PyCaret for time-series decomposition.
  
  Furthermore, it shows how to preprocess data and plot time series decomposition by breaking it down into its basic components: trend, seasonality, and residual (or irregular) fluctuations.

- `time-series-anomaly-detection.ipynb` [![Open on GitHub](https://img.shields.io/badge/Open%20on-GitHub-lightgray?logo=GitHub)](time-series-anomaly-detection.ipynb) [![Open in Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/crate/cratedb-examples/blob/main/topic/timeseries/time-series-anomaly-detection.ipynb)

  This notebook walks you through the anomaly detection analysis using the PyCaret library.

- `weather-data-grafana-dashboard.json`

  An exported JSON representation of a Grafana dashboard designed to visualize weather data. This dashboard includes a set of pre-defined panels and widgets that display various weather metrics. Additionally, within this dashboard configuration, there are advanced time-series analysis queries. These queries are tailored to fetch, aggregate, interpolate, and process weather data over time.

  To ensure the dashboard functions correctly, it's necessary to configure the data source within Grafana. This dashboard uses the `grafana-postgresql-datasource` or another configured default data source. In the data source settings, fill in the necessary parameters to connect to your CrateDB instance. This includes setting up the database name (`database=doc`), user, password, and host.



[CrateDB]: https://github.com/crate/crate
