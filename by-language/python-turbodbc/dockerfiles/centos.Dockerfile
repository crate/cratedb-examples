FROM quay.io/centos/centos:stream9

# Install Python, unixODBC, the PostgreSQL ODBC driver, and development libraries.
RUN dnf install --enablerepo=crb -y boost-devel g++ postgresql-odbc python3 python3-devel python3-pip unixODBC-devel

# Install Python, NumPy, PyArrow, and turbodbc.
ADD requirements*.txt .
RUN pip install --upgrade --requirement=requirements-prereq.txt
RUN MAKEFLAGS="-j$(nproc)" pip install --upgrade --requirement=requirements.txt --verbose
