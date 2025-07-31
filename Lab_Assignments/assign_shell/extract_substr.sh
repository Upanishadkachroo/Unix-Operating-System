#!/bin/bash

str="my name is upanishad kachroo from wce sangli"

#print length of string
echo ${#str}

#print the substring of the above str

echo ${str:20}#from 20 indx to end
echo ${str:0:20}
echo ${str:-30}
