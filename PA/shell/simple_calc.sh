#!/bin/bash
# Simple Calculator

echo "Enter first number: "
read a
echo "Enter second number: "
read b

echo "Choose operation: + - * /"
read op

case $op in
    +) result=$((a + b));;
    -) result=$((a - b));;
    \*) result=$((a * b));;
    /) result=$((a / b));;
    *) echo "Invalid operator"; exit;;
esac

echo "Result = $result"
