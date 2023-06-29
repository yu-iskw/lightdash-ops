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
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Parse arguments
flit_version="3.7.1"
flit_deps="production"
while (($# > 0)); do
  if [[ "$1" == "--flit-version" ]]; then
    flit_version="$2"
    shift 2
  elif [[ "$1" == "--flit-deps" ]]; then
    flit_deps="$2"
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
flit install --deps "${flit_deps:?}" --symlink
