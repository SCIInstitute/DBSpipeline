#!/bin/bash

if [[ -z "$SYSNAME" ]]; then
  echo environment not set.  run makeSysConfig.sh
  exit
fi

set -e

#Takes HCP annotation file in fsaverage space and puts it in subject space. Also outputs the files for use in tck2connectome
subject=$1


if [ -z "$subject" ]
then
	python3 "$CODEDIR/Python/Freesurfer/Connectome_maker.py"
else
	#Warp fsaverage to subject space
	for hemi in lh rh
	do
		mri_surf2surf --srcsubject fsaverage --trgsubject ${subject} --hemi ${hemi} --sval-annot ${DATADIR}/fsaverage/label/${hemi}.HCPMMP1.annot --tval ${DATADIR}/${subject}/label/${hemi}.HCPMMP1.annot
	done

	#convert annotation to volume
	mri_aparc2aseg --s ${subject} --annot HCPMMP1 --o ${subject}_HCP.mgz
	mrconvert -datatype uint32 ${subject}_HCP.mgz ${subject}_HCP.mif

	#fix annotations to match MRtrix conventions
	labelconvert ${subject}_HCP.mif $CODEDIR/Bash/Freesurfer/hcpmmp1_original.txt $CODEDIR/Bash/Freesurfer/hcpmmp1_ordered_edited.txt ${subject}_HCP.nii.gz

	#add any nifti volumes present in the folder to the parcellation, following the MRtrix convention
	python3 "$CODEDIR/Python/Freesurfer/Connectome_maker.py"
fi
