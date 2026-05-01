# kata-containers Removal Rationale

**Template ID:** `kata-containers`
**GitHub:** https://github.com/kata-containers/kata-containers
**Stars:** 7,832
**Decision:** Removed without replacement — not Docker-composable

## Why Removed

kata-containers is a system-level VM runtime that provides hardware-virtualized
container isolation. It replaces the Linux kernel with a lightweight virtual
machine per container, integrating at the containerd/CRI-O runtime level.

**It is not deployable as a Docker container or Docker Compose service.**
kata-containers installs as a system daemon (`containerd-shim-kata-v2`) that
intercepts container runtime requests at the infrastructure layer. You cannot
run kata-containers inside Docker — it runs *under* Docker as an alternative
OCI runtime.

## D009 Precedent

This follows D009 (K8s-native tools exclusion): "Docker Compose wrappers for
K8s storage orchestration or cluster tools are misleading to users. These
belong in a K8s-focused registry, not a Docker Compose one."

Same principle applies: kata-containers is a container *infrastructure* tool
(containerd runtime class), not a containerized *application*. A Docker Compose
wrapper would be non-functional and misleading.

## R022 Compliance

R022 requires documented rationale for template removal. This document serves
as the formal removal record. kata-containers was never added to the
`templates/` directory — it was identified in CANDIDATES.md during M004
planning, correctly classified as non-Docker-serviceable per D011's third tier
("removal for non-Docker-serviceable system-level tools"), and excluded before
template creation.

## What Users Should Do Instead

- **To use kata-containers**: Follow the [upstream installation guide](https://github.com/kata-containers/kata-containers/blob/main/docs/install)
- **For Docker Compose-native sandboxing**: Use existing Arcane security templates (trivy, grype, rustscan, bunkerweb)
- **For VM-level isolation**: Deploy kata-containers at the container runtime level alongside your orchestration platform (Kubernetes + Kata runtime class)
