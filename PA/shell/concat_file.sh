#!/bin/bash
# Concatenate multiple files

if [ "$#" -lt 2 ]; then
    echo "❌ Error: At least two filenames required."
    exit 1
fi

for file in "$@"
do
    if [ ! -f "$file" ]; then
        echo "❌ File not found: $file"
        exit 1
    fi
done

echo "✅ All files exist. Concatenating..."
cat "$@"
