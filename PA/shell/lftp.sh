#!/bin/bash
# Download file using lftp

read -p "Enter remote host (e.g. ftp.example.com): " host
read -p "Enter username: " user
read -s -p "Enter password: " pass
echo
read -p "Enter remote file path: " remotefile

lftp -u "$user","$pass" "$host" -e "get $remotefile; bye"
