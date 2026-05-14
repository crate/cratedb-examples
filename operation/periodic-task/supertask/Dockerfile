FROM docker.io/python:3.14-slim-bookworm

# Install `uv` package manager.
# - Tell uv to byte-compile packages for faster application startups.
# - Silence uv complaining about not being able to use hard links.
# - Install packages into the system Python environment.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
ENV \
    UV_COMPILE_BYTECODE="true" \
    UV_LINK_MODE="copy" \
    UV_SYSTEM_PYTHON="true"

# Install required Python packages.
ARG TARGETARCH
ARG TARGETVARIANT
COPY requirements.txt .
RUN --mount=type=cache,id=uv-${TARGETARCH}${TARGETVARIANT},target=/root/.cache/uv \
    uv pip install --requirements=requirements.txt

# Add the workflow program to be scheduled periodically.
COPY workflow.py .
CMD ["supertask", "run", "workflow.py"]
