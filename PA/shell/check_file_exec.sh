#!/bin/bash
# Check and modify execute permission

read -p "Enter filename: " file

if [ ! -e "$file" ]; then
    echo "❌ File does not exist."
    exit 1
fi

if [ -x "$file" ]; then
    echo "✅ File is executable. Removing execute permission..."
    chmod -x "$file"
    echo "Execute permission removed."
else
    echo "ℹ️ File is not executable."
fi
