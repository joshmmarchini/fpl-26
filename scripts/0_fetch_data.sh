#!/usr/bin/env bash
set -e

DATA_DIR="FPL-Core-Insights"
REPO_URL="https://github.com/olbauday/FPL-Core-Insights.git"

if [ -d "$DATA_DIR/.git" ]; then
  echo "Data repo already exists, pulling latest..."
  git -C "$DATA_DIR" pull
else
  echo "Cloning data repo..."
  git clone "$REPO_URL" "$DATA_DIR"
fi