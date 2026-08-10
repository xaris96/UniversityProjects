#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

python3.13 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements.lock.txt
python -m ipykernel install --user --name choices13k-py313 --display-name "choices13k (Python 3.13)"
python verify_env.py

echo "Setup complete. Select kernel: choices13k (Python 3.13)"
