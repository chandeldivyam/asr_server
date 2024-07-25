#!/bin/bash

# Define the container name
CONTAINER_NAME="fastapi-whisperx-container"

# Build the Docker image
docker build -t fastapi-whisperx-app .

# Check if the container is already running
if [ $(docker ps -q -f name=$CONTAINER_NAME) ]; then
    echo "Stopping and removing existing container..."
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
fi

# Run the Docker container
docker run -d --gpus all -p 12012:9000 --name $CONTAINER_NAME fastapi-whisperx-app
