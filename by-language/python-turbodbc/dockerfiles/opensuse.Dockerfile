# Set up openSUSE Linux with ODBC.
FROM registry.opensuse.org/opensuse/tumbleweed:20250329 AS build
#FROM registry.suse.com/suse/sle15 AS build

# Activate package repositories.
RUN zypper --gpg-auto-import-keys refresh

# Install Python and development libraries.
RUN zypper install -y \
    bc cmake git gcc-c++ \
    python313-devel python313-pip python313-pybind11 \
    update-alternatives uv

# Make recent Python version the default.
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.13 0
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.13 0
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3.13 0
RUN update-alternatives --install /usr/bin/pip3 pip3 /usr/bin/pip3.13 0


# Set up ODBC.
FROM build AS odbc

# Install unixODBC and the PostgreSQL ODBC driver.
RUN zypper install -y \
    psqlODBC unixODBC-devel


# Apache Arrow and simdutf.
FROM odbc AS arrow-simdutf

# Provide Apache Arrow by activating "scientific" package bundle.
# https://software.opensuse.org/download/package?package=apache-arrow&project=science
RUN zypper addrepo https://download.opensuse.org/repositories/science/openSUSE_Tumbleweed/science.repo
RUN zypper --gpg-auto-import-keys refresh

# Install Apache Arrow.
# https://arrow.apache.org/install/
RUN zypper install -y \
    apache-arrow

# Install ultra-fast Unicode routines.
RUN true \
    && git clone https://github.com/simdutf/simdutf --branch=v6.4.0 \
    && cd simdutf \
    && cmake -B build -DCMAKE_CXX_FLAGS=-Werror -DBUILD_SHARED_LIBS=ON \
    && cmake --build build \
    && cmake --install build

# Load shared library.
RUN ldconfig /usr/local/lib64/libsimdutf.so


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
    && uv pip install --upgrade --requirement=requirements-prereq.txt --verbose \
    && export WORKERS=$(bc -e "$(nproc) / 2") \
    && MAKEFLAGS="-j${WORKERS}" uv pip install --upgrade --requirement=requirements.txt --verbose
