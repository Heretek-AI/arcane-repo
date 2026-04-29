# Ollama — Local LLM Inference

[Ollama](https://ollama.ai) lets you run large language models locally on your own hardware. This template provides a Docker-based Ollama server with persistent model storage and optional NVIDIA GPU acceleration.

## Quick Start

1. **Start the server:**

   ```bash
   docker compose up -d
   ```

2. **Pull a model:**

   ```bash
   docker compose exec ollama ollama pull llama3.1:8b
   ```

3. **Run inference:**

   ```bash
   docker compose exec ollama ollama run llama3.1:8b "What is the capital of France?"
   ```

   Or via the REST API:

   ```bash
   curl http://localhost:11434/api/generate -d '{
     "model": "llama3.1:8b",
     "prompt": "What is the capital of France?",
     "stream": false
   }'
   ```

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable                  | Default   | Description                                      |
|---------------------------|-----------|--------------------------------------------------|
| `OLLAMA_HOST_PORT`        | `11434`   | Host port for the Ollama API                     |
| `OLLAMA_MODEL`            | `llama3.1:8b` | Default model to pull                       |
| `OLLAMA_KEEP_ALIVE`       | `5m`      | How long to keep models in memory after last use |
| `OLLAMA_NUM_PARALLEL`     | `1`       | Parallel request-processing threads              |
| `OLLAMA_MAX_LOADED_MODELS`| `1`       | Maximum models kept in memory simultaneously     |

## Available Models

Ollama supports hundreds of open-source models. Popular options include:

| Model              | Parameters | Size   | Command                          |
|--------------------|-----------|--------|----------------------------------|
| Llama 3.1          | 8B        | 4.7 GB | `ollama pull llama3.1:8b`        |
| Llama 3.1          | 70B       | 40 GB  | `ollama pull llama3.1:70b`       |
| Mistral            | 7B        | 4.1 GB | `ollama pull mistral`            |
| Gemma 2            | 9B        | 5.3 GB | `ollama pull gemma2:9b`          |
| CodeLlama          | 7B        | 3.8 GB | `ollama pull codellama`          |
| Phi-3              | 3.8B      | 2.3 GB | `ollama pull phi3:mini`          |

See the full library at [ollama.ai/library](https://ollama.ai/library).

## GPU Passthrough (NVIDIA)

For GPU-accelerated inference:

1. **Install prerequisites:**
   - [NVIDIA drivers](https://www.nvidia.com/drivers) for your GPU
   - [nvidia-container-toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html):
     ```bash
     sudo apt-get install nvidia-container-toolkit
     sudo systemctl restart docker
     ```

2. **Uncomment the `deploy` block** in `docker-compose.yml` — the section between lines 15-26 (marked with comments) that contains `deploy.resources.reservations.devices`.

3. **Restart the service:**
   ```bash
   docker compose up -d
   ```

4. **Verify GPU access:**
   ```bash
   docker compose exec ollama nvidia-smi
   ```

The container gracefully falls back to CPU if no GPU is available — just leave the `deploy` block commented out.

## Managing Models

**List downloaded models:**

```bash
docker compose exec ollama ollama list
```

**Remove a model:**

```bash
docker compose exec ollama ollama rm llama3.1:8b
```

**Pull multiple models:**

```bash
docker compose exec ollama ollama pull mistral
docker compose exec ollama ollama pull gemma2:9b
```

## API Endpoints

Ollama exposes a REST API on port 11434:

| Endpoint             | Method | Description                    |
|----------------------|--------|--------------------------------|
| `/api/generate`      | POST   | Generate a completion          |
| `/api/chat`          | POST   | Generate a chat completion     |
| `/api/embed`         | POST   | Generate text embeddings       |
| `/api/tags`          | GET    | List downloaded models         |
| `/api/pull`          | POST   | Download a model               |
| `/api/ps`            | GET    | List loaded models             |

Full API reference: [github.com/ollama/ollama/blob/main/docs/api.md](https://github.com/ollama/ollama/blob/main/docs/api.md)

## Health Check

```bash
curl http://localhost:11434/api/tags
```

A successful response returns a JSON object with a `models` array (may be empty if no models are pulled yet — the server is still healthy).
