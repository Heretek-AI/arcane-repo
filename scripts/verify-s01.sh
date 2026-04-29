#!/usr/bin/env bash
# =============================================================================
# verify-s01.sh — End-to-end verification for S01 template registry pipeline
#
# Tests:
#   1. Empty templates dir fails validation
#   2. Valid template passes --validate-only
#   3. Build produces registry.json file
#   4. registry.json has templates array
#   5. Auto-generated URLs match expected raw content pattern
#   6. content_hash is 64-char hex (SHA-256)
#   7. Duplicate ID fails validation
#   8. Missing required file fails validation
#   9. Invalid JSON in arcane.json fails validation
#
# Cleans up test artifacts after run.
# =============================================================================

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BUILD_SCRIPT="$ROOT_DIR/scripts/build-registry.js"
TEMPLATES_DIR="$ROOT_DIR/templates"
REGISTRY_FILE="$ROOT_DIR/registry.json"
SCHEMA_FILE="$ROOT_DIR/schema.json"

PASS=0
FAIL=0

# Change to ROOT_DIR so all paths are relative
cd "$ROOT_DIR"

# ── Colors ──────────────────────────────────────────────────────────────
GREEN='\033[0;32m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ── Helpers ─────────────────────────────────────────────────────────────

check() {
  local name="$1"
  shift
  if "$@"; then
    echo -e "  ${GREEN}✓${NC} $name"
    PASS=$((PASS + 1))
  else
    echo -e "  ${RED}✗${NC} $name"
    FAIL=$((FAIL + 1))
  fi
}

check_cmd() {
  local name="$1"
  local expected_exit="$2"
  shift 2
  local actual_exit=0
  "$@" 2>/dev/null || actual_exit=$?
  if [ "$actual_exit" -eq "$expected_exit" ]; then
    echo -e "  ${GREEN}✓${NC} $name"
    PASS=$((PASS + 1))
  else
    echo -e "  ${RED}✗${NC} $name (expected exit $expected_exit, got $actual_exit)"
    FAIL=$((FAIL + 1))
  fi
}

check_output() {
  local name="$1"
  local expected_pattern="$2"
  shift 2
  local output
  output="$("$@" 2>/dev/null)" || true
  if echo "$output" | grep -q "$expected_pattern"; then
    echo -e "  ${GREEN}✓${NC} $name"
    PASS=$((PASS + 1))
  else
    echo -e "  ${RED}✗${NC} $name (expected output matching: $expected_pattern)"
    echo "    got: $(echo "$output" | head -3)"
    FAIL=$((FAIL + 1))
  fi
}

cleanup_temp() {
  local dir="$1"
  rm -rf "$dir"
}

# ── Pre-flight checks ───────────────────────────────────────────────────

echo -e "${CYAN}═══ Pre-flight checks ═══${NC}"

check "Build script exists" test -f "$BUILD_SCRIPT"
check "Schema file exists" test -f "$SCHEMA_FILE"
check "Templates dir exists" test -d "$TEMPLATES_DIR"
check "Node.js available" command -v node >/dev/null 2>&1

# ── Test 1: Empty templates dir fails validation ────────────────────────

echo -e "\n${CYAN}═══ Test 1: Empty templates dir fails validation ═══${NC}"

BACKUP_DIR="$(mktemp -d)"
# Move all template folders out temporarily
for d in "$TEMPLATES_DIR"/*/; do
  [ -d "$d" ] && mv "$d" "$BACKUP_DIR/" 2>/dev/null || true
done

check_cmd "Empty templates dir → exit 1" 1 node "$BUILD_SCRIPT" --validate-only

# Restore templates
for d in "$BACKUP_DIR"/*/; do
  [ -d "$d" ] && mv "$d" "$TEMPLATES_DIR/" 2>/dev/null || true
done
rmdir "$BACKUP_DIR" 2>/dev/null || true

# ── Test 2: Valid template passes --validate-only ────────────────────────

echo -e "\n${CYAN}═══ Test 2: Valid template passes --validate-only ═══${NC}"

check_cmd "Valid test-app template → exit 0" 0 node "$BUILD_SCRIPT" --validate-only

# ── Test 3: Build produces registry.json ─────────────────────────────────

echo -e "\n${CYAN}═══ Test 3: Build produces registry.json ═══${NC}"

# Remove any prior registry.json
rm -f "$REGISTRY_FILE"
check_cmd "Build script exits 0" 0 node "$BUILD_SCRIPT"
check "registry.json was created" test -f "$REGISTRY_FILE"

# ── Test 4: registry.json has templates array ───────────────────────────

echo -e "\n${CYAN}═══ Test 4: registry.json content checks ═══${NC}"

check_output "registry.json has templates array" '"templates"' cat "$REGISTRY_FILE"

