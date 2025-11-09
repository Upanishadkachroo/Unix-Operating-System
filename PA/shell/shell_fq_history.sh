#!/bin/bash
# Frequency list of shell commands from history

echo "=== Top 5 Most Used Commands ==="
history | awk '{print $2}' | sort | uniq -c | sort -nr | head -5
