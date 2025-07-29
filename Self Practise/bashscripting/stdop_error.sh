#!/bin/bash

release_file=/etc/os-release
errorlog=/var/log/update_error.log
logfile=/var/log/update.log

#if [ -d /etc/pacman.d ]; then
if  grep -q "Arch" $release_file
then
        #host is arch based user
        sudo pacman -syu 1>>$logfile 2>>$errorlog
        if [ $? -ne 0 ]; then
                echo "an error occur please check, $errorlog file"
        fi
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
        sudo apt update 1>>$logfile 2>>$errorlog
        if [ $? -ne 0]; then
                echo "an error occired in log file, $errorlog file"
        fi

        sudo apt dist-upgrade -y  1>>$logfile 2>>$errorlog
        if [ $? -ne 0 ]; then
                echo "an error occur please check, $errorlog file"
        fi

fi
~                                                                                                                                                                                       
~                                                                                                                                                                                       
~                         
