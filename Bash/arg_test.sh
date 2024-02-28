#!/bin/bash

Help()
{
   # Display Help
   echo
   echo
   echo "Options:"
   echo
   echo "-h    Help "
   echo "Required:"
   echo "-T    T1 in ACPC space"
   echo "-w    WMnulled/FGATIR in ACPC space"
   echo "-u    DWI_up"
   echo "-l    bval *Required"
   echo "-c    bvec *Required"
   echo
   echo "Optional"
   echo "-d    DWI_down"
   echo "-t    T2 in ACPC space"
   echo "-F    FLAIR in ACPC space (only give one)"
   echo "-f    Freesurfer Subject ID"
   echo "-s    Use in Slurm/HiPerGator (y)"
   echo
   echo
}

while getopts ":h:T:t:F:w:u:d:l:c:f:s:" option; do
    case $option in
	T) T1=$OPTARG;;
	t) T2=$OPTARG;;
	F) FLAIR=$OPTARG;;
	w) WM=$OPTARG;;
	u) DWI_up=$OPTARG;;
	d) DWI_down=$OPTARG;;
	l) bval=$OPTARG;;
	f) FSID=$OPTARG;;
	s) slurm=$OPTARG;;
	h | * | :) Help && exit;;
    esac
done

if [ -z "$T1" ]
then
	echo -e "\nT1 Required\n"
	Help && exit 1;;
else
	echo "T1: $T1"
fi

if [ -z "$WM" ]
then
	echo -e "\nWMnulled or FGATIR Required\n"
	Help && exit 1;;
else
	echo "WM: $WM"
fi

if [ -z "$DWI_up" ]
then
	echo -e "\nDWI Required"
	Help && exit 1;;
else
	echo "DWI: $DWI_up"
fi

if [ [-z "$bval" || -z "$bvec" ] ]
then
	echo -e "\nGradient Information Required\n"
	Help && exit 1;;
else
	echo "bval: $bval"
	echo "bvec: $bvec"
fi

if [ -z "$FLAIR" ]
then
	echo -e "No FLAIR Given"
else
	echo "FLAIR: $FLAIR"
fi

if [ -z "$T2" ]
then
	echo -e "No T2 Given"
else
	echo "T2: $T2"
fi

if [ [ -z "$T2" && -z "$FLAIR" ] ]
then
	echo "No secondary input for Freesurfer given, this may affect the quality"
else
	echo -e "Only give one secondary input for Freesurfer!\n"
	Help && exit 1;;
fi

if [-z "$DWI_down" ]
then
	echo "No DWI reverse direction given, this may affect results"
else
	echo "DWI Reverse: $DWI_down"
fi

if [ -z "$FSID" ]
then
	echo "Freesurfer will not be run"
else
	echo "Freesurfer Subject ID: "$FSID"
fi