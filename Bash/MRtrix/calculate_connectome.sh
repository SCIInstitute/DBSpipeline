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

module load mrtrix
set -e
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
