#! /bin/sh
# add in SLURM scheduler info
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32gb
#SBATCH --time=12:00:00
#SBATCH --job-name=freesurf_recon_all
#SBATCH --mail-type=ALL
#SBATCH --mail-user=mphook@ufl.edu
#SBATCH --output=recon_all_%j.out



module load freesurfer/7.2.0

#SUBJECTS_DIR=/home/mphook/blue_butsonc/mphook/freesurfer/SimNIBS/FS_Subjects
SUBJECTS_DIR=$PWD
set -e
recon-all -s $1 -i $2 -all -parallel -openmp 8 -FLAIR $3 -FLAIRpial

mv $1 /home/mphook/blue_butsonc/mphook/freesurfer/SimNIBS/FS_Subjects