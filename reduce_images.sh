#! /usr/bin/env bash

mkdir -p half

for i in $( ls *.JPG); do 
    echo "reducing size: $i"
    convert -resize 50% $i half/$i
done

