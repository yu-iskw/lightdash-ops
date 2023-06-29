#!/bin/bash
set -Eeuo pipefail

# Constants
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Update the documentation of the CLI
typer lightdash_ops/cli/main.py utils docs --name "lightdash-ops" --output "docs/cli.md"

# Generate the JSON schemas and env template
python lightdash_ops/cli/main.py settings get | tee "${PROJECT_ROOT}/.env.template"
