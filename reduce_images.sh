#! /usr/bin/bash

if [ $# -lt 2 ] ; then
    echo "Usage: reduce_images.sh directory percentage"
    exit 0
fi

images_dir=$1
perc=$2

dest_dir=$images_dir"/reduced_"$2

echo " --------------- "
echo "  reduce_images  "
echo " --------------- "

echo "-- Processing image directory: "$images_dir
echo "-- Destination directory: "$dest_dir
echo "-- Reduce size will be: "$perc"%"

mkdir -p $dest_dir

shopt -s nocaseglob

total=$(ls -1 $images_dir/*.jpg | wc -l)
counter=0

for i in $(ls $images_dir/*.jpg); do
    echo -ne "converting ${i##*/}  ("$counter"/"$total") \r"
    convert -resize "$perc%" $i $dest_dir/${i##*/}
    counter=$(($counter+1))
done

echo "\n"
