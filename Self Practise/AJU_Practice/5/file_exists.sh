#!/bin/bash
# file_exists.sh - Check if file exists

echo "Enter file name to check:"
read file

if [ -f "$file" ]; then
    echo " File '$file' exists."
else
    echo "File '$file' does not exist."
fi
