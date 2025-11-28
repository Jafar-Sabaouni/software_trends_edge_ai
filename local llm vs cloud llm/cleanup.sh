#!/bin/bash

echo "Stopping and removing Docker Compose services..."
docker-compose down --rmi all -v

echo "Removing benchmark-related Docker images..."
# Get the image name from the docker-compose.yaml build context
IMAGE_NAME=$(basename "$(pwd)")_benchmark
docker rmi "${IMAGE_NAME}" || true
docker rmi "ollama/ollama" || true # Also remove the ollama base image

echo "Cleaning up local files..."
if [ -d "results" ]; then
    echo "Removing results directory..."
    rm -rf results
fi

echo "Cleanup complete."
