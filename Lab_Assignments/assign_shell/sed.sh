#!/bin/bash

echo "enter file name: "
read f

echo "enter starting pointer: "
read s

echo "enter ending pointer: "
read e

sed -n $s,$e\p $f
