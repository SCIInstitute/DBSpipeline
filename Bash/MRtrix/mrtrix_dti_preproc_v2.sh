#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=16gb
#SBATCH --time=05:00:00
#SBATCH --job-name=Preproc
#SBATCH --mail-type=ALL
#SBATCH --mail-user=mphook@ufl.edu
#SBATCH --output=Preproc_%j.out



Help()
{
   # Display Help
   echo
   echo "Syntax: scriptTemplate [-h|u|d|l|c|f|t|s]"
   echo "options:"
   echo "-h    Help "
   echo "-u    DWI_up, pass as string *Required "
   echo "-d    DWI_down, pass as string "
   echo "-l    bval, pass as string *Required"
   echo "-c    bvec, pass as string *Required"
   echo "-f    Freesurfer Subject ID"
   echo "-t    T1 in ACPC space"
   echo "-s    Use in Slurm/HiPerGator (y)"
   echo
}


# Get the options
while getopts ":h:u:d:l:c:f:t:s:" option; do
   case $option in
      u) DWI_up=$OPTARG;;
      d) DWI_down=$OPTARG;;
      l) dwi_bval=$OPTARG;;
      c) dwi_bvec=$OPTARG;;
      f) FSID=$OPTARG;;
      t) T1=$OPTARG;;
      s) slurm=$OPTARG;;
      h | * | :) Help && exit;;
   esac
done

set -e #exit on fail
mkdir proc_temp
cp $DWI_up proc_temp/DWI_up.nii.gz

#Check for reverse phase
if [ -z "$DWI_down" ]
then
        echo -e "\n\nNo Reverse Phase given, changing methods. **Warning** This will decrease quality\n\n"
else
	cp $DWI_down proc_temp/DWI_down.nii.gz
fi

cp $dwi_bval proc_temp/dwi.bval
cp $dwi_bvec proc_temp/dwi.bvec
cp $T1 proc_temp/T1_ACPC.nii.gz
cd proc_temp

if [ -z "$slurm" ]
then
	echo -e "\nUse on local computer\n"
  script=FSL_Slice_Remover.py
else
	echo -e "\nUse on HiPerGator\n"
	module load python
	script=../../../../FSL_Slice_Remover.py
fi

python $script

if [ -z "$slurm" ]
then
	echo -e "\n"
else
	module load ants
	module load fsl
	module load mrtrix
	module load freesurfer
fi



#Denoise
echo -e "\nDenoising\n"
dwidenoise DWI_up.nii.gz dwi_up_den.mif -noise noise.mif

#Unringing
echo -e "\nUnringing\n"
mrdegibbs dwi_up_den.mif dwi_up_den_unr.mif -axes 0,1

#b0 extraction
echo -e "\nb0 Extraction From Both Directions\n"
dwiextract dwi_up_den_unr.mif -fslgrad dwi.bvec dwi.bval extract_b0_AP.mif -bzero
mrmath extract_b0_AP.mif mean mean_b0_AP.mif -axis 3 #AP

if [ -z "$DWI_down" ]
then
	echo -e "\nNo PA Direction\n"
	cp mean_b0_AP.mif b0_hifi.mif
else
	dwiextract DWI_down.nii.gz -fslgrad dwi.bvec dwi.bval extract_b0_PA.mif -bzero
	mrmath extract_b0_PA.mif mean mean_b0_PA.mif -axis 3 #PA

	mrcat mean_b0_AP.mif mean_b0_PA.mif -axis 3 b0_hifi.mif
fi

#Eddy Unwarp
echo -e "\nEddy Unwarp\n"

if [ -z "$DWI_down" ]
then
	echo -e "\nPerforming without b0\n"
	dwifslpreproc dwi_up_den_unr.mif dwi_up_preproc.mif -pe_dir AP -rpe_none -eddy_options " --slm=linear" -fslgrad dwi.bvec dwi.bval
else
	dwifslpreproc dwi_up_den_unr.mif dwi_up_preproc.mif -pe_dir AP -rpe_pair -se_epi b0_hifi.mif -eddy_options " --slm=linear" -fslgrad dwi.bvec dwi.bval
