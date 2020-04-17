#!/bin/sh

  #do something in directory which is accessible with $folder:
  #do vts which didn't done


for kk in markage.*; do
  a=$( echo $kk | awk -F "." '{ print int($2)}')
done

for ((kk2=20;kk2<=$a;kk2=kk2+1))
do 
  echo "ploting ...  $kk2"
  python ~/code/git-code/plot_material/chiiplot_5.py $kk2 -300
done

