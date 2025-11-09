#!/bin/bash
# Locate file in system

read -p "Enter filename to search: " fname

echo "Searching..."
find / -name "$fname" 2>/dev/null
