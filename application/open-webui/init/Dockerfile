FROM python:3.13-slim-bookworm

# Configure operating system.
ENV DEBIAN_FRONTEND=noninteractive
ENV TERM=linux

RUN set -e \
    && apt-get update \
    && apt-get --yes install --no-install-recommends --no-install-suggests curl jq \
    && rm -rf /var/lib/apt/lists/*

# Install and configure `uv`.
# Guidelines that have been followed.
# - https://hynek.me/articles/docker-uv/

# Install the `uv` package manager.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY --from=ghcr.io/astral-sh/uv:latest /uvx /usr/local/bin/uvx

# - Tell uv to byte-compile packages for faster application startups.
# - Silence uv complaining about not being able to use hard links.
# - Prevent uv from accidentally downloading isolated Python builds.
# - Install packages into the system Python environment.
ENV \
    UV_COMPILE_BYTECODE=true \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_SYSTEM_PYTHON=true

RUN uv pip install crash cratedb-mcp httpie

RUN mkdir /app
WORKDIR /app
COPY .env setup.sh *.json *.sql /app/
