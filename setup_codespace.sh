#!/bin/bash

# This script sets up a development environment in a GitHub Codespace.
# It installs necessary packages, configures git, and sets up the workspace.

# エラー時に停止
set -e

echo "Creating Python virtual environment..."
python -m venv ./.venv

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Initializing Reflex..."
reflex init

echo "Setup complete!"

# end of file
