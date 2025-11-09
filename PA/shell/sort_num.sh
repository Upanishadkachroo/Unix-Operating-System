#!/bin/bash
# Sort 10 numbers in ascending order

echo "Enter 10 numbers:"
for i in {1..10}
do
    read num
    arr+=($num)
done

echo "Sorted numbers:"
printf "%s\n" "${arr[@]}" | sort -n
