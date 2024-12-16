#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32gb
#SBATCH --time=10:00:00
#SBATCH --job-name=Preproc
#SBATCH --partition=gpu
#SBATCH --gpus=geforce:1
#SBATCH --mail-type=ALL
#SBATCH --output=Preproc_%j.out



#TODO check freesurfer file -


if [[ -z "$SYSNAME" ]]; then
echo environment not set.  run makeSysConfig.sh
exit
fi

Help()
{
   # Display Help
   echo
   echo "Syntax: scriptTemplate [-h|u|d|l|c|a|e|f|t|s|:]"
   echo "options:"
   echo "-h    Help "
   echo "-u    DWI_up, pass as string *Required "
   echo "-d    DWI_down, pass as string "
   echo "-l    bval AP, pass as string *Required"
   echo "-c    bvec AP, pass as string *Required"
   echo "-a    bval PA *Required for mismatch data"
   echo "-e    bvec PA *Required for mismatch data"
   echo "-f    Freesurfer Subject ID"
   echo "-t    T1 in ACPC space *Required"
   echo "-s    Use in Slurm/HiPerGator ("y")"
   echo "-i    Subject ID"
   echo
}


# Get the options
while getopts ":h:u:d:l:c:a:e:f:t:s:i:" option; do
   case $option in
      u) DWI_up=$OPTARG;;
      d) DWI_down=$OPTARG;;
      l) dwi_bval=$OPTARG;;
      c) dwi_bvec=$OPTARG;;
      a) bval_PA=$OPTARG;;
      e) bvec_PA=$OPTARG;;
      f) FSID=$OPTARG;;
      t) T1=$OPTARG;;
      s) slurm=$OPTARG;;
      i) SID=$OPTARG;;
      h | * | :) Help && exit;;
   esac
done

set -e #exit on fail

