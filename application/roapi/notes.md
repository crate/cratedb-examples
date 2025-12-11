# Notes

## Backlog

```shell
# Currently, advanced options can't be provided at runtime, please use a config file.
# https://github.com/roapi/roapi#config-file
# echo '[{"tableName": "ubuntu-ami", "uri": "test_data/ubuntu-ami.json", "option": {"format": "json", "pointer": "/aaData", "array_encoded": true}}]' | \
#    http POST http://localhost:8080/api/table
#psql -P pager=off "postgresql://localhost:5434?sslmode=disable" -c 'SELECT * FROM "ubuntu-ami"'
```
