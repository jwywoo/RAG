#!/bin/bash

# Build the Docker image
docker build --platform linux/amd64 -t jwywoo/ha_rag_test .

# Push the Docker image to the repository
docker push jwywoo/ha_rag_test
