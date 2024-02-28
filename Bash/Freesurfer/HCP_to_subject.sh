#!/bin/bash

set -e

#Takes HCP annotation file in fsaverage space and puts it in subject space. Also outputs the files for use in tck2connectome
subject=$1

if [ -z "$subject" ]
then
	cp /mnt/z/Dropbox\ \(UFL\)/DataProcessing/Pipeline\ Code/Python/Freesurfer/Connectome_maker.py .
	python3 Connectome_maker.py
else
	#Warp fsaverage to subject space
	for hemi in lh rh
	do
		mri_surf2surf --srcsubject fsaverage --trgsubject ${subject} --hemi ${hemi} --sval-annot ${SUBJECTS_DIR}/fsaverage/label/${hemi}.HCPMMP1.annot --tval ${SUBJECTS_DIR}/${subject}/label/${hemi}.HCPMMP1.annot
	done

	#convert annotation to volume
	mri_aparc2aseg --s ${subject} --annot HCPMMP1 --o ${subject}_HCP.mgz
	mrconvert -datatype uint32 ${subject}_HCP.mgz ${subject}_HCP.mif

	#fix annotations to match MRtrix conventions
	labelconvert ${subject}_HCP.mif /mnt/z/Dropbox\ \(UFL\)/DataProcessing/Pipeline\ Code/Bash/Freesurfer/hcpmmp1_original.txt /mnt/z/Dropbox\ \(UFL\)/DataProcessing/Pipeline\ Code/Bash/Freesurfer/hcpmmp1_subcortex.txt ${subject}_HCP.nii.gz

	#add any nifti volumes present in the folder to the parcellation, following the MRtrix convention
	cp /mnt/z/Dropbox\ \(UFL\)/DataProcessing/Pipeline\ Code/Python/Freesurfer/Connectome_maker.py .
	python3 Connectome_maker.py
fi
