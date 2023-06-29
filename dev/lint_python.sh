#!/bin/bash
set -Eeuo pipefail

# Constants
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

pylint -v "${PROJECT_DIR}/lightdash_ops"
mypy "${PROJECT_DIR}/lightdash_ops"
