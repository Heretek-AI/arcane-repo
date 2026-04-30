# Voicebox AI — Speech Synthesis & Voice Cloning

> **Informational template — project could not be fully verified for Docker deployment.**
> Voicebox AI requires GPU inference and large model downloads.
> This template provides a minimal inline API wrapper for health checks and guidance.
> For full functionality, run on GPU-enabled hardware.

[Voicebox AI](https://github.com/voicebox-ai/voicebox) generates natural, expressive speech from text with voice cloning, emotion control, and multi-language support. It uses advanced neural TTS models for high-quality audio output.

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

## Native Installation (GPU Recommended)

```bash
pip install voicebox-ai
# with GPU support:
pip install voicebox-ai[gpu]
```

### CLI Usage

```bash
# Generate speech from text
voicebox speak --text "Hello, this is a test." --voice natural

# Clone a voice from a sample
voicebox clone --audio sample.wav --name "my_voice"

# Start the inference server
voicebox serve --port 8080
```

### Python API

```python
from voicebox import Voicebox

vb = Voicebox(model="base")

# Synthesize speech
audio = vb.synthesize(
    text="Welcome to Voicebox AI.",
    voice="natural",
    emotion="friendly",
    speed=1.0
)
vb.save(audio, "output.wav")

# Voice cloning
vb.clone_voice("my_voice", sample="speaker_sample.wav")
audio = vb.synthesize("Hello from the cloned voice", voice="my_voice")
```

## Configuration

| Variable         | Default     | Description                                    |
|------------------|-------------|------------------------------------------------|
| `VOICEBOX_PORT`  | `8000`      | Host port for the informational API            |

## API Endpoints

| Endpoint   | Method | Description                         |
|------------|--------|-------------------------------------|
| `/health`  | GET    | Health check                        |
| `/guide`   | GET    | Usage guidance and setup notes      |

## Infrastructure Requirements

- **GPU:** CUDA-capable GPU with 8GB+ VRAM (RTX 3080 / A4000+)
- **Model storage:** 5GB+ for model weights
- **Memory:** 8GB+ system RAM recommended

## Troubleshooting

| Symptom                              | Likely Cause                     | Fix                                                    |
|--------------------------------------|----------------------------------|--------------------------------------------------------|
| No speech synthesis available         | This is an informational stub    | Install voicebox-ai on GPU hardware for full features  |
| Container exits immediately           | pip install failure              | Run `docker compose logs voicebox` for details         |
| GPU not detected in Docker            | GPU passthrough not configured   | Add `deploy: resources: reservations: devices: ...`    |
| Models fail to download               | Insufficient disk space          | Ensure 10GB+ free space for models and dependencies    |
