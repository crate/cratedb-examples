FROM python:3.10

WORKDIR /app
COPY * /app

RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install
