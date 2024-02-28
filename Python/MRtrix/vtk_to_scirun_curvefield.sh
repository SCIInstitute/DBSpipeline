#!/bin/bash

mkdir SCIRun_files
slicer_fibers=*slicer.vtk
track_ext="_transformed.tck"
for convert in $slicer_fibers
do
filename=$(basename $convert _slicer.vtk)
tckconvert $convert "$filename$track_ext" -force
python3 tckConverter.py "$filename$track_ext" SCIRun_files/$filename
done

echo -e "\n\nDone!\n\n"