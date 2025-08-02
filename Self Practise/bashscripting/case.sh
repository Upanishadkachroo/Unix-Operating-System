#!/bin/bash

echo "What is your favourite linux distro"

echo "1. arch"
echo "2. ubuntu"
echo "3. debian"

read distro

case $distro in
	1) echo "Arch is rolling";;
	2) echo "Ubuntu is rolling";;
	3) echo "Debian is rolling";;
	*) echo "typed something else"
esac
