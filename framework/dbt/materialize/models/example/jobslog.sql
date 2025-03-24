{{ config(materialized='ephemeral') }}

SELECT id
	,started
	,ended
	,stmt
	,error
	,username
	,classification['type'] as type
FROM sys.jobs_log

