#!/usr/bin/env bash
# Convenience launcher for macOS / Linux.
# Sets up the virtual environment (via run.py) and starts the app.
set -e
cd "$(dirname "$0")"

# Prefer python3, fall back to python.
if command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
else
    PYTHON=python
fi

exec "$PYTHON" run.py
