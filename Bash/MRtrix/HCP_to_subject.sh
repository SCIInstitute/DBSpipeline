#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=16gb
#SBATCH --time=1:00:00
#SBATCH --job-name=HCP_fs
#SBATCH --mail-type=ALL
#SBATCH --output=HCP_fs_%j.out

# example call
# sbatch --mail-user=user@ufl.edu $CODEDIR/Bash/Freesurfer/HCP_to_subject.sh fs_pDummy

if [[ -z "$SYSNAME" ]]; then
  echo environment not set.  run makeSysConfig.sh
  exit
fi

if [ $SYSNAME == "hipergator" ]
then
module load fsl
module load freesurfer/6.0.0
module load perl/5.20.0
fi

#SUBJECTS_DIR=/home/mphook/blue_butsonc/mphook/freesurfer/SimNIBS/FS_Subjects
export SUBJECTS_DIR="${FREESURFERDIR}"/FS_Subjects

rel_path1="SCIRun"
rel_path2="Connectome"
rel_path3="Segmentations/HCP"
rel_path4="Segmentations/Hotspot"
rel_path5="Segmentations/White_matter"
set -e

#Takes HCP annotation file in fsaverage space and puts it in subject space. Also outputs the files for use in tck2connectome
subject=fs_{$1}
subject_LO=$1

for hemi in lh rh
do
mri_surf2surf --srcsubject fsaverage --trgsubject ${subject} --hemi ${hemi} --sval-annot ${SUBJECTS_DIR}/fsaverage/label/${hemi}.HCPMMP1.annot --tval ${SUBJECTS_DIR}/${subject}/label/${hemi}.HCPMMP1.annot
done

#HCP Volume Creation
echo $'\nCreate HCP Labelmap ***************************************************************************************************\n'
mri_aparc2aseg --s ${subject} --annot HCPMMP1 --o ${subject}_HCP.mgz


if [ $SYSNAME == "hipergator" ]
then
module load mrtrix
fi

mrconvert -datatype uint32 ${subject}_HCP.mgz ${subject}_HCP.mif -force
mkdir -p ${DATADIR}/${subject_LO}/$rel_path3
labelconvert ${subject}_HCP.mif ${CODEDIR}/Bash/Freesurfer/hcpmmp1_original.txt ${CODEDIR}/Bash/Freesurfer/hcpmmp1_subcortex.txt ${DATADIR}/${subject_LO}/${rel_path3}/HCP_FS.nii.gz

mkdir -p ${DATADIR}/${subject_LO}/$rel_path5
mrcalc ${subject}_HCP.mif 2 -eq ${DATADIR}/${subject_LO}/$rel_path5/WM_left.nii.gz -force
mrcalc ${subject}_HCP.mif 41 -eq ${DATADIR}/${subject_LO}/$rel_path5/WM_right.nii.gz -force

echo $'\n\n******************Done!****************\n\n'


# if [ -z "$subject" ]
# then
# 	python3 "$CODEDIR/Python/Freesurfer/Connectome_maker.py"
# else
# 	#Warp fsaverage to subject space
# 	for hemi in lh rh
# 	do
# 		mri_surf2surf --srcsubject fsaverage --trgsubject ${subject} --hemi ${hemi} --sval-annot ${DATADIR}/fsaverage/label/${hemi}.HCPMMP1.annot --tval ${DATADIR}/${subject}/label/${hemi}.HCPMMP1.annot
# 	done

# 	#convert annotation to volume
# 	mri_aparc2aseg --s ${subject} --annot HCPMMP1 --o ${subject}_HCP.mgz
# 	mrconvert -datatype uint32 ${subject}_HCP.mgz ${subject}_HCP.mif

# 	#fix annotations to match MRtrix conventions
# 	labelconvert ${subject}_HCP.mif $CODEDIR/Bash/Freesurfer/hcpmmp1_original.txt $CODEDIR/Bash/Freesurfer/hcpmmp1_ordered_edited.txt ${subject}_HCP.nii.gz

# 	#add any nifti volumes present in the folder to the parcellation, following the MRtrix convention
# 	python3 "$CODEDIR/Python/Freesurfer/Connectome_maker.py"
# fi

