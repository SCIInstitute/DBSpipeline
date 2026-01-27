#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=225gb
#SBATCH --time=20:00:00
#SBATCH --job-name=SCIRunS1
#SBATCH --mail-type=ALL
#SBATCH --output=SCIRunS1_%j.out
user=$(whoami)
#SBATCH --mail-user=${user}@ufl.edu

# example call
# sbatch --mail-user="user"@ufl.edu testSR.sh


module load python/3.10

#net=/blue/butsonc/Github/DBSpipeline/SRNetworks/test_file_outputs.srn5
profile=/blue/butsonc/Butson_Lab/Connectome/S1/ClinicalSimprofile.json

#python Python/SCIRun/RunSimulations.py -p $profile -n $net  -d

python Python/SCIRun/RunSimulations.py -p $profile  -d 

#python Python/SCIRun/RunSimulations.py -p $profile
