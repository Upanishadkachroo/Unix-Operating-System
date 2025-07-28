#!/bin/bash

release_file=/etc/os-release

#if [ -d /etc/pacman.d ]; then
if  grep -q "Arch" $release_file 
then 
	#host is arch based user
	sudo pacman -syu
fi

if grep -q "Debian" $release_file
then
	sudo apt update
	sudo apt dist-update
fi

#if [ -d /etc/apt ]; then
if  grep -q "Ubuntu" $release_file 
then 
	#host is debian or ubuntu based user
	sudo apt update
fi
