-- https://github.com/crate/cratedb-datasets

CREATE TABLE IF NOT EXISTS devices_readings (
   "ts" TIMESTAMP WITH TIME ZONE,
   "device_id" TEXT,
   "battery" OBJECT(DYNAMIC) AS (
      "level" BIGINT,
      "status" TEXT,
      "temperature" DOUBLE PRECISION
   ),
   "cpu" OBJECT(DYNAMIC) AS (
      "avg_1min" DOUBLE PRECISION,
      "avg_5min" DOUBLE PRECISION,
      "avg_15min" DOUBLE PRECISION
   ),
   "memory" OBJECT(DYNAMIC) AS (
      "free" BIGINT,
      "used" BIGINT
   )
);

CREATE TABLE IF NOT EXISTS devices_info (
    "device_id" TEXT,
    "api_version" TEXT,
    "manufacturer" TEXT,
    "model" TEXT,
    "os_name" TEXT
);

COPY "devices_readings"
  FROM 'https://cdn.crate.io/downloads/datasets/cratedb-datasets/cloud-tutorials/devices_readings.json.gz'
  WITH (compression = 'gzip');

COPY "devices_info"
  FROM 'https://cdn.crate.io/downloads/datasets/cratedb-datasets/cloud-tutorials/devices_info.json.gz'
  WITH (compression = 'gzip');
