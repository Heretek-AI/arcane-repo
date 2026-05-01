# Trivy — Comprehensive Security Scanner

[Trivy](https://github.com/aquasecurity/trivy) (34,785 ★) by Aqua Security scans containers, filesystems, Git repositories, and Kubernetes for vulnerabilities, misconfigurations, and secrets.

Trivy is a CLI-only tool — this template runs it as a `sleep infinity` container. All interaction is via `docker compose exec`.

## Quick Start

1. **Start the container:**

   ```bash
   docker compose up -d
   ```

2. **Scan a container image:**

   ```bash
   docker compose exec trivy trivy image nginx:latest
   ```

3. **Scan a filesystem:**

   ```bash
   docker compose exec trivy trivy fs /
   ```

4. **Scan a Git repository:**

   ```bash
   docker compose exec trivy trivy repo https://github.com/user/repo
   ```

## Common Commands

| Command | Description |
|---------|-------------|
| `trivy image <image>` | Scan a container image for vulnerabilities |
| `trivy fs <path>` | Scan a filesystem or directory |
| `trivy repo <url>` | Scan a Git repository |
| `trivy config <path>` | Scan configuration files (IaC, Kubernetes manifests) |
| `trivy sbom <image>` | Generate an SBOM for an image |
| `trivy --help` | Show all commands and flags |

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable | Default | Description |
|----------|---------|-------------|
| `TRIVY_CACHE_DIR` | `/root/.cache/trivy` | Cache location for vulnerability database |
| `TRIVY_QUIET` | `false` | Suppress progress output |
| `TRIVY_DEBUG` | `false` | Enable debug logging |
| `TRIVY_SEVERITY` | `CRITICAL,HIGH,MEDIUM` | Minimum severity to report |
| `TRIVY_TIMEOUT` | `5m0s` | Maximum scan duration |

## Scanning Local Images

The Docker socket is mounted so Trivy can scan images in the host Docker daemon. Pull the image you want to scan first, then run:

```bash
docker pull node:22-alpine
docker compose exec trivy trivy image node:22-alpine
```

## Scanning the Current Directory

The current directory is mounted at `/scan-target` as read-only:

```bash
docker compose exec trivy trivy fs /scan-target
```

## Supported Targets

- Container images (Docker, containerd, podman)
- Filesystems and directories
- Git repositories (remote and local)
- Kubernetes clusters and manifests
- Infrastructure as Code (Terraform, CloudFormation)
- SBOM generation (CycloneDX, SPDX)

Official docs: [aquasecurity.github.io/trivy](https://aquasecurity.github.io/trivy)
