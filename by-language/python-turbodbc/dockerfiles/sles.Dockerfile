FROM registry.suse.com/suse/sle15

# Add package repository for acquiring `boost-devel`.
# https://software.opensuse.org//download.html?project=home%3Afsirl%3Aboost1651&package=boost
RUN zypper addrepo https://download.opensuse.org/repositories/home:fsirl:boost1651/15.4/home:fsirl:boost1651.repo

# Add package repository for acquiring `python310`.
# https://download.opensuse.org/repositories/devel:/languages:/python:/backports/15.4/
RUN zypper addrepo https://download.opensuse.org/repositories/devel:/languages:/python:/backports/15.4/devel:languages:python:backports.repo

# Activate package repositories.
RUN zypper --gpg-auto-import-keys refresh

# Install Python, unixODBC, the PostgreSQL ODBC driver, and development libraries.
RUN zypper install -y boost-devel gcc-c++ psqlODBC python310 python310-devel python310-pip unixODBC-devel update-alternatives

# Make Python 3.10 the default Python 3, and add an alias `python3`.
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 0
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 0

# Install Python, NumPy, PyArrow, and turbodbc.
ADD requirements*.txt .
RUN pip install --upgrade --requirement=requirements-prereq.txt
RUN MAKEFLAGS="-j$(nproc)" pip install --upgrade --requirement=requirements.txt --verbose
