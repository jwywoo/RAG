#!/bin/bash

# Build the Docker image
docker build --platform linux/amd64 -t jwywoo/rag_test .

# Push the Docker image to the repository
docker push jwywoo/rag_test