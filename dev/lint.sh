#!/bin/bash
set -Eeuo pipefail

hooks=(
  end-of-file-fixer
  trailing-whitespace
  check-json
  check-yaml
  detect-private-key
  isort
  pylint
  python-safety-dependencies-check
)

for hook in "${hooks[@]}"; do
  pre-commit run --all-files "${hook:?}"
done
