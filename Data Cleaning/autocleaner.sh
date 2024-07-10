#!/bin/sh
for i in in/*; 
    do echo "cleaning:  " $i; 
    python3 cleaner.py $i;
    echo "done cleaning:  " $i;
done