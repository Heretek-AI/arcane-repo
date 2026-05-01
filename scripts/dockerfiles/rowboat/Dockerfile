# Rowboat — Multi-service AI coworker platform (Next.js)
# Upstream: rowboatlabs/rowboat (13.2k★) — open-source AI coworker with knowledge graph
# Builds the main Rowboat Next.js app from upstream source.
# The upstream agents/copilot services no longer exist on main branch — now built into the main app.
#
# Pattern: node-alpine multi-stage build (MEM036) — Node/Next.js projects
# Clone upstream source at build time → npm ci → next build → standalone production image

FROM node:18-alpine AS deps

RUN apk add --no-cache libc6-compat git
WORKDIR /build

# Clone upstream Rowboat at latest main
RUN git clone --depth 1 https://github.com/rowboatlabs/rowboat.git /tmp/rowboat && \
    cp -r /tmp/rowboat/apps/rowboat/* /build/ && \
    cp /tmp/rowboat/apps/rowboat/.npmrc /build/ 2>/dev/null || true && \
    cp /tmp/rowboat/apps/rowboat/.env.example /build/ 2>/dev/null || true && \
    rm -rf /tmp/rowboat

# Install dependencies
RUN npm ci

# ─── Build ─────────────────────────────────────────────────────────────
FROM deps AS builder

COPY --from=deps /build /app
WORKDIR /app

RUN npm run build

# ─── Production runtime ────────────────────────────────────────────────
FROM node:18-alpine AS runner

RUN apk add --no-cache curl

WORKDIR /app

ENV NODE_ENV=production

RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Copy standalone output + static files from Next.js build
COPY --from=builder --chown=nextjs:nodejs /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# Copy our FastAPI wrapper + health check helper
COPY scripts/dockerfiles/rowboat/server.py /app/server.py

# Install Python & FastAPI for the wrapper server
RUN apk add --no-cache python3 py3-pip && \
    pip3 install --no-cache-dir --break-system-packages fastapi uvicorn

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME=0.0.0.0

HEALTHCHECK --interval=30s --timeout=5s --retries=3 --start-period=60s \
    CMD curl -f http://localhost:3000/api/docs 2>/dev/null || curl -f http://localhost:${PORT:-3000}/ || exit 1

CMD ["python3", "/app/server.py"]
