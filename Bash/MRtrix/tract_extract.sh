#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=4gb
#SBATCH --time=00:30:00
#SBATCH --job-name=tract_pull
#SBATCH --mail-type=ALL
#SBATCH --output=meso_%j.out

#########

# Pull tracts from connectomes with their sift weighting

# sbatch --mail-user="user"@ufl.edu $CODEDIR/Bash/MRtrix/tract_extract.sh -r 361,366 -s p102 -p All -n Caudate
# OR
# sbatch --mail-user="user"@ufl.edu $CODEDIR/Bash/MRtrix/tract_extract.sh -s p102 -p All -n Caudate
# OR
# sbatch --mail-user="user"@ufl.edu $CODEDIR/Bash/MRtrix/tract_extract.sh -t MDPF -r 361,366 -s p102 -p All -n Caudate


# TODO: Remove mesocircuit_pull.sh and incorporate exemplar data (exemplar_pull.sh)
#########

set -e

if [[ -z "$SYSNAME" ]]; then
echo environment not set.  run makeSysConfig.sh
exit
fi

Help()
{
   # Display Help
   echo
   echo "Syntax: scriptTemplate [-h|r|s|p|n|t|c]"
   echo "options:"
   echo "-h    Help "
   echo "-r    Region(s) to project to. Can be a list. If not specified, all projections (per side) will be produced"
   echo "-s    Subject ID"
   echo "-p    Profile"
   echo "-n    Output Name"
   echo "-t    Target Nuclei Name"
   echo "-c    Contralateral Connections? (y)"
   echo
   echo "Pre-loaded Mesocircuit Regions for -r input, just give the (name), no need for -n either:"
   echo
   echo "(ACC) Anterior Cingulate and Medial Prefrontal Cortex: 58,238,59,239,57,237,180,360,61,241,60,240,179,359,62,242,64,244,165,345,63,243,69,249,65,245,88,268,164,344"
   echo "(Caudate) Caudate: 361,366"
   echo "(DLpfc) DorsoLateral Prefrontal Cortex: 26,206,98,278,97,277,70,250,68,248,67,247,73,253,71,251,87,267,86,266,84,264,85,265,83,263"
   echo "(InfPar) Inferior Parietal Cotrex: 143,323,146,326,145,325,144,324,148,328,116,296,147,327,149,329,150,330,151,331"
   echo "(InsFroOp) Insular and Frontal Opercular Cortex: 103,283,178,358,168,348,167,347,106,286,115,295,110,290,112,292,109,289,114,294,108,288,169,349,111,291"
   echo "(Premotor) Premotor Cortex: 96,276,54,234,10,190,11,191,12,192,56,236,78,258"
   echo "(SomaMot) Somatosensory and Motor Cortex: 8,188,9,189,53,233,51,231,52,232"
   echo "(SupPar) Superior Parietal Cortex: 50,230,48,228,49,229,95,275,117,297,47,227,45,225,42,222,29,209,46,226"
   echo "(TempParOcc) Temporo-Parieto-Occipital Junction: 140,320,141,321,139,319,28,208,25,205"
   echo "(ParaLobMidCC) Paracentral Lobular and Mid Cingulate Cortex: 39,219,36,216,37,217,40,220,41,221,55,235,44,224,43,223"
   echo
}


# Get the options
while getopts ":h:r:s:p:n:t:c:" option; do
   case $option in
      r) regions=$OPTARG;;
      s) subject=$OPTARG;;
      p) profile=$OPTARG;;
      n) name=$OPTARG;;
      t) targ=$OPTARG;;
      c) cont=$OPTARG;;
      h | * | :) Help && exit;;
   esac
done


