#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=8gb
#SBATCH --time=1:00:00
#SBATCH --job-name=Connectome
#SBATCH --mail-type=ALL
#SBATCH --mail-user=mphook@ufl.edu
#SBATCH --output=Connectome_%j.out

set -e

Help()
{
   # Display Help
   echo
   echo "options:"
   echo "-h    Help Page"
   echo "-L    Path to Lookup Table"
   echo "-s    Path to Subjects List"
   echo
}


# Get the options
while getopts ":h:L:s:" option; do
   case $option in
      L) lookup=$OPTARG;;
      s) subjects=$OPTARG;;
      h | * | :) Help && exit;;
   esac
done

if [ -z "$lookup" ]
then
    echo "ERROR: must supply lookup table"
    exit 1
fi
if [ -z "$subjects" ]
then
    echo "ERROR: must supply list of subjects"
    exit 1
fi

git_dir=/home/mphook/blue_butsonc/mphook/Github/

while read subject
do
    echo $subject
    module load python/3.10
    python ${git_dir}DBSpipeline/Python/Freesurfer/Connectome_maker.py --subject $subject --lookup $lookup
    module load mrtrix
    mrtransform -linear ${subject}/Tractography/Cleaned/ACPC_to_b0.txt \
        ${subject}/Connectome/HCP_parc_all.nii.gz \
        ${subject}/Connectome/HCP_parc_all_b0space.nii.gz -force
        
    tck2connectome ${subject}/Tractography/Cleaned/Fibers/whole_brain_fibers.tck \
        ${subject}/Connectome/HCP_parc_all_b0space.nii.gz \
        ${subject}/Connectome/connectome_matrix.csv \
        -tck_weights_in ${subject}/Tractography/Cleaned/Fibers/sift2_weights.txt \
        -keep_unassigned \
        -assignment_radial_search 3 \
        -out_assignments ${subject}/Tractography/Cleaned/Fibers/assignments.txt \
        -scale_invlength \
        -scale_invnodevol \
        -force
        
done < <(grep '' $subjects)

#module load python/3.10
#for d in */
#do
#	echo $d
#	python calculate_connectome.py --subject $d --left_ROI 371 --right_ROI 372
#done
