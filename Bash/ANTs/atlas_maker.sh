#! /bin/sh

# add in SLURM scheduler info
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=10
#SBATCH --mem=16gb
#SBATCH --time=80:00:00
#SBATCH --job-name=ANTs_atlas
#SBATCH --mail-type=ALL
#SBATCH --mail-user=mphook@ufl.edu
#SBATCH --output=ANTs_atlas_%j.out


module load ants
set -e

for file in *_wmn.nii.gz
do
	filename=$(basename $file _wmn.nii.gz)
	antsApplyTransforms -d 3 -i ${filename}_brainmask.nii.gz -r $file -o ${filename}_brainmask_resamp.nii.gz -n Linear #resampling data
	N4BiasFieldCorrection -d 3 -s 4 -r 0 -b "[200]" -c "[100x100x100x100,1e-07]" -i $file -o ${filename}_wmn_bfc.nii.gz -x ${filename}_brainmask_resamp.nii.gz --verbose 1 #two step bias correction
	N4BiasFieldCorrection -d 3 -s 2 -r 0 -b "[150]" -c "[100x100x100x100,1e-07]" -i ${filename}_wmn_bfc.nii.gz -o ${filename}_wmn_bfc.nii.gz -x ${filename}_brainmask_resamp.nii.gz --verbose 1
done


antsMultivariateTemplateConstruction2.sh -d 3 -o Atlas_ -i 4 -g 0.2 -c 2 -j 8 -k 1 -w 1 -f 6x4x2x1 -s 3x2x1x0 -q 100x100x75x20 -n 0 -r 1 -l 1 -m CC[2] -t BSplineSyN[0.1,26,0] *_wmn_bfc.nii.gz