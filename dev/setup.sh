#!/bin/bash
set -Eeuo pipefail

# Constants
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Parse arguments
while (($# > 0)); do
  if [[ "$1" == "--flit-version" ]]; then
    flit_version="$2"
    shift 2
  else
    echo "ERROR: Unrecognized argument ${1}" >&2
    exit 1
  fi
done

# Change to project directory
cd "$PROJECT_DIR" || exit 1

# Install dependencies
pip install -U flit=="${flit_version:?}"
flit install --deps develop --symlink
