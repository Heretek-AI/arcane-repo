---
title: "T-Pot — All-in-One Multi Honeypot Platform"
description: "T-Pot multi-honeypot platform with 5 core honeypot services (conpot, cowrie, dionaea, elasticpot, honeytrap) plus the management web UI — attack detection and visualization for security research"
---

# T-Pot — All-in-One Multi Honeypot Platform

T-Pot multi-honeypot platform with 5 core honeypot services (conpot, cowrie, dionaea, elasticpot, honeytrap) plus the management web UI — attack detection and visualization for security research

## Tags

<a href="/categories/security" class="tag-badge">security</a>

## Links

- [docker-compose.yml](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/tpotce/docker-compose.yml)
- [.env.example](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/tpotce/.env.example)
- [Documentation](https://raw.githubusercontent.com/Heretek-AI/arcane-repo/main/templates/tpotce/README.md)


## Metadata

| Field | Value |
|-------|-------|
| ID | `tpotce` |
| Version | 1.0.0 |
| Author | Arcane |
| Content Hash | `8bbc3535418a1cd6f1faf1251578108e6c4ccb05fbe91b736b32ca9180f20c11` |

## Quick Start

1. **Set the required password:**

   Copy `.env.example` to `.env` and set the web UI password:

   ```bash
   cp .env.example .env
   # Edit .env — set TPOT_WEB_PW to a strong password
   ```

2. **Start the stack:**

   ```bash
   docker compose up -d
   ```

3. **Access the management UI:**

   Open [https://localhost:64297](https://localhost:64297) in your browser. Login with `admin` / your `TPOT_WEB_PW`.

4. **Access the web dashboard:**

   Open [https://localhost:64294](https://localhost:64294) for the Kibana-based attack dashboard.

## Configuration

Copy `.env.example` to `.env` and edit:

### Required Variables

| Variable      | Description                                                         |
|---------------|---------------------------------------------------------------------|
| `TPOT_WEB_PW` | Password for the management web UI (username: `admin`).             |

### Optional Variables

| Variable           | Default   | Description                                          |
|--------------------|-----------|------------------------------------------------------|
| `TPOT_EXTIP`       | `0.0.0.0`  | External/public IP of this host                     |
| `COWRIE_SSH_PORT`  | `2222`    | Host port for SSH honeypot (Cowrie)                  |
| `COWRIE_TELNET_PORT`| `2323`   | Host port for Telnet honeypot (Cowrie)               |
| `ELASTICPOT_PORT`  | `9200`    | Host port for Elasticsearch honeypot (Elasticpot)    |
| `TPOT_UI_PORT`     | `64297`   | Host port for T-Pot management UI                    |
| `TPOT_WEB_PORT`    | `64294`   | Host port for T-Pot Kibana dashboard                 |
| `TPOT_WEB_USER`    | `admin`   | Web UI username                                      |

## Troubleshooting

| Symptom                         | Likely Cause                                | Fix                                                        |
|---------------------------------|---------------------------------------------|------------------------------------------------------------|
| UI login fails                  | `TPOT_WEB_PW` not set                       | Set `TPOT_WEB_PW` in `.env` and run `docker compose up -d` |
| Honeypots not receiving traffic | Ports not exposed or firewall blocking      | Verify port mappings in `.env` and firewall rules          |
| Management UI not loading       | Self-signed certificate warning in browser  | Click "Proceed anyway" or add certificate exception        |
| Container restart loop          | Missing required env var                    | Check `docker compose logs <service>` for error messages   |

Official docs: [github.com/telekom-security/tpotce](https://github.com/telekom-security/tpotce)

