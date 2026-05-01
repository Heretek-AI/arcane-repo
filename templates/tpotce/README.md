# T-Pot — All-in-One Multi-Honeypot Platform

[T-Pot](https://github.com/telekom-security/tpotce) (9,124 ★) by Deutsche Telekom Security bundles 10+ honeypot services with a unified management web UI for security research, threat intelligence, and attack visualization.

This template provides a simplified T-Pot stack with **5 core honeypots** plus the management web UI. Additional honeypot services are documented as optional add-ons.

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

## Services

| Service       | Image                          | Port(s)       | Description                                |
|---------------|--------------------------------|---------------|--------------------------------------------|
| `conpot`      | `dtagdevsec/conpot`            | —             | ICS/SCADA honeypot (Modbus, S7)            |
| `cowrie`      | `dtagdevsec/cowrie`            | 2222, 2323    | SSH + Telnet honeypot                      |
| `dionaea`     | `dtagdevsec/dionaea`           | —             | Multi-protocol malware capture honeypot    |
| `elasticpot`  | `dtagdevsec/elasticpot`        | 9200          | Elasticsearch honeypot                     |
| `honeytrap`   | `dtagdevsec/honeytrap`         | —             | Dynamic low-interaction honeypot           |
| `tpot-ui`     | `dtagdevsec/tpotce`            | 64297, 64294  | Management web UI + Kibana dashboard       |

All honeypot services run on a shared Docker bridge network (`tpotce_network`). The management UI has read-only access to the Docker socket for container monitoring.

## Optional Services

This template ships the core honeypot services. To add more, extend `docker-compose.yml` with these additional `dtagdevsec/*` images:

| Service            | Image                              | Type                     |
|--------------------|------------------------------------|--------------------------|
| `adbhoney`         | `dtagdevsec/adbhoney`              | Android Debug Bridge     |
| `citrixhoneypot`   | `dtagdevsec/citrixhoneypot`        | Citrix CVE-2019-19781    |
| `ddospot`          | `dtagdevsec/ddospot`               | DDoS honeypot            |
| `dicompot`         | `dtagdevsec/dicompot`              | DICOM medical device     |
| `fatt`             | `dtagdevsec/fatt`                  | File Analysis Tool       |
| `heralding`        | `dtagdevsec/heralding`             | Credential catcher       |
| `mailoney`         | `dtagdevsec/mailoney`              | SMTP honeypot            |
| `medpot`           | `dtagdevsec/medpot`                | HL7/FHIR medical         |
| `redishoneypot`    | `dtagdevsec/redishoneypot`         | Redis honeypot           |
| `sentrypeer`       | `dtagdevsec/sentrypeer`            | VoIP fraud detection     |
| `spidertrap`       | `dtagdevsec/spidertrap`            | Web spider honeypot      |
| `suricata`         | `dtagdevsec/suricata`              | Network IDS engine       |

Add each as a new service block in `docker-compose.yml`, attach it to `tpotce_net`, and add a named volume prefixed with `tpotce_`.

## Managing the Stack

**View logs:**

```bash
# All services
docker compose logs -f

# Specific honeypot
docker compose logs -f cowrie
docker compose logs -f dionaea
```

**Restart a service:**

```bash
docker compose restart cowrie
```

**Stop all services:**

```bash
docker compose down
```

## Volume Management

Each honeypot service and the UI have their own named volume:

| Volume                    | Service         |
|---------------------------|-----------------|
| `tpotce_conpot_data`      | `conpot`        |
| `tpotce_cowrie_data`      | `cowrie`        |
| `tpotce_dionaea_data`     | `dionaea`       |
| `tpotce_elasticpot_data`  | `elasticpot`    |
| `tpotce_honeytrap_data`   | `honeytrap`     |
| `tpotce_ui_data`          | `tpot-ui`       |

## Security Notes

- **Network exposure:** Honeypots are attack surfaces by design. Only expose them for security research. Do not map honeypot ports to public IPs without understanding the risks.
- **Isolation:** Place T-Pot on an isolated network segment, not your production LAN.
- **Web UI access:** The management UI uses self-signed certificates. Use a reverse proxy with a proper certificate in production.
- **Docker socket:** The UI mounts the Docker socket read-only for monitoring. Never mount it `rw` without understanding the implications.

## Troubleshooting

| Symptom                         | Likely Cause                                | Fix                                                        |
|---------------------------------|---------------------------------------------|------------------------------------------------------------|
| UI login fails                  | `TPOT_WEB_PW` not set                       | Set `TPOT_WEB_PW` in `.env` and run `docker compose up -d` |
| Honeypots not receiving traffic | Ports not exposed or firewall blocking      | Verify port mappings in `.env` and firewall rules          |
| Management UI not loading       | Self-signed certificate warning in browser  | Click "Proceed anyway" or add certificate exception        |
| Container restart loop          | Missing required env var                    | Check `docker compose logs <service>` for error messages   |

Official docs: [github.com/telekom-security/tpotce](https://github.com/telekom-security/tpotce)
