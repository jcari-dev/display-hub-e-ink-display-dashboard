if ! command -v docker &> /dev/null
then
    echo "Docker is not installed. Please install Docker and try again."
    exit 1
fi

if ! docker compose version &> /dev/null
then
    echo "Docker Compose is not installed. Please install Docker Compose (plugin) and try again."
    exit 1
fi

REPO_URL="https://github.com/jcari-dev/display-hub-e-ink-display-dashboard.git"
REPO_NAME=$(basename "$REPO_URL" .git)

if [ ! -d "$REPO_NAME" ]; then
    echo "Cloning repository..."
    git clone "$REPO_URL"
fi

cd "$REPO_NAME" || { echo "Failed to navigate to repository directory. Exiting."; exit 1; }

echo "Building containers..."
if ! docker compose build --no-cache; then
    echo "Failed to build containers. Exiting."
    exit 1
fi

echo "Starting containers..."
if ! docker compose up -d; then
    echo "Failed to start containers. Exiting."
    exit 1
fi

DEVICE_IP=$(hostname -I | awk '{print $1}')

echo "Installation complete. Access the web GUI at http://$DEVICE_IP"
