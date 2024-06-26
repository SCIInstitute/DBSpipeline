#!/bin/bash


Help()
{
   # Display Help
   echo
   echo "Syntax: scriptTemplate [-h|t|s]"
   echo "options:"
   echo "-h    Help "
   echo "-t    b0_to_T1 transfrom from slicer, must be .txt, pass as string"
   echo "-s    Freesurfer subject ID, pass as string"
   echo "Note: for use on system that has access to Freesurfer Subject Directory"
   echo
}


# Get the options
while getopts ":h:t:s:" option; do
   case $option in
      h) # display Help
         Help
         exit;;
      t) # Transform
         b0_trans=$OPTARG;;
      q) #FS recon all subject ID
         ID=$OPTARG;;
     \?) # Invalid option
         echo "Error: Invalid option"
         exit;;
   esac
done


mkdir gen_proc
transformconvert $b0_trans itk_import gen_proc/b0_to_T1_mrtrix.txt
cd gen_proc


#Five Tissue Type Generation
echo -e "\nFinding 5 tissue types in T1\n"
5ttgen -nocrop hsvs $SUBJECTS_DIR/$ID T1_5tt_FS.mif
echo -e "\nTransforming 5tt to b0 space\n"
mrtransform T1_5tt_FS.mif -linear b0_to_T1_mrtrix.txt -inverse -interp nearest T1_5tt_FS_b0space.mif

if [ -d "../Cleaned" ]
then
	echo -e "\nCleaned directory found\n"
else
	echo -e "\nCleaned directory not found, making one. Make sure to add these files to the ones from the preprocessing step\n"
	mkdir ../Cleaned
fi

echo -e "\nCopying files\n"
cp T1_5tt_FS_b0space.mif ../Cleaned/T1_5tt.mif
cd ..
echo -e "\n\nDone, ready for use in tckgen\n\n"

