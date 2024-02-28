#! /bin/sh
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=90gb
#SBATCH --time=6:00:00
#SBATCH --job-name=gpi_warp
#SBATCH --mail-type=ALL
#SBATCH --mail-user=mphook@ufl.edu
#SBATCH --output=ANTs_gpi_warp_%j.out
date;hostname;pwd

module load itk ants

antsRegistrationSyN.sh -d 3 -t s -n 8 -f $1 -m $2 -o gpi_warp_

date
