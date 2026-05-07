# WGCloud — Dockerfile
# Builds tianshiyeben/wgcloud — Java Spring Boot distributed monitoring
# 2-stage: Maven build + slim JRE runtime with FastAPI wrapper

# ── Stage 1: Build Spring Boot JAR with Maven ────────────────────
FROM maven:3.9-eclipse-temurin AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Clone upstream WGCloud source
RUN git clone --depth 1 https://github.com/tianshiyeben/wgcloud.git /tmp/wgcloud && \
    cp -r /tmp/wgcloud/* /build/ && \
    rm -rf /tmp/wgcloud

# Build the server module with Maven (skip tests for speed)
RUN cd /build/wgcloud-server && \
    mvn clean package -DskipTests -q && \
    cp target/wgcloud-server-*.jar /build/wgcloud-server-release.jar

# ── Stage 2: Production image ────────────────────────────────────
FROM eclipse-temurin:11

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    curl \
    && pip3 install --break-system-packages --no-cache-dir fastapi uvicorn \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy JAR and SQL schema from builder
COPY --from=builder /build/wgcloud-server-release.jar /app/wgcloud-server-release.jar
COPY --from=builder /build/sql/wgcloud.sql /app/wgcloud.sql
COPY scripts/dockerfiles/wgcloud/server.py /app/server.py

EXPOSE 9999

ENV WGCLOUD_PORT=9999

ENTRYPOINT ["python3", "/app/server.py"]
