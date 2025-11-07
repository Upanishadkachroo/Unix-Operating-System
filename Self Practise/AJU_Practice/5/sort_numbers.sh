#!/bin/bash
# sort_numbers.sh - Sort 10 numbers using Bubble Sort logic

echo "Enter 10 numbers:"
for ((i=0; i<10; i++))
do
    read arr[$i]
done

# Bubble sort
for ((i=0; i<10; i++))
do
    for ((j=i+1; j<10; j++))
    do
        if [ ${arr[$i]} -gt ${arr[$j]} ]; then
            temp=${arr[$i]}
            arr[$i]=${arr[$j]}
            arr[$j]=$temp
        fi
    done
done

echo "Numbers in ascending order:"
echo "${arr[@]}"
