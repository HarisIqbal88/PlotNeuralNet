#!/bin/bash
# Shell script to run in a WSL/Linux terminal to start the container.

# Set the name of the container.
CONTAINER_NAME=pnn

# Set the name of the image, from docker_build.sh.
IMAGE_NAME=pnn-docker
IMAGE_TAG=latest

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Set the directory for the codebase.
CODEBASE=$SCRIPT_DIR/

# Try to stop docker if it is running.
echo "Stopping docker..."
sudo killall -9 dockerd || :

# If the docker.pid file exists, then delete it
rm -rf /var/run/docker.pid || :

# Start docker in the background.
echo "Starting docker..."
sudo dockerd &
sleep 5

# Run the docker image.
echo "Running docker image..."
sudo docker run --gpus all --rm -it \
    -v $CODEBASE:/app \
    --name $CONTAINER_NAME \
    --network host \
    $IMAGE_NAME:$IMAGE_TAG
 