#!/bin/bash

while read -r i;
do
#        old_file=${i%%(*}
#        rm $old_file
#        mv "$i" "$old_file"
         echo $i
done <<< "$(find | grep "2013-03-17)$")"
