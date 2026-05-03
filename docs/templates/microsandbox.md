---
title: "Microsandbox"
description: "Secure local programmable sandboxes for AI agents — run untrusted code in isolated micro-VMs with Firecracker, KVM, and resource limits"
---

# Microsandbox

Secure local programmable sandboxes for AI agents — run untrusted code in isolated micro-VMs with Firecracker, KVM, and resource limits

## Tags

<a href="/categories/ai" class="tag-badge">ai</a> <a href="/categories/security" class="tag-badge">security</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/microsandbox/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/microsandbox/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/microsandbox/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `microsandbox` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `213736a4fea96e96f51aac555f0c227fa562fac4034b5cc9685c6df63492d709` |

## Quick Start

### Linux (with KVM)

1. **Verify KVM is available:**

   ```bash
   ls -l /dev/kvm
   ```

   If KVM is not available, enable it in your BIOS/UEFI or use a bare-metal Linux host.

2. **Start the container:**

   ```bash
   docker compose up -d
   ```

3. **Create and use a sandbox:**

   ```bash
   docker compose exec microsandbox microsandbox create --image alpine
   docker compose exec microsandbox microsandbox exec <sandbox-id> -- "echo hello"
   ```

### Apple Silicon (macOS)

On Apple Silicon, Microsandbox uses macOS Virtualization.framework — no KVM required. The `/dev/kvm` device mapping is ignored. Start as normal with `docker compose up`.

## Configuration

Copy `.env.example` to `.env` and edit:

| Variable                       | Default                     | Description                             |
|--------------------------------|-----------------------------|-----------------------------------------|
| `MICROSANDBOX_DATA_DIR`        | `/var/lib/microsandbox`     | Sandbox images and state                |
| `MICROSANDBOX_SOCKET_DIR`      | `/var/run/microsandbox`     | Socket path for sandbox communication   |
| `MICROSANDBOX_DEFAULT_IMAGE`   | `alpine`                    | Default OS image for new sandboxes      |
| `MICROSANDBOX_MEMORY_MB`       | `512`                       | Memory per sandbox (MB)                 |
| `MICROSANDBOX_CPU_COUNT`       | `1`                         | vCPU count per sandbox                  |
| `MICROSANDBOX_TIMEOUT_SEC`     | `30`                        | Default execution timeout (seconds)     |
| `MICROSANDBOX_LOG_LEVEL`       | `info`                      | Log verbosity                           |

