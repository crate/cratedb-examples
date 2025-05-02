CREATE TABLE IF NOT EXISTS "doc"."_dlt_version" (
	"version" bigint  NOT NULL,
	"engine_version" bigint  NOT NULL,
	"inserted_at" timestamp with time zone  NOT NULL,
	"schema_name" varchar  NOT NULL,
	"version_hash" varchar  NOT NULL,
	"schema" varchar  NOT NULL);
	CREATE TABLE IF NOT EXISTS "doc"."_dlt_loads" (
	"load_id" varchar  NOT NULL,
	"schema_name" varchar  ,
	"status" bigint  NOT NULL,
	"inserted_at" timestamp with time zone  NOT NULL,
	"schema_version_hash" varchar  );
	CREATE TABLE IF NOT EXISTS "doc"."_dlt_pipeline_state" (
	"version" bigint  NOT NULL,
	"engine_version" bigint  NOT NULL,
	"pipeline_name" varchar  NOT NULL,
	"state" varchar  NOT NULL,
	"created_at" timestamp with time zone  NOT NULL,
	"version_hash" varchar  ,
	"_dlt_load_id" varchar  NOT NULL,
	"_dlt_id" varchar UNIQUE NOT NULL);
	CREATE TABLE "doc"."player" (
	"avatar" varchar  ,
	"player_id" bigint  ,
	"aid" varchar  ,
	"url" varchar  ,
	"name" varchar  ,
	"username" varchar  ,
	"title" varchar  ,
	"followers" bigint  ,
	"country" varchar  ,
	"location" varchar  ,
	"last_online" bigint  ,
	"joined" bigint  ,
	"status" varchar  ,
	"is_streamer" boolean  ,
	"verified" boolean  ,
	"league" varchar  ,
	"_dlt_load_id" varchar  NOT NULL,
	"_dlt_id" varchar UNIQUE NOT NULL);
