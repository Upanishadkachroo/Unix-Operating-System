#!/bin/bash

process_name = "${1:-memory_user}"

pid=$(ps aux | grep -i "$process_name" | grep -v grep | awk '{print $2}')

if [ -z "$pid"]; then
	echo "Process '$process_name' not found"
	exit 1
fi

echo "Process found '$process_name' with pid '$pid'"
echo 

echo "Prcoess list all"
ps aux | grep -i "$PROCESS_NAME" | grep -v grep
echo

echo "pmap basic"
ps "$pid"
echo

echo "pmap with -x flag"
ps -x "$pid"

