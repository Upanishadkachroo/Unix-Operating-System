#!/bin/bash
echo "enter the file name:"
read f

cat $f

echo "enter the words u want to delete:"
read word

sed -i "s/\b$word\b//g" "$f"

echo "the output of the file is"
cat $f