fi

#ANTS Bias correction
echo -e "\nBias Correction\n"
dwibiascorrect ants dwi_up_preproc.mif dwi_up_cleaned.mif -bias bias.mif -fslgrad dwi.bvec dwi.bval

#Masking
echo -e "\nBrain mask\n"
dwi2mask dwi_up_cleaned.mif brain_mask.mif

#Fiber Orientation
echo -e "\nFiber Orientation\n"
dwi2response dhollander dwi_up_cleaned.mif wm.txt gm.txt csf.txt -voxels voxels.mif -fslgrad dwi.bvec dwi.bval
dwi2fod msmt_csd dwi_up_cleaned.mif -mask brain_mask.mif wm.txt wmfod.mif gm.txt gmfod.mif csf.txt csffod.mif -fslgrad dwi.bvec dwi.bval

#Intensity Normalization
echo -e "\nIntensity Normalization\n"
mtnormalise wmfod.mif wmfod_norm.mif csffod.mif csffod_norm.mif -mask brain_mask.mif

#Five Tissue Type Generation
echo -e "\nFinding 5 tissue types in T1\n"
#Transform 5tt to b0 space
mrconvert b0_hifi.mif b0_hifi.nii.gz

if [ -z "$FSID" ]
then
	echo -e "\nNo Freesurfer subject ID given, using FSL\n"
	mri_coreg --mov b0_hifi.nii.gz --ref T1_ACPC.nii.gz --reg b0_to_T1.lta
	mri_vol2vol --mov b0_hifi.nii.gz --targ T1_ACPC.nii.gz --lta b0_to_T1.lta --o T1_b0space.nii.gz --inv --nearest
	5ttgen fsl T1_b0space.nii.gz T1_5tt_b0space.nii.gz
else
	echo -e "\nUsing Freesurfer output\n"
	5ttgen -nocrop hsvs ${SUBJECTS_DIR}/${FSID} T1_5tt_FS.mif
	mrconvert T1_5tt_FS.mif T1_5tt.nii.gz
	bbregister --s ${FSID} --mov b0_hifi.nii.gz --reg b0_to_T1.lta --dti --o b0_ACPCspace.nii.gz
	mri_vol2vol --mov b0_hifi.nii.gz --targ T1_5tt.nii.gz --lta b0_to_T1.lta --o T1_5tt_b0space.nii.gz --inv --nearest
fi

#Prepare transformations
lta_convert --inlta b0_to_T1.lta --outitk ACPC_to_b0.txt --invert
lta_convert --inlta b0_to_T1.lta --outitk b0_to_ACPC.txt
transformconvert ACPC_to_b0.txt itk_import ACPC_to_b0_mrtrix.txt
transformconvert b0_to_ACPC.txt itk_import b0_to_ACPC_mrtrix.txt

echo -e "\nCreating Output Directory called 'Cleaned'\n"
mkdir ../Cleaned
echo -e "\nCopying Files\n"
mrconvert brain_mask.mif brain_mask.nii.gz
mrconvert dwi_up_cleaned.mif dwi_cleaned.nii.gz
cp brain_mask.nii.gz ../Cleaned/brain_mask.nii.gz
cp b0_hifi.nii.gz ../Cleaned/b0_hifi.nii.gz
cp dwi_cleaned.nii.gz ../Cleaned/dwi_cleaned.nii.gz
cp wmfod_norm.mif ../Cleaned/wmfod_norm.mif
cp T1_5tt_b0space.nii.gz ../Cleaned/T1_5tt.nii.gz
cp ACPC_to_b0_mrtrix.txt ../Cleaned/ACPC_to_b0.txt
cp b0_to_ACPC_mrtrix.txt ../Cleaned/b0_to_ACPC.txt

cd ..
echo -e "\n\nPreprocessing done, ready for tckgen\n\n"



# Notes for tck transformation

# warpinit b0.nii.gz wi.mif
# mrtransform wi.mif -linear T1_to_b0space.txt transform.mif -template b0 -interp linear -nan
# tcktransform fibers.tck transform.mif fibers_T1space.tck
