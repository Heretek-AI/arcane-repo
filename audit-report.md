# Arcane Template Audit Report

**Date:** 2026-05-02T11:21:18.249203+00:00
**Templates scanned:** 10
**Duration:** 1.48s
**Script version:** 1.0.0

## Summary

### By Severity

| Severity | Count |
|----------|-------|
| error | 0 |
| warning | 4 |
| info | 21 |
| pass | 14 |

### By Dimension

| Dimension | Findings |
|-----------|----------|
| classification | 10 |
| freshness | 10 |
| ports | 9 |
| reachability | 10 |

## Per-Dimension Findings

### Classification

| Template ID | Name | Severity | Message | Suggested Fix |
|-------------|------|----------|---------|---------------|
| 015 | 015 | info | Multiple source tags set: self-hosted, awesome-selfhosted | Each template should typically have one source tag; verify this is correct |
| 13ft | 13Ft | info | Multiple source tags set: self-hosted, yunohost | Each template should typically have one source tag; verify this is correct |
| 2fauth | 2Fauth | info | Multiple source tags set: self-hosted, yunohost | Each template should typically have one source tag; verify this is correct |
| abantecart | Abantecart | info | Multiple source tags set: self-hosted, yunohost | Each template should typically have one source tag; verify this is correct |
| activepieces | Activepieces | info | Multiple source tags set: self-hosted, portainer | Each template should typically have one source tag; verify this is correct |
| actual | Actual | info | Multiple source tags set: self-hosted, portainer | Each template should typically have one source tag; verify this is correct |
| adguardhome | Adguardhome | info | Multiple source tags set: self-hosted, yunohost | Each template should typically have one source tag; verify this is correct |
| admidio | Admidio | info | Multiple source tags set: self-hosted, yunohost | Each template should typically have one source tag; verify this is correct |
| adminer | Adminer | info | Multiple source tags set: self-hosted, yunohost | Each template should typically have one source tag; verify this is correct |
| adminerevo | Adminerevo | info | Multiple source tags set: self-hosted, yunohost | Each template should typically have one source tag; verify this is correct |

### Freshness

| Template ID | Name | Severity | Message | Suggested Fix |
|-------------|------|----------|---------|---------------|
| 015 | 015 | warning | Service '015': image last updated 1678 days ago (>365) — consider updating | Pull the latest image tag or rebuild if the image is maintained |
| 13ft | 13Ft | warning | Service '13ft': image last updated 618 days ago (>365) — consider updating | Pull the latest image tag or rebuild if the image is maintained |
| 2fauth | 2Fauth | pass | Service '2fauth': image updated 28 days ago (<=180) — fresh | — |
| abantecart | Abantecart | warning | Service 'abantecart': image last updated 1361 days ago (>365) — consider updating | Pull the latest image tag or rebuild if the image is maintained |
| activepieces | Activepieces | info | Service 'activepieces': last_updated unavailable via anonymous API — manual review needed | Verify image freshness via GHCR/Quay web UI or authenticated API |
| actual | Actual | warning | Service 'actual': image last updated 1234 days ago (>365) — consider updating | Pull the latest image tag or rebuild if the image is maintained |
| adguardhome | Adguardhome | pass | Service 'adguardhome': image updated 1 days ago (<=180) — fresh | — |
| admidio | Admidio | pass | Service 'admidio': image updated 0 days ago (<=180) — fresh | — |
| adminer | Adminer | pass | Service 'adminer': image updated 14 days ago (<=180) — fresh | — |
| adminerevo | Adminerevo | info | Service 'adminerevo': last_updated unavailable via anonymous API — manual review needed | Verify image freshness via GHCR/Quay web UI or authenticated API |

### Ports

| Template ID | Name | Severity | Message | Suggested Fix |
|-------------|------|----------|---------|---------------|
| 015 | 015 | info | Service(s) ['015'] expose well-known container port 8080 | Verify this is intentional (e.g. web app on 8080, DB on 3306) |
| 13ft | 13Ft | info | Service(s) ['13ft'] expose well-known container port 8080 | Verify this is intentional (e.g. web app on 8080, DB on 3306) |
| 2fauth | 2Fauth | info | Service(s) ['2fauth'] expose well-known container port 8080 | Verify this is intentional (e.g. web app on 8080, DB on 3306) |
| abantecart | Abantecart | info | Service(s) ['abantecart'] expose well-known container port 8080 | Verify this is intentional (e.g. web app on 8080, DB on 3306) |
| activepieces | Activepieces | info | Service(s) ['activepieces'] expose well-known container port 8080 | Verify this is intentional (e.g. web app on 8080, DB on 3306) |
| adguardhome | Adguardhome | info | Service(s) ['adguardhome'] expose well-known container port 8080 | Verify this is intentional (e.g. web app on 8080, DB on 3306) |
| admidio | Admidio | info | Service(s) ['admidio'] expose well-known container port 8080 | Verify this is intentional (e.g. web app on 8080, DB on 3306) |
| adminer | Adminer | info | Service(s) ['adminer'] expose well-known container port 8080 | Verify this is intentional (e.g. web app on 8080, DB on 3306) |
| adminerevo | Adminerevo | info | Service(s) ['adminerevo'] expose well-known container port 8080 | Verify this is intentional (e.g. web app on 8080, DB on 3306) |

### Reachability

| Template ID | Name | Severity | Message | Suggested Fix |
|-------------|------|----------|---------|---------------|
| 015 | 015 | pass | Service '015': image docker.io/bantul/015:latest is reachable on Docker Hub | — |
| 13ft | 13Ft | pass | Service '13ft': image docker.io/wasimaster/13ft:latest is reachable on Docker Hub | — |
| 2fauth | 2Fauth | pass | Service '2fauth': image docker.io/2fauth/2fauth:latest is reachable on Docker Hub | — |
| abantecart | Abantecart | pass | Service 'abantecart': image docker.io/abantecart/abantecart:latest is reachable on Docker Hub | — |
| activepieces | Activepieces | pass | Service 'activepieces': image ghcr.io/activepieces/activepieces:latest is reachable on GHCR | — |
| actual | Actual | pass | Service 'actual': image docker.io/phoenixashes/actual:latest is reachable on Docker Hub | — |
| adguardhome | Adguardhome | pass | Service 'adguardhome': image docker.io/adguard/adguardhome:latest is reachable on Docker Hub | — |
| admidio | Admidio | pass | Service 'admidio': image docker.io/admidio/admidio:latest is reachable on Docker Hub | — |
| adminer | Adminer | pass | Service 'adminer': image docker.io/library/adminer:latest is reachable on Docker Hub | — |
| adminerevo | Adminerevo | pass | Service 'adminerevo': image ghcr.io/shyim/adminerevo:latest is reachable on GHCR | — |
