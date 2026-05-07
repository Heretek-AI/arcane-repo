# Sunshine — Dockerfile
# Builds LizardByte/Sunshine (36k★) — self-hosted game stream host for Moonlight
# Multi-stage: builds Sunshine from source on ubuntu:22.04, installs .deb into runtime,
# wraps with FastAPI server exposing /health and /info endpoints.

# ── Stage 1: Build Sunshine from source ─────────────────────────────

FROM ubuntu:22.04 AS builder

ENV DEBIAN_FRONTEND=noninteractive
ENV MAKEFLAGS="-j2"

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt-get update && apt-get install -y --no-install-recommends \
    git cmake g++ \
    libavdevice-dev libboost-thread-dev libboost-filesystem-dev \
    libboost-log-dev libpulse-dev libopus-dev libevdev-dev \
    libxtst-dev libx11-dev libxfixes-dev libxrandr-dev \
    libdrm-dev libva-dev libvdpau-dev libssl-dev \
    libcurl4-openssl-dev libgl1-mesa-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build/sunshine

RUN git clone --depth 1 --branch v2025.924.154138 https://github.com/LizardByte/Sunshine.git . \
    && chmod +x scripts/linux_build.sh

# Install gcc-13 toolchain via ubuntu-toolchain-r/test PPA (Sunshine build dependencies)
# Separate the PPA addition and gcc install to avoid layer-cache issues on constrained runners
RUN apt-get update && apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:ubuntu-toolchain-r/test && \
    apt-get update && apt-get install -y --no-install-recommends gcc-13 g++-13 && \
    rm -rf /var/lib/apt/lists/*

# Build deps, cmake, build, and package
# Set MAKEFLAGS to limit parallelism and avoid OOM on constrained runners
ENV MAKEFLAGS="-j2"
# Tee build output to /tmp so cmake errors survive the artifact capture
RUN ./scripts/linux_build.sh \
        --sudo-off \
        --publisher-name='LizardByte' \
        --publisher-website='https://app.lizardbyte.dev' \
        --publisher-issue-url='https://app.lizardbyte.dev/support' \
        2>&1 | tee /tmp/build.log; \
    test "${PIPESTATUS[0]}" -eq 0 || { \
        echo "=== BUILD FAILED — dumping /tmp/build.log ==="; \
        cat /tmp/build.log; \
        exit 1; \
    }

# ── Stage 2: Runtime with FastAPI wrapper ──────────────────────────

FROM ubuntu:22.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install the Sunshine .deb from the builder
COPY --from=builder /build/sunshine/build/cpack_artifacts/Sunshine.deb /tmp/sunshine.deb
RUN apt-get update && apt-get install -y --no-install-recommends /tmp/sunshine.deb \
    && rm -f /tmp/sunshine.deb \
    && rm -rf /var/lib/apt/lists/*

# Install FastAPI for the health/info wrapper
RUN pip3 install --no-cache-dir fastapi uvicorn

# Expose Sunshine ports (health wrapper on 47991, web UI on 47990, main service ports)
EXPOSE 47991/tcp
EXPOSE 47984-47990/tcp
EXPOSE 48010/tcp
EXPOSE 47998-48000/udp

ARG PUID=1000
ENV PUID=${PUID}
ARG PGID=1000
ENV PGID=${PGID}
ENV TZ="UTC"
ARG UNAME=sunshine
ENV UNAME=${UNAME}

ENV HOME=/home/${UNAME}

RUN groupadd -f -g "${PGID}" "${UNAME}" \
    && useradd -lm -d ${HOME} -s /bin/bash -g "${PGID}" -u "${PUID}" "${UNAME}" \
    && mkdir -p ${HOME}/.config/sunshine \
    && ln -s ${HOME}/.config/sunshine /config \
    && chown -R ${UNAME}:${UNAME} ${HOME}

COPY scripts/dockerfiles/sunshine/server.py /app/server.py

WORKDIR /app

CMD python3 /app/server.py
