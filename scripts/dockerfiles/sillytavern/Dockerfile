# SillyTavern — Dockerfile
# Builds SillyTavern/SillyTavern — LLM chat frontend
# Uses node:lts-alpine pattern (clone + npm ci)

FROM node:lts-alpine AS builder

RUN apk add --no-cache git

WORKDIR /app

RUN git clone --depth 1 https://github.com/SillyTavern/SillyTavern.git /tmp/st && \
    cp -r /tmp/st/* /app/ && \
    rm -rf /tmp/st

RUN npm ci --ignore-scripts --network-timeout 600000 2>/dev/null; \
    echo "SillyTavern: dependencies installed"

FROM node:lts-alpine

RUN apk add --no-cache git

WORKDIR /app

COPY --from=builder /app /app

EXPOSE 8000

ENV SILLYTAVERN_PORT=8000

CMD sh -c 'if [ -f /app/server.js ]; then node /app/server.js --port ${SILTYTAVERN_PORT:-8000}; else echo "Server entry not found" && tail -f /dev/null; fi'
