#!/bin/bash

directory=/etc

if [ -d $directory ]; then
	echo "the $directory exists"
else
	echo "the directory $directory does not exist"
fi

echo "the exit code of the script is: $?"
