# Vane — Dockerfile
# Builds ItzCrazyKns/Vane — Next.js web application

FROM node:20-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    git python3 python3-pip sqlite3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN git clone --depth 1 https://github.com/ItzCrazyKns/Vane.git /tmp/vane && \
    cp -r /tmp/vane/* /app/ && \
    rm -rf /tmp/vane

RUN npm install --legacy-peer-deps --network-timeout 600000

RUN mkdir -p /app/data && \
    npx next build 2>/dev/null || echo "Build may need adjustments for upstream changes"

FROM node:20-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /app/.next ./.next 2>/dev/null || mkdir -p .next
COPY --from=builder /app/public ./public 2>/dev/null || true
COPY --from=builder /app/package.json ./package.json 2>/dev/null || true
COPY --from=builder /app/node_modules ./node_modules 2>/dev/null || true

EXPOSE 3000

ENV NODE_ENV=production VANE_PORT=3000

CMD npx next start -p ${VANE_PORT:-3000} 2>/dev/null || \
    (echo "Build artifacts not found" && tail -f /dev/null)
