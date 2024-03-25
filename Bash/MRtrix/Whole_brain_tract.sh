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

. $(dirname $(readlink -f $0))/../../scripts/sysUtils.sh

innitBashPaths -v


handle_options "$@"


if [ $SYSNAME == "hipergator" ]
then
module load fsl
module load freesurfer
module load mrtrix
module load python/3.10
fi

set -e
mkdir -p Fibers

# running in CWD, so run in subject dir?
# ${subject}/Tractography dir
T1file=Cleaned/T1_5tt.nii.gz
seed_dy=Cleaned/wmfod_norm.mif
out_tck=Fibers/whole_brain_fibers.tck
first_tckgen="tckgen -act $T1file -seed_dynamic $seed_dy -select 10000000 -cutoff 0.1 $seed_dy $out_tck -force"

if [ "$dryrun" = false ]; then
  eval "$first_tckgen"
else
  check=($(ls -1 $T1file $seed_dy $out_tck ))
  echo "$check[@]"
  echo "$first_tckgen"
fi


#Resampling
for file in Fibers/*fibers.tck
do
	filename=$(basename $file .tck)
  tck_res="tckresample -step_size 0.5 $file $file -force"
  if [ "$dryrun" = false ]; then
   eval "$tck_res"
  else
    echo $file
    echo $filename
    echo "$tck_res"
done

mu_file=Fibers/sift2_mu.txt
weights_file=Fibers/sift2_weights.txt

tck_sh_1="tcksift2 -act $T1file -out_mu $mu_file $out_tck $seed_dy $weights_file"
if [ "$dryrun" = false ]; then
  eval "$tck_sh_1"
else
  check=($(ls -1 $T1file -out_mu $mu_file $out_tck $seed_dy $weights_file))
  echo "$check[@]"
  echo "$tck_sh_1"
fi

$out_tck_100k=Fibers/whole_brain_100k_fibers.tck
ted="tckedit $out_tck -number 100k $out_tck_100k"

if [ "$dryrun" = false ]; then
  eval "$ted"
else
  check=($(ls -1 $out_tck $out_tck_100k))
  echo "$check[@]"
  echo "$ted"
fi


#Moving to ACPC space
warpinit Cleaned/T1_ACPC.nii.gz Cleaned/warp.mif -force
mrtransform warp.mif -linear Cleaned/ACPC_to_b0.txt Cleaned/transform.mif -template Cleaned/b0_hifi.nii.gz -interp cubic -nan -force
tcktransform Fibers/whole_brain_100k_fibers.tck Cleaned/transform.mif Fibers/whole_brain_100k_fibers_ACPC.tck -force

mkdir -p SCIRun_files
#File Conversion to SCIRun

python $CODEDIR/Python/MRtrix/tckConverter.py Fibers/whole_brain_100k_fibers_ACPC.tck SCIRun_files/whole_brain_100k

#for file in Fibers/*_fibers_ACPC.tck; do filename=$(basename $file _fibers_ACPC.tck); python3 tckConverter.py $file SCIRun_files/$filename; done
