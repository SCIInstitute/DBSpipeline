#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=8gb
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

if [ $SYSNAME == "hipergator" ]
then
  rel_path1="Connectome"
  rel_path2="Tractography"
else
  rel_path1="MRtrix/Connectome"
  rel_path2="MRtrix/Tractography"
fi


Help()
{
   # Display Help
   echo
   echo "options:"
   echo "-h    Help Page"
#   echo "-L    Path to Lookup Table"
   echo "-s    Path to Subjects List"
   echo "-d  path to subjects directory (will run all subjects)"
   echo
}

#lookup="${CODEDIR}/Bash/Freesurfer/connectome_lookup.csv"
# Get the options
while getopts ":h:L:s:" option; do
   case $option in
      d) d_dir=$OPTARG;;
      s) subjects=$OPTARG;;
      h | * | :) Help && exit;;
   esac
done

#if [ -z "$lookup" ]
#then
#    echo "ERROR: must supply lookup table"
#    exit 1
#fi
if ([ -z "$subjects" ] && [ -z "$d_dir" ])
then
    echo "ERROR: must supply list of subjects or directory to subjects"
    exit 1
fi

if [ -d "$d_dir" ]
then
  echo "running all subjects in : "
  echo "$d_dir"
  subjects_list=($(getSubjectsFromDir $d_dir))
else
  echo "Directory input not found:"
  echo "$d_dir"

  if [ -z "$subjects" ]
  then
    echo "ERROR: must supply list of subjects or directory to subjects"
    exit 1
  else
    echo "using list of subjects in:"
    echo "$subjects"
    readarray -t subjects_list < "$subjects"
#    subjects_list=("${(@f)$(< ${subjects} )}")
  fi
fi

echo ${#subjects_list[@]}



for subject in ${subjects_list[@]}
do
  echo $subject
  
  files=($(ls -1 "${DATADIR}"/"${subject}"/"${rel_path1}"/Stim/HCP_parc_all_*.nii.gz))
  
  for file in ${files[@]}
  do
    echo $file
    
    if [ $SYSNAME == "hipergator" ]
    then
      module load mrtrix
    fi
    
    filename=$(basename $file .nii.gz)
    
    mrtransform -linear "${DATADIR}"/"${subject}"/ACPC_to_b0.txt $file "${DATADIR}"/"${subject}"/"${rel_path1}"/HCP_parc_all_b0space.nii.gz  -force
    connectome_matrix="${DATADIR}"/"${subject}"/"${rel_path1}"/connectome_matrix_${filename: -1}.csv
    tck2connectome "${DATADIR}"/"${subject}"/"${rel_path2}"/whole_brain_fibers.tck "${DATADIR}"/"${subject}"/"${rel_path1}"/HCP_parc_all_b0space.nii.gz $connectome_matrix -tck_weights_in "${DATADIR}"/"${subject}"/"${rel_path2}"/sift2_weights.txt  -keep_unassigned -assignment_radial_search 3 -out_assignments "${DATADIR}"/"${subject}"/"${rel_path2}"/assignments_${filename: -1}.txt -force
        #-scale_invlength \
        #-scale_invnodevol
    
    
    if [ $SYSNAME == "hipergator" ]
    then
      module load python/3.10
    fi
    
    python calculate_connectome.py --matrix "$connectome_matrix" --subject ${subject} --left_ROI 371 --right_ROI 372
  done
done



getSubjectsFromDir() {
  local d_dir="$1"
  
  local files=($(ls -1d $d_dir/*))
  
  for f in ${files[@]}
  do
    if ([ -d "$f"/"$rel_path1" ] && [ -d "$f"/"$rel_path2" ] && [ -d "$f"/"$rel_path3" ])
    then
      echo $(basename $f)
    fi
  done
}