# Pre-loaded regions
case $regions in
  ACC)
    echo -e "\nACC region given\n"; name=$regions; regions=58,238,59,239,57,237,180,360,61,241,60,240,179,359,62,242,64,244,165,345,63,243,69,249,65,245,88,268,164,344;;
  Caudate)
    echo -e "\nCaudate region given\n"; name=$regions; regions=361,366;;
  DLpfc)
    echo -e "\nDLpfc region given\n"; name=$regions; regions=26,206,98,278,97,277,70,250,68,248,67,247,73,253,71,251,87,267,86,266,84,264,85,265,83,263;;
  InfPar)
    echo -e "\nInfPar region given\n"; name=$regions; regions=143,323,146,326,145,325,144,324,148,328,116,296,147,327,149,329,150,330,151,331;;
  InsFroOp)
    echo -e "\nInsFroOp region given\n"; name=$regions; regions=103,283,178,358,168,348,167,347,106,286,115,295,110,290,112,292,109,289,114,294,108,288,169,349,111,291;;
  Premotor)
    echo -e "\nPremotor region given\n"; name=$regions; regions=96,276,54,234,10,190,11,191,12,192,56,236,78,258;;
  SomaMot)
    echo -e "\nSomaMot region given\n"; name=$regions; regions=8,188,9,189,53,233,51,231,52,232;;
  SupPar)
    echo -e "\nSupPar region given\n"; name=$regions; regions=50,230,48,228,49,229,95,275,117,297,47,227,45,225,42,222,29,209,46,226;;
  TempParOcc)
    echo -e "\nTempParOcc region given\n"; name=$regions; regions=140,320,141,321,139,319,28,208,25,205;;
  ParaLobMidCC)
    echo -e "\nParaLobMidCC region given\n"; name=$regions; regions=39,219,36,216,37,217,40,220,41,221,55,235,44,224,43,223;;
  *)
    echo -e "\nNo pre-loads given, passing regions and name as is\n"
esac

if [ $SYSNAME == "hipergator" ]
then
  module load jq
fi

echo $subject
sub_dir="${DATADIR}/${subject}"
output_dir=${sub_dir}/Tractography/Cleaned/Fibers/${name}
assignment=assignments_${profile}.txt
index_key=MRtrix_index_key_${profile}.csv
mkdir -p ${output_dir}

