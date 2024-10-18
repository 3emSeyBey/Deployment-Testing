#!/bin/bash

# Navigate to the project directory
cd /root/Deployment-Testing

# Pull the latest changes from the main branch
git pull origin main

# Activate the virtual environment
source /root/Deployment-Testing/.venv/bin/activate

# Install any new dependencies
pip install -r requirements.txt

# Restart the Uvicorn service (if using systemd)
sudo systemctl restart uvicorn
