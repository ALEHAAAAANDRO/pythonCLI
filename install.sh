#!/bin/bash

echo "Installing dependencies..."
sudo apt-get update
sudo apt-get install -y python3-requests

echo "Moving scripts to appropriate directories..."
sudo cp api_utils.py /usr/lib/python3/site-packages/
sudo cp cli_tool.py /usr/local/bin/pythonCLI

echo "Making the main script executable..."
sudo chmod +x /usr/local/bin/pythonCLI

echo "Installation complete."

