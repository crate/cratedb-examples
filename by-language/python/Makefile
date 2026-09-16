default:
	@echo Sandbox support for Python example programs.
	@echo 'Use "make format", or "make lint".'
	@exit 1

format:
	ruff --fix .
	isort .
	black .

lint:
	ruff .
	isort --check .
	black --check .
	mypy --ignore-missing-imports .
