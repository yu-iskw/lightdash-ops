#!/bin/bash
set -Eeuo pipefail

# Constants
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# If LIGHTDASH_API_KEY isn't set, we skip some tests to deal with Lightdash
if [[ -z "${LIGHTDASH_API_KEY:-}" ]]; then
  echo "WARN: LIGHTDASH_API_KEY not set, skipping some tests" >&2
fi

pytest -v -s --cache-clear "${PROJECT_DIR}/lightdash_ops/tests"
