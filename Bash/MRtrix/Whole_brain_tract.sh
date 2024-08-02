#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=30gb
#SBATCH --time=20:00:00
#SBATCH --job-name=tckgen
#SBATCH --mail-type=ALL
#SBATCH --mail-user=mphook@ufl.edu
#SBATCH --output=tckgen_%j.out

# example call
# sbatch --mail-user=jess.tate@ufl.edu Whole_brain_tract.sh S1


if [[ -z "$SYSNAME" ]]; then
echo environment not set.  run makeSysConfig.sh
exit
fi

if [[ -z $1 ]]; then
echo required input: subject name
exit
fi

dryrun=false

subject=$1
sub_dir="${DATADIR}/${subject}"

if [ ! -d "$sub_dir" ]
then
echo "Subject directory does not exist: ${sub_dir}"
exit
fi


if [ $SYSNAME == "hipergator" ]
then
module load fsl
module load freesurfer
module load mrtrix
fi

set -e

if [[ $SYSNAME == "hipergator" ]]
then
  rel_path1="Connectome"
  rel_path2="Tractography/Cleaned"
  rel_path3="Tractography/Cleaned/Fibers"
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


mkdir -p ${sub_dir}/${rel_path3}

# running in CWD, so run in subject dir?
# ${subject}/Tractography dir
T1file=${sub_dir}/${rel_path2}/T1_5tt.nii.gz
seed_dy=${sub_dir}/${rel_path2}/wmfod_norm.mif
out_tck=${sub_dir}/${rel_path3}/whole_brain_fibers.tck

first_tckgen="tckgen -act $T1file -seed_dynamic $seed_dy -select 10000000 -cutoff 0.1 $seed_dy $out_tck -force"

if [ "$dryrun" = false ]; then
  eval "$first_tckgen"
else
  check=($(ls -1 $T1file $seed_dy $out_tck ))
  echo "$check[@]"
  echo "$first_tckgen"
fi


#Resampling
for file in ${sub_dir}/${rel_path3}/*fibers.tck
do
	filename=$(basename $file .tck)
  tck_res="tckresample -step_size 0.5 $file $file -force"
  if [ "$dryrun" = false ]; then
   eval "$tck_res"
  else
    echo $file
    echo $filename
    echo "$tck_res"
  fi
done

mu_file=${sub_dir}/${rel_path3}/sift2_mu.txt
weights_file=${sub_dir}/${rel_path3}/sift2_weights.txt

tck_sh_1="tcksift2 -act $T1file -out_mu $mu_file $out_tck $seed_dy $weights_file"
if [ "$dryrun" = false ]; then
  eval "$tck_sh_1"
else
  check=($(ls -1 $T1file $mu_file $out_tck $seed_dy $weights_file))
  echo "$check[@]"
  echo "$tck_sh_1"
fi

out_tck_100k=${sub_dir}/${rel_path3}/whole_brain_100k_fibers.tck
ted="tckedit $out_tck -number 100k $out_tck_100k"

if [ "$dryrun" = false ]; then
  eval "$ted"
else
  check=($(ls -1 $out_tck $out_tck_100k))
  echo "$check[@]"
  echo "$ted"
fi


T1_acpc_fname=${sub_dir}/${rel_path2}/T1_ACPC.nii.gz
warp_fname=${sub_dir}/${rel_path2}/warp.mif
ACPC_fname=${sub_dir}/${rel_path2}/ACPC_to_b0.txt
Trans_fname=${sub_dir}/${rel_path2}/transform.mif
b0_fname=${sub_dir}/${rel_path2}/b0_hifi.nii.gz
out_tck_100k_ACPC=${sub_dir}/${rel_path3}/whole_brain_100k_fibers_ACPC.tck


#Moving to ACPC space
warp_call="warpinit ${T1_acpc_fname} ${warp_fname} -force"
mrtrans_call="mrtransform ${warp_fname} -linear ${ACPC_fname} ${Trans_fname} -template ${b0_fname} -interp cubic -nan -force"
tcktrans_call="tcktransform ${out_tck_100k} ${Trans_fname} ${out_tck_100k_ACPC} -force"
if [ "$dryrun" = false ]; then
  eval "$warp_call"
  eval "$mrtrans_call"
  eval "$tcktrans_call"
else
  check=($(ls -1 ${T1_acpc_fname} ${warp_fname} ${ACPC_fname} ${Trans_fname} ${b0_fname} ${out_tck_100k_ACPC}))
  echo "$check[@]"
  echo "$warp_call"
  echo "$mrtrans_call"
  echo "$tcktrans_call"
fi





mkdir -p ${sub_dir}/SCIRun_files
#File Conversion to SCIRun



if [ $SYSNAME == "hipergator" ]
then
module load python/3.10
fi

sr_out_tck_100K=${sub_dir}/SCIRun_files/whole_brain_100k
py_call="python $CODEDIR/Python/MRtrix/tckConverter.py ${out_tck_100k_ACPC} ${sr_out_tck_100K}"

if [ "$dryrun" = false ]; then
  eval "$py_call"
else
  check=($(ls -1 ${out_tck_100k_ACPC} ${sr_out_tck_100K}.edge ${sr_out_tck_100K}.pts ))
  echo "$check[@]"
  echo "$py_call"
fi


#for file in Fibers/*_fibers_ACPC.tck; do filename=$(basename $file _fibers_ACPC.tck); python3 tckConverter.py $file SCIRun_files/$filename; done
