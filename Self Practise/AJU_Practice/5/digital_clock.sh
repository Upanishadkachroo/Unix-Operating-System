#!/bin/bash
# digital_clock.sh - Displays current time every second

while true
do
    clear
    echo "----------------------"
    echo " 🕒 DIGITAL CLOCK 🕒"
    echo "----------------------"
    date +"%H : %M : %S"
    sleep 1
done
