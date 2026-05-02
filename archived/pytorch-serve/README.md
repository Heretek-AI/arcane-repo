# PyTorch Serve — Production Model Serving

[TorchServe](https://github.com/pytorch/serve) is PyTorch's official model serving framework — deploy trained PyTorch models as production-ready REST APIs with built-in management, logging, and metrics.

## Quick Start

1. **Start the server:**

   ```bash
   docker compose up -d
   ```

2. **Check server health:**

   ```bash
   curl http://localhost:8080/ping
   ```

3. **Register a model archive** (`.mar` file):

   ```bash
   curl -X POST "http://localhost:8081/models?url=YOUR_MODEL.mar&model_name=my_model"
   ```

4. **Run inference:**

   ```bash
   curl http://localhost:8080/predictions/my_model \
     -H "Content-Type: application/json" \
     -d '{"input": "your tensor or data here"}'
   ```

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable                      | Default | Description                                    |
|-------------------------------|---------|------------------------------------------------|
| `TORCHSERVE_INFERENCE_PORT`   | `8080`  | Host port for inference (prediction) API       |
| `TORCHSERVE_MANAGEMENT_PORT`  | `8081`  | Host port for management API                   |
| `TORCHSERVE_MODELS`           | `all`   | Models to load on startup (comma-separated)    |
| `TS_SERVICE_ENVELOPE`         | `body`  | Envelope format for pre/post-processing        |

## Creating Model Archives

Package your trained PyTorch model into a `.mar` file:

```bash
docker compose exec pytorch-serve torch-model-archiver \
  --model-name my_model \
  --version 1.0 \
  --serialized-file /home/model-server/models/model.pt \
  --export-path /home/model-server/model-store \
  --handler my_handler.py
```

## API Endpoints

| Endpoint                  | Method | Description                           |
|---------------------------|--------|---------------------------------------|
| `/ping`                   | GET    | Health check                          |
| `/predictions/{model}`    | POST   | Run inference on a model              |
| `/models`                 | GET    | List registered models                |
| `/models`                 | POST   | Register a new model (management API) |
| `/models/{model}`         | DELETE | Unregister a model (management API)   |

## Model Store

Place `.mar` model archives in the `pytorch_serve_model_store` volume. They are automatically available for registration. Raw model files (`.pt`, `.pth`) go in `pytorch_serve_models`.

## Health Check

```bash
curl http://localhost:8080/ping
```

A healthy server returns `{"status": "Healthy"}`.

Full documentation: [pytorch.org/serve](https://pytorch.org/serve/)
