# Uncloud — Dockerfile
# Builds psviderski/uncloud — lightweight container orchestration with WireGuard mesh
# Multi-stage: Go binary (uncloudd) + Rust binary (corrosion) on alpine runtime
# Adapted from upstream Dockerfile: https://github.com/psviderski/uncloud

# ── Stage 1: Build Go daemon (uncloudd) ──────────────────────────
FROM golang:1.26-alpine AS uncloudd

ENV CGO_ENABLED=0

RUN apk add --no-cache git

WORKDIR /build

# Clone upstream uncloud source
RUN git clone --depth 1 https://github.com/psviderski/uncloud.git /tmp/uncloud && \
    cp -r /tmp/uncloud/* /build/ && \
    rm -rf /tmp/uncloud

RUN go mod download && go mod verify
RUN go build -o uncloudd ./cmd/uncloudd

# ── Stage 2: Download corrosion WireGuard agent ──────────────────
FROM alpine:3.23 AS corrosion-download

RUN ARCH=$(uname -m) && \
    CORROSION_ARCH=$(case "$ARCH" in \
      "x86_64") echo "x86_64" ;; \
      "aarch64") echo "aarch64" ;; \
      *) echo "Architecture '$ARCH' not supported" >&2 && exit 1 ;; \
    esac) \
    && wget -q -O /tmp/corrosion.tar.gz \
      "https://github.com/psviderski/corrosion/releases/latest/download/corrosion-${CORROSION_ARCH}-unknown-linux-gnu.tar.gz" \
    && tar -xzf /tmp/corrosion.tar.gz -C /tmp \
    && install /tmp/corrosion /usr/local/bin/corrosion \
    && rm /tmp/corrosion.tar.gz /tmp/corrosion

# ── Stage 3: Production image ────────────────────────────────────
FROM alpine:3.23

RUN apk add --no-cache \
    python3 \
    py3-pip \
    wireguard-tools \
    libcap \
    && pip3 install --break-system-packages --no-cache-dir fastapi uvicorn

RUN addgroup -S uncloud && adduser -SHD -h /nonexistent -G uncloud -g "" uncloud

WORKDIR /app

COPY --from=uncloudd /build/uncloudd /usr/local/bin/uncloudd
COPY --from=corrosion-download /usr/local/bin/corrosion /usr/local/bin/corrosion
COPY scripts/dockerfiles/uncloud/server.py /app/server.py

EXPOSE 8000

ENV UNCLOUD_PORT=8000

ENTRYPOINT ["python3", "/app/server.py"]
