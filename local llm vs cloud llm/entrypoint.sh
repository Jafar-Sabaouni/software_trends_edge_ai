#!/bin/bash

# Exit on error
set -e

echo "Starting Ollama server in the background..."
/usr/local/bin/ollama serve &
# Wait for the server to be ready
sleep 10

echo "Pulling the Gemma 3 (4B) model..."
/usr/local/bin/ollama pull gemma3:4b

echo "Ollama setup complete. Running the benchmark script..."
exec "$@"
