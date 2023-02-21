FROM python:3.11-slim-bullseye

ENV DEBIAN_FRONTEND=noninteractive

# Install prerequisites.
RUN apt-get update
RUN apt-get install --yes build-essential libboost-dev odbc-postgresql unixodbc-dev

# Install NumPy, PyArrow, and turbodbc.
ADD requirements*.txt .
RUN pip install --upgrade --requirement=requirements-prereq.txt
RUN MAKEFLAGS="-j$(nproc)" pip install --upgrade --requirement=requirements.txt --verbose
