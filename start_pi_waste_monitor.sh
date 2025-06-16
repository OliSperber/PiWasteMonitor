#!/bin/bash

echo "Waiting for 3 seconds to allow wifi connection..."
sleep 3

cd /home/pi/PiWasteMonitor
source pytorch_env/bin/activate

ping -c 1 google.com > /dev/null
if [ $? -eq 0 ]; then
    echo "Internet connection is found. Checking for updates..."
    git pull
    pip install -r requirements.txt
else
    echo "No internet connection. skipping checking for updates."
fi

echo "Running main.py"
python3 main.py