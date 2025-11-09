#!/bin/bash
# Word frequency list for wonderland.txt

file="wonderland.txt"

if [ ! -f "$file" ]; then
    echo "❌ $file not found!"
    exit 1
fi

cat "$file" | tr -cs '[:alpha:]' '\n' | tr '[:upper:]' '[:lower:]' | sort | uniq -c | sort -nr
