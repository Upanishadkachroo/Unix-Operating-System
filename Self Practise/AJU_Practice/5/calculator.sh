#!/bin/bash
# calculator.sh - Simple calculator using case

echo "Enter first number:"
read a
echo "Enter second number:"
read b
echo "Enter operator (+, -, *, /):"
read op

case $op in
    "+") res=$((a + b));;
    "-") res=$((a - b));;
    "*") res=$((a * b));;
    "/") 
        if [ $b -ne 0 ]; then
            res=$((a / b))
        else
            echo "Division by zero error!"
            exit 1
        fi;;
    *) echo "Invalid operator!"; exit 1;;
esac

echo "Result: $res"
