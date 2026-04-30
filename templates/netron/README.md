# Netron

> **Status: Desktop App — Sandbox Only**
> Netron is an Electron desktop application for visualizing neural network models. No Docker image exists for it. This template provides a documentation/sandbox container. Use `npx netron model.onnx` or visit [netron.app](https://netron.app) for real use.

[Netron](https://github.com/lutzroeder/netron) — Model visualization tool for neural networks, machine learning, and AI models

## Quick Start

1. **Copy the environment file:**

   ```bash
   cp .env.example .env
   ```

2. **Start the service:**

   ```bash
   docker compose up -d
   ```

3. **Access the service:**

   Open [http://localhost:8080](http://localhost:8080) in your browser.

## Configuration

Copy `.env.example` to `.env` and edit the values as needed.

## Service Details

The docker-compose.yml exposes environment variables documented in `.env.example`.
