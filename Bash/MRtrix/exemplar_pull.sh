#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=8gb
#SBATCH --time=1:00:00
#SBATCH --job-name=exemplar
#SBATCH --mail-type=ALL
#SBATCH --output=exemplar_%j.out


#########

# Pull exemplars from connectomes, currently runs without exclusive

# sbatch --mail-user="user"@ufl.edu $CODEDIR/Bash/MRtrix/exemplar_pull.sh -s p102 -e Brainstem -r 371,386 -n CL_bilat

#########

set -e

if [[ -z "$SYSNAME" ]]; then
echo environment not set.  run makeSysConfig.sh
exit
fi

if [ $SYSNAME == "hipergator" ]
then
	module load mrtrix
fi

Help()
{
   # Display Help
   echo
   echo "Syntax: scriptTemplate [-h|s|e|r|n|:]"
   echo "options:"
   echo "-h    Help "
   echo "-s    Subject ID"
   echo "-e    Experiment Name"
   echo "-r    Regions"
   echo "-n    Output File Name"
   echo
}


# Get the options
while getopts ":h:s:e:r:n:" option; do
   case $option in
      s) subject=$OPTARG;;
      e) experiment=$OPTARG;;
      r) ROI=$OPTARG;;
      n) filename=$OPTARG;;
      h | * | :) Help && exit;;
   esac
done

echo $subject
echo $experiment
echo $ROI
echo $filename

tract_dir="${DATADIR}/${subject}/Tractography/Cleaned"
connect_dir="${DATADIR}/${subject}/Connectome"
mkdir -p ${tract_dir}/Fibers/${filename}_exemplar
output_dir=${tract_dir}/Fibers/${filename}_exemplar

mrtransform -linear ${tract_dir}/ACPC_to_b0.txt ${connect_dir}/HCP_parc_all_${experiment}.nii.gz ${output_dir}/nodes.nii.gz -force

connectome2tck ${tract_dir}/Fibers/whole_brain_fibers.tck ${tract_dir}/assignments_${experiment}.txt ${output_dir}/${filename}_raw.tck -nodes $ROI -files single -exemplars ${output_dir}/nodes.nii.gz -tck_weights_in ${tract_dir}/Fibers/sift2_weights.txt -prefix_tck_weights_out ${output_dir}/${filename}_raw -keep_self -force
tckedit ${output_dir}/${filename}_raw.tck ${output_dir}/${filename}.tck -tck_weights_in ${output_dir}/${filename}_raw.csv -tck_weights_out ${output_dir}/${filename}.csv -minweight 1.001 -force
tcktransform ${output_dir}/${filename}.tck ${tract_dir}/transform.mif ${output_dir}/${filename}_ACPC.tck -force
tckconvert ${output_dir}/${filename}_ACPC.tck ${output_dir}/${filename}_ACPC.vtk -force

if [ $SYSNAME == "hipergator" ]
then
	module load python
fi

python ${CODEDIR}/Python/MRtrix/tckConverter.py ${output_dir}/${filename}_ACPC.tck ${output_dir}/${filename} --tract_data ${output_dir}/${filename}.csv
python ${CODEDIR}/Python/MRtrix/Add_Weights_To_VTK.py --input_vtk ${output_dir}/${filename}_ACPC.vtk --output_vtk ${output_dir}/${filename}_data.vtk --tract_data ${output_dir}/${filename}.tckdata

#temporary
python exemplar_regions.py --raw ${output_dir}/${filename}_raw.csv --profile ${DATADIR}/${subject}/${experiment}profile.json --macro ${CODEDIR}/Python/connectomics/connectome_maps/HCP_MacroRegions.json