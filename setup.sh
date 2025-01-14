#!/bin/bash

# Ensure Docker is installed
if ! command -v docker &> /dev/null
then
    echo "Docker is not installed. Please install Docker and try again."
    exit 1
fi

# Ensure Docker Compose is installed
if ! docker compose version &> /dev/null && ! command -v docker-compose &> /dev/null
then
    echo "Docker Compose is not installed. Please install Docker Compose and try again."
    exit 1
fi

# Clone the repository
REPO_URL="https://github.com/jcari-dev/display-hub-e-ink-display-dashboard.git"
REPO_NAME=$(basename "$REPO_URL" .git) 

echo "Cloning repository..."
git clone "$REPO_URL"

# Navigate to the cloned repository directory
if [ -d "$REPO_NAME" ]; then
    cd "$REPO_NAME" || exit
else
    echo "Failed to clone repository. Exiting."
    exit 1
fi

# Build and start the containers
echo "Building and starting containers..."
docker compose up --build -d || docker-compose up --build -d

# Get the IP address of the device
DEVICE_IP=$(hostname -I | awk '{print $1}')

echo "Installation complete. Access the web GUI at http://$DEVICE_IP"
