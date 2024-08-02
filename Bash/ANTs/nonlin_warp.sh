#! /bin/sh
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=90gb
#SBATCH --time=12:00:00
#SBATCH --job-name=nonlin_warp
#SBATCH --mail-type=ALL
#SBATCH --mail-user=mphook@ufl.edu
#SBATCH --output=ANTs_nonlin_warp_%j.out
date;hostname;pwd

set -e
module load itk ants
img_fixed=$1
img_moving=$2

antsRegistration -o nonlin_warp_ -d 3 --float --use-histogram-matching -r [$img_fixed,$img_moving,1] -t Affine[0.01] -m MI[$img_fixed,$img_moving,1,100,Random,0.02] -c [500x500x50,1e-8,20] -f 3x2x1 -s 4x2x1vox -t SyN[0.25] -m CC[$img_fixed,$img_moving,1,4] -c [50x50x50,0,5] -f 4x2x1 -s 1x0.5x0vox -v 1

antsApplyTransforms -d 3 -i AAN_Brainstem_MNI152_1mm_v2p0.nii -r $img_moving -o AAN.nii.gz -n GenericLabel -t [nonlin_warp_0GenericAffine.mat,1] -t nonlin_warp_1InverseWarp.nii.gz
date
