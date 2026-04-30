# Microsandbox — Secure AI Agent Sandboxes

[Microsandbox](https://github.com/superradcompany/microsandbox) provides secure, isolated micro-VMs for running untrusted code — purpose-built for AI agents that need to execute arbitrary code safely. Powered by Firecracker on Linux and Virtualization.framework on macOS.

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

## Platform Requirements

| Platform           | Requirement                        | Status        |
|--------------------|------------------------------------|---------------|
| Linux (x86_64)     | KVM enabled (`/dev/kvm`)          | Full support  |
| Linux (ARM64)      | KVM enabled                       | Full support  |
| Apple Silicon      | macOS 13+ Virtualization.framework| Full support  |
| Windows (WSL2)     | Nested virtualization             | Experimental  |
| Intel Mac          | Not supported                     | —             |

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

## Use Cases for AI Agents

Microsandbox is designed for AI agent tooling:

- **Code execution**: Run AI-generated code in isolation without risking the host
- **File system safety**: Sandboxes have their own filesystem — no host access
- **Network isolation**: Control whether sandboxes can access the network
- **Resource limits**: CPU, memory, and time limits prevent runaway processes
- **Programmatic API**: Manage sandboxes via CLI or programmatic SDK

## CLI Commands

| Command                                | Description                            |
|----------------------------------------|----------------------------------------|
| `microsandbox create --image alpine`   | Create a new sandbox                   |
| `microsandbox exec <id> -- "cmd"`      | Execute a command in a sandbox         |
| `microsandbox list`                    | List all active sandboxes              |
| `microsandbox destroy <id>`            | Terminate a sandbox                    |
| `microsandbox snapshot <id>`           | Snapshot sandbox state for later reuse |
| `microsandbox logs <id>`               | View sandbox execution logs            |

## Notes

- This container runs **privileged** (required for KVM/VM access). Only deploy on trusted infrastructure.
- The container does not expose a network port — all interaction is via `docker compose exec`.
- Sandbox state persists in the `microsandbox_data` volume.

Full documentation: [github.com/superradcompany/microsandbox](https://github.com/superradcompany/microsandbox)
