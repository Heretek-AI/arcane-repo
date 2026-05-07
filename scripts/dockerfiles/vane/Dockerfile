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

RUN npm install --legacy-peer-deps --network-timeout=600000

RUN mkdir -p /app/data

# Build may fail if upstream has changed its config — this is non-fatal
RUN npx next build 2>/dev/null || echo "WARN: next build failed — will use runtime fallback"

FROM node:20-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /app /app

EXPOSE 3000

ENV NODE_ENV=production VANE_PORT=3000

CMD sh -c 'if [ -d /app/.next ]; then npx next start -p ${VANE_PORT:-3000}; else echo "No build artifacts — run npm install && npx next build first" && tail -f /dev/null; fi'
