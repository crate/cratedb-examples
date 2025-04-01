# Set up Arch Linux.
FROM archlinux:base AS build

# Permit building packages using `makepkg` or `yay` within Docker container.
# https://blog.ganssle.io/tag/arch-linux.html
RUN pacman -Sy --noconfirm --needed base-devel bc binutils fakeroot git sudo
RUN useradd --create-home build
RUN echo 'build ALL=NOPASSWD: ALL' >> /etc/sudoers

# Install `yay` for easily installing AUR packages.
# https://aur.archlinux.org/packages/yay
RUN mkdir /yay-bin; chmod ugo+rwX /yay-bin
RUN true \
    && git clone https://aur.archlinux.org/yay-bin.git \
    && cd yay-bin \
    && sudo --user=build -- makepkg -si --noconfirm

RUN pacman -Sy --noconfirm --needed \
    boost pybind11 python-pip python-setuptools python-wheel uv


# Set up ODBC.
FROM build AS odbc

# Install unixODBC and the PostgreSQL ODBC driver.
# https://archlinux.org/packages/core/x86_64/unixodbc/
# https://aur.archlinux.org/packages/psqlodbc
RUN pacman -Sy --noconfirm --needed \
    unixodbc
RUN sudo --user=build -- yay -S --noconfirm --needed \
    psqlodbc


# Apache Arrow and simdutf.
FROM odbc AS arrow-simdutf

# Install Apache Arrow, NumPy, PyArrow.
RUN pacman -Sy --noconfirm --needed \
    arrow python-numpy python-pyarrow

# Install ultra-fast Unicode routines.
# https://github.com/simdutf/simdutf
RUN sudo --user=build -- yay -S --noconfirm --needed \
    simdutf-git


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

# Install turbodbc.
ADD requirements*.txt .
RUN \
    --mount=type=cache,id=user-cache,target=/root/.cache \
    true \
    && export WORKERS=$(bc -e "$(nproc) / 2") \
    && MAKEFLAGS="-j${WORKERS}" uv pip install --upgrade --requirement=requirements.txt --verbose


FROM turbodbc
