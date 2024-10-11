#! /bin/sh
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=64gb
#SBATCH --time=1:00:00
#SBATCH --job-name=ANTS_rigid
#SBATCH --mail-type=ALL
#SBATCH --mail-user=mphook@ufl.edu
#SBATCH --output=ANTs_rigid_%j.out
date;hostname;pwd

module load itk ants
img_fixed=$1
img_moving=$2

antsRegistration \
-d 3 \
-m MI[$img_fixed,$img_moving,1,100,Random,.2] \
-t Rigid[.01] \
-c [500x500x500,1e-6,100] \
-s 2x2x1vox \
-f 3x2x1 \
-l 1 \
-u \
-o rigid_

filename=$(basename $img_moving .nii.gz)
antsApplyTransforms -d 3 \
-i $img_moving \
-o ${filename}_registered.nii.gz \
-r $img_fixed \
-t *0GenericAffine.mat

date
