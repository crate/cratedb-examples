# ---------------------------
# Setup archlinux environment
# ---------------------------

# Include `yay` for easily installing AUR packages.

FROM archlinux:base-20230205.0.123931 as archlinux-build

# Allow building packages using `makepkg` within Docker container.
# https://blog.ganssle.io/tag/arch-linux.html
RUN pacman -Sy --noconfirm --needed base-devel binutils fakeroot git sudo
RUN useradd --create-home build
RUN echo 'build ALL=NOPASSWD: ALL' >> /etc/sudoers

# Install AUR package helper program `yay`.
# https://aur.archlinux.org/packages/yay
RUN mkdir /yay-bin; chmod ugo+rwX /yay-bin
USER build
RUN \
    git clone https://aur.archlinux.org/yay-bin.git && \
    cd yay-bin && \
    makepkg -si --noconfirm
USER root


# --------------------------
# Setup turbodbc environment
# --------------------------

# Install Python, unixODBC, PostgreSQL ODBC driver, and turbodbc.

FROM archlinux-build

# Install unixODBC.
# https://archlinux.org/packages/core/x86_64/unixodbc/
RUN pacman -Sy --noconfirm --needed unixodbc

# Install PostgreSQL ODBC driver.
# https://aur.archlinux.org/packages/psqlodbc
USER build
RUN yay -S --noconfirm psqlodbc
USER root

# Install NumPy, PyArrow, and turbodbc.
RUN pacman -Sy --noconfirm --needed boost python python-pip python-setuptools
ADD requirements*.txt .
RUN pip install --upgrade --requirement=requirements-prereq.txt
RUN MAKEFLAGS="-j$(nproc)" pip install --upgrade --requirement=requirements.txt --verbose
