ARG DASK_VERSION="latest-py3.13"

FROM docker.io/daskdev/dask:${DASK_VERSION}

# Enable concurrent multi-arch builds.
# https://github.com/docker/buildx/issues/549#issuecomment-1788297892
ARG TARGETPLATFORM
ARG TARGETOS
ARG TARGETARCH
ARG TARGETVARIANT

# Install and configure build prerequisites.
RUN apt-get update && apt-get install --yes --no-install-recommends --no-install-suggests git
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
ENV UV_COMPILE_BYTECODE="true"
ENV UV_LINK_MODE="copy"
ENV UV_SYSTEM_PYTHON="true"

# Install payload package.
COPY requirements.txt /
RUN \
    --mount=type=cache,id="uv-${TARGETARCH}${TARGETVARIANT}",target="/root/.cache/uv" \
    uv pip install --requirement="requirements.txt"
