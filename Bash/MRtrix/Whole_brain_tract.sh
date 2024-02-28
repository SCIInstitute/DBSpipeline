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

module load fsl
module load freesurfer
module load mrtrix
set -e
mkdir -p Fibers

tckgen -act T1_5tt.nii.gz -seed_dynamic wmfod_norm.mif -select 10000000 -cutoff 0.1 wmfod_norm.mif Fibers/whole_brain_fibers.tck -force

#Resampling
for file in Fibers/*fibers.tck
do
	filename=$(basename $file .tck)
	tckresample -step_size 0.5 $file $file -force
done

tcksift2 -act T1_5tt.nii.gz -out_mu Fibers/sift2_mu.txt Fibers/whole_brain_fibers.tck wmfod_norm.mif Fibers/sift2_weights.txt

tckedit Fibers/whole_brain_fibers.tck -number 100k Fibers/whole_brain_100k_fibers.tck

#Moving to ACPC space
warpinit T1_ACPC.nii.gz warp.mif -force
mrtransform warp.mif -linear ACPC_to_b0.txt transform.mif -template b0_hifi.nii.gz -interp cubic -nan -force
tcktransform Fibers/whole_brain_100k_fibers.tck transform.mif Fibers/whole_brain_100k_fibers_ACPC.tck -force

mkdir -p SCIRun_files
cp /home/mphook/blue_butsonc/mphook/MRtrix/tckConverter.py .
#File Conversion to SCIRun
module load python/3.10
python tckConverter.py Fibers/whole_brain_100k_fibers_ACPC.tck SCIRun_files/whole_brain_100k

#for file in Fibers/*_fibers_ACPC.tck; do filename=$(basename $file _fibers_ACPC.tck); python3 tckConverter.py $file SCIRun_files/$filename; done