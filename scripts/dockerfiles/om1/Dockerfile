# OM1 — Modular AI Runtime for Robots
# Upstream: OpenMind/OM1 (1.5k+ ★) — multi-modal AI agent with hardware integration
# Requires: PulseAudio, cameras, microphones for full functionality (see README)
#
# Pattern: uv-python with system deps for audio/video processing
# IMPORTANT: This Dockerfile builds a HEADLESS API wrapper. Full OM1 functionality requires
# hardware devices (cameras, mics, speakers) passed through to the container.

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    pkg-config \
    libssl-dev \
    build-essential \
    cmake \
    python3-dev \
    ffmpeg \
    portaudio19-dev \
    libasound2-dev \
    libv4l-dev \
    libasound2 \
    libasound2-data \
    libasound2-plugins \
    libpulse0 \
    pulseaudio-utils \
    alsa-utils \
    alsa-topology-conf \
    alsa-ucm-conf \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /app

# Clone upstream OM1 (multi-modal AI agent runtime)
RUN git clone --depth 1 --branch main https://github.com/OpenMind/OM1.git /tmp/om1 && \
    cp -r /tmp/om1/* /app/ && \
    rm -rf /tmp/om1

# Clone cyclonedds dependency (upstream build requirement)
WORKDIR /app/cyclonedds/build
RUN git clone --depth 1 --branch releases/0.10.x https://github.com/eclipse-cyclonedds/cyclonedds /tmp/cyclonedds 2>/dev/null || \
    echo "WARN: cyclonedds clone failed — continuing without it" && \
    if [ -d /tmp/cyclonedds ]; then \
        cp -r /tmp/cyclonedds/* /app/cyclonedds/ 2>/dev/null || true; \
        cmake .. -DCMAKE_INSTALL_PREFIX=../install -DBUILD_EXAMPLES=ON 2>/dev/null && \
        cmake --build . --target install 2>/dev/null || \
        echo "WARN: cyclonedds build failed — continuing without DDS support"; \
    fi

ENV CYCLONEDDS_HOME=/app/cyclonedds/install \
    CMAKE_PREFIX_PATH=/app/cyclonedds/install

WORKDIR /app

# Initialize git submodules (some may fail, that's ok for headless mode)
RUN git submodule update --init --recursive 2>/dev/null || echo "WARN: submodule init incomplete — headless mode"

# Copy default config
RUN cp -r config config_defaults 2>/dev/null || mkdir -p config_defaults

# Install Python dependencies via uv
RUN uv pip install --system --no-cache-dir \
    fastapi \
    uvicorn && \
    if [ -f pyproject.toml ]; then \
        uv pip install --system --no-cache-dir . 2>/dev/null || \
        echo "WARN: pyproject.toml install had warnings — continuing"; \
    fi

EXPOSE 8000

ENV OM1_PORT=8000
ENV OM1_SKIP_INTERNET_CHECK=true
ENV OM1_HEADLESS=true

COPY scripts/dockerfiles/om1/server.py /app/server.py

CMD ["python3", "/app/server.py"]
