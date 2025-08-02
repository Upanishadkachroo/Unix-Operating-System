#!/bin/bash

finished=0

while [ $finished -ne 1 ]; do
	echo "What is your favourite linux distro"

        echo "1. arch"
        echo "2. ubuntu"
        echo "3. debian"
	echo "4. if want to exit"

        read distro

        case $distro in
		1) echo "Arch is rolling";;
	        2) echo "Ubuntu is rolling";;
	        3) echo "Debian is rolling";;
		4) finished=1;;
	        *) echo "typed something else"
        esac
done

echo "end of while conditioning statement"

