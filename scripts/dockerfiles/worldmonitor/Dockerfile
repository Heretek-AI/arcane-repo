# World Monitor — Dockerfile
# Builds koala73/worldmonitor — monitoring dashboard

FROM node:22-alpine AS builder

RUN apk add --no-cache git

WORKDIR /app

RUN git clone --depth 1 https://github.com/koala73/worldmonitor.git /tmp/wm && \
    cp -r /tmp/wm/* /app/ && \
    rm -rf /tmp/wm

RUN npm ci --ignore-scripts 2>/dev/null; \
    npm run build 2>/dev/null || echo "Upstream build requires manual configuration"

FROM nginx:alpine

RUN apk add --no-cache nodejs npm

WORKDIR /app

COPY --from=builder /app /app

EXPOSE 80

CMD sh -c 'if [ -f /app/dist/index.html ]; then cp -r /app/dist/* /usr/share/nginx/html/ && nginx -g "daemon off;"; else echo "Static build not found" && tail -f /dev/null; fi'
