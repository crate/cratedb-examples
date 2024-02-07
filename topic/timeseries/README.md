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


[CrateDB]: https://github.com/crate/crate
