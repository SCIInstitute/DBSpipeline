#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=1gb
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
if [ -z "$subjects"]
then
    echo "ERROR: must supply list of subjects"
    exit 1
fi

sub_dir=/home/mphook/blue_butsonc/share/Connectome

while read subject || [ -n '$subject' ]
do
    echo $subject
    module load python/3.10
    python DBSpipeline/Python/Freesurfer/Connectome_maker.py --filepath $sub_dir --subject $subject --lookup $lookup
    
    module load mrtrix
    mrtransform -linear ${sub_dir}/${subject}/Cleaned/ACPC_to_b0.txt \
        ${sub_dir}/${subject}/Connectome/HCP_parc_all.nii.gz \
        ${sub_dir}/${subject}/Connectome/HCP_parc_all_b0space.nii.gz -force
        
    tck2connectome ${sub_dir}/${subject}/Cleaned/Fibers/whole_brain_fibers.tck \
        ${sub_dir}/${subject}/Connectome/HCP_parc_all_b0space.nii.gz \
        ${sub_dir}/${subject}/Connectome/connectome_matrix.csv \
        -tck_weights_in ${sub_dir}/${subject}/Cleaned/Fibers/sift2_weights.txt \
        -keep_unassigned \
        -assignment_radial_search 3 \
        -out_assignments ${sub_dir}/${subject}/Cleaned/Fibers/assignments.txt \
        -scale_invlength \
        -scale_invnodevol \
        -force
        

:'
module load mrtrix
for d in */
do
	echo $d
	mrtransform -linear ${PWD}/${d}Cleaned/ACPC_to_b0.txt ${PWD}/${d}Cleaned/Fibers/HCP_parc_all.nii.gz ${PWD}/${d}Cleaned/Fibers/HCP_parc_all_b0space.nii.gz -force

	tck2connectome ${PWD}/${d}Cleaned/Fibers/whole_brain_fibers.tck ${PWD}/${d}Cleaned/Fibers/HCP_parc_all_b0space.nii.gz ${PWD}/${d}Cleaned/Fibers/connectome_matrix.csv \
	    -tck_weights_in ${PWD}/${d}Cleaned/Fibers/sift2_weights.txt \
	    -keep_unassigned \
	    -assignment_radial_search 3 \
	    -out_assignments ${PWD}/${d}Cleaned/Fibers/assignments.txt \
	    -scale_invlength \
	    -scale_invnodevol \
	    -force
done

module load python/3.10
for d in */
do
	echo $d
	python calculate_connectome.py --subject $d --left_ROI 371 --right_ROI 372
done
'