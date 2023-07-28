#!/bin/bash

# Start the containers
docker-compose up -d --build

# Get the container name of the integration tests
integration_container=$(docker-compose ps -q my-app)

# Check if the integration tests container is running
if [ -z "$integration_container" ]; then
    echo "The integration tests container is not running. Exiting..."
    # Stop the containers
    docker-compose down
    exit 1
fi

# Run the integration tests with the specified container name
docker exec "$integration_container" pytest test_integration.py

# Check if the my-app container is running
my_app_container=$(docker ps -q --filter "name=my-app")

if [ -z "$my_app_container" ]; then
    echo "The my-app container is not running. Skipping the prediction test."
else
    # The my-app container is running, so run the prediction test
    docker exec "$my_app_container" pytest test_integration.py
fi

# Stop the containers
docker-compose down

# # Pause the script to keep the window open
# read -p "Press Enter to exit..."
