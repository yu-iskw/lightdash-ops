#!/bin/bash
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#

set -Eeuo pipefail

# Constants
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
PROJECT_DIR="$(dirname "${SCRIPT_DIR}")"

# If LIGHTDASH_API_KEY isn't set, we skip some tests to deal with Lightdash
if [[ -z "${LIGHTDASH_API_KEY:-}" ]]; then
  echo "WARN: LIGHTDASH_API_KEY not set, skipping some tests" >&2
fi

PYTHONPATH="${PROJECT_DIR}/lightdash_ops:${PYTHONPATH:-}" \
  pytest -v -s --cache-clear "${PROJECT_DIR}/lightdash_ops/tests"
