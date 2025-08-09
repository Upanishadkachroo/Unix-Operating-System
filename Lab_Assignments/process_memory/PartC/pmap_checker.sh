#!/bin/bash
PROCESS_NAME="${1:-memory_user}"


PID=$(ps aux | grep -i "$PROCESS_NAME" | grep -v grep | awk '{print $2}')

if [ -z "$PID" ]; then
    echo "Process '$PROCESS_NAME' not found."
    exit 1
fi

echo "Found process '$PROCESS_NAME' with PID: $PID"
echo


echo "=== Process List (filtered) ==="
ps aux | grep -i "$PROCESS_NAME" | grep -v grep
echo


echo "=== pmap basic ==="
pmap "$PID"
echo

echo "=== pmap extended (-x) ==="
pmap -x "$PID"
echo

echo "=== pmap full details (-XX) ==="
pmap -XX "$PID"
