#!/bin/bash
# Check Network Connection

read -p "Enter website or IP to ping: " site

if ping -c 2 "$site" &> /dev/null
then
    echo "✅ System is connected to network."
else
    echo "❌ Network connection not available."
fi
