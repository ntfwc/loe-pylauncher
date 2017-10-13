#!/bin/sh
SCRIPT_DIR=$(dirname "$0")
cd "$SCRIPT_DIR"

python3 -m unittest discover -s testing -p "*_test.py"
