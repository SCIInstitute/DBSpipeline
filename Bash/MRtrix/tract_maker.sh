#!/bin/bash

set -e
#For renaming
#for file in *-*; do arr=(${file//-/ }); filename=${arr[@]:1:2}; mv -- $file ${filename// /-}; done

codedir=/mnt/z/Dropbox\ \(UFL\)/DataProcessing/Pipeline\ Code

for file in *_left.nii.gz
do
	filename=$(basename $file .nii.gz)
	mrtransform -linear ACPC_to_b0.txt $file ${filename}_b0space.nii.gz -force
done

for file in *_right.nii.gz
do
	filename=$(basename $file .nii.gz)
	mrtransform -linear ACPC_to_b0.txt $file ${filename}_b0space.nii.gz -force
done

mkdir -p Fibers
for file in *_b0space.nii.gz
do
	filename=$(basename $file _b0space.nii.gz)
	#tckgen -act T1_5tt.nii.gz -backtrack -angle 22.5 -seed_image $file -cutoff 0.2 -seeds 5000 wmfod_norm.mif Fibers/${filename}_fibers.tck
	tckgen -act T1_5tt.nii.gz -seed_image $file -cutoff 0.1 wmfod_norm.mif Fibers/${filename}_fibers.tck -force
done

#Moving to ACPC space
warpinit T1_ACPC.nii.gz warp.mif -force
mrtransform warp.mif -linear ACPC_to_b0.txt transform.mif -template b0_hifi.nii.gz -interp cubic -nan -force
for file in Fibers/*fibers.tck
do
	filename=$(basename $file .tck)
	tckresample -step_size 0.5 $file $file -force
	tcktransform $file transform.mif Fibers/${filename}_ACPC.tck -force
done
mkdir -p SCIRun_files
#File Conversion to SCIRun
for file in Fibers/*_fibers_ACPC.tck
do
filename=$(basename $file _fibers_ACPC.tck)
python3 $codedir/Python/MRtrix/tckConverter.py $file SCIRun_files/$filename
done