for side in left right
do
    if [ $SYSNAME == "hipergator" ]
    then
	    module load mrtrix
    fi
    side_big=${side^^}
    side_marker=${side_big:0:1}
    # lookup_name=$(jq -r -c .lookup_table ${sub_dir}/${profile}profile.json)

    if [[ -f "${sub_dir}/${profile}profile.json" ]]; then
    json_file="${sub_dir}/${profile}profile.json"
    elif [[ -f "${sub_dir}/${profile}_profile.json" ]]; then
        json_file="${sub_dir}/${profile}_profile.json"
    else
        echo "No profile JSON found for ${profile}" >&2
        exit 1
    fi

    lookup_name=$(jq -r -c '.lookup_table' "$json_file")

    if [ -z $targ ]
    then
      echo -e "\n No target given, using the profile default\n"
      lookup=$(jq -r -c .${side}_ROI[] ${sub_dir}/${profile}profile.json) #JSON parsing
      roi=$({ read; while IFS=, read -r col1 lookup_index MRtrix_index; do if (( $lookup_index == ${lookup} )); then echo ${MRtrix_index}; fi; done; } < ${sub_dir}/Connectome/${index_key}) #Matrix lookup value
      label_name=$({ read; while IFS=, read -r Index Label File_index Filename Path; do if (( $Index == ${lookup} )); then echo ${Label}; fi; done; } < ${lookup_name}) #ROI name
    else
      echo -e "\nUsing target as ROI"
      label_name=${side_marker}_${targ}
      echo $label_name
      lookup=$({ read; while IFS=, read -r Index Label File_index Filename Path; do if [[ $Label == ${label_name} ]]; then echo ${Index}; fi; done; } < ${lookup_name})
      roi=$({ read; while IFS=, read -r col1 lookup_index MRtrix_index; do if (( $lookup_index == ${lookup} )); then echo ${MRtrix_index}; fi; done; } < ${sub_dir}/Connectome/${index_key})
      echo $roi
      # exit 125
    fi
    roi_name=${label_name##*_} #extract ROI name only, leave out side designation
    echo -e "\n${roi_name} ${side} to ${name}\n"
    tmp_dir=${output_dir}/tmp_${roi_name}_${side}
    mkdir -p $tmp_dir
    if [ -z $regions ]
    then
      nodes=${roi}
      echo -e "\nNo regions Specified, generating all connections\n"
      name=All
      connectome2tck ${sub_dir}/Tractography/Cleaned/Fibers/whole_brain_fibers.tck ${sub_dir}/Tractography/Cleaned/${assignment} ${tmp_dir}/${name}_${nodes} -nodes $nodes -force -files single -tck_weights_in ${sub_dir}/Tractography/Cleaned/Fibers/sift2_weights.txt -prefix_tck_weights_out ${tmp_dir}/${name}_${nodes}
    else
      nodes=''
      for region in ${regions//,/ } #convert lookup index to MRtrix index
      do
        nodes=${nodes},$({ read; while IFS=, read -r col1 lookup_index MRtrix_index; do if (( $lookup_index == ${region} )); then echo ${MRtrix_index}; fi; done; } < ${sub_dir}/Connectome/${index_key})
      done
      nodes=${nodes#*,},${roi}
      echo -e "\nGenerating region-specific connections\n"
      connectome2tck ${sub_dir}/Tractography/Cleaned/Fibers/whole_brain_fibers.tck ${sub_dir}/Tractography/Cleaned/${assignment} ${tmp_dir}/${name}_ -nodes $nodes -exclusive -force -files per_node -tck_weights_in ${sub_dir}/Tractography/Cleaned/Fibers/sift2_weights.txt -prefix_tck_weights_out ${tmp_dir}/${name}_
    fi
    
    cp ${tmp_dir}/${name}_${roi}.csv ${output_dir}/${roi_name}_${side}_${name}.csv
    tcktransform ${tmp_dir}/${name}_${roi}.tck ${sub_dir}/Tractography/Cleaned/transform.mif ${output_dir}/${roi_name}_${side}_${name}_ACPC.tck -force
    if [ -z $cont ]
    then
      echo -e "\nIpsilateral Connections\n"
      if [ $side == "left" ]
      then
        ex_zone=WM_right.nii.gz
      else
        ex_zone=WM_left.nii.gz
      fi
      tckedit ${output_dir}/${roi_name}_${side}_${name}_ACPC.tck -exclude ${sub_dir}/Segmentations/White_matter/${ex_zone} ${output_dir}/${roi_name}_${side}_${name}_ACPC.tck -tck_weights_in ${output_dir}/${roi_name}_${side}_${name}.csv -tck_weights_out ${output_dir}/${roi_name}_${side}_${name}.csv -force
    else
      echo -e "\nContralateral Connections\n"
      if [ $side == "left" ]
      then
        ex_zone=WM_right.nii.gz
      else
        ex_zone=WM_left.nii.gz
      fi
      tckedit ${output_dir}/${roi_name}_${side}_${name}_ACPC.tck -include ${sub_dir}/Segmentations/White_matter/${ex_zone} ${output_dir}/${roi_name}_${side}_${name}_ACPC.tck -tck_weights_in ${output_dir}/${roi_name}_${side}_${name}.csv -tck_weights_out ${output_dir}/${roi_name}_${side}_${name}.csv -force
    fi
    tckconvert ${output_dir}/${roi_name}_${side}_${name}_ACPC.tck ${output_dir}/${roi_name}_${side}_${name}_ACPC.vtk -force
    rm -r ${tmp_dir}
    if [ $SYSNAME == "hipergator" ]
    then
	    module load python
    fi
    python ${CODEDIR}/Python/MRtrix/tckConverter.py ${output_dir}/${roi_name}_${side}_${name}_ACPC.tck  ${output_dir}/${roi_name}_${side}_${name} --tract_data ${output_dir}/${roi_name}_${side}_${name}.csv
    python ${CODEDIR}/Python/MRtrix/Add_Weights_To_VTK.py --input_vtk ${output_dir}/${roi_name}_${side}_${name}_ACPC.vtk --output_vtk ${output_dir}/${roi_name}_${side}_${name}_weights.vtk --tract_data ${output_dir}/${roi_name}_${side}_${name}.tckdata
done

