#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=4gb
#SBATCH --time=1:00:00
#SBATCH --job-name=Connectome
#SBATCH --mail-type=ALL
#SBATCH --output=Connectome_%j.out

# example call
# sbatch --mail-user=jess.tate@ufl.edu calculate_connectome.sh -s  /blue/butsonc/Butson_Lab/Connectome/Testing/SubjectsShort.txt

if [[ -z "$SYSNAME" ]]; then
echo environment not set.  run makeSysConfig.sh
exit
fi

set -e

Help()
{
   # Display Help
   echo
   echo "options:"
   echo "-h    Help Page"
#   echo "-L    Path to Lookup Table"
   echo "-s    Path to Subjects List"
   echo
}

#lookup="${CODEDIR}/Bash/Freesurfer/connectome_lookup.csv"
# Get the options
while getopts ":h:L:s:" option; do
   case $option in
#      L) lookup=$OPTARG;;
      s) subjects=$OPTARG;;
      h | * | :) Help && exit;;
   esac
done

#if [ -z "$lookup" ]
#then
#    echo "ERROR: must supply lookup table"
#    exit 1
#fi
if [ -z "$subjects" ]
then
    echo "ERROR: must supply list of subjects"
    exit 1
fi



while read subject
do
    echo $subject
    
    if [ $SYSNAME == "hipergator" ]
    then
      module load python/3.10
    fi

    
    python "${CODEDIR}/Python/Freesurfer/Connectome_maker.py" --subject $subject
    echo $subject
    
    if [ $SYSNAME == "hipergator" ]
    then
      module load mrtrix
    fi
    
    mrtransform -linear ${DATADIR}/${subject}/Tractography/Cleaned/ACPC_to_b0.txt \
           ${DATADIR}/${subject}/Connectome/HCP_parc_all.nii.gz \
           ${DATADIR}/${subject}/Connectome/HCP_parc_all_b0space.nii.gz -force
        
    tck2connectome  ${DATADIR}/${subject}/Tractography/Cleaned/Fibers/whole_brain_fibers.tck \
        ${DATADIR}/${subject}/Connectome/HCP_parc_all_b0space.nii.gz \
        ${DATADIR}/${subject}/Connectome/connectome_matrix.csv \
        -tck_weights_in ${DATADIR}/${subject}/Tractography/Cleaned/Fibers/sift2_weights.txt \
        -keep_unassigned \
        -assignment_radial_search 3 \
        -out_assignments ${DATADIR}/${subject}/Tractography/Cleaned/Fibers/assignments.txt \
        -scale_invlength \
        -scale_invnodevol \
        -force
        
done < <(grep '' $subjects)

'
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
