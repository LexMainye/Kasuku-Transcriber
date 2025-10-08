#!/bin/bash

DOCKER_USERNAME="yourusername"
IMAGE_NAME="kasuku-transcriber"
TAG="optimized"

echo "Building optimized Docker image..."
docker build -t $DOCKER_USERNAME/$IMAGE_NAME:$TAG .

echo "Image size:"
docker images $DOCKER_USERNAME/$IMAGE_NAME:$TAG

echo "Pushing to Docker Hub..."
docker push $DOCKER_USERNAME/$IMAGE_NAME:$TAG

echo "Size comparison:"
echo "Original: ~20GB"
echo "Optimized: $(docker images $DOCKER_USERNAME/$IMAGE_NAME:$TAG --format "table {{.Size}}")"