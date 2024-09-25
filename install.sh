#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "Please, start with sudo."
   exit 1
fi

echo "Installing dependencies..."
apt-get update
apt-get install -y python3-module-requests

echo "Moving scripts to appropriate directories..."
cp api_utils.py /usr/lib/python3/site-packages/
cp cli_tool.py /usr/local/bin/pythonCLI

echo "Making the main script executable..."
chmod +x /usr/local/bin/pythonCLI

echo "Installation complete."

