# AionUi — Dockerfile
# Builds iOfficeAI/AionUi — AI-native UI framework
# Uses node:20-slim + bun multi-stage pattern (clone + install + build)

FROM node:20-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    git ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install bun
RUN npm install -g bun

WORKDIR /app

# Clone upstream AionUi (shallow clone, depth 1)
RUN git clone --depth 1 https://github.com/iOfficeAI/AionUi.git /tmp/aionui \
    && cp -r /tmp/aionui/. . \
    && rm -rf /tmp/aionui

# Install all dependencies (including devDeps for build)
# Note: package.json and bun.lock come from cloned source
RUN bun install --ignore-scripts

# Build renderer (web) and server bundle
RUN bun run build:renderer:web \
    && node scripts/build-server.mjs

# ---- Runtime image ----
FROM oven/bun:latest AS runtime

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy build artifacts from builder stage
COPY --from=builder /app/dist-server ./dist-server
COPY --from=builder /app/out/renderer ./out/renderer
COPY --from=builder /app/package.json ./

# Production dependencies only
RUN bun install --production --ignore-scripts

ENV PORT=3000
ENV NODE_ENV=production
ENV ALLOW_REMOTE=true
ENV DATA_DIR=/data

VOLUME ["/data"]
EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:${PORT:-3000}/health || exit 1

CMD ["bun", "dist-server/server.mjs"]
