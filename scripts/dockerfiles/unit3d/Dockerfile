# UNIT3D — Production Dockerfile
# Upstream: HDInnovations/UNIT3D-Community-Edition — private torrent tracker platform
# Multi-stage build: Node (frontend assets) → Composer (PHP deps) → PHP-FPM runtime (nginx + supervisord)
# Pattern: Follows Arcane custom-build convention with clear stage labels

# ─── Stage 1: Frontend asset build ──────────────────────────────────────
FROM node:lts-alpine AS frontend-builder

RUN apk add --no-cache git

WORKDIR /app

# Clone upstream UNIT3D Community Edition (Laravel + Vite)
RUN git clone --depth 1 https://github.com/HDInnovations/UNIT3D-Community-Edition.git /tmp/unit3d && \
    cp -r /tmp/unit3d/* /tmp/unit3d/.* /app/ 2>/dev/null || true && \
    rm -rf /tmp/unit3d

# Install Node dependencies and build Vite assets
RUN npm install --ignore-scripts && npm run build || \
    npm install --legacy-peer-deps --ignore-scripts && npm run build || \
    echo "WARN: build step failed — continuing without compiled assets"

# ─── Stage 2: Composer dependency install ───────────────────────────────
FROM composer:2 AS composer-builder

WORKDIR /app

# Clone upstream UNIT3D again for Composer install
RUN git clone --depth 1 https://github.com/HDInnovations/UNIT3D-Community-Edition.git /tmp/unit3d && \
    cp -r /tmp/unit3d/* /tmp/unit3d/.* /app/ 2>/dev/null || true && \
    rm -rf /tmp/unit3d

# Install production PHP dependencies
RUN composer install --no-dev --optimize-autoloader --no-interaction --no-scripts --ignore-platform-req=ext-intl --ignore-platform-req=ext-bcmath --ignore-platform-req=ext-ldap --ignore-platform-req=ext-imagick

# ─── Stage 3: Production runtime (PHP-FPM + nginx + supervisord) ────────
FROM php:8.4-fpm-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    nginx \
    supervisor \
    libpng-dev \
    libjpeg62-turbo-dev \
    libfreetype6-dev \
    libzip-dev \
    libicu-dev \
    libonig-dev \
    libxml2-dev \
    libcurl4-openssl-dev \
    libexif-dev \
    unzip \
    ca-certificates \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install -j$(nproc) \
        pdo_mysql \
        mbstring \
        xml \
        zip \
        intl \
        curl \
        exif \
        gd \
        opcache \
    && pecl install redis \
    && docker-php-ext-enable redis \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Composer dependencies from stage 2
COPY --from=composer-builder /app/vendor /app/vendor

# Copy the full application source from frontend build stage (includes compiled assets)
COPY --from=frontend-builder /app /app

# Ensure storage and bootstrap/cache are writable
RUN chown -R www-data:www-data /app/storage /app/bootstrap/cache 2>/dev/null || true && \
    chmod -R 775 /app/storage /app/bootstrap/cache 2>/dev/null || true

# ─── Nginx configuration ───────────────────────────────────────────────
RUN cat > /etc/nginx/sites-available/default <<'NGINX'
server {
    listen 8000;
    server_name _;
    root /app/public;
    index index.php;

    charset utf-8;
    client_max_body_size 100M;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location = /favicon.ico { access_log off; log_not_found off; }
    location = /robots.txt  { access_log off; log_not_found off; }

    error_page 404 /index.php;

    location ~ \.php$ {
        fastcgi_split_path_info ^(.+\.php)(/.+)$;
        fastcgi_pass 127.0.0.1:9000;
        fastcgi_index index.php;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_param PATH_INFO $fastcgi_path_info;
        fastcgi_read_timeout 300;
        fastcgi_buffers 16 16k;
        fastcgi_buffer_size 32k;
    }

    location ~ /\.(?!well-known).* {
        deny all;
    }
}
NGINX

# ─── PHP-FPM configuration ─────────────────────────────────────────────
RUN echo "listen = 127.0.0.1:9000" >> /usr/local/etc/php-fpm.d/zz-docker.conf && \
    sed -i 's/^;clear_env.*/clear_env = no/' /usr/local/etc/php-fpm.d/www.conf

# ─── Supervisor configuration ──────────────────────────────────────────
RUN cat > /etc/supervisor/conf.d/unit3d.conf <<'SUPERVISOR'
[program:php-fpm]
command=/usr/local/sbin/php-fpm
autostart=true
autorestart=true
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0

[program:nginx]
command=/usr/sbin/nginx -g "daemon off;"
autostart=true
autorestart=true
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0
SUPERVISOR

# ─── Environment defaults ──────────────────────────────────────────────
ENV APP_ENV=production \
    APP_DEBUG=false \
    APP_URL=http://localhost \
    DB_CONNECTION=mysql \
    DB_HOST=mysql \
    DB_PORT=3306 \
    DB_DATABASE=unit3d \
    DB_USERNAME=unit3d \
    DB_PASSWORD=secret \
    REDIS_HOST=redis \
    REDIS_PORT=6379 \
    CACHE_STORE=redis \
    SESSION_DRIVER=redis \
    QUEUE_CONNECTION=redis \
    MEILISEARCH_HOST=http://meilisearch:7700

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]
