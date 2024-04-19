#!/bin/bash

# not meant to run in slurm without a wrapper

###
# TODO: figure out spaces in paths problem
# TODO: FS ID lookup table
# TODO: add FS env to scripts


. $(dirname $(readlink -f $0))/../../scripts/sysUtils.sh

innitBashPaths -v

if [ $SYSNAME == "hipergator" ]
then
module load fsl
module load freesurfer/6.0.0
module load perl/5.20.0
fi

#SUBJECTS_DIR=/home/mphook/blue_butsonc/mphook/freesurfer/SimNIBS/FS_Subjects
export SUBJECTS_DIR="${FREESURFERDIR}"/FS_Subjects




set -e
echo recon-all -s "$1" -i "${2}" -all -parallel -openmp 8

recon-all -s "$1" -i "${2}" -all -parallel -openmp 8 #-FLAIR $3 -FLAIRpial

m2m_id="$1"
subject=${m2m_id}
home="${PWD}"


#mv ${home}/${subject_id} $SUBJECTS_DIR

#Transform heat maps into patient space
echo $'\nTransforming Cortial Heat Maps to Patient Space**********************************************************************\n'
for hemi in lh rh
do
	call1="mri_surf2surf --srcsubject fsaverage --trgsubject ${subject} --trgsurfreg sphere.reg --hemi ${hemi} --sval ${SUBJECTS_DIR}/${hemi}.fsaverage.gm.PET_EEGFMRI_DWI_ZSCORE_4D_INTERSECTIONONLY_MEAN.proj-mid.sm10.5pcnt.min1cmsq.caudalmiddlefrontal.mgh --tval ${SUBJECTS_DIR}/${subject}/surf/${hemi}.thresh.mgh"
  echo $call1
  $call1
  
	call2="mri_surf2surf --srcsubject fsaverage --trgsubject ${subject} --trgsurfreg sphere.reg --hemi ${hemi} --sval ${SUBJECTS_DIR}/${hemi}.fsaverage.gm.PET_EEGFMRI_DWI_ZSCORE_4D_INTERSECTIONONLY_MEAN.proj-mid.sm10.posthresh.frontal.mgh --tval ${SUBJECTS_DIR}/${subject}/surf/${hemi}.heatmap.mgh"
  echo $call2
  $call2
	#Also adding HCP annotations to subject
	call3="mri_surf2surf --srcsubject fsaverage --trgsubject ${subject} --hemi ${hemi} --sval-annot ${SUBJECTS_DIR}/fsaverage/label/${hemi}.HCPMMP1.annot --tval ${SUBJECTS_DIR}/${subject}/label/${hemi}.HCPMMP1.annot"
  echo $call3
  $call3
done

# Convert heat maps to vtk
echo $'\nConvert Heat Maps to vtk**********************************************************************************************\n'
cd ${SUBJECTS_DIR}/${subject}/surf

for hemi in lh rh
do
	mris_convert -c ${hemi}.thresh.mgh ${hemi}.pial ${hemi}.thresh.vtk
	mris_convert -c ${hemi}.heatmap.mgh ${hemi}.pial ${hemi}.heatmap.vtk
done

#Convert thresh map to volume
echo $'\nCreate volume of Thresholded Heatmap**********************************************************************************\n'
mri_surf2vol --o thresh.nii.gz --subject $subject_id --so lh.pial lh.thresh.mgh --so rh.pial rh.thresh.mgh

#Convert vtk to TriSurfField
echo $'\nConvert Heat Maps to .pts, .fac, and data*****************************************************************************\n'

if [ $SYSNAME == "hipergator" ]
then
module load python
fi

python ${CODEDIR}/Python/SCIRun/vtk_to_TriSurfField.py

mkdir SCIRun
mv *.pts ${PWD}/SCIRun
mv *.fac ${PWD}/SCIRun
mv *_data.txt ${PWD}/SCIRun

rm -r ${PWD}/SCIRun/*_threes.fac
cd ${home}

#HCP Volume Creation
echo $'\nCreate HCP Labelmap***************************************************************************************************\n'
mri_aparc2aseg --s ${subject} --annot HCPMMP1 --o ${subject}_HCP.mgz


if [ $SYSNAME == "hipergator" ]
then
module load mrtrix
fi

mrconvert -datatype uint32 ${subject}_HCP.mgz ${subject}_HCP.mif
labelconvert ${subject}_HCP.mif ${CODEDIR}/Bash/Freesurfer/hcpmmp1_original.txt ${SUBJECTS_DIR}/${subject}/freesurfer/hcpmmp1_ordered_edited.txt HCP_FS.nii.gz

echo $'\n\n******************Done!****************\n\n'
