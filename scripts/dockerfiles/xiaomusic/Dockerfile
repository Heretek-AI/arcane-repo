# Xiaomusic — Dockerfile
# Builds xiaomusic (hanxi/xiaomusic) — Xiaomi smart speaker music player with LLM integration
# Multi-arch: amd64 + arm64 (Alpine), armv7 (Debian)

FROM python:3.12-alpine

RUN apk add --no-cache \
    build-base \
    nodejs \
    npm \
    ffmpeg \
    zlib-dev \
    jpeg-dev \
    freetype-dev \
    lcms2-dev \
    openjpeg-dev \
    tiff-dev \
    libwebp-dev

RUN pip install --no-cache-dir pdm fastapi uvicorn
ENV PDM_CHECK_UPDATE=false

WORKDIR /app

RUN git clone --depth 1 https://github.com/hanxi/xiaomusic.git /app/src

WORKDIR /app/src

RUN pdm install --prod --no-editable -v && \
    npm install

# Build FFmpeg compatibility symlinks
RUN mkdir -p /app/ffmpeg/bin && \
    ln -s $(which ffmpeg) /app/ffmpeg/bin/ffmpeg && \
    ln -s $(which ffprobe) /app/ffmpeg/bin/ffprobe && \
    touch /app/.dockerenv

EXPOSE 8090 8091

ENV TZ=Asia/Shanghai
ENV PATH="/app/src/.venv/bin:/usr/local/bin:${PATH}"

COPY scripts/dockerfiles/xiaomusic/server.py /app/server.py

CMD /app/src/.venv/bin/python3 /app/src/xiaomusic.py & \
    /usr/local/bin/python3 /app/server.py & \
    wait -n
