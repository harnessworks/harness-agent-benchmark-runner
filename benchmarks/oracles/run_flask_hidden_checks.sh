#!/usr/bin/env bash
set -euo pipefail

TASK_ID="${1:?task id is required}"
shift
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

export PIP_DISABLE_PIP_VERSION_CHECK=1

python3 -m venv .venv
.venv/bin/python -m pip install -q -r requirements.txt
.venv/bin/python -m pytest -q
.venv/bin/python "$SCRIPT_DIR/flask_hidden_oracle.py" "$TASK_ID" "$@"
