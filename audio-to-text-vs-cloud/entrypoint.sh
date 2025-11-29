#!/bin/bash
set -e

echo "Starting benchmark..."
python3 scripts/benchmark.py
echo "Benchmark finished."

echo "Starting analysis..."
python3 scripts/analyse.py
echo "Analysis finished."
