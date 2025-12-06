# Backlog

```text
Transfer failed: Data transfer error: Failed to insert batch: error returned from database:
readerIndex: 1315907160, writerIndex: 215335 (expected: 0 <= readerIndex <= writerIndex <= capacity(215335))
```
```shell
tinyetl \
  "https://cdn2.crate.io/downloads/datasets/cratedb-datasets/machine-learning/automl/churn-dataset.csv" \
  "postgresql://crate:crate@localhost/testdrive#churn"
```
