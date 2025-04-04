# Set up Red Hat / CentOS / Alma Linux.
FROM quay.io/centos/centos:stream9 AS build
#FROM quay.io/centos/centos:stream10 AS build
#FROM almalinux:9.5 AS build

# Provide additional package repositories.
RUN dnf install -y epel-release || sudo dnf install -y oracle-epel-release-el$(cut -d: -f5 /etc/system-release-cpe | cut -d. -f1) || sudo dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-$(cut -d: -f5 /etc/system-release-cpe | cut -d. -f1).noarch.rpm
RUN dnf config-manager --set-enabled epel || :
RUN dnf config-manager --set-enabled powertools || :
RUN dnf config-manager --set-enabled crb || :
RUN dnf config-manager --set-enabled ol$(cut -d: -f5 /etc/system-release-cpe | cut -d. -f1)_codeready_builder || :
RUN dnf config-manager --set-enabled codeready-builder-for-rhel-$(cut -d: -f5 /etc/system-release-cpe | cut -d. -f1)-rhui-rpms || :
RUN subscription-manager repos --enable codeready-builder-for-rhel-$(cut -d: -f5 /etc/system-release-cpe | cut -d. -f1)-$(arch)-rpms || :

# Install recent Python and development libraries.
RUN dnf install -y \
    bc boost-devel g++ git python3.12-devel python3.12-pip python3.12-pybind11

# Make recent Python version the default.
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.12 0
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 0
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3.12 0
RUN update-alternatives --install /usr/bin/pip3 pip3 /usr/bin/pip3.12 0


# Set up ODBC.
FROM build AS odbc

# Install unixODBC and the PostgreSQL ODBC driver.
RUN dnf install -y \
    postgresql-odbc unixODBC-devel


# Apache Arrow and simdutf.
FROM odbc AS arrow-simdutf

# Install Apache Arrow.
# https://arrow.apache.org/install/
RUN dnf install -y https://apache.jfrog.io/artifactory/arrow/almalinux/$(cut -d: -f5 /etc/system-release-cpe | cut -d. -f1)/apache-arrow-release-latest.rpm
RUN dnf install -y \
    arrow-devel arrow-dataset-devel arrow-flight-devel arrow-flight-sql-devel parquet-devel

# Install ultra-fast Unicode routines.
# https://github.com/simdutf/simdutf
RUN true \
    && git clone https://github.com/simdutf/simdutf --branch=v6.4.0 \
    && cd simdutf \
    && cmake -B build -DCMAKE_CXX_FLAGS=-Werror -DBUILD_SHARED_LIBS=ON \
    && cmake --build build \
    && cmake --install build


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
