#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32gb
#SBATCH --time=1:00:00
#SBATCH --job-name=Tensors
#SBATCH --mail-type=ALL
#SBATCH --output=tensor_%j.out

if [[ -z "$SYSNAME" ]]; then
echo environment not set.  run makeSysConfig.sh
exit
fi

Help()
{
   # Display Help
   echo
   echo "Syntax: scriptTemplate [-h|d|l|c|f|m|s|i|:]"
   echo "options:"
   echo "-h    Help "
   echo "-d    DWI cleaned, pass as string *Required"
   echo "-l    bval AP, pass as string"
   echo "-c    bvec AP, pass as string"
   echo "-f    Freesurfer Subject ID *Required if no Mask"
   echo "-m    Coregistered Mask *Required if no Freesurfer"
   echo "-s    Use in Slurm/HiPerGator ("y")"
   echo "-i    Subject ID, will try to find ACPC_b0 transform if given"
   echo "-t    Transform, ACPC to b0"
   echo
}


# Get the options
while getopts ":h:d:l:c:f:m:s:i:" option; do
   case $option in
      d) DWI=$OPTARG;;
      l) dwi_bval=$OPTARG;;
      c) dwi_bvec=$OPTARG;;
      f) FSID=$OPTARG;;
      m) mask=$OPTARG;;
      s) slurm=$OPTARG;;
      i) SID=$OPTARG;;
      t) transform=$OPTARG;;
      h | * | :) Help && exit;;
   esac
done

set -e #exit on fail
if [ $SYSNAME == "hipergator" ]
then
  echo -e "\nUse on HiPerGator\n"
  module load mrtrix
  module load freesurfer/7.2.0
else
	echo -e "\nUse on local computer\n"
fi

if [ -z $dwi_bval ]
then
    echo -e "\nNo bval file given, assuming dwi has data"
    mrconvert $DWI dwi_tensor_prep.mif
else
    echo -e "\nAdding diffusion data to file"
    mrconvert $DWI -fslgrad dwi_bvec dwi_bval dwi_tensor_prep.mif
fi

if [ -n "$mask" ]
then
    echo -e "\nUsing provided mask and assuming it is coregistered\n"
    mrconvert $mask brainmask.mif -force
elif [ -n $SID ] && [-n $FSID]
then
    echo -e "\nGetting Transform from subject folder\n"
    cp ${DATADIR}/${SID}/Tractography/Cleaned/ACPC_to_b0.txt ${PWD}/transform.txt
elif [-n $transform ] && [-n $FSID]
then
    echo -e "\nUsing given transform\n"
    cp $transform ${PWD}/transform.txt
elif [-n $FSID] && [-z $transform ] && [ -z $SID ]
then
    echo -e "\nCreating transform using Freesurfer\n"
    5ttgen -nocrop hsvs ${SUBJECTS_DIR}/${FSID} T1_5tt_FS.mif -force #known to fail sometimes, maybe check mrstats for all zeros, if so, use fsl
	mrconvert T1_5tt_FS.mif T1_5tt.nii.gz -force
	bbregister --s ${FSID} --mov b0_hifi.nii.gz --reg b0_to_T1.lta --dti --o b0_ACPCspace.nii.gz
	mri_vol2vol --mov b0_hifi.nii.gz --targ T1_5tt.nii.gz --lta b0_to_T1.lta --o T1_5tt_b0space.nii.gz --inv
    lta_convert --inlta b0_to_T1.lta --outitk ACPC_to_b0.txt --invert
    lta_convert --inlta b0_to_T1.lta --outitk b0_to_ACPC.txt
    transformconvert ACPC_to_b0.txt itk_import ACPC_to_b0_mrtrix.txt -force
    transformconvert b0_to_ACPC.txt itk_import b0_to_ACPC_mrtrix.txt -force
    cp ACPC_to_b0_mrtrix.txt transform.txt
else
    echo -e "\nERROR: Not enough information\n"
    exit 1
fi


if [ -z $FSID ]
then
    dwi2tensor dwi_tensor_prep.mif -mask brainmask.mif dti.mif -force
    mrconvert brainmask.mif brain_mask.nii.gz -force
else
    echo -e "\nCreating mask from Freesurfer"
    SUBJECTS_DIR="${FREESURFERDIR}"/FS_Subjects
    cp ${SUBJECTS_DIR}/${FSID}/mri/brainmask.mgz .
    mrtransform brainmask.mgz -linear transform.txt brain_FS.mif
    mrfilter brain_FS.mif smooth -stdev 2 brain_FS_smooth.mif -force #Blur the image to remove small holes in the mask
    mrthreshold brain_FS_smooth.mif -abs 0 -comparison gt brainmask_FS.mif -force
    dwi2tensor dwi_tensor_prep.mif -mask brainmask_FS.mif dti.mif -force
    mrconvert brainmask_FS.mif brain_mask.nii.gz -force
fi

for count in 1 2 3
do
    tensor2metric dti.mif -value eigval${count}.nii.gz -num $count -force
    tensor2metric dti.mif -vector eigvec${count}.nii.gz -num $count -force
done

module load python/3.10 #version that has nibabel and pynrrd
python ${CODEDIR}/Python/SCIRun/nifti2nrrd.py --img brain_mask.nii.gz --datatype scalar
for count in 1 2 3
do
    python ${CODEDIR}/Python/SCIRun/nifti2nrrd.py --img eigval${count}.nii.gz --datatype scalar
    python ${CODEDIR}/Python/SCIRun/nifti2nrrd.py --img eigvec${count}.nii.gz --datatype vector
done