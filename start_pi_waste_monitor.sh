#!/bin/bash

source /home/pi/.bashrc

echo "Wachten op wifi-verbinding (max 45 sec)..."

MAX_WAIT=45
WAITED=0

while ! ping -c 1 -W 1 google.com > /dev/null 2>&1; do
    sleep 1
    WAITED=$((WAITED + 1))
    if [ $WAITED -ge $MAX_WAIT ]; then
        echo "Geen internetverbinding gevonden binnen 45 seconden."
        break
    fi
done

cd /home/pi/PiWasteMonitor
source pytorch_env/bin/activate

if ping -c 1 -W 1 google.com > /dev/null 2>&1; then
    echo "Internetverbinding aanwezig. Updates worden gecontroleerd..."
    git pull
    pip install -r requirements.txt
else
    echo "Nog steeds geen internet. Updates worden overgeslagen."
fi

echo "main.py wordt uitgevoerd..."
python3 main.py
