#!/bin/bash
# S02 Verification Script — wrapper for cross-platform Python checks
# Run: bash scripts/verify-s02.sh
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
python "$SCRIPT_DIR/verify-s02.py"
