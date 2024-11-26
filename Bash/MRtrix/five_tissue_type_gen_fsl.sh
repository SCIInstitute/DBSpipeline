#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=16gb
#SBATCH --time=05:00:00
#SBATCH --job-name=five_t_t
#SBATCH --mail-type=ALL
#SBATCH --output=five_t_t_%j.out


Help()
{
   # Display Help
   echo
   echo "Syntax: scriptTemplate [-h|t]"
   echo "options:"
   echo "-h    Help "
   echo "-t    T1 image registered to b0, pass as  string"
   echo "Note: for use in HiPerGator Environment/SLURM"
   echo
}


# Get the options
while getopts ":h:q:t:" option; do
   case $option in
      h) # display Help
         Help
         exit;;
      t) # T1
         T1=$OPTARG;;
      q) #test
         greeting=$OPTARG;;
     \?) # Invalid option
         echo "Error: Invalid option"
         exit;;
   esac
done

module load fsl
module load mrtrix

mkdir gen_proc
cp $T1 gen_proc/T1_in_b0space.nii.gz
cd gen_proc
mrconvert T1_in_b0space.nii.gz T1_in_b0space.mif

#Five Tissue Type Generation
echo -e "\nFinding 5 tissue types in T1\n"
5ttgen fsl T1_in_b0space.mif T1_5tt.mif
echo -e "\nGenerating GM/WM interface\n"
5tt2gmwmi T1_5tt.mif gmwmSeed.mif

if [ -d "../Cleaned" ]
then
	echo -e "\nCleaned directory found\n"
else
	echo -e "\nCleaned directory not found, making one. Make sure to add these files to the ones from the preprocessing step\n"
	mkdir ../Cleaned
fi

echo -e "\nCopying files\n"
cp T1_5tt.mif ../Cleaned/T1_5tt.mif
cp gmwmSeed.mif ../Cleaned/gmwmSeed.mif
cd ..
echo -e "\n\nDone, ready for use in tckgen\n\n"

