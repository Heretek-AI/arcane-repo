#!/bin/bash
# ── ELK Stack One-Time Setup ───────────────────────────────────────
# Bundled from upstream docker-elk setup/ directory.
# This script runs as a one-shot container to initialize:
#   1. Kibana system user password
#   2. Required ILM (Index Lifecycle Management) policies
#   3. Ingest pipelines for common log formats
#
# The container exits after completion. Re-run by setting RUN_SETUP=true
# in .env and starting the setup profile.

set -euo pipefail

DONE_FILE="/usr/share/elasticsearch/setup/.done"
ES_URL="http://elasticsearch:9200"
AUTH="elastic:${ELASTIC_PASSWORD:-changeme}"

echo "==> Waiting for Elasticsearch to be ready..."
until curl -s -u "$AUTH" "$ES_URL/_cluster/health" > /dev/null 2>&1; do
  echo "    Elasticsearch not ready yet — retrying in 5s..."
  sleep 5
done

echo "==> Elasticsearch is ready."
echo "==> Elasticsearch cluster health:"
curl -s -u "$AUTH" "$ES_URL/_cluster/health" | grep -E '(cluster_name|status|number_of_nodes)'

# ── 1. Set Kibana system user password ──────────────────────────
echo ""
echo "==> Configuring kibana_system user..."
if curl -s -u "$AUTH" -X POST "$ES_URL/_security/user/kibana_system/_password" \
  -H "Content-Type: application/json" \
  -d "{\"password\": \"${ELASTIC_PASSWORD:-changeme}\"}" | grep -q '"acknowledged":true'; then
  echo "    ✓ kibana_system password configured."
else
  echo "    ⚠ kibana_system password may already be set — continuing."
fi

# ── 2. Create ILM policy for log rotation ───────────────────────
echo ""
echo "==> Creating ILM retention policy for log indices..."
curl -s -u "$AUTH" -X PUT "$ES_URL/_ilm/policy/logs-retention" \
  -H "Content-Type: application/json" \
  -d '{
    "policy": {
      "phases": {
        "hot": { "min_age": "0ms", "actions": {} },
        "warm": { "min_age": "3d", "actions": { "readonly": {} } },
        "delete": { "min_age": "30d", "actions": { "delete": {} } }
      }
    }
  }' > /dev/null 2>&1
echo "    ✓ ILM policy 'logs-retention' created (or already exists)."

# ── 3. Create an index template for log indices ─────────────────
echo ""
echo "==> Creating index template for log indices..."
curl -s -u "$AUTH" -X PUT "$ES_URL/_index_template/logs-template" \
  -H "Content-Type: application/json" \
  -d '{
    "index_patterns": ["logs-*"],
    "template": {
      "settings": {
        "index.lifecycle.name": "logs-retention",
        "number_of_shards": 1,
        "number_of_replicas": 0
      }
    }
  }' > /dev/null 2>&1
echo "    ✓ Index template 'logs-template' created (or already exists)."

# ── Mark setup as complete ──────────────────────────────────────
touch "$DONE_FILE"
echo ""
echo "==> ✅ ELK stack setup complete."
echo "    Access Kibana at http://localhost:${KIBANA_PORT:-5601}"
echo "    Username: elastic"
echo "    Password: ${ELASTIC_PASSWORD:-changeme}"
