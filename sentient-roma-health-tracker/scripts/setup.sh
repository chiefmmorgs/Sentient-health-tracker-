#!/usr/bin/env bash
set -e
python -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "Create .env from .env.example and run:"
echo "uvicorn sentient_roma_api:app --reload --host 0.0.0.0 --port 8000"
