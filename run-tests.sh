#!/bin/sh
SCRIPT_DIR=$(dirname "$0")
cd "$SCRIPT_DIR"

python -m unittest discover -s testing -p "*_test.py"
