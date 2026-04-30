#!/usr/bin/env bash
# build-images.sh — Local helper for building template Docker images
# Usage: bash scripts/build-images.sh [template-name]
#   Without arguments, builds all templates with dockerfiles.
#   With a template name, builds only that one.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
REPO_OWNER="${REPO_OWNER:-Heretek-AI}"
REPO_NAME="${REPO_NAME:-arcane-repo}"
DOCKERFILES_DIR="$ROOT_DIR/scripts/dockerfiles"

build_image() {
  local template="$1"
  local dockerfile="$DOCKERFILES_DIR/$template/Dockerfile"

  if [ ! -f "$dockerfile" ]; then
    echo "SKIP: $template — no Dockerfile at $dockerfile"
    return
  fi

  local tag="ghcr.io/$REPO_OWNER/$template:latest"
  echo "BUILD: $template -> $tag"
  docker build -t "$tag" -f "$dockerfile" "$ROOT_DIR"
  echo "OK: $template built as $tag"
}

if [ $# -eq 0 ]; then
  for dir in "$DOCKERFILES_DIR"/*/; do
    template="$(basename "$dir")"
    build_image "$template"
  done
else
  build_image "$1"
fi

echo ""
echo "Done. Images tagged under ghcr.io/$REPO_OWNER/*"
