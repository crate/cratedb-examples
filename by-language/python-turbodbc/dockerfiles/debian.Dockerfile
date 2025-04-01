# Set up Debian Linux.
FROM debian:bookworm-slim AS build

# Configure system environment.
ENV DEBIAN_FRONTEND=noninteractive

# Install Python, unixODBC, the PostgreSQL ODBC driver, and development libraries.
RUN apt-get update
RUN apt-get install --yes \
    bc build-essential cmake git libboost-dev pkg-config \
    python3-pip python3-pybind11


# Set up ODBC.
FROM build AS odbc

# Install unixODBC and the PostgreSQL ODBC driver.
RUN apt-get install --yes \
    odbc-postgresql unixodbc-dev


# Apache Arrow and simdutf.
FROM odbc AS arrow-simdutf

# Install Apache Arrow.
# https://arrow.apache.org/install/
RUN apt install -y -V ca-certificates lsb-release wget
RUN wget https://repo1.maven.org/maven2/org/apache/arrow/$(lsb_release --id --short | tr 'A-Z' 'a-z')/apache-arrow-apt-source-latest-$(lsb_release --codename --short).deb
RUN apt install -y -V ./apache-arrow-apt-source-latest-$(lsb_release --codename --short).deb
RUN apt-get update
RUN apt-get install --yes \
    libarrow-dev libarrow-dataset-dev libarrow-acero-dev libarrow-flight-dev \
    libarrow-flight-sql-dev libgandiva-dev libparquet-dev

# Install ultra-fast Unicode routines.
# TODO: The version number here would need to be bumped, in order to validate
#       against new upstream releases. The Debian OCI image (this one) has been
#       selected to run on CI/GHA.
RUN true \
    && git clone https://github.com/simdutf/simdutf --branch=v6.4.0 \
    && cd simdutf \
    && cmake -B build -DCMAKE_CXX_FLAGS=-Werror -DBUILD_SHARED_LIBS=ON \
    && cmake --build build \
    && cmake --install build

# Load shared library.
RUN ldconfig /usr/local/lib/libsimdutf.so


# Set up turbodbc.
FROM arrow-simdutf AS turbodbc

# Configure Python environment.
ENV PIP_ROOT_USER_ACTION=ignore
ENV PIP_BREAK_SYSTEM_PACKAGES=true
ENV UV_BREAK_SYSTEM_PACKAGES=true
ENV UV_COMPILE_BYTECODE=true
ENV UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=never
ENV UV_SYSTEM_PYTHON=true

# Install NumPy, PyArrow, and turbodbc.
ADD requirements*.txt .
RUN \
    --mount=type=cache,id=user-cache,target=/root/.cache \
    true \
    && pip install uv \
    && uv pip install --upgrade --requirement=requirements-prereq.txt --verbose \
    && export WORKERS=$(bc -e "$(nproc) / 2") \
    && MAKEFLAGS="-j${WORKERS}" uv pip install --upgrade --requirement=requirements.txt --verbose


FROM turbodbc