# Parse with node for structured checks
check_output "templates array is non-empty" 'has templates' node -e "
  const r = JSON.parse(require('fs').readFileSync('registry.json', 'utf8'));
  console.log(r.templates.length > 0 ? 'has templates' : 'empty');
"

# ── Test 5: Auto-generated URLs match expected pattern ──────────────────

echo -e "\n${CYAN}═══ Test 5: Auto-generated URL checks ═══${NC}"

check_output "compose_url matches raw.githubusercontent.com" 'raw.githubusercontent.com' node -e "
  const r = JSON.parse(require('fs').readFileSync('registry.json', 'utf8'));
  r.templates.forEach(t => console.log(t.compose_url));
"

check_output "env_url matches raw.githubusercontent.com" 'raw.githubusercontent.com' node -e "
  const r = JSON.parse(require('fs').readFileSync('registry.json', 'utf8'));
  r.templates.forEach(t => console.log(t.env_url));
"

check_output "documentation_url matches raw.githubusercontent.com" 'raw.githubusercontent.com' node -e "
  const r = JSON.parse(require('fs').readFileSync('registry.json', 'utf8'));
  r.templates.forEach(t => console.log(t.documentation_url));
"

# ── Test 6: content_hash is present, 64 hex chars, SHA-256 ──────────────

echo -e "\n${CYAN}═══ Test 6: content_hash checks ═══${NC}"

check_output "content_hash is 64-char hex string" 'content_hash OK' node -e "
  const r = JSON.parse(require('fs').readFileSync('registry.json', 'utf8'));
  r.templates.forEach(t => {
    if (/^[a-f0-9]{64}$/.test(t.content_hash)) {
      console.log('content_hash OK');
    } else {
      console.log('INVALID:', t.content_hash);
      process.exit(1);
    }
  });
"

# ── Test 7: Duplicate ID fails validation ───────────────────────────────

echo -e "\n${CYAN}═══ Test 7: Duplicate ID fails validation ═══${NC}"

DUP_DIR="$TEMPLATES_DIR/dup-test"
mkdir -p "$DUP_DIR"
cp "$TEMPLATES_DIR/test-app/arcane.json" "$DUP_DIR/arcane.json"
cp "$TEMPLATES_DIR/test-app/docker-compose.yml" "$DUP_DIR/docker-compose.yml"
cp "$TEMPLATES_DIR/test-app/.env.example" "$DUP_DIR/.env.example"
cp "$TEMPLATES_DIR/test-app/README.md" "$DUP_DIR/README.md"

check_cmd "Duplicate ID → exit 1" 1 node "$BUILD_SCRIPT" --validate-only

cleanup_temp "$DUP_DIR"

# ── Test 8: Missing required file fails validation ──────────────────────

echo -e "\n${CYAN}═══ Test 8: Missing required file fails validation ═══${NC}"

MISSING_DIR="$TEMPLATES_DIR/missing-file-test"
mkdir -p "$MISSING_DIR"
cat > "$MISSING_DIR/arcane.json" << 'EOF'
{
  "id": "missing-file-test",
  "name": "Missing File Test",
  "description": "Testing missing required file detection",
  "version": "1.0.0",
  "author": "Test",
  "tags": ["test"]
}
EOF

# Only add docker-compose.yml, skip .env.example and README.md
cat > "$MISSING_DIR/docker-compose.yml" << 'EOF'
version: '3'
services:
  app:
    image: nginx:latest
EOF

check_cmd "Missing .env.example → exit 1" 1 node "$BUILD_SCRIPT" --validate-only

cleanup_temp "$MISSING_DIR"

# ── Test 9: Invalid JSON fails validation ──────────────────────────────

echo -e "\n${CYAN}═══ Test 9: Invalid arcane.json JSON fails validation ═══${NC}"

INVALID_DIR="$TEMPLATES_DIR/invalid-json-test"
mkdir -p "$INVALID_DIR"
echo 'this is not { valid json' > "$INVALID_DIR/arcane.json"
touch "$INVALID_DIR/docker-compose.yml"
touch "$INVALID_DIR/.env.example"
touch "$INVALID_DIR/README.md"

check_cmd "Invalid arcane.json JSON → exit 1" 1 node "$BUILD_SCRIPT" --validate-only

cleanup_temp "$INVALID_DIR"

# ── Summary ─────────────────────────────────────────────────────────────

echo -e "\n${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo -e "  ${GREEN}Passed: $PASS${NC}"
echo -e "  ${RED}Failed: $FAIL${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"

# Clean up registry.json generated by tests
rm -f "$REGISTRY_FILE"

if [ "$FAIL" -gt 0 ]; then
  exit 1
fi
echo -e "\n${GREEN}All verification checks passed.${NC}"
