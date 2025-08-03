#!/bin/bash

#the use of argument is to add multiple commands in our script

echo "You entered the argument: $1, $2, $3 and $4."

ls -lh $5

lines=$(ls -lh $5 | wc -l)
echo "You have $(($lines-1)) objects in the $5 directory"

