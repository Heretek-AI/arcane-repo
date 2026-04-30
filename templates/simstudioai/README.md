# SimStudio AI — 3D Simulation for AI Agents

> **Informational template — project could not be fully verified for Docker deployment.**
> SimStudio AI requires GPU-accelerated rendering and 3D engine dependencies.
> This template provides a minimal inline API wrapper for health checks and guidance.
> For full functionality, run on GPU-enabled bare metal or cloud instances.

[SimStudio AI](https://github.com/simstudioai/simstudio) provides photorealistic 3D simulation environments for training, testing, and evaluating AI agents. It supports reinforcement learning, embodied AI research, and multi-agent scenarios in rich virtual worlds.

## Quick Start

1. **Start the API wrapper:**

   ```bash
   cp .env.example .env
   docker compose up -d
   ```

2. **Verify it's running:**

   ```bash
   curl http://localhost:8000/health
   ```

3. **Get usage guidance:**

   ```bash
   curl http://localhost:8000/guide
   ```

## Native Installation (GPU Required)

```bash
pip install simstudio-ai
```

### Basic Usage

```bash
# Run a simulation with a trained agent
simstudio run --scene kitchen --agent your_agent.py

# Evaluate agent performance
simstudio eval --config evaluation_config.yaml

# Launch the visualizer
simstudio visualize --log results.json
```

### Python API

```python
import simstudio as ss

# Create a simulation environment
env = ss.Environment(scene="kitchen", render=False)
agent = ss.Agent.load("your_agent.pth")

for episode in range(100):
    obs = env.reset()
    done = False
    while not done:
        action = agent.act(obs)
        obs, reward, done = env.step(action)
```

## Configuration

| Variable            | Default     | Description                                    |
|---------------------|-------------|------------------------------------------------|
| `SIMSTUDIOAI_PORT`  | `8000`      | Host port for the informational API            |

## API Endpoints

| Endpoint   | Method | Description                         |
|------------|--------|-------------------------------------|
| `/health`  | GET    | Health check                        |
| `/guide`   | GET    | Usage guidance and setup notes      |

## Infrastructure Requirements

- **GPU:** CUDA-capable GPU (NVIDIA) with 8GB+ VRAM
- **Rendering:** Hardware-accelerated 3D rendering support
- **Storage:** 10GB+ for scenes and agent models
- **Memory:** 16GB+ system RAM recommended

For GPU cloud instances, consider:

| Provider      | GPU Options                    | Starting Price |
|---------------|--------------------------------|----------------|
| RunPod        | A100, A6000, RTX 4090         | $0.34/hr       |
| Vast.ai       | Various (RTX 3090, A5000)     | $0.20/hr       |
| Lambda Cloud  | A100, H100                     | $1.10/hr       |
| Paperspace    | A4000, A5000, A100             | $0.51/hr       |

## Troubleshooting

| Symptom                              | Likely Cause                     | Fix                                                    |
|--------------------------------------|----------------------------------|--------------------------------------------------------|
| No simulation available               | This is an informational stub    | Install simstudio-ai on GPU hardware for full features |
| Container exits immediately           | pip install failure              | Run `docker compose logs simstudioai` for details      |
| GPU not detected in Docker            | GPU passthrough not configured   | Add `deploy: resources: reservations: devices: ...`    |
