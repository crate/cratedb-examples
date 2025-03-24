{{ config(materialized='ephemeral') }}

SELECT id
	,started
	,stmt
	,error
	,username
FROM sys.jobs_log

