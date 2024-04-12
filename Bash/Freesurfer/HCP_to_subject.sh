#!/bin/bash

. $(dirname $(readlink -f $0))/../../scripts/sysUtils.sh

innitBashPaths -v

set -e

#Takes HCP annotation file in fsaverage space and puts it in subject space. Also outputs the files for use in tck2connectome
subject=$1

#codedir=/mnt/z/Dropbox\ \(UFL\)/DataProcessing/Pipeline\ Code
export SUBJECTS_DIR="${FREESURFERDIR}"/FS_Subjects

echo ${SUBJECTS_DIR}

if [ -z "$subject" ]
then
	python3 $CODEDIR/Python/Freesurfer/Connectome_maker.py
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
	labelconvert ${subject}_HCP.mif $CODEDIR/Bash/Freesurfer/hcpmmp1_original.txt $CODEDIR/Bash/Freesurfer/hcpmmp1_subcortex.txt ${subject}_HCP.nii.gz

	#add any nifti volumes present in the folder to the parcellation, following the MRtrix convention
	python3 $CODEDIR/Python/Freesurfer/Connectome_maker.py
fi
