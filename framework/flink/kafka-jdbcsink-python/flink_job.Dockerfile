FROM python:3.10-bullseye
# Python version is important, because as of today (2024-03-04) kafka-flink is only
# supported for python<=3.10

ARG POSTGRESQL_JAR_URL
ARG FLINK_SQL_JAR_URL
ARG FLINK_KAFKA_JAR_URL

WORKDIR /app
COPY * /app
RUN wget ${POSTGRESQL_JAR_URL} --directory-prefix=/app/jars
RUN wget ${FLINK_SQL_JAR_URL} --directory-prefix=/app/jars
RUN wget ${FLINK_KAFKA_JAR_URL} --directory-prefix=/app/jars

RUN apt update && apt install -y openjdk-11-jdk
RUN pip install poetry

RUN poetry config virtualenvs.create false && poetry install