if [ -z "$SID" ]
then
  if [ -z "$FSID" ]
  then
    echo "no subject ID or FSID.  Using 'temp' for directory name"
    SID="temp"
  else
    SID=${FSID#fs_}
    echo "no subject ID.  Used FSID to get: $SID"
  fi
fi


# TEMPDIR is scratch dir root.  Probably shouldn't be made automatically
if [ ! -d $TEMPDIR ]
then
  echo "trying to use $TEMPDIR for temp files, but it doesn't exist."
  echo "please check env variables and//or run makeSysConfig.sh"
  exit
fi

tmp_dir=$TEMPDIR/$SID/proc_temp
mkdir -p $tmp_dir
cp $DWI_up $tmp_dir/DWI_up.nii.gz

cwd=$PWD




#Check for reverse phase
if [ -z "$DWI_down" ]
then
        echo -e "\n\nNo Reverse Phase given, changing methods. **Warning** This will decrease quality\n\n"
else
	cp $DWI_down $tmp_dir/DWI_down.nii.gz
fi

cp $dwi_bval $tmp_dir/dwi.bval
cp $dwi_bvec $tmp_dir/dwi.bvec
if [ -z "$bval_PA" ]
then
	echo -e "\nbval and bvec should match for both directions\n"
	cp $dwi_bval $tmp_dir/dwi_PA.bval
	cp $dwi_bvec $tmp_dir/dwi_PA.bvec
else
	cp $bval_PA $tmp_dir/dwi_PA.bval
	cp $bvec_PA $tmp_dir/dwi_PA.bvec
fi
cp $T1 $tmp_dir/T1_ACPC.nii.gz

if [ $SYSNAME == "hipergator" ]
then
  echo -e "\nUse on HiPerGator\n"
  module load python cuda
else
	echo -e "\nUse on local computer\n"
fi

# I think the rest of the script assumes the location is the temp dir
cd $tmp_dir

script=${CODEDIR}/Python/MRtrix/FSL_Slice_leveler.py

python $script

if [ $SYSNAME == "hipergator" ]
then
	module load ants
	module load fsl
	module load mrtrix
	module load freesurfer/7.2.0
fi

#SUBJECTS_DIR=/home/mphook/blue_butsonc/mphook/freesurfer/SimNIBS/FS_Subjects
SUBJECTS_DIR="${FREESURFERDIR}"/FS_Subjects

#Denoise
echo -e "\nDenoising\n"
dwidenoise DWI_up.nii.gz dwi_up_den.mif -noise noise.mif -force

#Unringing
echo -e "\nUnringing\n"
mrdegibbs dwi_up_den.mif dwi_up_den_unr.mif -axes 0,1 -force

#b0 extraction
echo -e "\nb0 Extraction From Both Directions\n"
dwiextract dwi_up_den_unr.mif -fslgrad dwi.bvec dwi.bval extract_b0_AP.mif -bzero -force
mrmath extract_b0_AP.mif mean mean_b0_AP.mif -axis 3 -force #AP

if [ -z "$DWI_down" ]
then
	echo -e "\nNo PA Direction\n"
	cp mean_b0_AP.mif b0_hifi.mif
else
	dwiextract DWI_down.nii.gz -fslgrad dwi_PA.bvec dwi_PA.bval extract_b0_PA.mif -bzero -force
	mrmath extract_b0_PA.mif mean mean_b0_PA.mif -axis 3 -force #PA

	mrcat mean_b0_AP.mif mean_b0_PA.mif -axis 3 b0_uncorrected.mif -force
fi

#Eddy Unwarp
echo -e "\nEddy Unwarp\n"

if [ -z "$DWI_down" ]
then
	echo -e "\nPerforming without b0\n"
	dwifslpreproc dwi_up_den_unr.mif dwi_up_preproc.mif -pe_dir AP -rpe_none -eddy_options " --slm=linear" -fslgrad dwi.bvec dwi.bval -force
else
	dwifslpreproc dwi_up_den_unr.mif dwi_up_preproc.mif -pe_dir AP -rpe_pair -se_epi b0_uncorrected.mif -eddy_options " --slm=linear" -fslgrad dwi.bvec dwi.bval -force
fi


#ANTS Bias correction
echo -e "\nBias Correction\n"
dwibiascorrect ants dwi_up_preproc.mif dwi_up_cleaned.mif -bias bias.mif -fslgrad dwi.bvec dwi.bval -force

# Upsample dwi to 1.5mm 
mrgrid dwi_up_cleaned.mif regrid -voxel 1.5 dwi_up_cleaned_resamp.mif -force
mrconvert dwi_up_cleaned_resamp.mif dwi_cleaned_resamp.mif -fslgrad dwi.bvec dwi.bval -force

#Masking
echo -e "\nBrain mask\n"
dwi2mask dwi_cleaned_resamp.mif brain_mask.mif -force

#Getting Unique bval Numbers
read -a value < dwi.bval
uniq=($(printf "%s\n" "${value[@]}" | sort | uniq -c | sort -rnk1 | awk '{ print $2 }'))
uniq_num=${#uniq[@]}

#Fiber Orientation
echo -e "\nFiber Orientation\n"
dwi2response dhollander dwi_cleaned_resamp.mif wm.txt gm.txt csf.txt -voxels voxels.mif -force
if (( $uniq_num > 2))
then
	echo -e "\nRunning Multi-shell\n"
	dwi2fod msmt_csd dwi_cleaned_resamp.mif -mask brain_mask.mif wm.txt wmfod.mif gm.txt gmfod.mif csf.txt csffod.mif -force
	echo -e "\nIntensity Normalization\n"
	mtnormalise wmfod.mif wmfod_norm.mif csffod.mif csffod_norm.mif gmfod.mif gmfod_norm.mif -mask brain_mask.mif -force
elif [ -z "$slurm" ]
then
	#WARNING: MRtrix in Docker does not work for files in Dropbox for some stupid reason. Must be on physical mounted drive on computer
	echo -e "\nRunning on Docker\n"
	docker run -v "$PWD:$PWD" -w "$PWD" --rm -t kaitj/mrtrix3tissue:v5.2.9 bash -c "ss3t_csd_beta1 dwi_cleaned_resamp.mif wm.txt wmfod.mif gm.txt gmfod.mif csf.txt csffod.mif -mask brain_mask.mif -nthreads 8 -force"
	echo -e "\nIntensity Normalization\n"
	mtnormalise wmfod.mif wmfod_norm.mif csffod.mif csffod_norm.mif gmfod.mif gmfod_norm.mif -mask brain_mask.mif -force
else
	echo -e "\nRunning Single-shell\n"
	module load mrtrix3tissue
	ss3t_csd_beta1 dwi_cleaned_resamp.mif wm.txt wmfod.mif gm.txt gmfod.mif csf.txt csffod.mif -mask brain_mask.mif -nthreads 8 -force
	module unload mrtrix3tissue
	module load mrtrix
	echo -e "\nIntensity Normalization\n"
	mtnormalise wmfod.mif wmfod_norm.mif csffod.mif csffod_norm.mif gmfod.mif gmfod_norm.mif -mask brain_mask.mif -force
fi

#Five Tissue Type Generation
echo -e "\nFinding 5 tissue types in T1\n"

#Create new b0
dwiextract dwi_cleaned_resamp.mif -fslgrad dwi.bvec dwi.bval b0_hifi.mif -bzero -force
mrconvert b0_hifi.mif b0_hifi.nii.gz -force

#Transform 5tt to b0 space

if [ -z "$FSID" ]
then
	echo -e "\nNo Freesurfer subject ID given, using FSL\n"
	5ttgen fsl T1_ACPC.nii.gz T1_5tt_ACPCspace.nii.gz -force
	mri_coreg --mov b0_hifi.nii.gz --ref T1_ACPC.nii.gz --reg b0_to_T1.lta
	mri_vol2vol --mov b0_hifi.nii.gz --targ T1_5tt_ACPCspace.nii.gz --lta b0_to_T1.lta --o T1_5tt_b0space.nii.gz --inv
else
	echo -e "\nUsing Freesurfer output\n"
	module unload fsl
	5ttgen -nocrop hsvs ${SUBJECTS_DIR}/${FSID} T1_5tt_FS.mif -force #known to fail sometimes, maybe check mrstats for all zeros, if so, use fsl
	mrconvert T1_5tt_FS.mif T1_5tt.nii.gz -force
	bbregister --s ${FSID} --mov b0_hifi.nii.gz --reg b0_to_T1.lta --dti --o b0_ACPCspace.nii.gz
	mri_vol2vol --mov b0_hifi.nii.gz --targ T1_5tt.nii.gz --lta b0_to_T1.lta --o T1_5tt_b0space.nii.gz --inv
	#mri_coreg --mov b0_hifi.nii.gz --ref T1_ACPC.nii.gz --reg b0_to_T1.lta
fi

#Prepare transformations
lta_convert --inlta b0_to_T1.lta --outitk ACPC_to_b0.txt --invert
lta_convert --inlta b0_to_T1.lta --outitk b0_to_ACPC.txt
transformconvert ACPC_to_b0.txt itk_import ACPC_to_b0_mrtrix.txt -force
transformconvert b0_to_ACPC.txt itk_import b0_to_ACPC_mrtrix.txt -force


sub_dir=$DATADIR/$SID

if [ ! -d $sub_dir ]
then
  echo "making subject dir: $sub_dir"
  echo "This is not normally supposed to happen.  Please check files, environments, and inputs"
  mkdir - p $sub_dir
fi
  

clean_dir=$sub_dir/Tractography/Cleaned
echo -e "\nCreating Output Directory: $clean_dir\n"
mkdir -p $clean_dir

if [ $SYSNAME == "hipergator" ]
then
	#Tensor Reconstruction
	echo -e "\nTensor Reconstrunction\n"
	dwi2tensor dwi_cleaned_resamp.mif -mask brain_mask.mif dti.mif -force
	mrconvert dti.mif dti.nii.gz -force
	tensor2metric dti.mif -fa fa.nii.gz -force
	#module load python/3.8
	#python ${CODEDIR}/Python/MRtrix/dtiConverter.py
	#cp tensor.nrrd $clean_dir/tensor.nrrd
	#cp fa.nrrd $clean_dir/fa.nrrd
	cp dti.nii.gz $clean_dir/dti.nii.gz
	cp fa.nii.gz $clean_dir/fa.nii.gz
else
	echo -e "\nNo Tensor Reconstruction\n"
fi


echo -e "\nCopying Files\n"
mrconvert brain_mask.mif brain_mask.nii.gz -force
mrconvert dwi_cleaned_resamp.mif dwi_cleaned.nii.gz -force
cp brain_mask.nii.gz $clean_dir/brain_mask.nii.gz
cp b0_hifi.nii.gz $clean_dir/b0_hifi.nii.gz
cp dwi_cleaned.nii.gz $clean_dir/dwi_cleaned.nii.gz
cp dwi_cleaned_resamp.mif $clean_dir/dwi_cleaned.mif
cp wmfod_norm.mif $clean_dir/wmfod_norm.mif
cp T1_5tt_b0space.nii.gz $clean_dir/T1_5tt.nii.gz
cp ACPC_to_b0_mrtrix.txt $clean_dir/ACPC_to_b0.txt
cp b0_to_ACPC_mrtrix.txt $clean_dir/b0_to_ACPC.txt
cp T1_ACPC.nii.gz $clean_dir/T1_ACPC.nii.gz

cd $cwd

echo -e "\n\nPreprocessing done, ready for tckgen\n\n"



# Notes for tck transformation

# warpinit b0.nii.gz wi.mif
# mrtransform wi.mif -linear T1_to_b0space.txt transform.mif -template b0 -interp linear -nan
# tcktransform fibers.tck transform.mif fibers_T1space.tck
