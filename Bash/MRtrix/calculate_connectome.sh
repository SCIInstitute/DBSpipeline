#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=32gb
#SBATCH --time=6:00:00
#SBATCH --job-name=Connectome
#SBATCH --mail-type=ALL
#SBATCH --output=Connectome_L_%j.out

# example call
# sbatch --mail-user="user"@ufl.edu calculate_connectome.sh -l  /blue/butsonc/Butson_Lab/Connectome/Testing/SubjectsShort.txt

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
  module load ants
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
   echo "-l    Path to Subjects List"
   echo "-d  path to subjects directory (will run all subjects)"
   echo "-f  force rerun connectome maker"
   echo "-u  force upgrade of connectome maker data"
   echo "-r  radius of assignment method [3]"
   echo "-t  test run"
   echo "-e  experiment tag to run"
   echo "-a  assignment method [\"assignment_radial_search 3\"].  options from MRtrix: https://mrtrix.readthedocs.io/en/dev/reference/commands/tck2connectome.html#options"
   echo "-s run stimulated regions.  requires extra files"
   echo "-i begining index to use for stimulation regions in Connectome_maker.py"
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
  local experiment="$7"
  local stim=$8
  local stim_index="$9"
  local upgrade=${10}
  local atlas_mapping="${11}"
  
#  files=($(ls -1 "${DATADIR}/${subject}/${rel_path1}/Stim/HCP_parc_all_"*".nii.gz"))
  
#  subject_path="${DATADIR}/${subject}/${rel_path1}/Stim/"
#  subject_path="${DATADIR}/${subject}/${rel_path1}/"
  subject_path="${DATADIR}/${subject}/"
#  file_pattern="HCP_parc_all_*.nii.gz"

#  echo $file_pattern
  echo "$subject_path"
  
# pfiles=($(ls -1 ${subject_path}/{${subject}{\-,\.,_,},}${experiment}{,_,-,.}profile.json 2>/dev/null || true ))
#  echo ${#pfiles[@]}
#  for file in ${pfiles[@]}

  
  find "$subject_path" -type f \( -name "${experiment}[\-,\.,_]profile.json" -o -name "${experiment}profile.json" \) -print0 | while IFS= read -r -d '' file;
  do
    echo "file = $file"
    
#    if [[ $file == *"/HCP_parc_all_b0space.nii.gz" ]]
#    then
#      continue
#    fi

    echo "rerun: $rerun testrun: $testrun radius: $radius mdist: $mdist stim: $stim upgrade: $upgrade"
    
    if [ "$SYSNAME" == "hipergator" ]
    then
      module load python/3.10
    fi

    python_call="python ${CODEDIR}/Python/Freesurfer/Connectome_maker.py -p ${file}"
    if [ "$upgrade" = true ] ; then
      python_call=$python_call" -u"
      rerun=true
    fi
    if [ "$rerun" = true ] ; then
      python_call=$python_call" -f"
    fi
    if [ "$stim" = true ] ; then
      python_call=$python_call" -s"
    fi
    
    if [ -n "$stim_index" ] ; then
      python_call="$python_call -i ${stim_index}"
    fi
    
    if [ -n "$atlas_mapping" ] ; then
      python_call="$python_call -m ${atlas_mapping}"
    fi
    
    
    if [ "$testrun" = true ]; then
      echo "this is the call that would run: "
      echo $python_call
    else
      echo "running: "
      echo $python_call
      $python_call
    fi
        
    # heres where to add connectome maker
    python_call="python ${CODEDIR}/Python/MRtrix/makeConnectomeMatrix.py -p ${file} -a ${assignment} -r ${radius} -d ${mdist}"
    # upgrade not implemented in these other scripts
    if [ "$rerun" = true ] ; then
      python_call=$python_call" -f"
    fi
    if [ "$stim" = true ] ; then
      python_call=$python_call" -s"
    fi
    if [ "$testrun" = true ]; then
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
    # upgrade not yet implemented
    if [ "$rerun" = true ] ; then
      python_call=$python_call" -f"
    fi
    if [ "$stim" = true ] ; then
      python_call=$python_call" -s"
    fi
    
    if [ "$testrun" = true ]; then
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
upgrade=false
stim=false

while getopts "hd:l:a:r:tfum:e:si:p:" option; do
   case $option in
      d) d_dir=$OPTARG;;
      l) subjects=$OPTARG;;
      a) assignment=$OPTARG;;
      r) radius=$OPTARG;;
      t) testrun=true;;
      f) rerun=true;;
      u) upgrade=true;;
      m) mdist=$OPTARG;;
      e) experiment=$OPTARG;;
      s) stim=true;;
      i) stim_index=$OPTARG;;
      p) atlas_mapping=$OPTARG;;
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
      run_loop "$subject" "$assignment" "$rerun" "$testrun" "$radius" "$mdist" "$experiment" "$stim" "$stim_index" "$upgrade" "$atlas_mapping"
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
      
      run_loop "$subject" "$assignment" "$rerun" "$testrun" "$radius" "$mdist" "$experiment" "$stim" "$stim_index" "$upgrade" "$atlas_mapping"

    done < "$subjects"
  fi
fi





