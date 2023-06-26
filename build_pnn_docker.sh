#!/bin/bash
# Script to build the docker container
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR

# Try to stop docker if it is running.
echo "Stopping docker..."
sudo killall -9 dockerd || :

# If the docker.pid file exists, then delete it
rm -rf /var/run/docker.pid || :

# Start docker in the background.
echo "Starting docker..."
sudo dockerd &
sleep 5

# Enable buildkit
export DOCKER_BUILDKIT=1

# Remove all builds not built in the last 24 hours and not associated with a container
yes y 2>/dev/null | docker image prune -a --filter "until=24h" 

# This will build the full docker image. Use buildkit inline cache.
docker build -t pnn-docker:latest \
        -f Dockerfile \
        --progress=plain \
        --cache-from pnn-docker:latest \
        --build-arg BUILDKIT_INLINE_CACHE=1 \
        . 2>&1 | tee ./docker_build.log

# --no-cache \