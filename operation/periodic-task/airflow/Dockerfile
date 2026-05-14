FROM astrocrpublic.azurecr.io/runtime:3.2-3-base

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
USER root
COPY requirements.txt .
ARG TARGETARCH
ARG TARGETVARIANT
RUN --mount=type=cache,id=uv-${TARGETARCH}${TARGETVARIANT},target=/root/.cache/uv \
    uv pip install --requirements=requirements.txt
USER astro

# Add programs to be scheduled periodically to the `dags` folder.
# Their schedule is defined inline with the program source.
COPY workflows.py ./dags/
CMD ["airflow", "standalone"]
