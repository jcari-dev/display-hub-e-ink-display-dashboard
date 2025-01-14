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

echo "Cloning repository..."
git clone "$REPO_URL"

if [ -d "$REPO_NAME" ]; then
    cd "$REPO_NAME" || exit
else
    echo "Failed to clone repository. Exiting."
    exit 1
fi

echo "Building and starting containers..."
docker compose up --build -d

DEVICE_IP=$(hostname -I | awk '{print $1}')

echo "Installation complete. Access the web GUI at http://$DEVICE_IP"
