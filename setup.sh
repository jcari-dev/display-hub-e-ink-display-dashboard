#!/bin/bash

if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker and try again."
    exit 1
fi

if ! docker compose version &> /dev/null; then
    echo "Docker Compose (plugin) is not installed. Please install it and try again."
    exit 1
fi

REPO_URL="https://github.com/jcari-dev/display-hub-e-ink-display-dashboard.git"
REPO_NAME=$(basename "$REPO_URL" .git)

echo "Cloning repository..."
if git clone "$REPO_URL"; then
    cd "$REPO_NAME" || { echo "Failed to navigate to repository directory. Exiting."; exit 1; }
else
    echo "Failed to clone repository. Exiting."
    exit 1
fi

echo "Building and starting containers..."
if docker compose up --build -d --privileged --device=/dev/gpiomem; then
    DEVICE_IP=$(hostname -I | awk '{print $1}')
    echo "Installation complete. Access the web GUI at http://$DEVICE_IP"
else
    echo "Failed to start Docker Compose. Exiting."
    exit 1
fi
