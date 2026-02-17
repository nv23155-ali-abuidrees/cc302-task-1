#!/usr/bin/env bash
set -e
# Simple script to set up and run the app using the repository .venv

# Use .venv if it exists, otherwise recommend manual venv creation
if [ -d ".venv" ]; then
  echo "Activating .venv..."
  # shellcheck disable=SC1091
  source .venv/bin/activate
else
  echo "No .venv directory found. Create one with: python -m venv .venv"
  echo "Then run: source .venv/bin/activate && pip install -r requirements.txt"
  exit 1
fi

echo "Installing requirements (idempotent)..."
pip install -r requirements.txt

echo "Starting Flask app on port 5000..."
python appp.py
