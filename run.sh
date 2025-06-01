#!/bin/bash

while true; do
    echo "Starting Furina..."
    python3 index.py
    
    # If exit code is 0 (clean shutdown), break the loop
    if [ $? -eq 0 ]; then
        break
    fi
    
    echo "Bot crashed. Restarting in 5 seconds..."
    sleep 5
done
