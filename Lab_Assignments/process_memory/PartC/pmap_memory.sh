#!/bin/bash

PROCESS_NAME="memory_user"

echo "=== Step 1: Start your $PROCESS_NAME program so it prints its PID ==="
echo "Waiting for PID..."
sleep 2


PID=$(ps aux | grep -i "$PROCESS_NAME" | grep -v grep | awk '{print $2}')

if [ -z "$PID" ]; then
    echo "Process '$PROCESS_NAME' not found. Please start it before running this script."
    exit 1
fi

echo " Found process '$PROCESS_NAME' with PID: $PID"
echo

echo "=== 1) After allocation but before touching pages (lazy allocation) ==="
pmap -x "$PID" | grep -i anon
pmap -x "$PID" | tail -n 1
echo " RSS should be small or zero — only virtual space reserved."
echo

read -p "Press Enter once you have touched/written each page in memory_user..."


echo "=== 2) After touching pages (force allocation) ==="
pmap -x "$PID" | grep -i anon
pmap -x "$PID" | tail -n 1
echo " RSS should have jumped — physical pages allocated."
echo " Dirty will increase if writes occurred."
echo

read -p "Kill the program now, then press Enter to continue..."

echo "=== 3) After program exit ==="
if ps -p "$PID" > /dev/null; then
    echo " Program still running. Please kill it first."
else
    echo "Program terminated. Memory mapping gone."
fi

echo
echo " Note: pmap -x sums may overcount due to shared pages."
echo "For unique memory (USS) or proportional share (PSS), see:"
echo "  /proc/$PID/smaps   or   /proc/$PID/smaps_rollup"

