#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=8gb
#SBATCH --time=3:00:00
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

if [[ $SYSNAME == "hipergator" ]]
then
  rel_path1="Connectome"
  rel_path2="Tractography"
  rel_path3="Tractography"
  rel_path4="Segmentations"
  module load jq
else
#  rel_path1="MRtrix/Connectome"
#  rel_path2="MRtrix/Tractography/Cleaned"
#  rel_path3="MRtrix/Tractography/Fibers"
#  rel_path4="MRtrix/Segmentations"
  rel_path1="Connectome"
  rel_path2="Tractography/Cleaned"
  rel_path3="Tractography/Cleaned/Fibers"
  rel_path4="Segmentations"
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
   echo "-f  force rerun connectome maker"
   echo "-r  radius of assignment method [3]"
   echo "-t  test run"
   echo "-e  experiment tag to run"
   echo "-a  assignment method [\"assignment_radial_search 3\"].  options from MRtrix: https://mrtrix.readthedocs.io/en/dev/reference/commands/tck2connectome.html#options"
   echo
}

#default_assignment="assignment_radial_search 3"
default_assignment="assignment_end_voxels"



getSubjectsFromFile() {
  local subs="$1"
  
  while read -r line;
    do
    echo -e "${line}\n"
  done < "$subs"
#  echo $sub_list
}

run_loop() {
  local subject="$1"
  local assignment="$2"
  local rerun=$3
  local testrun=$4
  local radius=$5
  local mdist=$6
  local experiment=$7
  
#  files=($(ls -1 "${DATADIR}/${subject}/${rel_path1}/Stim/HCP_parc_all_"*".nii.gz"))
  
#  subject_path="${DATADIR}/${subject}/${rel_path1}/Stim/"
#  subject_path="${DATADIR}/${subject}/${rel_path1}/"
  subject_path="${DATADIR}/${subject}/"
#  file_pattern="HCP_parc_all_*.nii.gz"
  file_pattern=$experiment"*profile.json"

  
#  echo ${#files[@]}
  
  find "$subject_path" -type f -name "$file_pattern" -print0 | while IFS= read -r -d '' file;
  do
    echo "file = $file"
    
#    if [[ $file == *"/HCP_parc_all_b0space.nii.gz" ]]
#    then
#      continue
#    fi

    echo "rerun: $rerun testrun: $testrun radius: $radius mdist: $mdist"
    
    if [ $SYSNAME == "hipergator" ]
    then
      module load python/3.10
    fi

    python_call="python ${CODEDIR}/Python/Freesurfer/Connectome_maker.py -p ${file}"
    if [ $rerun = true ] ; then
      python_call=$python_call" -f"
    fi
    
    if [ $testrun = true ]; then
      echo "this is the call that would run: "
      echo $python_call
    else
      echo "running: "
      echo $python_call
      $python_call
    fi
        
    # heres where to add connectome maker
    python_call="python ${CODEDIR}/Python/MRtrix/makeConnectomeMatrix.py -p ${file} -a ${assignment} -r ${radius} -d ${mdist}"
    
    if [ $testrun = true ]; then
      echo "this is the call that would run: "
      echo $python_call
    else
      echo "running: "
      echo $python_call
      $python_call
    fi
    
#    echo "${CODEDIR}"
#    echo "${connectome_matrix}"
#    echo "${file}"
    
    python_call="python ${CODEDIR}/Python/MRtrix/calculate_connectome.py -p ${file}"
    
    if [ $testrun = true ]; then
      echo "this is the call that would run: "
      echo $python_call
    else
      echo "running: "
      echo $python_call
      $python_call
    fi

  done
}

#==========================

# Get the options

testrun=false
rerun=false

while getopts "hd:s:a:r:tfm:e:" option; do
   case $option in
      d) d_dir=$OPTARG;;
      s) subjects=$OPTARG;;
      a) assignment=$OPTARG;;
      r) radius=$OPTARG;;
      t) testrun=true;;
      f) rerun=true;;
      m) mdist=$OPTARG;;
      e) experiment=$OPTARG;;
      h | * | :) Help && exit;;
   esac
done

if [ -z "$assignment" ]
then
    echo "using default assignment"
    assignment=$default_assignment
fi

echo "$assignment"


if [ -z "$experiment" ]
then
    echo "running all profiles"
    experiment=""
else
    echo "running experiment profiles with: $experiment"
fi

if [ -z "$radius" ]
then
    echo "using default assignment radius"
    radius=3
fi

if [ -z "$mdist" ]
then
    echo "using default assignment max distance"
    mdist=0
fi

if ([ -z "$subjects" ] && [ -z "$d_dir" ])
then
    echo "ERROR: must supply list of subjects or directory to subjects"
    exit 1
fi

if [ -d "$d_dir" ]
then

  echo "running all subjects in : "
  echo "$d_dir"
  
#  sfiles=($(ls -1d "$d_dir/"*))
#  
#  echo ${#sfiles[@]}
#  echo $sfiles
#  echo "looping"

  find "$d_dir" -maxdepth 1 -type d -print0 | while read -r -d $'\0' sf;
  do
#    echo "checking dir $sf"

    if ([ -d "$sf/$rel_path1" ] && [ -d "$sf/$rel_path2" ] && [ -d "$sf/$rel_path4" ])
    then
      subject=$(basename "$sf")
      echo "valid subject: $subject"
      run_loop "$subject" "$assignment" $rerun $testrun $radius $mdist $experiment
#    else
#      echo "skipping $sf"
    fi
  done

else
  echo "Directory input not found:"
  echo "$d_dir"

  if [ -z "$subjects" ]
  then
    echo "ERROR: must supply list of subjects or directory to subjects"
    exit 1
  else
    echo "using list of subjects in:"
    echo "${subjects}"
    while read -r subject;
    do
      echo "$subject"
      
      run_loop "$subject" "$assignment" $rerun $testrun $radius $mdist $experiment

    done < "$subjects"
  fi
fi





