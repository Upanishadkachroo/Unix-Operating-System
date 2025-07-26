#!/bin/bash

comand=/snap/bin/htop

if [ -f $command ]; then
	echo "$comand is available lets run it.."
else 
	echo "not available lets install.."
	sudo apt update && sudo apt install -y htop
fi

$comand
