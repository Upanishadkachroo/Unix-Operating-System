#!/bin/bash
# Download webpage

read -p "Enter URL: " url
wget "$url"

echo "✅ Download complete."
