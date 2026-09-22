#!/usr/bin/env bash
set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
export PYTHONPATH="$ROOT/backend"
echo "Starting RescueVoice API on http://localhost:8000"
python start.py
