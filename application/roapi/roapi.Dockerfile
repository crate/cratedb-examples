# Temporarily build ROAPI for CrateDB, until an obligatory
# improvement is included into an official release.
# https://github.com/roapi/roapi/pull/416

# Source: https://github.com/roapi/roapi/blob/main/Dockerfile

ARG RUST_VER=1.86.0-bookworm

FROM rust:${RUST_VER} AS foundation

RUN curl -L --proto '=https' --tlsv1.2 -sSf https://raw.githubusercontent.com/cargo-bins/cargo-binstall/main/install-from-binstall-release.sh | bash
RUN cargo binstall trunk

# Add WebAssembly target for UI build.
RUN rustup target add wasm32-unknown-unknown

# Install cmake for snmalloc.
RUN apt-get update \
    && apt-get install --no-install-recommends -y cmake

FROM foundation AS builder

RUN cargo install --locked --git https://github.com/roapi/roapi.git --rev 4d649d78 --jobs default --bins roapi --features database
RUN cargo install --list

# Assemble the final image
FROM debian:bookworm-slim
LABEL org.opencontainers.image.source=https://github.com/roapi/roapi

RUN apt-get update \
    && apt-get install -y libssl-dev ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Use `roapi` program from custom build.
COPY --from=builder /usr/local/cargo/bin/roapi /usr/local/bin/roapi

# Use test data from vanilla image.
COPY --from=ghcr.io/roapi/roapi:latest /test_data /test_data

EXPOSE 8080
ENTRYPOINT ["roapi"]
