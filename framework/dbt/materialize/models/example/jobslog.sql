{{ config(materialized='ephemeral') }}

select * from sys.jobs_log
