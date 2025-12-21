.DEFAULT_GOAL:=help

.PHONY: test
test: ## Run the integration tests.
	@\
	docker compose up --detach --wait
	sh client_crash.sh
	sh client_pgsql.sh
	uv run client_dbapi.py
	uv run client_sqlalchemy.py
	uv run client_psycopg.py
	docker compose down

.PHONY: help
help: ## Show this help message.
	@echo 'usage: make [target]'
	@echo
	@echo 'targets:'
	@grep -E '^[8+a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
