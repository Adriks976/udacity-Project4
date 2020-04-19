#!/usr/bin/env bash

set -x

# This tags and uploads an image to Docker Hub

# Step 1:
# This is your Docker ID/path
dockerpath=adrik976/udacity-prediction

# Step 2
# Run the Docker Hub container with kubernetes

kubectl run prediction\
    --generator=run-pod/v1\
    --image=$dockerpath\
    --port=80 --labels app=prediction


kubectl wait pod/prediction --for=condition=Ready --timeout=-1s

# Step 3:
# List kubernetes pods
kubectl get pods

# Step 4:
# Forward the container port to a host
kubectl port-forward prediction 8000:80
